"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { loadProgress } from "@/lib/courseProgressStore";

/** "Start" or "Continue at step n" — picks the first unfinished step. */
export function TopicStart({ topic, stepIds }: { topic: number; stepIds: string[] }) {
  const [next, setNext] = useState<number | null>(null);
  const [doneN, setDoneN] = useState(0);
  useEffect(() => {
    const p = loadProgress();
    const done = stepIds.map((id) => !!p.done[`t${topic}:${id}`]);
    setDoneN(done.filter(Boolean).length);
    const first = done.indexOf(false);
    setNext(first === -1 ? 0 : first);
  }, [topic, stepIds]);
  const started = doneN > 0;
  const pct = Math.round((100 * doneN) / Math.max(1, stepIds.length));

  return (
    <div className="flex flex-col items-start gap-3 md:items-end">
      <Link href={`/topic/${topic}/${(next ?? 0) + 1}`} className="btn px-7 py-3 text-[15px]">
        {started ? (pct === 100 ? "Review the topic" : "Continue") : "Start the topic"} <span aria-hidden>→</span>
      </Link>
      {started && <span className="text-xs text-muted">{pct}% complete</span>}
    </div>
  );
}
