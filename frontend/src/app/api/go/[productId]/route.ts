import { NextRequest, NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

// Real products with affiliate URLs
const mockProducts = [
  { id: '1', name: 'Apple AirPods Pro', affiliate_url: 'https://amazon.in/Apple-AirPods-Pro-MLWK3HN-A/dp/B09JQJX3BY' },
  { id: '2', name: 'Samsung Galaxy S24 Ultra', affiliate_url: 'https://amazon.in/s?k=Samsung+Galaxy+S24+Ultra' },
  { id: '3', name: 'Apple Watch Series 9', affiliate_url: 'https://amazon.in/Apple-Watch-Series-45mm-Midnight/dp/B0CCY6WL9D' },
  { id: '4', name: 'MacBook Pro 14 M3', affiliate_url: 'https://amazon.in/s?k=MacBook+Pro+14+M3' },
  { id: '5', name: 'Dell P2423D 24" Monitor', affiliate_url: 'https://amazon.in/s?k=Dell+Monitor+24' },
  { id: '6', name: 'Corsair K95 RGB Mechanical Keyboard', affiliate_url: 'https://amazon.in/s?k=Mechanical+Keyboard+RGB' },
  { id: '7', name: 'Logitech MX Master 3S Mouse', affiliate_url: 'https://amazon.in/s?k=Logitech+Mouse' },
  { id: '8', name: 'Anker USB-C Cable 100W', affiliate_url: 'https://amazon.in/s?k=USB+C+Cable' },
  { id: '9', name: 'Premium Phone Stand', affiliate_url: 'https://amazon.in/s?k=Phone+Stand' },
  { id: '10', name: 'Logitech StreamCam HD Webcam', affiliate_url: 'https://amazon.in/s?k=Webcam' },
];

export async function GET(
  request: NextRequest,
  { params }: { params: { productId: string } }
) {
  try {
    const productId = params.productId;

    // Find product
    const product = mockProducts.find(p => p.id === productId);

    if (!product) {
      return NextResponse.json(
        { error: 'Product not found' },
        { status: 404 }
      );
    }

    // Redirect to affiliate URL
    return NextResponse.redirect(product.affiliate_url, { status: 301 });
  } catch (error) {
    console.error('Error processing redirect:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
