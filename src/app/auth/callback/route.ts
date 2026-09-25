import { NextResponse } from "next/server";
import { supabaseServer } from "@/lib/supabase/server";

/** Google login lands here: swap the one-time code for a session, then continue. */
export async function GET(req: Request) {
  const url = new URL(req.url);
  const code = url.searchParams.get("code");
  const next = url.searchParams.get("next") || "/";
  const safe = next.startsWith("/") && !next.startsWith("//") ? next : "/";
  const sb = await supabaseServer();
  if (sb && code) await sb.auth.exchangeCodeForSession(code);
  return NextResponse.redirect(new URL(safe, url.origin));
}
