import { NextRequest, NextResponse } from "next/server";

/**
 * Delete a price alert (mock)
 * DELETE /api/alerts/[id]
 */

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // Mock: just return success
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Alert deletion error:", error);
    return NextResponse.json(
      { error: "Failed to delete alert" },
      { status: 500 }
    );
  }
}
