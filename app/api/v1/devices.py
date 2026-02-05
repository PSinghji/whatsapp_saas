from fastapi import APIRouter, Depends, HTTPException
from ...core.database import get_database
from ...models.device import DeviceCreate, DeviceOut
from ...services.whatsapp.python_bridge import WhatsAppPythonBridge
import uuid
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=DeviceOut)
async def add_device(device_in: DeviceCreate):
    db = get_database()
    session_id = str(uuid.uuid4())
    device_dict = device_in.dict()
    device_dict["session_id"] = session_id
    device_dict["status"] = "disconnected"
    
    result = await db.devices.insert_one(device_dict)
    device_dict["_id"] = str(result.inserted_id)
    return device_dict

@router.get("/{device_id}/qr")
async def get_device_qr(device_id: str):
    db = get_database()
    device = await db.devices.find_one({"_id": ObjectId(device_id)})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    bridge = WhatsAppPythonBridge(device["session_id"])
    await bridge.start()
    qr_path = await bridge.get_qr()
    return {"qr_path": qr_path}

@router.get("/", response_model=list[DeviceOut])
async def list_devices(user_id: str):
    db = get_database()
    cursor = db.devices.find({"user_id": user_id})
    devices = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        devices.append(doc)
    return devices
