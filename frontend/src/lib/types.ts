// Affiliate tracking types
export interface AffiliateClick {
  id: string;
  product_id: string;
  user_id?: string;
  session_id: string;
  affiliate_link: string;
  source_url: string;
  user_agent: string;
  ip_address: string;
  created_at: string;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  image_url: string;
  price: number;
  affiliate_url: string;
  category: string;
  created_at: string;
  updated_at: string;
}

export interface SavedSearch {
  id: string;
  user_id: string;
  search_query: string;
  filters: Record<string, any>;
  created_at: string;
}

export interface PriceAlert {
  id: string;
  user_id: string;
  product_id: string;
  target_price: number;
  is_active: boolean;
  created_at: string;
}
