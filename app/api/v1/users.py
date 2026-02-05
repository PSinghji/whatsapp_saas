from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ...core.database import get_database
from ...core import security
from ...models.user import UserCreate, UserOut, UserUpdate
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=UserOut)
async def create_user(user_in: UserCreate):
    db = get_database()
    existing_user = await db.users.find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_dict = user_in.dict()
    password = user_dict.pop("password")
    user_dict["hashed_password"] = security.get_password_hash(password)
    
    result = await db.users.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict

@router.get("/me", response_model=UserOut)
async def read_user_me(current_user: str = Depends(security.create_access_token)): # Simplified for now
    # In real implementation, use a dependency to get current user from token
    pass

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, user_in: UserUpdate):
    db = get_database()
    update_data = {k: v for k, v in user_in.dict().items() if v is not None}
    if "password" in update_data:
        update_data["hashed_password"] = security.get_password_hash(update_data.pop("password"))
    
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    user["_id"] = str(user["_id"])
    return user
