import asyncio
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env", override=True)

# MongoDB connection
mongo_url = os.environ["MONGO_URI"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

from amazon_service import AmazonService

# Your Amazon Affiliate Tag
AFFILIATE_TAG = "finezofficial-21"

# ==========================================================
# ADD YOUR PRODUCTS HERE
# Categories: 'Electronics', 'Beauty', 'Home Gadgets', 'Fashion', 'Fitness'
# ==========================================================
MY_MANUAL_PRODUCTS = [
    # Add your products here like this:
    # {
    #     "title": "Product Name",
    #     "category": "Electronics",
    #     "affiliate_link": "https://www.amazon.in/dp/ASIN",
    #     "image_url": "https://m.media-amazon.com/images/I/image.jpg",
    #     "price": 999.0,
    #     "benefits": "Description of benefits",
    #     "featured": True
    # },
]

async def add_manual_products():
    try:
        if not MY_MANUAL_PRODUCTS or MY_MANUAL_PRODUCTS[0]["title"] == "Example Product Name":
            print("Error: Please add your real products to the MY_MANUAL_PRODUCTS list first!")
            return

        print(f"Adding {len(MY_MANUAL_PRODUCTS)} products to the database...")
        
        products_to_insert = []
        for product_data in MY_MANUAL_PRODUCTS:
            raw_link = product_data.get("affiliate_link") or product_data.get("affiliateLink")
            asin = AmazonService.extract_asin(raw_link)
            
            if not asin:
                print(f"Skipping {product_data.get('title')}: Invalid Amazon URL")
                continue
                
            # Verify availability (optional, fallback to manual if fails)
            result = AmazonService.verify_availability(asin)
            
            if not result["available"]:
                print(f"Warning for {product_data.get('title')}: {result.get('reason')}. Using manual data.")
                # Ensure we have minimum data if scraper fails
                if not product_data.get("price") or not product_data.get("image_url"):
                    print(f"Skipping {product_data.get('title')}: Manual data incomplete (needs price and image_url)")
                    continue
                
                price = product_data.get("price")
                image = product_data.get("image_url")
                fullImage = product_data.get("image_url")
                title = product_data.get("title")
            else:
                price = result["price"]
                image = result["image"]
                fullImage = result["fullImage"]
                title = result.get("title") or product_data["title"]

            # Construct product according to the new exact system
            product_doc = {
                "id": str(uuid.uuid4()),
                "title": title,
                "category": product_data["category"],
                "asin": asin,
                "image": image,
                "fullImage": fullImage,
                "affiliateLink": AmazonService.generate_affiliate_link(asin),
                "benefits": product_data.get("benefits", ""),
                "price": price,
                "rating": product_data.get("rating", 4.8),
                "featured": product_data.get("featured", False),
                "clicks": 0,
                "review_count": 1200,
                "verified": True,
                "type": "affiliate",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Compatibility fields
            product_doc["affiliate_link"] = product_doc["affiliateLink"]
            product_doc["image_url"] = product_doc["image"]
            product_doc["image_small"] = product_doc["image"]
            product_doc["image_full"] = product_doc["fullImage"]
            product_doc["why_this_product"] = product_doc["benefits"]
            product_doc["description"] = product_doc["benefits"]
            
            products_to_insert.append(product_doc)
        
        if products_to_insert:
            await db.products.insert_many(products_to_insert)
            print(f"Successfully added {len(products_to_insert)} products with the new FineZ system!")
        else:
            print("No valid products were found to add.")

    except Exception as e:
        print(f"Error adding products: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(add_manual_products())
