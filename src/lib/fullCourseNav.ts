import "server-only";

import type { CourseTopic, VideoSource } from "./fullCourseTypes";
import type { StepListSection } from "@/components/learn/StepList";

/** Outline labels for a topic's steps (never includes answers). */
export function buildStepList(topic: CourseTopic, manifest: Record<string, VideoSource>): StepListSection[] {
  let index = 0;
  return topic.sections.map((s) => {
    let practiceNo = 0;
    return {
      title: s.title,
      kind: s.kind,
      items: s.steps.map((st) => {
        const i = index++;
        if (st.kind === "video")
          return {
            index: i,
            kind: "video" as const,
            id: st.id,
            label: st.solution ? "Worked solution" : st.title,
            soon: !manifest[st.id],
            minutes: st.minutes,
            solution: !!st.solution,
          };
        if (st.kind === "card") return { index: i, kind: "card" as const, id: st.id, label: st.title };
        if (s.kind === "practice")
          return { index: i, kind: "question" as const, id: st.id, label: `Question ${++practiceNo}`, n: practiceNo, group: st.group };
        return { index: i, kind: "question" as const, id: st.id, label: st.number ? `Question ${st.number}` : "Try this question" };
      }),
    };
  });
}
