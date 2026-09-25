import { NextResponse } from "next/server";
import { supabaseServer } from "@/lib/supabase/server";

export async function POST(req: Request) {
  const sb = await supabaseServer();
  if (sb) await sb.auth.signOut();
  return NextResponse.redirect(new URL("/", req.url), { status: 303 });
}
