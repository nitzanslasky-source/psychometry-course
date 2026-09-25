import Link from "next/link";
import { listSimulationSections } from "@/lib/content";
import { SimScores } from "@/components/extras/SimScores";

export const metadata = { title: "Exam simulations — Psychometry" };

export default function SimulationsPage() {
  const rows = listSimulationSections();
  const exams = new Map<string, { label: string; sections: typeof rows }>();
  for (const r of rows) {
    const k = r.exam.source_exam;
    if (!exams.has(k)) exams.set(k, { label: r.exam.source_exam_label, sections: [] });
    exams.get(k)!.sections.push(r);
  }
  const list = [...exams.values()].reverse(); // newest first

  return (
    <main className="mx-auto max-w-5xl px-6">
      <header className="rise-in pb-10 pt-14">
        <div className="eyebrow">Exam practice</div>
        <h1 className="display mt-3 text-[52px]">Section simulations</h1>
        <p className="mt-3 max-w-2xl text-[16px] text-ink-soft">
          Real quantitative sections from past psychometric exams, in English, exactly as they were given: 20 questions,
          20 minutes, the official answer key. Your answers are graded when you submit, then you can review every
          question.
        </p>
      </header>

      <div className="card divide-y divide-line">
        {list.map((e) => (
          <div key={e.label} className="grid items-center gap-4 px-6 py-5 sm:grid-cols-[1fr_auto]">
            <div>
              <div className="display text-[26px]">{e.label.replace(/ Psychometric.*$/i, "")}</div>
              <div className="text-xs text-muted">Quantitative Reasoning · {e.sections.length} sections</div>
            </div>
            <div className="flex flex-wrap gap-2">
              {e.sections.map((s) => (
                <Link key={s.section.section_id} href={`/simulation/${s.section.section_id}`} className="btn-ghost gap-3">
                  Section {s.section.position}
                  <SimScores sectionId={s.section.section_id} />
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
