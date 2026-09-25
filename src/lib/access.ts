/**
 * Who can see what. Everything here is a plain rule — the check itself lives in src/middleware.ts.
 *
 * Free for everyone (the "try before you buy" preview):
 *  - the home page, contents and every topic's outline page
 *  - the whole first topic of each subject (lessons, questions, solutions)
 *  - Dictionary, Listen and Mental math
 * Everything else — the rest of the lessons, simulations, review, rules, search — needs an active purchase.
 */
export const FREE_TOPICS = new Set([1, 21, 30, 40]); // first topic of Algebra, Word Problems, Geometry, Verbal

const OPEN_PREFIXES = ["/plan", "/login", "/auth", "/join", "/account", "/dictionary", "/listen", "/mental-math", "/api/payments", "/_next", "/figures", "/favicon"];

export type AccessNeed = "open" | "paid";

export function accessFor(pathname: string): AccessNeed {
  if (pathname === "/") return "open";
  if (OPEN_PREFIXES.some((p) => pathname === p || pathname.startsWith(p + "/") || pathname.startsWith(p + "?"))) return "open";
  const m = pathname.match(/^\/topic\/(\d+)(\/\d+)?\/?$/);
  if (m) return !m[2] || FREE_TOPICS.has(Number(m[1])) ? "open" : "paid"; // outline pages are always open
  return "paid";
}

/** Accounts are switched on only when the Supabase keys are configured (see SETUP.md). */
export const accountsEnabled = () => !!(process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);
