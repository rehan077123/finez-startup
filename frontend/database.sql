-- FineZ Database Schema for Supabase/Postgres

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ==================== ENUMS ====================

CREATE TYPE user_plan AS ENUM ('free', 'pro', 'enterprise');
CREATE TYPE product_platform AS ENUM ('amazon', 'flipkart', 'meesho', 'croma', 'myntra', 'nykaa', 'ajio');
CREATE TYPE vendor_plan AS ENUM ('free', 'basic', 'premium', 'enterprise');
CREATE TYPE subscription_status AS ENUM ('active', 'paused', 'cancelled', 'pending');

-- ==================== USERS ====================

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  avatar_url TEXT,
  plan user_plan DEFAULT 'free',
  referral_code TEXT UNIQUE,
  referred_by UUID REFERENCES users(id),
  language_preference TEXT DEFAULT 'en',
  budget_preference_min INTEGER,
  budget_preference_max INTEGER,
  favorite_categories TEXT[] DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_referral_code ON users(referral_code);
CREATE INDEX idx_users_plan ON users(plan);

-- ==================== SEARCHES ====================

CREATE TABLE searches (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  query_raw TEXT NOT NULL,
  query_language TEXT,
  query_translated TEXT,
  intent_category TEXT,
  intent_budget_min INTEGER,
  intent_budget_max INTEGER,
  intent_use_case TEXT,
  intent_priorities TEXT[] DEFAULT '{}',
  intent_brand_exclude TEXT[] DEFAULT '{}',
  results_count INTEGER DEFAULT 0,
  session_id TEXT,
  ip_hash TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_searches_user_id ON searches(user_id);
CREATE INDEX idx_searches_created_at ON searches(created_at DESC);
CREATE INDEX idx_searches_session_id ON searches(session_id);
CREATE INDEX idx_searches_query_raw ON searches USING GIN(query_raw gin_trgm_ops);

-- ==================== PRODUCTS ====================

CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  external_id TEXT NOT NULL,
  platform product_platform NOT NULL,
  name TEXT NOT NULL,
  brand TEXT,
  category TEXT,
  subcategory TEXT,
  description TEXT,
  images TEXT[] DEFAULT '{}',
  specs JSONB,
  current_price INTEGER,
  original_price INTEGER,
  discount_percent INTEGER DEFAULT 0,
  rating DECIMAL(3,2),
  rating_count INTEGER DEFAULT 0,
  in_stock BOOLEAN DEFAULT true,
  affiliate_url TEXT,
  affiliate_tag TEXT,
  finez_score DECIMAL(3,2),
  ai_summary TEXT,
  ai_pros TEXT[] DEFAULT '{}',
  ai_cons TEXT[] DEFAULT '{}',
  verified BOOLEAN DEFAULT false,
  sponsored BOOLEAN DEFAULT false,
  last_fetched_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(external_id, platform)
);

CREATE INDEX idx_products_platform ON products(platform);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_products_finez_score ON products(finez_score DESC);
CREATE INDEX idx_products_created_at ON products(created_at DESC);
CREATE INDEX idx_products_name ON products USING GIN(name gin_trgm_ops);

-- ==================== PRICE HISTORY ====================

CREATE TABLE price_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  platform TEXT,
  price INTEGER,
  in_stock BOOLEAN,
  recorded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_price_history_product_id ON price_history(product_id);
CREATE INDEX idx_price_history_recorded_at ON price_history(recorded_at DESC);

-- ==================== AFFILIATE CLICKS ====================

CREATE TABLE affiliate_clicks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  platform TEXT,
  session_id TEXT,
  ip_hash TEXT,
  source_page TEXT,
  utm_source TEXT,
  utm_medium TEXT,
  utm_campaign TEXT,
  converted BOOLEAN DEFAULT false,
  commission_earned INTEGER DEFAULT 0,
  clicked_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_affiliate_clicks_user_id ON affiliate_clicks(user_id);
CREATE INDEX idx_affiliate_clicks_product_id ON affiliate_clicks(product_id);
CREATE INDEX idx_affiliate_clicks_session_id ON affiliate_clicks(session_id);
CREATE INDEX idx_affiliate_clicks_clicked_at ON affiliate_clicks(clicked_at DESC);

-- ==================== SAVED LISTS ====================

CREATE TABLE saved_lists (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  is_public BOOLEAN DEFAULT false,
  share_token TEXT UNIQUE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_saved_lists_user_id ON saved_lists(user_id);
CREATE INDEX idx_saved_lists_share_token ON saved_lists(share_token);

-- ==================== SAVED LIST ITEMS ====================

CREATE TABLE saved_list_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  list_id UUID NOT NULL REFERENCES saved_lists(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  notes TEXT,
  added_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_saved_list_items_list_id ON saved_list_items(list_id);
CREATE INDEX idx_saved_list_items_product_id ON saved_list_items(product_id);

-- ==================== PRICE ALERTS ====================

CREATE TABLE price_alerts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  target_price INTEGER NOT NULL,
  notified BOOLEAN DEFAULT false,
  notified_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_price_alerts_user_id ON price_alerts(user_id);
CREATE INDEX idx_price_alerts_product_id ON price_alerts(product_id);
CREATE INDEX idx_price_alerts_notified ON price_alerts(notified);

-- ==================== VENDORS ====================

CREATE TABLE vendors (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  brand_name TEXT NOT NULL,
  logo_url TEXT,
  website TEXT,
  description TEXT,
  plan vendor_plan DEFAULT 'free',
  monthly_budget INTEGER DEFAULT 0,
  verified BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_vendors_user_id ON vendors(user_id);
CREATE INDEX idx_vendors_verified ON vendors(verified);
CREATE INDEX idx_vendors_plan ON vendors(plan);

-- ==================== VENDOR PRODUCTS ====================

CREATE TABLE vendor_products (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  vendor_id UUID NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  sponsored_budget INTEGER DEFAULT 0,
  sponsored_active BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_vendor_products_vendor_id ON vendor_products(vendor_id);
CREATE INDEX idx_vendor_products_product_id ON vendor_products(product_id);

-- ==================== REVIEWS CACHE ====================

CREATE TABLE reviews_cache (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  platform TEXT,
  total_reviews INTEGER,
  verified_purchase_count INTEGER,
  ai_summary TEXT,
  top_pros TEXT[] DEFAULT '{}',
  top_cons TEXT[] DEFAULT '{}',
  most_praised TEXT,
  most_complained TEXT,
  cached_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reviews_cache_product_id ON reviews_cache(product_id);

-- ==================== REFERRALS ====================

CREATE TABLE referrals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  referrer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  referred_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  reward_given BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_referrals_referrer_id ON referrals(referrer_id);
CREATE INDEX idx_referrals_referred_id ON referrals(referred_id);

-- ==================== SUBSCRIPTIONS ====================

CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  razorpay_subscription_id TEXT UNIQUE,
  plan TEXT,
  status subscription_status DEFAULT 'pending',
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);

-- ==================== ROW LEVEL SECURITY ====================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE searches ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_lists ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_list_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE price_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE vendors ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Users can see their own data
CREATE POLICY "Users can view own data" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own data" ON users
  FOR UPDATE USING (auth.uid() = id);

-- Users can see their own searches
CREATE POLICY "Users can view own searches" ON searches
  FOR SELECT USING (user_id IS NULL OR auth.uid() = user_id);

-- Users can see their own lists
CREATE POLICY "Users can view own lists" ON saved_lists
  FOR SELECT USING (auth.uid() = user_id OR is_public = true);

-- Everyone can see public products
CREATE POLICY "Products are public" ON products
  FOR SELECT USING (true);

-- Updated timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
