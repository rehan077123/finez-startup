import asyncio
import hashlib
import hmac
import json
import math
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

from providers.base import AffiliateProvider


def _slugify(value: str) -> str:
    v = (value or "").lower().strip()
    v = re.sub(r"[^a-z0-9\s-]", "", v)
    v = re.sub(r"[\s-]+", "-", v).strip("-")
    return v or "product"


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _get_signature_key(secret_key: str, date_stamp: str, region: str, service: str) -> bytes:
    k_date = _sign(("AWS4" + secret_key).encode("utf-8"), date_stamp)
    k_region = _sign(k_date, region)
    k_service = _sign(k_region, service)
    k_signing = _sign(k_service, "aws4_request")
    return k_signing


class AmazonPaapiProvider(AffiliateProvider):
    id = "amazon"
    name = "Amazon"

    def __init__(self) -> None:
        self._access_key = os.environ.get("AMAZON_PAAPI_ACCESS_KEY", "").strip()
        self._secret_key = os.environ.get("AMAZON_PAAPI_SECRET_KEY", "").strip()
        self._partner_tag = os.environ.get("AMAZON_PAAPI_PARTNER_TAG", os.environ.get("AMAZON_PARTNER_TAG", "finezofficial-21")).strip()
        self._host = os.environ.get("AMAZON_PAAPI_HOST", "webservices.amazon.in").strip()
        self._region = os.environ.get("AMAZON_PAAPI_REGION", "eu-west-1").strip()
        self._marketplace = os.environ.get("AMAZON_PAAPI_MARKETPLACE", "www.amazon.in").strip()

    def _assert_configured(self) -> None:
        if not self._access_key or not self._secret_key or not self._partner_tag:
            raise RuntimeError("Amazon PA-API env vars missing: AMAZON_PAAPI_ACCESS_KEY, AMAZON_PAAPI_SECRET_KEY, AMAZON_PAAPI_PARTNER_TAG")

    def _signed_headers(self, *, payload_json: str, target: str, canonical_uri: str) -> Dict[str, str]:
        amz_date = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        date_stamp = amz_date[:8]
        canonical_querystring = ""

        canonical_headers = (
            "content-encoding:amz-1.0\n"
            "content-type:application/json; charset=utf-8\n"
            f"host:{self._host}\n"
            f"x-amz-date:{amz_date}\n"
            f"x-amz-target:{target}\n"
        )
        signed_headers = "content-encoding;content-type;host;x-amz-date;x-amz-target"
        payload_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()

        canonical_request = (
            f"POST\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
        )

        algorithm = "AWS4-HMAC-SHA256"
        credential_scope = f"{date_stamp}/{self._region}/ProductAdvertisingAPI/aws4_request"
        string_to_sign = (
            f"{algorithm}\n{amz_date}\n{credential_scope}\n"
            f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
        )

        signing_key = _get_signature_key(self._secret_key, date_stamp, self._region, "ProductAdvertisingAPI")
        signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

        authorization_header = (
            f"{algorithm} Credential={self._access_key}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        )

        return {
            "Content-Encoding": "amz-1.0",
            "Content-Type": "application/json; charset=utf-8",
            "Host": self._host,
            "X-Amz-Date": amz_date,
            "X-Amz-Target": target,
            "Authorization": authorization_header,
        }

    def _search_items(self, *, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._assert_configured()
        canonical_uri = "/paapi5/searchitems"
        target = "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems"
        url = f"https://{self._host}{canonical_uri}"
        payload_json = json.dumps(payload)
        headers = self._signed_headers(payload_json=payload_json, target=target, canonical_uri=canonical_uri)
        resp = requests.post(url, data=payload_json, headers=headers, timeout=25)
        resp.raise_for_status()
        return resp.json()

    def _affiliate_url(self, asin: str) -> str:
        return f"https://www.amazon.in/dp/{asin}?tag={self._partner_tag}"

    def _map_item(
        self,
        *,
        item: Dict[str, Any],
        category: str,
        subcategory: Optional[str],
    ) -> Dict[str, Any]:
        asin = item.get("ASIN")
        title = (((item.get("ItemInfo") or {}).get("Title") or {}).get("DisplayValue")) or ""
        detail_url = item.get("DetailPageURL") or ""

        images = item.get("Images") or {}
        primary = images.get("Primary") or {}
        image_small = ((primary.get("Medium") or {}).get("URL")) or ((primary.get("Small") or {}).get("URL")) or ""
        image_full = ((primary.get("Large") or {}).get("URL")) or image_small

        offers = item.get("Offers") or {}
        listings = offers.get("Listings") or []
        first_listing = listings[0] if listings else {}
        price_obj = (first_listing.get("Price") or {})
        price_amount = price_obj.get("Amount")
        savings_obj = price_obj.get("Savings") or {}
        discount_amount = savings_obj.get("Amount")

        availability = (first_listing.get("Availability") or {}).get("Message") or ""

        reviews = item.get("CustomerReviews") or {}
        star_rating = reviews.get("StarRating")
        total_reviews = reviews.get("TotalReviews")
        try:
            rating = float(star_rating) if star_rating is not None else 0.0
        except Exception:
            rating = 0.0
        try:
            reviews_count = int(total_reviews) if total_reviews is not None else 0
        except Exception:
            reviews_count = 0

        trending_score = float(rating) * math.log(float(reviews_count) + 1.0)
        now = datetime.now(timezone.utc).isoformat()

        universal = {
            "provider": self.id,
            "category": category,
            "subcategory": subcategory,
            "title": title,
            "description": title,
            "image": image_small or image_full,
            "fullImage": image_full or image_small,
            "affiliateUrl": self._affiliate_url(asin) if asin else detail_url,
            "sourceUrl": detail_url,
            "price": float(price_amount) if price_amount is not None else None,
            "discount": float(discount_amount) if discount_amount is not None else None,
            "rating": rating,
            "reviewsCount": reviews_count,
            "badge": "Trending" if trending_score > 10 else None,
            "tags": [],
            "availability": availability or None,
            "clickCount": 0,
            "trendingScore": trending_score,
            "seoSlug": f"{_slugify(title)}-{asin}" if asin else _slugify(title),
            "featured": False,
            "createdAt": now,
            "updatedAt": now,
            "asin": asin,
        }

        compatibility = {
            "why_this_product": "Amazon trending pick",
            "benefits": "Amazon trending pick",
            "type": "affiliate",
            "affiliate_link": universal["affiliateUrl"],
            "affiliateLink": universal["affiliateUrl"],
            "affiliate_network": "Amazon",
            "image_url": universal["image"],
            "image_small": universal["image"],
            "image_full": universal["fullImage"],
            "review_count": reviews_count,
            "clicks": 0,
            "verified": True,
            "premium": False,
        }

        return {**universal, **compatibility}

    async def fetch_trending(
        self,
        *,
        category: str,
        subcategory: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        payload = {
            "PartnerTag": self._partner_tag,
            "PartnerType": "Associates",
            "Marketplace": self._marketplace,
            "ItemCount": min(max(int(limit), 1), 10),
            "Resources": [
                "ItemInfo.Title",
                "Images.Primary.Small",
                "Images.Primary.Medium",
                "Images.Primary.Large",
                "Offers.Listings.Price",
                "Offers.Listings.Availability.Message",
                "CustomerReviews.StarRating",
                "CustomerReviews.TotalReviews",
            ],
        }

        if subcategory:
            payload["Keywords"] = subcategory
        else:
            payload["Keywords"] = category

        def _call() -> Dict[str, Any]:
            return self._search_items(payload=payload)

        data = await asyncio.to_thread(_call)
        items = (data.get("SearchResult") or {}).get("Items") or []
        mapped: List[Dict[str, Any]] = []
        for item in items:
            mapped.append(self._map_item(item=item, category=category, subcategory=subcategory))
        return mapped

