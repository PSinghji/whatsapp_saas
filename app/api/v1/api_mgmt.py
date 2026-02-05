from fastapi import APIRouter, Depends, HTTPException
import secrets
from ...core.database import get_database
from bson import ObjectId

router = APIRouter()

@router.post("/keys/generate")
async def generate_api_key(user_id: str):
    db = get_database()
    api_key = secrets.token_urlsafe(32)
    
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"api_key": api_key}}
    )
    return {"api_key": api_key}

@router.get("/keys/me")
async def get_my_api_key(user_id: str):
    db = get_database()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    return {"api_key": user.get("api_key")}
