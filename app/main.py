from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .core.config import settings
from .core.database import connect_to_mongo, close_mongo_connection
from .api.v1 import auth, users, devices, api_mgmt, subscriptions, billing, support, monitoring
import os

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Setup templates and static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# API Routes
app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(users.router, prefix=settings.API_V1_STR + "/users", tags=["users"])
app.include_router(devices.router, prefix=settings.API_V1_STR + "/devices", tags=["devices"])
app.include_router(api_mgmt.router, prefix=settings.API_V1_STR + "/api-management", tags=["api-management"])
app.include_router(subscriptions.router, prefix=settings.API_V1_STR + "/subscriptions", tags=["subscriptions"])
app.include_router(billing.router, prefix=settings.API_V1_STR + "/billing", tags=["billing"])
app.include_router(support.router, prefix=settings.API_V1_STR + "/support", tags=["support"])
app.include_router(monitoring.router, prefix=settings.API_V1_STR + "/monitoring", tags=["monitoring"])

# Frontend Routes
@app.get("/")
@app.get("/dashboard")
async def dashboard(request: Request):
    # Mock data for demonstration
    stats = {
        "credits": 1500.00,
        "active_devices": 3,
        "messages_sent": 12450
    }
    recent_logs = [
        {"time": "2026-02-05 10:30", "action": "Campaign 'Promo' Started", "status": "Success"},
        {"time": "2026-02-05 09:15", "action": "Device 'Pixel 6' Connected", "status": "Success"},
        {"time": "2026-02-04 18:45", "action": "API Key Generated", "status": "Success"},
    ]
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "active_page": "dashboard",
        "stats": stats,
        "recent_logs": recent_logs
    })

@app.get("/devices")
async def devices_page(request: Request):
    # Mock devices
    devices = [
        {"id": "1", "name": "Main Office", "session_id": "sess_001", "status": "connected"},
        {"id": "2", "name": "Support Line", "session_id": "sess_002", "status": "disconnected"},
    ]
    return templates.TemplateResponse("devices.html", {
        "request": request, 
        "active_page": "devices",
        "devices": devices
    })

@app.get("/campaigns")
async def campaigns_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, "active_page": "campaigns"})

@app.get("/billing")
async def billing_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, "active_page": "billing"})
