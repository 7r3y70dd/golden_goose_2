from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.web.dashboard import get_dashboard_html

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_root():
    return get_dashboard_html()

@router.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard():
    return get_dashboard_html()

# Add this endpoint to fetch opportunities
@router.get("/api/opportunities")
async def get_opportunities():
    # Placeholder for actual implementation
    return {
        "opportunities": [],
        "status": "success",
        "message": "Data loaded successfully"
    }