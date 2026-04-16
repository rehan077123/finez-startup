import re
import requests
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

AMAZON_AFFILIATE_TAG = "finezofficial-21"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

class AmazonService:
    @staticmethod
    def extract_asin(url: str) -> Optional[str]:
        """Extract ASIN from an Amazon URL."""
        if not url:
            return None
        
        asin_patterns = [
            r"/dp/([A-Z0-9]{10})",
            r"/gp/product/([A-Z0-9]{10})",
            r"/ASIN/([A-Z0-9]{10})",
            r"asin=([A-Z0-9]{10})",
        ]
        
        for pattern in asin_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None

    @staticmethod
    def generate_affiliate_link(asin: str) -> str:
        """Generate a clean Amazon India affiliate link."""
        return f"https://www.amazon.in/dp/{asin}?tag={AMAZON_AFFILIATE_TAG}"

    @staticmethod
    def verify_availability(asin: str) -> Dict[str, Any]:
        """
        Check if a product is available on Amazon India.
        Returns a dict with availability info.
        """
        url = f"https://www.amazon.in/dp/{asin}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 404:
                return {"available": False, "reason": "Page not found"}
            
            response.raise_for_status()
            html = response.text

            # Check for common unavailability markers
            unavailable_markers = [
                "currently unavailable",
                "we don't know when or if this item will be back in stock",
                "out of stock"
            ]
            
            is_unavailable = any(marker in html.lower() for marker in unavailable_markers)
            if is_unavailable:
                return {"available": False, "reason": "Currently unavailable"}

            # Check for price
            price = AmazonService._extract_price(html)
            if price is None:
                # Sometimes price is hidden for unavailable items
                return {"available": False, "reason": "No price/offer found"}

            # Check for image
            image_url = AmazonService._extract_image(html)
            if not image_url:
                return {"available": False, "reason": "No main image found"}

            # High-res image extraction
            full_image_url = AmazonService._extract_full_image(html) or image_url

            return {
                "available": True,
                "price": price,
                "image": image_url,
                "fullImage": full_image_url,
                "title": AmazonService._extract_title(html)
            }

        except Exception as e:
            logger.error(f"Error verifying ASIN {asin}: {e}")
            return {"available": False, "reason": f"Verification failed: {str(e)}"}

    @staticmethod
    def _extract_price(html: str) -> Optional[float]:
        """Extract price from Amazon product page HTML."""
        # Try different price patterns
        patterns = [
            r'<span class="a-price-whole">([\d,]+)</span>',
            r'<span id="priceblock_ourprice" class="[^"]*">[^0-9]*([\d,.]+)',
            r'<span id="priceblock_dealprice" class="[^"]*">[^0-9]*([\d,.]+)',
            r'<span class="a-offscreen">[^0-9]*([\d,.]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                price_str = match.group(1).replace(',', '')
                try:
                    return float(price_str)
                except ValueError:
                    continue
        return None

    @staticmethod
    def _extract_image(html: str) -> Optional[str]:
        """Extract main product image URL."""
        # Try landing image pattern
        match = re.search(r'id="landingImage"[^>]*src="([^"]+)"', html)
        if match:
            return match.group(1)
        
        # Try JSON pattern
        match = re.search(r'"initial":\[\{"hiRes":"([^"]+)"', html)
        if match:
            return match.group(1)
            
        return None

    @staticmethod
    def _extract_full_image(html: str) -> Optional[str]:
        """Extract high-resolution image URL."""
        match = re.search(r'"imgTagWrapperId"\s*:\s*\{[^}]*"hiRes"\s*:\s*"([^"]+)"', html)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def _extract_title(html: str) -> Optional[str]:
        """Extract product title."""
        match = re.search(r'id="productTitle"[^>]*>\s*([^<]+)\s*</span>', html)
        if match:
            return match.group(1).strip()
        
        match = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
        if match:
            return match.group(1).split(':')[0].strip()
            
        return None
