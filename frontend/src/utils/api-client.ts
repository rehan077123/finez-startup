// API client for frontend

export async function apiCall<T>(
  endpoint: string,
  options: RequestInit = {}
) {
  const url = `/api${endpoint}`;
  
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return (await response.json()) as T;
}

export const api = {
  search: (query: string, filters?: any) =>
    apiCall("/search", {
      method: "POST",
      body: JSON.stringify({ query, filters }),
    }),
  
  getProduct: (id: string) => 
    apiCall(`/products/${id}`),
  
  getProducts: (page?: number, limit?: number) =>
    apiCall(`/products?page=${page}&limit=${limit}`),
  
  getPriceHistory: (productId: string) =>
    apiCall(`/price-history/${productId}`),
  
  trackClick: (productId: string, platform: string) =>
    apiCall(`/go/${productId}`, {
      method: "POST",
      body: JSON.stringify({ platform }),
    }),
  
  setPriceAlert: (productId: string, targetPrice: number) =>
    apiCall("/alerts", {
      method: "POST",
      body: JSON.stringify({ productId, targetPrice }),
    }),
  
  getReviews: (productId: string, platform: string) =>
    apiCall(`/reviews/${productId}?platform=${platform}`),
  
  shareProduct: (productId: string) =>
    apiCall(`/share?productId=${productId}`),
};
