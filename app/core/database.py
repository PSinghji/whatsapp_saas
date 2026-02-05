from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.db = db.client[settings.DATABASE_NAME]
    # Create indexes
    await db.db.users.create_index("email", unique=True)
    await db.db.devices.create_index("session_id", unique=True)

async def close_mongo_connection():
    db.client.close()

def get_database():
    return db.db
