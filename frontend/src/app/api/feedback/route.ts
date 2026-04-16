import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const { email, reason } = body;

    if (!email) {
      return NextResponse.json(
        { error: "Email is required" },
        { status: 400 }
      );
    }

    // In production, send actual email using Resend or similar
    console.log(`[Feedback] Email: ${email}, Reason: ${reason}`);

    return NextResponse.json({
      success: true,
      message: "Feedback received",
      email,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to submit feedback", details: String(error) },
      { status: 500 }
    );
  }
}
