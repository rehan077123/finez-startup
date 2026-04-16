# FINEZ: Phase 0 Implementation Guide (Weeks 1-4)

## OVERVIEW
Phase 0 is the foundation. Everything built after depends on these core systems being correct.

**Timeline**: 4 weeks  
**Team**: 3 backend engineers, 1 devops, 1 database architect  
**Budget**: $50K  
**Goal**: Rock-solid foundations for $1B+ platform

---

## WEEK 1: DATABASE & INFRASTRUCTURE FOUNDATIONS

### Task 1.1: MongoDB Schema Redesign [5 days]
**Owner**: Database Architect  
**Status**: NOT STARTED

**Current State**: 
- Basic product schema
- No seller/creator support
- No analytics data structure

**Deliverables**:
- [ ] New collections designed (20 total)
  - `products` (5M+ documents)
  - `sellers` (user data + tier + analytics)
  - `creators` (extended profile + stats)
  - `digital_products` (marketplace items)
  - `orders` (order history)
  - `reviews` (ratings + text)
  - `tags` (normalized categories)
  - `categories` (hierarchy)
  - `affiliates` (affiliate data)
  - `ai_tools` (special category)
  - `analytics_events` (for ML)
  - And 9 more support collections

- [ ] Migration script written
  - Backup current data
  - Transform old schema → new schema
  - Verify integrity
  - Rollback capability

- [ ] Indexing strategy
  - Compound indexes for common queries
  - Text indexes for search
  - Sparse indexes for optional fields
  - Time-based indexes for pagination

**Success Criteria**:
- ✅ All collections created with validation
- ✅ Indexes built (query<50ms for common queries)
- ✅ Migration script tested on backup
- ✅ Rollback tested successfully

**Commands**:
```bash
# Create migration branch
git checkout -b phase0/db-schema

# MongoDB migration
python backend/migrations/001_redesign_schema.py

# Test migration on backup
mongorestore --drop backup/
python backend/tests/test_schema_integrity.py
```

---

### Task 1.2: PostgreSQL Setup for OLTP [3 days]
**Owner**: Database Architect  
**Status**: NOT STARTED

**Why PostgreSQL alongside MongoDB?**
- Transactions for payments/orders (ACID compliance required)
- Foreign key constraints
- Better for financial data
- Easier auditing/compliance

**Deliverables**:
- [ ] PostgreSQL RDS provisioned
  - db.r5.2xlarge (64GB RAM, 8 vCPU)
  - Multi-AZ for high availability
  - Automated backups (35 day retention)
  - SSL encryption enabled

- [ ] Schema created
  - `users` table (id, email, password_hash, tier, created_at)
  - `sellers` table (seller_id, user_id, verification_status, payout_method, tier)
  - `orders` table (id, buyer_id, seller_id, product_id, amount, commission, status)
  - `payments` table (id, order_id, gateway, transaction_id, status)
  - `refunds` table (id, order_id, reason, amount, status)
  - `affiliate_earnings` table (id, affiliate_id, product_id, commission, status)
  - `audit_log` table (changes for compliance)

- [ ] Connection pooling
  - PgBouncer configuration
  - Max connections: 200
  - Timeout: 25 seconds

**Success Criteria**:
- ✅ DB accessible from app servers
- ✅ All tables created with constraints
- ✅ Connection pool healthy
- ✅ Backups working

**Commands**:
```bash
# Create PostgreSQL RDS
aws rds create-db-instance \
  --db-instance-identifier finez-primary \
  --db-instance-class db.r5.2xlarge \
  --engine postgres \
  --allocated-storage 500 \
  --multi-az

# Apply schema
psql $DATABASE_URL < backend/migrations/001_create_tables.sql

# Test connection pooling
pgbouncer -d -c pgbouncer.ini
```

---

### Task 1.3: Elasticsearch Setup [2 days]
**Owner**: Backend Engineer  
**Status**: NOT STARTED

**Deliverables**:
- [ ] Elasticsearch cluster deployed
  - 3 master nodes (dedicated)
  - 4 data nodes (t3.large each)
  - 2 ingest nodes (for processing)
  - 10GB heap per node

- [ ] Index setup
  - `products` index (5M documents)
    - Fields: title, description, category, tags, price, rating, seller_name
    - Analyzer: standard analyzer + edge_ngram for autocomplete
    - Shard setup: 5 shards, 2 replicas

  - `autocomplete` index
    - Specialized for search suggestions
    - Lower replica count (1 replica)

  - `analytics` index
    - 30-day rotation
    - Optimize for read-heavy workload

- [ ] Ingestion pipeline
  - Connect MongoDB → Elasticsearch via Logstash
  - Real-time sync on product updates
  - Daily full re-index (off-peak)

**Success Criteria**:
- ✅ Cluster health GREEN
- ✅ All indices healthy
- ✅ Search latency <200ms for p99
- ✅ Indexing lag <5 seconds

**Commands**:
```bash
# Deploy Elasticsearch
terraform apply -target=aws_elasticsearch_domain.finez

# Create indices
curl -X PUT http://localhost:9200/products \
  -H "Content-Type: application/json" \
  -d @backend/search/mappings/products.json

# Test search
curl "http://localhost:9200/products/_search?q=laptop"
```

---

## WEEK 2: AUTHENTICATION & AUTHORIZATION

### Task 2.1: RBAC System Implementation [4 days]
**Owner**: Backend Engineer  
**Status**: NOT STARTED

**Role Hierarchy**:
```
ADMIN
  ├─ SUPER_ADMIN (full access)
  ├─ CONTENT_ADMIN (moderation, featured products)
  ├─ FINANCE_ADMIN (payments, payouts, disputes)
  └─ SUPPORT_ADMIN (buyer/seller support)

SELLER
  ├─ TIER_1 (1-10 products, 5% commission)
  ├─ TIER_2 (11-100 products, 8% commission)
  ├─ TIER_3 (100+ products, 10% commission)
  └─ ENTERPRISE (custom terms)

CREATOR
  ├─ BASIC (free tier)
  ├─ PRO ($9/month)
  └─ PRO_MAX ($199/month)

AFFILIATE
  ├─ TIER_1 (0-$100/week)
  ├─ TIER_2 ($100-1K/week)
  └─ TIER_3 ($1K+/week)

USER (buyer/consumer)
```

**Deliverables**:
- [ ] RBAC middleware
  ```python
  # backend/middleware/rbac.py
  @require_role("seller", "tier_2")
  @require_permission("can_list_product")
  async def create_product(req, user):
      ...
  ```

- [ ] Role assignment endpoints
  - POST /admin/users/{id}/assign-role
  - POST /admin/sellers/{id}/set-tier
  - POST /sellers/{id}/apply-tier-upgrade

- [ ] Permission matrix
  - Encoded as JSON in cache
  - Fast lookup (Redis)
  - Updated on role change

- [ ] Tests
  - Unit tests for each role
  - Permission matrix verification
  - Edge cases (user changing tiers mid-purchase)

**Success Criteria**:
- ✅ All 5 roles working
- ✅ Tier transitions tested
- ✅ Admin permissions locked down
- ✅ Zero permission bypass vulnerabilities

---

### Task 2.2: JWT + OAuth2 Enhancement [3 days]
**Owner**: Backend Engineer  
**Status**: NOT STARTED

**Current State**: Basic JWT only

**Deliverables**:
- [ ] OAuth2 providers
  - Google login (primary)
  - GitHub login (secondary)
  - Apple login (for mobile)

- [ ] Token management
  - Access token (30 min expiry)
  - Refresh token (30 days expiry)
  - Automatic token refresh
  - Token revocation on logout

- [ ] Device tracking
  - Store device fingerprint on login
  - Allow logging out from other devices
  - Show "active sessions" in account settings

- [ ] 2FA for sellers
  - TOTP (Time-based One-Time Password)
  - SMS backup codes
  - Recovery email

**Success Criteria**:
- ✅ OAuth2 flows working
- ✅ Token refresh working seamlessly
- ✅ 2FA implemented + tested
- ✅ No security leaks in token handling

---

## WEEK 3: SEARCH INFRASTRUCTURE

### Task 3.1: Elasticsearch Integration [4 days]
**Owner**: Backend Engineer  
**Status**: NOT STARTED

**Deliverables**:
- [ ] Advanced search queries
  ```python
  # Faceted search with filters
  GET /search?q=laptop&category=Electronics&price_min=500&price_max=2000
  
  # Autocomplete
  GET /search/autocomplete?q=lap
  
  # Spell correction
  GET /search?q=lapto  # Returns results for "laptop"
  
  # Trending searches
  GET /search/trending
  ```

- [ ] Search analytics
  - Track all searches
  - Calculate CTR per query
  - Identify low-performing queries
  - Find typos/misspellings

- [ ] Search performance tuning
  - Query optimization (< 200ms p99)
  - Cache hot queries
  - Pre-compute popular searches

**Success Criteria**:
- ✅ Search latency < 200ms (p99)
- ✅ Autocomplete latency < 100ms
- ✅ Spell correction working
- ✅ Analytics data flowing

---

### Task 3.2: Search API Endpoints [2 days]
**Owner**: Backend Engineer  
**Status**: NOT STARTED

**Endpoints to Build**:
```
GET    /api/v1/search
GET    /api/v1/search/autocomplete
GET    /api/v1/search/trending
GET    /api/v1/search/suggestions
GET    /api/v1/search/filters/{category}
```

---

## WEEK 4: ADMIN DASHBOARD & SYSTEM MONITORING

### Task 4.1: Admin Dashboard v1 [3 days]
**Owner**: Frontend Engineer  
**Status**: NOT STARTED

**Pages**:
- [ ] Dashboard (metrics overview)
  - Total users, sellers, creators
  - Daily GMV
  - Key metrics graph
  - Recent orders

- [ ] Product Moderation Queue
  - Show 50 products pending approval
  - Reject/approve functionality
  - Bulk actions
  - Notes/reasons

- [ ] Seller Management
  - List all sellers
  - Search/filter by tier/status
  - View seller details
  - Manual tier upgrades
  - Suspend/ban sellers

- [ ] Analytics
  - Daily/weekly/monthly GMV
  - Category breakdown
  - Top products
  - Top sellers
  - User retention

- [ ] Settings
  - Commission rates
  - Commission tiers
  - Featured product pricing
  - Category settings

**Success Criteria**:
- ✅ Dashboard loads < 2s
- ✅ Moderation can process 100 products/hour
- ✅ All admin actions logged
- ✅ Mobile responsive

---

### Task 4.2: Monitoring & Alerts [2 days]
**Owner**: DevOps Engineer  
**Status**: NOT STARTED

**Deliverables**:
- [ ] DataDog setup
  - API monitoring (latency, errors)
  - Database monitoring (query time, connections)
  - Infrastructure monitoring (CPU, memory, disk)
  - Custom metrics (GMV, order count, search queries)

- [ ] Alerts configured
  - Latency > 500ms (p99)
  - Error rate > 1%
  - CPU > 80%
  - Memory > 85%
  - Database connections > 180
  - Search lag > 10s

- [ ] Dashboards
  - Platform health dashboard
  - Real-time metrics
  - Historical trends
  - Alert history

**Success Criteria**:
- ✅ All systems monitored
- ✅ Alerts tested
- ✅ On-call rotation set up
- ✅ Runbooks written

---

## PHASE 0 DELIVERABLES CHECKLIST

### Infrastructure
- [ ] MongoDB schema redesigned + migrated
- [ ] PostgreSQL RDS set up + configured
- [ ] Elasticsearch cluster deployed + configured
- [ ] Redis cluster set up
- [ ] CI/CD pipeline working
- [ ] Infrastructure as Code (Terraform)
- [ ] Backup strategy implemented
- [ ] Disaster recovery tested

### Backend
- [ ] RBAC system working
- [ ] JWT + OAuth2 enhanced
- [ ] 2FA for sellers
- [ ] Advanced search API
- [ ] Admin endpoints
- [ ] Error handling standardized
- [ ] Logging structured (JSON)
- [ ] API versioning in place

### Frontend
- [ ] Admin dashboard built
- [ ] Login/signup enhanced
- [ ] Search UI improved
- [ ] Mobile responsive
- [ ] Performance optimized

### Security
- [ ] TLS 1.3 enabled
- [ ] Secrets managed securely
- [ ] Rate limiting configured
- [ ] CORS policies set
- [ ] Security headers added (CSP, X-Frame-Options, etc.)
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified

### Monitoring
- [ ] DataDog configured
- [ ] Sentry error tracking
- [ ] Alerts configured
- [ ] Dashboards created
- [ ] Runbooks written
- [ ] On-call schedule

### Testing
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] Load testing (simulate 100K users)
- [ ] Security testing
- [ ] Database migration tested

---

## PHASE 0 SUCCESS METRICS

| Metric | Target |
|--------|--------|
| **API latency (p99)** | < 200ms |
| **Search latency (p99)** | < 200ms |
| **Database query time (p99)** | < 100ms |
| **Uptime** | 99.9% |
| **Error rate** | < 0.5% |
| **Test coverage** | > 80% |
| **Page load time** | < 2s |

---

## RESOURCE ALLOCATION - PHASE 0

| Role | Allocation | Weekly Hours |
|------|-----------|--------------|
| Database Architect | 100% | 40h |
| Backend Engineer #1 | 100% | 40h |
| Backend Engineer #2 | 80% | 32h |
| Frontend Engineer | 50% | 20h |
| DevOps Engineer | 100% | 40h |
| QA Engineer | 60% | 24h |

**Total Man-hours**: 196 hours  
**Cost**: ~$50K (assuming $250/hr average loaded cost)

---

## RISKS & MITIGATION

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|-----------|
| DB migration fails | 🔴 High | Medium | Test on backup, rollback plan |
| Search index large | 🟡 Medium | High | Start with 1M docs, scale gradually |
| RBAC too complex | 🟡 Medium | Medium | Start simple, iterate based on feedback |
| Performance regression | 🟠 Medium-High | Medium | Load test before deploy, monitor |
| Security hole discovered | 🔴 High | Low | Penetration testing, code review |

---

## DAILY STANDUP TEMPLATE (WEEK 1-4)

```
Date: 2026-04-09

✅ COMPLETED
- Database schema approved by team
- MongoDB indices created
- PostgreSQL RDS provisioned

🚧 IN PROGRESS
- MongoDB migration script (90% done)
- RBAC implementation (70% done)
- Elasticsearch setup (50% done)

🔴 BLOCKERS
- AWS account permissions (need DevOps access)

📅 NEXT 24 HOURS
- Complete migration script
- Start RBAC tests
- Set up Elasticsearch cluster

📊 PROGRESS: 40%
```

---

*Document Status: DRAFT - PHASE 0 GUIDE*
*Last Updated: April 2026*
