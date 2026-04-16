import { NextRequest, NextResponse } from "next/server";

interface VerifyPaymentRequest {
  paymentId: string;
  orderId: string;
  signature: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: VerifyPaymentRequest = await request.json();

    if (!body.paymentId || !body.orderId || !body.signature) {
      return NextResponse.json(
        { error: "paymentId, orderId, and signature are required" },
        { status: 400 }
      );
    }

    // In production, verify with Razorpay using HMAC SHA256
    const isValid = body.signature.length > 0; // Mock validation

    if (!isValid) {
      return NextResponse.json(
        { error: "Payment signature verification failed" },
        { status: 400 }
      );
    }

    return NextResponse.json({
      success: true,
      verified: true,
      paymentId: body.paymentId,
      orderId: body.orderId,
      message: "Payment verified successfully",
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Payment verification failed", details: String(error) },
      { status: 500 }
    );
  }
}
