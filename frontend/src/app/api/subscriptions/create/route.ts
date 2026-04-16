import { NextRequest, NextResponse } from "next/server";

interface SubscriptionRequest {
  userId: string;
  planId: string;
  paymentMethodId?: string;
  billingCycle?: "monthly" | "yearly";
}

export async function POST(request: NextRequest) {
  try {
    const body: SubscriptionRequest = await request.json();

    if (!body.userId || !body.planId) {
      return NextResponse.json(
        { error: "userId and planId are required" },
        { status: 400 }
      );
    }

    // In production, create subscription in Razorpay
    const subscriptionId = `sub_${Date.now()}`;

    return NextResponse.json({
      success: true,
      subscriptionId,
      userId: body.userId,
      planId: body.planId,
      billingCycle: body.billingCycle || "monthly",
      status: "active",
      nextBillingDate: new Date(
        Date.now() + 30 * 24 * 60 * 60 * 1000
      ).toISOString(),
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Subscription creation failed", details: String(error) },
      { status: 500 }
    );
  }
}
