import { NextRequest, NextResponse } from "next/server";

interface VerifyEmailRequest {
  token: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: VerifyEmailRequest = await request.json();

    if (!body.token) {
      return NextResponse.json(
        { error: "Verification token is required" },
        { status: 400 }
      );
    }

    // Verify token (in production, check against database)
    // For now, mock verification
    const isValid = body.token.length > 10;

    if (!isValid) {
      return NextResponse.json(
        { error: "Invalid or expired token" },
        { status: 400 }
      );
    }

    return NextResponse.json({
      success: true,
      message: "Email verified successfully",
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Email verification failed", details: String(error) },
      { status: 500 }
    );
  }
}
