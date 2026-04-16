"""
Restore all original product images from add_category_products.py
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Import the original products data
import sys
sys.path.insert(0, str(Path(__file__).parent))
from add_category_products import PRODUCTS_BY_CATEGORY

async def restore_images():
    ROOT_DIR = Path('.')
    load_dotenv(ROOT_DIR / '.env')
    
    mongo_url = os.environ.get("MONGO_URI") or os.environ.get("MONGO_URL")
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ["DB_NAME"]]
    
    updated = 0
    
    # Flatten all products from categories
    for category, products in PRODUCTS_BY_CATEGORY.items():
        for product in products:
            # Find product by title and restore its image
            result = await db.products.update_one(
                {'title': product['title']},
                {'$set': {
                    'image_url': product['image_url'],
                    'image_small': product.get('image_small', product['image_url']),
                    'image_full': product.get('image_full', product['image_url']),
                }}
            )
            
            if result.matched_count > 0:
                updated += 1
                print(f"✓ Restored: {product['title']}")
    
    print(f'\n✅ Restored {updated} products with original images!')
    client.close()

asyncio.run(restore_images())
