from fastapi import APIRouter, Depends
from ...core.database import get_database
from ...services.billing import BillingService
from bson import ObjectId

router = APIRouter()

@router.get("/history/{user_id}")
async def get_billing_history(user_id: str):
    db = get_database()
    cursor = db.credits_history.find({"user_id": user_id}).sort("timestamp", -1)
    history = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        history.append(doc)
    return history

@router.post("/recharge")
async def recharge_wallet(user_id: str, amount: float):
    # In real app, integrate with payment gateway (Stripe/Razorpay)
    await BillingService.add_credits(user_id, amount, "Manual Recharge")
    return {"status": "success", "new_balance": "..."}
