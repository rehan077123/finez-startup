import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    // Verify webhook signature
    const signature = request.headers.get("webhook-signature");

    if (!signature) {
      return NextResponse.json(
        { error: "Missing webhook signature" },
        { status: 401 }
      );
    }

    const body = await request.json();

    // Handle different webhook events
    switch (body.event) {
      case "payment.success":
        console.log("Payment successful:", body.orderId);
        // Update order status
        break;

      case "payment.failed":
        console.log("Payment failed:", body.orderId);
        // Notify user
        break;

      case "subscription.started":
        console.log("Subscription started:", body.userId);
        // Grant premium features
        break;

      case "subscription.cancelled":
        console.log("Subscription cancelled:", body.userId);
        // Remove premium features
        break;

      default:
        console.log("Unknown event:", body.event);
    }

    return NextResponse.json({
      success: true,
      event: body.event,
      processed: true,
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Webhook processing failed", details: String(error) },
      { status: 500 }
    );
  }
}
