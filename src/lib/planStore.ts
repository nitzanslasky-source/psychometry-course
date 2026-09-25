"use client";

/** The student's study-plan settings (the plan itself is recalculated every day from what's left). */
export interface PlanSettings {
  exam: string; // YYYY-MM-DD
  days: number[]; // study weekdays, 0 = Sunday
  minutes: number; // per study day
}
const KEY = "plan.v1";

export function loadPlan(): PlanSettings | null {
  if (typeof window === "undefined") return null;
  try {
    return JSON.parse(localStorage.getItem(KEY) || "null");
  } catch {
    return null;
  }
}
export function savePlan(p: PlanSettings | null) {
  try {
    if (p) localStorage.setItem(KEY, JSON.stringify(p));
    else localStorage.removeItem(KEY);
    window.dispatchEvent(new Event("progress-change"));
  } catch {}
}
