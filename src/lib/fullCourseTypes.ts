/**
 * The full recorded course (exported from the Teacher Studio by studio-build/export_student.py).
 * Student-facing only: no scripts, slides or teacher notes ever reach this data.
 */

export type SubjectKey = "algebra" | "word-problems" | "geometry" | "verbal";

export interface CourseVideoStep {
  kind: "video";
  id: string;
  title: string;
  minutes?: number;
  /** True for a worked-solution video that follows its question. */
  solution?: boolean;
  questionId?: string;
}

export interface CourseQuestionStep {
  kind: "question";
  id: string;
  /** MathJax \( \) delimiters. */
  stem: string;
  choices: string[];
  /** 0-based. */
  correct: number;
  explanation: string[];
  /** Guided question number within its topic (locked; matches the recorded video). */
  number?: number;
  figure?: string;
  passageId?: string;
  group?: string;
  instructions?: string;
}

export interface CourseCardStep {
  kind: "card";
  id: string;
  title: string;
  intro: string;
  tables: { title: string; head: string[]; rows: string[][] }[];
  tips: string[];
}

export type CourseStep = CourseVideoStep | CourseQuestionStep | CourseCardStep;

export interface CourseSection {
  id: string;
  title: string;
  kind: "learn" | "practice" | string;
  steps: CourseStep[];
}

export interface CourseTopic {
  id: number;
  title: string;
  subject: SubjectKey;
  sections: CourseSection[];
  passages: Record<string, { title: string; paragraphs: string[] }>;
}

export interface OutlineTopic {
  id: number;
  title: string;
  videos: number;
  questions: number;
  minutes: number;
  steps: number;
}

export interface CourseOutline {
  subjects: { key: SubjectKey; title: string; topics: OutlineTopic[] }[];
}

/** Where a recorded video is hosted. A video id missing from the manifest = not recorded yet. */
export type VideoSource =
  | { provider: "bunny"; libraryId: string; videoGuid: string }
  | { provider: "url"; url: string };
