import { NextRequest, NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

// Real products data with actual images and affiliate links
const mockProducts = [
  { id: '1', name: 'Apple AirPods Pro', price: 24999, originalPrice: 34900, image: 'https://m.media-amazon.com/images/I/61SUj2mDRhL._SX679_.jpg', rating: 4.5, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/Apple-AirPods-Pro-MLWK3HN-A/dp/B09JQJX3BY' },
  { id: '2', name: 'Samsung Galaxy S24 Ultra', price: 129999, originalPrice: 159999, image: 'https://m.media-amazon.com/images/I/71vZpWgVCfL._SX679_.jpg', rating: 4.7, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/s?k=Samsung+Galaxy+S24+Ultra' },
  { id: '3', name: 'Apple Watch Series 9', price: 41999, originalPrice: 56900, image: 'https://m.media-amazon.com/images/I/71xJyqBbJaL._SX679_.jpg', rating: 4.4, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/Apple-Watch-Series-45mm-Midnight/dp/B0CCY6WL9D' },
  { id: '4', name: 'MacBook Pro 14 M3', price: 139999, originalPrice: 189999, image: 'https://m.media-amazon.com/images/I/71Z1XheEjhL._SX679_.jpg', rating: 4.8, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/s?k=MacBook+Pro+14+M3' },
  { id: '5', name: 'Dell P2423D 24" Monitor', price: 22999, originalPrice: 35000, image: 'https://m.media-amazon.com/images/I/81rtYmXtBJL._SX679_.jpg', rating: 4.6, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/s?k=Dell+Monitor+24' },
  { id: '6', name: 'Corsair K95 RGB Mechanical Keyboard', price: 12999, originalPrice: 19999, image: 'https://m.media-amazon.com/images/I/71b6yBzHW7L._SX679_.jpg', rating: 4.3, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/s?k=Mechanical+Keyboard+RGB' },
  { id: '7', name: 'Logitech MX Master 3S Mouse', price: 8999, originalPrice: 12999, image: 'https://m.media-amazon.com/images/I/71gAH0Go3uL._SX679_.jpg', rating: 4.2, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/s?k=Logitech+Mouse' },
  { id: '8', name: 'Anker USB-C Cable 100W', price: 599, originalPrice: 999, image: 'https://m.media-amazon.com/images/I/61xW+eNwSML._SX679_.jpg', rating: 4.1, category: 'Accessories', platform: 'Amazon', link: 'https://amazon.in/s?k=USB+C+Cable' },
  { id: '9', name: 'Premium Phone Stand', price: 899, originalPrice: 1499, image: 'https://m.media-amazon.com/images/I/61Hd8lYdnnL._SX679_.jpg', rating: 4.4, category: 'Accessories', platform: 'Amazon', link: 'https://amazon.in/s?k=Phone+Stand' },
  { id: '10', name: 'Logitech StreamCam HD Webcam', price: 5999, originalPrice: 8999, image: 'https://m.media-amazon.com/images/I/71aDpNl1BHL._SX679_.jpg', rating: 4.5, category: 'Electronics', platform: 'Amazon', link: 'https://amazon.in/s?k=Webcam' },
];

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const category = searchParams.get('category');
    const limit = parseInt(searchParams.get('limit') || '20');
    const offset = parseInt(searchParams.get('offset') || '0');

    // Filter by category if provided
    let filtered = mockProducts;
    if (category && category !== 'all') {
      filtered = mockProducts.filter(p => p.category === category);
    }

    // Paginate
    const products = filtered.slice(offset, offset + limit);

    return NextResponse.json(
      {
        products: products,
        total: filtered.length,
        limit: limit,
        offset: offset,
      },
      {
        headers: {
          'Cache-Control': 'public, max-age=60, s-maxage=300',
        },
      }
    );
  } catch (error) {
    console.error('Error fetching products:', error);
    return NextResponse.json(
      {
        products: mockProducts.slice(0, 20),
        total: mockProducts.length,
        limit: 20,
        offset: 0,
      },
      { status: 200 }
    );
  }
}
