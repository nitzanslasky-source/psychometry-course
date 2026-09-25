import { NextResponse } from "next/server";
import { grantAccess } from "@/lib/grant";

/**
 * Payment provider → "this person paid" → access granted to their email.
 *
 * NOT CONNECTED YET: the provider hasn't been chosen. When it is (Grow / Cardcom / Stripe …):
 *  1. set its webhook / "success notification" URL to  https://<your-domain>/api/payments/webhook?key=<PAYMENT_WEBHOOK_SECRET>
 *  2. adapt `readPayment` below to that provider's payload (and verify its signature if it signs requests).
 * Until then it accepts a simple JSON body { "email": "...", "reference": "..." } with the secret key,
 * which is also handy for testing.
 */
async function readPayment(req: Request): Promise<{ email: string; reference?: string } | null> {
  const type = req.headers.get("content-type") || "";
  const body: Record<string, unknown> = type.includes("json")
    ? await req.json().catch(() => ({}))
    : Object.fromEntries((await req.formData().catch(() => new FormData())).entries());
  const email = String(body.email ?? body.customer_email ?? body.payerEmail ?? "");
  const reference = body.reference ?? body.transactionId ?? body.id;
  return email.includes("@") ? { email, reference: reference ? String(reference) : undefined } : null;
}

export async function POST(req: Request) {
  const secret = process.env.PAYMENT_WEBHOOK_SECRET;
  const key = new URL(req.url).searchParams.get("key") || req.headers.get("x-webhook-key");
  if (!secret || key !== secret) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  const p = await readPayment(req);
  if (!p) return NextResponse.json({ error: "no email in payment" }, { status: 400 });
  const r = await grantAccess(p.email, process.env.PAYMENT_PROVIDER || "webhook", p.reference);
  return NextResponse.json({ ok: true, ...r });
}
