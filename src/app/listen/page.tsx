import { getDictionary } from "@/lib/extras";
import { ListenPlayer } from "@/components/extras/ListenPlayer";

export const metadata = { title: "Listen — Psychometry" };

export default function ListenPage() {
  const entries = getDictionary();
  return (
    <main className="mx-auto max-w-5xl px-6">
      <header className="rise-in pb-10 pt-14">
        <div className="eyebrow">Vocabulary on the go</div>
        <h1 className="display mt-3 text-[52px]">Listen</h1>
        <p className="mt-3 max-w-2xl text-[16px] text-ink-soft">
          Short vocabulary episodes for the bus, the gym or a walk: each word, its Hebrew meaning, then the word again.
          Turn on <b className="font-medium text-ink">Quiz mode</b> to get a pause to say the meaning yourself first.
        </p>
      </header>
      <ListenPlayer entries={entries} />
    </main>
  );
}
