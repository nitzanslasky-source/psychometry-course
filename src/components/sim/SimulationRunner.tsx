"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { QuestionCard } from "./QuestionCard";
import { ClusterIntro } from "./ClusterIntro";
import type { SolutionMethod } from "@/lib/quizTypes";
import { PostSectionReviewSheet } from "./PostSectionReviewSheet";
import { gradeSection } from "@/app/simulation/actions";
import { formatClock, useCountdown } from "@/lib/useCountdown";
import { appendAttempts, getOrCreateUserId, updateAttemptErrorReason } from "@/lib/attemptStore";
import {
  SECTION_SECONDS,
  type Cluster,
  type ErrorReason,
  type QuestionAttempt,
  type SectionWithQuestions,
} from "@/lib/types";

type Phase = "start" | "running" | "review";
type TimerMode = "timed" | "untimed";
type Layout = "paged" | "scroll";

export function SimulationRunner({ data }: { data: SectionWithQuestions }) {
  const { exam, section, questions } = data;

  const [phase, setPhase] = useState<Phase>("start");
  const [timerMode, setTimerMode] = useState<TimerMode>("timed");
  const [layout, setLayout] = useState<Layout>("paged");
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [flagged, setFlagged] = useState<Record<string, boolean>>({});
  const [index, setIndex] = useState(0);
  const [autoSubmitted, setAutoSubmitted] = useState(false);
  /** Answer key, fetched from the server only at submission time. */
  const [key, setKey] = useState<Record<string, number>>({});
  // Worked solutions arrive with the grade, never with the questions — see gradeSection.
  const [methods, setMethods] = useState<Record<string, SolutionMethod[]>>({});
  const [grading, setGrading] = useState(false);
  /** Total seconds spent on the section, frozen at submission. */
  const [totalSeconds, setTotalSeconds] = useState(0);
  /** Seconds spent per question id, accumulated while it is on screen. */
  const [perQuestion, setPerQuestion] = useState<Record<string, number>>({});
  /** Countdown seconds remaining at the moment each question's answer was last set (timed mode only). */
  const [remainingAtAnswer, setRemainingAtAnswer] = useState<Record<string, number>>({});
  /** This section's just-built attempt log, for the review sheet. */
  const [attemptRecords, setAttemptRecords] = useState<QuestionAttempt[]>([]);

  const answersRef = useRef(answers);
  answersRef.current = answers;
  const elapsedRef = useRef(0);
  const perQuestionRef = useRef<Record<string, number>>({});
  perQuestionRef.current = perQuestion;
  const flaggedRef = useRef(flagged);
  flaggedRef.current = flagged;
  const remainingAtAnswerRef = useRef(remainingAtAnswer);
  remainingAtAnswerRef.current = remainingAtAnswer;

  const finish = useCallback(async () => {
    setGrading(true);
    setTotalSeconds(elapsedRef.current);
    try {
      const res = await gradeSection(section.section_id, answersRef.current);
      setKey(res.key);
      setMethods(res.methods);

      const attemptedAt = new Date().toISOString();
      const userId = getOrCreateUserId();
      const records: QuestionAttempt[] = questions.map((q) => {
        const userChoice = answersRef.current[q.id] ?? null;
        const correctChoice = res.key[q.id];
        const remAtAnswer = remainingAtAnswerRef.current[q.id];
        const submissionType =
          userChoice === null
            ? "SKIPPED_UNATTEMPTED"
            : timerMode === "timed" && remAtAnswer !== undefined && remAtAnswer <= 5
              ? "TIMED_OUT_GUESS"
              : "SUBMITTED";
        return {
          attempt_id: `${userId}::${q.id}::${attemptedAt}`,
          user_id: userId,
          pool: q.pool,
          section_id: section.section_id,
          question_id: q.id,
          topic: q.topic,
          subtopic: q.subtopic,
          sub_category_id: q.sub_category_id,
          submission_type: submissionType,
          time_spent_seconds: perQuestionRef.current[q.id] ?? 0,
          user_choice: userChoice,
          correct_choice: correctChoice,
          is_correct: userChoice !== null && userChoice === correctChoice,
          is_flagged: !!flaggedRef.current[q.id],
          error_reason: null,
          attempted_at: attemptedAt,
        };
      });
      appendAttempts(records);
      setAttemptRecords(records);
    } finally {
      setGrading(false);
      setPhase("review");
    }
  }, [section.section_id, questions, timerMode]);

  const submit = useCallback(() => {
    const blanks = questions.filter((q) => answersRef.current[q.id] === undefined).length;
    if (blanks > 0) {
      const ok = window.confirm(
        `${blanks} question${blanks === 1 ? "" : "s"} still unanswered. Finish the section anyway?`,
      );
      if (!ok) return;
    }
    void finish();
  }, [finish, questions]);
  const handleExpire = useCallback(() => {
    setAutoSubmitted(true);
    void finish();
  }, [finish]);

  const clock = useCountdown({
    seconds: SECTION_SECONDS,
    running: phase === "running",
    mode: timerMode,
    onExpire: handleExpire,
  });

  elapsedRef.current = clock.elapsed;

  // Attribute wall-clock time to whichever question is currently on screen.
  // In scroll layout the whole section is visible, so time is tracked per section only.
  useEffect(() => {
    if (phase !== "running" || layout !== "paged") return;
    const id = questions[index]?.id;
    if (!id) return;
    const tick = window.setInterval(() => {
      setPerQuestion((prev) => ({ ...prev, [id]: (prev[id] ?? 0) + 1 }));
    }, 1000);
    return () => window.clearInterval(tick);
  }, [phase, layout, index, questions]);

  const answeredCount = Object.keys(answers).length;
  const unanswered = questions.filter((q) => answers[q.id] === undefined);
  const score = useMemo(
    () => questions.filter((q) => key[q.id] !== undefined && answers[q.id] === key[q.id]).length,
    [questions, answers, key],
  );

  /** Cluster that a given 1-based position falls in. */
  const clusterFor = useCallback(
    (pos: number): Cluster | undefined =>
      section.clusters.find((c) => pos >= c.from && pos <= c.to),
    [section.clusters],
  );

  const select = (id: string, n: number) => {
    setAnswers((prev) => ({ ...prev, [id]: n }));
    // Only meaningful in timed mode — untimed has no "final 5 seconds" to guess under.
    if (timerMode === "timed") {
      setRemainingAtAnswer((prev) => ({ ...prev, [id]: clock.remaining }));
    }
  };

  // ----------------------------------------------------------------- start
  if (phase === "start") {
    return (
      <main className="mx-auto max-w-3xl px-5 py-10">
        <Link href="/simulations" className="text-sm text-ink-soft hover:underline">
          ← All sections
        </Link>
        <h1 className="mt-3 text-2xl font-bold">{section.title}</h1>
        <p className="text-sm text-muted">
          {exam.source_exam_label} · {questions.length} questions
        </p>

        <div className="mt-6 rounded-xl border border-hair bg-white p-6">
          <p className="whitespace-pre-line text-sm">{exam.boilerplate.section_intro}</p>

          <fieldset className="mt-6">
            <legend className="text-sm font-semibold">Timing</legend>
            <div className="mt-2 space-y-2">
              <Choice
                checked={timerMode === "timed"}
                onChange={() => setTimerMode("timed")}
                title="Timed (exam conditions)"
                hint="20:00 for the section. Auto-submits at 0:00 and grades what you've answered."
              />
              <Choice
                checked={timerMode === "untimed"}
                onChange={() => setTimerMode("untimed")}
                title="Untimed practice"
                hint="The clock counts up so you can see your pace, but nothing is cut off."
              />
            </div>
          </fieldset>

          <fieldset className="mt-6">
            <legend className="text-sm font-semibold">Layout</legend>
            <div className="mt-2 space-y-2">
              <Choice
                checked={layout === "paged"}
                onChange={() => setLayout("paged")}
                title="One question per screen"
                hint="Next/Back with a question palette. Closest to the real computerized test."
              />
              <Choice
                checked={layout === "scroll"}
                onChange={() => setLayout("scroll")}
                title="Full section on one page"
                hint="Scroll through all 20 questions like the printed exam."
              />
            </div>
          </fieldset>

          <details className="mt-6 text-sm">
            <summary className="cursor-pointer text-ink-soft">
              {exam.boilerplate.general_comments_title}
            </summary>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-[13.5px]">
              {exam.boilerplate.general_comments.map((c, i) => (
                <li key={i}>{c}</li>
              ))}
            </ul>
          </details>

          <button
            onClick={() => setPhase("running")}
            className="mt-7 w-full rounded-lg bg-ink px-4 py-3 font-medium text-white hover:bg-neutral-800"
          >
            Begin section
          </button>
        </div>
      </main>
    );
  }

  // ---------------------------------------------------------------- review
  const reviewing = phase === "review";
  const visible = layout === "paged" && !reviewing ? [questions[index]] : questions;

  return (
    <main className="mx-auto max-w-3xl px-5 pb-24 pt-6">
      <header className="sticky top-0 z-10 -mx-5 mb-4 border-b border-hair bg-neutral-100/95 px-5 py-3 backdrop-blur">
        <div className="flex items-baseline justify-between gap-4">
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              {/* Always offer a way back out of a section. */}
              <Link
                href="/simulations"
                className="shrink-0 rounded border border-hair bg-white px-2 py-0.5 text-xs text-ink-soft hover:border-neutral-400"
                title="Back to all sections"
              >
                ← Home
              </Link>
              <span className="truncate font-semibold">{section.title}</span>
            </div>
            <div className="mt-0.5 text-xs text-muted">
              {exam.source_exam_label} ·{" "}
              {reviewing ? (
                <>
                  {score} / {questions.length} correct · took {formatClock(totalSeconds)}
                </>
              ) : (
                <>
                  <span className="font-medium text-ink">
                    {answeredCount} of {questions.length} answered
                  </span>
                  {unanswered.length > 0 && <> · {unanswered.length} left</>}
                </>
              )}
            </div>
          </div>
          {!reviewing && (
            <div className="text-right">
              <div
                className={[
                  "font-mono text-lg tabular-nums",
                  timerMode === "timed" && clock.remaining <= 60 ? "text-bad" : "",
                  clock.overtime ? "text-bad" : "",
                ].join(" ")}
                aria-live="off"
              >
                {timerMode === "untimed" && clock.overtime ? "+" : ""}
                {formatClock(
                  timerMode === "untimed" && clock.overtime
                    ? clock.elapsed - SECTION_SECONDS
                    : clock.value,
                )}
              </div>
              <div className="text-[11px] text-muted">
                {timerMode === "timed" ? "remaining" : "elapsed"} · {formatClock(clock.elapsed)} used
              </div>
            </div>
          )}
        </div>
        {!reviewing && (
          <div className="mt-2 h-1 w-full overflow-hidden rounded bg-neutral-300">
            <div
              className="h-full bg-ink transition-all"
              style={{ width: `${(answeredCount / questions.length) * 100}%` }}
            />
          </div>
        )}
      </header>

      {reviewing && (
        <div className="mb-5 rounded-xl border border-hair bg-white p-5">
          <div className="text-lg font-semibold">
            {score} / {questions.length} correct
          </div>
          <p className="mt-1 text-sm text-muted">
            {autoSubmitted
              ? "Time expired — the section was submitted automatically."
              : "Section submitted."}{" "}
            Correct answers are shown in green; your incorrect picks in red.
          </p>

          <dl className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
            <Stat label="Time taken" value={formatClock(totalSeconds)} />
            <Stat
              label="Avg / question"
              value={formatClock(Math.round(totalSeconds / questions.length))}
            />
            <Stat
              label="vs. 20:00 limit"
              value={
                totalSeconds <= SECTION_SECONDS
                  ? `${formatClock(SECTION_SECONDS - totalSeconds)} under`
                  : `${formatClock(totalSeconds - SECTION_SECONDS)} over`
              }
              tone={totalSeconds <= SECTION_SECONDS ? "ok" : "bad"}
            />
            <Stat label="Unanswered" value={String(questions.length - answeredCount)} />
          </dl>

          <PostSectionReviewSheet
            methods={methods}
            attempts={attemptRecords}
            questions={questions}
            onSetReason={(attemptId, reason: ErrorReason) => {
              updateAttemptErrorReason(attemptId, reason);
              setAttemptRecords((prev) =>
                prev.map((a) => (a.attempt_id === attemptId ? { ...a, error_reason: reason } : a)),
              );
            }}
          />

          {Object.keys(perQuestion).length > 0 && (
            <details className="mt-4 text-sm">
              <summary className="cursor-pointer text-ink-soft">Time per question</summary>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {questions.map((q) => {
                  const secs = perQuestion[q.id] ?? 0;
                  const right = key[q.id] !== undefined && answers[q.id] === key[q.id];
                  return (
                    <span
                      key={q.id}
                      className={`rounded border px-2 py-1 text-xs tabular-nums ${
                        right ? "border-ok text-ok" : "border-bad text-bad"
                      }`}
                      title={right ? "Correct" : "Incorrect or unanswered"}
                    >
                      {q.position_in_section}: {formatClock(secs)}
                    </span>
                  );
                })}
              </div>
              <p className="mt-2 text-xs text-muted">
                Per-question times are recorded in one-question-per-screen view; in full-page view
                only the section total is tracked.
              </p>
            </details>
          )}
          <div className="mt-3 flex gap-2">
            <Link
              href="/simulations"
              className="rounded-lg border border-hair px-3 py-2 text-sm hover:border-neutral-400"
            >
              All sections
            </Link>
            <button
              onClick={() => {
                setAnswers({});
                setFlagged({});
                setIndex(0);
                setAutoSubmitted(false);
                setKey({});
                setMethods({});
                setTotalSeconds(0);
                setPerQuestion({});
                setRemainingAtAnswer({});
                setAttemptRecords([]);
                elapsedRef.current = 0;
                setPhase("start");
              }}
              className="rounded-lg border border-hair px-3 py-2 text-sm hover:border-neutral-400"
            >
              Retake
            </button>
          </div>
        </div>
      )}

      <div className="rounded-xl border border-hair bg-white px-6 py-4">
        {visible.map((q) => {
          const cluster = clusterFor(q.position_in_section);
          // Show the cluster header/intro when this question opens the cluster, or
          // always in paged mode (the shared graph must stay visible with each question).
          const showIntro =
            !!cluster && (layout === "paged" ? true : q.position_in_section === cluster.from);
          return (
            <div key={q.id}>
              {showIntro && cluster && (
                <ClusterIntro
                  cluster={cluster}
                  boilerplate={exam.boilerplate}
                  collapsible={layout === "paged"}
                />
              )}
              <QuestionCard
                question={q}
                number={q.position_in_section}
                selected={answers[q.id] ?? null}
                onSelect={(n) => select(q.id, n)}
                reveal={reviewing ? "revealed" : "hidden"}
                correctAnswer={key[q.id]}
                hideFigures={cluster?.figure_path ? [cluster.figure_path] : []}
                flagged={flagged[q.id]}
                onToggleFlag={
                  reviewing ? undefined : () => setFlagged((f) => ({ ...f, [q.id]: !f[q.id] }))
                }
              />
            </div>
          );
        })}
      </div>

      {!reviewing && layout === "paged" && (
        <nav className="mt-5 rounded-xl border border-hair bg-white p-4">
          <div className="flex flex-wrap gap-1.5">
            {questions.map((q, i) => {
              const state = answers[q.id]
                ? "bg-ink text-white"
                : flagged[q.id]
                  ? "bg-amber-100 border-amber-400"
                  : "bg-white";
              return (
                <button
                  key={q.id}
                  onClick={() => setIndex(i)}
                  className={`h-8 w-8 rounded border text-xs ${state} ${
                    i === index ? "ring-2 ring-ink" : "border-hair"
                  }`}
                  aria-label={`Question ${q.position_in_section}`}
                >
                  {q.position_in_section}
                </button>
              );
            })}
          </div>
          <div className="mt-4 flex items-center justify-between gap-3">
            <button
              onClick={() => setIndex((i) => Math.max(0, i - 1))}
              disabled={index === 0}
              className="rounded-lg border border-hair px-4 py-2 text-sm disabled:opacity-40"
            >
              ← Back
            </button>
            <button
              onClick={() =>
                setFlagged((f) => ({
                  ...f,
                  [questions[index].id]: !f[questions[index].id],
                }))
              }
              className="rounded-lg border border-hair px-3 py-2 text-sm hover:border-neutral-400"
            >
              {flagged[questions[index].id] ? "Unflag" : "Flag for review"}
            </button>
            {index < questions.length - 1 ? (
              <button
                onClick={() => setIndex((i) => Math.min(questions.length - 1, i + 1))}
                className="rounded-lg border border-hair px-4 py-2 text-sm hover:border-neutral-400"
              >
                Next →
              </button>
            ) : (
              <button
                onClick={submit}
                disabled={grading}
                className="rounded-lg bg-ink px-4 py-2 text-sm font-medium text-white hover:bg-neutral-800 disabled:opacity-50"
              >
                {grading ? "Grading…" : "Finish section"}
              </button>
            )}
          </div>
        </nav>
      )}

      {!reviewing && (
        <div className="mt-5 flex items-center justify-between gap-3">
          <button
            onClick={() => setLayout((l) => (l === "paged" ? "scroll" : "paged"))}
            className="rounded-lg border border-hair bg-white px-3 py-2 text-sm hover:border-neutral-400"
          >
            {layout === "paged" ? "Switch to full-page view" : "Switch to one-per-screen"}
          </button>
          <button
            onClick={submit}
            disabled={grading}
            className="rounded-lg bg-ink px-5 py-2.5 font-medium text-white hover:bg-neutral-800 disabled:opacity-50"
          >
            {grading ? "Grading…" : "Finish section"}
          </button>
        </div>
      )}
    </main>
  );
}

function Stat({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone?: "ok" | "bad";
}) {
  return (
    <div className="rounded-lg border border-hair px-3 py-2">
      <dt className="text-[11px] uppercase tracking-wide text-muted">{label}</dt>
      <dd
        className={[
          "font-mono text-sm tabular-nums",
          tone === "ok" ? "text-ok" : "",
          tone === "bad" ? "text-bad" : "",
        ].join(" ")}
      >
        {value}
      </dd>
    </div>
  );
}

function Choice({
  checked,
  onChange,
  title,
  hint,
}: {
  checked: boolean;
  onChange: () => void;
  title: string;
  hint: string;
}) {
  return (
    <label
      className={`flex cursor-pointer gap-3 rounded-lg border p-3 ${
        checked ? "border-neutral-800 bg-neutral-50" : "border-hair"
      }`}
    >
      <input type="radio" checked={checked} onChange={onChange} className="mt-1" />
      <span>
        <span className="block text-sm font-medium">{title}</span>
        <span className="block text-[13px] text-muted">{hint}</span>
      </span>
    </label>
  );
}
