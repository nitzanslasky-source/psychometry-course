import "server-only";

import { flattenSteps, getOutline, getTopic } from "./fullCourse";
import { getDictionary } from "./extras";
import { listSimulationSections } from "./content";
import { SUBJECT } from "./subjects";

export interface SearchDoc {
  /** kind: topic · lesson · question · card · word · exam */
  k: "topic" | "lesson" | "question" | "card" | "word" | "exam";
  t: string; // title
  s: string; // where
  h: string; // href
  x?: string; // extra searchable text
}

const plain = (s: string) =>
  s
    .replace(/\\\(|\\\)/g, "")
    .replace(/\\[a-z]+\{?/gi, " ")
    .replace(/[{}]/g, "")
    .replace(/<[^>]+>/g, "")
    .replace(/\s+/g, " ")
    .trim();

let cache: SearchDoc[] | null = null;

export function getSearchIndex(): SearchDoc[] {
  if (cache) return cache;
  const out: SearchDoc[] = [];
  for (const subj of getOutline().subjects)
    for (const t of subj.topics) {
      const topic = getTopic(t.id);
      if (!topic) continue;
      out.push({ k: "topic", t: t.title, s: SUBJECT[subj.key].label, h: `/topic/${t.id}` });
      let practiceNo = 0;
      flattenSteps(topic).forEach(({ step, sectionIndex }, i) => {
        const h = `/topic/${t.id}/${i + 1}`;
        const practice = topic.sections[sectionIndex].kind === "practice";
        if (step.kind === "video" && !step.solution) out.push({ k: "lesson", t: step.title, s: t.title, h });
        else if (step.kind === "card")
          out.push({
            k: "card",
            t: step.title,
            s: t.title,
            h,
            x: plain([step.intro, ...step.tables.flatMap((tb) => tb.rows.flat()), ...step.tips].join(" ")).slice(0, 600),
          });
        else if (step.kind === "question") {
          const label = practice ? `Practice question ${++practiceNo}` : step.number ? `Question ${step.number}` : "Question";
          out.push({ k: "question", t: `${label} · ${t.title}`, s: plain(step.stem).slice(0, 140), h, x: plain(step.stem).slice(0, 220) });
        }
      });
    }
  for (const e of getDictionary()) out.push({ k: "word", t: e.w, s: e.def, h: `/dictionary?q=${encodeURIComponent(e.w)}` });
  for (const r of listSimulationSections())
    out.push({ k: "exam", t: `${r.exam.source_exam_label.replace(/ Psychometric.*$/i, "")} · Section ${r.section.position}`, s: "Exam simulation", h: `/simulation/${r.section.section_id}` });
  cache = out;
  return out;
}
