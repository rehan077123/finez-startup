import { NextRequest, NextResponse } from "next/server";

interface SocialCardRequest {
  productId: string;
  productName: string;
  productPrice: number;
  productImage?: string;
  platform: "twitter" | "facebook" | "pinterest" | "linkedin";
}

export async function POST(request: NextRequest) {
  try {
    const body: SocialCardRequest = await request.json();

    if (!body.productName || !body.productPrice) {
      return NextResponse.json(
        { error: "productName and productPrice are required" },
        { status: 400 }
      );
    }

    const templates: Record<string, string> = {
      twitter: `Just found "${body.productName}" for $${body.productPrice.toFixed(2)} on @FineZDeals! Amazing deal! 🎉 #Shopping #Deals`,
      facebook: `Check out this deal! ${body.productName} is available for just $${body.productPrice.toFixed(2)}!`,
      pinterest: `${body.productName} - Only $${body.productPrice.toFixed(2)} | Best Deals on FineZ`,
      linkedin: `Discover great deals on quality products like ${body.productName} at unbeatable prices on FineZ.`,
    };

    return NextResponse.json({
      success: true,
      productId: body.productId,
      platform: body.platform,
      cardContent: templates[body.platform],
      ogImage: body.productImage || "https://finez.com/og-image.png",
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to generate social card", details: String(error) },
      { status: 500 }
    );
  }
}
