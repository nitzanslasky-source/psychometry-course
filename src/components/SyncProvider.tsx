"use client";

import { useEffect } from "react";
import { supabaseBrowser } from "@/lib/supabase/client";

/**
 * Keeps a student's progress in their account, so it follows them to every device.
 * Local storage stays the fast working copy; this merges it with the account on login and
 * saves changes back a couple of seconds after they happen.
 */
const K = { progress: "fullCourseProgress.v1", srs: "srs.v1", attempts: "nite_attempts_v1" } as const;
const OWNER = "sync.owner";
const read = (k: string, empty: unknown) => {
  try {
    return JSON.parse(localStorage.getItem(k) || "null") ?? empty;
  } catch {
    return empty;
  }
};

type Progress = { done?: Record<string, true>; answers?: Record<string, number>; lastStep?: unknown };
type Srs = Record<string, { due: number }>;
type Attempt = { attempt_id: string; question_id: string };

function merge(local: { progress: Progress; srs: Srs; attempts: Attempt[] }, remote: { progress: Progress; srs: Srs; attempts: Attempt[] }) {
  const progress: Progress = {
    done: { ...(remote.progress.done || {}), ...(local.progress.done || {}) },
    answers: { ...(remote.progress.answers || {}), ...(local.progress.answers || {}) },
    lastStep: local.progress.lastStep ?? remote.progress.lastStep,
  };
  const srs: Srs = { ...remote.srs };
  for (const [k, v] of Object.entries(local.srs)) if (!srs[k] || v.due >= srs[k].due) srs[k] = v; // the later schedule wins
  const seen = new Set<string>();
  const attempts = [...remote.attempts, ...local.attempts].filter((a) => {
    const id = a.attempt_id + "|" + a.question_id;
    if (seen.has(id)) return false;
    seen.add(id);
    return true;
  });
  return { progress, srs, attempts };
}

export function SyncProvider() {
  useEffect(() => {
    const sb = supabaseBrowser();
    if (!sb) return;
    let userId: string | null = null;
    let timer: ReturnType<typeof setTimeout> | null = null;

    const local = () => ({ progress: read(K.progress, {}), srs: read(K.srs, {}), attempts: read(K.attempts, []) });
    const push = () => {
      if (!userId) return;
      if (timer) clearTimeout(timer);
      timer = setTimeout(async () => {
        const s = local();
        await sb.from("student_state").upsert({ user_id: userId, ...s, updated_at: new Date().toISOString() });
      }, 2000);
    };

    const start = async () => {
      const { data } = await sb.auth.getUser();
      const user = data.user;
      if (!user) {
        // logged out on this device: don't leave the previous student's work behind
        if (localStorage.getItem(OWNER)) {
          Object.values(K).forEach((k) => localStorage.removeItem(k));
          localStorage.removeItem(OWNER);
        }
        return;
      }
      userId = user.id;
      const prevOwner = localStorage.getItem(OWNER);
      const mine = !prevOwner || prevOwner === user.id ? local() : { progress: {}, srs: {}, attempts: [] };
      const { data: row } = await sb.from("student_state").select("progress,srs,attempts").eq("user_id", user.id).maybeSingle();
      const merged = merge(mine, { progress: row?.progress || {}, srs: row?.srs || {}, attempts: row?.attempts || [] });
      const before = JSON.stringify(local());
      localStorage.setItem(K.progress, JSON.stringify(merged.progress));
      localStorage.setItem(K.srs, JSON.stringify(merged.srs));
      localStorage.setItem(K.attempts, JSON.stringify(merged.attempts));
      localStorage.setItem(OWNER, user.id);
      await sb.from("student_state").upsert({ user_id: user.id, ...merged, updated_at: new Date().toISOString() });
      // first sync on a new device brought work in: reload once so every screen shows it
      if (before !== JSON.stringify(local()) && !sessionStorage.getItem("sync.reloaded")) {
        sessionStorage.setItem("sync.reloaded", "1");
        location.reload();
      }
    };

    void start();
    const events = ["progress-change", "srs-change", "attempts-change"];
    events.forEach((e) => window.addEventListener(e, push));
    const { data: sub } = sb.auth.onAuthStateChange((ev: string) => {
      if (ev === "SIGNED_IN") void start();
      if (ev === "SIGNED_OUT") {
        Object.values(K).forEach((k) => localStorage.removeItem(k));
        localStorage.removeItem(OWNER);
        userId = null;
      }
    });
    return () => {
      events.forEach((e) => window.removeEventListener(e, push));
      sub.subscription.unsubscribe();
      if (timer) clearTimeout(timer);
    };
  }, []);
  return null;
}
