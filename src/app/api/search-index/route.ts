import { NextResponse } from "next/server";
import { getSearchIndex } from "@/lib/searchIndex";

/** The whole-site search index (loaded once, the first time a student opens search). */
export async function GET() {
  return NextResponse.json(getSearchIndex(), { headers: { "Cache-Control": "private, max-age=3600" } });
}
