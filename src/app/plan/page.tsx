import { getPlanData } from "@/lib/planData";
import { StudyPlan } from "@/components/extras/StudyPlan";

export const metadata = { title: "My study plan — Psychometry" };

export default function PlanPage() {
  const { steps, topics, sims } = getPlanData();
  return (
    <main className="mx-auto max-w-5xl px-6">
      <header className="rise-in pb-10 pt-14">
        <div className="eyebrow">Study plan</div>
        <h1 className="display mt-3 text-[52px]">My study plan</h1>
        <p className="mt-3 max-w-2xl text-[16px] text-ink-soft">
          Tell us your exam date and how much time you have — you’ll get what to study each day, quantitative and verbal
          side by side, and the last two weeks kept for exam simulations and review. The plan adjusts itself every day to
          what you’ve actually done.
        </p>
      </header>
      <StudyPlan steps={steps} topics={topics} sims={sims} />
    </main>
  );
}
