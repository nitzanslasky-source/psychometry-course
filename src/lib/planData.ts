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
 * The study order follows the teacher's Hebrew course schedule (2-month course, day by day): subjects are mixed
 * every day, fundamentals come first, psychometric thinking early, and the writing task is spread over the first
 * two weeks (intro → language → content → planning → argument → rebuttal → opening/closing/structure).
 * [topicId] = the whole topic; [50, "b"] = the writing-task lessons whose ids start with "vr50-b" (with the cards
 * and workshops that follow them). Topics missing from the list are added at the end.
 */
const ORDER: [number, string?][] = [
  [1], [30], [2], [4], [31], [6], [8], [32], [9], [10], [33], // days 1-5: fundamentals
  [51], [50, "a"], // day 6: psychometric thinking, intro to the writing task
  [39], [42], [21], [50, "b"], [50, "c"], // day 8
  [50, "d"], [3], // day 9
  [43], [50, "e"], [50, "f"], // days 10-11
  [50, "g"], [22], // day 12
  [41], [50, "h"], [50, "i"], [5], // day 13
  [7], [44], [23], [11], [24], [49], [12], // days 15-20
  [45], [25], [40], [34], [13], [52], [26], [14], // days 22-26 (charts: day 24)
  [46], [35], [15], [47], [27], [16], [17], // days 29-33
  [36], [18], [28], [48], [37], [19], // days 36-40
  [20], [29], [38], // days 43-44
];

export function getPlanData() {
  const subs = getOutline().subjects;
  const all = subs.flatMap((s) => s.topics.map((t) => ({ t, subject: s.key })));
  const byId = new Map(all.map((x) => [x.t.id, x]));
  const listed = new Set(ORDER.map(([id]) => id));
  const order: { t: (typeof all)[number]["t"]; subject: string; part?: string }[] = [];
  for (const [id, part] of ORDER) {
    const x = byId.get(id);
    if (x) order.push({ ...x, part });
  }
  for (const x of all) if (!listed.has(x.t.id)) order.push(x);

  const topics: PlanTopic[] = [];
  const steps: PlanStep[] = [];
  const seen = new Set<number>();
  for (const { t, subject, part } of order) {
    const topic = getTopic(t.id);
    if (!topic) continue;
    if (!seen.has(t.id)) topics.push({ id: t.id, title: t.title, subject });
    seen.add(t.id);
    const flat = flattenSteps(topic);
    let from = 0,
      to = flat.length;
    if (part) {
      // the part runs from its first lesson to the first lesson of the next part of the same topic
      const starts = ORDER.filter(([id, p]) => id === t.id && p).map(([, p]) => p as string);
      const at = (p: string) => flat.findIndex(({ step }) => step.id.startsWith(`vr${t.id}-${p}`));
      from = Math.max(0, at(part));
      const later = starts.slice(starts.indexOf(part) + 1).map(at).filter((k) => k > from);
      to = later.length ? Math.min(...later) : flat.length;
    }
    flat.slice(from, to).forEach(({ step, sectionIndex }, j) => {
      const i = from + j;
      const practice = topic.sections[sectionIndex].kind === "practice";
      const k: PlanStep["k"] = step.kind === "video" ? (step.solution ? "q" : "v") : step.kind === "card" ? "c" : practice ? "p" : "q";
      const m =
        step.kind === "video" ? Math.max(2, Math.round((step.minutes || 3) * 1.4) + 1) : step.kind === "card" ? 3 : practice ? 3 : 2; // practice: solving + checking the answer + reviewing the explanation
      steps.push({ id: step.id, t: t.id, n: i + 1, k, m });
    });
  }
  const sims = listSimulationSections().map((r) => ({
    id: r.section.section_id,
    label: `${r.exam.source_exam_label.replace(/ Psychometric.*$/i, "")} · Section ${r.section.position}`,
  }));
  return { topics, steps, sims: sims.reverse() };
}
