import { Review } from "@/components/extras/Review";

export const metadata = { title: "Review — Psychometry" };

export default function ReviewPage() {
  return (
    <main className="mx-auto max-w-5xl px-6">
      <header className="rise-in pb-10 pt-14">
        <div className="eyebrow">Spaced review</div>
        <h1 className="display mt-3 text-[52px]">Review</h1>
        <p className="mt-3 max-w-2xl text-[16px] text-ink-soft">
          A few minutes a day. Every question you got wrong — in lessons, practice or simulations — comes back here, and
          so do the words and rules you choose. Each time you get it right it returns later: after 1, 3, 7, 16 and 35
          days, until it’s yours.
        </p>
      </header>
      <Review />
    </main>
  );
}
