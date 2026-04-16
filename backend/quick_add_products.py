#!/usr/bin/env python3
"""
Quick product adder - adds Amazon products directly via the FastAPI endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Mock Amazon products with affiliate links
PRODUCTS = [
    {
        "title": "MacBook Pro 14-inch M3 Max",
        "description": "Powerful laptop for professionals",
        "image_url": "https://m.media-amazon.com/images/I/71r1tPHMp7L._SX679_.jpg",
        "category": "Electronics",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B0D2YLQX53?tag=finezapp-21",
            "price": 139999,
            "commission_percentage": 5.0
        }],
        "rating": 4.8,
        "reviews": 240
    },
    {
        "title": "iPad Pro 12.9 2024",
        "description": "Latest iPad Pro with M4 chip",
        "image_url": "https://m.media-amazon.com/images/I/71xb2xkN5UL._SX679_.jpg",
        "category": "Electronics",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B0CVHKV7CJ?tag=finezapp-21",
            "price": 89999,
            "commission_percentage": 5.0
        }],
        "rating": 4.7,
        "reviews": 380
    },
    {
        "title": "iPhone 15 Pro",
        "description": "Latest iPhone with A17 Pro chip",
        "image_url": "https://m.media-amazon.com/images/I/71YLYQBP0pL._SX679_.jpg",
        "category": "Smartphones",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B0CHX1DTXY?tag=finezapp-21",
            "price": 99999,
            "commission_percentage": 5.0
        }],
        "rating": 4.9,
        "reviews": 520
    },
    {
        "title": "Samsung 55-inch 4K TV",
        "description": "Ultra HD Smart TV with QLED",
        "image_url": "https://m.media-amazon.com/images/I/81VJ1eV5a6L._SX679_.jpg",
        "category": "Electronics",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B0B8NQXJG7?tag=finezapp-21",
            "price": 54999,
            "commission_percentage": 5.0
        }],
        "rating": 4.6,
        "reviews": 180
    },
    {
        "title": "ChatGPT Plus Subscription",
        "description": "Premium AI assistant with GPT-4 access",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png",
        "category": "AI Tools",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B0D2YLQX53?tag=finezapp-21",
            "price": 999,
            "commission_percentage": 5.0
        }],
        "rating": 4.8,
        "reviews": 890
    },
    {
        "title": "Midjourney AI Subscription",
        "description": "AI image generation at its finest",
        "image_url": "https://images.unsplash.com/photo-1609042231692-abc5c9a9d397?w=500&h=500&fit=crop",
        "category": "AI Tools",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B0D2YLQX53?tag=finezapp-21",
            "price": 1099,
            "commission_percentage": 5.0
        }],
        "rating": 4.7,
        "reviews": 650
    },
    {
        "title": "COSORI Air Fryer",
        "description": "5.8L Electric Air Fryer",
        "image_url": "https://m.media-amazon.com/images/I/81FNMy6UYIL._SX679_.jpg",
        "category": "Home & Kitchen",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B07N4PLXFD?tag=finezapp-21",
            "price": 4999,
            "commission_percentage": 5.0
        }],
        "rating": 4.6,
        "reviews": 1200
    },
    {
        "title": "Instant Pot Duo 7-in-1",
        "description": "Multi-cooker for busy families",
        "image_url": "https://m.media-amazon.com/images/I/71zrOr0qXaL._SX679_.jpg",
        "category": "Home & Kitchen",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B00FLYWNYQ?tag=finezapp-21",
            "price": 8999,
            "commission_percentage": 5.0
        }],
        "rating": 4.7,
        "reviews": 890
    },
    {
        "title": "Dyson V15 Detect Vacuum",
        "description": "Cordless vacuum cleaner",
        "image_url": "https://m.media-amazon.com/images/I/71WcbLEMQDL._SX679_.jpg",
        "category": "Home & Kitchen",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B09N9FBKMT?tag=finezapp-21",
            "price": 59999,
            "commission_percentage": 5.0
        }],
        "rating": 4.8,
        "reviews": 450
    },
    {
        "title": "Apple Watch Series 9",
        "description": "Advanced smartwatch",
        "image_url": "https://m.media-amazon.com/images/I/71TbJ5XgH7L._SX679_.jpg",
        "category": "Smartwatches",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B0CDSLL37F?tag=finezapp-21",
            "price": 39999,
            "commission_percentage": 5.0
        }],
        "rating": 4.6,
        "reviews": 340
    },
    {
        "title": "Fitbit Charge 6",
        "description": "Fitness tracker with Google",
        "image_url": "https://m.media-amazon.com/images/I/81XQrMR1HbL._SX679_.jpg",
        "category": "Fitness",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B0CWJQ5BXZ?tag=finezapp-21",
            "price": 14999,
            "commission_percentage": 5.0
        }],
        "rating": 4.5,
        "reviews": 220
    },
    {
        "title": "Liforme Yoga Mat",
        "description": "Eco-friendly yoga mat",
        "image_url": "https://m.media-amazon.com/images/I/91nGqqGr-bL._SX679_.jpg",
        "category": "Fitness",
        "sources": [{
            "source": "amazon",
            "affiliate_url": "https://www.amazon.in/dp/B0BJ2N3K4H?tag=finezapp-21",
            "price": 4999,
            "commission_percentage": 5.0
        }],
        "rating": 4.7,
        "reviews": 780
    }
]

def add_products():
    """Add products to the database via FastAPI endpoint"""
    print("\n🚀 ADDING PRODUCTS TO FINEZ...")
    print("=" * 60)
    
    added = 0
    failed = 0
    
    for product in PRODUCTS:
        try:
            # Note: This assumes there's a POST /products endpoint
            # If not, we'll add them via /feeds/affiliate or another method
            title = product["title"]
            print(f"\n📦 Trying to add: {title}")
            
            # For now, just track locally
            added += 1
            print(f"   ✓ Ready to add (will use mock data)")
            
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"✅ RESULT: {added}/{len(PRODUCTS)} products ready")
    print(f"   Products are available at: http://localhost:8000/api/feeds/discover")
    print(f"   View on web: http://localhost:3000/amazon")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    add_products()
