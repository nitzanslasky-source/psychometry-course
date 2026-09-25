"use client";

/**
 * Spaced review (Leitner boxes), stored on this device until accounts land.
 * Items come back after 1, 3, 7, 16 and 35 days; a miss sends an item back to box 1.
 *
 * Keys:  q:<topic>:<questionId>  course question
 *        s:<questionId>          exam-simulation question
 *        w:<word>                dictionary word
 *        c:<cardId>              rules card
 */
const KEY = "srs.v1";
const DAY = 24 * 60 * 60 * 1000;
export const INTERVALS = [1, 3, 7, 16, 35]; // days, by box 1..5

export type SrsKind = "q" | "s" | "w" | "c";
export interface SrsItem {
  key: string;
  kind: SrsKind;
  box: number;
  due: number;
  added: number;
  /** Times answered correctly in review. */
  wins: number;
}

type Store = Record<string, SrsItem>;

function load(): Store {
  if (typeof window === "undefined") return {};
  try {
    return JSON.parse(localStorage.getItem(KEY) || "{}") as Store;
  } catch {
    return {};
  }
}
function save(s: Store) {
  try {
    localStorage.setItem(KEY, JSON.stringify(s));
    window.dispatchEvent(new Event("srs-change"));
  } catch {}
}

const startOfDay = (t: number) => {
  const d = new Date(t);
  d.setHours(0, 0, 0, 0);
  return d.getTime();
};

export function srsAll(): SrsItem[] {
  return Object.values(load());
}
export function srsHas(key: string) {
  return !!load()[key];
}

/** Add an item (due tomorrow by default, or today with `now`). Existing items are reset to box 1 if `again`. */
export function srsAdd(key: string, opts: { now?: boolean; again?: boolean } = {}) {
  const s = load();
  const kind = key.split(":")[0] as SrsKind;
  const due = opts.now ? Date.now() : startOfDay(Date.now()) + DAY;
  if (s[key] && !opts.again) return;
  s[key] = { key, kind, box: 1, due, added: s[key]?.added ?? Date.now(), wins: s[key]?.wins ?? 0 };
  save(s);
}

export function srsRemove(key: string) {
  const s = load();
  delete s[key];
  save(s);
}

/** Record a review result and schedule the next one. */
export function srsGrade(key: string, knew: boolean) {
  const s = load();
  const it = s[key];
  if (!it) return;
  it.box = knew ? Math.min(INTERVALS.length, it.box + 1) : 1;
  it.wins += knew ? 1 : 0;
  it.due = startOfDay(Date.now()) + INTERVALS[it.box - 1] * DAY;
  save(s);
}

export function srsDue(now = Date.now()): SrsItem[] {
  return srsAll()
    .filter((i) => i.due <= now)
    .sort((a, b) => a.due - b.due);
}

/** Items that have reached the last box and been recalled there are "mastered". */
export const isMastered = (i: SrsItem) => i.box >= INTERVALS.length && i.wins >= INTERVALS.length;
