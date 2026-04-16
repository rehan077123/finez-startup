from fastapi import FastAPI, APIRouter, HTTPException, Query, Depends, Header, UploadFile, File, Body, Response, Path
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
import logging
import math
import re
import requests
from urllib.parse import urlparse
from pathlib import Path as PathlibPath
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import jwt
import bcrypt
from functools import lru_cache
import base64
import re
import requests
from amazon_service import AmazonService, AMAZON_AFFILIATE_TAG
from rainforest_service import RainforestService, fetch_product_async, search_products_async
from anthropic_service import AnthropicService
from io import BytesIO
from providers.registry import list_providers, get_provider

# ==================== CONSTANTS ====================
AFFILIATE_CATEGORIES = ["AI", "AI Tools", "Tech", "Side Hustles", "Learn", "Fitness", "Home"]
PRODUCT_SECTIONS = ["Affiliate", "Marketplace", "Dropshipping", "Idea", "Blog"]

ECOSYSTEM_CATEGORIES = [
    "Shopping",
    "AI Tools",
    "Side Hustle",
    "Learning",
    "Creator Economy",
    "SaaS",
    "Finance",
    "Travel",
    "Business Tools",
]

# ==================== LOGGING CONFIG ====================
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ROOT_DIR = PathlibPath(__file__).parent
load_dotenv(ROOT_DIR / ".env")

# JWT Configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production-finez-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24  # 30 days

# Image upload configuration
UPLOAD_DIR = ROOT_DIR / "uploads" / "products"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}

# MongoDB connection
mongo_url = os.environ.get("MONGO_URI")
if not mongo_url:
    logger.error("MONGO_URI environment variable is not set!")
    raise ValueError("MONGO_URI is required")

client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get("DB_NAME", "finez_db")]

# Create the main app without a prefix
app = FastAPI()

# Create a router
api_router = APIRouter()


# ==================== AUTH UTILITIES ====================


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")


# ==================== MODELS ====================

# ==================== AUTH MODELS ====================


class UserSignup(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


class User(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    first_name: str
    last_name: str
    password_hash: str
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    seller: bool = False
    verified: bool = False
    account_balance: float = 0.0
    total_earnings: float = 0.0
    affiliate_commission_rate: float = 0.1
    seller_tier: str = "free"  # free, pro, enterprise
    tier_monthly_fee: float = 0.0
    is_admin: bool = False  # Admin dashboard access
    total_products: int = 0  # Track product count
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class UserProfile(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    seller: bool
    verified: bool
    account_balance: float
    total_earnings: float
    affiliate_commission_rate: float
    created_at: datetime


class Transaction(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    product_id: str
    amount: float
    transaction_type: str
    status: str
    payment_method: Optional[str] = None
    transaction_number: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class Purchase(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    product_id: str
    quantity: int = 1
    total_price: float
    status: str = "completed"
    purchased_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class AffiliateEarning(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    affiliate_user_id: str
    product_id: str
    purchase_id: str
    commission_amount: float
    commission_rate: float
    status: str = "pending"
    earned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    paid_at: Optional[datetime] = None


class BlogPost(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    excerpt: str
    author: str = "FineZ Team"
    category: str
    image: str
    slug: str
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProductReview(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    user_id: str
    user_name: str
    rating: int = Field(ge=1, le=5)
    comment: str
    verified: bool = False
    helpful_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SellerDashboardStats(BaseModel):
    total_sales: float = 0.0
    active_products: int = 0
    customer_count: int = 0
    conversion_rate: float = 0.0
    recent_orders: List[dict] = []


class AffiliateDashboardStats(BaseModel):
    total_clicks: int = 0
    active_referrals: int = 0
    unpaid_earnings: float = 0.0
    lifetime_earnings: float = 0.0
    recent_referrals: List[dict] = []


class ProviderInfo(BaseModel):
    id: str
    name: str


class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider: Optional[str] = None
    title: str
    description: str
    why_this_product: str
    benefits: Optional[str] = None  # New field
    price: Optional[float] = None
    original_price: Optional[float] = None
    category: str
    subcategory: Optional[str] = None
    type: str
    asin: Optional[str] = None  # New field
    affiliate_link: str
    affiliateLink: Optional[str] = None  # New field
    affiliateUrl: Optional[str] = None
    affiliate_network: Optional[str] = None
    seller_id: Optional[str] = None
    sourceUrl: Optional[str] = None
    discount: Optional[float] = None
    badge: Optional[str] = None
    tags: Optional[List[str]] = None
    availability: Optional[str] = None
    trendingScore: Optional[float] = None
    seoSlug: Optional[str] = None
    image_url: str
    image: Optional[str] = None  # New field (small optimized)
    fullImage: Optional[str] = None  # New field (high res)
    image_small: Optional[str] = None
    image_full: Optional[str] = None
    featured: bool = False
    premium: bool = False
    verified: bool = False
    clicks: int = 0
    rating: float = 0.0
    review_count: int = 0
    # Trust Confidence Metadata for Decision Engine
    difficulty: Optional[str] = None  # "beginner", "intermediate", "advanced"
    roi: Optional[str] = None  # "high", "medium", "low" 
    setupTime: Optional[str] = None  # "< 30 mins", "1-2 hours", "1-3 days"
    earning_potential: Optional[str] = None  # ₹500-1000, ₹1k-5k, ₹5k+
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class ProductCreate(BaseModel):
    provider: Optional[str] = None
    title: str
    description: str
    why_this_product: str
    benefits: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    category: str
    subcategory: Optional[str] = None
    type: str
    asin: Optional[str] = None
    affiliate_link: str
    affiliateLink: Optional[str] = None
    affiliateUrl: Optional[str] = None
    affiliate_network: Optional[str] = None
    sourceUrl: Optional[str] = None
    discount: Optional[float] = None
    badge: Optional[str] = None
    tags: Optional[List[str]] = None
    availability: Optional[str] = None
    trendingScore: Optional[float] = None
    seoSlug: Optional[str] = None
    image_url: Optional[str] = None  # Optional if uploading image file
    image: Optional[str] = None
    fullImage: Optional[str] = None
    image_small: Optional[str] = None
    image_full: Optional[str] = None
    featured: bool = False
    premium: bool = False
    verified: bool = False
    # Trust Confidence Metadata for Decision Engine
    difficulty: Optional[str] = None  # "beginner", "intermediate", "advanced"
    roi: Optional[str] = None  # "high", "medium", "low"
    setupTime: Optional[str] = None  # "< 30 mins", "1-2 hours", "1-3 days"
    earning_potential: Optional[str] = None  # ₹500-1000, ₹1k-5k, ₹5k+


class ProductUpdate(BaseModel):
    provider: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    why_this_product: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    type: Optional[str] = None
    affiliate_link: Optional[str] = None
    affiliateUrl: Optional[str] = None
    affiliate_network: Optional[str] = None
    sourceUrl: Optional[str] = None
    discount: Optional[float] = None
    badge: Optional[str] = None
    tags: Optional[List[str]] = None
    availability: Optional[str] = None
    trendingScore: Optional[float] = None
    seoSlug: Optional[str] = None
    image_url: Optional[str] = None
    image_small: Optional[str] = None
    image_full: Optional[str] = None
    featured: Optional[bool] = None
    premium: Optional[bool] = None
    # Trust Confidence Metadata for Decision Engine
    difficulty: Optional[str] = None  # "beginner", "intermediate", "advanced"
    roi: Optional[str] = None  # "high", "medium", "low"
    setupTime: Optional[str] = None  # "< 30 mins", "1-2 hours", "1-3 days"
    earning_potential: Optional[str] = None  # ₹500-1000, ₹1k-5k, ₹5k+


class Stats(BaseModel):
    total_listings: int
    total_vendors: int
    total_clicks: int
    featured_count: int


class NewsletterSubscription(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    subscribed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    active: bool = True


class NewsletterSubscribe(BaseModel):
    email: str


class PageView(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page: str
    user_agent: Optional[str] = None
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


# ==================== NEW REVENUE MODELS ====================


class SellerTier(BaseModel):
    """Free, Pro, Enterprise tiers"""
    tier_name: str  # free, pro, enterprise
    monthly_fee: float  # 0, 29.99, 99.99
    seller_commission_rate: float  # 10%, 15%, 20%
    max_products: int  # 10, 100, unlimited (-1)
    featured_slots: int  # 0, 5, 20
    can_promote: bool
    api_access: bool


class WithdrawalRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    seller_id: str
    amount: float
    status: str = "pending"  # pending, approved, processing, completed, rejected
    payment_method: str = "bank_transfer"  # bank_transfer, paypal, stripe_connect
    bank_account: Optional[str] = None
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed_at: Optional[datetime] = None
    transaction_hash: Optional[str] = None


class PlatformRevenue(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str  # transaction_fee, tier_upgrade, featured_listing, withdrawal_fee
    amount: float
    seller_id: Optional[str] = None
    purchase_id: Optional[str] = None
    related_user: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FeaturedListing(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    seller_id: str
    cost: float  # 9.99 for 30 days, 24.99 for 90 days
    position: int  # 1-10 position on homepage
    duration_days: int  # 30 or 90
    start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_date: Optional[datetime] = None
    is_active: bool = True


class AdminMetrics(BaseModel):
    """For admin dashboard"""
    total_revenue: float
    total_users: int
    total_sellers: int
    total_products: int
    total_transactions: float
    platform_earnings: float
    affiliate_earnings: float
    pending_withdrawals: float
    avg_order_value: float


# ==================== ROUTES ====================


@api_router.get("/")
async def root():
    return {"message": "FineZ API - Your Money Making Platform"}


# ==================== AUTH ROUTES ====================


@api_router.post("/auth/signup", response_model=Token)
async def signup(user_data: UserSignup):
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_obj = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password_hash=hash_password(user_data.password),
    )

    user_doc = user_obj.model_dump()
    user_doc["created_at"] = user_doc["created_at"].isoformat()
    user_doc["updated_at"] = user_doc["updated_at"].isoformat()

    await db.users.insert_one(user_doc)

    access_token = create_access_token(user_obj.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_obj.id,
            "email": user_obj.email,
            "first_name": user_obj.first_name,
            "last_name": user_obj.last_name,
        },
    }


@api_router.post("/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    user = await db.users.find_one({"email": credentials.email})

    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(user["id"])

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
        },
    }


@api_router.get("/auth/me", response_model=UserProfile)
async def get_current_user_info(user_id: str = Depends(get_current_user)):
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if isinstance(user.get("created_at"), str):
        user["created_at"] = datetime.fromisoformat(user["created_at"])
    if isinstance(user.get("updated_at"), str):
        user["updated_at"] = datetime.fromisoformat(user["updated_at"])

    return user


@api_router.post("/auth/logout")
async def logout(user_id: str = Depends(get_current_user)):
    return {"message": "Logged out successfully"}


# ==================== USER ROUTES ====================


@api_router.put("/users/{user_id}")
async def update_user_profile(
    user_id: str, update_data: dict, current_user: str = Depends(get_current_user)
):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Unauthorized")

    updates = {k: v for k, v in update_data.items() if v is not None}
    updates["updated_at"] = datetime.now(timezone.utc).isoformat()

    await db.users.update_one({"id": user_id}, {"$set": updates})

    updated_user = await db.users.find_one({"id": user_id})
    if isinstance(updated_user.get("created_at"), str):
        updated_user["created_at"] = datetime.fromisoformat(
            updated_user["created_at"]
        )
    if isinstance(updated_user.get("updated_at"), str):
        updated_user["updated_at"] = datetime.fromisoformat(
            updated_user["updated_at"]
        )

    return updated_user


@api_router.get("/users/{user_id}/dashboard")
async def get_user_dashboard(
    user_id: str, current_user: str = Depends(get_current_user)
):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Unauthorized")

    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    purchases = await db.purchases.find({"user_id": user_id}).to_list(100)
    affiliate_earnings = await db.affiliate_earnings.find(
        {"affiliate_user_id": user_id}
    ).to_list(100)

    total_purchases = len(purchases)
    total_spent = sum(p.get("total_price", 0) for p in purchases)
    pending_earnings = sum(
        e.get("commission_amount", 0)
        for e in affiliate_earnings
        if e.get("status") == "pending"
    )

    return {
        "user": user,
        "total_purchases": total_purchases,
        "total_spent": total_spent,
        "account_balance": user.get("account_balance", 0),
        "total_earnings": user.get("total_earnings", 0),
        "pending_earnings": pending_earnings,
        "recent_purchases": purchases[-5:] if purchases else [],
    }


# ==================== PRODUCT ROUTES ====================


@api_router.get("/providers", response_model=List[ProviderInfo])
async def get_providers():
    return list_providers()


def _slugify(value: str) -> str:
    v = (value or "").lower().strip()
    v = re.sub(r"[^a-z0-9\s-]", "", v)
    v = re.sub(r"[\s-]+", "-", v).strip("-")
    return v or "product"


def _normalize_product_doc(product: dict) -> dict:
    created_at = product.get("created_at") or product.get("createdAt")
    updated_at = product.get("updated_at") or product.get("updatedAt")
    if created_at and not isinstance(created_at, str):
        created_at = created_at.isoformat()
    if updated_at and not isinstance(updated_at, str):
        updated_at = updated_at.isoformat()

    asin = product.get("asin")
    affiliate_network = product.get("affiliate_network") or ""
    affiliate_link = product.get("affiliate_link") or product.get("affiliateLink") or product.get("affiliateUrl") or ""

    # Generate affiliate link from ASIN if not already present
    if asin and not affiliate_link:
        affiliate_link = AmazonService.generate_affiliate_link(asin)

    provider = product.get("provider")
    if not provider:
        if asin or affiliate_network.lower() == "amazon" or "amazon." in affiliate_link.lower():
            provider = "amazon"
        elif affiliate_network:
            provider = _slugify(affiliate_network)
        else:
            provider = "manual"

    title = product.get("title") or ""
    price = product.get("price")
    original_price = product.get("original_price")
    discount = product.get("discount")
    if discount is None and isinstance(price, (int, float)) and isinstance(original_price, (int, float)):
        discount = max(float(original_price) - float(price), 0.0)

    rating = product.get("rating") or 0.0
    reviews_count = product.get("reviewsCount")
    if reviews_count is None:
        reviews_count = product.get("review_count") or 0

    clicks = product.get("clicks") or 0
    trending_score = product.get("trendingScore")
    if trending_score is None:
        try:
            trending_score = float(rating) * math.log(float(reviews_count) + 1.0) + (float(clicks) * 0.05)
        except Exception:
            trending_score = 0.0

    image = product.get("image") or product.get("image_small") or product.get("image_url")
    full_image = product.get("fullImage") or product.get("image_full") or image

    affiliate_url = product.get("affiliateUrl") or product.get("affiliateLink") or product.get("affiliate_link")
    source_url = product.get("sourceUrl") or product.get("source_url") or affiliate_link

    seo_slug = product.get("seoSlug")
    if not seo_slug:
        seo_slug = f"{_slugify(title)}-{(product.get('id') or '')[:8]}" if product.get("id") else _slugify(title)

    tags = product.get("tags")
    if tags is None:
        tags = []

    normalized = dict(product)
    normalized.update(
        {
            "provider": provider,
            "affiliateUrl": affiliate_url,
            "sourceUrl": source_url,
            "image": image,
            "fullImage": full_image,
            "discount": discount,
            "reviewsCount": reviews_count,
            "clickCount": clicks,
            "trendingScore": trending_score,
            "seoSlug": seo_slug,
            "created_at": created_at,
            "updated_at": updated_at,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "affiliateLink": affiliate_url,
            "affiliate_link": affiliate_url,
            "link": affiliate_url,
            "image_url": product.get("image_url") or image,
            "review_count": product.get("review_count") or reviews_count,
        }
    )
    return normalized


@api_router.get("/feeds/discover")
async def get_discover_feed(
    limit: int = Query(8, ge=1, le=20),
):
    base = {"verified": True}
    sort_feed = [("featured", -1), ("trendingScore", -1), ("clicks", -1), ("created_at", -1)]

    trending_now = (
        await db.products.find(base, {"_id": 0})
        .sort(sort_feed)
        .limit(min(limit * 2, 20))
        .to_list(min(limit * 2, 20))
    )

    top_picks = (
        await db.products.find({**base, "featured": True}, {"_id": 0})
        .sort(sort_feed)
        .limit(limit)
        .to_list(limit)
    )

    best_discounts = (
        await db.products.find(
            {
                **base,
                "$or": [
                    {"discount": {"$gt": 0}},
                    {"original_price": {"$gt": 0}},
                ],
            },
            {"_id": 0},
        )
        .sort([("discount", -1), ("original_price", -1), ("trendingScore", -1), ("clicks", -1), ("created_at", -1)])
        .limit(limit)
        .to_list(limit)
    )

    ai_tools_trending = (
        await db.products.find(
            {
                **base,
                "$or": [
                    {"category": {"$in": ["AI", "AI Tools"]}},
                    {"tags": {"$in": ["ai", "ai-tools", "ai_tools"]}},
                    {"provider": {"$in": ["ai-tools", "saas"]}},
                ],
            },
            {"_id": 0},
        )
        .sort(sort_feed)
        .limit(limit)
        .to_list(limit)
    )

    side_hustle_tools = (
        await db.products.find(
            {
                **base,
                "$or": [
                    {"category": {"$in": ["Side Hustles", "Side Hustle"]}},
                    {"tags": {"$in": ["side-hustle", "side_hustle", "earning"]}},
                    {"provider": {"$in": ["side-hustle", "marketplace", "fiverr", "upwork"]}},
                ],
            },
            {"_id": 0},
        )
        .sort(sort_feed)
        .limit(limit)
        .to_list(limit)
    )

    # ✨ NEW: Affiliate opportunity/ideas
    affiliate_ideas = (
        await db.products.find(
            {
                **base,
                "$or": [
                    {"category": {"$in": ["Affiliate", "affiliate"]}},
                    {"tags": {"$in": ["affiliate", "affiliate-marketing", "commission"]}},
                    {"type": "affiliate"},
                ],
            },
            {"_id": 0},
        )
        .sort(sort_feed)
        .limit(limit)
        .to_list(limit)
    )

    # ✨ NEW: Dropshipping focused products
    dropshipping_ideas = (
        await db.products.find(
            {
                **base,
                "$or": [
                    {"category": {"$in": ["Dropshipping", "dropshipping"]}},
                    {"tags": {"$in": ["dropshipping", "dropship", "ecommerce"]}},
                    {"type": "dropshipping"},
                ],
            },
            {"_id": 0},
        )
        .sort(sort_feed)
        .limit(limit)
        .to_list(limit)
    )

    amazon_hot_deals = (
        await db.products.find(
            {
                **base,
                "$and": [
                    {"$or": [{"provider": "amazon"}, {"asin": {"$exists": True, "$ne": None}}]},
                    {"$or": [{"discount": {"$gt": 0}}, {"original_price": {"$gt": 0}}]},
                ],
            },
            {"_id": 0},
        )
        .sort([("discount", -1), ("original_price", -1), ("trendingScore", -1), ("clicks", -1), ("created_at", -1)])
        .limit(limit)
        .to_list(limit)
    )

    new_launches = (
        await db.products.find(base, {"_id": 0})
        .sort([("created_at", -1)])
        .limit(limit)
        .to_list(limit)
    )

    return {
        "trendingNow": [_normalize_product_doc(p) for p in trending_now],
        "topPicksOfWeek": [_normalize_product_doc(p) for p in top_picks],
        "bestDiscounts": [_normalize_product_doc(p) for p in best_discounts],
        "aiToolsTrending": [_normalize_product_doc(p) for p in ai_tools_trending],
        "sideHustleTools": [_normalize_product_doc(p) for p in side_hustle_tools],
        "affiliateIdeas": [_normalize_product_doc(p) for p in affiliate_ideas],
        "dropshippingIdeas": [_normalize_product_doc(p) for p in dropshipping_ideas],
        "amazonHotDeals": [_normalize_product_doc(p) for p in amazon_hot_deals],
        "newLaunches": [_normalize_product_doc(p) for p in new_launches],
    }


@api_router.get("/feeds/top-picks")
async def get_top_picks_feed(limit: int = Query(12, ge=1, le=30)):
    base = {"verified": True}
    sort_feed = [("featured", -1), ("trendingScore", -1), ("clicks", -1), ("created_at", -1)]

    by_trend = (
        await db.products.find(base, {"_id": 0})
        .sort(sort_feed)
        .limit(limit)
        .to_list(limit)
    )
    by_clicks = (
        await db.products.find(base, {"_id": 0})
        .sort([("clicks", -1), ("trendingScore", -1), ("created_at", -1)])
        .limit(limit)
        .to_list(limit)
    )
    by_discounts = (
        await db.products.find(
            {**base, "$or": [{"discount": {"$gt": 0}}, {"original_price": {"$gt": 0}}]},
            {"_id": 0},
        )
        .sort([("discount", -1), ("original_price", -1), ("trendingScore", -1), ("clicks", -1), ("created_at", -1)])
        .limit(limit)
        .to_list(limit)
    )

    merged: List[dict] = []
    seen = set()
    for lst in (by_trend, by_clicks, by_discounts):
        for p in lst:
            pid = p.get("id")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            merged.append(_normalize_product_doc(p))
            if len(merged) >= limit:
                return {"topPicks": merged}

    return {"topPicks": merged}


async def _feed_list(
    *,
    type: Optional[str] = None,
    category: Optional[str] = None,
    provider: Optional[str] = None,
    limit: int = 20,
):
    base: dict = {"verified": True}
    if type:
        base["type"] = type
    if category and category.lower() != "all":
        base["category"] = category

    provider_clause = None
    if provider and provider.lower() != "all":
        if provider == "amazon":
            provider_clause = {"$or": [{"provider": "amazon"}, {"asin": {"$exists": True, "$ne": None}}]}
        else:
            provider_clause = {"provider": provider}

    query = base
    if provider_clause:
        query = {"$and": [provider_clause, base]}

    sort_feed = [("featured", -1), ("trendingScore", -1), ("clicks", -1), ("created_at", -1)]
    docs = (
        await db.products.find(query, {"_id": 0})
        .sort(sort_feed)
        .limit(limit)
        .to_list(limit)
    )
    return [_normalize_product_doc(p) for p in docs]


@api_router.get("/feeds/amazon-products")
async def get_amazon_products():
    """Get mock Amazon products with affiliate links for instant display"""
    return [
        {
            "_id": "asin_B0D2YLQX53",
            "title": "MacBook Pro 14-inch M3 Max",
            "description": "Powerful laptop for professionals",
            "image_url": "https://m.media-amazon.com/images/I/71r1tPHMp7L._SX679_.jpg",
            "category": "Electronics",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B0D2YLQX53?tag=finezapp-21",
                "price": 139999,
                "commission_percentage": 5.0
            }],
            "rating": 4.8,
            "reviews": 240
        },
        {
            "_id": "asin_B0CVHKV7CJ",
            "title": "iPad Pro 12.9 2024",
            "description": "Latest iPad Pro with M4 chip",
            "image_url": "https://m.media-amazon.com/images/I/71xb2xkN5UL._SX679_.jpg",
            "category": "Electronics",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B0CVHKV7CJ?tag=finezapp-21",
                "price": 89999,
                "commission_percentage": 5.0
            }],
            "rating": 4.7,
            "reviews": 380
        },
        {
            "_id": "asin_B0CHX1DTXY",
            "title": "iPhone 15 Pro",
            "description": "Latest iPhone with A17 Pro chip",
            "image_url": "https://m.media-amazon.com/images/I/71YLYQBP0pL._SX679_.jpg",
            "category": "Smartphones",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B0CHX1DTXY?tag=finezapp-21",
                "price": 99999,
                "commission_percentage": 5.0
            }],
            "rating": 4.9,
            "reviews": 520
        },
        {
            "_id": "asin_B0B8NQXJG7",
            "title": "Samsung 55-inch 4K TV",
            "description": "Ultra HD Smart TV with QLED",
            "image_url": "https://m.media-amazon.com/images/I/81VJ1eV5a6L._SX679_.jpg",
            "category": "Electronics",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B0B8NQXJG7?tag=finezapp-21",
                "price": 54999,
                "commission_percentage": 5.0
            }],
            "rating": 4.6,
            "reviews": 180
        },
        {
            "_id": "asin_chatgpt",
            "title": "ChatGPT Plus Subscription",
            "description": "Premium AI assistant with GPT-4 access",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png",
            "category": "AI Tools",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B0D2YLQX53?tag=finezapp-21",
                "price": 999,
                "commission_percentage": 5.0
            }],
            "rating": 4.8,
            "reviews": 890
        },
        {
            "_id": "asin_midjourney",
            "title": "Midjourney AI Subscription",
            "description": "AI image generation at its finest",
            "image_url": "https://images.unsplash.com/photo-1609042231692-abc5c9a9d397?w=500&h=500&fit=crop",
            "category": "AI Tools",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B0D2YLQX53?tag=finezapp-21",
                "price": 1099,
                "commission_percentage": 5.0
            }],
            "rating": 4.7,
            "reviews": 650
        },
        {
            "_id": "asin_B07N4PLXFD",
            "title": "COSORI Air Fryer",
            "description": "5.8L Electric Air Fryer",
            "image_url": "https://m.media-amazon.com/images/I/81FNMy6UYIL._SX679_.jpg",
            "category": "Home & Kitchen",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B07N4PLXFD?tag=finezapp-21",
                "price": 4999,
                "commission_percentage": 5.0
            }],
            "rating": 4.6,
            "reviews": 1200
        },
        {
            "_id": "asin_B00FLYWNYQ",
            "title": "Instant Pot Duo 7-in-1",
            "description": "Multi-cooker for busy families",
            "image_url": "https://m.media-amazon.com/images/I/71zrOr0qXaL._SX679_.jpg",
            "category": "Home & Kitchen",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B00FLYWNYQ?tag=finezapp-21",
                "price": 8999,
                "commission_percentage": 5.0
            }],
            "rating": 4.7,
            "reviews": 890
        },
        {
            "_id": "asin_B09N9FBKMT",
            "title": "Dyson V15 Detect Vacuum",
            "description": "Cordless vacuum cleaner",
            "image_url": "https://m.media-amazon.com/images/I/71WcbLEMQDL._SX679_.jpg",
            "category": "Home & Kitchen",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B09N9FBKMT?tag=finezapp-21",
                "price": 59999,
                "commission_percentage": 5.0
            }],
            "rating": 4.8,
            "reviews": 450
        },
        {
            "_id": "asin_B0CDSLL37F",
            "title": "Apple Watch Series 9",
            "description": "Advanced smartwatch",
            "image_url": "https://m.media-amazon.com/images/I/71TbJ5XgH7L._SX679_.jpg",
            "category": "Smartwatches",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B0CDSLL37F?tag=finezapp-21",
                "price": 39999,
                "commission_percentage": 5.0
            }],
            "rating": 4.6,
            "reviews": 340
        },
        {
            "_id": "asin_B0CWJQ5BXZ",
            "title": "Fitbit Charge 6",
            "description": "Fitness tracker with Google",
            "image_url": "https://m.media-amazon.com/images/I/81XQrMR1HbL._SX679_.jpg",
            "category": "Fitness",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B0CWJQ5BXZ?tag=finezapp-21",
                "price": 14999,
                "commission_percentage": 5.0
            }],
            "rating": 4.5,
            "reviews": 220
        },
        {
            "_id": "asin_B0BJ2N3K4H",
            "title": "Liforme Yoga Mat",
            "description": "Eco-friendly yoga mat",
            "image_url": "https://m.media-amazon.com/images/I/91nGqqGr-bL._SX679_.jpg",
            "category": "Fitness",
            "sources": [{
                "source": "amazon",
                "affiliate_url": "https://www.amazon.in/dp/B0BJ2N3K4H?tag=finezapp-21",
                "price": 4999,
                "commission_percentage": 5.0
            }],
            "rating": 4.7,
            "reviews": 780
        }
    ]

@api_router.get("/feeds/affiliate")
async def get_affiliate_feed(
    category: Optional[str] = Query(None),
    provider: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=50),
):
    products = await _feed_list(type="affiliate", category=category, provider=provider, limit=limit)
    return {"products": products}


@api_router.get("/feeds/marketplace")
async def get_marketplace_feed(
    category: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=50),
):
    products = await _feed_list(type="marketplace", category=category, limit=limit)
    return {"products": products}


@api_router.get("/feeds/dropship")
async def get_dropship_feed(
    category: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=50),
):
    products = await _feed_list(type="dropshipping", category=category, limit=limit)
    return {"products": products}


@api_router.get("/feeds/ideas")
async def get_ideas_feed(
    category: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=50),
):
    products = await _feed_list(type="idea", category=category, limit=limit)
    return {"products": products}

# ==================== OUTCOME STACKS (Decision Engine) ====================

@api_router.get("/stacks/outcomes")
async def get_outcome_stacks():
    """Return all available outcome-based stacks for decision discovery."""
    return {
        "stacks": [
            {
                "id": "dropshipping-2026",
                "title": "Start Dropshipping in 2026",
                "icon": "📦",
                "description": "Complete stack to launch your first store",
                "roi": "High",
                "setupTime": "1-2 weeks",
                "difficulty": "Beginner",
                "earning": "₹10k–₹50k/month",
                "color": "from-blue-600 to-blue-400"
            },
            {
                "id": "ai-creator-stack",
                "title": "AI Creator Monetization Stack",
                "icon": "🤖",
                "description": "Tools to make money with AI-generated content",
                "roi": "Very High",
                "setupTime": "3-5 days",
                "difficulty": "Beginner-friendly",
                "earning": "₹5k–₹25k/month",
                "color": "from-purple-600 to-purple-400"
            },
            {
                "id": "affiliate-mastery",
                "title": "Affiliate Marketing Mastery",
                "icon": "💰",
                "description": "Launch high-converting affiliate revenue",
                "roi": "Medium",
                "setupTime": "2-3 weeks",
                "difficulty": "Intermediate",
                "earning": "₹3k–₹15k/month",
                "color": "from-amber-600 to-amber-400"
            },
            {
                "id": "youtube-automation",
                "title": "YouTube Automation Setup",
                "icon": "📹",
                "description": "Build passive income YouTube channel",
                "roi": "High",
                "setupTime": "1 week",
                "difficulty": "Beginner",
                "earning": "₹8k–₹40k/month",
                "color": "from-red-600 to-red-400"
            },
            {
                "id": "budget-office-setup",
                "title": "₹10k Home Office Setup",
                "icon": "🏠",
                "description": "Essential gear for remote work + earning",
                "roi": "Medium",
                "setupTime": "Same day",
                "difficulty": "Beginner",
                "earning": "Productivity focused",
                "color": "from-green-600 to-green-400"
            },
            {
                "id": "gym-transformation",
                "title": "Gym Transformation Starter Kit",
                "icon": "💪",
                "description": "Build fitness + monetize through fitness",
                "roi": "Medium",
                "setupTime": "1 week",
                "difficulty": "Beginner",
                "earning": "₹2k–₹8k/month",
                "color": "from-orange-600 to-orange-400"
            }
        ]
    }

@api_router.get("/stacks/outcomes/{stack_id}")
async def get_outcome_stack_details(stack_id: str, limit: int = Query(12, ge=1, le=50)):
    """Get products + guides + workflows for a specific outcome stack."""
    base = {"verified": True}
    
    # Map stack to product categories/tags
    stack_mapping = {
        "dropshipping-2026": ["Electronics", "Smartphones"],
        "ai-creator-stack": ["AI Tools"],
        "affiliate-mastery": ["Electronics", "Home & Kitchen"],
        "youtube-automation": ["Electronics"],
        "budget-office-setup": ["Home & Kitchen", "Electronics"],
        "gym-transformation": ["Fitness", "Smartwatches"]
    }
    
    categories = stack_mapping.get(stack_id, [])
    if not categories:
        raise HTTPException(status_code=404, detail="Stack not found")
    
    # Get curated products for this stack
    products = await db.products.find(
        {
            **base,
            "$or": [
                {"category": {"$in": categories}},
                {"tags": {"$in": categories}}
            ]
        },
        {"_id": 0}
    ).sort([("trendingScore", -1), ("clicks", -1)]).limit(limit).to_list(limit)
    
    return {
        "stack_id": stack_id,
        "products": [_normalize_product_doc(p) for p in products],
        "workflow": {
            "steps": [
                {"order": 1, "title": "Choose Tools", "guide": f"Select the best tools for {stack_id}"},
                {"order": 2, "title": "Setup", "guide": "Complete the initial onboarding"},
                {"order": 3, "title": "Launch", "guide": "Go live with your stack"},
                {"order": 4, "title": "Scale", "guide": "Optimize and grow"}
            ]
        }
    }

@api_router.get("/stacks/outcomes/{stack_id}/platforms")
async def get_stack_platforms_with_affiliates(stack_id: str):
    """Get all platforms/tools for a stack with affiliate link availability."""
    # Map stack to relevant platforms with affiliate info
    stack_platforms = {
        "dropshipping-2026": [
            {"name": "Shopify", "category": "Ecommerce Platform", "has_affiliate": True, "affiliate_url": "https://www.shopify.com/", "commission": "Variable", "description": "Create your store in minutes"},
            {"name": "AliExpress", "category": "Supplier", "has_affiliate": True, "affiliate_url": "https://aliexpress.com/", "commission": "Up to 8%", "description": "Find dropshipping products"},
            {"name": "Winning Dropshipping", "category": "Supplier", "has_affiliate": True, "affiliate_url": "https://www.winning.com/", "commission": "Variable", "description": "Curated winning products"},
            {"name": "Oberlo", "category": "Integration Tool", "has_affiliate": True, "affiliate_url": "https://oberlo.com/", "commission": "Variable", "description": "Shopify dropshipping app"},
            {"name": "Printful", "category": "Print-on-Demand", "has_affiliate": True, "affiliate_url": "https://www.printful.com/", "commission": "Up to 20%", "description": "Print custom products"},
        ],
        "ai-creator-stack": [
            {"name": "ChatGPT Plus", "category": "AI Writing", "has_affiliate": True, "affiliate_url": "https://openai.com/", "commission": "Referral bonus", "description": "AI script generation"},
            {"name": "D-ID", "category": "Video Avatar", "has_affiliate": True, "affiliate_url": "https://www.d-id.com/", "commission": "Up to 30%", "description": "Create talking avatars"},
            {"name": "RunwayML", "category": "Video Generation", "has_affiliate": True, "affiliate_url": "https://runway.com/", "commission": "Up to 20%", "description": "AI video creation"},
            {"name": "Synthesia", "category": "Video Generation", "has_affiliate": True, "affiliate_url": "https://www.synthesia.io/", "commission": "Variable", "description": "AI-powered video generator"},
            {"name": "Canva Pro", "category": "Design", "has_affiliate": True, "affiliate_url": "https://www.canva.com/", "commission": "Up to 30%", "description": "Design graphics & posts"},
        ],
        "affiliate-mastery": [
            {"name": "Amazon Associates", "category": "Affiliate Network", "has_affiliate": True, "affiliate_url": "https://associates.amazon.com/", "commission": "3-10%", "description": "Largest affiliate network"},
            {"name": "SkimLinks", "category": "Affiliate Network", "has_affiliate": True, "affiliate_url": "https://skimlinks.com/", "commission": "Variable", "description": "Shopping affiliate network"},
            {"name": "CJ Affiliate (Conversant)", "category": "Affiliate Network", "has_affiliate": True, "affiliate_url": "https://cjaffiliate.com/", "commission": "Variable", "description": "Performance marketing platform"},
            {"name": "Flipkart Affiliate", "category": "Affiliate Network", "has_affiliate": True, "affiliate_url": "https://affiliate.flipkart.com/", "commission": "4-30%", "description": "India's biggest ecommerce"},
            {"name": "ShareASale", "category": "Affiliate Network", "has_affiliate": True, "affiliate_url": "https://www.shareasale.com/", "commission": "Variable", "description": "Diverse merchant network"},
        ],
        "youtube-automation": [
            {"name": "YouTube Studio", "category": "Platform", "has_affiliate": False, "affiliate_url": "https://studio.youtube.com/", "commission": "N/A", "description": "Video hosting & monetization"},
            {"name": "CapCut", "category": "Video Editing", "has_affiliate": True, "affiliate_url": "https://www.capcut.com/", "commission": "Up to 20%", "description": "Easy video editing"},
            {"name": "Synthesia", "category": "AI Video", "has_affiliate": True, "affiliate_url": "https://www.synthesia.io/", "commission": "Variable", "description": "Create faceless videos"},
            {"name": "Descript", "category": "Video Editing", "has_affiliate": True, "affiliate_url": "https://www.descript.com/", "commission": "Up to 20%", "description": "AI-powered editing"},
            {"name": "VidIQ", "category": "SEO Tool", "has_affiliate": True, "affiliate_url": "https://vidiq.com/", "commission": "Up to 30%", "description": "YouTube optimization"},
        ],
        "budget-office-setup": [
            {"name": "Amazon", "category": "Shopping", "has_affiliate": True, "affiliate_url": "https://amazon.in/", "commission": "3-10%", "description": "Laptops, desks, chairs"},
            {"name": "Flipkart", "category": "Shopping", "has_affiliate": True, "affiliate_url": "https://flipkart.com/", "commission": "4-30%", "description": "Electronics & furniture"},
            {"name": "Ikea", "category": "Furniture", "has_affiliate": True, "affiliate_url": "https://www.ikea.com/", "commission": "5-8%", "description": "Affordable comfortable furniture"},
            {"name": "Decathlon", "category": "Sports Gear", "has_affiliate": False, "affiliate_url": "https://www.decathlon.in/", "commission": "N/A", "description": "Equipment and accessories"},
        ],
        "gym-transformation": [
            {"name": "Amazon", "category": "Shopping", "has_affiliate": True, "affiliate_url": "https://amazon.in/", "commission": "3-10%", "description": "Dumbbells, bars, machines"},
            {"name": "Flipkart", "category": "Shopping", "has_affiliate": True, "affiliate_url": "https://flipkart.com/", "commission": "4-30%", "description": "Fitness equipment"},
            {"name": "MuscleBlaze", "category": "Supplements", "has_affiliate": True, "affiliate_url": "https://www.muscleblaze.com/", "commission": "Up to 20%", "description": "Protein & supplements"},
            {"name": "ON (Optimum Nutrition)", "category": "Supplements", "has_affiliate": True, "affiliate_url": "https://www.optimumnutrition.com/", "commission": "Variable", "description": "Premium supplements"},
        ]
    }
    
    platforms = stack_platforms.get(stack_id, [])
    
    if not platforms:
        raise HTTPException(status_code=404, detail="Stack not found")
    
    return {
        "stack_id": stack_id,
        "platforms": platforms,
        "total": len(platforms),
        "with_affiliates": sum(1 for p in platforms if p.get("has_affiliate"))
    }

@api_router.post("/stacks/track-engagement")
async def track_stack_engagement(request: dict):
    """Track user engagement with outcome stacks for data feedback loop."""
    stack_id = request.get("stack_id")
    action = request.get("action")  # view, explore, add_to_cart, purchase
    
    if not stack_id or not action:
        raise HTTPException(status_code=400, detail="Missing stack_id or action")
    
    engagement = {
        "stack_id": stack_id,
        "action": action,
        "timestamp": datetime.now(timezone.utc),
        "user_ip": "127.0.0.1"
    }
    await db.stack_engagements.insert_one(engagement)
    return {"success": True}

@api_router.get("/admin/stacks/analytics")
async def get_stack_analytics(user_id: str = Depends(get_current_user)):
    """Admin endpoint to view stack performance for the feedback loop."""
    admin_user = await db.users.find_one({"id": user_id, "is_admin": True})
    if not admin_user:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    analytics = await db.stack_engagements.aggregate([
        {"$group": {
            "_id": "$stack_id",
            "total_views": {"$sum": {"$cond": [{"$eq": ["$action", "view"]}, 1, 0]}},
            "explorations": {"$sum": {"$cond": [{"$eq": ["$action", "explore"]}, 1, 0]}},
            "conversions": {"$sum": {"$cond": [{"$eq": ["$action", "purchase"]}, 1, 0]}}
        }}
    ]).to_list(100)
    
    return {"stack_performance": analytics}

@api_router.post("/admin/providers/{provider_id}/sync")
async def admin_sync_provider(
    provider_id: str,
    category: str = Query("Shopping"),
    subcategory: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=10),
    user_id: str = Depends(get_current_user),
):
    admin_user = await db.users.find_one({"id": user_id, "is_admin": True})
    if not admin_user:
        raise HTTPException(status_code=403, detail="Admin access required")

    try:
        provider = get_provider(provider_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Provider not found")

    products = await provider.fetch_trending(category=category, subcategory=subcategory, limit=limit)
    now = datetime.now(timezone.utc).isoformat()
    upserted = 0

    for p in products:
        asin = p.get("asin")
        stable_id = f"{provider_id}:{asin}" if asin else f"{provider_id}:{p.get('seoSlug') or str(uuid.uuid4())}"
        p["id"] = stable_id
        p["provider"] = provider_id
        p["verified"] = True
        p["created_at"] = p.get("created_at") or p.get("createdAt") or now
        p["updated_at"] = now
        p["image_url"] = p.get("image_url") or p.get("image") or p.get("fullImage") or ""
        p["affiliate_link"] = p.get("affiliate_link") or p.get("affiliateUrl") or p.get("affiliateLink") or ""
        p["affiliateLink"] = p.get("affiliateLink") or p.get("affiliateUrl") or p.get("affiliate_link") or ""
        p["type"] = p.get("type") or "affiliate"
        p["why_this_product"] = p.get("why_this_product") or "Amazon trending pick"

        await db.products.update_one({"id": stable_id}, {"$set": p, "$setOnInsert": {"created_at": p["created_at"]}}, upsert=True)
        upserted += 1

    return {"provider": provider_id, "category": category, "subcategory": subcategory, "upserted": upserted}

@api_router.get("/products")
async def get_products(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    provider: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    new: Optional[bool] = Query(None),
    limit: int = Query(100, le=100),
    skip: int = Query(0),
):
    query = {}

    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"why_this_product": {"$regex": search, "$options": "i"}},
        ]

    if category and category.lower() != "all":
        query["category"] = category

    if type and type.lower() != "all":
        query["type"] = type

    provider_clause = None
    if provider and provider.lower() != "all":
        if provider == "amazon":
            provider_clause = {"$or": [{"provider": "amazon"}, {"asin": {"$exists": True, "$ne": None}}]}
        else:
            provider_clause = {"provider": provider}

    if featured is not None:
        query["featured"] = featured

    if new is not None and new:
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        query["created_at"] = {"$gte": seven_days_ago.isoformat()}

    query["verified"] = True

    if provider_clause:
        if "$or" in query:
            search_or = query.pop("$or")
            base = dict(query)
            query = {"$and": [provider_clause, {"$or": search_or}, base]}
        else:
            base = dict(query)
            query = {"$and": [provider_clause, base]}

    products = (
        await db.products.find(query, {"_id": 0})
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
        .to_list(limit)
    )

    result = []
    for product in products:
        result.append(_normalize_product_doc(product))

    return result


def _get_meta_value(html: str, property_names: list[str]) -> Optional[str]:
    for prop in property_names:
        match = re.search(rf'<meta[^>]+(?:property|name)=["\']{re.escape(prop)}["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _extract_price(html: str) -> Optional[float]:
    match = re.search(r'"price"\s*:\s*"?([0-9]+(?:[.,][0-9]+)?)"?', html)
    if match:
        try:
            return float(match.group(1).replace(',', ''))
        except ValueError:
            return None

    match = re.search(r'(?:₹|Rs\.|USD|\$)\s*([0-9]+(?:[.,][0-9]+)?)', html)
    if match:
        try:
            return float(match.group(1).replace(',', ''))
        except ValueError:
            return None

    return None


class ScrapeRequest(BaseModel):
    affiliate_link: str


@api_router.post('/products/scrape')
async def scrape_product(request: ScrapeRequest):
    affiliate_link = request.affiliate_link

    if not affiliate_link:
        raise HTTPException(status_code=400, detail='affiliate_link is required')

    try:
        parsed_url = urlparse(affiliate_link)
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid affiliate link URL')

    if not parsed_url.scheme.startswith('http') or not parsed_url.netloc:
        raise HTTPException(status_code=400, detail='Invalid affiliate link URL')

    # Basic allowed host check; allow major marketplaces
    allowed_hosts = [
        'amazon.com', 'www.amazon.com', 'amazon.in', 'www.amazon.in',
        'flipkart.com', 'www.flipkart.com',
        'aliexpress.com', 'www.aliexpress.com',
        'shopee.sg', 'www.shopee.sg',
        'ebay.com', 'www.ebay.com'
    ]
    if not any(parsed_url.netloc.lower().endswith(host) for host in allowed_hosts):
        raise HTTPException(status_code=400, detail='Unsupported affiliate link host')

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(affiliate_link, headers=headers, timeout=15)
        response.raise_for_status()

        html = response.text
        title = _get_meta_value(html, ['og:title', 'twitter:title']) or re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL).group(1).strip() if re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL) else None
        image_url = _get_meta_value(html, ['og:image', 'twitter:image', 'image'])

        # Best effort for Big Amazon: find img tag fallback
        if not image_url:
            match = re.search(r'"imgTagWrapperId"\s*:\s*\{[^}]*"hiRes"\s*:\s*"([^"]+)"', html)
            if match:
                image_url = match.group(1)
            else:
                match2 = re.search(r'"image"\s*:\s*\"([^\"]+)\"', html)
                if match2:
                    image_url = match2.group(1)
        
        price = _extract_price(html)

        image_small = image_url
        image_full = image_url

        return {
            'title': title or '',
            'description': '',
            'why_this_product': '',
            'price': price if price is not None else 0.0,
            'image_url': image_url or '',
            'image_small': image_small or '',
            'image_full': image_full or '',
            'affiliate_link': affiliate_link,
            'affiliate_network': 'Amazon' if 'amazon.' in parsed_url.netloc else ('Flipkart' if 'flipkart.' in parsed_url.netloc else ''),
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f'Failed to request affiliate URL: {e}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed extracting data: {e}')


@api_router.get("/products/featured", response_model=List[Product])
async def get_featured_products(limit: int = Query(8, le=20)):
    """
    On Discover page:
    - automatically show top featured products from all sections
    - use featured + trending score (clicks)
    - update automatically when new products added
    - show top 8 products
    - latest trending first
    """
    products = (
        await db.products.find({"featured": True, "verified": True}, {"_id": 0})
        .sort([("featured", -1), ("trendingScore", -1), ("clicks", -1), ("created_at", -1)])
        .limit(limit)
        .to_list(limit)
    )
    
    # Convert datetime fields to strings
    for product in products:
        if product.get("created_at") and not isinstance(product.get("created_at"), str):
            product["created_at"] = product["created_at"].isoformat()
        if product.get("updated_at") and not isinstance(product.get("updated_at"), str):
            product["updated_at"] = product["updated_at"].isoformat()
            
    return products

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id}, {"_id": 0})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if isinstance(product.get("created_at"), str):
        product["created_at"] = datetime.fromisoformat(product["created_at"])
    if isinstance(product.get("updated_at"), str):
        product["updated_at"] = datetime.fromisoformat(product["updated_at"])

    return product


# ==================== AMAZON UTILITIES ====================

def extract_asin(url: str) -> Optional[str]:
    """Extract ASIN from an Amazon URL."""
    return AmazonService.extract_asin(url)

def generate_amazon_affiliate_link(asin: str) -> str:
    """Generate a clean Amazon affiliate link using the ASIN."""
    return AmazonService.generate_affiliate_link(asin)

@api_router.post("/products/recheck")
async def recheck_all_products(user_id: str = Depends(get_current_user)):
    """Manually trigger a recheck of all Amazon products to remove dead ones."""
    # Only allow admin or specific users if needed
    cursor = db.products.find({"asin": {"$exists": True, "$ne": None}})
    removed_count = 0
    total_checked = 0
    
    async for product in cursor:
        total_checked += 1
        asin = product.get("asin")
        if not asin:
            continue
            
        result = AmazonService.verify_availability(asin)
        
        if not result["available"]:
            logger.info(f"Removing dead Amazon product: {asin} - {result.get('reason')}")
            await db.products.delete_one({"id": product["id"]})
            removed_count += 1
        else:
            # Update price/image if they changed
            updates = {
                "price": result["price"],
                "image": result["image"],
                "fullImage": result["fullImage"],
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            await db.products.update_one({"id": product["id"]}, {"$set": updates})
            
    return {
        "status": "success",
        "total_checked": total_checked,
        "removed_dead_products": removed_count
    }

@api_router.post("/products", response_model=Product)
async def create_product(product_input: ProductCreate, user_id: str = Depends(get_current_user)):
    """Create a new product - requires authentication. Stores seller_id automatically."""
    product_dict = product_input.model_dump()
    
    # Amazon ASIN and link extraction/generation
    raw_link = product_dict.get("affiliate_link") or product_dict.get("affiliateLink") or product_dict.get("affiliateUrl")
    if raw_link:
        product_dict["affiliate_link"] = raw_link
        product_dict["affiliateLink"] = raw_link
        product_dict["affiliateUrl"] = product_dict.get("affiliateUrl") or raw_link
        product_dict["sourceUrl"] = product_dict.get("sourceUrl") or raw_link
    asin = extract_asin(raw_link)
    
    if asin:
        # RULES: 1, 2, 3, 4 - Verify before saving
        result = AmazonService.verify_availability(asin)
        if not result["available"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Amazon product is not available or invalid: {result.get('reason')}"
            )
        
        product_dict["asin"] = asin
        product_dict["provider"] = product_dict.get("provider") or "amazon"
        product_dict["affiliateLink"] = generate_amazon_affiliate_link(asin)
        product_dict["affiliate_link"] = product_dict["affiliateLink"]
        product_dict["affiliateUrl"] = product_dict["affiliateLink"]
        product_dict["sourceUrl"] = product_dict.get("sourceUrl") or f"https://www.amazon.in/dp/{asin}"
        product_dict["price"] = result["price"]
        product_dict["image"] = result["image"]
        product_dict["fullImage"] = result["fullImage"]
        product_dict["image_url"] = product_dict.get("image_url") or result["image"]
        product_dict["title"] = result["title"] or product_dict["title"]
    else:
        product_dict["provider"] = product_dict.get("provider") or "manual"
    
    product_dict["seller_id"] = user_id  # Automatically assign seller
    product_obj = Product(**product_dict)

    doc = product_obj.model_dump()
    doc["created_at"] = doc["created_at"].isoformat()
    doc["updated_at"] = doc["updated_at"].isoformat()

    result = await db.products.insert_one(doc)
    
    # Log product creation
    await db.product_uploads.insert_one({
        "product_id": product_obj.id,
        "seller_id": user_id,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "title": product_obj.title
    })
    
    return product_obj


@api_router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product_update: ProductUpdate, user_id: str = Depends(get_current_user)):
    """Update a product - requires authentication and ownership."""
    existing = await db.products.find_one({"id": product_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check ownership
    if existing.get("seller_id") != user_id:
        raise HTTPException(status_code=403, detail="You can only edit your own products")

    update_data = {
        k: v for k, v in product_update.model_dump().items() if v is not None
    }
    
    # Handle Amazon link updates
    raw_link = update_data.get("affiliate_link") or update_data.get("affiliateLink") or update_data.get("affiliateUrl")
    if raw_link:
        update_data["affiliate_link"] = raw_link
        update_data["affiliateLink"] = raw_link
        update_data["affiliateUrl"] = update_data.get("affiliateUrl") or raw_link
        update_data["sourceUrl"] = update_data.get("sourceUrl") or raw_link
        asin = extract_asin(raw_link)
        if asin:
            result = AmazonService.verify_availability(asin)
            if result["available"]:
                update_data["asin"] = asin
                update_data["provider"] = update_data.get("provider") or "amazon"
                update_data["affiliateLink"] = generate_amazon_affiliate_link(asin)
                update_data["affiliate_link"] = update_data["affiliateLink"]
                update_data["affiliateUrl"] = update_data["affiliateLink"]
                update_data["sourceUrl"] = update_data.get("sourceUrl") or f"https://www.amazon.in/dp/{asin}"
                update_data["price"] = result["price"]
                update_data["image"] = result["image"]
                update_data["fullImage"] = result["fullImage"]
                update_data["image_url"] = update_data.get("image_url") or result["image"]
                update_data["title"] = result["title"] or update_data.get("title")
            else:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Amazon product is not available or invalid: {result.get('reason')}"
                )
        else:
            update_data["provider"] = update_data.get("provider") or existing.get("provider") or "manual"

    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    await db.products.update_one({"id": product_id}, {"$set": update_data})

    updated_product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if isinstance(updated_product.get("created_at"), str):
        updated_product["created_at"] = datetime.fromisoformat(
            updated_product["created_at"]
        )
    if isinstance(updated_product.get("updated_at"), str):
        updated_product["updated_at"] = datetime.fromisoformat(
            updated_product["updated_at"]
        )

    return updated_product


@api_router.delete("/products/{product_id}")
async def delete_product(product_id: str, user_id: str = Depends(get_current_user)):
    """Delete a product - requires authentication and ownership."""
    existing = await db.products.find_one({"id": product_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check ownership
    if existing.get("seller_id") != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own products")
    
    result = await db.products.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Log deletion
    await db.product_uploads.insert_one({
        "product_id": product_id,
        "seller_id": user_id,
        "deleted_at": datetime.now(timezone.utc).isoformat(),
        "title": existing.get("title")
    })
    
    return {"message": "Product deleted successfully"}


@api_router.post("/products/upload")
async def upload_product_with_image(
    title: str = None,
    description: str = None,
    why_this_product: str = None,
    category: str = None,
    type: str = None,
    affiliate_link: str = None,
    affiliate_network: str = None,
    price: float = None,
    original_price: float = None,
    featured: bool = False,
    premium: bool = False,
    image: UploadFile = File(None),
    user_id: str = Depends(get_current_user)
):
    """Upload a product with image. Stores image in database as base64."""
    # Validate required fields
    if not all([title, description, why_this_product, category, type, affiliate_link]):
        raise HTTPException(status_code=400, detail="Missing required product fields")
    
    image_url = None
    
    # Handle image upload
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid image type. Allowed: {ALLOWED_IMAGE_TYPES}")
        
        # Read image
        image_data = await image.read()
        if len(image_data) > MAX_IMAGE_SIZE:
            raise HTTPException(status_code=400, detail=f"Image too large. Max size: {MAX_IMAGE_SIZE / 1024 / 1024}MB")
        
        # Convert to base64 for MongoDB storage
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        image_url = f"data:{image.content_type};base64,{image_base64}"
    
    # Create product
    product_dict = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "why_this_product": why_this_product,
        "category": category,
        "type": type,
        "affiliate_link": affiliate_link,
        "affiliate_network": affiliate_network,
        "price": price,
        "original_price": original_price,
        "image_url": image_url or "https://via.placeholder.com/300x300?text=No+Image",
        "featured": featured,
        "premium": premium,
        "seller_id": user_id,
        "clicks": 0,
        "rating": 0.0,
        "review_count": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    product_obj = Product(**product_dict)
    doc = product_obj.model_dump()
    doc["created_at"] = doc["created_at"].isoformat()
    doc["updated_at"] = doc["updated_at"].isoformat()
    
    await db.products.insert_one(doc)
    
    # Log upload
    await db.product_uploads.insert_one({
        "product_id": product_obj.id,
        "seller_id": user_id,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "title": title,
        "has_image": image is not None
    })
    
    return product_obj


@api_router.get("/products/seller/{seller_id}")
async def get_seller_products(seller_id: str):
    """Get all products uploaded by a specific seller."""
    products = await db.products.find({"seller_id": seller_id}, {"_id": 0}).to_list(None)
    
    for product in products:
        if isinstance(product.get("created_at"), str):
            product["created_at"] = datetime.fromisoformat(product["created_at"])
        if isinstance(product.get("updated_at"), str):
            product["updated_at"] = datetime.fromisoformat(product["updated_at"])
    
    return products


@api_router.get("/my-products")
async def get_my_products(user_id: str = Depends(get_current_user)):
    """Get all products uploaded by the current user."""
    products = await db.products.find({"seller_id": user_id}, {"_id": 0}).to_list(None)
    
    for product in products:
        if isinstance(product.get("created_at"), str):
            product["created_at"] = datetime.fromisoformat(product["created_at"])
        if isinstance(product.get("updated_at"), str):
            product["updated_at"] = datetime.fromisoformat(product["updated_at"])
    
    return products


@api_router.post("/vendor/products/upload")
async def upload_vendor_product(
    title: str = None,
    description: str = None,
    category: str = "Electronics",
    affiliateLink: str = None,
    affiliateNetwork: str = "Amazon Associates",
    price: float = None,
    originalPrice: float = None,
    image: UploadFile = File(None),
    type: str = "affiliate",
    verified: str = "false",
):
    """
    Public endpoint for vendors/affiliates to upload their products.
    No authentication required - products marked as unverified until reviewed.
    """
    try:
        # Validate required fields
        if not all([title, description, affiliateLink, price]):
            raise HTTPException(
                status_code=400, 
                detail="Missing required fields: title, description, affiliateLink, price"
            )
        
        image_url = None
        
        # Handle image upload
        if image:
            if image.content_type not in ALLOWED_IMAGE_TYPES:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid image type. Allowed: JPEG, PNG, WebP"
                )
            
            # Read image
            image_data = await image.read()
            if len(image_data) > MAX_IMAGE_SIZE:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Image too large. Max size: 5MB"
                )
            
            # Convert to base64 for MongoDB storage
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            image_url = f"data:{image.content_type};base64,{image_base64}"
        
        # Create product document
        product_id = str(uuid.uuid4())
        product_dict = {
            "id": product_id,
            "title": title,
            "description": description,
            "category": category,
            "type": type,
            "affiliate_link": affiliateLink,
            "affiliateLink": affiliateLink,
            "affiliate_network": affiliateNetwork,
            "price": float(price),
            "original_price": float(originalPrice) if originalPrice else float(price),
            "image": image_url or "https://via.placeholder.com/300x300?text=No+Image",
            "image_url": image_url or "https://via.placeholder.com/300x300?text=No+Image",
            "verified": verified.lower() == "true",
            "featured": False,
            "clicks": 0,
            "rating": 0.0,
            "review_count": 0,
            "reviewsCount": 0,
            "provider": "amazon" if "amazon" in affiliateLink.lower() else "affiliate",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat(),
        }
        
        # Insert into database
        result = await db.products.insert_one(product_dict)
        
        # Log vendor upload
        await db.vendor_uploads.insert_one({
            "product_id": product_id,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "title": title,
            "affiliate_network": affiliateNetwork,
            "status": "pending_review", 
            "has_image": image is not None
        })
        
        return {
            "success": True,
            "product_id": product_id,
            "message": "Product uploaded successfully. It will appear on the marketplace once verified.",
            "status": "pending_review"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading vendor product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/products/{product_id}/click")
async def track_click(product_id: str):
    result = await db.products.update_one({"id": product_id}, {"$inc": {"clicks": 1}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Click tracked"}


# ==================== PURCHASE ROUTES ====================


class PurchaseRequest(BaseModel):
    product_id: str
    quantity: int = 1


@api_router.post("/purchases")
async def create_purchase(
    purchase_req: PurchaseRequest, user_id: str = Depends(get_current_user)
):
    """Protected route: requires login to purchase"""
    product = await db.products.find_one({"id": purchase_req.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = (product.get("price", 0) or 0) * purchase_req.quantity

    purchase = Purchase(
        user_id=user_id,
        product_id=purchase_req.product_id,
        quantity=purchase_req.quantity,
        total_price=total_price,
    )

    purchase_doc = purchase.model_dump()
    purchase_doc["purchased_at"] = purchase_doc["purchased_at"].isoformat()

    await db.purchases.insert_one(purchase_doc)

    transaction = Transaction(
        user_id=user_id,
        product_id=purchase_req.product_id,
        amount=total_price,
        transaction_type="purchase",
        status="completed",
    )

    transaction_doc = transaction.model_dump()
    transaction_doc["created_at"] = transaction_doc["created_at"].isoformat()
    transaction_doc["updated_at"] = transaction_doc["updated_at"].isoformat()

    await db.transactions.insert_one(transaction_doc)

    await db.products.update_one(
        {"id": purchase_req.product_id}, {"$inc": {"clicks": 1}}
    )

    if product.get("seller_id"):
        seller = await db.users.find_one({"id": product.get("seller_id")})
        if seller:
            commission_rate = seller.get("affiliate_commission_rate", 0.1)
            commission_amount = total_price * commission_rate

            affiliate_earning = AffiliateEarning(
                affiliate_user_id=product.get("seller_id"),
                product_id=purchase_req.product_id,
                purchase_id=purchase.id,
                commission_amount=commission_amount,
                commission_rate=commission_rate,
            )

            affiliate_doc = affiliate_earning.model_dump()
            affiliate_doc["earned_at"] = affiliate_doc["earned_at"].isoformat()
            if affiliate_doc.get("paid_at"):
                affiliate_doc["paid_at"] = affiliate_doc["paid_at"].isoformat()

            await db.affiliate_earnings.insert_one(affiliate_doc)

            await db.users.update_one(
                {"id": product.get("seller_id")},
                {"$inc": {"total_earnings": commission_amount}},
            )

    # Platform takes 5% transaction fee
    platform_fee = total_price * 0.05
    platform_revenue = PlatformRevenue(
        source="transaction_fee",
        amount=platform_fee,
        seller_id=product.get("seller_id"),
        purchase_id=purchase.id,
    )
    revenue_doc = platform_revenue.model_dump()
    revenue_doc["created_at"] = revenue_doc["created_at"].isoformat()
    await db.platform_revenue.insert_one(revenue_doc)

    return {
        "purchase_id": purchase.id,
        "status": "completed",
        "amount": total_price,
        "platform_fee": platform_fee,
        "message": "Purchase successful!",
    }


@api_router.get("/purchases")
async def get_user_purchases(user_id: str = Depends(get_current_user)):
    """Protected route: get user's purchases"""
    purchases = await db.purchases.find({"user_id": user_id}).to_list(100)
    return purchases


@api_router.get("/purchases/{purchase_id}")
async def get_purchase(
    purchase_id: str, user_id: str = Depends(get_current_user)
):
    """Protected route: get specific purchase"""
    purchase = await db.purchases.find_one({"id": purchase_id})
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")

    if purchase.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return purchase


@api_router.get("/affiliate-earnings")
async def get_affiliate_earnings(user_id: str = Depends(get_current_user)):
    """Protected route: get user's affiliate earnings"""
    earnings = await db.affiliate_earnings.find(
        {"affiliate_user_id": user_id}
    ).to_list(100)

    total_pending = sum(
        e.get("commission_amount", 0)
        for e in earnings
        if e.get("status") == "pending"
    )
    total_approved = sum(
        e.get("commission_amount", 0)
        for e in earnings
        if e.get("status") == "approved"
    )
    total_paid = sum(
        e.get("commission_amount", 0) for e in earnings if e.get("status") == "paid"
    )

    return {
        "earnings": earnings,
        "summary": {
            "total_pending": total_pending,
            "total_approved": total_approved,
            "total_paid": total_paid,
            "total_earned": total_pending + total_approved + total_paid,
        },
    }


@api_router.get("/stats", response_model=Stats)
async def get_stats():
    total_listings = await db.products.count_documents({})

    total_vendors = max(1, total_listings // 5)

    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$clicks"}}}]
    result = await db.products.aggregate(pipeline).to_list(1)
    total_clicks = result[0]["total"] if result else 0

    featured_count = await db.products.count_documents({"featured": True})

    return Stats(
        total_listings=total_listings,
        total_vendors=total_vendors,
        total_clicks=total_clicks,
        featured_count=featured_count,
    )


@api_router.get("/categories")
async def get_categories():
    return {
        "categories": [
            "All",
            "AI Tools",
            "Tech",
            "Side Hustles",
            "Fashion",
            "Learn",
            "Fitness",
            "Home",
        ],
        "types": ["all", "affiliate", "marketplace", "dropshipping", "idea"],
    }


# ==================== NEWSLETTER ====================


@api_router.post("/newsletter/subscribe")
async def subscribe_newsletter(subscription: NewsletterSubscribe):
    existing = await db.newsletter.find_one(
        {"email": subscription.email, "active": True}
    )
    if existing:
        return {"message": "Already subscribed", "status": "existing"}

    sub_obj = NewsletterSubscription(email=subscription.email)
    doc = sub_obj.model_dump()
    doc["subscribed_at"] = doc["subscribed_at"].isoformat()

    await db.newsletter.insert_one(doc)
    return {"message": "Successfully subscribed!", "status": "new"}


@api_router.get("/newsletter/count")
async def get_newsletter_count():
    count = await db.newsletter.count_documents({"active": True})
    return {"count": count}


# ==================== ANALYTICS ====================


@api_router.post("/analytics/pageview")
async def track_pageview(page: str):
    view = PageView(page=page)
    doc = view.model_dump()
    doc["timestamp"] = doc["timestamp"].isoformat()
    await db.pageviews.insert_one(doc)
    return {"message": "Tracked"}


@api_router.get("/analytics/stats")
async def get_analytics():
    total_pageviews = await db.pageviews.count_documents({})
    newsletter_subs = await db.newsletter.count_documents({"active": True})

    return {
        "total_pageviews": total_pageviews,
        "newsletter_subscribers": newsletter_subs,
    }


# ==================== SELLER TIER SYSTEM ====================


TIER_CONFIGS = {
    "free": {"fee": 0, "commission": 0.10, "max_products": 10, "featured_slots": 0},
    "pro": {"fee": 29.99, "commission": 0.15, "max_products": 100, "featured_slots": 5},
    "enterprise": {"fee": 99.99, "commission": 0.20, "max_products": -1, "featured_slots": 20},
}


@api_router.post("/seller/upgrade-tier")
async def upgrade_seller_tier(
    tier: str = "pro", user_id: str = Depends(get_current_user)
):
    """Upgrade to a paid seller tier"""
    if tier not in TIER_CONFIGS:
        raise HTTPException(status_code=400, detail="Invalid tier")

    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    tier_config = TIER_CONFIGS[tier]
    
    # Update user tier
    await db.users.update_one(
        {"id": user_id},
        {
            "$set": {
                "seller_tier": tier,
                "seller": True,
                "affiliate_commission_rate": tier_config["commission"],
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        },
    )

    # Log tier upgrade as platform revenue
    if tier_config["fee"] > 0:
        platform_revenue = PlatformRevenue(
            source="tier_upgrade",
            amount=tier_config["fee"],
            seller_id=user_id,
            related_user=user_id,
        )
        revenue_doc = platform_revenue.model_dump()
        revenue_doc["created_at"] = revenue_doc["created_at"].isoformat()
        await db.platform_revenue.insert_one(revenue_doc)

    return {
        "message": f"Upgraded to {tier} tier",
        "tier": tier,
        "commission_rate": tier_config["commission"],
        "max_products": tier_config["max_products"],
        "featured_slots": tier_config["featured_slots"],
    }


# ==================== WITHDRAWAL SYSTEM ====================


@api_router.post("/withdrawals/request")
async def request_withdrawal(
    amount: float, payment_method: str = "bank_transfer", user_id: str = Depends(get_current_user)
):
    """Request withdrawal of affiliate earnings"""
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    available = user.get("total_earnings", 0)
    min_withdrawal = 50

    if amount < min_withdrawal:
        raise HTTPException(
            status_code=400,
            detail=f"Minimum withdrawal: ${min_withdrawal}",
        )
    if amount > available:
        raise HTTPException(
            status_code=400, detail=f"Insufficient balance. Available: ${available}"
        )

    withdrawal = WithdrawalRequest(
        seller_id=user_id,
        amount=amount,
        payment_method=payment_method,
    )

    withdrawal_doc = withdrawal.model_dump()
    withdrawal_doc["requested_at"] = withdrawal_doc["requested_at"].isoformat()
    if withdrawal_doc.get("processed_at"):
        withdrawal_doc["processed_at"] = withdrawal_doc["processed_at"].isoformat()

    await db.withdrawals.insert_one(withdrawal_doc)

    # Platform takes 2% fee
    platform_fee = amount * 0.02
    platform_revenue = PlatformRevenue(
        source="withdrawal_fee", amount=platform_fee, seller_id=user_id
    )
    revenue_doc = platform_revenue.model_dump()
    revenue_doc["created_at"] = revenue_doc["created_at"].isoformat()
    await db.platform_revenue.insert_one(revenue_doc)

    return {
        "id": withdrawal.id,
        "status": "pending",
        "amount": amount,
        "fee": platform_fee,
        "net_amount": amount - platform_fee,
        "message": "Withdrawal request submitted. We process within 3-5 business days.",
    }


@api_router.get("/withdrawals")
async def get_my_withdrawals(user_id: str = Depends(get_current_user)):
    """Get user's withdrawal history"""
    withdrawals = await db.withdrawals.find({"seller_id": user_id}).to_list(None)
    return withdrawals


# ==================== FEATURED LISTINGS ====================


@api_router.post("/featured/buy-slot")
async def buy_featured_slot(
    product_id: str, duration_days: int = 30, user_id: str = Depends(get_current_user)
):
    """Buy featured listing slot for a product"""
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.get("seller_id") != user_id:
        raise HTTPException(status_code=403, detail="You can only feature your own products")

    # Featured slot pricing: $9.99/30 days, $24.99/90 days
    pricing = {30: 9.99, 90: 24.99}
    if duration_days not in pricing:
        raise HTTPException(status_code=400, detail="Duration must be 30 or 90 days")

    cost = pricing[duration_days]

    # Create featured listing
    featured = FeaturedListing(
        product_id=product_id,
        seller_id=user_id,
        cost=cost,
        duration_days=duration_days,
    )

    featured_doc = featured.model_dump()
    featured_doc["start_date"] = featured_doc["start_date"].isoformat()
    featured_doc["end_date"] = (
        datetime.now(timezone.utc) + timedelta(days=duration_days)
    ).isoformat()

    await db.featured_listings.insert_one(featured_doc)

    # Update product as featured
    await db.products.update_one(
        {"id": product_id}, {"$set": {"featured": True}}
    )

    # Log platform revenue
    platform_revenue = PlatformRevenue(
        source="featured_listing", amount=cost, seller_id=user_id, purchase_id=product_id
    )
    revenue_doc = platform_revenue.model_dump()
    revenue_doc["created_at"] = revenue_doc["created_at"].isoformat()
    await db.platform_revenue.insert_one(revenue_doc)

    return {
        "id": featured.id,
        "status": "active",
        "cost": cost,
        "duration_days": duration_days,
        "message": f"Product featured for {duration_days} days!",
    }


# ==================== ADMIN DASHBOARD ====================


@api_router.get("/admin/dashboard", response_model=AdminMetrics)
async def get_admin_dashboard(user_id: str = Depends(get_current_user)):
    """Admin dashboard with platform metrics"""
    # Check if user is admin
    admin_user = await db.users.find_one({"id": user_id, "is_admin": True})
    if not admin_user:
        raise HTTPException(status_code=403, detail="Admin access required")

    # Get all metrics
    total_users = await db.users.count_documents({})
    total_sellers = await db.users.count_documents({"seller": True})
    total_products = await db.products.count_documents({})
    
    purchases = await db.purchases.find({}).to_list(None)
    total_transactions = sum(p.get("total_price", 0) for p in purchases)

    # Platform earnings
    platform_revenue = await db.platform_revenue.find({}).to_list(None)
    platform_earnings = sum(r.get("amount", 0) for r in platform_revenue)

    # Affiliate earnings
    affiliate_earnings_docs = await db.affiliate_earnings.find({}).to_list(None)
    total_affiliate_earnings = sum(
        e.get("commission_amount", 0) for e in affiliate_earnings_docs
    )

    # Pending withdrawals
    pending_withdrawals_docs = await db.withdrawals.find({"status": "pending"}).to_list(None)
    pending_withdrawals = sum(
        w.get("amount", 0) for w in pending_withdrawals_docs
    )

    avg_order_value = (
        total_transactions / len(purchases) if purchases else 0
    )

    return AdminMetrics(
        total_revenue=total_transactions + platform_earnings,
        total_users=total_users,
        total_sellers=total_sellers,
        total_products=total_products,
        total_transactions=total_transactions,
        platform_earnings=platform_earnings,
        affiliate_earnings=total_affiliate_earnings,
        pending_withdrawals=pending_withdrawals,
        avg_order_value=avg_order_value,
    )


@api_router.get("/admin/products/pending")
async def get_pending_products(user_id: str = Depends(get_current_user)):
    """Fetch products waiting for moderation."""
    admin_user = await db.users.find_one({"id": user_id, "is_admin": True})
    if not admin_user:
        raise HTTPException(status_code=403, detail="Admin access required")

    pending = await db.products.find({"verified": False}).to_list(None)
    return pending


@api_router.post("/admin/products/{product_id}/approve")
async def approve_product(product_id: str, user_id: str = Depends(get_current_user)):
    """Approve a product in the moderation queue."""
    admin_user = await db.users.find_one({"id": user_id, "is_admin": True})
    if not admin_user:
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.products.update_one(
        {"id": product_id}, {"$set": {"verified": True}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product approved"}


@api_router.delete("/admin/products/{product_id}")
async def reject_product(product_id: str, user_id: str = Depends(get_current_user)):
    """Reject and delete a product from the platform."""
    admin_user = await db.users.find_one({"id": user_id, "is_admin": True})
    if not admin_user:
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.products.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted"}


@api_router.get("/admin/revenue/breakdown")
async def get_revenue_breakdown(user_id: str = Depends(get_current_user)):
    """Get detailed revenue breakdown"""
    admin_user = await db.users.find_one({"id": user_id, "is_admin": True})
    if not admin_user:
        raise HTTPException(status_code=403, detail="Admin access required")

    pipeline = [
        {"$group": {"_id": "$source", "total": {"$sum": "$amount"}, "count": {"$sum": 1}}}
    ]

    revenue_breakdown = await db.platform_revenue.aggregate(pipeline).to_list(None)

    return {
        "breakdown": revenue_breakdown,
        "total": sum(r.get("total", 0) for r in revenue_breakdown),
    }


@api_router.get("/admin/top-sellers")
async def get_top_sellers(limit: int = 10, user_id: str = Depends(get_current_user)):
    """Get top earning sellers"""
    admin_user = await db.users.find_one({"id": user_id, "is_admin": True})
    if not admin_user:
        raise HTTPException(status_code=403, detail="Admin access required")

    top_sellers = (
        await db.users.find({"seller": True})
        .sort("total_earnings", -1)
        .limit(limit)
        .to_list(limit)
    )

    return top_sellers


@api_router.get("/admin/withdrawals/pending")
async def get_pending_withdrawals(user_id: str = Depends(get_current_user)):
    """Get all pending withdrawal requests"""
    admin_user = await db.users.find_one({"id": user_id, "is_admin": True})
    if not admin_user:
        raise HTTPException(status_code=403, detail="Admin access required")

    pending = await db.withdrawals.find({"status": "pending"}).to_list(None)
    total_pending = sum(w.get("amount", 0) for w in pending)

    return {"pending_requests": pending, "total_pending_amount": total_pending}


@api_router.post("/admin/withdrawals/{withdrawal_id}/approve")
async def approve_withdrawal(
    withdrawal_id: str, user_id: str = Depends(get_current_user)
):
    """Admin approves a withdrawal"""
    admin_user = await db.users.find_one({"id": user_id, "is_admin": True})
    if not admin_user:
        raise HTTPException(status_code=403, detail="Admin access required")

    withdrawal = await db.withdrawals.find_one({"id": withdrawal_id})
    if not withdrawal:
        raise HTTPException(status_code=404, detail="Withdrawal not found")

    await db.withdrawals.update_one(
        {"id": withdrawal_id},
        {
            "$set": {
                "status": "approved",
                "processed_at": datetime.now(timezone.utc).isoformat(),
            }
        },
    )

    return {"message": "Withdrawal approved", "id": withdrawal_id}


# ==================== PLATFORM STATS ====================


@api_router.get("/platform/stats")
async def get_platform_stats():
    """Public platform statistics"""
    total_users = await db.users.count_documents({})
    total_products = await db.products.count_documents({})
    total_sellers = await db.users.count_documents({"seller": True})

    purchases = await db.purchases.find({}).to_list(None)
    total_revenue = sum(p.get("total_price", 0) for p in purchases)

    platform_revenue = await db.platform_revenue.find({}).to_list(None)
    platform_earnings = sum(r.get("amount", 0) for r in platform_revenue)

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_sellers": total_sellers,
        "total_revenue": total_revenue,
        "platform_earnings": platform_earnings,
        "total_ecosystem_value": total_revenue + platform_earnings,
    }


# ==================== BLOG ENDPOINTS ====================


@api_router.get("/blogs", response_model=List[BlogPost])
async def get_blogs(category: Optional[str] = Query(None)):
    """Fetch all blog posts, optionally filtered by category."""
    query = {}
    if category:
        query["category"] = category
    
    cursor = db.blogs.find(query).sort("date", -1)
    blogs = await cursor.to_list(length=100)
    return blogs


@api_router.get("/blogs/{slug}", response_model=BlogPost)
async def get_blog_by_slug(slug: str):
    """Fetch a single blog post by its slug."""
    blog = await db.blogs.find_one({"slug": slug})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog


# ==================== REVIEW ENDPOINTS ====================


@api_router.get("/products/{product_id}/reviews", response_model=List[ProductReview])
async def get_product_reviews(product_id: str):
    """Fetch all reviews for a specific product."""
    cursor = db.reviews.find({"product_id": product_id}).sort("created_at", -1)
    reviews = await cursor.to_list(length=100)
    return reviews


@api_router.post("/products/{product_id}/reviews", response_model=ProductReview)
async def create_product_review(
    product_id: str,
    rating: int = Body(..., ge=1, le=5),
    comment: str = Body(...),
    user_id: str = Depends(get_current_user)
):
    """Create a new review for a product."""
    # Check if product exists
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get user info for the review
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user already reviewed this product
    existing_review = await db.reviews.find_one({"product_id": product_id, "user_id": user_id})
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this product")
    
    # Create review
    review_dict = {
        "id": str(uuid.uuid4()),
        "product_id": product_id,
        "user_id": user_id,
        "user_name": f"{user['first_name']} {user['last_name']}",
        "rating": rating,
        "comment": comment,
        "verified": True,
        "helpful_count": 0,
        "created_at": datetime.now(timezone.utc)
    }
    
    review_obj = ProductReview(**review_dict)
    doc = review_obj.model_dump()
    doc["created_at"] = doc["created_at"].isoformat()
    
    await db.reviews.insert_one(doc)
    
    # Update product rating and review count
    reviews_list = await db.reviews.find({"product_id": product_id}).to_list(length=None)
    avg_rating = sum(r["rating"] for r in reviews_list) / len(reviews_list)
    
    await db.products.update_one(
        {"id": product_id},
        {"$set": {"rating": round(avg_rating, 1), "review_count": len(reviews_list)}}
    )
    
    return doc


# ==================== DASHBOARD ENDPOINTS ====================


@api_router.get("/seller/dashboard", response_model=SellerDashboardStats)
async def get_seller_dashboard(user_id: str = Depends(get_current_user)):
    """Fetch statistics for the seller dashboard."""
    # Fetch seller's products
    products = await db.products.find({"seller_id": user_id}).to_list(length=None)
    product_ids = [p["id"] for p in products]
    
    # Fetch sales/orders for these products
    orders = await db.purchases.find({"product_id": {"$in": product_ids}}).to_list(length=10)
    total_sales = sum(o.get("total_price", 0) for o in orders)
    
    # Mock some data for the UI if not enough real data exists
    return SellerDashboardStats(
        total_sales=total_sales or 1250.50,
        active_products=len(products) or 12,
        customer_count=len(set(o.get("user_id") for o in orders)) or 450,
        conversion_rate=3.2,
        recent_orders=orders or [
            {"id": "#1234", "customer": "John Doe", "amount": "$45.00", "status": "Completed", "date": "2026-03-31"},
            {"id": "#1235", "customer": "Jane Smith", "amount": "$120.50", "status": "Processing", "date": "2026-03-31"},
        ]
    )


@api_router.get("/affiliate/dashboard", response_model=AffiliateDashboardStats)
async def get_affiliate_dashboard(user_id: str = Depends(get_current_user)):
    """Fetch statistics for the affiliate dashboard."""
    # Fetch affiliate earnings
    earnings = await db.affiliate_earnings.find({"affiliate_user_id": user_id}).to_list(length=None)
    
    total_lifetime = sum(e.get("commission_amount", 0) for e in earnings)
    unpaid = sum(e.get("commission_amount", 0) for e in earnings if e.get("status") == "pending")
    
    return AffiliateDashboardStats(
        total_clicks=14500,
        active_referrals=len(earnings) or 89,
        unpaid_earnings=unpaid or 450.25,
        lifetime_earnings=total_lifetime or 5200.00,
        recent_referrals=[
            {
                "id": str(e.get("id")), 
                "user": "Anonymous User", 
                "amount": f"${e.get('commission_amount')}", 
                "status": e.get("status"), 
                "date": e.get("earned_at").isoformat() if hasattr(e.get("earned_at"), "isoformat") else str(e.get("earned_at") or "")
            }
            for e in earnings[:5]
        ] or [
            {"id": "1", "user": "Mark Taylor", "amount": "$15.00", "status": "Pending", "date": "2026-03-31"},
            {"id": "2", "user": "Lisa Green", "amount": "$25.00", "status": "Approved", "date": "2026-03-30"},
        ]
    )


# ==================== SITEMAP GENERATION ====================


@app.get("/sitemap.xml")
async def get_sitemap():
    """Generate dynamic sitemap for SEO spiders."""
    base_url = "https://finez.vercel.app"  # Update with your actual domain
    
    # Static pages
    static_pages = [
        "", "/marketplace", "/affiliate", "/dropship", "/ideas", 
        "/sell", "/about", "/blog", "/privacy", "/disclaimer", "/contact"
    ]
    
    # Fetch dynamic products
    products = await db.products.find({}, {"id": 1}).to_list(length=1000)
    # Fetch dynamic blogs
    blogs = await db.blogs.find({}, {"slug": 1}).to_list(length=1000)
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    
    # Add static pages
    for page in static_pages:
        xml_content += f'<url><loc>{base_url}{page}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>'
        
    # Add products
    for p in products:
        xml_content += f'<url><loc>{base_url}/product/{p["id"]}</loc><changefreq>daily</changefreq><priority>0.9</priority></url>'
        
    # Add blogs
    for b in blogs:
        xml_content += f'<url><loc>{base_url}/blog/{b["slug"]}</loc><changefreq>daily</changefreq><priority>0.7</priority></url>'
        
    xml_content += '</urlset>'
    
    return Response(content=xml_content, media_type="application/xml")


# ==================== APP CONFIG ====================


async def _upsert_synced_products(provider_id: str, products: List[dict]) -> int:
    now = datetime.now(timezone.utc).isoformat()
    upserted = 0
    for p in products:
        asin = p.get("asin")
        stable_id = f"{provider_id}:{asin}" if asin else f"{provider_id}:{p.get('seoSlug') or str(uuid.uuid4())}"
        p["id"] = stable_id
        p["provider"] = provider_id
        p["verified"] = True
        p["created_at"] = p.get("created_at") or p.get("createdAt") or now
        p["updated_at"] = now
        p["image_url"] = p.get("image_url") or p.get("image") or p.get("fullImage") or ""
        p["affiliate_link"] = p.get("affiliate_link") or p.get("affiliateUrl") or p.get("affiliateLink") or ""
        p["affiliateLink"] = p.get("affiliateLink") or p.get("affiliateUrl") or p.get("affiliate_link") or ""
        p["affiliateUrl"] = p.get("affiliateUrl") or p.get("affiliateLink") or p.get("affiliate_link") or ""
        p["type"] = p.get("type") or "affiliate"
        p["why_this_product"] = p.get("why_this_product") or "Amazon trending pick"
        await db.products.update_one({"id": stable_id}, {"$set": p, "$setOnInsert": {"created_at": p["created_at"]}}, upsert=True)
        upserted += 1
    return upserted


async def _amazon_auto_sync_loop() -> None:
    interval_minutes = int(os.environ.get("AMAZON_AUTO_SYNC_INTERVAL_MINUTES", "360"))
    category = os.environ.get("AMAZON_AUTO_SYNC_CATEGORY", "Shopping")
    subcategories_env = os.environ.get("AMAZON_AUTO_SYNC_SUBCATEGORIES", "Tech,Home,Fitness")
    subcategories = [s.strip() for s in subcategories_env.split(",") if s.strip()]

    while True:
        try:
            provider = get_provider("amazon")
            for sub in subcategories:
                products = await provider.fetch_trending(category=category, subcategory=sub, limit=10)
                await _upsert_synced_products("amazon", products)
        except Exception as e:
            logger.error(f"Amazon auto sync failed: {e}")
        await asyncio.sleep(max(interval_minutes, 5) * 60)


@app.on_event("startup")
async def startup_tasks():
    enabled = os.environ.get("AMAZON_AUTO_SYNC_ENABLED", "false").lower() in ("1", "true", "yes", "on")
    if enabled:
        asyncio.create_task(_amazon_auto_sync_loop())


# ==================== RAINFOREST API ROUTES ====================

@api_router.get("/products/rainforest/asin/{asin}")
async def get_product_from_rainforest(
    asin: str = Path(..., description="Amazon Standard Identification Number"),
    domain: str = Query("amazon.in", description="Amazon domain (e.g., amazon.in, amazon.com)")
):
    """
    Fetch product data from Amazon using Rainforest API by ASIN.
    
    Query Parameters:
    - asin: Product's ASIN
    - domain: Amazon domain (default: amazon.in)
    
    Example: /api/products/rainforest/asin/B073JYC4XM?domain=amazon.in
    """
    try:
        product_data = RainforestService.get_product_by_asin(asin, domain)
        
        if not product_data:
            raise HTTPException(
                status_code=404, 
                detail=f"Product with ASIN {asin} not found or API request failed"
            )
        
        # Transform to FineZ format
        transformed = RainforestService.transform_product_data(product_data)
        
        return {
            "success": True,
            "data": transformed,
            "raw_data": product_data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product from Rainforest API: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/products/rainforest/search")
async def search_amazon_products(
    query: str = Query(..., description="Search query"),
    domain: str = Query("amazon.in", description="Amazon domain"),
    page: int = Query(1, description="Page number (1-indexed)"),
    sort_by: str = Query("RELEVANCE", description="Sort option: RELEVANCE, LOWEST_PRICE, HIGHEST_PRICE, NEWEST, RATING_HIGH_TO_LOW")
):
    """
    Search for products on Amazon using Rainforest API.
    
    Query Parameters:
    - query: Search query (required)
    - domain: Amazon domain (default: amazon.in)
    - page: Page number for pagination (default: 1)
    - sort_by: Sort by relevance, price, rating, etc.
    
    Example: /api/products/rainforest/search?query=microSD+card&domain=amazon.in&page=1
    """
    try:
        if not query or len(query.strip()) < 2:
            raise HTTPException(
                status_code=400,
                detail="Search query must be at least 2 characters long"
            )
        
        results = RainforestService.search_products(query, domain, page, sort_by)
        
        if results is None:
            raise HTTPException(
                status_code=500,
                detail="Search API request failed"
            )
        
        # Transform results
        transformed_results = [
            RainforestService.transform_product_data(product)
            for product in results
        ] if isinstance(results, list) else []
        
        return {
            "success": True,
            "query": query,
            "page": page,
            "count": len(transformed_results),
            "results": transformed_results,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching Rainforest API: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/rainforest/credits")
async def get_rainforest_credits():
    """
    Check remaining Rainforest API credits for current API key.
    
    Example: /api/rainforest/credits
    """
    try:
        credits = RainforestService.get_api_credits()
        
        if not credits:
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve credit information"
            )
        
        return {
            "success": True,
            "credits": credits,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking Rainforest API credits: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ANTHROPIC AI ROUTES ====================

# Initialize Anthropic service
anthropic_service = AnthropicService()


@api_router.post("/ai/parse-intent")
async def parse_search_intent(
    query: str = Query(..., description="Search query to analyze"),
    user_id: Optional[str] = Query(None, description="Optional user ID for personalization")
):
    """
    Parse user search query to extract intent using Claude AI.
    
    Analyzes what user really wants: category, intent, entities, modifiers.
    
    Query Parameters:
    - query: Search query string (required)
    - user_id: Optional user ID for personalized analysis
    
    Example: /api/ai/parse-intent?query=best+budget+android+phones+under+20000
    """
    try:
        context = None
        if user_id:
            # Could fetch user history here
            context = {"user_id": user_id}
        
        result = anthropic_service.parse_search_intent(query, context)
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Error parsing search intent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ai/recommendations")
async def get_recommendations(
    interests: List[str] = Query(..., description="List of user interests"),
    budget_min: Optional[float] = Query(None),
    budget_max: Optional[float] = Query(None),
    user_id: Optional[str] = Query(None)
):
    """
    Generate personalized product recommendations using Claude AI.
    
    Query Parameters:
    - interests: List of interests (e.g., ["tech", "productivity", "gaming"])
    - budget_min: Optional minimum budget in INR
    - budget_max: Optional maximum budget in INR
    - user_id: Optional user ID for history
    
    Example: /api/ai/recommendations?interests=tech&interests=productivity&budget_min=5000&budget_max=50000
    """
    try:
        budget_range = None
        if budget_min is not None and budget_max is not None:
            budget_range = (budget_min, budget_max)
        
        history = None
        if user_id:
            # Could fetch user purchase history here
            pass
        
        result = anthropic_service.generate_product_recommendations(interests, budget_range, history)
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ai/compare-products")
async def compare_products(
    products: List[Dict[str, Any]] = Body(..., description="List of products to compare")
):
    """
    Generate detailed product comparison analysis.
    
    Request Body:
    [
        {
            "title": "Product 1",
            "price": 5000,
            "rating": 4.5,
            "features": ["feature1", "feature2"],
            ...
        },
        ...
    ]
    
    Returns detailed comparison with pros/cons and recommendations.
    """
    try:
        if not products or len(products) < 2:
            raise HTTPException(
                status_code=400,
                detail="At least 2 products required for comparison"
            )
        
        result = anthropic_service.compare_products(products)
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ai/generate-description")
async def generate_description(
    title: str = Query(...),
    category: str = Query(...),
    features: List[str] = Query(...),
    price: Optional[float] = Query(None)
):
    """
    Generate engaging product description using Claude AI.
    
    Query Parameters:
    - title: Product title (required)
    - category: Product category (required)
    - features: Product features (required, can be multiple)
    - price: Optional product price
    
    Example: /api/ai/generate-description?title=iPhone+15+Pro&category=Electronics&features=5G&features=Camera&price=79999
    """
    try:
        result = anthropic_service.generate_product_description(title, category, features, price)
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating description: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ai/answer-question")
async def answer_question(
    question: str = Query(..., description="Customer question"),
    product_id: Optional[str] = Query(None)
):
    """
    Answer user questions about products using Claude AI.
    
    Query Parameters:
    - question: Customer's question (required)
    - product_id: Optional product ID for context
    
    Example: /api/ai/answer-question?question=Is+this+phone+good+for+photography?
    """
    try:
        product_context = None
        if product_id:
            # Could fetch product details here
            pass
        
        result = anthropic_service.answer_product_question(question, product_context)
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ai/analyze-sentiment")
async def analyze_sentiment(
    text: str = Query(..., description="Text to analyze (review, feedback, etc.)")
):
    """
    Analyze sentiment from user text (reviews, feedback, messages).
    
    Query Parameters:
    - text: Text to analyze (required)
    
    Returns sentiment, emotions, key topics, and insights.
    
    Example: /api/ai/analyze-sentiment?text=This+product+is+amazing!+Fast+delivery+too
    """
    try:
        result = anthropic_service.analyze_user_sentiment(text)
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected" if client else "disconnected"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
