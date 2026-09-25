import { MentalMath } from "@/components/extras/MentalMath";

export const metadata = { title: "Mental math — Psychometry" };

export default function MentalMathPage() {
  return (
    <main className="mx-auto max-w-5xl px-6">
      <header className="rise-in pb-10 pt-14">
        <div className="eyebrow">Practice games</div>
        <h1 className="display mt-3 text-[52px]">Mental math</h1>
        <p className="mt-3 max-w-2xl text-[16px] text-ink-soft">
          Sixty-second rounds to make the basics automatic — times tables, division, squares, roots and fractions. A
          few rounds a day saves minutes on every exam section.
        </p>
      </header>
      <MentalMath />
    </main>
  );
}
