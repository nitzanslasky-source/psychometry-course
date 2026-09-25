import Link from "next/link";
import { notFound } from "next/navigation";
import { flattenSteps, getTopic, getVideoManifest } from "@/lib/fullCourse";
import { buildStepList } from "@/lib/fullCourseNav";
import { StepList } from "@/components/learn/StepList";
import { StepView } from "@/components/learn/StepView";
import { IconArrowLeft } from "@/components/icons";

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

  const label =
    step.kind === "video"
      ? step.solution ? "Worked solution" : "Video lesson"
      : step.kind === "card"
        ? "Rules to know"
        : section.kind === "practice" ? `Practice · ${item.label}` : item.label.replace(" — try it", "");
  const nextLabel =
    step.kind === "question" && next?.kind === "video" && next.solution ? "Watch the worked solution →" : undefined;

  return (
    <main className="mx-auto grid max-w-6xl gap-8 px-5 py-8 lg:grid-cols-[1fr_300px]">
      <div className="min-w-0">
        <Link href={`/topic/${topic.id}`} className="link-subtle inline-flex items-center gap-1 text-sm">
          <IconArrowLeft width={15} height={15} /> {topic.title}
        </Link>
        <div className="mt-4">
          <StepView
            step={step}
            label={label}
            video={step.kind === "video" ? manifest[step.id] ?? null : null}
            passage={step.kind === "question" && step.passageId ? topic.passages[step.passageId] : null}
            nav={{
              topic: topic.id,
              index,
              total: all.length,
              prevHref: index > 0 ? `/topic/${topic.id}/${index}` : undefined,
              nextHref: index + 1 < all.length ? `/topic/${topic.id}/${index + 2}` : undefined,
              nextLabel,
            }}
          />
        </div>
      </div>
      <aside className="hidden lg:block">
        <div className="surface-card material-panel sticky top-20 max-h-[calc(100vh-6rem)] overflow-y-auto p-4">
          <StepList topic={topic.id} sections={sections} current={index} compact />
        </div>
      </aside>
    </main>
  );
}
