import "server-only";

import { flattenSteps, getOutline, getTopic } from "./fullCourse";
import { getAllCards, getDictionary } from "./extras";
import { listExams } from "./content";
import { METHOD_KINDS } from "./quizTypes";
import type { CourseCardStep } from "./fullCourseTypes";

/** Everything the review screens need to show one item, looked up by its SRS key. */
export type ReviewItem =
  | {
      key: string;
      kind: "q";
      where: string;
      href: string;
      solutionHref?: string;
      stem: string;
      choices: string[];
      correct: number; // 0-based
      explanation: string[];
      figure?: string;
      instructions?: string;
      passage?: { title: string; paragraphs: string[] };
    }
  | {
      key: string;
      kind: "s";
      where: string;
      href: string;
      stem: string;
      choices: string[];
      correct: number; // 0-based
      explanation: string[];
      figures: string[];
      optionFigures?: string[];
    }
  | { key: string; kind: "w"; where: string; w: string; def: string; ex: string; note?: string }
  | { key: string; kind: "c"; where: string; href: string; card: CourseCardStep };

let cache: Map<string, ReviewItem> | null = null;

function build(): Map<string, ReviewItem> {
  const m = new Map<string, ReviewItem>();
  // course questions
  for (const s of getOutline().subjects)
    for (const t of s.topics) {
      const topic = getTopic(t.id);
      if (!topic) continue;
      const all = flattenSteps(topic);
      all.forEach(({ step, sectionIndex }, i) => {
        if (step.kind !== "question") return;
        const next = all[i + 1]?.step;
        const sec = topic.sections[sectionIndex];
        const key = `q:${t.id}:${step.id}`;
        m.set(key, {
          key,
          kind: "q",
          where: `${t.title} · ${sec.kind === "practice" ? "Practice" : step.number ? `Question ${step.number}` : "Lesson question"}`,
          href: `/topic/${t.id}/${i + 1}`,
          solutionHref: next?.kind === "video" && next.solution ? `/topic/${t.id}/${i + 2}` : undefined,
          stem: step.stem,
          choices: step.choices,
          correct: step.correct,
          explanation: step.explanation,
          figure: step.figure,
          instructions: step.instructions,
          passage: step.passageId ? topic.passages[step.passageId] : undefined,
        });
      });
    }
  // exam simulations
  for (const exam of listExams()) {
    const label = exam.source_exam_label.replace(/ Psychometric.*$/i, "");
    for (const q of exam.questions) {
      if (q.cancelled || q.correct_answer === undefined) continue;
      const sec = exam.sections.find((x) => x.section_id === q.section_id);
      const key = `s:${q.id}`;
      m.set(key, {
        key,
        kind: "s",
        where: `${label} · Section ${sec?.position ?? ""} · Question ${q.position_in_section}`,
        href: `/simulation/${q.section_id}`,
        stem: q.stem,
        choices: q.options,
        correct: q.correct_answer - 1,
        explanation: (q.methods || []).map((x) => `${METHOD_KINDS[x.kind] ?? "Solution"}: ${x.text}`),
        figures: (q.figure_paths || []).map((f) => "/" + f.replace(/^\//, "")),
        optionFigures: q.option_figure_paths?.map((f) => "/" + f.replace(/^\//, "")),
      });
    }
  }
  // dictionary
  for (const e of getDictionary()) m.set(`w:${e.w}`, { key: `w:${e.w}`, kind: "w", where: "Dictionary", w: e.w, def: e.def, ex: e.ex, note: e.note });
  // rules cards
  for (const c of getAllCards())
    m.set(`c:${c.card.id}`, { key: `c:${c.card.id}`, kind: "c", where: `Rules · ${c.topicTitle}`, href: `/topic/${c.topicId}/${c.step}`, card: c.card });
  return m;
}

export function getReviewItems(keys: string[]): ReviewItem[] {
  if (!cache) cache = build();
  return keys.map((k) => cache!.get(k)).filter((x): x is ReviewItem => !!x);
}

/** Core-list words, in order — the pool "add new words" draws from. */
export function coreWordKeys(): string[] {
  return getDictionary()
    .filter((e) => e.core)
    .map((e) => `w:${e.w}`);
}
