import asyncio
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from amazon_service import AmazonService

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

async def update_tags():
    """
    Update all Amazon affiliate links in the database to use the correct tag.
    """
    logger.info("Updating all Amazon links to use 'finezofficial-21'...")
    
    cursor = db.products.find({"asin": {"$exists": True, "$ne": None}})
    updated_count = 0
    
    async for product in cursor:
        asin = product.get("asin")
        if not asin:
            continue
            
        new_link = AmazonService.generate_affiliate_link(asin)
        
        # Check if update is needed
        if product.get("affiliateLink") != new_link or product.get("affiliate_link") != new_link:
            updates = {
                "affiliateLink": new_link,
                "affiliate_link": new_link
            }
            await db.products.update_one({"id": product["id"]}, {"$set": updates})
            updated_count += 1
            logger.info(f"Updated tag for ASIN: {asin}")

    logger.info(f"Update complete. Total products updated: {updated_count}")
    client.close()

if __name__ == "__main__":
    asyncio.run(update_tags())
