"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { loadProgress, type CourseProgress } from "@/lib/courseProgressStore";
import type { CourseOutline, SubjectKey } from "@/lib/fullCourseTypes";
import { SUBJECT, pad2 } from "@/lib/subjects";

interface Props {
  outline: CourseOutline;
  stepIds: Record<number, string[]>;
  recorded: Record<number, number>;
  totals: { videos: number; lessons: number; questions: number; topics: number; hours: number };
}

export function LearnHome({ outline, stepIds, recorded, totals }: Props) {
  const [p, setP] = useState<CourseProgress | null>(null);
  useEffect(() => setP(loadProgress()), []);

  const topics = useMemo(() => outline.subjects.flatMap((s) => s.topics.map((t) => ({ ...t, subject: s.key }))), [outline]);
  const pct = (t: number) => {
    const ids = stepIds[t] || [];
    if (!p || !ids.length) return 0;
    return Math.round((100 * ids.filter((id) => p.done[`t${t}:${id}`]).length) / ids.length);
  };
  const resume = p?.lastStep ? topics.find((t) => t.id === p.lastStep!.topic) : undefined;

  const [tab, setTab] = useState<SubjectKey>("algebra");
  useEffect(() => {
    if (resume) setTab(resume.subject);
  }, [resume?.subject]); // eslint-disable-line react-hooks/exhaustive-deps
  const subject = outline.subjects.find((s) => s.key === tab)!;
  const firstTopic = outline.subjects[0].topics[0];

  return (
    <>
      {/* ---------------------------------------------------------------- hero */}
      <section className="mx-auto grid max-w-6xl gap-12 px-6 pb-16 pt-16 md:grid-cols-[1.4fr_1fr] md:pt-24">
        <div className="rise-in">
          <div className="eyebrow">Quantitative &amp; Verbal Reasoning</div>
          <h1 className="display mt-5 text-[52px] sm:text-[68px]">
            Everything the exam asks,
            <br />
            <span className="italic text-gold">taught step by step.</span>
          </h1>
          <p className="mt-6 max-w-lg text-[17px] leading-relaxed text-ink-soft">
            Short video lessons, guided questions you try before watching the solution, the rules worth knowing by
            heart, and practice — in the order that builds real understanding.
          </p>
          <div className="mt-9 flex flex-wrap gap-3">
            {resume && p?.lastStep ? (
              <Link href={`/topic/${resume.id}/${p.lastStep.index + 1}`} className="btn">
                Continue · {resume.title}
                <Arrow />
              </Link>
            ) : (
              <Link href={`/topic/${firstTopic.id}/1`} className="btn">
                Start the course
                <Arrow />
              </Link>
            )}
            <a href="#contents" className="btn-ghost">
              Browse the contents
            </a>
          </div>
        </div>
        <dl className="rise-in grid grid-cols-2 content-center gap-x-8 gap-y-10 border-line md:border-l md:pl-12" style={{ animationDelay: "80ms" }}>
          <Stat n={totals.videos} label="video lessons" />
          <Stat n={totals.questions.toLocaleString()} label="questions" />
          <Stat n={totals.topics} label="topics" />
          <Stat n={`${totals.hours}h`} label="of teaching" />
        </dl>
      </section>

      {/* ---------------------------------------------------------------- tools */}
      <section className="mx-auto max-w-6xl px-6 pb-16">
        <div className="eyebrow">Beyond the lessons</div>
        <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[
            { href: "/review", t: "Review", d: "Your mistakes, words and rules — back at the right moment." },
            { href: "/simulations", t: "Simulations", d: "Real exam sections: 20 questions, 20 minutes." },
            { href: "/rules", t: "Rules to know", d: "Every formula and rule from the course, on one page." },
            { href: "/dictionary", t: "Dictionary", d: "Exam vocabulary with meanings and examples — tap to hear it." },
            { href: "/listen", t: "Listen", d: "Vocabulary episodes for the bus, the gym or a walk." },
            { href: "/mental-math", t: "Mental math", d: "60-second rounds: times tables, squares, fractions." },
          ].map((x) => (
            <Link key={x.href} href={x.href} className="pressable card group p-5 transition-shadow hover:shadow-lift">
              <div className="display text-[26px]">{x.t}</div>
              <p className="mt-2 text-sm text-muted">{x.d}</p>
              <div className="mt-4 text-sm text-ink">
                Open <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* ---------------------------------------------------------------- contents */}
      <section id="contents" className="scroll-mt-20 border-t border-line bg-white/60">
        <div className="mx-auto max-w-6xl px-6 py-16">
          <div className="flex flex-wrap items-end justify-between gap-6">
            <div>
              <div className="eyebrow">Contents</div>
              <h2 className="display mt-3 text-[40px]">Four subjects, one path.</h2>
            </div>
            <div role="tablist" aria-label="Subjects" className="flex flex-wrap gap-1 rounded-full border border-line bg-paper p-1">
              {outline.subjects.map((s) => (
                <button
                  key={s.key}
                  role="tab"
                  aria-selected={tab === s.key}
                  onPointerDown={() => setTab(s.key)}
                  onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && setTab(s.key)}
                  className={[
                    "pressable rounded-full px-4 py-2 text-sm transition-colors duration-150",
                    tab === s.key ? "bg-ink text-white" : "text-ink-soft hover:bg-paper-deep",
                  ].join(" ")}
                >
                  {SUBJECT[s.key].short}
                </button>
              ))}
            </div>
          </div>

          <div key={tab} className="fade-in mt-10 grid gap-10 lg:grid-cols-[280px_1fr]">
            <aside>
              <div className="h-1 w-10 rounded-full" style={{ background: SUBJECT[tab].color }} />
              <h3 className="display mt-4 text-[32px]">{SUBJECT[tab].label}</h3>
              <p className="mt-3 text-sm leading-relaxed text-muted">{SUBJECT[tab].blurb}</p>
              <p className="mt-4 text-sm text-ink-soft">
                {subject.topics.length} topics · {subject.topics.reduce((n, t) => n + t.lessons, 0)} lessons ·{" "}
                {subject.topics.reduce((n, t) => n + t.questions, 0)} questions
              </p>
            </aside>

            <ol className="divide-y divide-line border-y border-line">
              {subject.topics.map((t, i) => {
                const done = pct(t.id);
                const rec = recorded[t.id] || 0;
                return (
                  <li key={t.id}>
                    <Link
                      href={`/topic/${t.id}`}
                      className="group grid grid-cols-[3rem_1fr_auto] items-center gap-4 py-5 transition-colors hover:bg-paper/70 sm:grid-cols-[3.5rem_1fr_auto]"
                    >
                      <span className="font-serif text-[28px] leading-none" style={{ color: SUBJECT[tab].color }}>
                        {pad2(i + 1)}
                      </span>
                      <span className="min-w-0">
                        <span className="block text-[17px] font-medium text-ink group-hover:underline group-hover:decoration-line group-hover:underline-offset-4">
                          {t.title}
                        </span>
                        <span className="mt-1 block text-[13px] text-muted">
                          {t.lessons} {t.lessons === 1 ? "lesson" : "lessons"} · {t.questions} questions · about{" "}
                          {Math.max(5, Math.round((t.minutes * 1.4) / 5) * 5)} min
                          {rec < t.videos && <span className="text-faint"> · {rec === 0 ? "videos coming soon" : `${rec}/${t.videos} videos ready`}</span>}
                        </span>
                      </span>
                      <span className="flex items-center gap-3">
                        {done > 0 && <Ring pct={done} color={SUBJECT[tab].color} />}
                        <span className="text-faint transition-transform duration-300 group-hover:translate-x-1">→</span>
                      </span>
                    </Link>
                  </li>
                );
              })}
            </ol>
          </div>
        </div>
      </section>
    </>
  );
}

function Stat({ n, label }: { n: number | string; label: string }) {
  return (
    <div>
      <dt className="display text-[44px]">{n}</dt>
      <dd className="mt-1 text-sm text-muted">{label}</dd>
    </div>
  );
}

export function Ring({ pct, color, size = 30 }: { pct: number; color: string; size?: number }) {
  const r = size / 2 - 3;
  const c = 2 * Math.PI * r;
  return (
    <span className="relative inline-flex items-center justify-center" title={`${pct}% done`}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#e7e3da" strokeWidth="3" />
        <circle
          className="progress-fill"
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="3"
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={c * (1 - pct / 100)}
        />
      </svg>
      <span className="sr-only">{pct}% done</span>
    </span>
  );
}

export function Arrow() {
  return <span aria-hidden>→</span>;
}
