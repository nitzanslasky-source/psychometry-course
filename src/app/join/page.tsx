import Link from "next/link";
import { currentStudent } from "@/lib/supabase/server";
import { getOutline } from "@/lib/fullCourse";

export const metadata = { title: "Get full access — Psychometry" };
export const dynamic = "force-dynamic";

/**
 * The "buy" page. Payment itself happens on the provider's hosted page (PAYMENT_LINK in .env),
 * which reports back to /api/payments/webhook — that grants access to the paying email.
 */
export default async function JoinPage({ searchParams }: { searchParams: Promise<{ next?: string }> }) {
  const { next } = await searchParams;
  const me = await currentStudent();
  const all = getOutline().subjects.flatMap((s) => s.topics);
  const lessons = all.reduce((n, t) => n + t.lessons, 0);
  const questions = all.reduce((n, t) => n + t.questions, 0);
  const solutions = all.reduce((n, t) => n + t.videos, 0) - lessons;
  const link = process.env.PAYMENT_LINK;
  const price = process.env.NEXT_PUBLIC_PRICE_LABEL;
  const contact = process.env.NEXT_PUBLIC_CONTACT_EMAIL;
  const payHref = link && me.user ? `${link}${link.includes("?") ? "&" : "?"}email=${encodeURIComponent(me.user.email)}` : link;

  return (
    <main className="mx-auto max-w-5xl px-6">
      <section className="rise-in grid gap-12 pb-16 pt-16 md:grid-cols-[1.3fr_1fr]">
        <div>
          <div className="eyebrow">Full access</div>
          <h1 className="display mt-4 text-[52px] sm:text-[60px]">The whole course, start to exam day.</h1>
          <ul className="mt-8 space-y-3 text-[16px] text-ink-soft">
            {[
              `${all.length} topics — Algebra, Word Problems, Geometry and Verbal Reasoning — with ${lessons} video lessons`,
              `${questions.toLocaleString()} questions and ${solutions} worked-solution videos`,
              "Real exam sections in English, timed, with full solutions",
              "Review: your mistakes come back until they stick",
              "Rules to know, the dictionary, Listen and Mental math",
            ].map((x) => (
              <li key={x} className="flex gap-3">
                <span className="mt-1 text-gold">✓</span>
                <span>{x}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="card self-start p-8">
          {me.access && me.user ? (
            <>
              <div className="display text-[32px]">You’re in.</div>
              <p className="mt-2 text-sm text-muted">{me.user.email} has full access.</p>
              <Link href={next || "/"} className="btn mt-6 w-full py-3">
                Continue learning →
              </Link>
            </>
          ) : (
            <>
              {price && <div className="display text-[44px]">{price}</div>}
              <p className="mt-1 text-sm text-muted">One payment · full access to everything</p>
              {!me.user && me.enabled ? (
                <>
                  <p className="mt-6 text-sm text-ink-soft">First, log in or create your account (free, no password):</p>
                  <Link href={`/login?next=${encodeURIComponent("/join" + (next ? `?next=${encodeURIComponent(next)}` : ""))}`} className="btn mt-3 w-full py-3">
                    Log in / sign up
                  </Link>
                </>
              ) : payHref ? (
                <a href={payHref} className="btn mt-6 w-full py-3">
                  Get full access →
                </a>
              ) : (
                <p className="mt-6 rounded-xl bg-paper-deep p-4 text-sm text-ink-soft">
                  Online payment opens soon.{contact ? <> To join now, write to <b className="font-medium text-ink">{contact}</b>.</> : null}
                </p>
              )}
              {me.user && <p className="mt-4 text-xs text-muted">Access will be added to {me.user.email}.</p>}
              <p className="mt-6 border-t border-line pt-4 text-xs text-muted">
                Not sure yet? The first topic of every subject is free — <Link href="/#contents" className="link">try it</Link>.
              </p>
            </>
          )}
        </div>
      </section>
    </main>
  );
}
