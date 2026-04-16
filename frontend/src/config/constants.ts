// Configuration constants for FineZ

export const CONFIG = {
  // App
  APP_NAME: "FineZ",
  APP_URL: process.env.NEXT_PUBLIC_APP_URL || "https://finezapp.com",
  
  // Supabase
  SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
  SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  
  // Redis
  REDIS_URL: process.env.UPSTASH_REDIS_REST_URL,
  REDIS_TOKEN: process.env.UPSTASH_REDIS_REST_TOKEN,
  
  // External APIs
  ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
  RAINFOREST_API_KEY: process.env.RAINFOREST_API_KEY,
  GOOGLE_TRANSLATE_API_KEY: process.env.GOOGLE_TRANSLATE_API_KEY,
  
  // Affiliate Programs
  AMAZON_TAG: process.env.AMAZON_AFFILIATE_TAG,
  FLIPKART_ID: process.env.FLIPKART_AFFILIATE_ID,
  FLIPKART_TOKEN: process.env.FLIPKART_AFFILIATE_TOKEN,
  CUELINKS_KEY: process.env.CUELINKS_API_KEY,
  
  // Payments
  RAZORPAY_KEY: process.env.RAZORPAY_KEY_ID,
  RAZORPAY_SECRET: process.env.RAZORPAY_KEY_SECRET,
  
  // Email
  RESEND_KEY: process.env.RESEND_API_KEY,
  
  // Monitoring
  SENTRY_DSN: process.env.SENTRY_DSN,
  POSTHOG_KEY: process.env.NEXT_PUBLIC_POSTHOG_KEY,
  
  // Feature Flags
  ENABLE_VENDOR_MODE: process.env.NEXT_PUBLIC_ENABLE_VENDOR_MODE === "true",
  ENABLE_AFFILIATE: process.env.NEXT_PUBLIC_ENABLE_AFFILIATE_PROGRAM === "true",
  ENABLE_PRICE_ALERTS: process.env.NEXT_PUBLIC_ENABLE_PRICE_ALERTS === "true",
};

export const PLATFORMS = {
  AMAZON: {
    name: "Amazon",
    color: "bg-orange-500",
    icon: "🛒",
  },
  FLIPKART: {
    name: "Flipkart",
    color: "bg-blue-600",
    icon: "📱",
  },
  MEESHO: {
    name: "Meesho",
    color: "bg-pink-500",
    icon: "🎁",
  },
  CROMA: {
    name: "Croma",
    color: "bg-red-600",
    icon: "💻",
  },
  MYNTRA: {
    name: "Myntra",
    color: "bg-orange-400",
    icon: "👗",
  },
  NYKAA: {
    name: "Nykaa",
    color: "bg-purple-500",
    icon: "💄",
  },
  AJIO: {
    name: "Ajio",
    color: "bg-blue-500",
    icon: "🛍️",
  },
};

export const CATEGORIES = [
  "Electronics",
  "Fashion",
  "Home & Kitchen",
  "Beauty",
  "Sports & Outdoors",
  "Books & Media",
  "Toys & Games",
  "Health & Wellness",
  "Automotive",
  "Pet Supplies",
];

export const LANGUAGES = {
  en: "English",
  hi: "हिंदी",
  ta: "தமிழ்",
  bn: "বাংলা",
};

export const PLANS = {
  FREE: {
    name: "Free",
    price: 0,
    features: [
      "Unlimited searches",
      "5 saved lists",
      "Price alerts on 5 products",
      "Basic filters",
    ],
  },
  PRO: {
    name: "Pro",
    price: 499,
    features: [
      "Everything in Free",
      "30 saved lists",
      "Price alerts on 50 products",
      "Advanced filters",
      "Comparison tool",
      "AI buying guides",
      "No ads",
    ],
  },
  ENTERPRISE: {
    name: "Enterprise",
    price: 4999,
    features: [
      "Everything in Pro",
      "Unlimited lists & alerts",
      "API access",
      "Custom integrations",
      "Priority support",
      "White label option",
    ],
  },
};

export const COMMISSION_RATES = {
  AMAZON: 0.05, // 5%
  FLIPKART: 0.04, // 4%
  MEESHO: 0.03, // 3%
  CROMA: 0.02, // 2%
  MYNTRA: 0.04, // 4%
  NYKAA: 0.06, // 6%
  AJIO: 0.02, // 2%
};

export const CACHE_TTL = {
  PRODUCTS: 3600, // 1 hour
  SEARCHES: 300, // 5 minutes
  PRICE_HISTORY: 86400, // 1 day
  REVIEWS: 604800, // 7 days
};
