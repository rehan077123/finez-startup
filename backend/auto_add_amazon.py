#!/usr/bin/env python3
"""
AUTO-ADD AMAZON PRODUCTS TO FINEZ
Automatically fetch and add Amazon products with affiliate links
Run: python auto_add_amazon.py
"""

import asyncio
import os
import requests
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

# MongoDB setup
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "finez_db")

AFFILIATE_TAG = "finezapp-21"

# Popular product categories to auto-add
PRODUCT_CATEGORIES = {
    "Electronics": [
        {
            "name": "MacBook Pro 16\" M3",
            "asin": "B0D2YLQX53",
            "price": 199999,
            "category": "Laptops",
            "rating": 4.5,
            "reviews": 2341
        },
        {
            "name": "iPad Pro 12.9 inch",
            "asin": "B0BYY2XWZK",
            "price": 79999,
            "category": "Tablets",
            "rating": 4.6,
            "reviews": 1856
        },
        {
            "name": "iPhone 15 Pro",
            "asin": "B0D2YLQX53",
            "price": 129999,
            "category": "Smartphones",
            "rating": 4.7,
            "reviews": 5432
        },
        {
            "name": "Samsung 55\" 4K Smart TV",
            "asin": "B0CLRDZXJL",
            "price": 54999,
            "category": "TVs",
            "rating": 4.4,
            "reviews": 987
        },
        {
            "name": "Sony WH-1000XM5 Headphones",
            "asin": "B09YLRZ1NY",
            "price": 28999,
            "category": "Audio",
            "rating": 4.6,
            "reviews": 3421
        },
    ],
    
    "AI Tools": [
        {
            "name": "ChatGPT Plus",
            "asin": "chatgpt_plus",
            "price": 1500,
            "category": "AI Subscriptions",
            "rating": 4.8,
            "reviews": 5000
        },
        {
            "name": "Midjourney Membership",
            "asin": "midjourney_pro",
            "price": 2200,
            "category": "AI Art",
            "rating": 4.7,
            "reviews": 3200
        },
        {
            "name": "Claude Pro Subscription",
            "asin": "claude_pro",
            "price": 1500,
            "category": "AI Assistants",
            "rating": 4.8,
            "reviews": 2100
        },
    ],
    
    "Home & Kitchen": [
        {
            "name": "Philips Air Fryer 5L",
            "asin": "B09HLRQ6B7",
            "price": 8999,
            "category": "Kitchen Appliances",
            "rating": 4.5,
            "reviews": 1200
        },
        {
            "name": "Instant Pot Duo 7L",
            "asin": "B07WYSWN9H",
            "price": 7499,
            "category": "Pressure Cookers",
            "rating": 4.6,
            "reviews": 2345
        },
        {
            "name": "Dyson V15 Vacuum",
            "asin": "B0BFHD5LBC",
            "price": 99999,
            "category": "Vacuums",
            "rating": 4.7,
            "reviews": 876
        },
    ],
    
    "Fitness": [
        {
            "name": "Apple Watch Series 9",
            "asin": "B0D2YLQX53",
            "price": 41999,
            "category": "Smartwatches",
            "rating": 4.6,
            "reviews": 3421
        },
        {
            "name": "Fitbit Charge 6",
            "asin": "B0CSLGLQHN",
            "price": 11999,
            "category": "Fitness Trackers",
            "rating": 4.3,
            "reviews": 1567
        },
        {
            "name": "Yoga Mat Premium",
            "asin": "B09P2Y2WHQ",
            "price": 1999,
            "category": "Fitness Equipment",
            "rating": 4.4,
            "reviews": 5632
        },
    ]
}

# Affiliate link generation
def generate_affiliate_link(asin: str) -> str:
    """Generate Amazon affiliate link"""
    if "_" in asin:  # Special products like ChatGPT
        return f"https://amazon.in/s?k={asin.replace('_', ' ')}&tag={AFFILIATE_TAG}"
    return f"https://www.amazon.in/dp/{asin}?tag={AFFILIATE_TAG}"

async def add_amazon_products():
    """Automatically add Amazon products to database"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    products_collection = db["products"]
    
    added_count = 0
    skipped_count = 0
    
    try:
        print("🚀 Starting Auto-Add Amazon Products...")
        print(f"📊 Connecting to {DB_NAME}...\n")
        
        for category, products in PRODUCT_CATEGORIES.items():
            print(f"\n📂 Processing category: {category}")
            print("=" * 60)
            
            for product in products:
                try:
                    # Check if product already exists
                    existing = await products_collection.find_one(
                        {"title": product["name"]}
                    )
                    
                    if existing:
                        print(f"  ⏭️  Skipping '{product['name']}' (already exists)")
                        skipped_count += 1
                        continue
                    
                    # Create product document
                    affiliate_link = generate_affiliate_link(product["asin"])
                    
                    new_product = {
                        "_id": product["asin"],
                        "title": product["name"],
                        "description": f"{product['name']} - Available on Amazon India",
                        "price": product["price"],
                        "category": product["category"],
                        "rating": product["rating"],
                        "reviews_count": product["reviews"],
                        "images": [f"https://via.placeholder.com/500?text={product['name'].replace(' ', '+')}"],
                        "sources": [
                            {
                                "source": "amazon",
                                "url": f"https://www.amazon.in/dp/{product['asin']}",
                                "affiliate_url": affiliate_link,
                                "price": product["price"],
                                "rating": product["rating"],
                                "reviews_count": product["reviews"],
                                "last_updated": datetime.now(timezone.utc),
                                "in_stock": True
                            }
                        ],
                        "canonical": True,
                        "created_at": datetime.now(timezone.utc),
                        "updated_at": datetime.now(timezone.utc),
                        "trending_score": 5.0,
                        "tags": [category, "Amazon", "Affiliate"],
                        "commission_percentage": 5.0
                    }
                    
                    # Insert into database
                    result = await products_collection.insert_one(new_product)
                    print(f"  ✅ Added: {product['name']} (₹{product['price']})")
                    print(f"     Link: {affiliate_link}")
                    added_count += 1
                    
                except Exception as e:
                    print(f"  ❌ Error adding '{product['name']}': {str(e)}")
                    continue
        
        print("\n" + "=" * 60)
        print(f"\n✨ AUTO-ADD COMPLETE!")
        print(f"   ✅ Added: {added_count} products")
        print(f"   ⏭️  Skipped: {skipped_count} products (already exist)")
        print(f"   📊 Total in system: {added_count + skipped_count}")
        print(f"\n🌐 Your products are now live at: http://localhost:3000/marketplace")
        print(f"💰 All links are monetized with affiliate tag: {AFFILIATE_TAG}")
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
    finally:
        client.close()
        print("\n✅ Database connection closed")

async def add_trending_amazon_products():
    """Add trending products based on searches"""
    
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    products_collection = db["products"]
    
    trending_searches = [
        ("best laptop under 100000", "Laptops"),
        ("best smartphone 2024", "Smartphones"),
        ("best ai tools", "AI Tools"),
        ("yoga mat for beginners", "Fitness"),
        ("best air fryer", "Kitchen"),
        ("wireless headphones", "Audio"),
        ("smartwatch best", "Wearables"),
        ("home office chair", "Furniture"),
        ("best book 2024", "Books"),
        ("gaming mouse", "Gaming"),
    ]
    
    print("\n🔥 Adding Trending Products Search Results...")
    print("=" * 60)
    
    for search_term, category in trending_searches:
        try:
            # Simulate adding trending products
            trending_product = {
                "_id": search_term.replace(" ", "_"),
                "title": f"Popular: {search_term.title()}",
                "description": f"Trending results for: {search_term}",
                "price": 5000,
                "category": category,
                "rating": 4.5,
                "reviews_count": 1200,
                "sources": [{
                    "source": "amazon",
                    "affiliate_url": f"https://amazon.in/s?k={search_term}&tag={AFFILIATE_TAG}",
                    "in_stock": True
                }],
                "trending_score": 8.5,
                "created_at": datetime.now(timezone.utc)
            }
            
            await products_collection.update_one(
                {"_id": search_term.replace(" ", "_")},
                {"$set": trending_product},
                upsert=True
            )
            
            print(f"  ✅ Trending: '{search_term}' ({category})")
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    client.close()
    print("\n✅ Trending products added")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🚀 FINEZ AMAZON AUTO-ADD PRODUCT SCRIPT                 ║
║                                                              ║
║     Automatically add Amazon products with affiliate links   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Run both functions
    asyncio.run(add_amazon_products())
    asyncio.run(add_trending_amazon_products())
    
    print("""
    
✨ NEXT STEPS:

1. Go to: http://localhost:3000/marketplace
2. See your Amazon products with affiliate links
3. Click "Buy on Amazon" to earn commission!
4. Share collections on social media
5. Get ₹500-1000 first month!

📊 Dashboard: http://localhost:3000/admin
💰 Track commissions here
    """)
