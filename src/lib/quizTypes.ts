/** Solution-method labels for exam questions (copied from the elite project). */
export const METHOD_KINDS = {
  algebra: "Algebra",
  "plug-in": "Plug in numbers",
  "check-answers": "Check the answers",
  structure: "Structure",
  understanding: "Understanding",
} as const;

export type MethodKind = keyof typeof METHOD_KINDS;

export interface SolutionMethod {
  kind: MethodKind;
  text: string;
}
