import { NextRequest, NextResponse } from "next/server";

export const dynamic = 'force-dynamic';

interface ProductComparisonRequest {
  productIds: string[];
  specs?: string[];
}

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const productIds = searchParams.getAll("ids");

    if (!productIds || productIds.length === 0) {
      return NextResponse.json(
        { error: "At least one product ID is required" },
        { status: 400 }
      );
    }

    // Mock comparison data
    const mockProducts: Record<string, any> = {
      1: {
        id: "1",
        name: "iPhone 15 Pro",
        price: 999,
        storage: "256GB",
        ram: "8GB",
        battery: "3200mAh",
        rating: 4.8,
      },
      2: {
        id: "2",
        name: "Samsung S24",
        price: 999,
        storage: "512GB",
        ram: "12GB",
        battery: "4000mAh",
        rating: 4.6,
      },
    };

    const products = productIds
      .map((id) => mockProducts[id])
      .filter(Boolean);

    return NextResponse.json({
      success: true,
      products,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to fetch comparison", details: String(error) },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body: ProductComparisonRequest = await request.json();

    if (!body.productIds || body.productIds.length === 0) {
      return NextResponse.json(
        { error: "At least one product ID is required" },
        { status: 400 }
      );
    }

    // Generate comparison report (mock)
    const mockProducts = [
      {
        id: body.productIds[0],
        name: "Product A",
        specs: { Price: "$99", RAM: "8GB", Storage: "256GB" },
        winner: true,
      },
      {
        id: body.productIds[1],
        name: "Product B",
        specs: { Price: "$129", RAM: "12GB", Storage: "512GB" },
        winner: false,
      },
    ];

    return NextResponse.json({
      success: true,
      comparison: {
        products: mockProducts.filter((p) =>
          body.productIds.includes(p.id)
        ),
        verdict: `${mockProducts[0].name} offers better value`,
      },
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to create comparison", details: String(error) },
      { status: 500 }
    );
  }
}
