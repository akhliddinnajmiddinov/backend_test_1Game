from fastapi import FastAPI
from app.api.tournament import router as tournament_router
from app.db import get_db  # Import for dependency injection

app = FastAPI(
    title="Mini-Tournament System",
    description="A FastAPI-based API for managing tournaments and player registrations",
    version="0.1.0",
)

# Include the tournament router with prefix and tags
app.include_router(
    tournament_router,
    prefix="/tournaments",
    tags=["tournaments"],
)

@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint for the Tournament API.
    """
    return {"message": "Welcome to the Mini-Tournament System API"}