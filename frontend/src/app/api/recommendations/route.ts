import { NextRequest, NextResponse } from "next/server";

export const dynamic = 'force-dynamic';

interface RecommendationRequest {
  userId?: string;
  productId?: string;
  category?: string;
  limit?: number;
}

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const userId = searchParams.get("userId");
    const productId = searchParams.get("productId");
    const category = searchParams.get("category");
    const limit = parseInt(searchParams.get("limit") || "10");

    // Mock recommendations based on context
    const mockRecommendations = [
      {
        id: "rec1",
        name: "Recommended Product 1",
        price: 149.99,
        rating: 4.7,
        reason: "Based on your browsing history",
      },
      {
        id: "rec2",
        name: "Recommended Product 2",
        price: 199.99,
        rating: 4.6,
        reason: "Customers also bought this",
      },
      {
        id: "rec3",
        name: "Recommended Product 3",
        price: 129.99,
        rating: 4.8,
        reason: "Trending in your category",
      },
    ];

    return NextResponse.json({
      success: true,
      recommendations: mockRecommendations.slice(0, limit),
      context: {
        userId,
        productId,
        category,
      },
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to fetch recommendations", details: String(error) },
      { status: 500 }
    );
  }
}
