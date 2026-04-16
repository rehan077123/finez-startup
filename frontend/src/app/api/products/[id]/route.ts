import { NextRequest, NextResponse } from 'next/server';

// Real products
const mockProducts = [
  { id: '1', name: 'Apple AirPods Pro', price: 24999, originalPrice: 34900, image: 'https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg', rating: 4.5, category: 'Electronics', description: 'Premium wireless earbuds with active noise cancellation', link: 'https://amazon.in/Apple-AirPods-Pro-MLWK3HN-A/dp/B09JQJX3BY' },
  { id: '2', name: 'Samsung Galaxy S24 Ultra', price: 129999, originalPrice: 159999, image: 'https://m.media-amazon.com/images/I/71vZpWgVCfL._SX679_.jpg', rating: 4.7, category: 'Electronics', description: 'Latest flagship smartphone with 200MP camera', link: 'https://amazon.in/s?k=Samsung+Galaxy+S24+Ultra' },
  { id: '3', name: 'Apple Watch Series 9', price: 41999, originalPrice: 56900, image: 'https://m.media-amazon.com/images/I/71xJyqBbJaL._SX679_.jpg', rating: 4.4, category: 'Electronics', description: 'Advanced health and fitness tracker', link: 'https://amazon.in/Apple-Watch-Series-45mm-Midnight/dp/B0CCY6WL9D' },
  { id: '4', name: 'MacBook Pro 14 M3', price: 139999, originalPrice: 189999, image: 'https://m.media-amazon.com/images/I/71Z1XheEjhL._SX679_.jpg', rating: 4.8, category: 'Electronics', description: 'Powerful laptop for professionals and developers', link: 'https://amazon.in/s?k=MacBook+Pro+14+M3' },
];

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const product = mockProducts.find(p => p.id === params.id);

    if (!product) {
      return NextResponse.json(
        { error: 'Product not found' },
        { status: 404 }
      );
    }

    return NextResponse.json(product, {
      headers: {
        'Cache-Control': 'public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800',
      },
    });
  } catch (error) {
    console.error('Error fetching product:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
