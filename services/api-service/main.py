import uvicorn
from app.core.config import settings
from fastapi import FastAPI
from app.api.router import api_router

# 1. This MUST be at the very edge of the file (no spaces/tabs before it)
app = FastAPI(title=settings.PROJECT_NAME)

# 2. This must also be at the top level
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    # 3. This block only runs when you call 'python main.py'
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=settings.APP_PORT, 
        reload=True
    )