import { notFound } from "next/navigation";
import { flattenSteps, getTopic, getVideoManifest } from "@/lib/fullCourse";
import { buildStepList } from "@/lib/fullCourseNav";
import { StepView } from "@/components/learn/StepView";
import { SUBJECT } from "@/lib/subjects";
import { videoEmbed } from "@/lib/video";

export const dynamic = "force-dynamic";

export default async function StepPage({ params }: { params: Promise<{ topic: string; step: string }> }) {
  const { topic: rawT, step: rawS } = await params;
  const topic = getTopic(Number(rawT));
  if (!topic) notFound();
  const all = flattenSteps(topic);
  const index = Number(rawS) - 1;
  if (!Number.isInteger(index) || index < 0 || index >= all.length) notFound();

  const manifest = getVideoManifest();
  const { step, sectionIndex } = all[index];
  const sections = buildStepList(topic, manifest);
  const item = sections.flatMap((s) => s.items).find((x) => x.index === index)!;
  const section = topic.sections[sectionIndex];
  const next = all[index + 1]?.step;
  const subj = SUBJECT[topic.subject];

  const label =
    step.kind === "video"
      ? step.solution
        ? `Worked solution · ${step.title.replace("Worked solution · ", "")}`
        : "Lesson"
      : step.kind === "card"
        ? "Rules to know by heart"
        : section.kind === "practice"
          ? `Practice · ${item.group ? item.group + " · " : ""}Question ${item.n}`
          : `${item.label} · try it first`;
  const nextLabel =
    step.kind === "question" && next?.kind === "video" && next.solution ? "Watch the solution" : undefined;

  return (
    <main>
      <StepView
        step={step}
        label={label}
        sections={sections}
        video={step.kind === "video" ? videoEmbed(manifest[step.id]) : null}
        passage={step.kind === "question" && step.passageId ? topic.passages[step.passageId] : null}
        nav={{
          topic: topic.id,
          topicTitle: topic.title,
          subjectLabel: subj.label,
          accent: subj.color,
          index,
          total: all.length,
          prevHref: index > 0 ? `/topic/${topic.id}/${index}` : undefined,
          nextHref: index + 1 < all.length ? `/topic/${topic.id}/${index + 2}` : undefined,
          nextLabel,
        }}
      />
    </main>
  );
}
