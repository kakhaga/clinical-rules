from fastapi import APIRouter
from app.api.routes import patient, evaluation

# This is the master router for version 1 of your API
api_router = APIRouter()

# We "include" the patients router here. 
# The prefix means all patient URLs will start with /patients
api_router.include_router(
    patient.router, 
    prefix="/patients", 
    tags=["patients"]
)

# Later, you can add more like this:
api_router.include_router(
    evaluation.router, 
    prefix="/evaluation", 
    tags=["evaluation"]
)