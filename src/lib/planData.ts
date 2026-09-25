import "server-only";

import { flattenSteps, getOutline, getTopic } from "./fullCourse";
import { listSimulationSections } from "./content";

/** One step in course order, with an estimate of how long it takes (minutes). */
export interface PlanStep {
  id: string;
  t: number; // topic id
  n: number; // 1-based step number in the topic (for the link)
  k: "v" | "q" | "p" | "c"; // lesson video · question/solution · practice question · rules card
  m: number;
}
export interface PlanTopic {
  id: number;
  title: string;
  subject: string;
}

/**
 * The study order: the quantitative topics in course order, with the verbal topics woven in evenly,
 * so a student works on both every week (as in a real prep course) instead of all verbal at the end.
 */
export function getPlanData() {
  const subs = getOutline().subjects;
  const quant = subs.filter((s) => s.key !== "verbal").flatMap((s) => s.topics.map((t) => ({ t, subject: s.key })));
  const verbal = subs.filter((s) => s.key === "verbal").flatMap((s) => s.topics.map((t) => ({ t, subject: s.key })));
  const order: typeof quant = [];
  const every = quant.length / Math.max(1, verbal.length);
  let vi = 0;
  quant.forEach((q, i) => {
    order.push(q);
    if (vi < verbal.length && i + 1 >= Math.round((vi + 1) * every)) order.push(verbal[vi++]);
  });
  while (vi < verbal.length) order.push(verbal[vi++]);

  const topics: PlanTopic[] = [];
  const steps: PlanStep[] = [];
  for (const { t, subject } of order) {
    const topic = getTopic(t.id);
    if (!topic) continue;
    topics.push({ id: t.id, title: t.title, subject });
    flattenSteps(topic).forEach(({ step, sectionIndex }, i) => {
      const practice = topic.sections[sectionIndex].kind === "practice";
      const k: PlanStep["k"] = step.kind === "video" ? (step.solution ? "q" : "v") : step.kind === "card" ? "c" : practice ? "p" : "q";
      const m =
        step.kind === "video" ? Math.max(2, Math.round((step.minutes || 3) * 1.4) + 1) : step.kind === "card" ? 3 : practice ? 1.5 : 2;
      steps.push({ id: step.id, t: t.id, n: i + 1, k, m });
    });
  }
  const sims = listSimulationSections().map((r) => ({
    id: r.section.section_id,
    label: `${r.exam.source_exam_label.replace(/ Psychometric.*$/i, "")} · Section ${r.section.position}`,
  }));
  return { topics, steps, sims: sims.reverse() };
}
