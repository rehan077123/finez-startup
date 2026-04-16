import { NextRequest, NextResponse } from "next/server";

interface RefundRequest {
  paymentId: string;
  orderId: string;
  amount?: number;
  reason?: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: RefundRequest = await request.json();

    if (!body.paymentId || !body.orderId) {
      return NextResponse.json(
        { error: "paymentId and orderId are required" },
        { status: 400 }
      );
    }

    // In production, call Razorpay refund API
    const refundId = `ref_${Date.now()}`;

    return NextResponse.json({
      success: true,
      refundId,
      paymentId: body.paymentId,
      orderId: body.orderId,
      amount: body.amount,
      reason: body.reason || "Refund requested",
      status: "processed",
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Refund processing failed", details: String(error) },
      { status: 500 }
    );
  }
}
