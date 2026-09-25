"use client";

import { useEffect, useState } from "react";
import { srsAdd, srsHas, srsRemove } from "@/lib/srs";

/** Toggle a word or rules card in the student's spaced review. */
export function AddToReview({ srsKey, compact }: { srsKey: string; compact?: boolean }) {
  const [on, setOn] = useState(false);
  useEffect(() => {
    const sync = () => setOn(srsHas(srsKey));
    sync();
    window.addEventListener("srs-change", sync);
    return () => window.removeEventListener("srs-change", sync);
  }, [srsKey]);
  return (
    <button
      type="button"
      aria-pressed={on}
      title={on ? "In your review — click to remove" : "Add to your spaced review"}
      onPointerDown={() => (on ? srsRemove(srsKey) : srsAdd(srsKey))}
      className={[
        "pressable inline-flex shrink-0 items-center gap-1.5 rounded-full border text-xs transition-colors",
        compact ? "h-7 px-2.5" : "px-3 py-1.5",
        on ? "border-ink bg-ink text-white" : "border-line text-muted hover:border-faint hover:text-ink",
      ].join(" ")}
    >
      {on ? "✓ In review" : "+ Review"}
    </button>
  );
}
