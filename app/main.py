from fastapi import FastAPI
from .core.config import settings
from .core.database import connect_to_mongo, close_mongo_connection
from .api.v1 import auth, users, devices, api_mgmt, subscriptions, billing, support, monitoring

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(users.router, prefix=settings.API_V1_STR + "/users", tags=["users"])
app.include_router(devices.router, prefix=settings.API_V1_STR + "/devices", tags=["devices"])
app.include_router(api_mgmt.router, prefix=settings.API_V1_STR + "/api-management", tags=["api-management"])
app.include_router(subscriptions.router, prefix=settings.API_V1_STR + "/subscriptions", tags=["subscriptions"])
app.include_router(billing.router, prefix=settings.API_V1_STR + "/billing", tags=["billing"])
app.include_router(support.router, prefix=settings.API_V1_STR + "/support", tags=["support"])
app.include_router(monitoring.router, prefix=settings.API_V1_STR + "/monitoring", tags=["monitoring"])
