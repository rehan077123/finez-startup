"""
Script to update all affiliate links with your REAL affiliate IDs
Run this AFTER you get approved by affiliate programs
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
import os
from dotenv import load_dotenv  # type: ignore
from pathlib import Path

from dotenv import load_dotenv  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

# Load environment variables from .env file
ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env", override=True)

# MongoDB connection
mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

# ==========================================
# ⚠️ REPLACE THESE WITH YOUR REAL IDs ⚠️
# ==========================================

YOUR_AFFILIATE_IDS = {
    # Amazon India - Get from: https://affiliate-program.amazon.in/
    "amazon_id": "yourname-21",  # ⚠️ REPLACE THIS
    # Flipkart - Get from: https://affiliate.flipkart.com/
    "flipkart_id": "your_flipkart_id",  # ⚠️ REPLACE THIS
    # Cuelinks - Get from: https://www.cuelinks.com/
    "cuelinks_id": "your_cuelinks_subid",  # ⚠️ REPLACE THIS
    # Shopify Partners - Get from: https://www.shopify.com/partners
    "shopify_ref": "your_shopify_ref",  # ⚠️ REPLACE THIS
    # Hostinger - Get from: https://www.hostinger.com/affiliates
    "hostinger_ref": "your_hostinger_ref",  # ⚠️ REPLACE THIS
    # Coursera - Get from: https://www.coursera.org/affiliate
    "coursera_ref": "your_coursera_ref",  # ⚠️ REPLACE THIS
}

# Mapping of what to replace
LINK_UPDATES = {
    # Amazon links
    "amazon.in": f"https://www.amazon.in/dp/{{product_id}}?tag="
    f"{YOUR_AFFILIATE_IDS['amazon_id']}",
    "amazon.com": f"https://www.amazon.com/dp/{{product_id}}?tag="
    f"{YOUR_AFFILIATE_IDS['amazon_id']}",
    # For now, keep other links as placeholder - update when you get approved
}


async def update_affiliate_links():
    """Update all affiliate links in database"""

    print("🔄 Starting affiliate link update...")
    print("\n⚠️  IMPORTANT: Make sure you've replaced the placeholder IDs above!\n")

    # Confirm before proceeding
    confirm = input(
        "Have you replaced YOUR_AFFILIATE_IDS with real values? (yes/no): ")
    if confirm.lower() != "yes":
        print("❌ Please update YOUR_AFFILIATE_IDS first, then run again.")
        return

    # Get all products
    products = await db.products.find({}).to_list(1000)

    updated_count = 0

    for product in products:
        affiliate_link = product.get("affiliate_link", "")

        # Check if it has placeholder
        if "?ref=yourid" in affiliate_link or "tag=yourid" in affiliate_link:
            # Update based on network
            if "amazon" in affiliate_link:
                # Extract product ID and rebuild link
                if "amazon.in" in affiliate_link:
                    # Example: https://amazon.in/dp/PRODUCT?tag=yourid
                    product_id = (
                        affiliate_link.split("/dp/")[-1].split("?")[0]
                        if "/dp/" in affiliate_link
                        else "B08X"
                    )
                    new_link = (
                        f"https://www.amazon.in/dp/{product_id}?tag="
                        f"{YOUR_AFFILIATE_IDS['amazon_id']}"
                    )
                else:
                    product_id = (
                        affiliate_link.split("/dp/")[-1].split("?")[0]
                        if "/dp/" in affiliate_link
                        else "B08X"
                    )
                    new_link = (
                        f"https://www.amazon.com/dp/{product_id}?tag="
                        f"{YOUR_AFFILIATE_IDS['amazon_id']}"
                    )

                # Update in database
                await db.products.update_one(
                    {"_id": product["_id"]},
                    {
                        "$set": {
                            "affiliate_link": new_link,
                            "affiliate_network": "Amazon Associates",
                        }
                    },
                )
                updated_count += 1
                print(f"✅ Updated: {product.get('title', 'Unknown')[:50]}...")

            elif "flipkart" in affiliate_link:
                # For Flipkart, you'll get specific link from their dashboard
                print(
                    f"⚠️  Flipkart link needs manual update: {product.get('title', 'Unknown')[:50]}"
                )

            else:
                # For other links, replace ref=yourid with actual ref
                new_link = affiliate_link.replace(
                    "?ref=yourid", f'?ref={YOUR_AFFILIATE_IDS["amazon_id"]}'
                )
                await db.products.update_one(
                    {"_id": product["_id"]}, {
                        "$set": {"affiliate_link": new_link}}
                )
                updated_count += 1
                print(f"✅ Updated: {product.get('title', 'Unknown')[:50]}...")

    print(f"\n🎉 DONE! Updated {updated_count} affiliate links!")
    print("\n💡 Next steps:")
    print("1. Test a few product links to make sure they work")
    print("2. Check your affiliate dashboards to track clicks")
    print("3. Start driving traffic to your site!")

    client.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🔗 FineZ Affiliate Link Updater")
    print("=" * 60)
    asyncio.run(update_affiliate_links())
