#!/usr/bin/env node
/**
 * Give (or take away) full access by hand — e.g. a student who paid by bank transfer, or a free pass.
 *
 *   node scripts/grant-access.mjs student@example.com            # give access
 *   node scripts/grant-access.mjs student@example.com --revoke   # remove access
 *   node scripts/grant-access.mjs --list                         # who has access
 *
 * Reads NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY from .env.local.
 */
import fs from "node:fs";
import { createClient } from "@supabase/supabase-js";

for (const line of fs.existsSync(".env.local") ? fs.readFileSync(".env.local", "utf8").split("\n") : []) {
  const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
  if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, "");
}
const url = process.env.NEXT_PUBLIC_SUPABASE_URL, key = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!url || !key) { console.error("Set NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env.local first."); process.exit(1); }
const sb = createClient(url, key, { auth: { persistSession: false } });
const [arg, flag] = process.argv.slice(2);

if (arg === "--list") {
  const { data, error } = await sb.from("entitlements").select("email,status,source,created_at").order("created_at");
  if (error) throw error;
  console.table(data);
} else if (arg && arg.includes("@")) {
  const email = arg.trim().toLowerCase();
  if (flag === "--revoke") {
    const { error } = await sb.from("entitlements").update({ status: "revoked" }).eq("email", email);
    if (error) throw error;
    console.log("Access removed for", email);
  } else {
    const { error } = await sb.from("entitlements").insert({ email, source: "manual" });
    if (error) throw error;
    console.log("Full access granted to", email);
  }
} else {
  console.log("Usage: node scripts/grant-access.mjs <email> [--revoke]  |  --list");
}
