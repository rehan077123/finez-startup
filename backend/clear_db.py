import asyncio
import os
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

async def clear_database():
    try:
        print("Starting full product and blog cleanup...")
        
        # Delete all products
        product_result = await db.products.delete_many({})
        print(f"Successfully deleted {product_result.deleted_count} products.")
        
        # Delete all blogs
        blog_result = await db.blogs.delete_many({})
        print(f"Successfully deleted {blog_result.deleted_count} blog posts.")
        
        # Optional: Clear categories/reviews if they exist
        if "reviews" in await db.list_collection_names():
            review_result = await db.reviews.delete_many({})
            print(f"Successfully deleted {review_result.deleted_count} reviews.")

        print("Cleanup complete. The marketplace is now empty.")

    except Exception as e:
        print(f"Error during cleanup: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(clear_database())
