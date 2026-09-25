import { getAllCards } from "@/lib/extras";
import { RulesBook } from "@/components/extras/RulesBook";

export const metadata = { title: "Rules to know — Psychometry" };

export default function RulesPage() {
  const items = getAllCards();
  return (
    <main className="mx-auto max-w-6xl px-6">
      <header className="rise-in pb-10 pt-14">
        <div className="eyebrow">Memory cards</div>
        <h1 className="display mt-3 text-[52px]">Rules to know by heart</h1>
        <p className="mt-3 max-w-2xl text-[16px] text-ink-soft">
          Every rule, formula and table from the course in one place — {items.length} cards, each linked back to the lesson
          it comes from. Perfect for a quick review before practice or the exam.
        </p>
      </header>
      <RulesBook items={items} />
    </main>
  );
}
