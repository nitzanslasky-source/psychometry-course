/**
 * Data access for the full recorded course (content/full-course/, exported from the Teacher Studio).
 * Read from disk on the server so the ~2.6 MB of course content never ships as one bundle.
 */
import "server-only";

import fs from "node:fs";
import path from "node:path";
import type { CourseOutline, CourseStep, CourseTopic, VideoSource } from "./fullCourseTypes";

const DIR = path.join(process.cwd(), "content", "full-course");

function readJson<T>(file: string): T {
  return JSON.parse(fs.readFileSync(path.join(DIR, file), "utf8")) as T;
}

export function getOutline(): CourseOutline {
  return readJson<CourseOutline>("outline.json");
}

export function getTopic(id: number): CourseTopic | null {
  const file = path.join(DIR, "topics", `t${id}.json`);
  if (!Number.isInteger(id) || !fs.existsSync(file)) return null;
  return readJson<CourseTopic>(`topics/t${id}.json`);
}

/** Every step of a topic in order (learn sections, then practice), with its section. */
export function flattenSteps(topic: CourseTopic): { step: CourseStep; sectionIndex: number }[] {
  return topic.sections.flatMap((s, sectionIndex) => s.steps.map((step) => ({ step, sectionIndex })));
}

/** Recorded videos. Re-read on each request so newly uploaded videos appear without a rebuild in dev. */
export function getVideoManifest(): Record<string, VideoSource> {
  try {
    const m = readJson<Record<string, VideoSource | string>>("video-manifest.json");
    return Object.fromEntries(Object.entries(m).filter(([k]) => !k.startsWith("_"))) as Record<string, VideoSource>;
  } catch {
    return {};
  }
}
