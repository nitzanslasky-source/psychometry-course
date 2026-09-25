"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { loadProgress, type CourseProgress } from "@/lib/courseProgressStore";
import type { CourseOutline } from "@/lib/fullCourseTypes";
import { IconChevronRight } from "@/components/icons";

interface Props {
  outline: CourseOutline;
  /** topic id → every step id (for progress). */
  stepIds: Record<number, string[]>;
  /** topic id → number of recorded (available) videos. */
  recorded: Record<number, number>;
}

export function LearnHome({ outline, stepIds, recorded }: Props) {
  const [p, setP] = useState<CourseProgress | null>(null);
  useEffect(() => setP(loadProgress()), []);

  const pct = (t: number) => {
    const ids = stepIds[t] || [];
    if (!p || !ids.length) return 0;
    return Math.round((100 * ids.filter((id) => p.done[`t${t}:${id}`]).length) / ids.length);
  };
  const resume = p?.lastStep;
  const resumeTitle = resume
    ? outline.subjects.flatMap((s) => s.topics).find((t) => t.id === resume.topic)?.title
    : undefined;

  return (
    <>
      {resume && resumeTitle && (
        <Link
          href={`/topic/${resume.topic}/${resume.index + 1}`}
          className="surface-card surface-card-hover mt-6 flex items-center justify-between gap-4 p-5"
        >
          <div>
            <div className="text-xs font-semibold uppercase tracking-wide text-brand-600 dark:text-brand-400">
              Continue where you left off
            </div>
            <div className="mt-1 font-semibold">{resumeTitle}</div>
          </div>
          <IconChevronRight className="text-muted" width={18} height={18} />
        </Link>
      )}

      {outline.subjects.map((s) => (
        <section key={s.key} className="rise-in mt-12">
          <h2 className="text-2xl font-bold">{s.title}</h2>
          <ul className="mt-3 grid gap-3 sm:grid-cols-2">
            {s.topics.map((t) => {
              const done = pct(t.id);
              const rec = recorded[t.id] || 0;
              return (
                <li key={t.id}>
                  <Link href={`/topic/${t.id}`} className="surface-card surface-card-hover block p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div className="font-semibold leading-snug">{t.title}</div>
                      <span className="shrink-0 text-xs text-muted dark:text-neutral-400">
                        {done > 0 ? `${done}%` : ""}
                      </span>
                    </div>
                    <div className="mt-1 text-xs text-muted dark:text-neutral-400">
                      {t.videos} video{t.videos === 1 ? "" : "s"} · {t.questions} questions · ~{Math.max(1, Math.round(t.minutes))} min
                      {rec < t.videos && (
                        <span className="ml-1">
                          · {rec === 0 ? "videos coming soon" : `${rec}/${t.videos} videos ready`}
                        </span>
                      )}
                    </div>
                    <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-hair dark:bg-white/10">
                      <div className="progress-fill h-full rounded-full bg-brand-500" style={{ width: `${done}%` }} />
                    </div>
                  </Link>
                </li>
              );
            })}
          </ul>
        </section>
      ))}
    </>
  );
}
