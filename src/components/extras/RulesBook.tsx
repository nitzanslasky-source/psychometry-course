"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { CourseCardStep, SubjectKey } from "@/lib/fullCourseTypes";
import { SUBJECT } from "@/lib/subjects";
import { MemoryCard } from "@/components/learn/MemoryCard";

interface Item {
  card: CourseCardStep;
  topicId: number;
  topicTitle: string;
  subject: SubjectKey;
  step: number;
}

/** All "rules to know" cards, by subject, with a quick index. */
export function RulesBook({ items }: { items: Item[] }) {
  const subjects = useMemo(() => [...new Set(items.map((i) => i.subject))], [items]);
  const [tab, setTab] = useState<SubjectKey>(subjects[0]);
  const list = items.filter((i) => i.subject === tab);
  const accent = SUBJECT[tab].color;

  return (
    <div>
      <div role="tablist" aria-label="Subjects" className="flex w-fit flex-wrap gap-1 rounded-full border border-line bg-white p-1">
        {subjects.map((s) => (
          <button
            key={s}
            role="tab"
            aria-selected={tab === s}
            onPointerDown={() => setTab(s)}
            onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && setTab(s)}
            className={["pressable rounded-full px-4 py-2 text-sm transition-colors", tab === s ? "bg-ink text-white" : "text-ink-soft hover:bg-paper-deep"].join(" ")}
          >
            {SUBJECT[s].short} <span className={tab === s ? "text-white/60" : "text-faint"}>{items.filter((i) => i.subject === s).length}</span>
          </button>
        ))}
      </div>

      <div key={tab} className="fade-in mt-10 grid gap-12 lg:grid-cols-[240px_1fr]">
        <nav aria-label="Cards" className="lg:sticky lg:top-24 lg:self-start">
          <div className="eyebrow mb-3">{SUBJECT[tab].label}</div>
          <ol className="space-y-1 text-sm">
            {list.map((i) => (
              <li key={i.card.id}>
                <a href={`#${i.card.id}`} className="pressable block rounded-lg px-2 py-1.5 text-ink-soft hover:bg-paper-deep hover:text-ink">
                  {i.card.title}
                </a>
              </li>
            ))}
          </ol>
        </nav>

        <div className="space-y-16">
          {list.map((i) => (
            <article key={i.card.id} id={i.card.id} className="scroll-mt-24">
              <MemoryCard
                step={i.card}
                accent={accent}
                heading={
                  <div>
                    <Link href={`/topic/${i.topicId}/${i.step}`} className="eyebrow hover:text-ink" style={{ color: accent }}>
                      {i.topicTitle} →
                    </Link>
                    <h2 className="display mt-2 text-[36px]">{i.card.title}</h2>
                  </div>
                }
              />
            </article>
          ))}
        </div>
      </div>
    </div>
  );
}
