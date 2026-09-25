"use client";

import { useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { SearchDoc } from "@/lib/searchIndex";

const KIND: Record<SearchDoc["k"], string> = {
  topic: "Topics",
  lesson: "Lessons",
  card: "Rules to know",
  word: "Dictionary",
  question: "Questions",
  exam: "Exam simulations",
};
const ORDER: SearchDoc["k"][] = ["topic", "lesson", "card", "word", "exam", "question"];
const LIMIT: Record<SearchDoc["k"], number> = { topic: 5, lesson: 6, card: 4, word: 5, exam: 4, question: 6 };

let indexPromise: Promise<SearchDoc[]> | null = null;
const loadIndex = () => (indexPromise ??= fetch("/api/search-index").then((r) => r.json()));

function score(d: SearchDoc, q: string, words: string[]) {
  const t = d.t.toLowerCase();
  if (t === q) return 100;
  if (t.startsWith(q)) return 80;
  if (words.every((w) => t.includes(w))) return 60 - Math.min(20, t.length / 10);
  const all = `${t} ${d.s.toLowerCase()} ${(d.x || "").toLowerCase()}`;
  if (words.every((w) => all.includes(w))) return 30;
  return 0;
}

/** Search button for the header + the ⌘K search panel. */
export function Search() {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const [docs, setDocs] = useState<SearchDoc[] | null>(null);
  const [sel, setSel] = useState(0);
  const input = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const show = useCallback(() => {
    setOpen(true);
    void loadIndex().then(setDocs);
  }, []);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        show();
      }
      if (e.key === "/" && !open && !/INPUT|TEXTAREA/.test((e.target as HTMLElement)?.tagName)) {
        e.preventDefault();
        show();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, show]);
  useEffect(() => {
    if (open) setTimeout(() => input.current?.focus(), 10);
    else setQ("");
  }, [open]);

  const groups = useMemo(() => {
    const query = q.trim().toLowerCase();
    if (!docs || query.length < 2) return [];
    const words = query.split(/\s+/);
    const scored = docs.map((d) => ({ d, s: score(d, query, words) })).filter((x) => x.s > 0);
    return ORDER.map((k) => ({
      k,
      items: scored
        .filter((x) => x.d.k === k)
        .sort((a, b) => b.s - a.s)
        .slice(0, LIMIT[k])
        .map((x) => x.d),
    })).filter((g) => g.items.length);
  }, [docs, q]);
  const flat = groups.flatMap((g) => g.items);
  useEffect(() => setSel(0), [q]);

  const go = (d: SearchDoc) => {
    setOpen(false);
    router.push(d.h);
  };

  return (
    <>
      <button
        type="button"
        onClick={show}
        className="pressable flex items-center gap-2 rounded-full border border-line bg-white px-3 py-1.5 text-sm text-muted hover:border-faint hover:text-ink"
        aria-label="Search the course"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" aria-hidden>
          <circle cx="11" cy="11" r="7" />
          <path d="m20 20-3.5-3.5" />
        </svg>
        <span className="hidden sm:inline">Search</span>
        <kbd className="hidden rounded border border-line px-1 text-[10px] text-faint lg:inline">⌘K</kbd>
      </button>

      {open && (
        <div className="fixed inset-0 z-[60]" role="dialog" aria-modal="true" aria-label="Search">
          <button type="button" aria-label="Close search" className="fade-in absolute inset-0 bg-ink/30" onClick={() => setOpen(false)} />
          <div className="rise-in relative mx-auto mt-[10vh] w-[min(640px,92vw)] overflow-hidden rounded-2xl bg-paper shadow-lift">
            <div className="flex items-center gap-3 border-b border-line px-5">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6e7481" strokeWidth="2" aria-hidden>
                <circle cx="11" cy="11" r="7" />
                <path d="m20 20-3.5-3.5" />
              </svg>
              <input
                ref={input}
                value={q}
                onChange={(e) => setQ(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Escape") setOpen(false);
                  if (e.key === "ArrowDown") {
                    e.preventDefault();
                    setSel((s) => Math.min(flat.length - 1, s + 1));
                  }
                  if (e.key === "ArrowUp") {
                    e.preventDefault();
                    setSel((s) => Math.max(0, s - 1));
                  }
                  if (e.key === "Enter" && flat[sel]) go(flat[sel]);
                }}
                placeholder="Search lessons, rules, words, questions…"
                className="h-14 flex-1 bg-transparent text-[16px] outline-none"
              />
              <kbd className="rounded border border-line px-1.5 text-[11px] text-faint">esc</kbd>
            </div>
            <div className="max-h-[60vh] overflow-y-auto p-2">
              {!docs && <p className="p-4 text-sm text-muted">Loading…</p>}
              {docs && q.trim().length < 2 && (
                <p className="p-4 text-sm text-muted">Try “percentages”, “triangle”, “analogies”, “circle area” or a word like “ambiguous”.</p>
              )}
              {docs && q.trim().length >= 2 && !flat.length && <p className="p-4 text-sm text-muted">Nothing found for “{q}”.</p>}
              {groups.map((g) => (
                <div key={g.k} className="mb-2">
                  <div className="eyebrow px-3 pb-1 pt-3">{KIND[g.k]}</div>
                  {g.items.map((d) => {
                    const idx = flat.indexOf(d);
                    return (
                      <button
                        key={d.k + d.h + d.t}
                        type="button"
                        onMouseEnter={() => setSel(idx)}
                        onClick={() => go(d)}
                        className={["flex w-full flex-col items-start rounded-xl px-3 py-2 text-left", idx === sel ? "bg-ink text-white" : "hover:bg-paper-deep"].join(" ")}
                      >
                        <span className="text-[15px] font-medium">{d.t}</span>
                        <span className={["line-clamp-1 text-xs", idx === sel ? "text-white/65" : "text-muted"].join(" ")}>{d.s}</span>
                      </button>
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
