import { NextRequest, NextResponse } from "next/server";

// Mock products for search
const mockProducts = [
  { id: '1', name: 'Apple AirPods Pro', price: 24999, originalPrice: 34900, image: 'https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg', rating: 4.5, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/Apple-AirPods-Pro-MLWK3HN-A/dp/B09JQJX3BY' },
  { id: '2', name: 'Samsung Galaxy S24 Ultra', price: 129999, originalPrice: 159999, image: 'https://m.media-amazon.com/images/I/71vZpWgVCfL._SX679_.jpg', rating: 4.7, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/s?k=Samsung+Galaxy+S24+Ultra' },
  { id: '3', name: 'Apple Watch Series 9', price: 41999, originalPrice: 56900, image: 'https://m.media-amazon.com/images/I/71xJyqBbJaL._SX679_.jpg', rating: 4.4, category: 'Electronics', platform: 'Flipkart', link: 'https://flipkart.com/search?q=Apple+Watch' },
  { id: '4', name: 'MacBook Pro 14 M3', price: 139999, originalPrice: 189999, image: 'https://m.media-amazon.com/images/I/71Z1XheEjhL._SX679_.jpg', rating: 4.8, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/s?k=MacBook+Pro+14+M3' },
];

export async function POST(request: NextRequest) {
  try {
    const { query, userId, filters } = await request.json();

    if (!query) {
      return NextResponse.json(
        { error: "Query is required" },
        { status: 400 }
      );
    }

    // Mock search: filter products by query
    let results = mockProducts.filter(p =>
      p.name.toLowerCase().includes(query.toLowerCase())
    );

    if (filters?.platform) {
      results = results.filter(p => p.platform === filters.platform);
    }

    if (filters?.minPrice) {
      results = results.filter(p => p.price >= filters.minPrice);
    }

    if (filters?.maxPrice) {
      results = results.filter(p => p.price <= filters.maxPrice);
    }

    const response = {
      count: results.length,
      results: results,
      intent: 'search',
    };

    return NextResponse.json(response);
  } catch (error) {
    console.error("Search error:", error);
    return NextResponse.json(
      { error: "Search failed" },
      { status: 500 }
    );
  }
}
