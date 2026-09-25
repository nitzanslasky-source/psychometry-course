import Link from "next/link";
import { notFound } from "next/navigation";
import { getOutline, getTopic, getVideoManifest } from "@/lib/fullCourse";
import { buildStepList } from "@/lib/fullCourseNav";
import { StepList } from "@/components/learn/StepList";
import { TopicStart } from "@/components/learn/TopicStart";
import { SUBJECT, pad2 } from "@/lib/subjects";

export const dynamic = "force-dynamic";

export default async function TopicPage({ params }: { params: Promise<{ topic: string }> }) {
  const { topic: raw } = await params;
  const topic = getTopic(Number(raw));
  if (!topic) notFound();
  const manifest = getVideoManifest();
  const sections = buildStepList(topic, manifest);
  const subj = SUBJECT[topic.subject];
  const siblings = getOutline().subjects.find((s) => s.key === topic.subject)!.topics;
  const pos = siblings.findIndex((t) => t.id === topic.id);
  const meta = siblings[pos];
  const prevT = siblings[pos - 1];
  const nextT = siblings[pos + 1];
  const stepIds = sections.flatMap((s) => s.items.map((i) => i.id));
  const lessons = sections.flatMap((s) => s.items).filter((i) => i.kind === "video" && !i.solution).length;

  return (
    <main className="mx-auto max-w-6xl px-6">
      <nav className="pt-8 text-sm text-muted" aria-label="Breadcrumb">
        <Link href="/#contents" className="link">
          Contents
        </Link>
        <span className="mx-2 text-faint">/</span>
        <span>{subj.label}</span>
      </nav>

      <header className="rise-in grid gap-10 border-b border-line pb-12 pt-10 md:grid-cols-[1fr_auto] md:items-end">
        <div>
          <div className="flex items-baseline gap-4">
            <span className="display text-[64px]" style={{ color: subj.color }}>
              {pad2(pos + 1)}
            </span>
            <span className="eyebrow">{subj.label}</span>
          </div>
          <h1 className="display mt-2 text-[48px] sm:text-[56px]">{topic.title}</h1>
          <p className="mt-4 text-[15px] text-muted">
            {lessons} {lessons === 1 ? "lesson" : "lessons"} · {meta.questions} questions · about{" "}
            {Math.max(5, Math.round((meta.minutes * 1.4) / 5) * 5)} min of video
          </p>
        </div>
        <TopicStart topic={topic.id} stepIds={stepIds} />
      </header>

      <div className="grid gap-12 py-12 lg:grid-cols-[1fr_260px]">
        <StepList topic={topic.id} sections={sections} accent={subj.color} />
        <aside className="space-y-8 text-sm lg:sticky lg:top-24 lg:self-start">
          <div>
            <div className="eyebrow mb-3">How each topic works</div>
            <ul className="space-y-2.5 text-ink-soft">
              <li><b className="font-medium text-ink">▶ Lesson</b> — watch the idea explained.</li>
              <li><b className="font-medium text-ink">? Question</b> — try it yourself first.</li>
              <li><b className="font-medium text-ink">↳ Worked solution</b> — then watch it solved.</li>
              <li><b className="font-medium text-ink">≡ Rules</b> — worth knowing by heart.</li>
              <li><b className="font-medium text-ink">Practice</b> — on your own, at the end.</li>
            </ul>
          </div>
          <div className="space-y-2 border-t border-line pt-6">
            {prevT && (
              <Link href={`/topic/${prevT.id}`} className="block text-muted hover:text-ink">
                ← {prevT.title}
              </Link>
            )}
            {nextT && (
              <Link href={`/topic/${nextT.id}`} className="block text-muted hover:text-ink">
                Next topic: {nextT.title} →
              </Link>
            )}
          </div>
        </aside>
      </div>
    </main>
  );
}
