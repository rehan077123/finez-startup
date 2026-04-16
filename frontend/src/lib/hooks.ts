'use client';

import { useEffect, useState, useCallback } from 'react';

interface Product {
  id: string;
  name: string;
  price: number;
  images?: string[];
  platform?: string;
  [key: string]: any;
}

interface UseProductResult {
  data: Product | null;
  product: Product | null;
  loading: boolean;
  isLoading: boolean;
  error: Error | null;
}

interface UseProductsResult {
  products: { products: Product[]; total: number } | null;
  loading: boolean;
  error: Error | null;
}

export function useProducts(
  category?: string,
  limit: number = 20,
  offset: number = 0
): UseProductsResult {
  const [products, setProducts] = useState<{ products: Product[]; total: number } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams({
          limit: limit.toString(),
          offset: offset.toString(),
        });
        if (category && category !== 'all') {
          params.append('category', category);
        }
        const response = await fetch(`/api/products?${params}`);
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch products');
        }
        setProducts(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error(String(err)));
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, [category, limit, offset]);

  return { products, loading, error };
}

export function useProduct(productId: string): UseProductResult {
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!productId) return;
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/products/${productId}`);
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch product');
        }
        setProduct(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error(String(err)));
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [productId]);

  return { data: product, product, loading, isLoading: loading, error };
}

export function useWishlist() {
  const [wishlist, setWishlist] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    try {
      if (typeof window !== 'undefined') {
        const saved = localStorage.getItem('wishlist');
        if (saved) {
          setWishlist(JSON.parse(saved));
        }
      }
    } catch (err) {
      console.error('Error loading wishlist:', err);
    }
  }, []);

  const saveWishlist = useCallback((items: string[]) => {
    try {
      if (typeof window !== 'undefined') {
        localStorage.setItem('wishlist', JSON.stringify(items));
      }
    } catch (err) {
      console.error('Error saving wishlist:', err);
    }
  }, []);

  const addToWishlist = useCallback(
    (productId: string) => {
      setWishlist((prev) => {
        if (prev.includes(productId)) return prev;
        const updated = [...prev, productId];
        saveWishlist(updated);
        return updated;
      });
    },
    [saveWishlist]
  );

  const removeFromWishlist = useCallback(
    (productId: string) => {
      setWishlist((prev) => {
        const updated = prev.filter((id) => id !== productId);
        saveWishlist(updated);
        return updated;
      });
    },
    [saveWishlist]
  );

  const isInWishlist = useCallback(
    (productId: string) => wishlist.includes(productId),
    [wishlist]
  );

  return {
    wishlist,
    addToWishlist,
    removeFromWishlist,
    isInWishlist,
    loading,
    error,
    items: wishlist,
    removeItem: removeFromWishlist,
    clearWishlist: () => {
      setWishlist([]);
      saveWishlist([]);
    },
  };
}
