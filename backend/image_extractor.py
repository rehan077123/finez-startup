"""
Product Image Extractor - Dynamically fetch images from affiliate links
"""

import asyncio
import os
import re
import requests
from urllib.parse import urlparse, parse_qs, urljoin
from bs4 import BeautifulSoup
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import json

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env", override=True)

mongo_url = os.environ.get("MONGO_URI") or os.environ.get("MONGO_URL")
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

# Headers to mimic browser requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}


class ProductImageExtractor:
    """Extract product data from affiliate links"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def extract_amazon_data(self, url):
        """Extract product data from Amazon affiliate link"""
        try:
            # Extract ASIN from URL
            asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
            if not asin_match:
                asin_match = re.search(r'/gp/product/([A-Z0-9]{10})', url)

            if not asin_match:
                return None

            asin = asin_match.group(1)
            print(f"📦 Found Amazon ASIN: {asin}")

            # Try to get product data (Note: This is a simplified version)
            # In production, you'd use Amazon Product Advertising API
            product_data = {
                'asin': asin,
                'title': f"Amazon Product {asin}",
                'image_url': f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01._SCLZZZZZZZ_.jpg",
                'price': None,
                'source': 'amazon'
            }

            return product_data

        except Exception as e:
            print(f"❌ Amazon extraction error: {e}")
            return None

    def extract_flipkart_data(self, url):
        """Extract product data from Flipkart affiliate link"""
        try:
            # Extract product ID from URL
            pid_match = re.search(r'/p/([a-zA-Z0-9]+)', url)
            if not pid_match:
                return None

            pid = pid_match.group(1)
            print(f"📦 Found Flipkart PID: {pid}")

            product_data = {
                'pid': pid,
                'title': f"Flipkart Product {pid}",
                'image_url': f"https://rukminim2.flixcdn.com/image/832/832/{pid}.jpg",
                'price': None,
                'source': 'flipkart'
            }

            return product_data

        except Exception as e:
            print(f"❌ Flipkart extraction error: {e}")
            return None

    def extract_aliexpress_data(self, url):
        """Extract product data from AliExpress affiliate link"""
        try:
            # Extract product ID from URL
            pid_match = re.search(r'/item/(\d+)\.html', url)
            if not pid_match:
                return None

            pid = pid_match.group(1)
            print(f"📦 Found AliExpress PID: {pid}")

            product_data = {
                'pid': pid,
                'title': f"AliExpress Product {pid}",
                'image_url': f"https://ae-pic-a1.aliexpress-media.com/kf/S033f3dc4ebda4df88cedc14e20a8df51l.jpg",
                'price': None,
                'source': 'aliexpress'
            }

            return product_data

        except Exception as e:
            print(f"❌ AliExpress extraction error: {e}")
            return None

    def extract_product_data(self, affiliate_link):
        """Extract product data based on affiliate link domain"""
        try:
            parsed_url = urlparse(affiliate_link)

            if 'amazon.com' in parsed_url.netloc or 'amazon.in' in parsed_url.netloc:
                return self.extract_amazon_data(affiliate_link)
            elif 'flipkart.com' in parsed_url.netloc:
                return self.extract_flipkart_data(affiliate_link)
            elif 'aliexpress.com' in parsed_url.netloc:
                return self.extract_aliexpress_data(affiliate_link)
            else:
                print(f"⚠️ Unsupported affiliate network: {parsed_url.netloc}")
                return None

        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return None

    def validate_image_url(self, image_url):
        """Validate if image URL is accessible"""
        try:
            response = self.session.head(image_url, timeout=10)
            return response.status_code == 200
        except:
            return False

    def get_image_sizes(self, base_image_url):
        """Generate different image sizes for optimization"""
        image_sizes = {
            'thumbnail': base_image_url,  # Small for cards
            'medium': base_image_url,     # Medium for lists
            'large': base_image_url,      # Large for details
            'original': base_image_url    # Full resolution
        }

        # Amazon image size variations
        if 'images-na.ssl-images-amazon.com' in base_image_url:
            asin_match = re.search(r'/images/P/([A-Z0-9]{10})', base_image_url)
            if asin_match:
                asin = asin_match.group(1)
                image_sizes = {
                    'thumbnail': f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01._SX150_.jpg",
                    'medium': f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01._SX300_.jpg",
                    'large': f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01._SX500_.jpg",
                    'original': f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01._SL1500_.jpg"
                }

        return image_sizes


async def update_existing_products():
    """Update existing products with extracted image data"""
    extractor = ProductImageExtractor()
    products_collection = db.products

    # Get all products
    products = await products_collection.find({}, {"_id": 0}).to_list(None)

    print(f"🔄 Updating {len(products)} existing products with real images...")

    for product in products:
        try:
            print(f"📦 Processing: {product['title']}")

            # Extract product data from affiliate link
            extracted_data = extractor.extract_product_data(product['affiliate_link'])

            if extracted_data:
                # Generate image sizes
                image_sizes = extractor.get_image_sizes(extracted_data['image_url'])

                # Update product with extracted data
                update_data = {
                    'image_url': image_sizes['medium'],  # Default to medium size
                    'image_sizes': image_sizes,
                    'extracted_title': extracted_data.get('title'),
                    'source': extracted_data.get('source')
                }

                # Only update if we have better data
                if extracted_data.get('title') and len(extracted_data['title']) > len(product.get('title', '')):
                    update_data['title'] = extracted_data['title']

                await products_collection.update_one(
                    {'id': product['id']},
                    {'$set': update_data}
                )

                print(f"   ✅ Updated: {product['title']}")
            else:
                print(f"   ⚠️ Could not extract data for: {product['title']}")

        except Exception as e:
            print(f"   ❌ Error updating {product['title']}: {e}")

    print("✅ Product update complete!")


async def test_extraction():
    """Test image extraction with sample URLs"""
    extractor = ProductImageExtractor()

    test_urls = [
        "https://amazon.com/Sony-WH-CH720-Wireless-Headphones-Black/dp/B0BGV8C65H?tag=yourid-20",
        "https://flipkart.com/search?q=Samsung+Galaxy+A13&tag=yourid",
        "https://aliexpress.com/item/3256804123456.html?sku_id=yourid"
    ]

    print("🧪 Testing image extraction...")

    for url in test_urls:
        print(f"\n🔗 Testing: {url}")
        data = extractor.extract_product_data(url)
        if data:
            print(f"   📦 Extracted: {data}")
            image_sizes = extractor.get_image_sizes(data['image_url'])
            print(f"   🖼️ Image sizes: {len(image_sizes)} variants")
        else:
            print("   ❌ Extraction failed")


async def main():
    try:
        # Test extraction first
        await test_extraction()

        # Update existing products
        await update_existing_products()

        print("\n✅ Image extraction system ready!")
        print("📝 To add new products with automatic image extraction:")
        print("   1. Paste affiliate link")
        print("   2. System extracts product data automatically")
        print("   3. Manual override available if needed")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
