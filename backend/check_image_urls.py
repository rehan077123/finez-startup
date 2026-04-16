import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

async def check_products():
    ROOT_DIR = Path('.')
    load_dotenv(ROOT_DIR / '.env')
    
    mongo_url = os.environ['MONGO_URI']
    DB_NAME = os.environ['DB_NAME']
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[DB_NAME]
    
    products = await db.products.find({}, {'_id': 0, 'id': 1, 'title': 1, 'image_url': 1}).limit(5).to_list(5)
    
    for p in products:
        print(f"Title: {p.get('title')}")
        print(f"Image URL: {p.get('image_url')}")
        print('---')

asyncio.run(check_products())
