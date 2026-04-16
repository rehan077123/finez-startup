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

AMAZON_PRODUCTS = [
    # ========== ELECTRONICS (10) ==========
    {"title": "Sony WH-1000XM5 Headphones", "description": "Premium wireless noise-canceling headphones.", "price": 348.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Sony-WH-1000XM5-Canceling-Headphones-Hands-Free/dp/B09XS7JWHH", "image_url": ""},
    {"title": "Apple MacBook Air M3 (2024)", "description": "13-inch laptop with Apple M3 chip.", "price": 1099.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Apple-2024-MacBook-13-inch-Laptop/dp/B0CX2169S7", "image_url": ""},
    {"title": "Samsung Galaxy S24 Ultra", "description": "Flagship smartphone with AI features.", "price": 1299.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Samsung-Smartphone-Unlocked-Processor-Titanium/dp/B0CMDJ7Y4F", "image_url": ""},
    {"title": "Kindle Paperwhite (16 GB)", "description": "6.8\" display with adjustable warm light.", "price": 149.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Kindle-Paperwhite-16-GB-adjustable-warm/dp/B09TMN644Z", "image_url": ""},
    {"title": "Apple Watch Series 9", "description": "Smartwatch with advanced health sensors.", "price": 329.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Apple-Watch-Series-Smartwatch-Aluminum/dp/B0CHX698X3", "image_url": ""},
    {"title": "Bose QuietComfort Ultra", "description": "World-class noise-canceling headphones.", "price": 429.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Bose-QuietComfort-Ultra-Bluetooth-Headphones/dp/B0CCZ26B5V", "image_url": ""},
    {"title": "Logitech MX Master 3S", "description": "High-performance wireless mouse.", "price": 99.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Logitech-MX-Master-3S-Graphite/dp/B09HM94VPP", "image_url": ""},
    {"title": "Anker 737 Power Bank", "description": "24,000mAh portable charger with 140W output.", "price": 149.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Anker-PowerBank-24-000mAh-Smart-Display/dp/B09VPHVT2Z", "image_url": ""},
    {"title": "DJI Mini 4 Pro Drone", "description": "Ultralight drone with 4K HDR video.", "price": 759.0, "category": "Electronics", "affiliate_link": "https://www.amazon.com/DJI-Mini-Pro-Remote-Control/dp/B0CHM6K6P3", "image_url": ""},
    {"title": "Nintendo Switch OLED Model", "description": "7-inch OLED screen gaming console.", "price": 349.99, "category": "Electronics", "affiliate_link": "https://www.amazon.com/Nintendo-Switch-OLED-Model-Neon-Blue/dp/B098RL6SBJ", "image_url": ""},

    # ========== BEAUTY (10) ==========
    {"title": "COSRX Snail Mucin Essence", "description": "Viral Korean skincare for hydration.", "price": 14.50, "category": "Beauty", "affiliate_link": "https://www.amazon.com/COSRX-Repairing-Hydrating-Packaging-Calculated/dp/B00PBX3L7K", "image_url": ""},
    {"title": "Dyson Airwrap Multi-Styler", "description": "Luxury hair styling with no extreme heat.", "price": 599.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Dyson-Airwrap-Multi-Styler-Complete-Nickel/dp/B0B5Z8R6S8", "image_url": ""},
    {"title": "Laneige Lip Sleeping Mask", "description": "Hydrating lip treatment with antioxidants.", "price": 24.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/LANEIGE-Lip-Sleeping-Mask-Berry/dp/B099YMTN9L", "image_url": ""},
    {"title": "The Ordinary Niacinamide Serum", "description": "Blemish-fighting vitamin and mineral formula.", "price": 6.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Ordinary-Niacinamide-10-Zinc-1/dp/B06X9Z6KSM", "image_url": ""},
    {"title": "Olaplex No. 3 Hair Perfector", "description": "Repair and strengthen damaged hair.", "price": 30.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Olaplex-No-3-Hair-Perfector/dp/B0086OTU10", "image_url": ""},
    {"title": "Paula's Choice 2% BHA Exfoliant", "description": "Unclogs pores and smooths skin texture.", "price": 34.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Paulas-Choice-SKIN-PERFECTING-Exfoliant-Blackheads/dp/B00949CT6C", "image_url": ""},
    {"title": "Revlon One-Step Hair Dryer Brush", "description": "Dry and volumize hair in one step.", "price": 39.99, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Revlon-One-Step-Dryer-Volumizer-Black/dp/B01LSUQSB0", "image_url": ""},
    {"title": "CeraVe Moisturizing Cream", "description": "Dermatologist-recommended for dry skin.", "price": 17.78, "category": "Beauty", "affiliate_link": "https://www.amazon.com/CeraVe-Moisturizing-Cream-Daily-Moisturizer/dp/B00TTD9BRC", "image_url": ""},
    {"title": "Hero Cosmetics Mighty Patch", "description": "Invisible acne patches for quick healing.", "price": 12.99, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Hero-Cosmetics-Mighty-Patch-Original/dp/B074PVTPBW", "image_url": ""},
    {"title": "Sol de Janeiro Bum Bum Cream", "description": "Firming body cream with signature scent.", "price": 48.0, "category": "Beauty", "affiliate_link": "https://www.amazon.com/Sol-Janeiro-Brazilian-Bum-Cream/dp/B013G679S0", "image_url": ""},

    # ========== HOME GADGETS (10) ==========
    {"title": "Fullstar Vegetable Chopper", "description": "Time-saving kitchen multi-tool.", "price": 24.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Fullstar-Vegetable-Chopper-Spiralizer-Cutter/dp/B0764HS4SL", "image_url": ""},
    {"title": "Ember Smart Mug 2", "description": "App-controlled temperature-regulated mug.", "price": 129.95, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Ember-Temperature-Control-Smart-14-oz/dp/B07W9RL9MB", "image_url": ""},
    {"title": "Ninja AF101 Air Fryer", "description": "Healthier cooking with crisp results.", "price": 89.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Ninja-AF101-Fryer-Black-Gray/dp/B07FDJMC9Q", "image_url": ""},
    {"title": "Ring Video Doorbell", "description": "Smart security for your front door.", "price": 99.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Ring-Video-Doorbell-Satin-Nickel-2020-Release/dp/B08N5NQ869", "image_url": ""},
    {"title": "iRobot Roomba j7+ Vacuum", "description": "Self-emptying and obstacle-avoiding robot vacuum.", "price": 599.0, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/iRobot-Roomba-Self-Emptying-Robot-Vacuum/dp/B094NX6Z69", "image_url": ""},
    {"title": "Philips Hue Starter Kit", "description": "Industry-standard smart home lighting.", "price": 159.0, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Philips-Hue-White-Ambiance-Starter/dp/B073SSK6P8", "image_url": ""},
    {"title": "Instant Pot Duo 7-in-1", "description": "Versatile multi-cooker and pressure cooker.", "price": 99.95, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Instant-Pot-Multi-Use-Programmable-Pressure/dp/B00FLYWNYQ", "image_url": ""},
    {"title": "Vitamix E310 Blender", "description": "Professional-grade high-power blender.", "price": 349.95, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Vitamix-Explorian-Blender-Professional-Grade-Container/dp/B0758JHZM3", "image_url": ""},
    {"title": "Levoit Core 300 Air Purifier", "description": "Compact HEPA air filter for clean air.", "price": 99.99, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Levoit-Purifier-Home-Allergies-Pets/dp/B07VVK39F7", "image_url": ""},
    {"title": "Keurig K-Elite Coffee Maker", "description": "Single-serve coffee with iced setting.", "price": 149.0, "category": "Home Gadgets", "affiliate_link": "https://www.amazon.com/Keurig-K-Elite-Coffee-Maker-Single/dp/B078NPHS99", "image_url": ""},

    # ========== FASHION (10) ==========
    {"title": "Carhartt Men's K87 T-Shirt", "description": "Heavyweight durable pocket t-shirt.", "price": 19.99, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Carhartt-Mens-K87-Workwear-Pocket-T-Shirt/dp/B00029PGEU", "image_url": ""},
    {"title": "Levi's 501 Original Fit Jeans", "description": "The quintessential iconic blue jean.", "price": 59.50, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Levis-Mens-501-Original-Jeans/dp/B0018ON274", "image_url": ""},
    {"title": "Nike Air Force 1 Sneakers", "description": "Classic street-style basketball shoes.", "price": 115.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/NIKE-Air-Force-Low-Mens/dp/B00186RER6", "image_url": ""},
    {"title": "Adidas Stan Smith Shoes", "description": "Minimalist and timeless tennis sneakers.", "price": 100.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/adidas-Originals-Smith-Sneaker-White/dp/B000Y17BFW", "image_url": ""},
    {"title": "Ray-Ban Wayfarer Sunglasses", "description": "Iconic and unmistakable frame design.", "price": 171.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Ray-Ban-RB2140-Original-Wayfarer-Sunglasses/dp/B001GNBJQY", "image_url": ""},
    {"title": "Birkenstock Arizona Sandals", "description": "Unmatched comfort with cork footbeds.", "price": 110.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Birkenstock-Arizona-Soft-Footbed-Suede/dp/B002LZUE76", "image_url": ""},
    {"title": "North Face Borealis Backpack", "description": "Durable and organized all-day pack.", "price": 99.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/THE-NORTH-FACE-Borealis-Backpack/dp/B092S6V6G2", "image_url": ""},
    {"title": "Lululemon Align Leggings", "description": "Soft, high-performance athleisure wear.", "price": 98.0, "category": "Fashion", "affiliate_link": "https://shop.lululemon.com/p/womens-pants/Align-Pant-2", "image_url": ""},
    {"title": "Champion Reverse Weave Hoodie", "description": "Classic heavyweight sweatshirt built to last.", "price": 50.0, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Champion-Reverse-Weave-Hoodie-Oxford/dp/B0058X09VO", "image_url": ""},
    {"title": "Crocs Classic Clogs", "description": "Lightweight and versatile comfort clogs.", "price": 49.99, "category": "Fashion", "affiliate_link": "https://www.amazon.com/Crocs-Classic-Clog-White-Women/dp/B0014C5S7S", "image_url": ""},

    # ========== FITNESS (10) ==========
    {"title": "Renpho Smart Body Scale", "description": "Analyzes 13 essential body metrics.", "price": 24.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/RENPHO-Bluetooth-Bathroom-Composition-Smartphone/dp/B01N1UX8RW", "image_url": ""},
    {"title": "Bowflex Adjustable Dumbbells", "description": "Replaces 15 sets of weights in one pair.", "price": 429.0, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Bowflex-SelectTech-552-Adjustable-Dumbbells/dp/B001ARYU58", "image_url": ""},
    {"title": "Fitbit Charge 6 Tracker", "description": "Comprehensive health and activity tracking.", "price": 159.95, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Fitbit-Charge-Fitness-Tracker-Google/dp/B0C8V4C4D7", "image_url": ""},
    {"title": "Garmin Forerunner 255 Watch", "description": "Precision GPS for serious runners.", "price": 349.99, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Garmin-Forerunner-Running-Smartwatch-Advanced/dp/B09XF86Q6X", "image_url": ""},
    {"title": "Theragun Mini Massage Gun", "description": "Portable deep tissue recovery tool.", "price": 199.0, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Theragun-Mini-Portable-Percussive-Therapy/dp/B0BHTMT81Y", "image_url": ""},
    {"title": "Hydro Flask 32oz Bottle", "description": "Insulated stainless steel water bottle.", "price": 44.95, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Hydro-Flask-Wide-Mouth-Straw/dp/B083G9Y55N", "image_url": ""},
    {"title": "Manduka PRO Yoga Mat", "description": "Ultra-dense and high-performance yoga mat.", "price": 129.0, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Manduka-PRO-Yoga-Mat-Black/dp/B00008I73T", "image_url": ""},
    {"title": "TRX Suspension Trainer", "description": "Full-body workout system for home use.", "price": 199.95, "category": "Fitness", "affiliate_link": "https://www.amazon.com/TRX-All-One-Suspension-Trainer/dp/B073XG8W1X", "image_url": ""},
    {"title": "Peloton Bike+ Indoor Cycling", "description": "Immersive home cardio with live classes.", "price": 2495.0, "category": "Fitness", "affiliate_link": "https://www.onepeloton.com/bikes", "image_url": ""},
    {"title": "Iron Flask Sports Bottle", "description": "Double-walled vacuum-insulated bottle.", "price": 24.95, "category": "Fitness", "affiliate_link": "https://www.amazon.com/Iron-Flask-Sports-Water-Bottle/dp/B07N3S1K5W", "image_url": ""},

    # ========== AI TOOLS (10) ==========
    {"title": "ChatGPT Plus Subscription", "description": "Access GPT-4 and advanced AI tools.", "price": 20.0, "category": "AI Tools", "affiliate_link": "https://openai.com/chatgpt", "image_url": ""},
    {"title": "Claude.ai Pro", "description": "Most capable model for complex reasoning.", "price": 20.0, "category": "AI Tools", "affiliate_link": "https://claude.ai", "image_url": ""},
    {"title": "Midjourney AI Art", "description": "Generate stunning realistic AI images.", "price": 30.0, "category": "AI Tools", "affiliate_link": "https://www.midjourney.com", "image_url": ""},
    {"title": "Jasper AI Copywriting", "description": "Enterprise-grade AI marketing platform.", "price": 49.0, "category": "AI Tools", "affiliate_link": "https://www.jasper.ai", "image_url": ""},
    {"title": "Notion AI Integration", "description": "Write and organize faster with built-in AI.", "price": 10.0, "category": "AI Tools", "affiliate_link": "https://www.notion.so/product/ai", "image_url": ""},
    {"title": "Canva Magic Design", "description": "AI-powered graphics and visual editing.", "price": 12.99, "category": "AI Tools", "affiliate_link": "https://www.canva.com", "image_url": ""},
    {"title": "Perplexity AI Pro", "description": "AI search engine with real-time sources.", "price": 20.0, "category": "AI Tools", "affiliate_link": "https://www.perplexity.ai", "image_url": ""},
    {"title": "Synthesia Video AI", "description": "Generate videos with realistic AI avatars.", "price": 30.0, "category": "AI Tools", "affiliate_link": "https://www.synthesia.io", "image_url": ""},
    {"title": "Descript Audio/Video AI", "description": "Text-based video and podcast editing.", "price": 15.0, "category": "AI Tools", "affiliate_link": "https://www.descript.com", "image_url": ""},
    {"title": "Copy.ai Marketing Tool", "description": "Scale your content with AI writing.", "price": 36.0, "category": "AI Tools", "affiliate_link": "https://www.copy.ai", "image_url": ""},

    # ========== SIDE HUSTLES (10) ==========
    {"title": "Fiverr Freelancing Platform", "description": "Start selling your digital skills online.", "price": 0.0, "category": "Side Hustles", "affiliate_link": "https://www.fiverr.com", "image_url": ""},
    {"title": "Upwork Professional Network", "description": "Find high-paying freelance contracts.", "price": 0.0, "category": "Side Hustles", "affiliate_link": "https://www.upwork.com", "image_url": ""},
    {"title": "Etsy Creative Marketplace", "description": "Sell handmade and digital downloads.", "price": 0.0, "category": "Side Hustles", "affiliate_link": "https://www.etsy.com", "image_url": ""},
    {"title": "Amazon Associates Program", "description": "Earn by promoting millions of products.", "price": 0.0, "category": "Side Hustles", "affiliate_link": "https://affiliate-program.amazon.com", "image_url": ""},
    {"title": "Printful POD Service", "description": "Start an apparel brand with no inventory.", "price": 0.0, "category": "Side Hustles", "affiliate_link": "https://www.printful.com", "image_url": ""},
    {"title": "Teachable Course Creator", "description": "Build and sell your own online courses.", "price": 39.0, "category": "Side Hustles", "affiliate_link": "https://teachable.com", "image_url": ""},
    {"title": "Gumroad Digital Shop", "description": "Sell ebooks and digital art easily.", "price": 0.0, "category": "Side Hustles", "affiliate_link": "https://gumroad.com", "image_url": ""},
    {"title": "Shopify Ecommerce", "description": "Build your own independent brand store.", "price": 29.0, "category": "Side Hustles", "affiliate_link": "https://www.shopify.com", "image_url": ""},
    {"title": "Coursera Affiliate Program", "description": "Promote degrees from top universities.", "price": 0.0, "category": "Side Hustles", "affiliate_link": "https://www.coursera.org/affiliates", "image_url": ""},
    {"title": "Bluehost Blog Hosting", "description": "Start a profitable blog with WordPress.", "price": 2.95, "category": "Side Hustles", "affiliate_link": "https://www.bluehost.com", "image_url": ""},

    # ========== LEARN (10) ==========
    {"title": "Coursera Plus Subscription", "description": "Unlimited access to 7,000+ courses.", "price": 59.0, "category": "Learn", "affiliate_link": "https://www.coursera.org", "image_url": ""},
    {"title": "Udemy Online Courses", "description": "Learn practical and job-ready skills.", "price": 13.99, "category": "Learn", "affiliate_link": "https://www.udemy.com", "image_url": ""},
    {"title": "Skillshare Membership", "description": "Join a community for creative learning.", "price": 8.25, "category": "Learn", "affiliate_link": "https://www.skillshare.com", "image_url": ""},
    {"title": "LinkedIn Learning", "description": "Boost your career with verified certificates.", "price": 29.99, "category": "Learn", "affiliate_link": "https://www.linkedin.com/learning", "image_url": ""},
    {"title": "Masterclass Access", "description": "Learn from world-class industry legends.", "price": 180.0, "category": "Learn", "affiliate_link": "https://www.masterclass.com", "image_url": ""},
    {"title": "Audible Premium Plus", "description": "Best-selling audiobooks on the go.", "price": 14.95, "category": "Learn", "affiliate_link": "https://www.audible.com", "image_url": ""},
    {"title": "Kindle Unlimited", "description": "Unlimited reading from millions of titles.", "price": 9.99, "category": "Learn", "affiliate_link": "https://www.amazon.com/kindle-unlimited", "image_url": ""},
    {"title": "Codecademy Pro", "description": "Hands-on coding for modern tech careers.", "price": 19.99, "category": "Learn", "affiliate_link": "https://www.codecademy.com", "image_url": ""},
    {"title": "Brilliant.org Premium", "description": "Interactive math and science puzzles.", "price": 12.49, "category": "Learn", "affiliate_link": "https://brilliant.org", "image_url": ""},
    {"title": "Duolingo Super", "description": "Master a new language with gamified lessons.", "price": 6.99, "category": "Learn", "affiliate_link": "https://www.duolingo.com", "image_url": ""},
]

async def seed_amazon_products():
    try:
        print(f"Adding {len(AMAZON_PRODUCTS)} Amazon products with empty image fields...")
        
        # Clear existing products first
        await db.products.delete_many({})
        
        products_to_insert = []
        for product_data in AMAZON_PRODUCTS:
            product_data["id"] = str(uuid.uuid4())
            product_data["clicks"] = 0
            # Realistic random ratings
            product_data["rating"] = 4.5 + (hash(product_data["title"]) % 5) / 10
            product_data["review_count"] = 500 + (hash(product_data["title"]) % 10000)
            product_data["verified"] = True
            product_data["type"] = "affiliate" if product_data["price"] > 0 else "idea"
            product_data["created_at"] = datetime.now(timezone.utc).isoformat()
            product_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            products_to_insert.append(product_data)
        
        await db.products.insert_many(products_to_insert)
        print("Successfully seeded 80 Amazon products!")

    except Exception as e:
        print(f"Error seeding products: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_amazon_products())
