import { getDictionary } from "@/lib/extras";
import { Dictionary } from "@/components/extras/Dictionary";

export const metadata = { title: "Dictionary — Psychometry" };

export default function DictionaryPage() {
  const entries = getDictionary();
  return (
    <main className="mx-auto max-w-5xl px-6">
      <header className="rise-in pb-6 pt-14">
        <div className="eyebrow">Vocabulary</div>
        <h1 className="display mt-3 text-[52px]">Dictionary</h1>
        <p className="mt-3 max-w-2xl text-[16px] text-ink-soft">
          {entries.length.toLocaleString()} words and expressions worth knowing for the verbal sections — each with a
          plain-English meaning and an example. Words from real exam analogies are marked. Tap ♪ to hear a word, or
          listen to them all in <a href="/listen" className="link">Listen</a>.
        </p>
      </header>
      <Dictionary entries={entries} />
    </main>
  );
}
