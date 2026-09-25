"use client";

import { useEffect, useRef, useState } from "react";

/**
 * Wall-clock countdown. Uses a deadline timestamp rather than accumulating
 * setInterval ticks, so tab throttling or a backgrounded tab cannot inflate the
 * remaining time — important because exam pacing is the whole point of timed mode.
 *
 * In untimed mode the value counts UP as elapsed overtime instead.
 */
export function useCountdown({
  seconds,
  running,
  mode,
  onExpire,
  resetKey,
}: {
  seconds: number;
  running: boolean;
  mode: "timed" | "untimed";
  onExpire?: () => void;
  /** Change this to force a clean restart (e.g. "play again") without remounting. */
  resetKey?: string | number;
}) {
  const [now, setNow] = useState(() => Date.now());
  const startedAt = useRef<number | null>(null);
  const fired = useRef(false);
  const onExpireRef = useRef(onExpire);
  onExpireRef.current = onExpire;
  const prevResetKey = useRef(resetKey);

  useEffect(() => {
    if (resetKey === undefined || resetKey === prevResetKey.current) return;
    prevResetKey.current = resetKey;
    startedAt.current = null;
    fired.current = false;
    setNow(Date.now());
  }, [resetKey]);

  useEffect(() => {
    if (!running) return;
    if (startedAt.current === null) startedAt.current = Date.now();
    const id = window.setInterval(() => setNow(Date.now()), 250);
    return () => window.clearInterval(id);
  }, [running]);

  const elapsed = startedAt.current === null ? 0 : Math.floor((now - startedAt.current) / 1000);
  const remaining = Math.max(0, seconds - elapsed);

  useEffect(() => {
    if (!running || mode !== "timed" || fired.current) return;
    if (remaining === 0 && startedAt.current !== null) {
      fired.current = true;
      onExpireRef.current?.();
    }
  }, [remaining, running, mode]);

  return {
    /** Seconds left in timed mode; seconds of overtime in untimed mode. */
    value: mode === "timed" ? remaining : elapsed,
    elapsed,
    remaining,
    overtime: mode === "untimed" && elapsed > seconds,
  };
}

export function formatClock(totalSeconds: number): string {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}
