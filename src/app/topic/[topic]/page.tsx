import Link from "next/link";
import { notFound } from "next/navigation";
import { getTopic, getVideoManifest } from "@/lib/fullCourse";
import { buildStepList } from "@/lib/fullCourseNav";
import { StepList } from "@/components/learn/StepList";
import { IconArrowLeft } from "@/components/icons";

export const dynamic = "force-dynamic";

export default async function TopicPage({ params }: { params: Promise<{ topic: string }> }) {
  const { topic: raw } = await params;
  const topic = getTopic(Number(raw));
  if (!topic) notFound();
  const sections = buildStepList(topic, getVideoManifest());

  return (
    <main className="mx-auto max-w-3xl px-5 py-10">
      <Link href="/" className="link-subtle inline-flex items-center gap-1 text-sm">
        <IconArrowLeft width={15} height={15} /> All topics
      </Link>
      <h1 className="mt-3 text-3xl font-bold">{topic.title}</h1>
      <div className="mt-4">
        <Link href={`/topic/${topic.id}/1`} className="btn-primary">
          Start the topic
        </Link>
      </div>
      <div className="surface-card mt-8 p-5">
        <StepList topic={topic.id} sections={sections} />
      </div>
    </main>
  );
}
