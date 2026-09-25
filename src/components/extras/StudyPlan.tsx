"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { loadProgress } from "@/lib/courseProgressStore";
import { loadPlan, savePlan, type PlanSettings } from "@/lib/planStore";
import type { PlanStep, PlanTopic } from "@/lib/planData";
import { SUBJECT } from "@/lib/subjects";
import type { SubjectKey } from "@/lib/fullCourseTypes";

const DAY = 86400000;
const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const FINAL_DAYS = 14; // last two weeks: exam simulations + review
const KIND: Record<PlanStep["k"], string> = { v: "lesson", q: "question", p: "practice", c: "rules card" };

const midnight = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
const iso = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
const fmt = (d: Date) => d.toLocaleDateString(undefined, { weekday: "short", day: "numeric", month: "short" });

interface DayPlan {
  date: Date;
  final: boolean;
  items: { topic: PlanTopic; from: number; to: number; count: number; kinds: Record<string, number>; minutes: number }[];
  sims: { id: string; label: string }[];
  minutes: number;
}

function schedule(s: PlanSettings, steps: PlanStep[], topics: PlanTopic[], sims: { id: string; label: string }[], done: Record<string, true>) {
  const today = midnight(new Date());
  const exam = midnight(new Date(s.exam + "T00:00"));
  const finalStart = new Date(exam.getTime() - FINAL_DAYS * DAY);
  const left = steps.filter((st) => !done[`t${st.t}:${st.id}`]);
  const totalMin = left.reduce((n, st) => n + st.m, 0);
  const tById = new Map(topics.map((t) => [t.id, t]));

  const studyDays: Date[] = [];
  for (let d = today; d < exam; d = new Date(d.getTime() + DAY)) if (s.days.includes(d.getDay())) studyDays.push(d);
  const learnDays = studyDays.filter((d) => d < finalStart);
  const finalDays = studyDays.filter((d) => d >= finalStart);
  const needPerDay = learnDays.length ? Math.ceil(totalMin / learnDays.length) : Infinity;

  const plan: DayPlan[] = [];
  let i = 0;
  for (const d of learnDays) {
    const day: DayPlan = { date: d, final: false, items: [], sims: [], minutes: 0 };
    while (i < left.length && (day.minutes === 0 || day.minutes + left[i].m <= s.minutes + 5)) {
      const st = left[i++];
      const last = day.items[day.items.length - 1];
      if (last && last.topic.id === st.t) {
        last.to = st.n;
        last.count++;
        last.minutes += st.m;
        last.kinds[st.k] = (last.kinds[st.k] || 0) + 1;
      } else day.items.push({ topic: tById.get(st.t)!, from: st.n, to: st.n, count: 1, minutes: st.m, kinds: { [st.k]: 1 } });
      day.minutes += st.m;
    }
    plan.push(day);
  }
  // final stretch: one simulation section per day (two if time allows), then review
  let si = 0;
  for (const d of finalDays) {
    const n = s.minutes >= 60 ? 2 : 1;
    plan.push({ date: d, final: true, items: [], sims: sims.slice(si, si + n), minutes: n * 25 + 15 });
    si += n;
  }
  return { plan, leftSteps: left.length, totalMin, needPerDay, overflow: left.length - i, learnDays: learnDays.length, exam };
}

export function StudyPlan({ steps, topics, sims }: { steps: PlanStep[]; topics: PlanTopic[]; sims: { id: string; label: string }[] }) {
  const [settings, setSettings] = useState<PlanSettings | null>(null);
  const [done, setDone] = useState<Record<string, true>>({});
  const [editing, setEditing] = useState(false);
  useEffect(() => {
    setSettings(loadPlan());
    setDone(loadProgress().done);
  }, []);

  const result = useMemo(() => (settings ? schedule(settings, steps, topics, sims, done) : null), [settings, steps, topics, sims, done]);

  if (!settings || editing)
    return (
      <PlanForm
        initial={settings}
        onSave={(p) => {
          savePlan(p);
          setSettings(p);
          setEditing(false);
        }}
        onCancel={settings ? () => setEditing(false) : undefined}
      />
    );
  if (!result) return null;

  const { plan, needPerDay, overflow, totalMin, leftSteps, exam } = result;
  const daysLeft = Math.ceil((exam.getTime() - midnight(new Date()).getTime()) / DAY);
  const today = plan[0] && plan[0].date.getTime() === midnight(new Date()).getTime() ? plan[0] : null;
  const next = plan.slice(today ? 1 : 0, today ? 8 : 7);

  return (
    <div>
      <div className="flex flex-wrap items-end justify-between gap-6">
        <dl className="grid grid-cols-3 gap-8">
          <Stat n={daysLeft} label="days to the exam" />
          <Stat n={leftSteps} label="steps left" />
          <Stat n={`${Math.round(totalMin / 60)}h`} label="of study left" />
        </dl>
        <button type="button" className="btn-ghost" onClick={() => setEditing(true)}>
          Change plan
        </button>
      </div>

      {overflow > 0 && (
        <p className="mt-6 rounded-2xl border border-bad/30 bg-[#fbf1f0] p-4 text-sm text-ink-soft">
          At {settings.minutes} minutes a day there isn’t enough time to finish before the final two weeks — you’d need
          about <b className="text-ink">{Math.ceil(needPerDay / 5) * 5} minutes</b> on each study day, or more study days.
        </p>
      )}

      <section className="mt-10">
        <div className="eyebrow">Today · {fmt(midnight(new Date()))}</div>
        {today ? <DayCard day={today} big /> : <p className="card mt-3 p-6 text-muted">No study planned today — enjoy the break.</p>}
      </section>

      <section className="mt-12">
        <div className="eyebrow">Coming up</div>
        <div className="mt-3 grid gap-3 md:grid-cols-2">
          {next.map((d) => (
            <DayCard key={iso(d.date)} day={d} />
          ))}
        </div>
      </section>
    </div>
  );
}

function DayCard({ day, big }: { day: DayPlan; big?: boolean }) {
  return (
    <div className={["card", big ? "mt-3 p-6" : "p-5"].join(" ")}>
      {!big && <div className="mb-2 text-sm font-medium">{fmt(day.date)}</div>}
      {day.final ? (
        <ul className="space-y-2 text-[15px]">
          {day.sims.map((s) => (
            <li key={s.id}>
              <Link href={`/simulation/${s.id}`} className="link">
                Exam simulation · {s.label}
              </Link>
            </li>
          ))}
          <li>
            <Link href="/review" className="link">
              Review your mistakes
            </Link>
          </li>
        </ul>
      ) : (
        <ul className="space-y-3">
          {day.items.map((it) => {
            const color = SUBJECT[it.topic.subject as SubjectKey]?.color;
            const what = Object.entries(it.kinds)
              .map(([k, n]) => `${n} ${KIND[k as PlanStep["k"]]}${n > 1 ? (k === "q" ? "s" : k === "p" ? "" : "s") : ""}`)
              .join(" · ");
            return (
              <li key={it.topic.id + ":" + it.from} className="flex items-start gap-3">
                <span className="mt-2 h-2 w-2 shrink-0 rounded-full" style={{ background: color }} />
                <div className="min-w-0 flex-1">
                  <Link href={`/topic/${it.topic.id}/${it.from}`} className={["font-medium hover:underline", big ? "text-[17px]" : "text-[15px]"].join(" ")}>
                    {it.topic.title}
                  </Link>
                  <div className="text-xs text-muted">
                    steps {it.from}–{it.to} · {what}
                  </div>
                </div>
                {big && (
                  <Link href={`/topic/${it.topic.id}/${it.from}`} className="btn px-4 py-1.5">
                    Start
                  </Link>
                )}
              </li>
            );
          })}
        </ul>
      )}
      <div className="mt-3 text-xs text-faint">about {Math.round(day.minutes)} min</div>
    </div>
  );
}

function PlanForm({ initial, onSave, onCancel }: { initial: PlanSettings | null; onSave: (p: PlanSettings) => void; onCancel?: () => void }) {
  const inThree = iso(new Date(Date.now() + 90 * DAY));
  const [exam, setExam] = useState(initial?.exam || inThree);
  const [days, setDays] = useState<number[]>(initial?.days || [0, 1, 2, 3, 4]);
  const [minutes, setMinutes] = useState(initial?.minutes || 60);
  const tooSoon = new Date(exam + "T00:00").getTime() - Date.now() < 21 * DAY;
  return (
    <form
      className="card max-w-xl space-y-7 p-8"
      onSubmit={(e) => {
        e.preventDefault();
        if (days.length) onSave({ exam, days, minutes });
      }}
    >
      <label className="block">
        <span className="text-sm font-medium">When is your exam?</span>
        <input type="date" required value={exam} min={iso(new Date())} onChange={(e) => setExam(e.target.value)} className="mt-2 block w-full rounded-xl border border-line bg-white px-4 py-3 outline-none focus:border-ink" />
        {tooSoon && <span className="mt-2 block text-xs text-bad">Less than three weeks — the plan will focus on what matters most, but it will be tight.</span>}
      </label>
      <fieldset>
        <legend className="text-sm font-medium">Which days can you study?</legend>
        <div className="mt-2 flex flex-wrap gap-1.5">
          {WEEKDAYS.map((d, i) => {
            const on = days.includes(i);
            return (
              <button key={d} type="button" aria-pressed={on} onClick={() => setDays(on ? days.filter((x) => x !== i) : [...days, i].sort())} className={["pressable h-11 w-14 rounded-xl border text-sm", on ? "border-ink bg-ink text-white" : "border-line bg-white text-ink-soft"].join(" ")}>
                {d}
              </button>
            );
          })}
        </div>
      </fieldset>
      <label className="block">
        <span className="text-sm font-medium">How long on a study day?</span>
        <div className="mt-2 flex flex-wrap gap-1.5">
          {[30, 45, 60, 90, 120, 180].map((m) => (
            <button key={m} type="button" aria-pressed={minutes === m} onClick={() => setMinutes(m)} className={["pressable rounded-xl border px-4 py-2.5 text-sm", minutes === m ? "border-ink bg-ink text-white" : "border-line bg-white text-ink-soft"].join(" ")}>
              {m < 60 ? `${m} min` : `${m / 60} h`}
            </button>
          ))}
        </div>
      </label>
      <div className="flex gap-3">
        <button type="submit" className="btn px-6 py-3" disabled={!days.length}>
          {initial ? "Update my plan" : "Make my plan"}
        </button>
        {onCancel && (
          <button type="button" className="btn-ghost" onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

function Stat({ n, label }: { n: number | string; label: string }) {
  return (
    <div>
      <dt className="display text-[44px] leading-none">{n}</dt>
      <dd className="mt-1 text-sm text-muted">{label}</dd>
    </div>
  );
}
