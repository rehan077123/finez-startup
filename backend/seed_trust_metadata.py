#!/usr/bin/env python3
"""
Seed existing products with trust confidence metadata.
This adds difficulty, ROI, setupTime, and earning potential fields based on product type.
"""

import asyncio
import os
from motor.motor_asyncio import AsyncClient
from datetime import datetime, timezone

# MongoDB connection
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL", "mongodb://localhost:27017")
DB_NAME = "finez_db"
COLLECTION_NAME = "products"

# Trust metadata patterns by category/type
METADATA_TEMPLATES = {
    "laptop": {
        "difficulty": "beginner",
        "roi": "high",
        "setupTime": "< 30 mins",
        "earning_potential": "₹5k-20k"
    },
    "camera": {
        "difficulty": "intermediate",
        "roi": "high",
        "setupTime": "1-3 days",
        "earning_potential": "₹10k-50k"
    },
    "course": {
        "difficulty": "intermediate",
        "roi": "high",
        "setupTime": "1-2 hours",
        "earning_potential": "₹500-5k"
    },
    "software": {
        "difficulty": "beginner",
        "roi": "medium",
        "setupTime": "< 30 mins",
        "earning_potential": "₹1k-10k"
    },
    "tools": {
        "difficulty": "beginner",
        "roi": "medium",
        "setupTime": "< 30 mins",
        "earning_potential": "₹1k-5k"
    },
    "dropshipping": {
        "difficulty": "advanced",
        "roi": "high",
        "setupTime": "1-3 days",
        "earning_potential": "₹10k-100k"
    },
    "affiliate": {
        "difficulty": "intermediate",
        "roi": "medium",
        "setupTime": "1-2 hours",
        "earning_potential": "₹1k-10k"
    },
    "default": {
        "difficulty": "beginner",
        "roi": "medium",
        "setupTime": "1-2 hours",
        "earning_potential": "₹1k-5k"
    }
}


async def seed_metadata():
    """Add trust metadata to all products"""
    client = AsyncClient(MONGODB_ATLAS_URL)
    database = client[DB_NAME]
    collection = database[COLLECTION_NAME]

    try:
        # Find all products
        cursor = collection.find({})
        products = await cursor.to_list(length=None)
        
        print(f"Found {len(products)} products to update")
        
        count = 0
        for product in products:
            # Skip if already has metadata
            if product.get("difficulty"):
                print(f"Skipping {product.get('title', 'Unknown')} - already has metadata")
                continue
            
            # Determine template based on category or keywords
            template = METADATA_TEMPLATES["default"]
            
            category = (product.get("category", "") or "").lower()
            title = (product.get("title", "") or "").lower()
            description = (product.get("description", "") or "").lower()
            
            # Check category
            for key in METADATA_TEMPLATES:
                if key != "default" and (
                    key in category or 
                    key in title or
                    key in description
                ):
                    template = METADATA_TEMPLATES[key]
                    break
            
            # Update product
            result = await collection.update_one(
                {"_id": product["_id"]},
                {
                    "$set": {
                        **template,
                        "updated_at": datetime.now(timezone.utc)
                    }
                }
            )
            
            if result.modified_count > 0:
                count += 1
                print(f"✓ Updated: {product.get('title', 'Unknown')} → {template}")
            
        print(f"\n✅ Successfully updated {count} products with trust metadata!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_metadata())
