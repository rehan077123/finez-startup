import { NextRequest, NextResponse } from "next/server";

interface PaymentInitRequest {
  orderId: string;
  amount: number;
  currency?: string;
  email: string;
  phone: string;
  description?: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: PaymentInitRequest = await request.json();

    if (!body.orderId || !body.amount || !body.email) {
      return NextResponse.json(
        { error: "orderId, amount, and email are required" },
        { status: 400 }
      );
    }

    // In production, integrate with Razorpay API
    // For now, generate mock payment link
    const paymentId = `pay_${Date.now()}`;
    const paymentLink = `https://checkout.razorpay.com/?key=${paymentId}`;

    return NextResponse.json({
      success: true,
      paymentId,
      orderId: body.orderId,
      amount: body.amount,
      currency: body.currency || "USD",
      paymentLink,
      expiresIn: 15 * 60, // 15 minutes
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Payment initialization failed", details: String(error) },
      { status: 500 }
    );
  }
}
