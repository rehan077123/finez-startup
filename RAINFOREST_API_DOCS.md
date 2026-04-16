# Rainforest API Integration for FineZ

## Overview

Rainforest API integration has been added to FineZ backend to fetch real-time Amazon product data. This allows you to:

- Fetch product details by ASIN
- Search for products on Amazon
- Track API credit usage
- Transform Amazon data into FineZ format

## Setup

1. **API Key**: The Rainforest API key is already configured in `.env`:
   ```
   RAINFOREST_API_KEY="F80EE51A48E2443D93911F9FBCAAB780"
   ```

2. **Files Added**:
   - `backend/rainforest_service.py` - Main service logic
   - API endpoints in `backend/server.py` (routes starting with `/api/products/rainforest/` and `/api/rainforest/`)

## API Endpoints

### 1. Get Product by ASIN

**Endpoint**: `GET /api/products/rainforest/asin/{asin}`

**Parameters**:
- `asin` (path) - Amazon Standard Identification Number (required)
- `domain` (query) - Amazon domain, default: "amazon.in"

**Example Request**:
```bash
curl "http://localhost:8000/api/products/rainforest/asin/B073JYC4XM?domain=amazon.in"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "title": "SanDisk 128GB Class 10 microSDXC Memory Card",
    "brand": "SanDisk",
    "asin": "B073JYC4XM",
    "price": 3100,
    "currency": "INR",
    "rating": 4.4,
    "reviews_count": 347491,
    "in_stock": true,
    "category": "Computers & Accessories",
    "image_url": "https://m.media-amazon.com/images/...",
    "url": "https://www.amazon.in/...",
    "source": "amazon",
    "platform": "amazon.in"
  },
  "raw_data": { ... },
  "timestamp": "2026-04-13T04:16:32Z"
}
```

### 2. Search Products

**Endpoint**: `GET /api/products/rainforest/search`

**Parameters**:
- `query` (query) - Search query string (required)
- `domain` (query) - Amazon domain, default: "amazon.in"
- `page` (query) - Page number (1-indexed), default: 1
- `sort_by` (query) - Sort option: RELEVANCE, LOWEST_PRICE, HIGHEST_PRICE, NEWEST, RATING_HIGH_TO_LOW

**Example Request**:
```bash
curl "http://localhost:8000/api/products/rainforest/search?query=microSD+card&domain=amazon.in&page=1&sort_by=RATING_HIGH_TO_LOW"
```

**Response**:
```json
{
  "success": true,
  "query": "microSD card",
  "page": 1,
  "count": 5,
  "results": [
    {
      "title": "SanDisk 128GB Class 10 microSDXC Memory Card",
      "brand": "SanDisk",
      "asin": "B073JYC4XM",
      "price": 3100,
      "rating": 4.4,
      "reviews_count": 347491,
      ...
    },
    ...
  ],
  "timestamp": "2026-04-13T04:16:32Z"
}
```

### 3. Check API Credits

**Endpoint**: `GET /api/rainforest/credits`

**Example Request**:
```bash
curl "http://localhost:8000/api/rainforest/credits"
```

**Response**:
```json
{
  "success": true,
  "credits": {
    "credits_used": 1,
    "credits_remaining": 99,
    "success": true
  },
  "timestamp": "2026-04-13T04:16:32Z"
}
```

## Service Methods

The `RainforestService` class in `rainforest_service.py` provides these methods:

### Static Methods

1. **`get_product_by_asin(asin, amazon_domain, include_fields)`**
   - Fetch product data by ASIN
   - Returns: Product dict or None

2. **`search_products(query, amazon_domain, page, sort_by)`**
   - Search for products
   - Returns: Search results dict or None

3. **`get_price_history(asin, amazon_domain)`**
   - Get pricing information
   - Returns: Price data dict or None

4. **`get_api_credits()`**
   - Check remaining API credits
   - Returns: Credit info dict or None

5. **`transform_product_data(rainforest_product)`**
   - Transform Rainforest product data to FineZ format
   - Returns: Transformed product dict

### Async Helpers

1. **`fetch_product_async(asin, domain)`**
   - Async wrapper for fetching products

2. **`search_products_async(query, domain, page)`**
   - Async wrapper for searching products

## Usage Examples

### Python Backend Integration

```python
from rainforest_service import RainforestService

# Fetch a product
product = RainforestService.get_product_by_asin("B073JYC4XM", "amazon.in")

if product:
    # Transform to FineZ format
    finez_product = RainforestService.transform_product_data(product)
    print(finez_product['title'])
    print(finez_product['price'])
```

### Frontend Integration (JavaScript/TypeScript)

```typescript
// Fetch product by ASIN
const fetchProduct = async (asin: string) => {
  const response = await fetch(
    `/api/products/rainforest/asin/${asin}?domain=amazon.in`
  );
  const data = await response.json();
  return data.data;
};

// Search products
const searchProducts = async (query: string) => {
  const response = await fetch(
    `/api/products/rainforest/search?query=${encodeURIComponent(query)}&sort_by=RATING_HIGH_TO_LOW`
  );
  const data = await response.json();
  return data.results;
};

// Check credits
const checkCredits = async () => {
  const response = await fetch('/api/rainforest/credits');
  const data = await response.json();
  return data.credits;
};
```

## Data Transformation

The `transform_product_data()` method converts Rainforest API response to FineZ format:

**Rainforest Fields** → **FineZ Fields**:
- `title` → `title`
- `brand` → `brand`
- `asin` → `asin`
- `link` → `url`
- `main_image.link` → `image_url`
- `rating` → `rating`
- `ratings_total` → `reviews_count`
- `buybox_winner.availability.type` → `in_stock`
- `search_alias.title` → `category`
- `feature_bullets` → `features`
- `specifications` → `specifications`

## Database Integration

To store fetched products in MongoDB:

```python
from rainforest_service import RainforestService

# Fetch and transform
product_data = RainforestService.get_product_by_asin(asin, domain)
transformed = RainforestService.transform_product_data(product_data)

# Store in MongoDB
await db.products.insert_one({
    **transformed,
    "created_at": datetime.now(timezone.utc),
    "updated_at": datetime.now(timezone.utc)
})
```

## API Credit Usage

Each request to Rainforest API uses 1 credit:
- **Plan**: 100 credits/month (starter)
- **Current Credits**: 99 remaining (used 1 for demo)
- **Cost**: Variable based on tier

Monitor credits using the `/api/rainforest/credits` endpoint.

## Error Handling

The service includes comprehensive error handling:

- Request failures are logged
- None returned on API errors
- HTTPException raised with appropriate status codes
- All errors are async-friendly

## Testing

Test the integration with curl:

```bash
# Test product fetch
curl "http://localhost:8000/api/products/rainforest/asin/B073JYC4XM"

# Test search
curl "http://localhost:8000/api/products/rainforest/search?query=iphone"

# Test credits
curl "http://localhost:8000/api/rainforest/credits"
```

## Next Steps

1. **Integrate with Database**: Store fetched products in MongoDB
2. **Cache Results**: Use Redis to cache frequent searches
3. **Batch Processing**: Create script to fetch products for specific categories
4. **Price Tracking**: Store price history over time
5. **Update Seeding**: Use Rainforest API instead of manual data
6. **Frontend Integration**: Add product search UI component

## Support

For issues or questions:
- Check `rainforest_service.py` for method documentation
- Review server logs for API errors
- Verify API key in `.env`
- Check Rainforest API credit balance
- Consume documentation at https://www.rainforestapi.com/docs
