from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database import engine

def get_core_schema_table_counts(conn):
    query = text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'core' 
        AND table_type = 'BASE TABLE';
    """)
    print(f"☑️ Table record counts in CORE: ")
    tables = conn.execute(query).fetchall()
    for table_row in tables:
        table_name = table_row[0]
        count_query = text(f'SELECT COUNT(*) FROM "core"."{table_name}";')
        result = conn.execute(count_query).scalar()
        print(f"📊 {table_name:20}: {result:,}")


def run_ingestion_etl():
    """
    Triggers the PostgreSQL stored procedure to move data from RAW to CORE.
    """
    print("🔄 Initializing ETL transformation...")

    try:
        # We use engine.begin() so the CALL and COMMIT are handled together
        with engine.begin() as conn:
            # 1. Execute the master controller procedure
            print("  ⏳ Calling core.run_full_etl()...")
            conn.execute(text("CALL core.run_full_etl();"))
            
            print("✅ ETL Procedure executed successfully.")

            # 2. Verify results (Quick count check)
            get_core_schema_table_counts(conn)

    except SQLAlchemyError as e:
        print(f"❌ ETL Failed!")
        print(f"Error Details: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_ingestion_etl()