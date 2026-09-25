"use client";

import { useTypeset } from "@/components/MathJaxProvider";
import type { Boilerplate, Cluster } from "@/lib/types";
import { RichText } from "./RichText";

/**
 * Renders a cluster header — "Questions and Problems (Questions 1-7)",
 * "Graph Comprehension (Questions 8-12)" or "Table Comprehension (Questions
 * 17-20)" — plus, for the data-comprehension clusters, the shared intro text, the
 * artwork (one or two images), and the "disregard the information appearing in the
 * other questions" note. Wording comes from the official exam and must not be
 * reworded.
 */
export function ClusterIntro({
  cluster,
  boilerplate,
  collapsible,
}: {
  cluster: Cluster;
  boilerplate: Boilerplate;
  collapsible?: boolean;
}) {
  const ref = useTypeset<HTMLDivElement>([cluster.header]);
  const isGraph = cluster.type !== "questions_and_problems";

  const body = (
    <>
      {cluster.intro && (
        <div className="whitespace-pre-line text-[14.5px] leading-relaxed">
          <RichText text={cluster.intro} />
        </div>
      )}
      {[cluster.figure_path, cluster.secondary_figure_path]
        .filter(Boolean)
        .map((src) => (
          <figure key={src} className="my-4">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`/${src}`}
              alt="graph"
              className="max-w-full rounded border border-hair bg-white"
            />
          </figure>
        ))}
      {isGraph && (
        <div className="text-[14.5px]">{boilerplate.graph_disregard_note}</div>
      )}
      {cluster.translator_note && (
        <div className="mt-3 border-l-2 border-hair pl-3 text-[13.5px] italic text-slate-600">
          <span className="font-semibold not-italic">Translator&rsquo;s note (not part of the exam):</span>{" "}
          {cluster.translator_note}
        </div>
      )}
    </>
  );

  return (
    <div ref={ref} className="mt-6 border-t-2 border-ink pt-3.5 first:mt-0">
      <h3 className="mb-1.5 text-base font-semibold italic">{cluster.header}</h3>
      {isGraph && collapsible ? (
        <details className="text-sm" open>
          <summary className="cursor-pointer text-ink-soft">Graph and instructions</summary>
          <div className="mt-2">{body}</div>
        </details>
      ) : (
        body
      )}
      {isGraph && <div className="mt-3 font-bold">{boilerplate.questions_heading}</div>}
    </div>
  );
}
