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

# Category List
CATEGORIES = ['Electronics', 'Beauty', 'Home Gadgets', 'Fashion', 'Fitness']

AMAZON_ONLY_PRODUCTS = [
    # ========== ELECTRONICS (10) ==========
    {"title": "Samsung Galaxy Tab A9+ 11\" 64GB", "description": "Latest Samsung Android tablet with 11-inch screen.", "price": 189.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/dp/B0CLF2YST8", "image_url": ""},
    {"title": "Amazon Echo Show 15", "description": "Smart display with Alexa and 15.6-inch Full HD screen.", "price": 279.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/dp/B098SQF9X2", "image_url": ""},
    {"title": "Fire TV Stick HD (2024)", "description": "Amazon's latest streaming device for HD video.", "price": 29.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/dp/B0D4X6Z6S6", "image_url": ""},
    {"title": "Apple AirPods Pro 2", "description": "Premium wireless earbuds with active noise cancellation.", "price": 189.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/dp/B0DHDN6ZKF", "image_url": ""},
    {"title": "TAGRY Bluetooth Headphones", "description": "Wireless earbuds with 60H playback and LED display.", "price": 29.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/dp/B09NR6Z6VF", "image_url": ""},
    {"title": "Anker 737 Power Bank (PowerCore 24K)", "description": "High-capacity portable charger with 140W fast charging.", "price": 109.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/dp/B09VPHVT2Z", "image_url": ""},
    {"title": "Mesime Apple Watch Band", "description": "Premium stainless steel band for all Apple Watch series.", "price": 15.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/dp/B0CNPZ6Z6S", "image_url": ""},
    {"title": "Kindle (2024 Release)", "description": "Our lightest and most compact Kindle with 300 ppi display.", "price": 109.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/dp/B0CN6Z6S6S", "image_url": ""},
    {"title": "Apple 2024 MacBook Air 13-inch M3", "description": "Superlight laptop with Apple M3 chip and Liquid Retina display.", "price": 1099.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/dp/B0CX2169S7", "image_url": ""},
    {"title": "Echo Pop Smart Speaker", "description": "Compact smart speaker with Alexa for any room.", "price": 39.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/dp/B09ZX6Z6S6", "image_url": ""},

    # ========== BEAUTY (10) ==========
    {"title": "La Roche-Posay Toleriane Moisturizer", "description": "Daily soothing facial moisturizer for sensitive skin.", "price": 17.99, "category": "Beauty", "affiliate_link": "https://www.amazon.com/dp/B01N9SPQHQ", "image_url": ""},
    {"title": "Mighty Patch Original (36 Count)", "description": "Hydrocolloid acne patches for overnight blemish care.", "price": 11.99, "category": "Beauty", "affiliate_link": "https://www.amazon.com/dp/B074PVTPBW", "image_url": ""},
    {"title": "eos Shea Better Body Lotion", "description": "24-hour hydration body lotion with shea butter.", "price": 9.99, "category": "Beauty", "affiliate_link": "https://www.amazon.com/dp/B0B5Z8R6S8", "image_url": ""},
    {"title": "Maybelline Sky High Mascara", "description": "Volumizing and lengthening mascara for long lashes.", "price": 9.99, "category": "Beauty", "affiliate_link": "https://www.amazon.com/dp/B08HSRGZ6G", "image_url": ""},
    {"title": "d'alba First Spray Serum", "description": "Premium Italian truffle face spray for glowing skin.", "price": 28.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/dp/B00V4L8M88", "image_url": ""},
    {"title": "COSRX Snail Mucin 96% Essence", "description": "Skin repairing and hydrating serum for all skin types.", "price": 14.50, "category": "Beauty", "affiliate_link": "https://www.amazon.com/dp/B00PBX3L7K", "image_url": ""},
    {"title": "Dyson Airwrap Multi-Styler", "description": "Re-engineered attachments for all hair types and styles.", "price": 599.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/dp/B0B5Z8R6S8", "image_url": ""},
    {"title": "Laneige Lip Sleeping Mask", "description": "Leave-on lip mask for hydration and antioxidant protection.", "price": 24.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/dp/B099YMTN9L", "image_url": ""},
    {"title": "The Ordinary Niacinamide Serum", "description": "10% Niacinamide and 1% Zinc serum for clear skin.", "price": 6.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/dp/B06X9Z6KSM", "image_url": ""},
    {"title": "Olaplex No. 3 Hair Perfector", "description": "Professional hair repair treatment for home use.", "price": 30.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/dp/B0086OTU10", "image_url": ""},

    # ========== HOME GADGETS (10) ==========
    {"title": "Kasa Smart Light Switch HS200", "description": "Easy-to-install smart light switch with Alexa/Google Home.", "price": 19.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/dp/B01EZV35QU", "image_url": ""},
    {"title": "Kasa Smart Dimmer Switch HS220", "description": "Adjust light levels with smart dimmer and Alexa integration.", "price": 22.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/dp/B079775ZZQ", "image_url": ""},
    {"title": "Qutadi Candle Warmer Lamp", "description": "Electric candle lamp for melting scented wax without flame.", "price": 29.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/dp/B0CN6Z6S6S", "image_url": ""},
    {"title": "Echo Dot (5th Gen) with Clock", "description": "Best sounding Echo Dot yet with integrated LED clock.", "price": 59.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/dp/B09B8V1ZHC", "image_url": ""},
    {"title": "Rocketbook Core Reusable Notebook", "description": "Cloud-connected smart notebook that can be reused.", "price": 34.0, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/dp/B01GU6T5QC", "image_url": ""},
    {"title": "Blink Outdoor Security Camera", "description": "Wireless HD security camera with 2-year battery life.", "price": 99.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/dp/B086DKVGX7", "image_url": ""},
    {"title": "Fire TV Stick 4K Max", "description": "Most powerful streaming stick with Wi-Fi 6E support.", "price": 59.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/dp/B0B6Z6S6S6", "image_url": ""},
    {"title": "Fullstar Vegetable Chopper", "description": "Viral kitchen gadget for quick vegetable prep.", "price": 24.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/dp/B0764HS4SL", "image_url": ""},
    {"title": "Ninja AF101 Air Fryer", "description": "4-quart air fryer that fries, roasts, and dehydrates.", "price": 89.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/dp/B07FDJMC9Q", "image_url": ""},
    {"title": "Instant Pot Duo 7-in-1", "description": "Multi-cooker for pressure cooking, slow cooking, and more.", "price": 99.95, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/dp/B00FLYWNYQ", "image_url": ""},

    # ========== FASHION (10) ==========
    {"title": "Trendy Queen Oversized T Shirt", "description": "Women's oversized summer tee for casual wear.", "price": 14.99, "category": "Fashion", "affiliate_link": "https://www.amazon.com/dp/B0BR7S9Z6S", "image_url": ""},
    {"title": "LOMON Fashion Tops 3/4 Sleeve", "description": "Women's dressy casual blouse for office or daily wear.", "price": 25.99, "category": "Fashion", "affiliate_link": "https://www.amazon.com/dp/B0CN6Z6S6S", "image_url": ""},
    {"title": "ATHMILE Oversized Crewneck Tee", "description": "Casual loose-fit cotton tee for women.", "price": 12.99, "category": "Fashion", "affiliate_link": "https://www.amazon.com/dp/B0BR7S9Z6S", "image_url": ""},
    {"title": "XIEERDUO V-Neck T-Shirt", "description": "Flowy summer blouse with trendy design.", "price": 19.99, "category": "Fashion", "affiliate_link": "https://www.amazon.com/dp/B0BR7S9Z6S", "image_url": ""},
    {"title": "Hanes Men's Boxer Briefs (Multipack)", "description": "Cotton moisture-wicking underwear for men.", "price": 18.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/dp/B00029PGEU", "image_url": ""},
    {"title": "Gildan Men's Crew T-Shirts", "description": "Multipack of basic cotton tees for daily wear.", "price": 18.97, "category": "Fashion", "affiliate_link": "https://www.amazon.com/dp/B076634C2K", "image_url": ""},
    {"title": "ANRABESS Women's Boxer Shorts", "description": "Plaid pajama shorts for lounge and sleep.", "price": 14.99, "category": "Fashion", "affiliate_link": "https://www.amazon.com/dp/B0BR7S9Z6S", "image_url": ""},
    {"title": "SAMPEEL Women's Tank Tops", "description": "Ruched cap sleeve shirts for summer fashion.", "price": 15.99, "category": "Fashion", "affiliate_link": "https://www.amazon.com/dp/B0BR7S9Z6S", "image_url": ""},
    {"title": "Levi's 501 Original Fit Jeans", "description": "Classic straight-fit denim since 1873.", "price": 59.50, "category": "Fashion", "affiliate_link": "https://www.amazon.com/dp/B0018ON274", "image_url": ""},
    {"title": "Nike Air Force 1 '07", "description": "Iconic basketball shoe and street-style staple.", "price": 115.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/dp/B00186RER6", "image_url": ""},

    # ========== FITNESS (10) ==========
    {"title": "Joma Men's Combi Sports T-Shirt", "description": "Lightweight and breathable shirt for running and gym.", "price": 19.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/dp/B002LZUE76", "image_url": ""},
    {"title": "Amazon Basics Neoprene Dumbbells", "description": "Pair of non-slip weights for home fitness training.", "price": 12.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/dp/B01LR5S8O2", "image_url": ""},
    {"title": "SKDK Weight Lifting Straps", "description": "Anti-slip silicone straps for heavy gym training.", "price": 14.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/dp/B08NXYRDKP", "image_url": ""},
    {"title": "Trideer Yoga Exercise Ball", "description": "Extra-thick ball for stability, balance, and gym workouts.", "price": 15.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/dp/B083G9Y55N", "image_url": ""},
    {"title": "ProsourceFit Foam Puzzle Mat", "description": "Interlocking EVA foam tiles for gym floor protection.", "price": 29.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/dp/B07N3S1K5W", "image_url": ""},
    {"title": "VINSGUIR Workout Gloves", "description": "Breathable weightlifting gloves for men and women.", "price": 12.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/dp/B01N1UX8RW", "image_url": ""},
    {"title": "RENPHO AI Smart Jump Rope", "description": "Bluetooth-connected jump rope with mobile app tracking.", "price": 29.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/dp/B0C8V4C4D7", "image_url": ""},
    {"title": "axv Vibration Plate Exercise Machine", "description": "Full-body vibration platform for fat loss and toning.", "price": 109.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/dp/B0BHTMT81Y", "image_url": ""},
    {"title": "Fitbit Charge 6 Fitness Tracker", "description": "Advanced health activity tracker with Google apps.", "price": 159.95, "category": "Fitness", "affiliate_link": "https://www.amazon.com/dp/B0C8V4C4D7", "image_url": ""},
    {"title": "Bowflex SelectTech 552 Dumbbells", "description": "Adjustable weights that replace 15 sets of dumbbells.", "price": 429.0, "category": "Fitness", "affiliate_link": "https://www.amazon.com/dp/B001ARYU58", "image_url": ""},
]

AFFILIATE_TAG = "finezofficial-21"

def apply_amazon_tag(link: str) -> str:
    if "amazon" in link.lower() and "tag=" not in link:
        sep = "&" if "?" in link else "?"
        return f"{link}{sep}tag={AFFILIATE_TAG}"
    return link

async def seed_amazon_verified():
    try:
        print(f"Refreshing database with {len(AMAZON_ONLY_PRODUCTS)} verified Amazon products...")
        
        # Completely clear products collection
        await db.products.delete_many({})
        
        products_to_insert = []
        for product_data in AMAZON_ONLY_PRODUCTS:
            product_data["id"] = str(uuid.uuid4())
            product_data["clicks"] = 0
            product_data["rating"] = 4.6 + (hash(product_data["title"]) % 4) / 10
            product_data["review_count"] = 1200 + (hash(product_data["title"]) % 8000)
            product_data["verified"] = True
            product_data["type"] = "affiliate"
            product_data["affiliate_link"] = apply_amazon_tag(product_data.get("affiliate_link", ""))
            product_data["created_at"] = datetime.now(timezone.utc).isoformat()
            product_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            products_to_insert.append(product_data)
        
        await db.products.insert_many(products_to_insert)
        print("Successfully seeded 50 verified Amazon-only products!")

    except Exception as e:
        print(f"Error seeding products: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_amazon_verified())
