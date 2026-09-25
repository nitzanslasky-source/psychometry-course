import { LoginForm } from "./LoginForm";

export const metadata = { title: "Log in — Psychometry" };

export default async function LoginPage({ searchParams }: { searchParams: Promise<{ next?: string }> }) {
  const { next } = await searchParams;
  const safeNext = next && next.startsWith("/") && !next.startsWith("//") ? next : "/";
  return (
    <main className="mx-auto max-w-md px-6">
      <header className="rise-in pb-8 pt-16 text-center">
        <h1 className="display text-[48px]">Welcome</h1>
        <p className="mt-2 text-ink-soft">Log in or create your account — no password needed.</p>
      </header>
      <LoginForm next={safeNext} />
      <p className="mt-6 text-center text-xs text-muted">Your progress, mistakes and review are saved to your account on every device.</p>
    </main>
  );
}
