/**
 * Single data-access seam for question content.
 *
 * Backed by validated JSON files today. When Supabase lands, only the bodies of
 * these functions change — the JSON already matches the DB data model, so callers
 * (pages/components) need no edits. Keep all content reads going through here.
 */
import "server-only";

import winter2019 from "../../content/simulation/psychometric_winter_2019_quant.json";
import spring2019 from "../../content/simulation/psychometric_spring_2019_quant.json";
import spring2020 from "../../content/simulation/psychometric_spring_2020_quant.json";
import autumn2020 from "../../content/simulation/psychometric_autumn_2020_quant.json";
import winter2020 from "../../content/simulation/psychometric_winter_2020_quant.json";
import spring2021 from "../../content/simulation/psychometric_spring_2021_quant.json";
import autumn2021 from "../../content/simulation/psychometric_autumn_2021_quant.json";
import winter2022 from "../../content/simulation/psychometric_winter_2022_quant.json";
import autumn2022 from "../../content/simulation/psychometric_autumn_2022_quant.json";
import winter2023 from "../../content/simulation/psychometric_winter_2023_quant.json";
import spring2023 from "../../content/simulation/psychometric_spring_2023_quant.json";
import autumn2023 from "../../content/simulation/psychometric_autumn_2023_quant.json";
import winter2024 from "../../content/simulation/psychometric_winter_2024_quant.json";
import spring2024 from "../../content/simulation/psychometric_spring_2024_quant.json";
import autumn2024 from "../../content/simulation/psychometric_autumn_2024_quant.json";
import spring2025 from "../../content/simulation/psychometric_spring_2025_quant.json";
import winter2025 from "../../content/simulation/psychometric_winter_2025_quant.json";
import autumn2025 from "../../content/simulation/psychometric_autumn_2025_quant.json";
import spring2026 from "../../content/simulation/psychometric_spring_2026_quant.json";
import type { Exam, Pool, Question, SectionWithQuestions } from "./types";
import type { SolutionMethod } from "./quizTypes";

// Chronological, matching the order sections are listed to the student.
const EXAMS: Exam[] = [
  winter2019 as unknown as Exam,
  spring2019 as unknown as Exam,
  winter2020 as unknown as Exam,
  spring2020 as unknown as Exam,
  autumn2020 as unknown as Exam,
  spring2021 as unknown as Exam,
  autumn2021 as unknown as Exam,
  winter2022 as unknown as Exam,
  autumn2022 as unknown as Exam,
  winter2023 as unknown as Exam,
  spring2023 as unknown as Exam,
  autumn2023 as unknown as Exam,
  winter2024 as unknown as Exam,
  spring2024 as unknown as Exam,
  autumn2024 as unknown as Exam,
  winter2025 as unknown as Exam,
  spring2025 as unknown as Exam,
  autumn2025 as unknown as Exam,
  spring2026 as unknown as Exam,
];

function byPool(questions: Question[], pool: Pool): Question[] {
  return questions.filter((q) => q.pool === pool);
}

export function listExams(): Exam[] {
  return EXAMS;
}

/**
 * Sections available for Mode B. Simulation pool only — drill questions must
 * never appear here, and vice versa.
 */
export function listSimulationSections(): {
  exam: Exam;
  section: Exam["sections"][number];
  count: number;
}[] {
  const out: { exam: Exam; section: Exam["sections"][number]; count: number }[] = [];
  for (const exam of EXAMS) {
    for (const section of [...exam.sections].sort((a, b) => a.position - b.position)) {
      const count = byPool(exam.questions, "simulation").filter(
        (q) => q.section_id === section.section_id,
      ).length;
      if (count > 0) out.push({ exam, section, count });
    }
  }
  return out;
}

/**
 * One full section in original exam order — never shuffled. Section simulations
 * present the untouched section exactly as it was administered.
 *
 * `correct_answer` and `methods` are both STRIPPED here: this payload is serialized
 * into the client bundle, so shipping either would let a student read every answer
 * from view-source mid-simulation — a worked solution gives the answer away just as
 * surely as the key does. Grading happens in the `gradeSection` server action, which
 * returns both once the section is submitted.
 */
export function getSimulationSection(sectionId: string): SectionWithQuestions | null {
  for (const exam of EXAMS) {
    const section = exam.sections.find((s) => s.section_id === sectionId);
    if (!section) continue;
    const questions = byPool(exam.questions, "simulation")
      .filter((q) => q.section_id === sectionId)
      .sort((a, b) => a.position_in_section - b.position_in_section)
      .map(({ correct_answer: _key, methods: _solutions, ...rest }) => rest as Question);
    if (questions.length === 0) return null;
    return {
      exam: {
        source_exam: exam.source_exam,
        source_exam_label: exam.source_exam_label,
        boilerplate: exam.boilerplate,
      },
      section,
      questions,
    };
  }
  return null;
}

/** Answer key for grading, kept server-side so it is not shipped with the questions. */
export function getAnswerKey(sectionId: string): Record<string, number> {
  const key: Record<string, number> = {};
  for (const exam of EXAMS) {
    for (const q of exam.questions) {
      // Reads the raw JSON, which always carries the key (unlike client payloads).
      // Questions NITE voided after the sitting are omitted, so they are neither
      // scored nor counted in the total (see Question.cancelled).
      if (q.cancelled) continue;
      if (q.section_id === sectionId && q.correct_answer !== undefined) {
        key[q.id] = q.correct_answer;
      }
    }
  }
  return key;
}

/**
 * Worked solutions for a section, kept server-side alongside the answer key so they
 * are not shipped with the questions. Returned by `gradeSection` after submission.
 */
export function getSectionMethods(sectionId: string): Record<string, SolutionMethod[]> {
  const out: Record<string, SolutionMethod[]> = {};
  for (const exam of EXAMS) {
    for (const q of exam.questions) {
      if (q.section_id === sectionId && q.methods?.length) {
        out[q.id] = q.methods;
      }
    }
  }
  return out;
}

/** Drill pool — wired up in Mode A once the topic taxonomy is supplied. */
export function listDrillTopics(): { topic: string; subtopic: string; count: number }[] {
  const counts = new Map<string, { topic: string; subtopic: string; count: number }>();
  for (const exam of EXAMS) {
    for (const q of byPool(exam.questions, "drill")) {
      const k = `${q.topic}\u0000${q.subtopic}`;
      const hit = counts.get(k);
      if (hit) hit.count += 1;
      else counts.set(k, { topic: q.topic, subtopic: q.subtopic, count: 1 });
    }
  }
  return [...counts.values()];
}
