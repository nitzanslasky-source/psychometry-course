import { NextResponse } from "next/server";
import { coreWordKeys, getReviewItems } from "@/lib/reviewData";

/** POST { keys: string[] } → the items to show in Review.  GET → the core word list (for "add new words"). */
export async function POST(req: Request) {
  const body = (await req.json().catch(() => ({}))) as { keys?: unknown };
  const keys = Array.isArray(body.keys) ? body.keys.filter((k): k is string => typeof k === "string").slice(0, 400) : [];
  return NextResponse.json(getReviewItems(keys));
}

export async function GET() {
  return NextResponse.json(coreWordKeys());
}
