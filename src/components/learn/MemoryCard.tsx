"use client";

import { useTypeset } from "@/components/MathJaxProvider";
import type { CourseCardStep } from "@/lib/fullCourseTypes";

/* ---------------------------------------------------------------- memory card */

function Cell({ text }: { text: string }) {
  return text.startsWith("!") ? <strong className="font-semibold">{text.slice(1)}</strong> : <>{text}</>;
}

export function MemoryCard({ step, accent, heading }: { step: CourseCardStep; accent: string; heading?: React.ReactNode }) {
  const ref = useTypeset<HTMLDivElement>([step.id]);
  return (
    <div ref={ref}>
      {heading ?? <h1 className="display text-[40px] sm:text-[48px]">{step.title}</h1>}
      {step.intro && <p className="mt-3 text-[16px] text-ink-soft">{step.intro}</p>}
      {step.tables.map((t, ti) => (
        <div key={ti} className="mt-8">
          {t.title && <h3 className="mb-3 text-[15px] font-semibold">{t.title}</h3>}
          <div className="card overflow-x-auto">
            <table className="w-full border-collapse text-[14px]">
              {t.head.length > 0 && (
                <thead>
                  <tr>
                    {t.head.map((h, i) => (
                      <th key={i} className="border-b border-line bg-paper px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-[0.1em] text-muted">
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
              )}
              <tbody>
                {t.rows.map((r, ri) => (
                  <tr key={ri} className="border-b border-line last:border-0">
                    {r.map((c, ci) => (
                      <td key={ci} className="px-4 py-3 align-top leading-relaxed">
                        <Cell text={c} />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
      {step.tips.length > 0 && (
        <div className="mt-8 border-l-2 pl-5" style={{ borderColor: accent }}>
          <div className="eyebrow mb-2">Remember</div>
          <ul className="space-y-1.5 text-[15px] text-ink-soft">
            {step.tips.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
