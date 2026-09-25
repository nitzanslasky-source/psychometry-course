"use client";

import { useDeferredValue, useEffect, useMemo, useState } from "react";
import type { DictEntry, DictLabel } from "@/lib/extras";
import { canSpeak, speak, stopSpeaking } from "@/lib/speech";
import { AddToReview } from "./AddToReview";

const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
const first = (w: string) => (w.replace(/^[^a-z]+/i, "")[0] || "#").toUpperCase();

export const LABEL_TEXT: Record<DictLabel, string> = {
  "EXAM ANALOGY": "Exam analogy",
  "EXAM VOCABULARY": "Exam word",
  "ADDITIONAL WORD": "Worth knowing",
  "ANALOGY PRACTICE": "Analogy practice",
  READING: "Reading",
};
const FILTERS: { id: string; label: string; test: (e: DictEntry) => boolean }[] = [
  { id: "all", label: "All words", test: () => true },
  { id: "analogy", label: "Analogies", test: (e) => e.label === "EXAM ANALOGY" || e.label === "ANALOGY PRACTICE" },
  { id: "exam", label: "From real exams", test: (e) => e.label === "EXAM ANALOGY" || e.label === "EXAM VOCABULARY" },
  { id: "core", label: "Core list", test: (e) => !!e.core },
];

export function Dictionary({ entries, initialQuery = "" }: { entries: DictEntry[]; initialQuery?: string }) {
  const [q, setQ] = useState(initialQuery);
  const [filter, setFilter] = useState("all");
  const [speakOk, setSpeakOk] = useState(false);
  useEffect(() => setSpeakOk(canSpeak()), []);
  const query = useDeferredValue(q.trim().toLowerCase());
  const test = FILTERS.find((f) => f.id === filter)!.test;

  const shown = useMemo(
    () =>
      entries.filter(
        (e) => test(e) && (!query || e.w.toLowerCase().includes(query) || e.def.toLowerCase().includes(query)),
      ),
    [entries, query, test],
  );
  const groups = useMemo(() => {
    const m = new Map<string, DictEntry[]>();
    for (const e of shown) {
      const k = first(e.w);
      if (!m.has(k)) m.set(k, []);
      m.get(k)!.push(e);
    }
    return m;
  }, [shown]);

  return (
    <div>
      <div className="material edge-bottom sticky top-16 z-20 -mx-6 px-6 py-4">
        <div className="flex flex-wrap items-center gap-3">
          <label className="relative min-w-[240px] flex-1">
            <span className="sr-only">Search the dictionary</span>
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search a word or a meaning…"
              className="w-full rounded-full border border-line bg-white px-5 py-3 text-[15px] outline-none transition-shadow focus:border-ink focus:shadow-[0_0_0_1px_#101826]"
            />
          </label>
          <span className="text-sm tabular-nums text-muted">{shown.length} words</span>
        </div>
        <div className="mt-3 flex flex-wrap items-center gap-1.5">
          {FILTERS.map((f) => (
            <button
              key={f.id}
              type="button"
              onPointerDown={() => setFilter(f.id)}
              aria-pressed={filter === f.id}
              className={["pressable rounded-full px-3.5 py-1.5 text-[13px]", filter === f.id ? "bg-ink text-white" : "border border-line bg-white text-ink-soft"].join(" ")}
            >
              {f.label}
            </button>
          ))}
          {!query && (
            <nav className="ml-auto hidden flex-wrap gap-0.5 text-xs md:flex" aria-label="Jump to letter">
              {LETTERS.map((l) => (
                <a
                  key={l}
                  href={`#letter-${l}`}
                  className={["pressable flex h-6 w-6 items-center justify-center rounded", groups.has(l) ? "text-ink-soft hover:bg-paper-deep" : "pointer-events-none text-faint/50"].join(" ")}
                >
                  {l}
                </a>
              ))}
            </nav>
          )}
        </div>
      </div>

      {shown.length === 0 && <p className="py-16 text-center text-muted">No words match “{q}”.</p>}

      <div className="mt-4">
        {[...groups.entries()].map(([letter, list]) => (
          <section key={letter} id={`letter-${letter}`} className="scroll-mt-44">
            <h2 className="display border-b border-line pb-2 pt-10 text-[40px] text-gold">{letter}</h2>
            <ul className="divide-y divide-line">
              {list.map((e) => (
                <li key={e.w} className="grid gap-x-8 gap-y-2 py-6 sm:grid-cols-[13rem_1fr]">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="display text-[26px] leading-tight">{e.w}</span>
                      {speakOk && (
                        <button
                          type="button"
                          aria-label={`Hear “${e.w}”`}
                          onPointerDown={() => {
                            stopSpeaking();
                            void speak(e.w, "en", 0.9);
                          }}
                          className="pressable flex h-7 w-7 shrink-0 items-center justify-center rounded-full border border-line text-[11px] text-muted hover:border-faint hover:text-ink"
                        >
                          ♪
                        </button>
                      )}
                    </div>
                    <div className="mt-1 flex items-center gap-2">
                      <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-gold">{LABEL_TEXT[e.label]}</span>
                    </div>
                    <div className="mt-2">
                      <AddToReview srsKey={`w:${e.w}`} compact />
                    </div>
                  </div>
                  <div className="max-w-2xl">
                    <p className="text-[16px] leading-relaxed text-ink">{e.def}</p>
                    <p className="mt-1.5 text-[15px] italic leading-relaxed text-ink-soft">“{e.ex}”</p>
                    {e.note && <p className="mt-1.5 text-[13px] text-muted">{e.note}</p>}
                  </div>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </div>
  );
}
