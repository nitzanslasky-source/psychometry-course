"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useTypeset } from "@/components/MathJaxProvider";
import { RichText } from "@/components/sim/RichText";
import { MemoryCard } from "@/components/learn/MemoryCard";
import { loadAttempts } from "@/lib/attemptStore";
import { isMastered, srsAdd, srsAll, srsDue, srsGrade, srsHas, srsRemove, type SrsItem } from "@/lib/srs";
import type { ReviewItem } from "@/lib/reviewData";

async function fetchItems(keys: string[]): Promise<ReviewItem[]> {
  if (!keys.length) return [];
  const r = await fetch("/api/review-items", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ keys }) });
  return (await r.json()) as ReviewItem[];
}

/** Wrong answers in exam simulations join the review automatically. */
function syncSimulationMistakes() {
  const latest = new Map<string, boolean>();
  for (const a of loadAttempts()) if (a.pool === "simulation") latest.set(a.question_id, a.is_correct);
  for (const [qid, ok] of latest) if (!ok && !srsHas(`s:${qid}`)) srsAdd(`s:${qid}`, { now: true });
}

type Tab = "today" | "mistakes";

export function Review() {
  const [tab, setTab] = useState<Tab>("today");
  const [items, setItems] = useState<SrsItem[]>([]);
  const refresh = useCallback(() => setItems(srsAll()), []);
  useEffect(() => {
    syncSimulationMistakes();
    refresh();
    window.addEventListener("srs-change", refresh);
    return () => window.removeEventListener("srs-change", refresh);
  }, [refresh]);

  const due = items.filter((i) => i.due <= Date.now()).length;
  const mistakes = items.filter((i) => i.kind === "q" || i.kind === "s").length;
  const mastered = items.filter(isMastered).length;

  return (
    <div>
      <dl className="grid grid-cols-3 gap-4 sm:max-w-xl">
        <Stat n={due} label="due today" />
        <Stat n={items.length} label="in your review" />
        <Stat n={mastered} label="mastered" />
      </dl>

      <div role="tablist" className="mt-10 flex w-fit gap-1 rounded-full border border-line bg-white p-1">
        {(
          [
            ["today", "Today’s review"],
            ["mistakes", `My mistakes${mistakes ? ` · ${mistakes}` : ""}`],
          ] as [Tab, string][]
        ).map(([id, label]) => (
          <button
            key={id}
            role="tab"
            aria-selected={tab === id}
            onPointerDown={() => setTab(id)}
            onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && setTab(id)}
            className={["pressable rounded-full px-4 py-2 text-sm", tab === id ? "bg-ink text-white" : "text-ink-soft hover:bg-paper-deep"].join(" ")}
          >
            {label}
          </button>
        ))}
      </div>

      <div key={tab} className="fade-in mt-8">{tab === "today" ? <Session /> : <Mistakes items={items} />}</div>
    </div>
  );
}

function Stat({ n, label }: { n: number; label: string }) {
  return (
    <div>
      <dt className="display text-[44px] leading-none">{n}</dt>
      <dd className="mt-1 text-sm text-muted">{label}</dd>
    </div>
  );
}

/* ------------------------------------------------------------------ today's session */

function Session() {
  const [queue, setQueue] = useState<ReviewItem[] | null>(null);
  const [i, setI] = useState(0);
  const [knewN, setKnewN] = useState(0);

  const start = useCallback(async () => {
    syncSimulationMistakes(); // child effects run before the parent's — sync here too
    const keys = srsDue().map((x) => x.key).slice(0, 40);
    setQueue(await fetchItems(keys));
    setI(0);
    setKnewN(0);
  }, []);
  useEffect(() => {
    void start();
  }, [start]);

  const addWords = async (n: number) => {
    const all = (await (await fetch("/api/review-items")).json()) as string[];
    const fresh = all.filter((k) => !srsHas(k)).slice(0, n);
    fresh.forEach((k) => srsAdd(k, { now: true }));
    await start();
  };

  if (!queue) return <p className="text-muted">Loading…</p>;

  if (i >= queue.length)
    return (
      <div className="card p-8 text-center">
        {queue.length > 0 ? (
          <>
            <div className="display text-[40px]">Done for today.</div>
            <p className="mt-2 text-muted">
              You knew {knewN} of {queue.length}. The ones you missed come back tomorrow; the rest come back later and later.
            </p>
          </>
        ) : (
          <>
            <div className="display text-[40px]">Nothing to review right now.</div>
            <p className="mx-auto mt-2 max-w-md text-muted">
              Questions you get wrong in the course or in simulations appear here automatically, and come back at growing
              intervals until they stick. You can also add words and rules cards.
            </p>
          </>
        )}
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <button type="button" className="btn" onClick={() => void addWords(10)}>
            Add 10 new vocabulary words
          </button>
          <Link href="/rules" className="btn-ghost">
            Add rules cards
          </Link>
        </div>
      </div>
    );

  const item = queue[i];
  const done = (knew: boolean) => {
    srsGrade(item.key, knew);
    if (knew) setKnewN((n) => n + 1);
    setI((x) => x + 1);
  };
  return (
    <div>
      <div className="mb-4 flex items-center justify-between text-sm text-muted">
        <span>{item.where}</span>
        <span className="tabular-nums">
          {i + 1} / {queue.length}
        </span>
      </div>
      <div className="mb-6 h-1 overflow-hidden rounded-full bg-line">
        <div className="progress-fill h-full rounded-full bg-ink" style={{ width: `${(i / queue.length) * 100}%` }} />
      </div>
      <div key={item.key} className="step-in-next">
        <ReviewCard item={item} onDone={done} />
      </div>
    </div>
  );
}

/** One review item: a question to answer again, or a word / rules card to recall. */
export function ReviewCard({ item, onDone }: { item: ReviewItem; onDone: (knew: boolean) => void }) {
  if (item.kind === "q" || item.kind === "s") return <QuestionAgain item={item} onDone={onDone} />;
  return <Recall item={item} onDone={onDone} />;
}

function QuestionAgain({ item, onDone }: { item: Extract<ReviewItem, { kind: "q" | "s" }>; onDone: (knew: boolean) => void }) {
  const [picked, setPicked] = useState<number | null>(null);
  const [checked, setChecked] = useState(false);
  const ref = useTypeset<HTMLDivElement>([item.key, checked]);
  const right = picked === item.correct;
  return (
    <div ref={ref} className="max-w-read">
      {item.kind === "q" && item.passage && (
        <details className="card mb-6 px-6 py-4">
          <summary className="cursor-pointer text-sm text-muted">Show the passage</summary>
          <div className="mt-3 space-y-3 font-serif text-[18px] leading-relaxed">
            {item.passage.paragraphs.map((p, k) => (
              <p key={k}>
                <span className="mr-2 font-sans text-xs text-faint">{k + 1}</span>
                {p}
              </p>
            ))}
          </div>
        </details>
      )}
      {item.kind === "q" && item.instructions && <p className="mb-4 border-l-2 border-line pl-4 text-sm italic text-muted">{item.instructions}</p>}
      <div className="whitespace-pre-line text-[18px] leading-[1.65]">
        <RichText text={item.stem} />
      </div>
      {item.kind === "q" && item.figure && (
        <div className="card mt-6 p-5">
          <div className="mx-auto max-w-md [&>svg]:h-auto [&>svg]:w-full" dangerouslySetInnerHTML={{ __html: item.figure }} />
        </div>
      )}
      {item.kind === "s" &&
        item.figures.map((f) => (
          // eslint-disable-next-line @next/next/no-img-element
          <img key={f} src={f} alt="" className="card mt-6 max-h-80 w-auto p-3" />
        ))}
      <ol className="mt-6 space-y-2.5">
        {item.choices.map((c, k) => {
          const isC = checked && k === item.correct;
          const isW = checked && k === picked && !right;
          return (
            <li
              key={k}
              role="radio"
              aria-checked={picked === k}
              tabIndex={checked ? -1 : 0}
              onPointerDown={() => !checked && setPicked(k)}
              className={[
                "flex items-start gap-4 rounded-2xl border bg-white px-5 py-3.5",
                checked ? "" : "pressable cursor-pointer hover:border-faint",
                isC ? "anim-land border-ok bg-[#f1f8f4]" : isW ? "anim-nope border-bad bg-[#fbf1f0]" : !checked && picked === k ? "border-ink shadow-[0_0_0_1px_#101826]" : "border-line",
              ].join(" ")}
            >
              <span className="mt-px flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-line text-xs text-muted">{k + 1}</span>
              {item.kind === "s" && item.optionFigures?.[k] ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={item.optionFigures[k]} alt={`Choice ${k + 1}`} className="max-h-32" />
              ) : (
                <span>
                  <RichText text={c} />
                </span>
              )}
            </li>
          );
        })}
      </ol>
      {!checked ? (
        <button type="button" className="btn mt-6" disabled={picked === null} onClick={() => setChecked(true)}>
          Check answer
        </button>
      ) : (
        <div className="rise-in card mt-6 p-6">
          <div className={["display text-[26px]", right ? "text-ok" : "text-bad"].join(" ")}>
            {right ? "Correct — it’s sticking." : `The answer is choice ${item.correct + 1}.`}
          </div>
          <div className="mt-2 space-y-1.5 text-[15px] text-ink-soft">
            {item.explanation.map((e, k) => (
              <p key={k}>
                <RichText text={e} />
              </p>
            ))}
          </div>
          <div className="mt-5 flex flex-wrap items-center gap-3">
            <button type="button" className="btn" onClick={() => onDone(right)}>
              Next
            </button>
            {item.kind === "q" && item.solutionHref && (
              <Link href={item.solutionHref} className="btn-ghost">
                Watch the worked solution
              </Link>
            )}
            <Link href={item.href} className="text-sm text-muted underline decoration-line underline-offset-4 hover:text-ink">
              Open in the {item.kind === "q" ? "lesson" : "simulation"}
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

function Recall({ item, onDone }: { item: Extract<ReviewItem, { kind: "w" | "c" }>; onDone: (knew: boolean) => void }) {
  const [shown, setShown] = useState(false);
  return (
    <div className="card p-8">
      <div className="eyebrow">{item.kind === "w" ? "What does it mean?" : "Can you recall this card?"}</div>
      <div className="display mt-4 text-[48px] leading-tight">{item.kind === "w" ? item.w : item.card.title}</div>
      {!shown ? (
        <button type="button" className="btn mt-8" onClick={() => setShown(true)} autoFocus>
          Show {item.kind === "w" ? "the meaning" : "the card"}
        </button>
      ) : (
        <div className="rise-in mt-6">
          {item.kind === "w" ? (
            <div className="max-w-xl">
              <p className="text-[18px]">{item.def}</p>
              <p className="mt-2 italic text-ink-soft">“{item.ex}”</p>
              {item.note && <p className="mt-2 text-sm text-muted">{item.note}</p>}
            </div>
          ) : (
            <MemoryCard step={item.card} accent="#a8812e" heading={<span />} />
          )}
          <div className="mt-8 flex gap-3">
            <button type="button" className="btn-ghost" onClick={() => onDone(false)}>
              Not yet
            </button>
            <button type="button" className="btn" onClick={() => onDone(true)}>
              I knew it
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ my mistakes */

function Mistakes({ items }: { items: SrsItem[] }) {
  const keys = useMemo(() => items.filter((i) => i.kind === "q" || i.kind === "s").sort((a, b) => b.added - a.added).map((i) => i.key), [items]);
  const [data, setData] = useState<ReviewItem[] | null>(null);
  const [open, setOpen] = useState<string | null>(null);
  useEffect(() => {
    void fetchItems(keys).then(setData);
  }, [keys]);
  const ref = useTypeset<HTMLUListElement>([data?.length]);

  if (!data) return <p className="text-muted">Loading…</p>;
  if (!data.length)
    return <p className="card p-8 text-center text-muted">No mistakes saved yet. Wrong answers in lessons, practice and simulations will collect here.</p>;
  const box = new Map(items.map((i) => [i.key, i]));

  return (
    <ul ref={ref} className="card divide-y divide-line">
      {data.map((it) => {
        if (it.kind !== "q" && it.kind !== "s") return null;
        const b = box.get(it.key);
        return (
          <li key={it.key} className="px-6 py-5">
            {open === it.key ? (
              <ReviewCard
                item={it}
                onDone={(knew) => {
                  srsGrade(it.key, knew);
                  setOpen(null);
                }}
              />
            ) : (
              <div className="grid gap-3 sm:grid-cols-[1fr_auto] sm:items-center">
                <div className="min-w-0">
                  <div className="text-xs text-muted">
                    {it.where}
                    {b && <span className="ml-2 text-faint">· next review {new Date(b.due).toLocaleDateString(undefined, { day: "numeric", month: "short" })}</span>}
                  </div>
                  <div className="mt-1 line-clamp-2 text-[15px]">
                    <RichText text={it.stem} />
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  <button type="button" className="btn px-4 py-2" onClick={() => setOpen(it.key)}>
                    Try again
                  </button>
                  {it.kind === "q" && it.solutionHref && (
                    <Link href={it.solutionHref} className="btn-ghost px-4 py-2">
                      Solution
                    </Link>
                  )}
                  <button type="button" className="px-2 text-sm text-faint hover:text-ink" onClick={() => srsRemove(it.key)} aria-label="Remove from mistakes">
                    ✕
                  </button>
                </div>
              </div>
            )}
          </li>
        );
      })}
    </ul>
  );
}
