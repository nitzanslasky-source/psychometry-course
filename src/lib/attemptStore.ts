"use client";

/**
 * Client-only attempt log. The app has no backend today, so this is localStorage-backed;
 * every function guards on `typeof window` so it's safe to import from client components
 * that may render before mount (see AnalyticsDashboard's useEffect-based load).
 */
import type { ErrorReason, QuestionAttempt } from "./types";

const USER_ID_KEY = "nite_user_id";
const ATTEMPTS_KEY = "nite_attempts_v1";

function randomId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) return crypto.randomUUID();
  return `id_${Date.now()}_${Math.random().toString(36).slice(2)}`;
}

export function getOrCreateUserId(): string {
  if (typeof window === "undefined") return "anonymous";
  try {
    const existing = window.localStorage.getItem(USER_ID_KEY);
    if (existing) return existing;
    const id = randomId();
    window.localStorage.setItem(USER_ID_KEY, id);
    return id;
  } catch {
    return "anonymous";
  }
}

export function loadAttempts(): QuestionAttempt[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = window.localStorage.getItem(ATTEMPTS_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? (parsed as QuestionAttempt[]) : [];
  } catch {
    return [];
  }
}

function saveAttempts(attempts: QuestionAttempt[]): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(ATTEMPTS_KEY, JSON.stringify(attempts));
  } catch {
    // Full or unavailable storage (private browsing, quota) — degrade silently.
  }
}

/** Append-only: a retake adds a fresh batch rather than overwriting prior attempts. */
export function appendAttempts(newAttempts: QuestionAttempt[]): void {
  const current = loadAttempts();
  saveAttempts([...current, ...newAttempts]);
}

export function updateAttemptErrorReason(attemptId: string, reason: ErrorReason): void {
  const current = loadAttempts();
  saveAttempts(
    current.map((a) => (a.attempt_id === attemptId ? { ...a, error_reason: reason } : a)),
  );
}
