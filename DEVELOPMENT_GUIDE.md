# FineZ Development Guide

## Getting Started

### 1. Environment Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Update .env.local with your values:
# - NEXT_PUBLIC_SUPABASE_URL
# - NEXT_PUBLIC_SUPABASE_ANON_KEY
# - UPSTASH_REDIS_REST_URL
# - UPSTASH_REDIS_REST_TOKEN
# - ANTHROPIC_API_KEY (for AI features)
# - RAZORPAY_KEY_ID & RAZORPAY_KEY_SECRET (for payments)
# - etc.
```

### 2. Database Setup

```bash
# Create tables in Supabase
# 1. Go to Supabase SQL Editor
# 2. Create a new query
# 3. Copy contents from database.sql
# 4. Run the query to create all 16 tables with indexes and RLS policies

# Verify tables were created
npm run prisma:generate
npm run prisma:studio # Opens Prisma Studio at http://localhost:5555
```

### 3. Local Development

```bash
# Start development server
npm run dev

# Open http://localhost:3000
# Homepage should load with navigation
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Auth pages (login, signup, etc.)
│   │   ├── (main)/            # Main public pages
│   │   ├── (vendor)/          # Vendor dashboard
│   │   ├── (admin)/           # Admin panel
│   │   ├── api/               # API routes
│   │   ├── globals.css        # Global styles
│   │   └── layout.tsx         # Root layout
│   ├── components/
│   │   ├── ui/                # Base UI components (Button, Input, etc.)
│   │   ├── layout/            # Page layouts (Header, Footer)
│   │   ├── search/            # Search-related components
│   │   ├── product/           # Product display components
│   │   └── results/           # Search results components
│   ├── config/
│   │   ├── constants.ts       # App constants (platforms, pricing, etc.)
│   │   ├── supabase.ts        # Supabase client setup
│   │   └── redis.ts           # Redis client setup
│   ├── hooks/                 # Custom React hooks
│   ├── lib/                   # External integrations (AI, payments, etc.)
│   ├── utils/
│   │   ├── helpers.ts         # 20+ utility functions
│   │   ├── api-client.ts      # Typed API wrapper
│   │   └── validation.ts      # Zod schemas
│   ├── middleware.ts          # Next.js middleware
│   ├── i18n.ts               # i18n configuration
│   └── providers/             # App providers (Query, Theme, etc.)
├── messages/                  # i18n translations (en.json, hi.json, etc.)
├── prisma/
│   └── schema.prisma          # ORM schema
├── public/
│   ├── manifest.json          # PWA manifest
│   └── sw.js                  # Service worker
├── database.sql               # Supabase schema
├── next.config.js             # Next.js config
├── tsconfig.json              # TypeScript config
├── tailwind.config.js         # Tailwind CSS config
└── package.json               # Dependencies
```

## Key Completed Components

### Pages
- ✅ Home page (`/`)
- ✅ Search page (`/search`)
- ✅ Product detail page (`/product/[id]`)
- ✅ Login page (`/login`)
- ✅ Signup page (`/signup`)
- ✅ Forgot password page (`/forgot-password`)

### UI Components (14 built)
- ✅ Button, Input
- ✅ Badge, Card
- ✅ Modal, Skeleton, Toast, Select
- ✅ Avatar, Switch, Spinner
- ✅ Progress, Tabs, Tooltip

### API Routes
- ✅ POST `/api/search` - AI search with intent parsing
- ✅ GET/POST/DELETE `/api/alerts` - Price alerts
- ✅ GET `/api/products` - Products list
- ✅ GET `/api/products/[id]` - Product detail
- ✅ GET `/api/go/[productId]` - Affiliate tracker

### Utilities & Hooks
- ✅ 20+ utility functions (formatPrice, generateSessionId, etc.)
- ✅ 11 custom React hooks
- ✅ Redis cache helpers
- ✅ Typed API client

## Priority Tasks to Complete

### Phase 1: Complete Core Features
```
1. Build all missing UI components (6 remaining)
   - [ ] TextField, Accordion
   - [ ] Dropdown, Combobox, RadioGroup

2. Build all 15+ missing pages
   - [ ] Wishlist, Price alerts manager
   - [ ] Deals, Category browser
   - [ ] Admin and vendor dashboards

3. Build search feature components
   - [ ] SearchBar with autocomplete
   - [ ] SearchFilters with chips
   - [ ] SearchHistory
```

### Phase 2: Integrations
```
1. Anthropic API
   - Intent parsing (budget, category, use case)
   - Product summarization
   - Buying guide generation

2. Razorpay Payment
   - Subscription creation
   - Webhook handling

3. Resend Email
   - Email templates
   - Notification system

4. Analytics
   - Sentry for error tracking
   - PostHog for analytics
```

### Phase 3: Backend Services
```
1. Authentication
   - Supabase Auth integration
   - Protected routes
   - Session management

2. Database Operations
   - Seed data loading
   - Price history updates
   - Alert checking cron

3. External API Integration
   - Product data fetching (Rainforest)
   - Price tracking
   - Competitor monitoring
```

## Common Development Patterns

### Creating a New Page

```typescript
// src/app/(main)/new-page/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button, Card } from "@/components/ui";

export default function NewPage() {
  const router = useRouter();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Your logic here
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8">Page Title</h1>
      {/* Page content */}
    </div>
  );
}
```

### Creating a New API Route

```typescript
// src/app/api/new-endpoint/route.ts
import { NextRequest, NextResponse } from "next/server";
import { supabaseServer } from "@/config/supabase";

export async function GET(request: NextRequest) {
  try {
    // Your logic here
    const { data, error } = await supabaseServer
      .from("your_table")
      .select("*");

    if (error) throw error;

    return NextResponse.json(data);
  } catch (error) {
    console.error("Error:", error);
    return NextResponse.json(
      { error: "Failed to fetch data" },
      { status: 500 }
    );
  }
}
```

### Using Custom Hooks

```typescript
import { useSearch, useProduct, usePriceAlert } from "@/hooks";

export default function MyComponent() {
  // Fetch search results
  const { data: results, isLoading, error } = useSearch("laptop under 50000");

  // Fetch single product
  const { data: product } = useProduct("product-id");

  // Set price alert
  const { mutate: setPriceAlert, isPending } = usePriceAlert({
    productId: "product-id",
    targetPrice: 40000,
  });

  return (
    // Your JSX
  );
}
```

## Environment Variables

Create `.env.local` with:

```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxxxx

# Redis
UPSTASH_REDIS_REST_URL=https://xxxxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxxxx

# AI
ANTHROPIC_API_KEY=sk-xxxxx

# Payments
RAZORPAY_KEY_ID=rzp_live_xxxxx
RAZORPAY_KEY_SECRET=xxxxx

# Email
RESEND_API_KEY=re_xxxxx

# Google Translate
GOOGLE_TRANSLATE_API_KEY=xxxxx

# External APIs
RAINFOREST_API_KEY=xxxxx

# Analytics
SENTRY_DSN=https://xxxxx@xxxxx.ingest.sentry.io/xxxxx
NEXT_PUBLIC_POSTHOG_KEY=phc_xxxxx

# Firebase
NEXT_PUBLIC_FIREBASE_CONFIG={"apiKey":"xxxxx",...}
```

## Database Management

### View/Edit Data (Prisma Studio)
```bash
npm run prisma:studio
# Opens http://localhost:5555
```

### Generate Prisma Client
```bash
npm run prisma:generate
```

### Reset Database
```bash
npm run prisma:reset
# WARNING: Deletes all data and re-runs migrations
```

## Testing

### Run Tests
```bash
npm run test
```

### E2E Tests
```bash
npm run test:e2e
```

## Deployment

### Build for Production
```bash
npm run build
```

### Start Production Server
```bash
npm start
```

### Deploy to Vercel
```bash
# Push to GitHub
git push origin main

# Vercel automatically deploys from main branch
# Set environment variables in Vercel dashboard
```

## Troubleshooting

### Common Issues

**1. Supabase Connection Error**
```
Solution: Check NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in .env.local
```

**2. Redis Connection Error**
```
Solution: Check UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN
```

**3. Build Errors**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

**4. TypeScript Errors**
```bash
# Regenerate Prisma client
npm run prisma:generate

# Clear Next.js cache
rm -rf .next
npm run build
```

## Performance Tips

1. **Caching**: Redis cache is configured for:
   - Products: 5 minutes
   - Searches: 1 hour
   - Alerts: 1 hour
   - Products: 300 seconds

2. **Image Optimization**: Use Next.js Image component
   ```tsx
   import Image from "next/image";
   <Image src="/..." alt="..." width={200} height={200} />
   ```

3. **Code Splitting**: Lazy load heavy components
   ```tsx
   const HeavyComponent = dynamic(() => import('./HeavyComponent'));
   ```

## Next Steps

1. **Run Database Setup**
   - Copy `database.sql` to Supabase SQL editor
   - Run to create all 16 tables

2. **Configure Environment**
   - Set up Supabase project
   - Create Upstash Redis database
   - Get API keys for integrations

3. **Test Basic Flow**
   - npm run dev
   - Navigate to home page
   - Test search functionality
   - Verify product detail page

4. **Continue Building**
   - Use BUILD_MANIFEST.md for remaining components
   - Follow priority order (core features first)
   - Integration testing as you go

---

**Questions?** Check the respective integration docs or raise an issue.
