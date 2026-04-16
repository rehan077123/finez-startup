import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Mapping of categories to good Unsplash images
CATEGORY_IMAGES = {
    'Tech': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=500&h=500&fit=crop',
    'AI Tools': 'https://images.unsplash.com/photo-1677442d019cecf3da310dd2daea6f7e?w=500&h=500&fit=crop',
    'Side Hustles': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=500&h=500&fit=crop',
    'Fashion': 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500&h=500&fit=crop',
    'Learn': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=500&h=500&fit=crop',
    'Fitness': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=500&h=500&fit=crop',
    'Home': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&h=500&fit=crop',
}

async def fix_images():
    ROOT_DIR = Path('.')
    load_dotenv(ROOT_DIR / '.env')
    
    mongo_url = os.environ['MONGO_URI']
    DB_NAME = os.environ['DB_NAME']
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[DB_NAME]
    
    # Get all products
    products = await db.products.find({}, {'_id': 0, 'id': 1, 'title': 1, 'category': 1, 'image_url': 1}).to_list(None)
    
    updated = 0
    for product in products:
        category = product.get('category', 'Tech')
        image_url = CATEGORY_IMAGES.get(category, CATEGORY_IMAGES['Tech'])
        
        # Update product with new image URL
        await db.products.update_one(
            {'id': product['id']},
            {'$set': {'image_url': image_url, 'image_small': image_url, 'image_full': image_url}}
        )
        updated += 1
        print(f"✓ {product['title']}: {image_url}")
    
    print(f'\n✅ Updated {updated} products with working images!')
    client.close()

asyncio.run(fix_images())
