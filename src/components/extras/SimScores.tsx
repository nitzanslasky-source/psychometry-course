"use client";

import { useEffect, useState } from "react";
import { loadAttempts } from "@/lib/attemptStore";

/** Best score so far for a simulation section (from the attempts saved on this device). */
export function SimScores({ sectionId }: { sectionId: string }) {
  const [best, setBest] = useState<string | null>(null);
  useEffect(() => {
    const byAttempt = new Map<string, { right: number; total: number }>();
    for (const a of loadAttempts()) {
      if (a.section_id !== sectionId || a.pool !== "simulation") continue;
      const r = byAttempt.get(a.attempt_id) || { right: 0, total: 0 };
      r.total++;
      if (a.is_correct) r.right++;
      byAttempt.set(a.attempt_id, r);
    }
    const all = [...byAttempt.values()];
    if (all.length) {
      const b = all.reduce((x, y) => (y.right > x.right ? y : x));
      setBest(`${b.right}/${b.total}`);
    }
  }, [sectionId]);
  return best ? <span className="text-xs text-gold">{best}</span> : null;
}
