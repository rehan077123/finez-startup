# Supabase Setup Guide

## 1. Create a Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Create a new project
4. Note down your:
   - Project URL (`NEXT_PUBLIC_SUPABASE_URL`)
   - Anon Public Key (`NEXT_PUBLIC_SUPABASE_ANON_KEY`)
   - Service Role Key (`SUPABASE_SERVICE_ROLE_KEY`)

## 2. Create Database Tables

Run these queries in the Supabase SQL editor:

### Products Table
```sql
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  image_url TEXT,
  price DECIMAL(10, 2),
  affiliate_url TEXT NOT NULL,
  category TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX products_category_idx ON products(category);
CREATE INDEX products_created_at_idx ON products(created_at DESC);
```

### Affiliate Clicks Table
```sql
CREATE TABLE affiliate_clicks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES products(id),
  user_id UUID,
  session_id TEXT NOT NULL,
  affiliate_link TEXT,
  source_url TEXT,
  user_agent TEXT,
  ip_address TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX clicks_product_idx ON affiliate_clicks(product_id);
CREATE INDEX clicks_user_idx ON affiliate_clicks(user_id);
CREATE INDEX clicks_session_idx ON affiliate_clicks(session_id);
```

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  email TEXT UNIQUE NOT NULL,
  display_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Saved Searches Table
```sql
CREATE TABLE saved_searches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  search_query TEXT NOT NULL,
  filters JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX searches_user_idx ON saved_searches(user_id);
```

### Price Alerts Table
```sql
CREATE TABLE price_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  product_id UUID REFERENCES products(id),
  target_price DECIMAL(10, 2),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX alerts_user_idx ON price_alerts(user_id);
CREATE INDEX alerts_product_idx ON price_alerts(product_id);
```

## 3. Set RLS Policies

```sql
-- Allow public read on products
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public products are viewable by everyone" ON products
  FOR SELECT USING (true);

-- Allow logging affiliate clicks
ALTER TABLE affiliate_clicks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can insert clicks" ON affiliate_clicks
  FOR INSERT WITH CHECK (true);
CREATE POLICY "Clicks are viewable by everyone" ON affiliate_clicks
  FOR SELECT USING (true);
```

## 4. Copy Environment Variables

Copy the values from Supabase to your `.env.local`:

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
```

## 5. Test Connection

Run the app and check if you can fetch products from the API.
