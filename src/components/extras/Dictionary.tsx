"use client";

import { useDeferredValue, useEffect, useMemo, useState } from "react";
import type { DictEntry } from "@/lib/extras";
import { canSpeak, speak, stopSpeaking } from "@/lib/speech";

const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
const first = (w: string) => (w.replace(/^[^a-z]+/i, "")[0] || "#").toUpperCase();

export function Dictionary({ entries }: { entries: DictEntry[] }) {
  const [q, setQ] = useState("");
  const [examOnly, setExamOnly] = useState(false);
  const [speakOk, setSpeakOk] = useState(false);
  useEffect(() => setSpeakOk(canSpeak()), []);
  const query = useDeferredValue(q.trim().toLowerCase());

  const shown = useMemo(
    () =>
      entries.filter(
        (e) =>
          (!examOnly || e.exam) &&
          (!query || e.w.toLowerCase().includes(query) || (e.he || "").includes(query) || (e.def || "").toLowerCase().includes(query)),
      ),
    [entries, query, examOnly],
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
              placeholder="Search a word, a meaning, or Hebrew…"
              className="w-full rounded-full border border-line bg-white px-5 py-3 text-[15px] outline-none transition-shadow focus:border-ink focus:shadow-[0_0_0_1px_#101826]"
              autoFocus
            />
          </label>
          <button
            type="button"
            onPointerDown={() => setExamOnly(!examOnly)}
            aria-pressed={examOnly}
            className={["pressable rounded-full border px-4 py-2.5 text-sm", examOnly ? "border-ink bg-ink text-white" : "border-line bg-white text-ink-soft"].join(" ")}
          >
            From real exams
          </button>
          <span className="text-sm text-muted tabular-nums">{shown.length} words</span>
        </div>
        {!query && (
          <nav className="mt-3 flex flex-wrap gap-1 text-xs" aria-label="Jump to letter">
            {LETTERS.map((l) => (
              <a
                key={l}
                href={`#letter-${l}`}
                className={["pressable flex h-7 w-7 items-center justify-center rounded-md", groups.has(l) ? "text-ink-soft hover:bg-paper-deep" : "pointer-events-none text-faint/60"].join(" ")}
              >
                {l}
              </a>
            ))}
          </nav>
        )}
      </div>

      {shown.length === 0 && <p className="py-16 text-center text-muted">No words match “{q}”.</p>}

      <div className="mt-6">
        {[...groups.entries()].map(([letter, list]) => (
          <section key={letter} id={`letter-${letter}`} className="scroll-mt-44">
            <h2 className="display border-b border-line pb-2 pt-8 text-[36px] text-gold">{letter}</h2>
            <ul className="divide-y divide-line">
              {list.map((e) => (
                <li key={e.w} className="grid grid-cols-[1fr_auto] items-start gap-4 py-3.5 sm:grid-cols-[minmax(0,14rem)_1fr_auto]">
                  <div className="font-medium text-ink">
                    {e.w}
                    {e.exam && <span className="ml-2 align-middle text-[10px] font-semibold uppercase tracking-[0.1em] text-gold">exam</span>}
                  </div>
                  <div className="col-span-2 text-[15px] text-ink-soft sm:col-span-1">
                    {e.he && (
                      <span dir="rtl" lang="he" className="text-[16px]">
                        {e.he}
                      </span>
                    )}
                    {e.he && e.def && <span className="mx-2 text-faint">·</span>}
                    {e.def && <span className="text-muted">{e.def}</span>}
                  </div>
                  {speakOk && (
                    <button
                      type="button"
                      aria-label={`Hear “${e.w}”`}
                      onPointerDown={() => {
                        stopSpeaking();
                        void speak(e.w, "en", 0.9);
                      }}
                      className="pressable row-start-1 flex h-8 w-8 items-center justify-center rounded-full border border-line text-xs text-muted hover:border-faint hover:text-ink sm:row-start-auto"
                    >
                      ♪
                    </button>
                  )}
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </div>
  );
}
