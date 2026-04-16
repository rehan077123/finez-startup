import { NextRequest, NextResponse } from "next/server";
import { getSupabaseServer, isSupabaseConfigured } from "@/config/supabase";
import { getRedis } from "@/config/redis";

export const dynamic = 'force-dynamic';

/**
 * Price alerts - set/get/delete price alerts
 * POST /api/alerts - Create alert
 * GET /api/alerts?userId=xxx - Get user alerts
 * DELETE /api/alerts/[id] - Delete alert
 */

export async function POST(request: NextRequest) {
  try {
    const { userId, productId, targetPrice, platform } = await request.json();

    if (!userId || !productId || !targetPrice) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 }
      );
    }

    if (!isSupabaseConfigured()) {
      return NextResponse.json(
        { error: "Supabase not configured" },
        { status: 500 }
      );
    }

    const { data, error } = await getSupabaseServer()
      .from("price_alerts")
      .insert({
        userId,
        productId,
        targetPrice,
        platform: platform || "AMAZON",
        isActive: true,
      })
      .select()
      .single();

    if (error) throw error;

    // Invalidate user's alerts cache
    await getRedis().del(`alerts:${userId}`);

    return NextResponse.json(data, { status: 201 });
  } catch (error) {
    console.error("Alert creation error:", error);
    return NextResponse.json(
      { error: "Failed to create alert" },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get("userId");

    if (!userId) {
      return NextResponse.json(
        { error: "userId is required" },
        { status: 400 }
      );
    }

    // Check cache
    const cached = await getRedis().get(`alerts:${userId}`);
    if (cached) {
      return NextResponse.json(JSON.parse(cached as string));
    }

    if (!isSupabaseConfigured()) {
      return NextResponse.json(
        { error: "Supabase not configured" },
        { status: 500 }
      );
    }

    const { data: alerts, error } = await getSupabaseServer()
      .from("price_alerts")
      .select("*")
      .eq("userId", userId)
      .eq("isActive", true);

    if (error) throw error;

    // Cache for 1 hour
    await getRedis().set(`alerts:${userId}`, JSON.stringify(alerts), { ex: 3600 });

    return NextResponse.json(alerts);
  } catch (error) {
    console.error("Alerts fetch error:", error);
    return NextResponse.json(
      { error: "Failed to fetch alerts" },
      { status: 500 }
    );
  }
}
