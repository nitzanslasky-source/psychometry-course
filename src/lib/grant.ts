import "server-only";

import { supabaseAdmin } from "./supabase/server";

/** Give an email full access (a paid order, or a manual grant). Safe to call twice for the same reference. */
export async function grantAccess(email: string, source: string, reference?: string) {
  const sb = supabaseAdmin();
  if (!sb) throw new Error("SUPABASE_SERVICE_ROLE_KEY is not set");
  const clean = email.trim().toLowerCase();
  if (reference) {
    const { data } = await sb.from("entitlements").select("id").eq("reference", reference).maybeSingle();
    if (data) return { already: true };
  }
  const { error } = await sb.from("entitlements").insert({ email: clean, source, reference: reference ?? null });
  if (error) throw error;
  return { already: false };
}
