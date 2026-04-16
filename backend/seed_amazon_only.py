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

AMAZON_ONLY_PRODUCTS = [
    # ========== ELECTRONICS (10) ==========
    {"title": "Sony WH-1000XM5 Headphones", "description": "Industry-leading wireless noise canceling headphones.", "price": 348.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Sony-WH-1000XM5-Canceling-Headphones-Hands-Free/dp/B09XS7JWHH", "image_url": ""},
    {"title": "Apple MacBook Air M3 (2024)", "description": "13-inch laptop with Apple M3 chip.", "price": 1099.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Apple-2024-MacBook-13-inch-Laptop/dp/B0CX2169S7", "image_url": ""},
    {"title": "Samsung Galaxy S24 Ultra", "description": "Flagship smartphone with AI and S Pen.", "price": 1299.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Samsung-Smartphone-Unlocked-Processor-Titanium/dp/B0CMDJ7Y4F", "image_url": ""},
    {"title": "Kindle Paperwhite (16 GB)", "description": "6.8\" display and adjustable warm light.", "price": 149.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Kindle-Paperwhite-16-GB-adjustable-warm/dp/B09TMN644Z", "image_url": ""},
    {"title": "Apple Watch Series 9", "description": "Smartwatch with advanced health sensors.", "price": 329.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Apple-Watch-Series-Smartwatch-Aluminum/dp/B0CHX698X3", "image_url": ""},
    {"title": "Bose QuietComfort Ultra", "description": "Bose's best noise canceling headphones.", "price": 429.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Bose-QuietComfort-Ultra-Bluetooth-Headphones/dp/B0CCZ26B5V", "image_url": ""},
    {"title": "Logitech MX Master 3S", "description": "Advanced wireless productivity mouse.", "price": 99.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Logitech-MX-Master-3S-Graphite/dp/B09HM94VPP", "image_url": ""},
    {"title": "Anker 737 Power Bank", "description": "24,000mAh portable charger with 140W.", "price": 149.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Anker-PowerBank-24-000mAh-Smart-Display/dp/B09VPHVT2Z", "image_url": ""},
    {"title": "DJI Mini 4 Pro Drone", "description": "Ultralight drone with 4K HDR video.", "price": 759.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/DJI-Mini-Pro-Remote-Control/dp/B0CHM6K6P3", "image_url": ""},
    {"title": "Nintendo Switch OLED Model", "description": "7-inch OLED screen gaming console.", "price": 349.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Nintendo-Switch-OLED-Model-Neon-Blue/dp/B098RL6SBJ", "image_url": ""},

    # ========== BEAUTY (10) ==========
    {"title": "COSRX Snail Mucin 96% Essence", "description": "Viral Korean skincare for skin repair.", "price": 14.50, "category": "Beauty", "affiliate_link": "https://www.amazon.com/COSRX-Repairing-Hydrating-Packaging-Calculated/dp/B00PBX3L7K", "image_url": ""},
    {"title": "Dyson Airwrap Multi-Styler", "description": "Luxury hair styling with Coanda airflow.", "price": 599.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Dyson-Airwrap-Multi-Styler-Complete-Nickel/dp/B0B5Z8R6S8", "image_url": ""},
    {"title": "Laneige Lip Sleeping Mask", "description": "Intensive lip treatment for hydration.", "price": 24.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/LANEIGE-Lip-Sleeping-Mask-Berry/dp/B099YMTN9L", "image_url": ""},
    {"title": "The Ordinary Niacinamide Serum", "description": "Vitamin and mineral blemish formula.", "price": 6.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Ordinary-Niacinamide-10-Zinc-1/dp/B06X9Z6KSM", "image_url": ""},
    {"title": "Olaplex No. 3 Hair Perfector", "description": "Repairs and strengthens hair from within.", "price": 30.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Olaplex-No-3-Hair-Perfector/dp/B0086OTU10", "image_url": ""},
    {"title": "Paula's Choice 2% BHA Exfoliant", "description": "Unclogs pores and evens skin tone.", "price": 34.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Paulas-Choice-SKIN-PERFECTING-Exfoliant-Blackheads/dp/B00949CT6C", "image_url": ""},
    {"title": "Revlon One-Step Dryer Brush", "description": "Hair dryer and volumizer in one tool.", "price": 39.99, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Revlon-One-Step-Dryer-Volumizer-Black/dp/B01LSUQSB0", "image_url": ""},
    {"title": "CeraVe Moisturizing Cream", "description": "Daily moisturizer for face and body.", "price": 17.78, "category": "Beauty", "affiliate_link": "https://www.amazon.com/CeraVe-Moisturizing-Cream-Daily-Moisturizer/dp/B00TTD9BRC", "image_url": ""},
    {"title": "Hero Cosmetics Mighty Patch", "description": "Hydrocolloid acne patches for healing.", "price": 12.99, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Hero-Cosmetics-Mighty-Patch-Original/dp/B074PVTPBW", "image_url": ""},
    {"title": "Sol de Janeiro Bum Bum Cream", "description": "Brazilian body cream with firming effect.", "price": 48.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Sol-Janeiro-Brazilian-Bum-Cream/dp/B013G679S0", "image_url": ""},

    # ========== HOME GADGETS (10) ==========
    {"title": "Fullstar Vegetable Chopper", "description": "Multi-blade kitchen time-saver.", "price": 24.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Fullstar-Vegetable-Chopper-Spiralizer-Cutter/dp/B0764HS4SL", "image_url": ""},
    {"title": "Ember Smart Mug 2", "description": "App-controlled coffee mug warmer.", "price": 129.95, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Ember-Temperature-Control-Smart-14-oz/dp/B07W9RL9MB", "image_url": ""},
    {"title": "Ninja AF101 Air Fryer", "description": "Crispy and healthy air frying results.", "price": 89.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Ninja-AF101-Fryer-Black-Gray/dp/B07FDJMC9Q", "image_url": ""},
    {"title": "Ring Video Doorbell", "description": "1080p HD smart doorbell security.", "price": 99.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Ring-Video-Doorbell-Satin-Nickel-2020-Release/dp/B08N5NQ869", "image_url": ""},
    {"title": "iRobot Roomba j7+ Vacuum", "description": "Self-emptying and smart navigation.", "price": 599.0, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/iRobot-Roomba-Self-Emptying-Robot-Vacuum/dp/B094NX6Z69", "image_url": ""},
    {"title": "Philips Hue Smart Bulb Kit", "description": "Color-changing LED smart lighting.", "price": 159.0, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Philips-Hue-White-Ambiance-Starter/dp/B073SSK6P8", "image_url": ""},
    {"title": "Instant Pot Duo 7-in-1", "description": "Pressure cooker and multi-cooker.", "price": 99.95, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Instant-Pot-Multi-Use-Programmable-Pressure/dp/B00FLYWNYQ", "image_url": ""},
    {"title": "Vitamix E310 Blender", "description": "High-performance professional blender.", "price": 349.95, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Vitamix-Explorian-Blender-Professional-Grade-Container/dp/B0758JHZM3", "image_url": ""},
    {"title": "Levoit Air Purifier", "description": "HEPA filter for home air quality.", "price": 99.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Levoit-Purifier-Home-Allergies-Pets/dp/B07VVK39F7", "image_url": ""},
    {"title": "Keurig K-Elite Maker", "description": "Single-serve coffee with strong setting.", "price": 149.0, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Keurig-K-Elite-Coffee-Maker-Single/dp/B078NPHS99", "image_url": ""},

    # ========== FASHION (10) ==========
    {"title": "Carhartt Men's K87 T-Shirt", "description": "Heavyweight cotton pocket t-shirt.", "price": 19.99, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Carhartt-Mens-K87-Workwear-Pocket-T-Shirt/dp/B00029PGEU", "image_url": ""},
    {"title": "Levi's 501 Original Jeans", "description": "Straight fit classic blue jeans.", "price": 59.50, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Levis-Mens-501-Original-Jeans/dp/B0018ON274", "image_url": ""},
    {"title": "Nike Air Force 1 Sneakers", "description": "Iconic low-top basketball shoes.", "price": 115.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/NIKE-Air-Force-Low-Mens/dp/B00186RER6", "image_url": ""},
    {"title": "Adidas Stan Smith Shoes", "description": "Classic minimalist tennis sneakers.", "price": 100.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/adidas-Originals-Smith-Sneaker-White/dp/B000Y17BFW", "image_url": ""},
    {"title": "Ray-Ban Wayfarer Sunglasses", "description": "Iconic frame with G-15 lenses.", "price": 171.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Ray-Ban-RB2140-Original-Wayfarer-Sunglasses/dp/B001GNBJQY", "image_url": ""},
    {"title": "Birkenstock Arizona Sandals", "description": "Comfortable cork footbed sandals.", "price": 110.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Birkenstock-Arizona-Soft-Footbed-Suede/dp/B002LZUE76", "image_url": ""},
    {"title": "North Face Borealis Pack", "description": "Durable and organized laptop bag.", "price": 99.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/THE-NORTH-FACE-Borealis-Backpack/dp/B092S6V6G2", "image_url": ""},
    {"title": "Fruit of the Loom Hoodies", "description": "Soft cotton-blend pullover hoodie.", "price": 18.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Fruit-Loom-Mens-Eversoft-Sweatshirts/dp/B076634C2K", "image_url": ""},
    {"title": "Champion Reverse Weave", "description": "Heavyweight durable athletic hoodie.", "price": 50.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Champion-Reverse-Weave-Hoodie-Oxford/dp/B0058X09VO", "image_url": ""},
    {"title": "Crocs Classic Clogs", "description": "Iconic lightweight comfort clogs.", "price": 49.99, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Crocs-Classic-Clog-White-Women/dp/B0014C5S7S", "image_url": ""},

    # ========== FITNESS (10) ==========
    {"title": "Renpho Smart Scale", "description": "Analyzes body fat and health metrics.", "price": 24.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/RENPHO-Bluetooth-Bathroom-Composition-Smartphone/dp/B01N1UX8RW", "image_url": ""},
    {"title": "Bowflex Dumbbells", "description": "Adjustable weights for home gyms.", "price": 429.0, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Bowflex-SelectTech-552-Adjustable-Dumbbells/dp/B001ARYU58", "image_url": ""},
    {"title": "Fitbit Charge 6", "description": "Health tracker with GPS and heart rate.", "price": 159.95, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Fitbit-Charge-Fitness-Tracker-Google/dp/B0C8V4C4D7", "image_url": ""},
    {"title": "Garmin Forerunner 255", "description": "Professional-grade running watch.", "price": 349.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Garmin-Forerunner-Running-Smartwatch-Advanced/dp/B09XF86Q6X", "image_url": ""},
    {"title": "Theragun Mini Massage", "description": "Deep muscle recovery massager.", "price": 199.0, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Theragun-Mini-Portable-Percussive-Therapy/dp/B0BHTMT81Y", "image_url": ""},
    {"title": "Hydro Flask 32oz", "description": "Insulated stainless steel bottle.", "price": 44.95, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Hydro-Flask-Wide-Mouth-Straw/dp/B083G9Y55N", "image_url": ""},
    {"title": "Manduka PRO Mat", "description": "Durable high-performance yoga mat.", "price": 129.0, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Manduka-PRO-Yoga-Mat-Black/dp/B00008I73T", "image_url": ""},
    {"title": "TRX Suspension Trainer", "description": "Bodyweight training system.", "price": 199.95, "category": "Fitness", "affiliate_link": "https://www.amazon.com/TRX-All-One-Suspension-Trainer/dp/B073XG8W1X", "image_url": ""},
    {"title": "BalanceFrom Dumbbells", "description": "Hex-shaped coated dumbbells set.", "price": 35.0, "category": "Fitness", "affiliate_link": "https://www.amazon.com/BalanceFrom-Dumbbell-Weights-Coated-Pounds/dp/B08NXYRDKP", "image_url": ""},
    {"title": "Iron Flask Sports Bottle", "description": "Triple-lid insulated water bottle.", "price": 24.95, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Iron-Flask-Sports-Water-Bottle/dp/B07N3S1K5W", "image_url": ""},
]

AFFILIATE_TAG = "finezofficial-21"

def apply_amazon_tag(link: str) -> str:
    if "amazon" in link.lower() and "tag=" not in link:
        sep = "&" if "?" in link else "?"
        return f"{link}{sep}tag={AFFILIATE_TAG}"
    return link

async def seed_amazon_only():
    try:
        print(f"Replacing database with {len(AMAZON_ONLY_PRODUCTS)} Amazon-only products...")
        
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
        print("Successfully seeded 50 Amazon-only products!")

    except Exception as e:
        print(f"Error seeding products: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_amazon_only())
