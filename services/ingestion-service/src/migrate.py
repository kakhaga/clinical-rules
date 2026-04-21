import os
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database import engine

def run_migrations():
    # 1. Get the directory where THIS script lives (ingestion-service/src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Go up one level to 'ingestion-service' and then into 'migrations'
    migrations_dir = os.path.join(current_dir, "..", "migrations")
    
    # Standardize the path
    migrations_dir = os.path.normpath(migrations_dir)

    if not os.path.exists(migrations_dir):
        print(f"❌ Error: Migrations directory not found at {migrations_dir}")
        return

    files = sorted([f for f in os.listdir(migrations_dir) if f.endswith(".sql")])

    try:
        with engine.begin() as conn:  # 'begin' starts a transaction for the whole block
            for filename in files:
                file_path = os.path.join(migrations_dir, filename)
                with open(file_path, "r") as f:
                    sql_script = f.read()
                    # Execute each file within the same transaction
                    try:
                        conn.execute(text(sql_script))
                        print(f"✅ Executed: {filename}")
                    except SQLAlchemyError as sae:
                        raise SQLAlchemyError(f"\n❌ Error during migration in file {filename}:") from sae
                        
        print("🎉 All migrations committed successfully.")
    except Exception as e:
        print(f"🛑 Migration failed. All changes rolled back. Error: {e}")

if __name__ == "__main__":
    # Ensure we are in the right directory context
    run_migrations()