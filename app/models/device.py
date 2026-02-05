from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    user_id: str
    platform: str = "python"  # python, nodejs, go, dotnet
    status: str = "disconnected"  # connected, disconnected, connecting, banned
    health: str = "good"

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    status: Optional[str] = None
    health: Optional[str] = None
    last_connected: Optional[datetime] = None

class DeviceInDB(DeviceBase):
    id: str = Field(alias="_id")
    session_id: str
    qr_code: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_connected: Optional[datetime] = None

class DeviceOut(DeviceBase):
    id: str = Field(alias="_id")
    session_id: str
    created_at: datetime
    last_connected: Optional[datetime] = None
