import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def check_db():
    mongo_url = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME", "finez_db")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print(f"Checking products with type='affiliate' and verified=True...")
    count = await db.products.count_documents({"type": "affiliate", "verified": True})
    print(f"Total verified affiliate products: {count}")
    
    if count > 0:
        sample = await db.products.find_one({"type": "affiliate", "verified": True})
        print(f"Sample product category: '{sample.get('category')}'")
        print(f"Sample product type: '{sample.get('type')}'")
        
    categories = await db.products.distinct("category", {"type": "affiliate", "verified": True})
    print(f"Categories found in DB: {categories}")

if __name__ == "__main__":
    asyncio.run(check_db())
