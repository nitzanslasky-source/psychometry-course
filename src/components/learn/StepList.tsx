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
  minutes?: number;
  /** A worked-solution video (shown under its question). */
  solution?: boolean;
  /** Practice question number within the section. */
  n?: number;
}

export interface StepListSection {
  title: string;
  kind: string;
  items: StepListItem[];
}

/** Topic outline: lessons as a syllabus, questions paired with their solutions, practice as number grids. */
export function StepList({
  topic,
  sections,
  current,
  compact,
  accent = "#101826",
  onNavigate,
}: {
  topic: number;
  sections: StepListSection[];
  current?: number;
  compact?: boolean;
  accent?: string;
  onNavigate?: () => void;
}) {
  const [p, setP] = useState<CourseProgress | null>(null);
  useEffect(() => setP(loadProgress()), [current]);
  const isDone = (id: string) => !!p?.done[`t${topic}:${id}`];

  return (
    <div className={compact ? "space-y-7" : "space-y-12"}>
      {sections.map((s, si) =>
        s.kind === "practice" ? (
          <PracticeGrid key={si} topic={topic} section={s} current={current} isDone={isDone} accent={accent} compact={compact} onNavigate={onNavigate} />
        ) : (
          <section key={si}>
            <div className="eyebrow mb-3">{s.title}</div>
            <ol className={compact ? "space-y-0.5" : "space-y-1"}>
              {s.items.map((it) => {
                const active = it.index === current;
                const done = isDone(it.id);
                const lesson = it.kind === "video" && !it.solution;
                return (
                  <li key={it.index} className={it.solution ? "pl-7" : lesson && !compact ? "pt-3 first:pt-0" : ""}>
                    <Link
                      href={`/topic/${topic}/${it.index + 1}`}
                      onClick={onNavigate}
                      aria-current={active ? "step" : undefined}
                      className={[
                        "pressable group flex items-center gap-3 rounded-xl px-3 transition-colors duration-150",
                        compact ? "py-1.5 text-[13px]" : "py-2.5 text-[15px]",
                        active ? "bg-ink text-white" : "hover:bg-paper-deep",
                      ].join(" ")}
                    >
                      <Marker kind={it.kind} solution={it.solution} done={done} active={active} accent={accent} />
                      <span className={["min-w-0 flex-1 truncate", lesson ? "font-medium" : "", it.solution && !active ? "text-muted" : ""].join(" ")}>
                        {it.label}
                      </span>
                      {it.soon ? (
                        <span className={["shrink-0 text-[11px]", active ? "text-white/60" : "text-faint"].join(" ")}>soon</span>
                      ) : it.minutes && lesson && !compact ? (
                        <span className="shrink-0 text-xs text-faint">{Math.max(1, Math.round(it.minutes * 1.4))} min</span>
                      ) : null}
                    </Link>
                  </li>
                );
              })}
            </ol>
          </section>
        ),
      )}
    </div>
  );
}

function Marker({ kind, solution, done, active, accent }: { kind: StepListItem["kind"]; solution?: boolean; done: boolean; active: boolean; accent: string }) {
  const base = "flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-[10px] transition-colors";
  if (done)
    return (
      <span className={base} style={{ background: active ? "#fff" : accent, color: active ? accent : "#fff" }} aria-label="done">
        ✓
      </span>
    );
  const ring = active ? "border border-white/50 text-white" : "border border-line text-muted";
  if (kind === "video") return <span className={`${base} ${ring}`}>{solution ? "↳" : "▶"}</span>;
  if (kind === "card") return <span className={`${base} ${ring}`}>≡</span>;
  return <span className={`${base} ${ring} font-semibold`}>?</span>;
}

function PracticeGrid({
  topic,
  section,
  current,
  isDone,
  accent,
  compact,
  onNavigate,
}: {
  topic: number;
  section: StepListSection;
  current?: number;
  isDone: (id: string) => boolean;
  accent: string;
  compact?: boolean;
  onNavigate?: () => void;
}) {
  const groups: { name: string; items: StepListItem[] }[] = [];
  for (const it of section.items) {
    const name = it.group || "Practice";
    if (!groups.length || groups[groups.length - 1].name !== name) groups.push({ name, items: [] });
    groups[groups.length - 1].items.push(it);
  }
  const doneN = section.items.filter((it) => isDone(it.id)).length;
  return (
    <section>
      <div className="mb-3 flex items-baseline justify-between gap-3">
        <div className="eyebrow">Practice · {section.title}</div>
        <div className="text-xs text-muted">
          {doneN}/{section.items.length}
        </div>
      </div>
      <div className={compact ? "space-y-3" : "space-y-5"}>
        {groups.map((g, gi) => (
          <div key={gi}>
            {groups.length > 1 && <div className={compact ? "mb-1.5 text-xs text-muted" : "mb-2 text-sm text-ink-soft"}>{g.name}</div>}
            <div className="flex flex-wrap gap-1.5">
              {g.items.map((it) => {
                const active = it.index === current;
                const done = isDone(it.id);
                return (
                  <Link
                    key={it.index}
                    href={`/topic/${topic}/${it.index + 1}`}
                    onClick={onNavigate}
                    aria-current={active ? "step" : undefined}
                    title={`Practice question ${it.n}`}
                    className={[
                      "pressable flex items-center justify-center rounded-lg text-xs tabular-nums transition-colors duration-150",
                      compact ? "h-7 w-7" : "h-9 w-9",
                      active ? "bg-ink text-white" : done ? "text-white" : "border border-line bg-white text-ink-soft hover:border-faint",
                    ].join(" ")}
                    style={done && !active ? { background: accent } : undefined}
                  >
                    {it.n}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
