# FineZ Frontend - Next.js 14 App

A modern, SSR-ready e-commerce product discovery platform built with Next.js 14, Supabase, and PWA.

## Features ✨

- **🚀 Server-Side Rendering (SSR)** - Every page is crawlable by Google
- **⚡ Incremental Static Regeneration (ISR)** - Product pages stay fresh without rebuilds
- **📱 Progressive Web App** - Install on Android home screen, 3x higher retention
- **🔗 Affiliate Tracking** - Server-side redirect logging for every "Buy Now" click
- **💾 Real-time Database** - Supabase for users, searches, price alerts, and click analytics
- **🎨 Beautiful UI** - Radix UI + Tailwind CSS
- **🌓 Dark Mode** - Built-in theme support
- **📊 Analytics Ready** - Built-in click tracking and conversion measurement

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
```bash
cp .env.example .env.local
```

Then fill in your Supabase credentials (see `SUPABASE_SETUP.md`)

### 3. Run Development Server
```bash
npm run dev
```

Visit http://localhost:3000

### 4. Build for Production
```bash
npm run build
npm start
```

## Project Structure

```
src/
├── app/                    # Next.js 14 App Router
│   ├── api/               # API routes (backend)
│   │   ├── go/[productId] # Affiliate click tracker
│   │   └── products/      # Product CRUD
│   ├── products/          # Product pages
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # Reusable React components
│   ├── theme-provider.tsx # Dark mode
│   └── service-worker-provider.tsx # PWA setup
└── lib/
    ├── supabase.ts        # Supabase client
    └── types.ts           # TypeScript interfaces
```

## Database Schema

See `SUPABASE_SETUP.md` for complete SQL. Tables include:

- **products** - Product catalog
- **affiliate_clicks** - Click tracking for analytics
- **users** - User accounts (via Supabase Auth)
- **saved_searches** - User's saved product searches
- **price_alerts** - Price monitoring

## API Endpoints

### Affiliate Redirect
```
GET /api/go/[productId]
→ Logs click
→ Redirects to affiliate URL
```

### Product Listing
```
GET /api/products?category=tech&limit=20&offset=0
→ Returns paginated products with total count
```

### Product Details
```
GET /api/products/[id]
→ Returns single product with caching headers
```

## Deployment

### Vercel (Recommended)
```bash
vercel
```

Automatic deployments from git, serverless functions, edge caching included.

### Docker
```bash
docker build -t finez .
docker run -p 3000:3000 finez
```

### Other Platforms
Works on any Node.js 18+ server. Set environment variables and run:
```bash
npm run build
npm start
```

## Performance

### Caching Strategy
- **Product pages**: 1h server + 1d edge + 7d stale-while-revalidate
- **API routes**: 1m server + 1h edge cache

### Expected Metrics
- LCP: < 2.5s (with caching)
- FID: < 100ms
- CLS: < 0.1

## PWA Installation

### Android
1. Open on Android Chrome
2. Menu → "Install app"
3. App appears on home screen

### iOS
1. Open in Safari
2. Share → "Add to Home Screen"

## Environment Variables

```env
NEXT_PUBLIC_SUPABASE_URL=               # Required: Your Supabase URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=          # Required: Public API key
SUPABASE_SERVICE_ROLE_KEY=              # Required: Server-only key
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm start            # Start production server
npm run lint         # Run ESLint
npm run type-check   # Check TypeScript
npm run format       # Format code with Prettier
npm run format:check # Check if code is formatted
```

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Next.js 14 | React framework with SSR/ISR |
| TypeScript | Type safety |
| Supabase | Postgres database + Auth |
| Tailwind CSS | Styling |
| Radix UI | Accessible components |
| React Hook Form | Form handling |
| Zod | Validation |
| next-pwa | PWA support |
| Sonner | Notifications |
| next-themes | Dark mode |

## Security

- ✅ HTTPS enforced in production
- ✅ XSS protection headers
- ✅ CSRF protection
- ✅ Security headers middleware
- ✅ SQL injection prevention (Supabase parameterized queries)
- ✅ Rate limiting ready

## Contributing

1. Create a feature branch
2. Make changes
3. Run `npm run format` and `npm run lint`
4. Submit pull request

## License

MIT
