"use client";

import {
  computeErrorReasonBreakdown,
  computeUnreachedCount,
  isTimeSinkQuestion,
} from "@/lib/analytics";
import { ERROR_REASONS, type ErrorReason, type Question, type QuestionAttempt } from "@/lib/types";
import { METHOD_KINDS, type SolutionMethod } from "@/lib/quizTypes";
import { useTypeset } from "@/components/MathJaxProvider";

/** Permits <b> and <i>, escaping everything else — mirrors PracticeQuestionCard's
 *  RichText. MathJax delimiters pass through untouched and are typeset by the hook
 *  on the sheet root. */
function RichText({ text }: { text: string }) {
  const parts = text.split(/(<\/?[bi]>)/g);
  let bold = false;
  let italic = false;
  return (
    <>
      {parts.map((p, i) => {
        if (p === "<b>") return (bold = true), null;
        if (p === "</b>") return (bold = false), null;
        if (p === "<i>") return (italic = true), null;
        if (p === "</i>") return (italic = false), null;
        const cls = [bold ? "font-semibold" : "", italic ? "italic" : ""].join(" ").trim();
        return cls ? <span key={i} className={cls}>{p}</span> : <span key={i}>{p}</span>;
      })}
    </>
  );
}

const REASON_LABELS: Record<ErrorReason, string> = {
  CALCULATION_ERROR: "Calculation error",
  MISREAD_STEM: "Misread stem",
  CONCEPT_DEFICIT: "Concept deficit",
  TIME_CRUNCH: "Time crunch",
  LUCKY_GUESS: "Lucky guess",
};

export function PostSectionReviewSheet({
  attempts,
  questions,
  methods,
  onSetReason,
}: {
  /** This section's just-completed attempt batch (not full cross-session history). */
  attempts: QuestionAttempt[];
  questions: Question[];
  /** Keyed by question id; arrives from gradeSection, so it is empty until submission. */
  methods?: Record<string, SolutionMethod[]>;
  onSetReason: (attemptId: string, reason: ErrorReason) => void;
}) {
  const ref = useTypeset<HTMLDivElement>([attempts.length, methods]);
  const questionById = new Map(questions.map((q) => [q.id, q]));
  const missed = attempts
    .filter((a) => a.is_flagged || !a.is_correct)
    .slice()
    .sort(
      (a, b) =>
        (questionById.get(a.question_id)?.position_in_section ?? 0) -
        (questionById.get(b.question_id)?.position_in_section ?? 0),
    );

  if (missed.length === 0) return null;

  const unreached = computeUnreachedCount(attempts);
  const breakdown = computeErrorReasonBreakdown(attempts);
  const taggedCount = breakdown.reduce((sum, b) => sum + b.count, 0);

  return (
    <div ref={ref} className="mt-5 rounded-xl border border-hair bg-white p-5">
      <h2 className="text-lg font-semibold">Post-Section Review</h2>
      <p className="mt-1 text-sm text-muted">
        {missed.length} question{missed.length === 1 ? "" : "s"} missed or flagged
        {unreached > 0 && <> · {unreached} unreached due to pacing</>}. Tag each with what went
        wrong so the analytics dashboard can tell a real gap from a rushed guess.
      </p>

      <ul className="mt-4 space-y-3">
        {missed.map((a) => {
          const q = questionById.get(a.question_id);
          return (
            <li key={a.attempt_id} className="rounded-lg border border-hair p-3">
              <div className="flex flex-wrap items-center gap-2 text-sm">
                <span className="font-semibold">Q{q?.position_in_section ?? "?"}</span>
                <span className="text-muted">
                  {a.topic} · {a.subtopic}
                </span>
                {a.is_flagged && (
                  <span className="rounded border border-amber-400 bg-amber-100 px-2 py-0.5 text-xs text-amber-900">
                    Flagged
                  </span>
                )}
                {a.submission_type === "SKIPPED_UNATTEMPTED" && (
                  <span className="rounded border border-hair bg-neutral-100 px-2 py-0.5 text-xs text-muted">
                    Unattempted
                  </span>
                )}
                {a.submission_type === "TIMED_OUT_GUESS" && (
                  <span className="rounded border border-hair bg-neutral-100 px-2 py-0.5 text-xs text-muted">
                    Timed-out guess
                  </span>
                )}
                {!a.is_correct && a.submission_type === "SUBMITTED" && (
                  <span className="rounded border border-bad bg-red-50 px-2 py-0.5 text-xs text-bad">
                    Incorrect
                  </span>
                )}
                {isTimeSinkQuestion(a) && (
                  <span className="rounded border border-amber-400 bg-amber-100 px-2 py-0.5 text-xs text-amber-900">
                    Time sink
                  </span>
                )}
              </div>

              {(methods?.[a.question_id]?.length ?? 0) > 0 && (
                <div className="mt-3 space-y-2 rounded-lg bg-neutral-50 p-3">
                  <div className="text-xs font-semibold uppercase tracking-wide text-muted">
                    How to solve it &mdash; {methods![a.question_id].length} way
                    {methods![a.question_id].length === 1 ? "" : "s"}
                  </div>
                  {methods![a.question_id].map((m, i) => (
                    <div key={i}>
                      <div className="text-xs font-semibold text-ink">{METHOD_KINDS[m.kind]}</div>
                      <div className="mt-0.5 text-sm text-muted">
                        <RichText text={m.text} />
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <div className="mt-2 flex flex-wrap gap-1.5">
                {ERROR_REASONS.map((reason) => (
                  <button
                    key={reason}
                    type="button"
                    onClick={() => onSetReason(a.attempt_id, reason)}
                    className={`rounded-full border px-3 py-1 text-xs ${
                      a.error_reason === reason
                        ? "border-ink bg-ink text-white"
                        : "border-hair bg-white text-muted hover:border-neutral-400"
                    }`}
                  >
                    {REASON_LABELS[reason]}
                  </button>
                ))}
              </div>
            </li>
          );
        })}
      </ul>

      {taggedCount > 0 && (
        <div className="mt-5">
          <h3 className="text-sm font-semibold">Error breakdown</h3>
          <div className="mt-2 space-y-1.5">
            {breakdown
              .filter((b) => b.count > 0)
              .map((b) => (
                <div key={b.reason} className="flex items-center gap-2 text-xs">
                  <span className="w-32 shrink-0 text-muted">{REASON_LABELS[b.reason]}</span>
                  <div className="h-2 flex-1 overflow-hidden rounded bg-neutral-200">
                    <div className="h-full bg-ink" style={{ width: `${b.pct}%` }} />
                  </div>
                  <span className="w-16 shrink-0 text-right tabular-nums text-muted">
                    {Math.round(b.pct)}% ({b.count})
                  </span>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
