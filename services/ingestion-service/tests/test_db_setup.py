from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from src.database import engine 

def verify_production_config():
    print("--- 🩺 Testing Connection via database.py ---")
    
    try:
        with engine.connect() as conn:
            # 1. Test basic heartbeat
            result = conn.execute(text("SELECT now();"))
            server_time = result.fetchone()[0]
            
            print(f"✅ Success! Connected to: {engine.url.host}")
            print(f"✅ Database Server Time: {server_time}")

            # 2. Check 'raw' schema
            schema_check = conn.execute(text("""
                SELECT schema_name FROM information_schema.schemata 
                WHERE schema_name = 'raw';
            """))
            
            if schema_check.fetchone():
                print("✅ Schema 'raw' already exists.")
            else:
                print("💡 'raw' schema not found yet. Ready for DDL migration.")

    except SQLAlchemyError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nCheck your .env file and ensure database.py is loading it correctly.")

if __name__ == "__main__":
    verify_production_config()