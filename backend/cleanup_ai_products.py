"""
Clean up AI-generated products from the database.
Removes products with Unsplash URLs (stock photos) and keeps only:
- User-uploaded products
- Products with real affiliate links and real image URLs
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env", override=True)

mongo_url = os.environ.get("MONGO_URI") or os.environ.get("MONGO_URL")
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]


async def clean_ai_products():
    """Remove AI-generated products (those with Unsplash URLs)"""
    products_collection = db.products
    
    print("🔍 Scanning for AI-generated products...")
    
    # Find products with Unsplash URLs (these are AI-generated/stock photos)
    ai_products = await products_collection.find({
        "image_url": {"$regex": "unsplash.com"}
    }).to_list(length=None)
    
    print(f"Found {len(ai_products)} AI-generated products with Unsplash URLs")
    
    if ai_products:
        # Delete them
        delete_result = await products_collection.delete_many({
            "image_url": {"$regex": "unsplash.com"}
        })
        print(f"✅ Deleted {delete_result.deleted_count} AI-generated products")
    
    # Find all remaining products
    remaining = await products_collection.find({}).to_list(length=None)
    print(f"\n📊 Remaining products: {len(remaining)}")
    
    if remaining:
        print("\n✅ Remaining products:")
        for product in remaining:
            print(f"  - {product.get('title')} (from {product.get('seller_id', 'system')})")
    else:
        print("\n⚠️  No products remaining. You can upload your own products now!")


async def main():
    try:
        await clean_ai_products()
        print("\n✅ Cleanup complete!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
