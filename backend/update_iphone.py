import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def update_iphone():
    mongo_url = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME", "finez_db")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("Updating iPhone 15 category to 'Tech' and ensuring type is 'affiliate'...")
    result = await db.products.update_many(
        {"title": {"$regex": "iPhone 15", "$options": "i"}},
        {"$set": {"category": "Tech", "type": "affiliate", "verified": True}}
    )
    print(f"Updated {result.modified_count} products.")

if __name__ == "__main__":
    asyncio.run(update_iphone())
