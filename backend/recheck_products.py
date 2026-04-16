import asyncio
import os
import logging
from datetime import datetime, timezone
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

async def recheck_products():
    """
    Job to verify all Amazon products in the database.
    Removes products that are no longer available or have no valid offers.
    Updates price and images for available products.
    """
    logger.info("Starting 24-hour product recheck job...")
    
    # Find all products with an ASIN (Amazon products)
    cursor = db.products.find({"asin": {"$exists": True, "$ne": None}})
    
    total_checked = 0
    removed_count = 0
    updated_count = 0
    
    async for product in cursor:
        total_checked += 1
        asin = product.get("asin")
        if not asin:
            continue
            
        logger.info(f"Checking ASIN: {asin} ({product.get('title')})")
        
        # Verify availability using AmazonService
        result = AmazonService.verify_availability(asin)
        
        if not result["available"]:
            logger.info(f"Removing dead/unavailable product: {asin} - Reason: {result.get('reason')}")
            await db.products.delete_one({"id": product["id"]})
            removed_count += 1
        else:
            # Update product details if they changed
            updates = {
                "price": result["price"],
                "image": result["image"],
                "fullImage": result["fullImage"],
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Check if actual changes were made
            has_changes = (
                product.get("price") != result["price"] or
                product.get("image") != result["image"] or
                product.get("fullImage") != result["fullImage"]
            )
            
            if has_changes:
                await db.products.update_one({"id": product["id"]}, {"$set": updates})
                updated_count += 1
                logger.info(f"Updated price/image for ASIN: {asin}")

    logger.info(f"Recheck job complete.")
    logger.info(f"Total checked: {total_checked}")
    logger.info(f"Removed dead products: {removed_count}")
    logger.info(f"Updated products: {updated_count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(recheck_products())
