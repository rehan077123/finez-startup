import { NextRequest, NextResponse } from "next/server";

interface ReviewSummaryRequest {
  productId: string;
  reviews: Array<{
    rating: number;
    text: string;
    author: string;
  }>;
}

// Grouping and summarization (can be enhanced with Anthropic API)
function summarizeReviews(reviews: ReviewSummaryRequest["reviews"]) {
  const grouped = {
    pros: [] as string[],
    cons: [] as string[],
    praise: [] as string[],
    complaints: [] as string[],
  };

  const keywordMapping = {
    pros: [
      "excellent",
      "great",
      "amazing",
      "good",
      "perfect",
      "best",
      "love",
      "awesome",
    ],
    cons: [
      "bad",
      "terrible",
      "poor",
      "worse",
      "hate",
      "disappointed",
      "broken",
      "doesn't work",
    ],
    praise: ["5 star", "highly recommend", "worth it", "best purchase"],
    complaints: [
      "waste of money",
      "not worth",
      "return",
      "disappointed",
      "regret",
    ],
  };

  reviews.forEach((review) => {
    const text = review.text.toLowerCase();
    Object.entries(keywordMapping).forEach(([key, keywords]) => {
      if (keywords.some((keyword) => text.includes(keyword))) {
        grouped[key as keyof typeof grouped].push(review.text);
      }
    });
  });

  return {
    pros: grouped.pros.slice(0, 3),
    cons: grouped.cons.slice(0, 3),
    praise: grouped.praise.slice(0, 2),
    complaints: grouped.complaints.slice(0, 2),
    averageRating:
      reviews.reduce((acc, r) => acc + r.rating, 0) / reviews.length,
    totalReviews: reviews.length,
  };
}

export async function POST(request: NextRequest) {
  try {
    const body: ReviewSummaryRequest = await request.json();

    if (!body.productId || !body.reviews) {
      return NextResponse.json(
        { error: "productId and reviews are required" },
        { status: 400 }
      );
    }

    if (body.reviews.length === 0) {
      return NextResponse.json(
        {
          success: true,
          summary: {
            pros: [],
            cons: [],
            praise: [],
            complaints: [],
            averageRating: 0,
            totalReviews: 0,
          },
        }
      );
    }

    const summary = summarizeReviews(body.reviews);

    return NextResponse.json({
      success: true,
      productId: body.productId,
      summary,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to summarize reviews", details: String(error) },
      { status: 500 }
    );
  }
}
