# Anthropic Claude AI Integration for FineZ

## Overview

Anthropic Claude AI integration has been added to FineZ backend to power intelligent features like:

- **Intent Parsing**: Understand what users really want to buy
- **Recommendations**: Personalized product suggestions
- **Product Comparison**: AI-powered detailed analysis
- **Content Generation**: Engaging product descriptions
- **Q&A Support**: Intelligent customer support
- **Sentiment Analysis**: Understand user feedback

## Setup

1. **API Key**: Configured in `.env`:
   ```
   ANTHROPIC_API_KEY="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"
   ```

2. **Files Added**:
   - `backend/anthropic_service.py` - Main service with AI methods
   - API endpoints in `backend/server.py` (routes starting with `/api/ai/`)

3. **Dependencies**:
   - `anthropic` package (included in requirements.txt)
   - Model: Claude 3.5 Sonnet (latest, most capable)

## API Endpoints

### 1. Parse Search Intent

**Endpoint**: `POST /api/ai/parse-intent`

Analyze user search query to extract intent, category, entities, and modifiers.

**Query Parameters**:
- `query` (string, required) - User's search query
- `user_id` (string, optional) - User ID for personalization

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ai/parse-intent?query=best+budget+android+phones+under+20000"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "success": true,
    "query": "best budget android phones under 20000",
    "analysis": "Primary Intent: price_comparison\nCategory: Electronics - Smartphones\nBudget: ₹5,000-₹20,000\nKey Entities: budget, android, price-range\n...",
    "model": "claude-3-5-sonnet-20241022",
    "timestamp": "2026-04-13T10:30:00"
  },
  "timestamp": "2026-04-13T10:30:00"
}
```

### 2. Get Recommendations

**Endpoint**: `POST /api/ai/recommendations`

Generate personalized product recommendations.

**Query Parameters**:
- `interests` (array of strings, required) - User interests (e.g., tech, productivity)
- `budget_min` (float, optional) - Minimum budget in INR
- `budget_max` (float, optional) - Maximum budget in INR
- `user_id` (string, optional) - User ID for history

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ai/recommendations?interests=tech&interests=productivity&budget_min=5000&budget_max=50000"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "success": true,
    "interests": ["tech", "productivity"],
    "recommendations": "Based on your interests in tech and productivity with a ₹5,000-₹50,000 budget:\n\n1. Laptops/Notebooks\n   - Budget 2-in-1s: Dell XPS 13, Lenovo Yoga\n   - Why: Perfect for productivity and portability\n...",
    "model": "claude-3-5-sonnet-20241022",
    "timestamp": "2026-04-13T10:30:00"
  },
  "timestamp": "2026-04-13T10:30:00"
}
```

### 3. Compare Products

**Endpoint**: `POST /api/ai/compare-products`

Generate detailed product comparison analysis.

**Request Body**:
```json
[
  {
    "title": "iPhone 15 Pro",
    "price": 129999,
    "rating": 4.7,
    "features": ["Dynamic Island", "A17 Pro chip", "48MP camera", "Titanium design"]
  },
  {
    "title": "Samsung S24 Ultra",
    "price": 119999,
    "rating": 4.6,
    "features": ["AMOLED display", "Snapdragon 8 Gen 3", "200MP camera", "AI features"]
  }
]
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ai/compare-products" \
  -H "Content-Type: application/json" \
  -d '[{"title": "iPhone 15 Pro", "price": 129999, "rating": 4.7}, ...]'
```

**Response**:
```json
{
  "success": true,
  "data": {
    "success": true,
    "product_count": 2,
    "comparison": "Detailed comparison table...\n\nPros:\niPhone 15 Pro:\n- Superior performance with A17 Pro\n- Better software integration\n- Excellent camera quality\n...",
    "model": "claude-3-5-sonnet-20241022",
    "timestamp": "2026-04-13T10:30:00"
  },
  "timestamp": "2026-04-13T10:30:00"
}
```

### 4. Generate Product Description

**Endpoint**: `POST /api/ai/generate-description`

Generate engaging marketing copy for products.

**Query Parameters**:
- `title` (string, required) - Product title
- `category` (string, required) - Product category
- `features` (array of strings, required) - Product features
- `price` (float, optional) - Product price

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ai/generate-description?title=iPhone+15+Pro&category=Electronics+-+Smartphones&features=Dynamic+Island&features=A17+Pro+chip&features=Titanium+design&price=129999"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "success": true,
    "title": "iPhone 15 Pro",
    "description": "Short Description (50 words):\nExperience premium innovation with iPhone 15 Pro. Powered by A17 Pro, featuring Dynamic Island, Titanium design, and revolutionary camera technology. The ultimate flagship phone for professionals.\n\nLong Description (200 words):\n...\n\nKey Selling Points:\n- Lightning-fast A17 Pro processor\n- Dynamic Island for seamless interaction\n- Professional-grade camera system\n- Premium titanium construction\n- Extended battery life\n- Advanced AI features\n\nWho Should Buy:\nProfessionals, content creators, photography enthusiasts, and those seeking premium Android alternative",
    "model": "claude-3-5-sonnet-20241022",
    "timestamp": "2026-04-13T10:30:00"
  },
  "timestamp": "2026-04-13T10:30:00"
}
```

### 5. Answer Product Question

**Endpoint**: `POST /api/ai/answer-question`

Answer customer questions about products.

**Query Parameters**:
- `question` (string, required) - Customer's question
- `product_id` (string, optional) - Product ID for context

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ai/answer-question?question=Is+this+phone+good+for+photography?"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "success": true,
    "question": "Is this phone good for photography?",
    "answer": "Haan bhai! 📸 This phone is amazing for photography!\n\nHere's why:\n\n1. **Camera Quality**: The 48MP main sensor captures incredible detail, perfect for professional-looking shots\n\n2. **Low Light Performance**: Advanced night mode means you can capture stunning photos even in dim lighting\n\n3. **Zoom Capabilities**: Optical and digital zoom let you frame shots perfectly\n\n4. **AI Enhancement**: Computational photography automatically optimizes every shot\n\n5. **Video Recording**: 4K video recording at 60fps for cinematic quality\n\nWhether you're a casual photographer or a serious content creator, this phone delivers!\n\nKya aur questions ho? 😊",
    "model": "claude-3-5-sonnet-20241022",
    "timestamp": "2026-04-13T10:30:00"
  },
  "timestamp": "2026-04-13T10:30:00"
}
```

### 6. Analyze Sentiment

**Endpoint**: `POST /api/ai/analyze-sentiment`

Analyze sentiment from user text (reviews, feedback, messages).

**Query Parameters**:
- `text` (string, required) - Text to analyze

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ai/analyze-sentiment?text=This+product+is+amazing!+Fast+delivery+and+great+quality"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "success": true,
    "text_preview": "This product is amazing! Fast delivery and great quality",
    "analysis": "Overall Sentiment: POSITIVE (95% confidence)\n\nEmotions Detected:\n- Joy/Happiness (strong)\n- Satisfaction (strong)\n- Trust (moderate)\n\nKey Topics:\n1. Product Quality - Positive perception\n2. Delivery Speed - Positive perception\n3. Overall Experience - Very Positive\n\nActionable Insights:\n- Customer is a strong advocate for the product\n- Highlight fast delivery as USP\n- Quality standards are meeting/exceeding expectations\n- Likely to give repeat business",
    "model": "claude-3-5-sonnet-20241022",
    "timestamp": "2026-04-13T10:30:00"
  },
  "timestamp": "2026-04-13T10:30:00"
}
```

## Service Methods

### AnthropicService Class

All methods are in `backend/anthropic_service.py`:

```python
from anthropic_service import AnthropicService

service = AnthropicService()

# Parse intent
result = service.parse_search_intent("best phones under 30k")

# Get recommendations
result = service.generate_product_recommendations(
    user_interests=["tech", "productivity"],
    budget_range=(10000, 100000)
)

# Compare products
result = service.compare_products([product1, product2, product3])

# Generate description
result = service.generate_product_description(
    title="Product Name",
    category="Category",
    features=["feature1", "feature2"],
    price=9999
)

# Answer question
result = service.answer_product_question("Is this good for gaming?")

# Analyze sentiment
result = service.analyze_user_sentiment("I love this product!")
```

## Frontend Integration (TypeScript/JavaScript)

```typescript
// Parse intent
const parseIntent = async (query: string) => {
  const response = await fetch(
    `/api/ai/parse-intent?query=${encodeURIComponent(query)}`,
    { method: 'POST' }
  );
  const data = await response.json();
  return data.data;
};

// Get recommendations
const getRecommendations = async (interests: string[], budgetMin: number, budgetMax: number) => {
  const params = new URLSearchParams();
  interests.forEach(i => params.append('interests', i));
  params.append('budget_min', budgetMin.toString());
  params.append('budget_max', budgetMax.toString());
  
  const response = await fetch(`/api/ai/recommendations?${params}`, { method: 'POST' });
  const data = await response.json();
  return data.data;
};

// Compare products
const compareProducts = async (products: any[]) => {
  const response = await fetch('/api/ai/compare-products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(products)
  });
  const data = await response.json();
  return data.data;
};

// Answer question
const askQuestion = async (question: string) => {
  const response = await fetch(
    `/api/ai/answer-question?question=${encodeURIComponent(question)}`,
    { method: 'POST' }
  );
  const data = await response.json();
  return data.data;
};

// Analyze sentiment
const analyzeSentiment = async (text: string) => {
  const response = await fetch(
    `/api/ai/analyze-sentiment?text=${encodeURIComponent(text)}`,
    { method: 'POST' }
  );
  const data = await response.json();
  return data.data;
};
```

## Database Integration

Store AI insights in MongoDB:

```python
from datetime import datetime, timezone

# Store analysis results
ai_analysis = {
    "type": "search_intent",
    "user_id": user_id,
    "query": "best phones under 30k",
    "intent_analysis": result.analysis,
    "created_at": datetime.now(timezone.utc),
    "model": "claude-3-5-sonnet-20241022"
}

await db.ai_analyses.insert_one(ai_analysis)

# Store sentiment analysis from reviews
sentiment_data = {
    "type": "review_sentiment",
    "product_id": product_id,
    "review_text": review_text,
    "sentiment": result.analysis,
    "created_at": datetime.now(timezone.utc)
}

await db.sentiment_analyses.insert_one(sentiment_data)
```

## Use Cases

### 1. Smart Search
- User types: "gaming laptop not too expensive"
- Intent parsing extracts: gaming, laptop, budget-conscious
- Return gaming laptops in ₹60k-₹150k range

### 2. Personalized Discovery
- User interests: [tech, productivity, gaming]
- Recommendation system suggests: gaming laptops, productivity monitors, mechanical keyboards
- Tailored to budget

### 3. Product Comparison Tool
- User selects 2-3 products to compare
- AI provides detailed analysis, pros/cons, best use cases
- Helps make informed decision

### 4. Content Generation
- Import products from Rainforest API
- Generate SEO-optimized descriptions automatically
- Maintain brand voice

### 5. Customer Support
- Auto-respond to common questions
- Provide helpful, Hinglish-friendly answers
- Route complex questions to humans

### 6. Review Analysis
- Analyze customer feedback at scale
- Identify key issues and praise
- Sentiment trends over time

### 7. Dynamic Pricing Insights
- Analyze competitor products
- Generate comparison content
- Support pricing decisions

## Rate Limits & Costs

**Claude 3.5 Sonnet Pricing** (as of April 2024):
- Input: $3 per 1M tokens
- Output: $15 per 1M tokens
- Average query: ~500 tokens input, ~500 tokens output
- Cost per request: ~$0.009

**Best Practices**:
- Cache frequently asked questions
- Batch recommendations generation
- Store results for similar queries
- Monitor token usage

## Error Handling

All routes include comprehensive error handling:

```json
{
  "success": false,
  "error": "API rate limit exceeded. Please try again later.",
  "timestamp": "2026-04-13T10:30:00"
}
```

## Testing

```bash
# Test intent parsing
curl -X POST "http://localhost:8000/api/ai/parse-intent?query=gaming+laptop"

# Test recommendations
curl -X POST "http://localhost:8000/api/ai/recommendations?interests=tech&interests=gaming"

# Test sentiment
curl -X POST "http://localhost:8000/api/ai/analyze-sentiment?text=Love+this+product"
```

## Next Steps

1. **Frontend Integration**: Build AI-powered search UI
2. **Caching Layer**: Cache intent parsing and recommendations
3. **Batch Processing**: Generate descriptions for all products
4. **Analytics Dashboard**: Track AI usage and insights
5. **A/B Testing**: Test different recommendation strategies
6. **Review System**: Automated review analysis pipeline
7. **Content Gen**: Bulk description generation for marketplace

## Support

- Anthropic Docs: https://docs.anthropic.com
- Claude API: https://console.anthropic.com
- Model Info: Claude 3.5 Sonnet (best for complex reasoning)
- Rate Limits: 50 requests/minute (standard tier)
