import asyncio
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

# MongoDB connection
mongo_url = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME", "finez_db")
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

AFFILIATE_TAG = "finezofficial-21"

def get_amazon_link(asin):
    return f"https://www.amazon.in/dp/{asin}?tag={AFFILIATE_TAG}"

AMAZON_PRODUCTS = [
    # ========== ELECTRONICS ==========
    {"title": "Sony WH-1000XM5 Noise Cancelling Headphones", "price": 29990, "category": "Electronics", "asin": "B09XS7JWHH", "img": "https://m.media-amazon.com/images/I/61+7y9To9vL._SL1500_.jpg", "why": "Industry-leading noise cancellation"},
    {"title": "Apple AirPods Pro (2nd Gen)", "price": 24900, "category": "Electronics", "asin": "B0BDHWDR12", "img": "https://m.media-amazon.com/images/I/61f1YfTQ9pL._SL1500_.jpg", "why": "Perfect for iPhone users"},
    {"title": "Logitech MX Master 3S Wireless Mouse", "price": 9495, "category": "Electronics", "asin": "B0B11S6YNF", "img": "https://m.media-amazon.com/images/I/61ni3t1ryQL._SL1500_.jpg", "why": "The ultimate productivity tool"},
    {"title": "SanDisk 1TB Extreme Portable SSD", "price": 8999, "category": "Electronics", "asin": "B08GTYFC37", "img": "https://m.media-amazon.com/images/I/712vS6+392L._SL1500_.jpg", "why": "Fast, rugged storage for creators"},
    {"title": "TP-Link AX3000 Wi-Fi 6 Router", "price": 5499, "category": "Electronics", "asin": "B085Z35GY6", "img": "https://m.media-amazon.com/images/I/51Zp0pxvXWL._SL1500_.jpg", "why": "Blazing fast internet speeds"},
    {"title": "Samsung 27-inch Curved Gaming Monitor", "price": 15999, "category": "Electronics", "asin": "B08J82K4S1", "img": "https://m.media-amazon.com/images/I/81m6-9ubYML._SL1500_.jpg", "why": "Immersive 144Hz gaming experience"},
    {"title": "Boat Rockerz 450 Bluetooth Headphones", "price": 1499, "category": "Electronics", "asin": "B07PR1CL3S", "img": "https://m.media-amazon.com/images/I/51mCH6-AnDL._SL1500_.jpg", "why": "Best budget wireless headphones"},
    {"title": "Realme Buds 2 Wired Earphones", "price": 599, "category": "Electronics", "asin": "B07X96XDFG", "img": "https://m.media-amazon.com/images/I/61+7y9To9vL._SL1500_.jpg", "why": "Superior sound at an amazing price"},

    # ========== MOBILE & LAPTOPS ==========
    {"title": "iPhone 15 Pro Max (256 GB)", "price": 148900, "category": "Mobile", "asin": "B0CHX1W1XY", "img": "https://m.media-amazon.com/images/I/81+GIkwqLIL._SL1500_.jpg", "why": "The most powerful iPhone ever"},
    {"title": "Samsung Galaxy S24 Ultra", "price": 129999, "category": "Mobile", "asin": "B0CS69S9RC", "img": "https://m.media-amazon.com/images/I/71R6BD6e8dL._SL1500_.jpg", "why": "AI-powered flagship with S Pen"},
    {"title": "OnePlus 12 5G", "price": 64999, "category": "Mobile", "asin": "B0CX5Z9X9X", "img": "https://m.media-amazon.com/images/I/71f5Eu5lJSL._SL1500_.jpg", "why": "Fast charging and smooth performance"},
    {"title": "MacBook Air M3 Laptop", "price": 114900, "category": "Laptops", "asin": "B0CM5L9Z9X", "img": "https://m.media-amazon.com/images/I/71f5Eu5lJSL._SL1500_.jpg", "why": "Incredibly thin and powerful"},
    {"title": "ASUS ROG Zephyrus G14", "price": 144990, "category": "Laptops", "asin": "B0C469STTM", "img": "https://m.media-amazon.com/images/I/718f-lC5TdL._SL1500_.jpg", "why": "Powerful 14-inch gaming laptop"},
    {"title": "HP Victus Gaming Laptop", "price": 68990, "category": "Laptops", "asin": "B0C2D1RLSR", "img": "https://m.media-amazon.com/images/I/81m6-9ubYML._SL1500_.jpg", "why": "Great performance for the price"},

    # ========== FASHION ==========
    {"title": "Nike Air Zoom Pegasus 40", "price": 10495, "category": "Fashion", "asin": "B0BZL7V86M", "img": "https://m.media-amazon.com/images/I/71A9B6Lz4kL._SL1500_.jpg", "why": "Reliable daily running shoes"},
    {"title": "Casio G-Shock GA-2100", "price": 8995, "category": "Fashion", "asin": "B09G9D8KRQ", "img": "https://m.media-amazon.com/images/I/61GLMJ7TQiL._SL1500_.jpg", "why": "Indestructible and stylish watch"},
    {"title": "Levis Men's 511 Slim Fit Jeans", "price": 2499, "category": "Fashion", "asin": "B07WNV1X9X", "img": "https://m.media-amazon.com/images/I/81m6-9ubYML._SL1500_.jpg", "why": "Classic slim fit denim"},
    {"title": "Ray-Ban Classic Wayfarer", "price": 12990, "category": "Fashion", "asin": "B001GNBJQY", "img": "https://m.media-amazon.com/images/I/51fSAn6vSXL._SL1000_.jpg", "why": "Timeless iconic sunglasses"},
    {"title": "Puma Men's Smash v2 Sneakers", "price": 2499, "category": "Fashion", "asin": "B07D9C9X9X", "img": "https://m.media-amazon.com/images/I/61ni3t1ryQL._SL1500_.jpg", "why": "Versatile and comfortable sneakers"},

    # ========== HOME & KITCHEN ==========
    {"title": "Philips Air Fryer XL", "price": 14999, "category": "Home", "asin": "B09BTX1X9X", "img": "https://m.media-amazon.com/images/I/71pCO76IDXL._SL1500_.jpg", "why": "Cook with 90% less fat"},
    {"title": "Eureka Forbes Vacuum Cleaner", "price": 8499, "category": "Home", "asin": "B08CR1X9X9", "img": "https://m.media-amazon.com/images/I/61ni3t1ryQL._SL1500_.jpg", "why": "Keep your home dust-free"},
    {"title": "Prestige Induction Cooktop", "price": 2899, "category": "Home", "asin": "B006361X9X", "img": "https://m.media-amazon.com/images/I/71pCO76IDXL._SL1500_.jpg", "why": "Fast and safe cooking for everyone"},
    {"title": "Amazon Basics Microfiber Bed Sheet", "price": 899, "category": "Home", "asin": "B00NLLUMX8", "img": "https://m.media-amazon.com/images/I/71R6BD6e8dL._SL1500_.jpg", "why": "Soft and durable bedding"},
    {"title": "Wipro Smart LED Bulb 9W", "price": 499, "category": "Home", "asin": "B07Z96XDFG", "img": "https://m.media-amazon.com/images/I/61ni3t1ryQL._SL1500_.jpg", "why": "Control your lights with your phone"},

    # ========== FITNESS ==========
    {"title": "Apple Watch Series 9", "price": 41900, "category": "Fitness", "asin": "B0CHX8X9X9", "img": "https://m.media-amazon.com/images/I/71f5Eu5lJSL._SL1500_.jpg", "why": "Advanced health and fitness tracking"},
    {"title": "Optimum Nutrition Whey Protein", "price": 3499, "category": "Fitness", "asin": "B002DYIZH6", "img": "https://m.media-amazon.com/images/I/71f5Eu5lJSL._SL1500_.jpg", "why": "Gold standard post-workout recovery"},
    {"title": "Boldfit Yoga Mat", "price": 999, "category": "Fitness", "asin": "B08CR1X9X9", "img": "https://m.media-amazon.com/images/I/71f5Eu5lJSL._SL1500_.jpg", "why": "Non-slip grip for yoga sessions"},
    {"title": "Fitbit Charge 6", "price": 14999, "category": "Fitness", "asin": "B0CJG1X9X9", "img": "https://m.media-amazon.com/images/I/71f5Eu5lJSL._SL1500_.jpg", "why": "Accurate heart rate and GPS"},

    # ========== CHEAP FINDS (<₹500) ==========
    {"title": "Boat Bassheads 100 Earphones", "price": 399, "category": "Electronics", "asin": "B071Z8M4KX", "img": "https://m.media-amazon.com/images/I/71pCO76IDXL._SL1500_.jpg", "why": "Incredible sound for under 500"},
    {"title": "Amazon Basics USB-C Cable", "price": 299, "category": "Tech", "asin": "B010S9N6OO", "img": "https://m.media-amazon.com/images/I/61ni3t1ryQL._SL1500_.jpg", "why": "Reliable fast charging cable"},
    {"title": "Plastic Water Bottle Set", "price": 199, "category": "Home", "asin": "B07WNV1X9X", "img": "https://m.media-amazon.com/images/I/71pCO76IDXL._SL1500_.jpg", "why": "Durable daily use bottles"},
    {"title": "Stainless Steel Straws", "price": 249, "category": "Home", "asin": "B08CR1X9X9", "img": "https://m.media-amazon.com/images/I/51fSAn6vSXL._SL1000_.jpg", "why": "Eco-friendly lifestyle choice"},
    {"title": "Mobile Stand for Desk", "price": 149, "category": "Tech", "asin": "B0CFY7N86M", "img": "https://m.media-amazon.com/images/I/61ni3t1ryQL._SL1500_.jpg", "why": "Convenient stand for your phone"},
    {"title": "Microfiber Cleaning Cloths", "price": 349, "category": "Home", "asin": "B009B0Z9X9", "img": "https://m.media-amazon.com/images/I/71R6BD6e8dL._SL1500_.jpg", "why": "Scratch-free cleaning for gadgets"},
]

# Dynamic filler generation with better variety
def generate_filler_products():
    categories = ["Electronics", "Fitness", "Dropshipping", "Tools", "Mobile", "Laptops", "Tech", "Fashion", "Home"]
    variety_images = [
        "https://m.media-amazon.com/images/I/61ni3t1ryQL._SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71pCO76IDXL._SL1500_.jpg",
        "https://m.media-amazon.com/images/I/51fSAn6vSXL._SL1000_.jpg",
        "https://m.media-amazon.com/images/I/81m6-9ubYML._SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71R6BD6e8dL._SL1500_.jpg",
        "https://m.media-amazon.com/images/I/61+7y9To9vL._SL1500_.jpg",
        "https://m.media-amazon.com/images/I/61Z6-ov-rjL._SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71A9B6Lz4kL._SL1500_.jpg",
        "https://m.media-amazon.com/images/I/61f1YfTQ9pL._SL1500_.jpg",
        "https://m.media-amazon.com/images/I/51mCH6-AnDL._SL1500_.jpg",
        "https://m.media-amazon.com/images/I/81+GIkwqLIL._SL1500_.jpg",
        "https://m.media-amazon.com/images/I/718f-lC5TdL._SL1500_.jpg"
    ]
    variety_asins = ["B0CFY7N86M", "B09G9D8KRQ", "B08J82K4S1", "B0B11S6YNF", "B09TMF6742", "B09XS7JWHH", "B0BDHWDR12", "B0B3C5FTZJ", "B0CHX1W1XY", "B0CS69S9RC", "B0CX5Z9X9X", "B0CM5L9Z9X"]
    
    filler = []
    for cat in categories:
        existing_count = len([p for p in AMAZON_PRODUCTS if p["category"] == cat])
        needed = 50 - existing_count
        for i in range(needed):
            asin = variety_asins[i % len(variety_asins)]
            img = variety_images[i % len(variety_images)]
            # Add price variety
            if cat == "Fashion":
                price = 299 + (i * 120)
            elif cat == "Home":
                price = 199 + (i * 90)
            elif cat == "Electronics":
                price = 499 + (i * 200)
            else:
                price = 399 + (i * 150)
                
            filler.append({
                "title": f"Top-Rated {cat} {['Essential', 'Premium', 'Must-Have', 'Choice'][i%4]} v{i+1}",
                "price": price,
                "category": cat,
                "asin": asin,
                "img": img,
                "why": f"Verified {cat.lower()} choice for quality and value"
            })
    return filler

AMAZON_PRODUCTS.extend(generate_filler_products())

async def seed_amazon():
    print(f"Connecting to {db_name}...")
    
    # CLEAR existing Amazon products
    print(f"Clearing existing Amazon products...")
    await db.products.delete_many({"affiliate_network": "Amazon"})
    
    print(f"Adding {len(AMAZON_PRODUCTS)} Amazon products with tag {AFFILIATE_TAG}...")
    
    docs = []
    for p in AMAZON_PRODUCTS:
        product_doc = {
            "id": str(uuid.uuid4()),
            "title": p["title"],
            "description": f"Real {p['title']} from our curated {p['category']} collection. Perfect for those looking for high-quality items at the best price.",
            "why_this_product": p["why"],
            "price": float(p["price"]),
            "category": p["category"],
            "type": "affiliate",
            "affiliate_link": get_amazon_link(p["asin"]),
            "affiliate_network": "Amazon",
            "image_url": p["img"],
            "featured": False,
            "premium": False,
            "verified": True,
            "rating": round(4.0 + (hash(p["title"]) % 10) / 10, 1),
            "review_count": (hash(p["title"]) % 1000) + 100,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        docs.append(product_doc)
    
    if docs:
        await db.products.insert_many(docs)
        print(f"SUCCESS: Seeded {len(docs)} diverse Amazon products!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_amazon())
