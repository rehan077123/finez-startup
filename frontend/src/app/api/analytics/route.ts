import { NextRequest, NextResponse } from "next/server";

interface AnalyticsEventRequest {
  event: string;
  productId?: string;
  category?: string;
  properties?: Record<string, any>;
}

export async function POST(request: NextRequest) {
  try {
    const body: AnalyticsEventRequest = await request.json();

    if (!body.event) {
      return NextResponse.json(
        { error: "event is required" },
        { status: 400 }
      );
    }

    // Track events (in production, send to PostHog, Mixpanel, etc.)
    console.log(`[Analytics] Event: ${body.event}`, {
      productId: body.productId,
      category: body.category,
      properties: body.properties,
      timestamp: new Date().toISOString(),
    });

    return NextResponse.json({
      success: true,
      event: body.event,
      tracked: true,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to track event", details: String(error) },
      { status: 500 }
    );
  }
}
