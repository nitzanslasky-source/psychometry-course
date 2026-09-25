"use client";

import { useEffect, useState } from "react";

/** Client-only reading-comfort preference — mirrors bookmarkStore.ts's pattern. A global
 *  toggle (not per-question) so it behaves like the dark-mode setting: set once, applies
 *  everywhere text/figures are shown during practice or simulation. */

const COMPACT_KEY = "nite_compact_mode_v1";

export function isCompactMode(): boolean {
  if (typeof window === "undefined") return false;
  return window.localStorage.getItem(COMPACT_KEY) === "1";
}

export function setCompactMode(value: boolean): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(COMPACT_KEY, value ? "1" : "0");
  window.dispatchEvent(new Event("compact-mode-change"));
}

/** Reads the preference post-mount (avoids a server/client hydration mismatch, same reason
 *  BatchList's completion state loads in an effect) and stays in sync if toggled elsewhere
 *  on the page (e.g. the header control) via the same event setCompactMode dispatches. */
export function useCompactMode(): boolean {
  const [compact, setCompact] = useState(false);
  useEffect(() => {
    setCompact(isCompactMode());
    const onChange = () => setCompact(isCompactMode());
    window.addEventListener("compact-mode-change", onChange);
    return () => window.removeEventListener("compact-mode-change", onChange);
  }, []);
  return compact;
}
