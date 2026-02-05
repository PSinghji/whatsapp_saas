from fastapi import APIRouter, Depends
from ...core.database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/tickets")
async def create_ticket(user_id: str, subject: str, message: str, category: str):
    db = get_database()
    ticket = {
        "user_id": user_id,
        "subject": subject,
        "category": category,
        "status": "open",
        "priority": "medium",
        "messages": [{
            "sender": "user",
            "text": message,
            "timestamp": datetime.utcnow()
        }],
        "created_at": datetime.utcnow()
    }
    result = await db.tickets.insert_one(ticket)
    return {"ticket_id": str(result.inserted_id)}

@router.get("/tickets/{user_id}")
async def list_user_tickets(user_id: str):
    db = get_database()
    cursor = db.tickets.find({"user_id": user_id})
    tickets = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        tickets.append(doc)
    return tickets
