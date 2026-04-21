import os
import csv
from database import engine
import hashlib

def get_file_hash(file_path):
    """Generates an MD5 hash of the file content."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        # Read in chunks to handle large files efficiently
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def should_process_file(cursor, filename, current_hash):
    """Checks if the file hash has changed since the last run."""
    cursor.execute("SELECT last_md5 FROM raw.file_registry WHERE filename = %s;", (filename,))
    result = cursor.fetchone()
    
    if result is None:
        return True # New file, never seen before
    
    return result[0] != current_hash # True if changed

def update_file_registry(cursor, filename, current_hash):
    """Updates the registry with the new hash after successful ingestion."""
    sql = """
        INSERT INTO raw.file_registry (filename, last_md5, processed_at)
        VALUES (%s, %s, NOW())
        ON CONFLICT (filename) DO UPDATE SET 
            last_md5 = EXCLUDED.last_md5,
            processed_at = NOW();
    """
    cursor.execute(sql, (filename, current_hash))

def load_csvs_to_raw(csv_directory="/home/guest/clinical-rules-engine/data"):
    """
    Reads specific CSV files and streams them into the 'raw' schema tables.
    """
    # Map of filename -> target table in 'raw' schema
    file_map = {
        "patients.csv": "raw.patients",
        "diagnoses.csv": "raw.diagnoses",
        "labs.csv": "raw.labs",
        "encounters.csv": "raw.encounters"
    }

    # Get the raw psycopg2 connection from SQLAlchemy
    raw_conn = engine.raw_connection()
    
    try:
        with raw_conn.cursor() as cursor:
            for filename, table_name in file_map.items():
                file_path = os.path.join(csv_directory, filename)
                
                if not os.path.exists(file_path):
                    print(f"⚠️  Skipping: {filename} (File not found at {file_path})")
                    continue

                # 1. Generate current hash
                current_hash = get_file_hash(file_path)

                # 2. Skip if file hasn't changed
                if not should_process_file(cursor, filename, current_hash):
                    print(f"⏭️  Skipping {filename}: No changes detected.")
                    continue

                # 3: Process file
                print(f"🧹 Truncate {table_name} for new ingestion")
                cursor.execute(f"TRUNCATE TABLE {table_name}")

                print(f"📥 Loading {filename} into {table_name}...")

                # We open the file and use COPY command for high-speed ingestion
                with open(file_path, 'r', encoding='utf-8') as f:
                    # SQL for COPY: assumes CSV has a header
                    # We specify the columns explicitly to skip the 'ingested_at' default column
                    
                    # 1. Get headers from CSV to ensure alignment
                    header = f.readline().strip()
                    f.seek(0) # Reset to beginning for copy_expert
                    
                    copy_sql = f"""
                        COPY {table_name} ({header}) 
                        FROM STDIN 
                        WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');
                    """
                    
                    cursor.copy_expert(sql=copy_sql, file=f)
                
                # 4. Update registry so we don't process it again in 60 seconds
                update_file_registry(cursor, filename, current_hash)
                
                print(f"✅ Successfully loaded {filename}")

            # Commit all loads at once
            raw_conn.commit()
            print("\n🚀 All available CSVs have been pushed to the 'raw' schema.")

    except Exception as e:
        raw_conn.rollback()
        print(f"❌ Ingestion failed: {e}")
    finally:
        raw_conn.close()

if __name__ == "__main__":
    # Test it using a 'data' folder at the root
    load_csvs_to_raw()