import asyncio
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env", override=True)

# MongoDB connection
mongo_url = os.environ["MONGO_URI"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

async def update_iphone_image():
    new_image_url = "https://m.media-amazon.com/images/I/71657TiFeHL._SL1500_.jpg"
    
    # Search for product containing "iPhone 15"
    query = {"title": {"$regex": "iPhone 15", "$options": "i"}}
    
    product = await db.products.find_one(query)
    
    if not product:
        logger.error("iPhone 15 not found in the database!")
        return

    logger.info(f"Updating image for product: {product.get('title')}")
    
    updates = {
        "image": new_image_url,
        "fullImage": new_image_url,
        "image_url": new_image_url, # Compatibility
        "image_small": new_image_url, # Compatibility
        "image_full": new_image_url # Compatibility
    }
    
    result = await db.products.update_one({"id": product["id"]}, {"$set": updates})
    
    if result.modified_count > 0:
        logger.info("Successfully updated the image!")
    else:
        logger.info("No changes were made (image might already be set).")

    client.close()

if __name__ == "__main__":
    asyncio.run(update_iphone_image())
