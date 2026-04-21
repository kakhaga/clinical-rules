import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables
load_dotenv()

print(os.getenv('DB_PORT'))

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Initialize engine
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    echo=os.getenv('DB_HOST') == "True" #TODO: change to False before git push
)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for orm models
Base = declarative_base()

# Helper function to generate database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()