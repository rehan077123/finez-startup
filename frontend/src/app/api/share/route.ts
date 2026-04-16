import { NextRequest, NextResponse } from "next/server";

interface ShareRequest {
  productId: string;
  productName: string;
  productImage?: string;
  productPrice: number;
  shareChannel: "twitter" | "facebook" | "whatsapp" | "email" | "link";
}

export async function POST(request: NextRequest) {
  try {
    const body: ShareRequest = await request.json();

    if (!body.productId || !body.productName) {
      return NextResponse.json(
        { error: "productId and productName are required" },
        { status: 400 }
      );
    }

    const baseUrl = process.env.NEXT_PUBLIC_APP_URL || "https://finez.com";
    const productUrl = `${baseUrl}/product/${body.productId}`;
    const text = encodeURIComponent(
      `Check out ${body.productName} for $${body.productPrice.toFixed(2)} on FineZ`
    );

    const shareLinks: Record<string, string> = {
      twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(productUrl)}&text=${text}`,
      facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(productUrl)}`,
      whatsapp: `https://wa.me/?text=${text}%20${encodeURIComponent(productUrl)}`,
      email: `mailto:?subject=${encodeURIComponent(body.productName)}&body=${text}`,
      link: productUrl,
    };

    return NextResponse.json({
      success: true,
      productId: body.productId,
      shareLinks: {
        [body.shareChannel]: shareLinks[body.shareChannel],
      },
      allShareLinks: shareLinks,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to generate share link", details: String(error) },
      { status: 500 }
    );
  }
}
