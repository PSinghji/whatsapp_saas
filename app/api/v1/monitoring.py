from fastapi import APIRouter
from ...core.database import get_database
import psutil

router = APIRouter()

@router.get("/health")
async def system_health():
    return {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "status": "healthy"
    }

@router.get("/logs/messages")
async def get_message_logs(limit: int = 100):
    db = get_database()
    cursor = db.messages.find().sort("created_at", -1).limit(limit)
    logs = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        logs.append(doc)
    return logs
