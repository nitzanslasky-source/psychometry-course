"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { useTypeset } from "@/components/MathJaxProvider";
import { loadProgress, markDone, recordAnswer, setLastStep, stepKey } from "@/lib/courseProgressStore";
import type {
  CourseQuestionStep,
  CourseStep,
  CourseVideoStep,
  VideoSource,
} from "@/lib/fullCourseTypes";
import { StepList, type StepListSection } from "./StepList";
import { MemoryCard } from "./MemoryCard";
import { AddToReview } from "@/components/extras/AddToReview";

interface Nav {
  topic: number;
  topicTitle: string;
  subjectLabel: string;
  accent: string;
  index: number;
  total: number;
  prevHref?: string;
  nextHref?: string;
  nextLabel?: string;
}

/** The learning screen: progress bar, one step, sticky Previous/Next, contents drawer. */
export function StepView({
  step,
  nav,
  video,
  passage,
  label,
  sections,
}: {
  step: CourseStep;
  nav: Nav;
  video?: VideoSource | null;
  passage?: { title: string; paragraphs: string[] } | null;
  label: string;
  sections: StepListSection[];
}) {
  const router = useRouter();
  useEffect(() => setLastStep(nav.topic, nav.index), [nav.topic, nav.index]);
  const complete = useCallback(() => markDone(nav.topic, step.id), [nav.topic, step.id]);

  // Enter along the direction of travel (Next → from the right, Previous → from the left).
  const [dir, setDir] = useState<"next" | "prev">("next");
  useEffect(() => {
    try {
      setDir(sessionStorage.getItem("stepDir") === "prev" ? "prev" : "next");
    } catch {}
  }, [step.id]);
  const go = useCallback((d: "next" | "prev") => {
    try {
      sessionStorage.setItem("stepDir", d);
    } catch {}
  }, []);

  const [drawer, setDrawer] = useState(false);
  useEffect(() => setDrawer(false), [step.id]);

  // ← / → move between steps (not while typing or while the drawer is open).
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === "Escape") setDrawer(false);
      if (drawer) return;
      if (e.key === "ArrowRight" && nav.nextHref) {
        if (step.kind !== "question") complete();
        go("next");
        router.push(nav.nextHref);
      }
      if (e.key === "ArrowLeft" && nav.prevHref) {
        go("prev");
        router.push(nav.prevHref);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [drawer, nav.nextHref, nav.prevHref, step.kind, complete, go, router]);

  const pct = ((nav.index + 1) / nav.total) * 100;
  const wide = step.kind === "video";

  return (
    <div className="min-h-[calc(100vh-4rem)] pb-28">
      {/* ------------------------------------------------ sub-bar with progress */}
      <div className="material edge-bottom sticky top-16 z-30 border-t border-line/60">
        <div className="mx-auto flex h-12 max-w-6xl items-center justify-between gap-4 px-6 text-sm">
          <Link href={`/topic/${nav.topic}`} className="pressable min-w-0 truncate text-ink-soft hover:text-ink">
            <span className="text-faint">←</span> {nav.topicTitle}
          </Link>
          <div className="flex shrink-0 items-center gap-4">
            <span className="hidden tabular-nums text-muted sm:inline">
              {nav.index + 1} / {nav.total}
            </span>
            <button type="button" onClick={() => setDrawer(true)} className="pressable rounded-full border border-line bg-white px-3.5 py-1 text-ink-soft hover:border-faint">
              Contents
            </button>
          </div>
        </div>
        <div className="h-[2px] bg-line/60">
          <div className="progress-fill h-full" style={{ width: `${pct}%`, background: nav.accent }} />
        </div>
      </div>

      {/* ------------------------------------------------ the step */}
      <div className={["mx-auto px-6 pt-10", wide ? "max-w-5xl" : "max-w-read"].join(" ")}>
        <div className="eyebrow" style={{ color: nav.accent }}>
          {label}
        </div>
        <div key={step.id} className={dir === "prev" ? "step-in-prev mt-4" : "step-in-next mt-4"}>
          {step.kind === "video" && <VideoStep step={step} video={video} onEnded={complete} />}
          {step.kind === "question" && <QuestionStep key={step.id} step={step} topic={nav.topic} passage={passage} accent={nav.accent} />}
          {step.kind === "card" && (
            <MemoryCard
              step={step}
              accent={nav.accent}
              heading={
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <h1 className="display text-[40px] sm:text-[48px]">{step.title}</h1>
                  <AddToReview srsKey={`c:${step.id}`} />
                </div>
              }
            />
          )}
        </div>
      </div>

      {/* ------------------------------------------------ bottom bar */}
      <div className="material edge-top fixed inset-x-0 bottom-0 z-30 border-t border-line/60">
        <div className="mx-auto flex h-[72px] max-w-6xl items-center justify-between gap-3 px-6">
          {nav.prevHref ? (
            <Link href={nav.prevHref} className="btn-ghost" onPointerDown={() => go("prev")}>
              <span aria-hidden>←</span> Previous
            </Link>
          ) : (
            <span />
          )}
          <span className="hidden text-xs text-muted md:block">Use ← → to move</span>
          {nav.nextHref ? (
            <Link
              href={nav.nextHref}
              className="btn"
              onPointerDown={() => go("next")}
              onClick={() => step.kind !== "question" && complete()}
            >
              {nav.nextLabel || "Next"} <span aria-hidden>→</span>
            </Link>
          ) : (
            <Link href={`/topic/${nav.topic}`} className="btn" onClick={complete}>
              Finish the topic ✓
            </Link>
          )}
        </div>
      </div>

      {/* ------------------------------------------------ contents drawer */}
      {drawer && (
        <div className="fixed inset-0 z-50" role="dialog" aria-modal="true" aria-label="Topic contents">
          <button type="button" aria-label="Close contents" className="fade-in absolute inset-0 bg-ink/25" onClick={() => setDrawer(false)} />
          <div className="drawer-in absolute inset-y-0 right-0 flex w-[min(400px,92vw)] flex-col bg-paper shadow-lift">
            <div className="flex items-center justify-between border-b border-line px-6 py-4">
              <div>
                <div className="eyebrow">{nav.subjectLabel}</div>
                <div className="display mt-1 text-[26px]">{nav.topicTitle}</div>
              </div>
              <button type="button" onClick={() => setDrawer(false)} className="pressable rounded-full px-3 py-1 text-sm text-muted hover:bg-paper-deep">
                Close
              </button>
            </div>
            <div className="flex-1 overflow-y-auto px-4 py-5">
              <StepList topic={nav.topic} sections={sections} current={nav.index} compact accent={nav.accent} onNavigate={() => setDrawer(false)} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ---------------------------------------------------------------- video */

function VideoStep({ step, video, onEnded }: { step: CourseVideoStep; video?: VideoSource | null; onEnded: () => void }) {
  return (
    <div>
      <h1 className="display text-[40px] sm:text-[48px]">{step.title}</h1>
      <div className="mt-6 overflow-hidden rounded-2xl bg-ink shadow-lift">
        <div className="relative aspect-video">
          {!video && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 text-center text-white">
              <div className="flex h-16 w-16 items-center justify-center rounded-full border border-white/25 text-xl text-white/80">▶</div>
              <div className="display mt-2 text-[28px]">Video coming soon</div>
              <div className="max-w-sm text-sm text-white/60">This lesson is being recorded. You can continue with the rest of the topic meanwhile.</div>
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
      {step.minutes ? <p className="mt-3 text-sm text-muted">About {Math.max(1, Math.round(step.minutes * 1.4))} minutes</p> : null}
    </div>
  );
}

/* ---------------------------------------------------------------- question */

function QuestionStep({
  step,
  topic,
  passage,
  accent,
}: {
  step: CourseQuestionStep;
  topic: number;
  passage?: { title: string; paragraphs: string[] } | null;
  accent: string;
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
    recordAnswer(topic, step.id, picked, step.correct);
    setChecked(true);
  };
  const retry = () => {
    setPicked(null);
    setChecked(false);
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (checked || e.metaKey || e.ctrlKey) return;
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
      {step.instructions && <p className="mb-5 border-l-2 border-line pl-4 text-sm italic text-muted">{step.instructions}</p>}
      <div className="text-[19px] leading-[1.65] text-ink">{step.stem}</div>
      {step.figure && (
        <figure className="card mt-7 p-6">
          <div className="mx-auto max-w-lg [&>svg]:h-auto [&>svg]:w-full" dangerouslySetInnerHTML={{ __html: step.figure }} />
          <figcaption className="mt-2 text-right text-xs text-faint">Figure not necessarily drawn to scale.</figcaption>
        </figure>
      )}

      <ol className="mt-8 list-none space-y-2.5 p-0" role="radiogroup">
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
                "flex items-start gap-4 rounded-2xl border bg-white px-5 py-4 text-[16px] transition-[border-color,box-shadow,background-color] duration-150",
                checked ? "cursor-default" : "pressable cursor-pointer select-none hover:border-faint",
                isCorrect ? "anim-land border-ok bg-[#f1f8f4]" : "",
                isWrong ? "anim-nope border-bad bg-[#fbf1f0]" : "",
                isPicked ? "border-ink shadow-[0_0_0_1px_#101826]" : "",
                !isCorrect && !isWrong && !isPicked ? "border-line" : "",
                checked && !isCorrect && !isWrong ? "opacity-60" : "",
              ].join(" ")}
            >
              <span
                className={[
                  "mt-px flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-semibold tabular-nums",
                  isCorrect ? "bg-ok text-white" : isWrong ? "bg-bad text-white" : isPicked ? "bg-ink text-white" : "border border-line text-muted",
                ].join(" ")}
                aria-hidden
              >
                {isCorrect ? "✓" : isWrong ? "✕" : i + 1}
              </span>
              <span className="leading-relaxed">{c}</span>
            </li>
          );
        })}
      </ol>

      {!checked ? (
        <div className="mt-6 flex items-center gap-4">
          <button type="button" className="btn" disabled={picked === null} onClick={check}>
            Check answer
          </button>
          <span className="text-xs text-faint">Keys 1–4 choose · Enter checks</span>
        </div>
      ) : (
        <div className="rise-in mt-8 rounded-2xl border border-line bg-white p-6">
          <div className="flex items-baseline justify-between gap-4">
            <div className={["display text-[28px]", picked === step.correct ? "text-ok" : "text-bad"].join(" ")}>
              {picked === step.correct ? "Correct." : `The answer is choice ${step.correct + 1}.`}
            </div>
            <button type="button" className="text-sm text-muted underline decoration-line underline-offset-4 hover:text-ink" onClick={retry}>
              Try again
            </button>
          </div>
          {step.explanation.length > 0 && (
            <div className="mt-3 space-y-2 text-[15px] leading-relaxed text-ink-soft" style={{ borderColor: accent }}>
              {step.explanation.map((e, i) => (
                <p key={i}>{e}</p>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function PassagePanel({ passage }: { passage: { title: string; paragraphs: string[] } }) {
  const [open, setOpen] = useState(true);
  return (
    <div className="card mb-8 overflow-hidden">
      <button type="button" className="pressable flex w-full items-center justify-between px-6 py-4 text-left" onClick={() => setOpen(!open)}>
        <span className="eyebrow">Reading passage{passage.title ? ` · ${passage.title}` : ""}</span>
        <span className="text-sm text-muted">{open ? "Hide" : "Show"}</span>
      </button>
      {open && (
        <div className="rise-in max-h-[52vh] space-y-4 overflow-y-auto border-t border-line px-6 py-5 font-serif text-[19px] leading-[1.6]">
          {passage.paragraphs.map((p, i) => (
            <p key={i} className="flex gap-4">
              <span className="w-5 shrink-0 pt-1 text-right font-sans text-xs text-faint tabular-nums">{i + 1}</span>
              <span>{p}</span>
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
