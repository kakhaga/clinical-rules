from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. The Engine: The actual connection to the DB
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=settings.DB_LOGS == "True")

# 2. The SessionLocal: A factory for creating new session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Dependency to use in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()