"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { loadProgress, type CourseProgress } from "@/lib/courseProgressStore";

export interface StepListItem {
  index: number;
  kind: "video" | "question" | "card";
  label: string;
  id: string;
  /** Video not recorded yet. */
  soon?: boolean;
  group?: string;
}

export interface StepListSection {
  title: string;
  kind: string;
  items: StepListItem[];
}

const ICON: Record<StepListItem["kind"], string> = { video: "▶", question: "?", card: "▤" };

/** Topic outline: sections with their steps, done ticks and the current step highlighted. */
export function StepList({
  topic,
  sections,
  current,
  compact,
}: {
  topic: number;
  sections: StepListSection[];
  current?: number;
  compact?: boolean;
}) {
  const [p, setP] = useState<CourseProgress | null>(null);
  useEffect(() => setP(loadProgress()), [current]);

  return (
    <div className="space-y-6">
      {sections.map((s, si) => {
        let lastGroup: string | undefined;
        return (
          <section key={si}>
            <h3 className={compact ? "text-sm font-semibold" : "text-lg font-semibold"}>
              {s.kind === "practice" ? "Practice · " : ""}
              {s.title}
            </h3>
            <ol className="mt-2 space-y-1">
              {s.items.map((it) => {
                const done = !!p?.done[`t${topic}:${it.id}`];
                const head = it.group && it.group !== lastGroup ? it.group : null;
                lastGroup = it.group;
                return (
                  <li key={it.index}>
                    {head && (
                      <div className="mb-1 mt-3 text-xs font-semibold uppercase tracking-wide text-muted dark:text-neutral-400">
                        {head}
                      </div>
                    )}
                    <Link
                      href={`/topic/${topic}/${it.index + 1}`}
                      className={[
                        "pressable flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm transition-colors duration-150",
                        it.index === current
                          ? "bg-brand-50 font-semibold text-brand-800 dark:bg-brand-500/15 dark:text-brand-200"
                          : "hover:bg-neutral-100 dark:hover:bg-white/5",
                      ].join(" ")}
                    >
                      <span
                        className={[
                          "flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[10px]",
                          done ? "bg-ok text-white" : "bg-hair text-muted dark:bg-white/10 dark:text-neutral-400",
                        ].join(" ")}
                        aria-hidden
                      >
                        {done ? "✓" : ICON[it.kind]}
                      </span>
                      <span className="min-w-0 flex-1 truncate">{it.label}</span>
                      {it.soon && <span className="shrink-0 text-[11px] text-muted">soon</span>}
                    </Link>
                  </li>
                );
              })}
            </ol>
          </section>
        );
      })}
    </div>
  );
}
