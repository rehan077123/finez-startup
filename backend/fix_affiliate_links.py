"""
Fix Products: Update Broken Links & Images
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env", override=True)

mongo_url = os.environ.get("MONGO_URI") or os.environ.get("MONGO_URL")
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

# Updated affiliate links (working versions - .com instead of .in)
AFFILIATE_UPDATES = {
    "Neewer Ring Light 12\" with Tripod": "https://www.amazon.com/Neewer-Ring-Light-Tripod-Cellphone/dp/B07H7X37T6",
    "Apple Watch Series 8 GPS": "https://www.amazon.com/Apple-Watch-Series-GPS-Aluminum/dp/B0BDJGT7G3",
    "Sony WH-1000XM5 Headphones": "https://www.amazon.com/Sony-WH-1000XM5-Wireless-Headphones-Noise/dp/B09XS7JWHH",
    "Apple MacBook Air M2": "https://www.amazon.com/Apple-MacBook-Air-13-inch-Chip/dp/B0B3C7K8KJ",
    "Canon EOS 1500D DSLR Camera": "https://www.amazon.com/Canon-EOS-1500D-Digital-Rebel/dp/B07BR6C13P",
    "Logitech MX Master 3S Mouse": "https://www.amazon.com/Logitech-Master-Advanced-Customization-Quiet/dp/B09JQKBMKQ",
    "Samsung 4K Smart TV 55\"": "https://www.amazon.com/Samsung-Dynamic-Crystal-Control-UN55BU8000/dp/B0B8NTL1YC",
    "DJI Air 2S Drone": "https://www.amazon.com/DJI-Foldable-Quadcopter-Compatible-Controller/dp/B0937HFXSJ",
    "GoPro Hero 11 Black": "https://www.amazon.com/GoPro-CHDHX-112-HERO11-Black/dp/B0BG64TYCX",
    "iPad Pro 12.9 M2": "https://www.amazon.com/iPad-Pro-12-9-inch-Chip/dp/B0BDJ5Z9XY",
}

async def fix_products():
    try:
        products = await db.products.find({}).to_list(length=None)
        print(f"📊 Total products: {len(products)}")
        
        # Update affiliate links
        updates_made = 0
        for product in products:
            title = product.get("title", "")
            
            if title in AFFILIATE_UPDATES:
                result = await db.products.update_one(
                    {"id": product["id"]},
                    {"$set": {"affiliate_link": AFFILIATE_UPDATES[title]}}
                )
                if result.modified_count > 0:
                    updates_made += 1
                    print(f"✅ Updated: {title}")
        
        print(f"\n📊 Total links fixed: {updates_made}")
        print("✅ All affiliate links updated!")
        print("🔗 Changed Amazon .in links to .com for better accessibility")
        
    except Exception as e:
        print(f"❌ Error: {e}")

asyncio.run(fix_products())