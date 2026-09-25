"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { supabaseBrowser } from "@/lib/supabase/client";

/** Log in with a one-time email code, or with Google. New emails get an account automatically. */
export function LoginForm({ next }: { next: string }) {
  const sb = supabaseBrowser();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [stage, setStage] = useState<"email" | "code">("email");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  if (!sb)
    return (
      <p className="card p-6 text-ink-soft">
        Accounts aren’t switched on yet on this copy of the site — everything is open for now. (See SETUP.md.)
      </p>
    );

  const sendCode = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setErr(null);
    const { error } = await sb.auth.signInWithOtp({ email: email.trim(), options: { shouldCreateUser: true } });
    setBusy(false);
    if (error) setErr(error.message);
    else setStage("code");
  };
  const verify = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setErr(null);
    const { error } = await sb.auth.verifyOtp({ email: email.trim(), token: code.trim(), type: "email" });
    setBusy(false);
    if (error) setErr("That code didn’t work — check it, or send a new one.");
    else {
      router.replace(next);
      router.refresh();
    }
  };
  const google = async () => {
    await sb.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: `${location.origin}/auth/callback?next=${encodeURIComponent(next)}` },
    });
  };

  return (
    <div className="card p-8">
      <button type="button" onClick={google} className="btn-ghost w-full py-3">
        <svg width="18" height="18" viewBox="0 0 48 48" aria-hidden>
          <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z" />
          <path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z" />
          <path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-7.9l-6.5 5C9.5 39.6 16.2 44 24 44z" />
          <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z" />
        </svg>
        Continue with Google
      </button>

      <div className="my-6 flex items-center gap-3 text-xs text-faint">
        <span className="h-px flex-1 bg-line" /> or with your email <span className="h-px flex-1 bg-line" />
      </div>

      {stage === "email" ? (
        <form onSubmit={sendCode} className="space-y-3">
          <label className="block">
            <span className="sr-only">Email</span>
            <input
              type="email"
              required
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full rounded-xl border border-line bg-white px-4 py-3 text-[15px] outline-none focus:border-ink focus:shadow-[0_0_0_1px_#101826]"
            />
          </label>
          <button type="submit" className="btn w-full py-3" disabled={busy || !email}>
            {busy ? "Sending…" : "Email me a login code"}
          </button>
        </form>
      ) : (
        <form onSubmit={verify} className="rise-in space-y-3">
          <p className="text-sm text-ink-soft">
            We sent a 6-digit code to <b className="font-medium text-ink">{email}</b>. It’s valid for an hour.
          </p>
          <input
            inputMode="numeric"
            autoComplete="one-time-code"
            required
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 8))}
            placeholder="123456"
            className="w-full rounded-xl border border-line bg-white px-4 py-3 text-center text-[24px] tracking-[0.4em] outline-none focus:border-ink"
            autoFocus
          />
          <button type="submit" className="btn w-full py-3" disabled={busy || code.length < 6}>
            {busy ? "Checking…" : "Log in"}
          </button>
          <button type="button" className="w-full text-sm text-muted underline decoration-line underline-offset-4" onClick={() => setStage("email")}>
            Use a different email
          </button>
        </form>
      )}
      {err && <p className="mt-4 text-sm text-bad">{err}</p>}
    </div>
  );
}
