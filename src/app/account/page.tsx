import Link from "next/link";
import { redirect } from "next/navigation";
import { currentStudent } from "@/lib/supabase/server";

export const metadata = { title: "My account — Psychometry" };
export const dynamic = "force-dynamic";

export default async function AccountPage() {
  const me = await currentStudent();
  if (me.enabled && !me.user) redirect("/login?next=/account");
  return (
    <main className="mx-auto max-w-xl px-6">
      <header className="rise-in pb-8 pt-16">
        <div className="eyebrow">Account</div>
        <h1 className="display mt-3 text-[48px]">My account</h1>
      </header>
      {!me.enabled ? (
        <p className="card p-6 text-ink-soft">Accounts aren’t switched on yet on this copy of the site.</p>
      ) : (
        <div className="card divide-y divide-line">
          <div className="flex items-center justify-between px-6 py-5">
            <span className="text-muted">Email</span>
            <span className="font-medium">{me.user?.email}</span>
          </div>
          <div className="flex items-center justify-between px-6 py-5">
            <span className="text-muted">Access</span>
            {me.access ? <span className="font-medium text-ok">Full course</span> : <Link href="/join" className="link">Free preview — get full access</Link>}
          </div>
          <div className="flex items-center justify-between px-6 py-5">
            <span className="text-muted">Progress</span>
            <span className="text-sm text-ink-soft">Saved to your account automatically</span>
          </div>
          <form action="/auth/signout" method="post" className="px-6 py-5">
            <button type="submit" className="btn-ghost">
              Log out
            </button>
          </form>
        </div>
      )}
    </main>
  );
}
