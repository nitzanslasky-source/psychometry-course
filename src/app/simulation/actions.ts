"use server";

import { getAnswerKey, getSectionMethods } from "@/lib/content";
import type { SolutionMethod } from "@/lib/quizTypes";

/**
 * Grades a submitted section server-side.
 *
 * The answer key and the worked solutions are deliberately NOT included in the
 * question payload sent to the browser: otherwise a student could read every answer
 * from view-source during a timed simulation. Both cross the wire only after the
 * section is submitted.
 */
export async function gradeSection(
  sectionId: string,
  answers: Record<string, number>,
): Promise<{
  key: Record<string, number>;
  methods: Record<string, SolutionMethod[]>;
  score: number;
  total: number;
}> {
  const key = getAnswerKey(sectionId);
  const ids = Object.keys(key);
  const score = ids.filter((id) => answers[id] === key[id]).length;
  return { key, methods: getSectionMethods(sectionId), score, total: ids.length };
}
