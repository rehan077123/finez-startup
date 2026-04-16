import { NextRequest, NextResponse } from "next/server";

interface IntentRequest {
  query: string;
  context?: string;
}

interface ParsedIntent {
  type: "search" | "product" | "comparePrice" | "findDeal" | "help" | "unknown";
  keywords: string[];
  category?: string;
  filters?: Record<string, any>;
  confidence: number;
}

// Simple intent parser - can be replaced with Anthropic API for ML-based intent
function parseIntent(query: string): ParsedIntent {
  const lowerQuery = query.toLowerCase();

  // Deal/discount intent
  if (
    lowerQuery.includes("cheap") ||
    lowerQuery.includes("discount") ||
    lowerQuery.includes("deal") ||
    lowerQuery.includes("sale")
  ) {
    return {
      type: "findDeal",
      keywords: [query],
      confidence: 0.9,
    };
  }

  // Compare intent
  if (
    lowerQuery.includes("compare") ||
    lowerQuery.includes("vs") ||
    lowerQuery.includes("versus") ||
    lowerQuery.includes("difference")
  ) {
    return {
      type: "comparePrice",
      keywords: query.split(/vs|versus|compare|difference/i),
      confidence: 0.85,
    };
  }

  // Price tracking intent
  if (
    lowerQuery.includes("price") ||
    lowerQuery.includes("cost") ||
    lowerQuery.includes("how much")
  ) {
    return {
      type: "search",
      keywords: [query],
      filters: { sortBy: "price" },
      confidence: 0.8,
    };
  }

  // Help intent
  if (
    lowerQuery.includes("help") ||
    lowerQuery.includes("how to") ||
    lowerQuery.includes("guide")
  ) {
    return {
      type: "help",
      keywords: [query],
      confidence: 0.9,
    };
  }

  // Default search
  return {
    type: "search",
    keywords: [query],
    confidence: 0.6,
  };
}

export async function POST(request: NextRequest) {
  try {
    const body: IntentRequest = await request.json();

    if (!body.query) {
      return NextResponse.json(
        { error: "Query is required" },
        { status: 400 }
      );
    }

    const intent = parseIntent(body.query);

    return NextResponse.json({
      success: true,
      intent,
      originalQuery: body.query,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to parse intent", details: String(error) },
      { status: 500 }
    );
  }
}
