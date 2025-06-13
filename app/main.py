from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.tournament import router as tournament_router

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

@app.get("/", include_in_schema=False)
async def root():
    """
    Root endpoint — redirect to Swagger docs.
    """
    return RedirectResponse(url="/docs", status_code=301)