from fastapi import APIRouter, Depends
from ...core.database import get_database
from bson import ObjectId

router = APIRouter()

@router.get("/plans")
async def list_plans():
    db = get_database()
    cursor = db.subscriptions.find()
    plans = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        plans.append(doc)
    return plans

@router.post("/assign")
async def assign_plan(user_id: str, plan_id: str):
    db = get_database()
    plan = await db.subscriptions.find_one({"_id": ObjectId(plan_id)})
    if not plan:
        return {"error": "Plan not found"}
    
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "subscription_plan": plan["name"],
            "message_limit": plan["message_limit"],
            "device_limit": plan["device_limit"]
        }}
    )
    return {"status": "success"}
