import type { SubjectKey } from "./fullCourseTypes";

/** Display identity per subject. Colours are used as small markers only. */
export const SUBJECT: Record<SubjectKey, { label: string; short: string; color: string; blurb: string }> = {
  algebra: {
    label: "Algebra",
    short: "Algebra",
    color: "#3d5a99",
    blurb: "Numbers, fractions, expressions, equations, powers and roots — the language every question is written in.",
  },
  "word-problems": {
    label: "Word Problems",
    short: "Word Problems",
    color: "#2f7d74",
    blurb: "Turning text into equations: ratios, percentages, rates, motion, counting and probability.",
  },
  geometry: {
    label: "Geometry",
    short: "Geometry",
    color: "#b0662b",
    blurb: "Angles, triangles, quadrilaterals, circles, solids, similarity and the coordinate plane.",
  },
  verbal: {
    label: "Verbal Reasoning",
    short: "Verbal",
    color: "#8a4a6b",
    blurb: "Analogies, sentence completion, logic, arguments, research questions and reading comprehension.",
  },
};

export const pad2 = (n: number) => String(n).padStart(2, "0");
