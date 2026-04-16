import { NextRequest, NextResponse } from "next/server";

interface AffiliateTrackRequest {
  productId: string;
  affiliation: string;
  referrer?: string;
  campaign?: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: AffiliateTrackRequest = await request.json();

    if (!body.productId || !body.affiliation) {
      return NextResponse.json(
        { error: "productId and affiliation are required" },
        { status: 400 }
      );
    }

    // Log affiliate click
    console.log({
      event: "affiliate_click",
      productId: body.productId,
      affiliation: body.affiliation,
      referrer: body.referrer,
      campaign: body.campaign,
      timestamp: new Date().toISOString(),
    });

    return NextResponse.json({
      success: true,
      trackingId: `track_${Date.now()}`,
      productId: body.productId,
      affiliation: body.affiliation,
      affiliateLink: `https://finez.com/go?product=${body.productId}&aff=${body.affiliation}`,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Affiliate tracking failed", details: String(error) },
      { status: 500 }
    );
  }
}
