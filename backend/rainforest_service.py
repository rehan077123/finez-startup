"""
Rainforest API Service for FineZ
Handles product data fetching from Amazon via Rainforest API
"""

import os
import logging
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio
from functools import lru_cache

logger = logging.getLogger(__name__)

RAINFOREST_API_URL = "https://api.rainforestapi.com/request"
RAINFOREST_API_KEY = os.environ.get("RAINFOREST_API_KEY", "F80EE51A48E2443D93911F9FBCAAB780")


class RainforestService:
    """Service to handle Rainforest API requests for Amazon product data."""

    @staticmethod
    def get_product_by_asin(
        asin: str,
        amazon_domain: str = "amazon.in",
        include_fields: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch product data from Amazon using ASIN via Rainforest API.
        
        Args:
            asin: Amazon Standard Identification Number
            amazon_domain: Amazon domain (default: amazon.in for India)
            include_fields: Optional specific fields to include in response
        
        Returns:
            Product data dict or None if request fails
        """
        try:
            params = {
                "api_key": RAINFOREST_API_KEY,
                "amazon_domain": amazon_domain,
                "asin": asin,
                "type": "product",
            }
            
            response = requests.get(RAINFOREST_API_URL, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get("request_info", {}).get("success"):
                logger.warning(f"Rainforest API returned unsuccessful response for ASIN {asin}")
                return None
            
            logger.info(f"Successfully fetched product data for ASIN {asin}")
            return data.get("product")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Rainforest API request failed for ASIN {asin}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error processing Rainforest API response: {str(e)}")
            return None

    @staticmethod
    def search_products(
        query: str,
        amazon_domain: str = "amazon.in",
        page: int = 1,
        sort_by: str = "RELEVANCE"
    ) -> Optional[Dict[str, Any]]:
        """
        Search for products on Amazon using keyword search.
        
        Args:
            query: Search query string
            amazon_domain: Amazon domain (default: amazon.in)
            page: Page number for pagination
            sort_by: Sort option (RELEVANCE, LOWEST_PRICE, HIGHEST_PRICE, NEWEST, RATING_HIGH_TO_LOW)
        
        Returns:
            Search results dict or None if request fails
        """
        try:
            params = {
                "api_key": RAINFOREST_API_KEY,
                "amazon_domain": amazon_domain,
                "type": "search",
                "search_term": query,
                "page": page,
                "sort_by": sort_by,
            }
            
            response = requests.get(RAINFOREST_API_URL, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get("request_info", {}).get("success"):
                logger.warning(f"Rainforest API returned unsuccessful search for query '{query}'")
                return None
            
            logger.info(f"Successfully searched products for query: {query}")
            return data.get("search_results")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Rainforest API search request failed for query '{query}': {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error processing Rainforest API search response: {str(e)}")
            return None

    @staticmethod
    def get_price_history(
        asin: str,
        amazon_domain: str = "amazon.in"
    ) -> Optional[Dict[str, Any]]:
        """
        Get price history for a product (if available).
        
        Args:
            asin: Amazon Standard Identification Number
            amazon_domain: Amazon domain
        
        Returns:
            Price history data or None
        """
        try:
            params = {
                "api_key": RAINFOREST_API_KEY,
                "amazon_domain": amazon_domain,
                "asin": asin,
                "type": "product",
            }
            
            response = requests.get(RAINFOREST_API_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            product = data.get("product")
            
            if product:
                # Extract pricing information
                buybox = product.get("buybox_winner", {})
                pricing = {
                    "asin": asin,
                    "current_price": buybox.get("price"),
                    "price_currency": buybox.get("price_currency", "INR"),
                    "availability": buybox.get("availability", {}).get("raw"),
                    "last_update": datetime.now().isoformat(),
                }
                return pricing
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching price history for ASIN {asin}: {str(e)}")
            return None

    @staticmethod
    def get_api_credits() -> Optional[Dict[str, Any]]:
        """
        Check remaining API credits for current API key.
        This is informational - actual credit check happens on each request.
        
        Returns:
            Credit info or None
        """
        try:
            # Make a minimal request to check credits
            params = {
                "api_key": RAINFOREST_API_KEY,
                "amazon_domain": "amazon.in",
                "asin": "B000000000",  # Invalid ASIN just to check credits
                "type": "product",
            }
            
            response = requests.get(RAINFOREST_API_URL, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                request_info = data.get("request_info", {})
                
                return {
                    "credits_used": request_info.get("credits_used"),
                    "credits_remaining": request_info.get("credits_remaining"),
                    "success": request_info.get("success"),
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking API credits: {str(e)}")
            return None

    @staticmethod
    def transform_product_data(rainforest_product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform Rainforest API product data to FineZ internal format.
        
        Args:
            rainforest_product: Raw product data from Rainforest API
        
        Returns:
            Transformed product data compatible with FineZ database
        """
        try:
            product = rainforest_product
            buybox = product.get("buybox_winner", {})
            
            # Extract images
            images = []
            if product.get("main_image"):
                images.append(product["main_image"]["link"])
            if product.get("images"):
                images.extend([img["link"] for img in product["images"]])
            
            # Extract rating breakdown
            rating_breakdown = product.get("rating_breakdown", {})
            
            # Build FineZ format
            return {
                "title": product.get("title"),
                "description": product.get("feature_bullets_flat", ""),
                "brand": product.get("brand"),
                "asin": product.get("asin"),
                "url": product.get("link"),
                "image_url": product.get("main_image", {}).get("link"),
                "images": images,
                "price": buybox.get("price"),
                "currency": "INR",
                "rating": product.get("rating"),
                "reviews_count": product.get("ratings_total", 0),
                "in_stock": buybox.get("availability", {}).get("type") != "out_of_stock",
                "category": product.get("search_alias", {}).get("title", "General"),
                "features": product.get("feature_bullets", []),
                "specifications": product.get("specifications", []),
                "source": "amazon",
                "platform": "amazon.in",
                "seller": buybox.get("seller_name"),
                "is_prime": buybox.get("is_prime", False),
                "rating_breakdown": rating_breakdown,
                "fetched_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error transforming product data: {str(e)}")
            return {}


# Async wrapper for integration with FastAPI
async def fetch_product_async(asin: str, domain: str = "amazon.in"):
    """Async wrapper for fetching products."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, 
        RainforestService.get_product_by_asin,
        asin,
        domain
    )


async def search_products_async(query: str, domain: str = "amazon.in", page: int = 1):
    """Async wrapper for searching products."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        RainforestService.search_products,
        query,
        domain,
        page
    )
