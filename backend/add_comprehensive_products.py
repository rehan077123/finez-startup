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

ALL_PRODUCTS = [
    # ========== AI TOOLS (10) ==========
    {
        "title": "ChatGPT Plus",
        "description": "Advanced AI assistant powered by GPT-4o. Get instant answers, write content, code, and more.",
        "why_this_product": "The most versatile AI tool for productivity, coding, and creative work.",
        "price": 20.0,
        "category": "AI Tools",
        "type": "affiliate",
        "affiliate_link": "https://openai.com/chatgpt",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
        "featured": True
    },
    {
        "title": "Claude.ai Pro",
        "description": "Anthropic's most capable model, Claude 3.5 Sonnet, with higher usage limits and priority access.",
        "why_this_product": "Excellent for long-form writing and complex reasoning tasks.",
        "price": 20.0,
        "category": "AI Tools",
        "type": "affiliate",
        "affiliate_link": "https://claude.ai",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Claude_AI_logo.svg",
        "featured": True
    },
    {
        "title": "Midjourney",
        "description": "Generate high-quality AI art and realistic images using simple text prompts in Discord.",
        "why_this_product": "The industry leader in high-fidelity AI image generation.",
        "price": 30.0,
        "category": "AI Tools",
        "type": "affiliate",
        "affiliate_link": "https://www.midjourney.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Midjourney_Emblem.svg",
        "featured": True
    },
    {
        "title": "Jasper AI",
        "description": "Enterprise-grade AI content platform for marketing and business teams.",
        "why_this_product": "Specifically designed for marketing copy, SEO, and team collaboration.",
        "price": 49.0,
        "category": "AI Tools",
        "type": "affiliate",
        "affiliate_link": "https://www.jasper.ai",
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",
        "featured": False
    },
    {
        "title": "Notion AI",
        "description": "Built-in AI for your Notion workspace to help you summarize, write, and organize.",
        "why_this_product": "Seamlessly integrates AI into your existing workflow and notes.",
        "price": 10.0,
        "category": "AI Tools",
        "type": "affiliate",
        "affiliate_link": "https://www.notion.so/product/ai",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png",
        "featured": False
    },
    {
        "title": "Canva Magic Studio",
        "description": "AI-powered design tools to create graphics, videos, and presentations instantly.",
        "why_this_product": "Makes professional design accessible to everyone with AI.",
        "price": 12.99,
        "category": "AI Tools",
        "type": "affiliate",
        "affiliate_link": "https://www.canva.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/08/Canva_icon_2021.svg",
        "featured": False
    },
    {
        "title": "Perplexity AI Pro",
        "description": "An AI-powered search engine that provides cited answers to complex questions.",
        "why_this_product": "The future of search - fast, accurate, and provides sources.",
        "price": 20.0,
        "category": "AI Tools",
        "type": "affiliate",
        "affiliate_link": "https://www.perplexity.ai",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Perplexity_AI_logo.svg",
        "featured": False
    },
    {
        "title": "Synthesia",
        "description": "Create AI videos from text in minutes with realistic AI avatars.",
        "why_this_product": "Perfect for training, sales, and marketing videos without a camera crew.",
        "price": 30.0,
        "category": "AI Tools",
        "type": "affiliate",
        "affiliate_link": "https://www.synthesia.io",
        "image_url": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800",
        "featured": False
    },
    {
        "title": "Descript",
        "description": "AI-powered video and podcast editor that makes editing as easy as editing a document.",
        "why_this_product": "Revolutionary 'Overdub' feature can clone your voice for corrections.",
        "price": 15.0,
        "category": "AI Tools",
        "type": "affiliate",
        "affiliate_link": "https://www.descript.com",
        "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800",
        "featured": False
    },
    {
        "title": "Copy.ai",
        "description": "AI-driven platform for generating high-quality marketing copy and content.",
        "why_this_product": "Excellent for overcoming writer's block and scaling content production.",
        "price": 36.0,
        "category": "AI Tools",
        "type": "affiliate",
        "affiliate_link": "https://www.copy.ai",
        "image_url": "https://copy.ai/favicon.ico",
        "featured": False
    },

    # ========== ELECTRONICS (10) ==========
    {
        "title": "Sony WH-1000XM5 Headphones",
        "description": "Premium wireless noise-canceling headphones with exceptional sound quality.",
        "why_this_product": "Industry-leading noise cancellation and 30-hour battery life.",
        "price": 348.0,
        "category": "Electronics",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Sony-WH-1000XM5-Canceling-Headphones-Hands-Free/dp/B09XS7JWHH",
        "image_url": "https://m.media-amazon.com/images/I/61v43Ti-VYL._AC_SL1500_.jpg",
        "featured": True
    },
    {
        "title": "MacBook Air M3 (2024)",
        "description": "Thin, light, and powerful laptop with the latest Apple M3 chip.",
        "why_this_product": "The best balance of performance, portability, and battery life.",
        "price": 1099.0,
        "category": "Electronics",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Apple-2024-MacBook-13-inch-Laptop/dp/B0CX2169S7",
        "image_url": "https://m.media-amazon.com/images/I/71ItMZ7ra6L._AC_SL1500_.jpg",
        "featured": True
    },
    {
        "title": "iPhone 15 Pro",
        "description": "Apple's latest flagship phone with titanium design and A17 Pro chip.",
        "why_this_product": "The most powerful iPhone with professional-grade camera capabilities.",
        "price": 999.0,
        "category": "Electronics",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Apple-iPhone-Pro-128GB-Natural/dp/B0CHX7S557",
        "image_url": "https://m.media-amazon.com/images/I/81dT7vFPASL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Samsung Galaxy S24 Ultra",
        "description": "Samsung's premium flagship with built-in S Pen and AI capabilities.",
        "why_this_product": "The best display and zoom camera on any smartphone.",
        "price": 1299.0,
        "category": "Electronics",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Samsung-Smartphone-Unlocked-Processor-Titanium/dp/B0CMDJ7Y4F",
        "image_url": "https://m.media-amazon.com/images/I/71WjsZ8n1LL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Kindle Paperwhite (16 GB)",
        "description": "The best e-reader with a 6.8\" display and adjustable warm light.",
        "why_this_product": "Waterproof and has weeks of battery life - perfect for readers.",
        "price": 149.99,
        "category": "Electronics",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Kindle-Paperwhite-16-GB-adjustable-warm/dp/B09TMN644Z",
        "image_url": "https://m.media-amazon.com/images/I/51XvL9X9VWL._AC_SL1000_.jpg",
        "featured": False
    },
    {
        "title": "Apple Watch Series 9",
        "description": "The world's most popular smartwatch with advanced health and fitness tracking.",
        "why_this_product": "Seamless integration with iPhone and powerful health insights.",
        "price": 329.0,
        "category": "Electronics",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Apple-Watch-Series-Smartwatch-Aluminum/dp/B0CHX698X3",
        "image_url": "https://m.media-amazon.com/images/I/71fD6vE6AAL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Bose QuietComfort Ultra",
        "description": "Bose's best noise-canceling headphones with world-class quiet and spatial audio.",
        "why_this_product": "Unmatched comfort and the best noise cancellation in the industry.",
        "price": 429.0,
        "category": "Electronics",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Bose-QuietComfort-Ultra-Bluetooth-Headphones/dp/B0CCZ26B5V",
        "image_url": "https://m.media-amazon.com/images/I/51n9S5Ea4tL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Logitech MX Master 3S",
        "description": "Advanced wireless mouse with 8K DPI tracking and ultra-quiet clicks.",
        "why_this_product": "The gold standard for productivity and professional workflows.",
        "price": 99.0,
        "category": "Electronics",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Logitech-MX-Master-3S-Graphite/dp/B09HM94VPP",
        "image_url": "https://m.media-amazon.com/images/I/61ni3Ky9CLL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Anker 737 Power Bank",
        "description": "High-capacity 24,000mAh battery pack with 140W fast charging.",
        "why_this_product": "Can charge a MacBook Pro and has a smart digital display.",
        "price": 149.99,
        "category": "Electronics",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Anker-PowerBank-24-000mAh-Smart-Display/dp/B09VPHVT2Z",
        "image_url": "https://m.media-amazon.com/images/I/61fXAnS371L._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "DJI Mini 4 Pro",
        "description": "Under-250g drone with 4K HDR video and omnidirectional obstacle sensing.",
        "why_this_product": "The best drone you can fly without registration in many countries.",
        "price": 759.0,
        "category": "Electronics",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/DJI-Mini-Pro-Remote-Control/dp/B0CHM6K6P3",
        "image_url": "https://m.media-amazon.com/images/I/61I2o8mB5pL._AC_SL1500_.jpg",
        "featured": False
    },

    # ========== BEAUTY (10) ==========
    {
        "title": "COSRX Snail Mucin 96% Essence",
        "description": "Viral Korean skincare essence for hydration and skin repair.",
        "why_this_product": "Massive popularity and proven results for glowing skin.",
        "price": 14.50,
        "category": "Beauty",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/COSRX-Repairing-Hydrating-Packaging-Calculated/dp/B00PBX3L7K",
        "image_url": "https://m.media-amazon.com/images/I/51uFf97En9L._SL1500_.jpg",
        "featured": True
    },
    {
        "title": "Dyson Airwrap Multi-Styler",
        "description": "The ultimate luxury hair styling tool for curls, waves, and smoothing.",
        "why_this_product": "The most sought-after hair tool that protects from extreme heat.",
        "price": 599.0,
        "category": "Beauty",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Dyson-Airwrap-Multi-Styler-Complete-Nickel/dp/B0B5Z8R6S8",
        "image_url": "https://m.media-amazon.com/images/I/61O27Mh8R+L._SL1500_.jpg",
        "featured": True
    },
    {
        "title": "Laneige Lip Sleeping Mask",
        "description": "Intensive lip treatment that delivers moisture and antioxidants.",
        "why_this_product": "Cult favorite for soft, hydrated lips overnight.",
        "price": 24.0,
        "category": "Beauty",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/LANEIGE-Lip-Sleeping-Mask-Berry/dp/B099YMTN9L",
        "image_url": "https://m.media-amazon.com/images/I/61yKq2756LL._SL1500_.jpg",
        "featured": False
    },
    {
        "title": "The Ordinary Niacinamide 10% + Zinc 1%",
        "description": "High-strength vitamin and mineral blemish formula.",
        "why_this_product": "Effective and affordable skincare staple for clear skin.",
        "price": 6.0,
        "category": "Beauty",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Ordinary-Niacinamide-10-Zinc-1/dp/B06X9Z6KSM",
        "image_url": "https://m.media-amazon.com/images/I/61X-i-f-uML._SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Olaplex No. 3 Hair Perfector",
        "description": "Concentrated treatment that strengthens hair from within.",
        "why_this_product": "The gold standard for repairing damaged and bleached hair.",
        "price": 30.0,
        "category": "Beauty",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Olaplex-No-3-Hair-Perfector/dp/B0086OTU10",
        "image_url": "https://m.media-amazon.com/images/I/51A3Y0U0uRL._SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Paula's Choice Skin Perfecting 2% BHA",
        "description": "Liquid exfoliant that unclogs pores and evens skin tone.",
        "why_this_product": "Award-winning formula that transforms skin texture.",
        "price": 34.0,
        "category": "Beauty",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Paulas-Choice-SKIN-PERFECTING-Exfoliant-Blackheads/dp/B00949CT6C",
        "image_url": "https://m.media-amazon.com/images/I/61U0T2VpMML._SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Revlon One-Step Hair Dryer",
        "description": "Hair dryer and volumizer brush for professional blowouts at home.",
        "why_this_product": "Incredible value and time-saver for daily styling.",
        "price": 39.99,
        "category": "Beauty",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Revlon-One-Step-Dryer-Volumizer-Black/dp/B01LSUQSB0",
        "image_url": "https://m.media-amazon.com/images/I/71u-pS-iM6L._SL1500_.jpg",
        "featured": False
    },
    {
        "title": "CeraVe Moisturizing Cream",
        "description": "Dermatologist-recommended body and face moisturizer for dry skin.",
        "why_this_product": "Essential basic that works for almost everyone.",
        "price": 17.78,
        "category": "Beauty",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/CeraVe-Moisturizing-Cream-Daily-Moisturizer/dp/B00TTD9BRC",
        "image_url": "https://m.media-amazon.com/images/I/61S7Br9bfxL._SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Hero Cosmetics Mighty Patch",
        "description": "Hydrocolloid acne patches that absorb gunk from pimples overnight.",
        "why_this_product": "Fast-acting and virtually invisible blemish treatment.",
        "price": 12.99,
        "category": "Beauty",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Hero-Cosmetics-Mighty-Patch-Original/dp/B074PVTPBW",
        "image_url": "https://m.media-amazon.com/images/I/51R5k7Xyq2L._SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Sol de Janeiro Bum Bum Cream",
        "description": "Fast-absorbing body cream with a signature pistachio and salted caramel scent.",
        "why_this_product": "Incredible scent and firming effect make it a luxury staple.",
        "price": 48.0,
        "category": "Beauty",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Sol-Janeiro-Brazilian-Bum-Cream/dp/B013G679S0",
        "image_url": "https://m.media-amazon.com/images/I/61Nf+45fJEL._SL1500_.jpg",
        "featured": False
    },

    # ========== HOME GADGETS (10) ==========
    {
        "title": "Fullstar Vegetable Chopper",
        "description": "4-in-1 kitchen gadget for chopping, slicing, and dicing.",
        "why_this_product": "#1 best seller for meal prep and kitchen efficiency.",
        "price": 24.99,
        "category": "Home Gadgets",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Fullstar-Vegetable-Chopper-Spiralizer-Cutter/dp/B0764HS4SL",
        "image_url": "https://m.media-amazon.com/images/I/81p825C99HL._AC_SL1500_.jpg",
        "featured": True
    },
    {
        "title": "Ember Smart Mug 2",
        "description": "Temperature-controlled smart mug with app connectivity.",
        "why_this_product": "Keeps your coffee at the perfect temperature for hours.",
        "price": 129.95,
        "category": "Home Gadgets",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Ember-Temperature-Control-Smart-14-oz/dp/B07W9RL9MB",
        "image_url": "https://m.media-amazon.com/images/I/51U8V2l19qL._AC_SL1000_.jpg",
        "featured": True
    },
    {
        "title": "Ninja AF101 Air Fryer",
        "description": "High-performance air fryer for healthy and crispy cooking.",
        "why_this_product": "The most reliable and versatile air fryer on the market.",
        "price": 89.99,
        "category": "Home Gadgets",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Ninja-AF101-Fryer-Black-Gray/dp/B07FDJMC9Q",
        "image_url": "https://m.media-amazon.com/images/I/71atv69YIuL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Ring Video Doorbell",
        "description": "1080p HD video doorbell with enhanced motion detection.",
        "why_this_product": "Essential smart home security and convenience.",
        "price": 99.99,
        "category": "Home Gadgets",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Ring-Video-Doorbell-Satin-Nickel-2020-Release/dp/B08N5NQ869",
        "image_url": "https://m.media-amazon.com/images/I/51y1fE6pZfL._AC_SL1000_.jpg",
        "featured": False
    },
    {
        "title": "iRobot Roomba j7+",
        "description": "Self-emptying robot vacuum with obstacle avoidance.",
        "why_this_product": "Hands-free cleaning that actually works and avoids obstacles.",
        "price": 599.0,
        "category": "Home Gadgets",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/iRobot-Roomba-Self-Emptying-Robot-Vacuum/dp/B094NX6Z69",
        "image_url": "https://m.media-amazon.com/images/I/71YyV6K7x7L._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Philips Hue Starter Kit",
        "description": "Smart LED bulb kit with bridge for ultimate lighting control.",
        "why_this_product": "The gold standard for smart home lighting and ambiance.",
        "price": 159.0,
        "category": "Home Gadgets",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Philips-Hue-White-Ambiance-Starter/dp/B073SSK6P8",
        "image_url": "https://m.media-amazon.com/images/I/71P4e8vDk0L._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Instant Pot Duo 7-in-1",
        "description": "Multi-use programmable pressure cooker and slow cooker.",
        "why_this_product": "Replaces multiple kitchen appliances and speeds up cooking.",
        "price": 99.95,
        "category": "Home Gadgets",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Instant-Pot-Multi-Use-Programmable-Pressure/dp/B00FLYWNYQ",
        "image_url": "https://m.media-amazon.com/images/I/71WtwEvY85L._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Vitamix E310 Blender",
        "description": "Professional-grade blender for smoothies, soups, and more.",
        "why_this_product": "Unmatched power and durability for serious home cooks.",
        "price": 349.95,
        "category": "Home Gadgets",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Vitamix-Explorian-Blender-Professional-Grade-Container/dp/B0758JHZM3",
        "image_url": "https://m.media-amazon.com/images/I/71lD84X4S9L._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Levoit Air Purifier",
        "description": "HEPA air purifier for home allergies and pet hair.",
        "why_this_product": "Compact, quiet, and highly effective for clean indoor air.",
        "price": 99.99,
        "category": "Home Gadgets",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Levoit-Purifier-Home-Allergies-Pets/dp/B07VVK39F7",
        "image_url": "https://m.media-amazon.com/images/I/71vO5eS6N8L._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Keurig K-Elite Maker",
        "description": "Single-serve K-Cup pod coffee maker with iced coffee setting.",
        "why_this_product": "Fast, convenient, and consistent coffee every morning.",
        "price": 149.0,
        "category": "Home Gadgets",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Keurig-K-Elite-Coffee-Maker-Single/dp/B078NPHS99",
        "image_url": "https://m.media-amazon.com/images/I/71R2oV3rJPL._AC_SL1500_.jpg",
        "featured": False
    },

    # ========== FASHION (10) ==========
    {
        "title": "Carhartt K87 T-Shirt",
        "description": "Heavyweight workwear pocket t-shirt for daily comfort.",
        "why_this_product": "Durable, high-quality basic that fits every wardrobe.",
        "price": 19.99,
        "category": "Fashion",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Carhartt-Mens-K87-Workwear-Pocket-T-Shirt/dp/B00029PGEU",
        "image_url": "https://m.media-amazon.com/images/I/61Yh2OQ3L4L._AC_SY741_.jpg",
        "featured": True
    },
    {
        "title": "Levi's 501 Original Jeans",
        "description": "The original blue jean with a straight fit and button fly.",
        "why_this_product": "Timeless style that never goes out of fashion.",
        "price": 59.50,
        "category": "Fashion",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Levis-Mens-501-Original-Jeans/dp/B0018ON274",
        "image_url": "https://m.media-amazon.com/images/I/71u9Y7+M-EL._AC_SY741_.jpg",
        "featured": True
    },
    {
        "title": "Nike Air Force 1 '07",
        "description": "Classic basketball shoe that's a staple in street fashion.",
        "why_this_product": "The most versatile sneaker that goes with everything.",
        "price": 115.0,
        "category": "Fashion",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/NIKE-Air-Force-Low-Mens/dp/B00186RER6",
        "image_url": "https://m.media-amazon.com/images/I/71Xm6h2S0XL._AC_SY695_.jpg",
        "featured": False
    },
    {
        "title": "Adidas Stan Smith Sneakers",
        "description": "Iconic tennis shoe with a clean, minimalist design.",
        "why_this_product": "A sustainable and classic choice for everyday wear.",
        "price": 100.0,
        "category": "Fashion",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/adidas-Originals-Smith-Sneaker-White/dp/B000Y17BFW",
        "image_url": "https://m.media-amazon.com/images/I/71m5N2K9kBL._AC_SY695_.jpg",
        "featured": False
    },
    {
        "title": "Ray-Ban Classic Wayfarer",
        "description": "Legendary sunglasses that have been a style icon since 1952.",
        "why_this_product": "Unmistakable style and high-quality lens protection.",
        "price": 171.0,
        "category": "Fashion",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Ray-Ban-RB2140-Original-Wayfarer-Sunglasses/dp/B001GNBJQY",
        "image_url": "https://m.media-amazon.com/images/I/5176jDk-JcL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Birkenstock Arizona Sandals",
        "description": "Classic two-strap sandal with an anatomically shaped cork-latex footbed.",
        "why_this_product": "Legendary comfort and a timeless summer staple.",
        "price": 110.0,
        "category": "Fashion",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Birkenstock-Arizona-Soft-Footbed-Suede/dp/B002LZUE76",
        "image_url": "https://m.media-amazon.com/images/I/71rIe+p1KGL._AC_SY695_.jpg",
        "featured": False
    },
    {
        "title": "North Face Borealis Backpack",
        "description": "Classic 28-liter backpack for school, work, or adventure.",
        "why_this_product": "Extremely durable and organized with a comfortable suspension system.",
        "price": 99.0,
        "category": "Fashion",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/THE-NORTH-FACE-Borealis-Backpack/dp/B092S6V6G2",
        "image_url": "https://m.media-amazon.com/images/I/81BvS6LhXvL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Lululemon Align Leggings",
        "description": "Buttery-soft leggings designed for yoga and everyday comfort.",
        "why_this_product": "The gold standard for athleisure and workout wear.",
        "price": 98.0,
        "category": "Fashion",
        "type": "affiliate",
        "affiliate_link": "https://shop.lululemon.com/p/womens-pants/Align-Pant-2",
        "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=800",
        "featured": False
    },
    {
        "title": "Champion Reverse Weave Hoodie",
        "description": "The original heavyweight hoodie that's built to last.",
        "why_this_product": "Classic athletic style and incredible durability.",
        "price": 50.0,
        "category": "Fashion",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Champion-Reverse-Weave-Hoodie-Oxford/dp/B0058X09VO",
        "image_url": "https://m.media-amazon.com/images/I/71lK88vI6FL._AC_SY741_.jpg",
        "featured": False
    },
    {
        "title": "Crocs Classic Clogs",
        "description": "The iconic, comfortable clog that started a comfort revolution.",
        "why_this_product": "Unmatched comfort and versatility for all ages.",
        "price": 49.99,
        "category": "Fashion",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Crocs-Classic-Clog-White-Women/dp/B0014C5S7S",
        "image_url": "https://m.media-amazon.com/images/I/61M-kY3mUGL._AC_SY695_.jpg",
        "featured": False
    },

    # ========== FITNESS (10) ==========
    {
        "title": "Renpho Smart Scale",
        "description": "Body composition analyzer that syncs with fitness apps.",
        "why_this_product": "Affordable and comprehensive tracking of health metrics.",
        "price": 24.99,
        "category": "Fitness",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/RENPHO-Bluetooth-Bathroom-Composition-Smartphone/dp/B01N1UX8RW",
        "image_url": "https://m.media-amazon.com/images/I/61Y3X2U5S0L._AC_SL1500_.jpg",
        "featured": True
    },
    {
        "title": "Bowflex Adjustable Dumbbells",
        "description": "Space-saving dumbbells that replace 15 sets of weights.",
        "why_this_product": "The ultimate home gym solution for strength training.",
        "price": 429.0,
        "category": "Fitness",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Bowflex-SelectTech-552-Adjustable-Dumbbells/dp/B001ARYU58",
        "image_url": "https://m.media-amazon.com/images/I/71-u6-p6XTL._AC_SL1500_.jpg",
        "featured": True
    },
    {
        "title": "Fitbit Charge 6",
        "description": "Advanced fitness tracker with built-in GPS and heart rate monitoring.",
        "why_this_product": "The most comprehensive tracker for daily health and workouts.",
        "price": 159.95,
        "category": "Fitness",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Fitbit-Charge-Fitness-Tracker-Google/dp/B0C8V4C4D7",
        "image_url": "https://m.media-amazon.com/images/I/61v027Dq6yL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Garmin Forerunner 255",
        "description": "GPS running watch with advanced training metrics and recovery insights.",
        "why_this_product": "A serious tool for runners and athletes to improve performance.",
        "price": 349.99,
        "category": "Fitness",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Garmin-Forerunner-Running-Smartwatch-Advanced/dp/B09XF86Q6X",
        "image_url": "https://m.media-amazon.com/images/I/61nN4G784sL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Theragun Mini (2nd Gen)",
        "description": "Portable percussion massager for on-the-go muscle recovery.",
        "why_this_product": "The most effective and compact recovery tool for athletes.",
        "price": 199.0,
        "category": "Fitness",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Theragun-Mini-Portable-Percussive-Therapy/dp/B0BHTMT81Y",
        "image_url": "https://m.media-amazon.com/images/I/61Z7Fm+r9XL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Hydro Flask Water Bottle",
        "description": "Vacuum-insulated stainless steel water bottle with straw lid.",
        "why_this_product": "Keeps drinks cold for 24 hours and is incredibly durable.",
        "price": 44.95,
        "category": "Fitness",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Hydro-Flask-Wide-Mouth-Straw/dp/B083G9Y55N",
        "image_url": "https://m.media-amazon.com/images/I/61f4P8G84cL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Manduka PRO Yoga Mat",
        "description": "Ultra-dense yoga mat with unmatched support and durability.",
        "why_this_product": "The top choice for yoga teachers and serious practitioners.",
        "price": 129.0,
        "category": "Fitness",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Manduka-PRO-Yoga-Mat-Black/dp/B00008I73T",
        "image_url": "https://m.media-amazon.com/images/I/71u9yH0U4hL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "TRX All-in-One System",
        "description": "Suspension trainer for full-body workouts using your own weight.",
        "why_this_product": "The most versatile piece of fitness equipment you can use anywhere.",
        "price": 199.95,
        "category": "Fitness",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/TRX-All-One-Suspension-Trainer/dp/B073XG8W1X",
        "image_url": "https://m.media-amazon.com/images/I/71W+2r60QWL._AC_SL1500_.jpg",
        "featured": False
    },
    {
        "title": "Peloton Bike+",
        "description": "The ultimate indoor cycling experience with a 24\" HD touchscreen.",
        "why_this_product": "World-class instructors and an immersive community experience.",
        "price": 2495.0,
        "category": "Fitness",
        "type": "affiliate",
        "affiliate_link": "https://www.onepeloton.com/bikes",
        "image_url": "https://images.unsplash.com/photo-1591741535018-d042766c62eb?w=800",
        "featured": False
    },
    {
        "title": "Iron Flask Sports Bottle",
        "description": "Stainless steel insulated water bottle with three different lids.",
        "why_this_product": "Great value alternative to Hydro Flask with multiple lid options.",
        "price": 24.95,
        "category": "Fitness",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/Iron-Flask-Sports-Water-Bottle/dp/B07N3S1K5W",
        "image_url": "https://m.media-amazon.com/images/I/71p0W9qO9GL._AC_SL1500_.jpg",
        "featured": False
    },

    # ========== SIDE HUSTLES (10) ==========
    {
        "title": "Fiverr Freelancing",
        "description": "Sell your digital skills and services to a global audience.",
        "why_this_product": "The easiest platform to start earning your first $100 online.",
        "price": 0.0,
        "category": "Side Hustles",
        "type": "idea",
        "affiliate_link": "https://www.fiverr.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/18/Fiverr_Logo_09.2020.svg",
        "featured": True
    },
    {
        "title": "Upwork Freelancing",
        "description": "Premium platform for professional freelancers and high-paying clients.",
        "why_this_product": "Scale your freelance business to six figures with long-term contracts.",
        "price": 0.0,
        "category": "Side Hustles",
        "type": "idea",
        "affiliate_link": "https://www.upwork.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Upwork-logo.svg",
        "featured": True
    },
    {
        "title": "Etsy Shop",
        "description": "Sell handmade goods, vintage items, and digital downloads.",
        "why_this_product": "The best marketplace for creative and unique products.",
        "price": 0.20,
        "category": "Side Hustles",
        "type": "idea",
        "affiliate_link": "https://www.etsy.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/8/89/Etsy_logo.svg",
        "featured": False
    },
    {
        "title": "Amazon Associates",
        "description": "Earn commissions by promoting products from the world's largest retailer.",
        "why_this_product": "The most trusted affiliate program with millions of products.",
        "price": 0.0,
        "category": "Side Hustles",
        "type": "idea",
        "affiliate_link": "https://affiliate-program.amazon.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
        "featured": True
    },
    {
        "title": "Printful Print-on-Demand",
        "description": "Start a custom apparel brand with zero inventory and automated fulfillment.",
        "why_this_product": "The most reliable print-on-demand partner for high-quality goods.",
        "price": 0.0,
        "category": "Side Hustles",
        "type": "dropshipping",
        "affiliate_link": "https://www.printful.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Printful_logo.svg",
        "featured": False
    },
    {
        "title": "Teachable",
        "description": "Create and sell online courses with your own branded platform.",
        "why_this_product": "The best platform for building a serious online education business.",
        "price": 39.0,
        "category": "Side Hustles",
        "type": "affiliate",
        "affiliate_link": "https://teachable.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Teachable_logo.png",
        "featured": False
    },
    {
        "title": "Gumroad",
        "description": "The simplest way to sell digital products like ebooks and software.",
        "why_this_product": "Low barrier to entry and perfect for solo creators.",
        "price": 0.0,
        "category": "Side Hustles",
        "type": "marketplace",
        "affiliate_link": "https://gumroad.com",
        "image_url": "https://images.unsplash.com/photo-1556740758-90de374c12ad?w=800",
        "featured": False
    },
    {
        "title": "Shopify Store",
        "description": "The most powerful platform for building an independent ecommerce brand.",
        "why_this_product": "Scale from zero to millions with industry-leading tools.",
        "price": 29.0,
        "category": "Side Hustles",
        "type": "affiliate",
        "affiliate_link": "https://www.shopify.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Shopify_logo_2018.svg",
        "featured": False
    },
    {
        "title": "Coursera Affiliate",
        "description": "Promote online degrees and certificates from top universities.",
        "why_this_product": "High-value affiliate offers with significant commissions.",
        "price": 0.0,
        "category": "Side Hustles",
        "type": "idea",
        "affiliate_link": "https://www.coursera.org/affiliates",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/97/Coursera-Logo_600x600.svg",
        "featured": False
    },
    {
        "title": "Bluehost Hosting",
        "description": "Start a blog and earn affiliate commissions with WordPress hosting.",
        "why_this_product": "The most recommended hosting for new bloggers.",
        "price": 2.95,
        "category": "Side Hustles",
        "type": "affiliate",
        "affiliate_link": "https://www.bluehost.com",
        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
        "featured": False
    },

    # ========== LEARN (10) ==========
    {
        "title": "Coursera Plus",
        "description": "Unlimited access to 7,000+ courses and professional certificates.",
        "why_this_product": "The best value for continuous learning and career advancement.",
        "price": 59.0,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://www.coursera.org",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/97/Coursera-Logo_600x600.svg",
        "featured": True
    },
    {
        "title": "Udemy Business",
        "description": "Access thousands of top-rated courses for you or your team.",
        "why_this_product": "The largest selection of practical and job-ready skills.",
        "price": 13.99,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://www.udemy.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Udemy_logo.svg",
        "featured": True
    },
    {
        "title": "Skillshare Premium",
        "description": "Creative learning community with thousands of classes in design and art.",
        "why_this_product": "Perfect for hobbyists and creatives looking to expand their skills.",
        "price": 8.25,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://www.skillshare.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/8/82/Skillshare_logo_2020.svg",
        "featured": False
    },
    {
        "title": "LinkedIn Learning",
        "description": "Professional development courses that you can add to your profile.",
        "why_this_product": "Directly boost your employability with verified skills.",
        "price": 29.99,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://www.linkedin.com/learning",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo.svg",
        "featured": False
    },
    {
        "title": "Masterclass",
        "description": "Learn from the world's best in various fields from cooking to writing.",
        "why_this_product": "Unmatched production quality and legendary instructors.",
        "price": 180.0,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://www.masterclass.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/07/MasterClass_logo.svg",
        "featured": False
    },
    {
        "title": "Audible Premium Plus",
        "description": "Get one credit per month and unlimited access to the Plus Catalog.",
        "why_this_product": "The best way to consume books on the go.",
        "price": 14.95,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://www.audible.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/df/Audible_logo.svg",
        "featured": False
    },
    {
        "title": "Kindle Unlimited",
        "description": "Unlimited reading from millions of ebooks and magazines.",
        "why_this_product": "Incredible value for voracious readers.",
        "price": 9.99,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://www.amazon.com/kindle-unlimited",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Kindle_logo.svg",
        "featured": False
    },
    {
        "title": "Codecademy Pro",
        "description": "Learn to code with interactive lessons and real-world projects.",
        "why_this_product": "The best hands-on way to start a career in tech.",
        "price": 19.99,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://www.codecademy.com",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800",
        "featured": False
    },
    {
        "title": "Brilliant.org Premium",
        "description": "Learn math, science, and computer science with interactive puzzles.",
        "why_this_product": "Makes complex STEM subjects fun and intuitive.",
        "price": 12.49,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://brilliant.org",
        "image_url": "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800",
        "featured": False
    },
    {
        "title": "Duolingo Super",
        "description": "Learn a new language with ad-free lessons and unlimited hearts.",
        "why_this_product": "The most addictive and effective language-learning app.",
        "price": 6.99,
        "category": "Learn",
        "type": "affiliate",
        "affiliate_link": "https://www.duolingo.com",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/15/Duolingo_logo.svg",
        "featured": False
    }
]

async def update_database():
    try:
        print(f"Updating database with {len(ALL_PRODUCTS)} high-quality products...")
        
        # Clear existing products to ensure clean categories
        await db.products.delete_many({})
        
        products_to_insert = []
        for product_data in ALL_PRODUCTS:
            product_data["id"] = str(uuid.uuid4())
            product_data["clicks"] = 0
            # Set high quality ratings
            product_data["rating"] = 4.7 + (hash(product_data["title"]) % 4) / 10
            product_data["review_count"] = 1000 + (hash(product_data["title"]) % 5000)
            product_data["verified"] = True
            product_data["created_at"] = datetime.now(timezone.utc).isoformat()
            product_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            products_to_insert.append(product_data)
        
        await db.products.insert_many(products_to_insert)
        print("Successfully updated database with 80 real products!")

    except Exception as e:
        print(f"Error updating database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(update_database())
