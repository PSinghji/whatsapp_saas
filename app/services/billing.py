from ..core.database import get_database
from bson import ObjectId
from datetime import datetime

class BillingService:
    @staticmethod
    async def add_credits(user_id: str, amount: float, reason: str):
        db = get_database()
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"credits": amount}}
        )
        await db.credits_history.insert_one({
            "user_id": user_id,
            "amount": amount,
            "type": "credit",
            "reason": reason,
            "timestamp": datetime.utcnow()
        })

    @staticmethod
    async def deduct_credits(user_id: str, amount: float, reason: str):
        db = get_database()
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if user["credits"] < amount:
            return False, "Insufficient credits"
        
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"credits": -amount}}
        )
        await db.credits_history.insert_one({
            "user_id": user_id,
            "amount": -amount,
            "type": "debit",
            "reason": reason,
            "timestamp": datetime.utcnow()
        })
        return True, "Success"
