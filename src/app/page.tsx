import { getOutline, getTopic, getVideoManifest, flattenSteps } from "@/lib/fullCourse";
import { LearnHome } from "@/components/learn/LearnHome";

export const metadata = { title: "Psychometry Course — All topics" };
export const dynamic = "force-dynamic";

export default function LearnPage() {
  const outline = getOutline();
  const manifest = getVideoManifest();
  const stepIds: Record<number, string[]> = {};
  const recorded: Record<number, number> = {};
  for (const s of outline.subjects)
    for (const t of s.topics) {
      const topic = getTopic(t.id);
      if (!topic) continue;
      const steps = flattenSteps(topic).map((x) => x.step);
      stepIds[t.id] = steps.map((x) => x.id);
      recorded[t.id] = steps.filter((x) => x.kind === "video" && manifest[x.id]).length;
    }

  return (
    <main className="mx-auto max-w-5xl px-5 py-10">
      <h1 className="text-4xl font-bold sm:text-5xl">The Full Course</h1>
      <p className="mt-2 max-w-2xl text-sm text-muted dark:text-neutral-400">
        Every topic of the Quantitative and Verbal Reasoning sections, in order: video lessons, guided
        questions with worked-solution videos, rules to know by heart, and practice.
      </p>
      <LearnHome outline={outline} stepIds={stepIds} recorded={recorded} />
    </main>
  );
}
