/**
 * Student progress through the full course, kept in localStorage (per device) until accounts land.
 * Keys: "t<topic>:<stepId>" → done; question answers keep the picked choice.
 */
"use client";

import { srsAdd } from "./srs";

const KEY = "fullCourseProgress.v1";

export interface CourseProgress {
  done: Record<string, true>;
  answers: Record<string, number>;
  lastStep?: { topic: number; index: number };
}

export function loadProgress(): CourseProgress {
  if (typeof window === "undefined") return { done: {}, answers: {} };
  try {
    const p = JSON.parse(window.localStorage.getItem(KEY) || "{}");
    return { done: p.done || {}, answers: p.answers || {}, lastStep: p.lastStep };
  } catch {
    return { done: {}, answers: {} };
  }
}

function save(p: CourseProgress) {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(p));
  } catch {
    /* storage full or blocked — progress just isn't kept */
  }
}

export const stepKey = (topic: number, stepId: string) => `t${topic}:${stepId}`;

export function markDone(topic: number, stepId: string) {
  const p = loadProgress();
  p.done[stepKey(topic, stepId)] = true;
  save(p);
}

/** Save a course answer. A wrong answer goes into spaced review (and "My mistakes"). */
export function recordAnswer(topic: number, stepId: string, choice: number, correct?: number) {
  if (correct !== undefined) {
    const key = `q:${topic}:${stepId}`;
    if (choice !== correct) srsAdd(key, { again: true });
  }
  const p = loadProgress();
  p.answers[stepKey(topic, stepId)] = choice;
  p.done[stepKey(topic, stepId)] = true;
  save(p);
}

export function setLastStep(topic: number, index: number) {
  const p = loadProgress();
  p.lastStep = { topic, index };
  save(p);
}

export function doneCount(p: CourseProgress, topic: number, stepIds: string[]) {
  return stepIds.reduce((n, id) => n + (p.done[stepKey(topic, id)] ? 1 : 0), 0);
}
