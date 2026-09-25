import "server-only";

import { cookies } from "next/headers";
import { createServerClient } from "@supabase/ssr";
import { createClient } from "@supabase/supabase-js";

/** Supabase for server components / route handlers, acting as the logged-in student. */
export async function supabaseServer() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !key) return null;
  const jar = await cookies();
  return createServerClient(url, key, {
    cookies: {
      getAll: () => jar.getAll(),
      setAll: (list) => {
        try {
          list.forEach(({ name, value, options }) => jar.set(name, value, options));
        } catch {
          /* called from a server component — the middleware refreshes cookies instead */
        }
      },
    },
  });
}

/** Admin client (service role) — ONLY for trusted server code such as the payment webhook. */
export function supabaseAdmin() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) return null;
  return createClient(url, key, { auth: { persistSession: false } });
}

/** The logged-in student and whether they have paid access. */
export async function currentStudent() {
  const sb = await supabaseServer();
  if (!sb) return { enabled: false as const, user: null, access: true };
  const { data } = await sb.auth.getUser();
  if (!data.user) return { enabled: true as const, user: null, access: false };
  const { data: ok } = await sb.rpc("has_access");
  return { enabled: true as const, user: { id: data.user.id, email: data.user.email ?? "" }, access: !!ok };
}
