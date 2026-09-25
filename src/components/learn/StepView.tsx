"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useTypeset } from "@/components/MathJaxProvider";
import { loadProgress, markDone, recordAnswer, setLastStep, stepKey } from "@/lib/courseProgressStore";
import type {
  CourseCardStep,
  CourseQuestionStep,
  CourseStep,
  CourseVideoStep,
  VideoSource,
} from "@/lib/fullCourseTypes";

interface Nav {
  topic: number;
  index: number;
  total: number;
  prevHref?: string;
  nextHref?: string;
  nextLabel?: string;
}

export function StepView({
  step,
  nav,
  video,
  passage,
  label,
}: {
  step: CourseStep;
  nav: Nav;
  video?: VideoSource | null;
  passage?: { title: string; paragraphs: string[] } | null;
  /** e.g. "Question 3" / "Practice · Question 12". */
  label: string;
}) {
  useEffect(() => setLastStep(nav.topic, nav.index), [nav.topic, nav.index]);
  const [done, setDone] = useState(false);
  useEffect(() => setDone(!!loadProgress().done[stepKey(nav.topic, step.id)]), [nav.topic, step.id]);
  const complete = () => {
    markDone(nav.topic, step.id);
    setDone(true);
  };
  // Enter along the direction of travel (Next → from the right, Previous → from the left).
  const [dir, setDir] = useState<"next" | "prev">("next");
  useEffect(() => {
    try {
      setDir(sessionStorage.getItem("stepDir") === "prev" ? "prev" : "next");
    } catch {}
  }, [step.id]);
  const go = (d: "next" | "prev") => {
    try {
      sessionStorage.setItem("stepDir", d);
    } catch {}
  };

  return (
    <div>
      <div className="text-xs font-semibold uppercase tracking-wide text-brand-600 dark:text-brand-400">
        {label} · step {nav.index + 1} of {nav.total}
      </div>
      <div key={step.id} className={dir === "prev" ? "step-in-prev mt-3" : "step-in-next mt-3"}>
        {step.kind === "video" && <VideoStep step={step} video={video} onEnded={complete} />}
        {step.kind === "question" && <QuestionStep key={step.id} step={step} topic={nav.topic} passage={passage} />}
        {step.kind === "card" && <CardStep step={step} />}
      </div>

      <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
        {nav.prevHref ? (
          <Link href={nav.prevHref} className="btn-secondary" onPointerDown={() => go("prev")}>
            ← Previous
          </Link>
        ) : (
          <span />
        )}
        <div className="flex items-center gap-3">
          {step.kind !== "question" && !done && (
            <button type="button" className="btn-secondary" onClick={complete}>
              Mark as done
            </button>
          )}
          {nav.nextHref ? (
            <Link
              href={nav.nextHref}
              className="btn-primary"
              onPointerDown={() => go("next")}
              onClick={() => step.kind !== "question" && complete()}
            >
              {nav.nextLabel || "Next →"}
            </Link>
          ) : (
            <Link href={`/topic/${nav.topic}`} className="btn-primary" onClick={complete}>
              Finish topic ✓
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}

/* ---------------------------------------------------------------- video */

function VideoStep({
  step,
  video,
  onEnded,
}: {
  step: CourseVideoStep;
  video?: VideoSource | null;
  onEnded: () => void;
}) {
  return (
    <div>
      <h1 className="text-2xl font-bold">{step.title}</h1>
      <div className="mt-4 overflow-hidden rounded-xl border border-hair bg-black shadow-card dark:border-white/10">
        <div className="relative aspect-video">
          {!video && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 bg-gradient-to-br from-neutral-800 to-neutral-950 text-center text-white">
              <div className="text-4xl opacity-70">▶</div>
              <div className="text-lg font-semibold">Video coming soon</div>
              <div className="max-w-sm text-sm text-white/70">
                This lesson is being recorded. You can continue with the rest of the topic in the meantime.
              </div>
            </div>
          )}
          {video?.provider === "bunny" && (
            <iframe
              className="absolute inset-0 h-full w-full"
              src={`https://iframe.mediadelivery.net/embed/${video.libraryId}/${video.videoGuid}?autoplay=false&preload=true&responsive=true`}
              allow="accelerometer; gyroscope; encrypted-media; picture-in-picture; fullscreen"
              allowFullScreen
              title={step.title}
            />
          )}
          {video?.provider === "url" && (
            // eslint-disable-next-line jsx-a11y/media-has-caption
            <video className="absolute inset-0 h-full w-full" src={video.url} controls onEnded={onEnded} />
          )}
        </div>
      </div>
      {step.minutes ? (
        <p className="mt-2 text-xs text-muted dark:text-neutral-400">About {Math.max(1, Math.round(step.minutes))} min</p>
      ) : null}
    </div>
  );
}

/* ---------------------------------------------------------------- question */

function QuestionStep({
  step,
  topic,
  passage,
}: {
  step: CourseQuestionStep;
  topic: number;
  passage?: { title: string; paragraphs: string[] } | null;
}) {
  const [picked, setPicked] = useState<number | null>(null);
  const [checked, setChecked] = useState(false);
  useEffect(() => {
    const a = loadProgress().answers[stepKey(topic, step.id)];
    if (a !== undefined) {
      setPicked(a);
      setChecked(true);
    }
  }, [topic, step.id]);
  const ref = useTypeset<HTMLDivElement>([step.id, checked]);

  const check = () => {
    if (picked === null) return;
    recordAnswer(topic, step.id, picked);
    setChecked(true);
  };
  const retry = () => {
    setPicked(null);
    setChecked(false);
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (checked || (e.target as HTMLElement)?.tagName === "INPUT") return;
      const n = Number(e.key);
      if (n >= 1 && n <= step.choices.length) setPicked(n - 1);
      if (e.key === "Enter" && picked !== null) check();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  return (
    <div ref={ref}>
      {passage && <PassagePanel passage={passage} />}
      <div className="surface-card p-6">
        {step.instructions && (
          <p className="mb-3 text-sm italic text-muted dark:text-neutral-400">{step.instructions}</p>
        )}
        <div className="whitespace-pre-line text-[17px] leading-relaxed">{step.stem}</div>
        {step.figure && (
          <figure className="mt-4">
            <div
              className="mx-auto max-w-xl [&>svg]:h-auto [&>svg]:w-full"
              dangerouslySetInnerHTML={{ __html: step.figure }}
            />
            <figcaption className="mt-1 text-right text-xs text-muted">Figure not necessarily drawn to scale.</figcaption>
          </figure>
        )}
        <ol className="mt-5 list-none space-y-2 p-0">
          {step.choices.map((c, i) => {
            const isCorrect = checked && i === step.correct;
            const isWrong = checked && i === picked && picked !== step.correct;
            const isPicked = !checked && i === picked;
            return (
              <li
                key={i}
                role="radio"
                aria-checked={picked === i}
                tabIndex={checked ? -1 : 0}
                onPointerDown={() => !checked && setPicked(i)}
                onKeyDown={(e) => {
                  if (!checked && (e.key === "Enter" || e.key === " ")) {
                    e.preventDefault();
                    setPicked(i);
                  }
                }}
                className={[
                  "flex items-start gap-3 rounded-xl border-2 px-3 py-2.5 transition-colors duration-150",
                  checked ? "cursor-default" : "pressable cursor-pointer select-none",
                  isCorrect ? "anim-land" : "",
                  isWrong ? "anim-nope" : "",
                  isCorrect ? "border-ok bg-emerald-50 dark:bg-emerald-500/10" : "",
                  isWrong ? "border-bad bg-red-50 dark:bg-red-500/10" : "",
                  isPicked ? "border-blue-600 bg-blue-50 ring-1 ring-blue-600 dark:border-blue-400 dark:bg-blue-500/10" : "",
                  !isCorrect && !isWrong && !isPicked
                    ? `border-hair bg-white dark:border-white/10 dark:bg-white/5 ${checked ? "" : "hover:border-neutral-400"}`
                    : "",
                ].join(" ")}
              >
                <span
                  className={[
                    "mt-0.5 flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full border-2 text-[10px] font-bold",
                    isCorrect ? "border-ok bg-ok text-white" : "",
                    isWrong ? "border-bad bg-bad text-white" : "",
                    isPicked ? "border-blue-600 bg-blue-600 text-white" : "",
                    !isCorrect && !isWrong && !isPicked ? "border-neutral-400 text-muted" : "",
                  ].join(" ")}
                  aria-hidden
                >
                  {i + 1}
                </span>
                <span>{c}</span>
              </li>
            );
          })}
        </ol>

        {!checked ? (
          <div className="mt-4 flex items-center gap-3">
            <button type="button" className="btn-primary" disabled={picked === null} onClick={check}>
              Check answer
            </button>
            <span className="text-xs text-muted">Keys 1–4 pick · Enter checks</span>
          </div>
        ) : (
          <div className="rise-in mt-5 border-t border-hair pt-4 dark:border-white/10">
            <div className={picked === step.correct ? "font-semibold text-ok" : "font-semibold text-bad"}>
              {picked === step.correct ? "Correct!" : `Not quite — the answer is choice ${step.correct + 1}.`}
            </div>
            {step.explanation.length > 0 && (
              <div className="mt-2 space-y-1 text-sm">
                {step.explanation.map((e, i) => (
                  <p key={i}>{e}</p>
                ))}
              </div>
            )}
            <button type="button" className="link-subtle mt-3 text-sm" onClick={retry}>
              Try again
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

function PassagePanel({ passage }: { passage: { title: string; paragraphs: string[] } }) {
  const [open, setOpen] = useState(true);
  return (
    <div className="surface-card mb-4 p-5">
      <button type="button" className="flex w-full items-center justify-between text-left" onClick={() => setOpen(!open)}>
        <span className="text-sm font-semibold uppercase tracking-wide text-muted">Passage{passage.title ? ` · ${passage.title}` : ""}</span>
        <span className="text-sm text-muted">{open ? "Hide" : "Show"}</span>
      </button>
      {open && (
        <div className="rise-in mt-3 max-h-[55vh] space-y-3 overflow-y-auto pr-2 text-[15px] leading-relaxed">
          {passage.paragraphs.map((p, i) => (
            <p key={i} className="flex gap-3">
              <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded bg-brand-50 text-xs font-bold text-brand-700 dark:bg-brand-500/15 dark:text-brand-300">
                {i + 1}
              </span>
              <span>{p}</span>
            </p>
          ))}
        </div>
      )}
    </div>
  );
}

/* ---------------------------------------------------------------- memory card */

function Cell({ text }: { text: string }) {
  const star = text.startsWith("!");
  return star ? <strong className="text-brand-700 dark:text-brand-300">{text.slice(1)}</strong> : <>{text}</>;
}

function CardStep({ step }: { step: CourseCardStep }) {
  const ref = useTypeset<HTMLDivElement>([step.id]);
  return (
    <div ref={ref} className="surface-card p-6">
      <div className="text-xs font-semibold uppercase tracking-wide text-accent-600">Rules to know by heart</div>
      <h1 className="mt-1 text-2xl font-bold">{step.title}</h1>
      {step.intro && <p className="mt-2 text-sm text-muted dark:text-neutral-400">{step.intro}</p>}
      {step.tables.map((t, ti) => (
        <div key={ti} className="mt-5">
          {t.title && <h3 className="mb-2 font-semibold">{t.title}</h3>}
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-sm">
              {t.head.length > 0 && (
                <thead>
                  <tr>
                    {t.head.map((h, i) => (
                      <th key={i} className="border border-hair bg-brand-50 px-3 py-2 text-left font-semibold dark:border-white/10 dark:bg-brand-500/10">
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
              )}
              <tbody>
                {t.rows.map((r, ri) => (
                  <tr key={ri}>
                    {r.map((c, ci) => (
                      <td key={ci} className="border border-hair px-3 py-2 align-top dark:border-white/10">
                        <Cell text={c} />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
      {step.tips.length > 0 && (
        <ul className="mt-5 list-disc space-y-1 pl-5 text-sm">
          {step.tips.map((t, i) => (
            <li key={i}>{t}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
