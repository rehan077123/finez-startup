# FINEZ: Technical Architecture for Billion-Dollar Scale

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER EXPERIENCE LAYER                     │
│  ┌────────────────┐  ┌─────────────┐  ┌──────────────────────┐  │
│  │  Web App       │  │  iOS App    │  │  Android App         │  │
│  │  (React)       │  │  (React     │  │  (React Native)      │  │
│  │                │  │   Native)   │  │                      │  │
│  └────────┬───────┘  └──────┬──────┘  └──────────┬───────────┘  │
│           │                 │                     │              │
└───────────┼─────────────────┼─────────────────────┼──────────────┘
            │                 │                     │
┌───────────┼─────────────────┼─────────────────────┼──────────────┐
│           ▼                 ▼                     ▼              │
│   ┌───────────────────────────────────────────────────────┐    │
│   │           API GATEWAY (Kong / AWS API Gateway)         │    │
│   │    Rate Limiting • Auth • Versioning • Analytics      │    │
│   └────────────────────┬────────────────────────────────┘    │
│                        │                                       │
│        APPLICATION LAYER (FastAPI / Node.js Microservices)    │
│                        │                                       │
│   ┌────────────────────┼─────────────────────────────────┐   │
│   │                    │                                  │   │
│   ▼                    ▼                    ▼             ▼   │
│  ┌──────────┐    ┌──────────┐      ┌───────────────┐  ┌──┐  │
│  │ Products │    │ Commerce │      │ Seller/Creator│  │AI│  │
│  │ Service  │    │ Service  │      │ Service       │  │  │  │
│  └──────────┘    └──────────┘      └───────────────┘  └──┘  │
│  ┌──────────┐    ┌──────────┐      ┌───────────────┐        │
│  │ Search   │    │ Orders   │      │ Payment       │        │
│  │ Service  │    │ Service  │      │ Service       │        │
│  └──────────┘    └──────────┘      └───────────────┘        │
│  ┌──────────┐    ┌──────────┐      ┌───────────────┐        │
│  │Analytics │    │ Auth     │      │Notification  │        │
│  │ Service  │    │ Service  │      │Service        │        │
│  └──────────┘    └──────────┘      └───────────────┘        │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
┌───────────────────────────┼───────────────────────────────────┐
│         DATA LAYER: MULTI-DATABASE STRATEGY                   │
│                            │                                   │
│   ┌────────────────────────┼──────────────────────────────┐  │
│   │                        ▼                              │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ MongoDB (Primary - Document Store)            │   │  │
│   │  │  - Products, Orders, Users, Sellers          │   │  │
│   │  │  - Replication across 3 regions              │   │  │
│   │  │  - 99.95% SLA                                │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ PostgreSQL (OLTP - Transactions)              │   │  │
│   │  │  - Orders, Payments, Refunds                  │   │  │
│   │  │  - User accounts, Seller tier                │   │  │
│   │  │  - High ACID compliance                      │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ Elasticsearch (Full-Text Search)              │   │  │
│   │  │  - Products index (5M+ documents)             │   │  │
│   │  │  - Auto-complete index                        │   │  │
│   │  │  - Analytics index (logs, events)             │   │  │
│   │  │  - Real-time search < 200ms p99              │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ Redis (Cache + Message Queue)                 │   │  │
│   │  │  - Session cache (15 min TTL)                │   │  │
│   │  │  - Product recommendation cache               │   │  │
│   │  │  - Real-time leaderboards                     │   │  │
│   │  │  - RabbitMQ for async tasks                  │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ TimescaleDB (Time-Series for Analytics)       │   │  │
│   │  │  - Product views per hour                     │   │  │
│   │  │  - Sales volume trends                        │   │  │
│   │  │  - User behavior over time                    │   │  │
│   │  │  - Auto-aggregation + compression             │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ DuckDB (OLAP - Analytics Queries)             │   │  │
│   │  │  - Ad-hoc analysis                            │   │  │
│   │  │  - CSV/Parquet export for BI                 │   │  │
│   │  │  - Fast aggregations                          │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   └──────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
┌───────────────────────────┼───────────────────────────────────┐
│         AI/ML LAYER: RECOMMENDATION ENGINE                    │
│                            │                                   │
│   ┌────────────────────────┼──────────────────────────────┐  │
│   │                        ▼                              │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ Feature Store (Feast)                         │   │  │
│   │  │  - Product features (category, price, etc)    │   │  │
│   │  │  - User features (preference vector)          │   │  │
│   │  │  - Co-occurrence matrices                     │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ ML Models (BentoML / Seldon)                  │   │  │
│   │  │  - Ranking model (XGBoost)                   │   │  │
│   │  │  - CTR prediction model                       │   │  │
│   │  │  - Conversion prediction                      │   │  │
│   │  │  - Embedding models (MLP)                     │   │  │
│   │  │  - Trend detection (ARIMA)                    │   │  │
│   │  │  - P(user will scroll down) model             │   │  │
│   │  │  - Real-time latency: < 100ms                │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ ML Pipeline (Airflow + dbt)                   │   │  │
│   │  │  - Daily model retraining                      │   │  │
│   │  │  - Feature engineering pipeline                │   │  │
│   │  │  - A/B testing framework                       │   │  │
│   │  │  - Model performance tracking                  │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   └──────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
┌───────────────────────────┼───────────────────────────────────┐
│         INFRASTRUCTURE & EXTERNAL INTEGRATIONS                │
│                            │                                   │
│   ┌────────────────────────┼──────────────────────────────┐  │
│   │                        ▼                              │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ CDN & Image Processing (CloudFront + Lambda) │   │  │
│   │  │  - Image resizing (600px, 1200px, orig)      │   │  │
│   │  │  - WebP conversion                            │   │  │
│   │  │  - Video transcoding to HLS                   │   │  │
│   │  │  - <1s delivery anywhere globally             │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ Payment Gateways                              │   │  │
│   │  │  - Stripe (US/EU)                             │   │  │
│   │  │  - Razorpay (India)                           │   │  │
│   │  │  - PayPal (Global)                            │   │  │
│   │  │  - Wise (Payouts)                             │   │  │
│   │  │  - ApplePay / GooglePay                       │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ Product Data Integrations                      │   │  │
│   │  │  - Amazon PA-API (polling + webhooks)         │   │  │
│   │  │  - Shopify (polling + webhooks)               │   │  │
│   │  │  - ClickBank API                              │   │  │
│   │  │  - ProductHunt API                            │   │  │
│   │  │  - OpenAI / Anthropic APIs                    │   │  │
│   │  │  - Custom webhooks for partners               │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ Email & Notifications                         │   │  │
│   │  │  - SendGrid (email)                           │   │  │
│   │  │  - Firebase Cloud Messaging (push)            │   │  │
│   │  │  - Twillio (SMS)                              │   │  │
│   │  │  - Slack integration (alerts)                 │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   │  ┌──────────────────────────────────────────────┐   │  │
│   │  │ Monitoring & Analytics                        │   │  │
│   │  │  - DataDog (APM)                              │   │  │
│   │  │  - Sentry (Error tracking)                    │   │  │
│   │  │  - Mixpanel (User analytics)                  │   │  │
│   │  │  - Google Analytics 4                         │   │  │
│   │  │  - Prometheus + Grafana (infrastructure)      │   │  │
│   │  └──────────────────────────────────────────────┘   │  │
│   │                                                      │  │
│   └──────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## TECHNOLOGY STACK

### Frontend
| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Web App** | React 18 + Vite | Fast builds, modern features |
| **Mobile** | React Native | Code sharing, faster dev |
| **State Mgmt** | Redux Toolkit | Scalable state, debugging |
| **UI Library** | Shadcn/ui + Tailwind | Beautiful, customizable |
| **Forms** | React Hook Form | Performance, flexible validation |
| **Data Fetching** | TanStack Query | Server state management |
| **Visualization** | Recharts | Simple charts and graphs |
| **Maps** | Mapbox (seller location) | Better experience than Google Maps |
| **Testing** | Vitest + React Testing | Fast component testing |

### Backend
| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Web Framework** | FastAPI | Type-safe, fast, great docs |
| **API Gateway** | Kong / AWS API Gateway | Rate limiting, versioning |
| **Background Jobs** | Celery + RabbitMQ | Async task processing |
| **Authentication** | JWT + OAuth2 | Stateless, scalable |
| **Validation** | Pydantic | Type safety at runtime |
| **Logging** | Structlog + JSON | Better filtering/analysis |
| **Testing** | Pytest | Comprehensive test coverage |

### Databases
| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **OLTP** | MongoDB + PostgreSQL | Flexible + ACID compliance |
| **Caching** | Redis | Session, leaderboards, recommendations |
| **Search** | Elasticsearch | Full-text, faceted search |
| **Analytics** | TimescaleDB + DuckDB | Time-series + OLAP queries |
| **Message Queue** | RabbitMQ | Async processing |

### ML/AI
| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Feature Store** | Feast | Centralized feature management |
| **Model Training** | XGBoost, LightGBM | Fast gradient boosting |
| **Embeddings** | Sentence-BERT | Semantic product similarity |
| **Model Serving** | BentoML, Seldon | Production ML serving |
| **Orchestration** | Airflow | ML pipeline scheduling |
| **Experiment Tracking** | MLflow | Model versioning |

### Infrastructure
| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Hosting** | AWS (EC2, ECS, Lambda) | Global, reliable, scalable |
| **Containerization** | Docker, Kubernetes | Deployment consistency |
| **CI/CD** | GitHub Actions | Integrated with GitHub |
| **Monitoring** | DataDog + Sentry | Comprehensive observability |
| **Logging** | CloudWatch + ELK | Centralized logging |
| **CDN** | CloudFront | Fast image/video delivery |
| **Email** | SendGrid | Reliable email delivery |

---

## DEPLOYMENT ARCHITECTURE

### Multi-Region Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                        GLOBAL LOAD BALANCER                  │
│                    (Route53 + CloudFront)                    │
└────┬─────────────────────────────────────────┬───────────────┘
     │                                          │
     ▼                                          ▼
┌──────────────────────┐            ┌──────────────────────┐
│  US REGION (N.Virginia)           │  EU REGION (Ireland) │
│  ECS Cluster (us-east-1)          │  ECS Cluster (eu-west-1)
│  - 3 API nodes                    │  - 3 API nodes
│  - 3 ML nodes                     │  - 3 ML nodes
│  - MongoDB replica                │  - MongoDB replica
│  - Redis cluster                  │  - Redis cluster
│  - Elasticsearch cluster          │  - Elasticsearch cluster
└──────────────────────┘            └──────────────────────┘
     │
     ▼
┌──────────────────────┐
│  ASIA REGION (Mumbai)│
│  ECS Cluster (ap-south-1)
│  - 4 API nodes (higher traffic)
│  - 4 ML nodes
│  - MongoDB primary
│  - Redis primary
│  - Elasticsearch primary
└──────────────────────┘
```

### Auto-Scaling Rules

| Component | Min | Max | Metric | Threshold |
|-----------|-----|-----|--------|-----------|
| **API nodes** | 3 | 50 | CPU % | >70% |
| **ML nodes** | 2 | 20 | Latency | >150ms |
| **Search nodes** | 2 | 15 | Indexing lag | >5s |
| **Cache** | 2 | 10 | Hit rate | <80% |
| **DB replicas** | 1 | 3 | Read QPS | >1000 |

---

## DATA MODELS

### Products Collection (MongoDB)
```javascript
{
  "_id": ObjectId,
  "title": "MacBook Pro 16\" M2",
  "description": "Powerful laptop for professionals",
  "sources": [
    {
      "source": "amazon",
      "url": "https://amazon.com/...",
      "affiliate_url": "https://amazon.com/...",
      "price": 1999.99,
      "rating": 4.5,
      "reviews_count": 2341,
      "last_updated": ISODate("2024-04-08")
    },
    {
      "source": "seller_xyz",
      "url": "https://finez.com/sellers/xyz/products/...",
      "price": 1899.99,
      "rating": 4.8,
      "reviews_count": 156
    }
  ],
  "category": "Laptops",
  "subcategories": ["Computers", "Apple", "Professional"],
  "tags": ["AI-friendly", "32GB RAM", "M2 chip"],
  "images": ["url1", "url2", "url3"],
  "trending_score": 8.5,
  "created_at": ISODate("2024-01-15"),
  "ml_embedding": [0.12, 0.45, 0.67, ...],
  "canonical": true,
  "duplicates": ["product_id_2", "product_id_3"]
}
```

### Orders Collection (PostgreSQL)
```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  buyer_id UUID NOT NULL,
  seller_id UUID NOT NULL,
  product_id UUID NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  commission DECIMAL(10, 2) NOT NULL,
  status ENUM('pending', 'completed', 'refunded', 'disputed'),
  created_at TIMESTAMP,
  completed_at TIMESTAMP,
  payment_method VARCHAR(20),
  affiliate_id UUID,
  affiliate_commission DECIMAL(10,2)
);

CREATE INDEX idx_buyer_id ON orders(buyer_id);
CREATE INDEX idx_seller_id ON orders(seller_id);
CREATE INDEX idx_status ON orders(status);
```

### Events Table (TimescaleDB)
```sql
CREATE TABLE events (
  time TIMESTAMPTZ NOT NULL,
  user_id UUID,
  event_type VARCHAR(50),
  product_id UUID,
  action VARCHAR(20),
  metadata JSONB
);

SELECT create_hypertable('events', 'time');
CREATE INDEX idx_user_time ON events (user_id, time DESC);
```

---

## API DESIGN

### Base URL
```
https://api.finez.com/v1
```

### Authentication
```bash
# OAuth2 + JWT
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# API Key (for third-party integrations)
X-API-Key: sk_live_abc123def456
```

### Endpoints Structure
```
GET    /products               # List all products
GET    /products?category=AI   # Filter by category
GET    /products/{id}          # Get product detail
POST   /products               # Create (sellers only)
PATCH  /products/{id}          # Update product

GET    /search?q=laptop        # Full-text search
GET    /search/autocomplete?q=lap   # Search suggestions

GET    /sellers/{id}           # Seller profile
POST   /sellers                # Register seller
GET    /sellers/{id}/products  # Seller's products
GET    /sellers/{id}/analytics # Seller dashboard

GET    /recommendations        # Personalized recommendations
GET    /trending              # Trending products
GET    /leaderboards          # Top products, sellers, creators

POST   /orders                 # Create order
GET    /orders/{id}            # Order status
GET    /orders                 # User's orders

POST   /auth/login             # Login
POST   /auth/signup            # Register
POST   /auth/refresh           # Refresh token
```

### Response Format
```json
{
  "success": true,
  "data": {...},
  "meta": {
    "timestamp": "2024-04-08T10:30:00Z",
    "version": "v1",
    "request_id": "req_abc123"
  }
}
```

### Error Handling
```json
{
  "success": false,
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product with ID xyz not found",
    "status": 404
  }
}
```

---

## PERFORMANCE TARGETS

### Page Load Times
| Page | Target | Threshold |
|------|--------|-----------|
| **Homepage** | < 1.5s | p95 < 3s |
| **Search Results** | < 1.2s | p95 < 2.5s |
| **Product Detail** | < 1.8s | p95 < 3.5s |
| **Seller Dashboard** | < 2s | p95 < 4s |

### API Response Times
| Endpoint | Target | Threshold |
|----------|--------|-----------|
| **Search** | <200ms | p99 < 500ms |
| **Recommendations** | <150ms | p99 < 300ms |
| **Product Detail** | <50ms | p99 < 100ms |
| **Leaderboards** | <100ms | p99 < 200ms |

### Infrastructure Metrics
| Metric | Target |
|--------|--------|
| **Uptime** | 99.95% |
| **Page Load (Core Web Vitals) - LCP** | < 2.5s |
| **CLS (Cumulative Layout Shift)** | < 0.1 |
| **FID (First Input Delay)** | < 100ms |
| **Image Delivery Time** | < 1s |
| **API Latency p99** | < 500ms |
| **DB Query p99** | < 100ms |

---

## SCALING STRATEGY

### Database Scaling
1. **Read replicas** for search + analytics queries (3+ replicas)
2. **Write optimization** with connection pooling (PgBouncer)
3. **Sharding** by product category when DB reaches 100GB
4. **Archive old data** to Parquet files on S3

### Cache Strategy
1. **Redis cluster** for session + recommendation cache
2. **CDN cache** for product images (30 days TTL)
3. **Elasticsearch cache** for search queries (1 hour TTL)
4. **Compute cache** for trending products (5 minutes TTL)

### ML Model Serving
1. **Batch predictions** for homepage recommendations (every 30 min)
2. **Real-time predictions** for search/detail page (latency: <100ms)
3. **Model A/B testing** with 10% of traffic on new models
4. **Feature caching** in Redis for fast inference

---

## SECURITY ARCHITECTURE

### Data Protection
- **Encryption in transit**: TLS 1.3
- **Encryption at rest**: AES-256 for sensitive data
- **Database encryption**: AWS RDS encryption
- **Secrets management**: AWS Secrets Manager

### Access Control
- **RBAC**: Role-based permissions (admin, seller, creator, user)
- **API keys**: Scoped access for third-party integrations
- **IP whitelisting**: For internal APIs
- **Rate limiting**: 100 req/min per user, 10K req/min for API customers

### PCI Compliance
- **No card storage**: Use Stripe/Razorpay tokenization
- **PCI-DSS Level 1**: Through payment processor
- **Regular penetration testing**: Quarterly

### Privacy
- **GDPR compliant**: EU data residency, data deletion on request
- **CCPA compliant**: California privacy laws
- **Privacy policy**: Clear data usage transparency
- **Cookie consent**: Explicit before tracking

---

## MONITORING & OBSERVABILITY

### Application Monitoring (DataDog)
- Request latency (p50, p95, p99)
- Error rate by endpoint
- Database query time
- Cache hit rate
- ML model predictions/latency

### Infrastructure Monitoring (Prometheus + Grafana)
- CPU, memory, disk usage
- Network I/O
- Database connections
- Redis memory
- Container restart rate

### Error Tracking (Sentry)
- Error frequency
- User impact
- Error grouping
- Release tracking
- Alerts on error spikes

### User Analytics (Mixpanel)
- Daily active users
- Feature adoption
- Conversion funnel
- Retention cohorts
- Revenue per user

---

*Document Status: DRAFT - TECHNICAL ARCHITECTURE*  
*Last Updated: April 2026*
