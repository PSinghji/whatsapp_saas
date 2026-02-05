from fastapi import APIRouter, Depends, HTTPException
from ...core.database import get_database
from ...services.billing import BillingService
from ...services.whatsapp.python_bridge import WhatsAppPythonBridge
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/send")
async def send_single_message(user_id: str, device_id: str, phone: str, message: str):
    db = get_database()
    
    # 1. Check credits
    success, msg = await BillingService.deduct_credits(user_id, 1.0, f"Message to {phone}")
    if not success:
        raise HTTPException(status_code=402, detail=msg)
    
    # 2. Get device
    device = await db.devices.find_one({"_id": ObjectId(device_id)})
    if not device or device["status"] != "connected":
        # Refund credits if device is not ready
        await BillingService.add_credits(user_id, 1.0, "Refund: Device not connected")
        raise HTTPException(status_code=400, detail="Device not connected")
    
    # 3. Log message
    message_doc = {
        "user_id": user_id,
        "device_id": device_id,
        "phone": phone,
        "content": message,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    result = await db.messages.insert_one(message_doc)
    
    # 4. Trigger background sending (Conceptual)
    # In real app, use Celery: send_whatsapp_message.delay(str(result.inserted_id))
    
    return {"message_id": str(result.inserted_id), "status": "queued"}
