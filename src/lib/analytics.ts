import { ERROR_REASONS, type ErrorReason, type QuestionAttempt } from "./types";

/** The "Unreached Questions due to Pacing" section-level metric. */
export function computeUnreachedCount(attempts: QuestionAttempt[]): number {
  return attempts.filter((a) => a.submission_type === "SKIPPED_UNATTEMPTED").length;
}

/** Slow brute-forcing rather than a NITE shortcut. */
export function isTimeSinkQuestion(a: QuestionAttempt): boolean {
  return a.time_spent_seconds > 90;
}

export interface ErrorReasonBreakdown {
  reason: ErrorReason;
  count: number;
  pct: number;
}

export function computeErrorReasonBreakdown(attempts: QuestionAttempt[]): ErrorReasonBreakdown[] {
  const tagged = attempts.filter(
    (a): a is QuestionAttempt & { error_reason: ErrorReason } => a.error_reason !== null,
  );
  const total = tagged.length;
  return ERROR_REASONS.map((reason) => {
    const count = tagged.filter((a) => a.error_reason === reason).length;
    return { reason, count, pct: total === 0 ? 0 : (count / total) * 100 };
  });
}
