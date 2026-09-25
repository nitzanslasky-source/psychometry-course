import { getOutline, getTopic, getVideoManifest, flattenSteps } from "@/lib/fullCourse";
import { LearnHome } from "@/components/learn/LearnHome";

export const metadata = { title: "Psychometry — the complete course" };
export const dynamic = "force-dynamic";

export default function HomePage() {
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
  const all = outline.subjects.flatMap((s) => s.topics);
  const totals = {
    videos: all.reduce((n, t) => n + t.videos, 0),
    lessons: all.reduce((n, t) => n + t.lessons, 0),
    questions: all.reduce((n, t) => n + t.questions, 0),
    topics: all.length,
    // scripts are timed at a reading pace; recorded lessons run ~40% longer
    hours: Math.round((all.reduce((n, t) => n + t.minutes, 0) * 1.4) / 60),
  };

  return (
    <main>
      <LearnHome outline={outline} stepIds={stepIds} recorded={recorded} totals={totals} />
    </main>
  );
}
