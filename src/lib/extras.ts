import "server-only";

import fs from "node:fs";
import path from "node:path";
import { getOutline, getTopic } from "./fullCourse";
import type { CourseCardStep, SubjectKey } from "./fullCourseTypes";

const DIR = path.join(process.cwd(), "content", "full-course");

export type DictLabel = "EXAM ANALOGY" | "EXAM VOCABULARY" | "ADDITIONAL WORD" | "ANALOGY PRACTICE" | "READING";

export interface DictEntry {
  w: string;
  label: DictLabel;
  /** Plain-English definition. */
  def: string;
  /** Example sentence. */
  ex: string;
  /** A short tip: contrast, related form, analogy pairing. */
  note?: string;
  /** From the core "Psychometric Vocabulary" list. */
  core?: boolean;
}

export function getDictionary(): DictEntry[] {
  return JSON.parse(fs.readFileSync(path.join(DIR, "dictionary.json"), "utf8")) as DictEntry[];
}

export interface CardWithPlace {
  card: CourseCardStep;
  topicId: number;
  topicTitle: string;
  subject: SubjectKey;
  /** 1-based step number of the card inside its topic. */
  step: number;
}

/** Every "rules to know" card in course order. */
export function getAllCards(): CardWithPlace[] {
  const out: CardWithPlace[] = [];
  for (const s of getOutline().subjects)
    for (const t of s.topics) {
      const topic = getTopic(t.id);
      if (!topic) continue;
      let n = 0;
      for (const sec of topic.sections)
        for (const st of sec.steps) {
          n++;
          if (st.kind === "card") out.push({ card: st, topicId: t.id, topicTitle: t.title, subject: s.key, step: n });
        }
    }
  return out;
}
