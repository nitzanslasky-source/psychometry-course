"use client";

import { useTypeset } from "@/components/MathJaxProvider";
import { QuestionScratchpad } from "./QuestionScratchpad";
import { useCompactMode } from "@/lib/uiPrefs";
import type { Question } from "@/lib/types";
import { RichText } from "./RichText";

export type Reveal = "hidden" | "revealed";

interface Props {
  question: Question;
  /** Student's current pick, 1-based; null if unanswered. */
  selected: number | null;
  onSelect: (n: number) => void;
  /** Simulations stay "hidden" until the whole section is submitted. */
  reveal: Reveal;
  /**
   * Correct option (1-based), supplied only once the section has been graded.
   * Kept out of the question payload so it cannot leak mid-attempt.
   */
  correctAnswer?: number;
  /** Suppress the cluster figure when it is already shown once above the cluster. */
  hideFigures?: string[];
  number: number;
  disabled?: boolean;
  flagged?: boolean;
  /** Omit to render a read-only "Flagged" badge instead of a clickable toggle. */
  onToggleFlag?: () => void;
}

/** Renders `<b>` emphasis that the translation carries, escaping everything else. */
export function QuestionCard({
  question,
  selected,
  onSelect,
  reveal,
  correctAnswer,
  hideFigures = [],
  number,
  disabled,
  flagged,
  onToggleFlag,
}: Props) {
  // Re-typeset when the question or reveal state changes.
  const ref = useTypeset<HTMLDivElement>([question.id, reveal, selected, correctAnswer]);
  const figures = (question.figure_paths ?? []).filter((f) => !hideFigures.includes(f));
  const optionFigures = question.option_figure_paths ?? [];
  const locked = reveal === "revealed" || disabled;
  const compact = useCompactMode();

  return (
    <div
      ref={ref}
      className={["border-t border-hair first:border-t-0", compact ? "py-3 text-sm" : "py-5"].join(" ")}
    >
      <QuestionScratchpad
        key={question.id}
        figurePaths={figures}
        compact={compact}
        topRightSlot={
          onToggleFlag ? (
            <button
              type="button"
              onClick={onToggleFlag}
              aria-pressed={!!flagged}
              className={`rounded border px-2 py-1 text-xs ${
                flagged
                  ? "border-amber-400 bg-amber-100 text-amber-900"
                  : "border-hair bg-white text-muted hover:border-neutral-400"
              }`}
              title={flagged ? "Unflag this question" : "Flag as unsure"}
            >
              {flagged ? "Flagged" : "Flag"}
            </button>
          ) : (
            flagged && (
              <span className="rounded border border-amber-400 bg-amber-100 px-2 py-1 text-xs text-amber-900">
                Flagged
              </span>
            )
          )
        }
      >
        <div className="flex gap-3">
          <div className="min-w-[2.2em] font-bold">{number}.</div>
          {/* whitespace-pre-line preserves the \n\n break between givens and the question */}
          <div className="flex-1 whitespace-pre-line">
            {question.cancelled && (
              <div className="mb-1.5 inline-block rounded border border-amber-300 bg-amber-50 px-2 py-0.5 text-xs font-semibold not-italic text-amber-800">
                NITE cancelled this question — it is not scored
              </div>
            )}
            <RichText text={question.stem} />
          </div>
        </div>
      </QuestionScratchpad>

      <ol className={["ml-[2.2em] list-none p-0", compact ? "mt-1.5 space-y-1" : "mt-3 space-y-2"].join(" ")}>
        {question.options.map((opt, i) => {
          const n = i + 1;
          const isCorrect = reveal === "revealed" && n === correctAnswer;
          const isWrongPick =
            reveal === "revealed" && n === selected && selected !== correctAnswer;
          const isPicked = reveal === "hidden" && n === selected;

          // A selected answer must be unmistakable at a glance: the student needs to
          // know which questions are done without re-reading them.
          const cls = [
            "flex items-center gap-3 rounded-md transition-colors",
            compact ? "px-2.5 py-1" : "px-3 py-2",
            locked ? "cursor-default" : "cursor-pointer",
            isCorrect ? "border-2 border-ok bg-emerald-50" : "",
            isWrongPick ? "border-2 border-bad bg-red-50" : "",
            isPicked ? "border-2 border-ink bg-paper-deep ring-1 ring-ink" : "",
            !isCorrect && !isWrongPick && !isPicked
              ? `border-2 border-hair bg-white ${locked ? "" : "hover:border-neutral-400 hover:bg-neutral-50"}`
              : "",
          ].join(" ");

          return (
            <li
              key={n}
              className={cls}
              onClick={() => !locked && onSelect(n)}
              role="radio"
              aria-checked={selected === n}
              tabIndex={locked ? -1 : 0}
              onKeyDown={(e) => {
                if (!locked && (e.key === "Enter" || e.key === " ")) {
                  e.preventDefault();
                  onSelect(n);
                }
              }}
            >
              {/* Radio-style indicator, filled when chosen. */}
              <span
                className={[
                  "flex h-[18px] w-[18px] shrink-0 items-center justify-center rounded-full border-2",
                  isCorrect ? "border-ok bg-ok" : "",
                  isWrongPick ? "border-bad bg-bad" : "",
                  isPicked ? "border-ink bg-ink" : "",
                  !isCorrect && !isWrongPick && !isPicked ? "border-neutral-400 bg-white" : "",
                ].join(" ")}
                aria-hidden="true"
              >
                {(isPicked || isCorrect || isWrongPick) && (
                  <span className="h-[6px] w-[6px] rounded-full bg-white" />
                )}
              </span>
              <span
                className={[
                  "min-w-[1.9em]",
                  isCorrect ? "font-bold text-ok" : "",
                  isWrongPick ? "font-bold text-bad" : "",
                  isPicked ? "font-bold text-ink-soft" : "",
                  !isCorrect && !isWrongPick && !isPicked ? "text-muted" : "",
                ].join(" ")}
              >
                ({n})
              </span>
              <span>
                {optionFigures[i] ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={`/${optionFigures[i]}`} alt={`option ${n}`} className="max-h-[190px] w-auto max-w-[260px]" />
                ) : (
                  <RichText text={opt} />
                )}
              </span>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
