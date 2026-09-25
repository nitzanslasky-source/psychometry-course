import { NextResponse, type NextRequest } from "next/server";
import { createServerClient } from "@supabase/ssr";
import { accessFor } from "@/lib/access";

/**
 * Keeps the login session fresh and locks paid pages.
 * - Accounts not configured yet (no Supabase keys): everything stays open, as during development.
 * - Paid page, not logged in → /login.   Paid page, logged in without a purchase → /join.
 */
export async function middleware(req: NextRequest) {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !key) return NextResponse.next();

  let res = NextResponse.next({ request: req });
  const sb = createServerClient(url, key, {
    cookies: {
      getAll: () => req.cookies.getAll(),
      setAll: (list) => {
        list.forEach(({ name, value }) => req.cookies.set(name, value));
        res = NextResponse.next({ request: req });
        list.forEach(({ name, value, options }) => res.cookies.set(name, value, options));
      },
    },
  });
  const { data } = await sb.auth.getUser();

  const path = req.nextUrl.pathname;
  if (accessFor(path) === "open") return res;

  const isApi = path.startsWith("/api/");
  const next = encodeURIComponent(path + req.nextUrl.search);
  if (!data.user) {
    if (isApi) return NextResponse.json({ error: "login required" }, { status: 401 });
    return NextResponse.redirect(new URL(`/login?next=${next}`, req.url));
  }
  const { data: ok } = await sb.rpc("has_access");
  if (!ok) {
    if (isApi) return NextResponse.json({ error: "purchase required" }, { status: 402 });
    return NextResponse.redirect(new URL(`/join?next=${next}`, req.url));
  }
  return res;
}

export const config = {
  // everything except static assets and images
  matcher: ["/((?!_next/static|_next/image|favicon.ico|figures/|.*\\.(?:png|jpg|jpeg|svg|webp|gif)$).*)"],
};
