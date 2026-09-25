import type { SolutionMethod } from "./quizTypes";

/** Question pools must never overlap: a question seen in drills would spoil a simulation. */
export type Pool = "simulation" | "drill";

export type Difficulty = "easy" | "medium" | "hard";


export interface Question {
  id: string;
  source_exam: string;
  source_question_number: number;
  section_id: string;
  position_in_section: number;
  pool: Pool;
  /** Domain title and subcategory name from QUANTITATIVE_TAXONOMY — kept as display
   *  strings so existing renders (PostSectionReviewSheet, etc.) need no changes. */
  topic: string;
  subtopic: string;
  /** SubCategory.id from src/lib/categories.ts — the join key back to practice mode. */
  sub_category_id: string;
  difficulty: Difficulty;
  /** May contain MathJax `\(...\)` and `\n\n` breaks before the final question sentence. */
  stem: string;
  options: string[];
  /**
   * 1-based, matching the official NITE answer key. Absent on payloads sent to the
   * browser for simulations — the key is withheld until the section is graded
   * server-side, so it cannot be read from view-source during the attempt.
   */
  correct_answer?: number;
  /**
   * Worked solutions, each labelled with the KIND of reasoning it uses. Absent on
   * payloads sent to the browser for simulations, for the same reason as
   * `correct_answer`: a solution gives the answer away just as effectively as the
   * key does. They cross the wire only after the section is graded.
   */
  methods?: SolutionMethod[];
  figure_paths?: string[];
  /** Set when the options themselves are images (e.g. "which graph describes..."). */
  option_figure_paths?: string[];
  cluster?: string;
  /**
   * NITE voided this question after the exam was administered — the printed page
   * carries a diagonal `השאלה בוטלה` overprint. It is kept in the corpus for
   * fidelity but excluded from scoring, since counting it would cost a student a
   * mark on an item that was not scored in the real sitting. Only known instance:
   * Spring 2024 §1 Q17.
   */
  cancelled?: boolean;
}

export type ClusterType = "questions_and_problems" | "graph_comprehension" | "table_comprehension";

export interface Cluster {
  type: ClusterType;
  header: string;
  from: number;
  to: number;
  intro?: string;
  figure_path?: string;
  /**
   * Second piece of shared artwork, when the cluster's data is split across two
   * images (Autumn 2020 §1: main table + fuel-price table; §2: line graph + the
   * two pie charts).
   */
  secondary_figure_path?: string;
  /**
   * Editorial gloss added by this project, NOT text from the exam. Kept out of
   * `intro` so official wording stays verbatim, and rendered visibly marked as a
   * translator's note. Used where a puzzle's premise depends on Hebrew
   * orthography — e.g. Autumn 2022 §2 transliterates the letters א-י to A-J.
   */
  translator_note?: string;
}

export interface Section {
  section_id: string;
  title: string;
  position: number;
  clusters: Cluster[];
}

export interface Boilerplate {
  section_intro: string;
  section_meta: string;
  gray_note: string;
  general_comments_title: string;
  general_comments: string[];
  graph_comprehension_lead: string;
  graph_comprehension_lead_five: string;
  graph_disregard_note: string;
  questions_heading: string;
}

export interface Exam {
  source_exam: string;
  source_exam_label: string;
  language: string;
  translated_from: string;
  answer_key_source: string;
  boilerplate: Boilerplate;
  sections: Section[];
  questions: Question[];
}

/** A section plus its questions, ready to render. */
export interface SectionWithQuestions {
  exam: Pick<Exam, "source_exam" | "source_exam_label" | "boilerplate">;
  section: Section;
  questions: Question[];
}

/** Per-section timing rules. NITE allots 20 minutes for 20 quantitative questions. */
export const SECTION_SECONDS = 20 * 60;

export type SubmissionType = "SUBMITTED" | "SKIPPED_UNATTEMPTED" | "TIMED_OUT_GUESS";

export type ErrorReason =
  | "CALCULATION_ERROR"
  | "MISREAD_STEM"
  | "CONCEPT_DEFICIT"
  | "TIME_CRUNCH"
  | "LUCKY_GUESS";

export const ERROR_REASONS: ErrorReason[] = [
  "CALCULATION_ERROR",
  "MISREAD_STEM",
  "CONCEPT_DEFICIT",
  "TIME_CRUNCH",
  "LUCKY_GUESS",
];

/**
 * One record per question per section attempt. Logged client-side (no backend today —
 * see attemptStore.ts) so a student can see sub-topic mastery and pacing across sessions.
 */
export interface QuestionAttempt {
  attempt_id: string;
  user_id: string;
  pool: Pool;
  section_id: string;
  question_id: string;
  topic: string;
  subtopic: string;
  sub_category_id: string;
  submission_type: SubmissionType;
  time_spent_seconds: number;
  /** 1-based; null only when submission_type is SKIPPED_UNATTEMPTED. */
  user_choice: number | null;
  /** 1-based, from the graded answer key. */
  correct_choice: number;
  /** Raw correctness — never adjusted by is_flagged. Section scores must read this, not analytics. */
  is_correct: boolean;
  is_flagged: boolean;
  error_reason: ErrorReason | null;
  attempted_at: string;
}
