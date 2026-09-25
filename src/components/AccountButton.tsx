import Link from "next/link";
import { currentStudent } from "@/lib/supabase/server";

/** Header: "Log in", or the student's initial linking to their account. Hidden when accounts are off. */
export async function AccountButton() {
  const me = await currentStudent();
  if (!me.enabled) return null;
  if (!me.user)
    return (
      <Link href="/login" className="pressable shrink-0 rounded-full bg-ink px-3.5 py-1.5 text-sm text-white">
        Log in
      </Link>
    );
  return (
    <Link href="/account" title={me.user.email} className="pressable flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gold text-sm font-semibold uppercase text-white">
      {me.user.email.slice(0, 1)}
    </Link>
  );
}
