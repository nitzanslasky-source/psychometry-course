import "server-only";

import type { CourseTopic, VideoSource } from "./fullCourseTypes";
import type { StepListSection } from "@/components/learn/StepList";

/** Short outline label for a step (never includes answers). */
export function buildStepList(topic: CourseTopic, manifest: Record<string, VideoSource>): StepListSection[] {
  let index = 0;
  let practiceNo = 0;
  return topic.sections.map((s) => ({
    title: s.title,
    kind: s.kind,
    items: s.steps.map((st) => {
      const i = index++;
      if (st.kind === "video")
        return { index: i, kind: "video" as const, id: st.id, label: st.title, soon: !manifest[st.id] };
      if (st.kind === "card") return { index: i, kind: "card" as const, id: st.id, label: st.title };
      const label =
        s.kind === "practice"
          ? `Question ${++practiceNo}`
          : st.number
            ? `Question ${st.number} — try it`
            : "Try this question";
      return { index: i, kind: "question" as const, id: st.id, label, group: st.group };
    }),
  }));
}
