"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { DictEntry } from "@/lib/extras";
import { canSpeak, hasHebrewVoice, speak, stopSpeaking, wait } from "@/lib/speech";

const SET = 25;

/** Vocabulary "podcast": the device reads each word, its Hebrew meaning, and the word again. */
export function ListenPlayer({ entries }: { entries: DictEntry[] }) {
  const words = useMemo(() => entries.filter((e) => e.he || e.def), [entries]);
  const sets = useMemo(() => {
    const out: { name: string; items: DictEntry[] }[] = [];
    for (let i = 0; i < words.length; i += SET) {
      const items = words.slice(i, i + SET);
      const a = items[0].w.replace(/^[^a-z]+/i, "").slice(0, 3);
      const b = items[items.length - 1].w.replace(/^[^a-z]+/i, "").slice(0, 3);
      out.push({ name: `${a} – ${b}`, items });
    }
    return out;
  }, [words]);

  const [ok, setOk] = useState(true);
  const [heVoice, setHeVoice] = useState(false);
  useEffect(() => {
    setOk(canSpeak());
    const t = setTimeout(() => setHeVoice(hasHebrewVoice()), 400); // voices load asynchronously
    return () => clearTimeout(t);
  }, []);

  const [setIdx, setSetIdx] = useState<number | null>(null);
  const [shuffle, setShuffle] = useState(false);
  const [quiz, setQuiz] = useState(false);
  const [rate, setRate] = useState(0.95);
  const [playing, setPlaying] = useState(false);
  const [pos, setPos] = useState(0);
  const [reveal, setReveal] = useState(true);

  const list = useMemo(() => {
    if (setIdx === null) return [];
    const items = [...sets[setIdx].items];
    if (shuffle) items.sort(() => Math.random() - 0.5);
    return items;
  }, [setIdx, shuffle, sets]);

  const run = useRef(0);
  const stop = useCallback(() => {
    run.current++;
    stopSpeaking();
    setPlaying(false);
  }, []);
  useEffect(() => stop, [stop]);

  const play = useCallback(
    async (from: number) => {
      const my = ++run.current;
      stopSpeaking();
      setPlaying(true);
      for (let i = from; i < list.length; i++) {
        if (run.current !== my) return;
        const e = list[i];
        setPos(i);
        setReveal(!quiz);
        await speak(e.w, "en", rate);
        if (run.current !== my) return;
        await wait(quiz ? 3200 : 600); // quiz: time to recall the meaning
        if (run.current !== my) return;
        setReveal(true);
        if (e.he && heVoice) await speak(e.he.split(" · ")[0], "he", rate);
        else if (e.def) await speak(e.def, "en", rate);
        else await wait(1400);
        if (run.current !== my) return;
        await wait(500);
        await speak(e.w, "en", rate * 0.95);
        if (run.current !== my) return;
        await wait(1100);
      }
      if (run.current === my) setPlaying(false);
    },
    [list, quiz, rate, heVoice],
  );

  // lock-screen / headphone controls where supported
  useEffect(() => {
    if (!("mediaSession" in navigator) || setIdx === null) return;
    navigator.mediaSession.metadata = new MediaMetadata({ title: `Vocabulary · ${sets[setIdx].name}`, artist: "Psychometry" });
    navigator.mediaSession.setActionHandler("play", () => void play(pos));
    navigator.mediaSession.setActionHandler("pause", stop);
    navigator.mediaSession.setActionHandler("nexttrack", () => void play(Math.min(list.length - 1, pos + 1)));
    navigator.mediaSession.setActionHandler("previoustrack", () => void play(Math.max(0, pos - 1)));
  }, [setIdx, sets, play, stop, pos, list.length]);

  if (!ok)
    return <p className="card p-6 text-ink-soft">This browser can’t read text aloud. Try Chrome or Safari on your phone or computer.</p>;

  if (setIdx === null)
    return (
      <div>
        <div className="eyebrow mb-4">{sets.length} episodes · {SET} words each</div>
        <ol className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {sets.map((s, i) => (
            <li key={i}>
              <button
                type="button"
                onClick={() => {
                  setSetIdx(i);
                  setPos(0);
                }}
                className="pressable card group flex w-full items-center gap-4 p-4 text-left transition-shadow hover:shadow-lift"
              >
                <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-ink text-sm text-white">▶</span>
                <span className="min-w-0">
                  <span className="block text-[13px] text-muted">Episode {i + 1}</span>
                  <span className="block truncate font-medium capitalize">{s.name}</span>
                </span>
              </button>
            </li>
          ))}
        </ol>
      </div>
    );

  const e = list[pos];
  return (
    <div className="mx-auto max-w-2xl">
      <button type="button" onClick={() => { stop(); setSetIdx(null); }} className="pressable text-sm text-muted hover:text-ink">
        ← All episodes
      </button>

      <div className="card mt-5 overflow-hidden">
        <div className="bg-ink px-8 pb-10 pt-8 text-white">
          <div className="flex items-center justify-between text-xs uppercase tracking-[0.14em] text-white/60">
            <span>Episode {setIdx + 1} · <span className="capitalize">{sets[setIdx].name}</span></span>
            <span className="tabular-nums">{pos + 1} / {list.length}</span>
          </div>
          <div key={pos} className="rise-in mt-10 text-center">
            <div className="display text-[56px] sm:text-[72px]">{e.w}</div>
            <div className={["mt-4 min-h-[2.5rem] transition-opacity duration-300", reveal ? "opacity-100" : "opacity-0"].join(" ")}>
              {e.he && <div dir="rtl" lang="he" className="text-[26px] text-[#e9d9ad]">{e.he}</div>}
              {e.def && <div className="mt-1 text-[16px] text-white/70">{e.def}</div>}
            </div>
          </div>
          <div className="mt-10 h-1 overflow-hidden rounded-full bg-white/15">
            <div className="progress-fill h-full rounded-full bg-[#e9d9ad]" style={{ width: `${((pos + 1) / list.length) * 100}%` }} />
          </div>
        </div>

        <div className="flex items-center justify-center gap-4 px-6 py-6">
          <button type="button" aria-label="Previous word" className="pressable flex h-11 w-11 items-center justify-center rounded-full border border-line text-ink-soft hover:border-faint" onClick={() => void (playing ? play(Math.max(0, pos - 1)) : setPos(Math.max(0, pos - 1)))}>
            ⏮
          </button>
          <button
            type="button"
            aria-label={playing ? "Pause" : "Play"}
            className="pressable flex h-16 w-16 items-center justify-center rounded-full bg-ink text-xl text-white shadow-lift"
            onClick={() => (playing ? stop() : void play(pos))}
          >
            {playing ? "❚❚" : "▶"}
          </button>
          <button type="button" aria-label="Next word" className="pressable flex h-11 w-11 items-center justify-center rounded-full border border-line text-ink-soft hover:border-faint" onClick={() => void (playing ? play(Math.min(list.length - 1, pos + 1)) : setPos(Math.min(list.length - 1, pos + 1)))}>
            ⏭
          </button>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-2 border-t border-line px-6 py-4 text-sm">
          <Toggle on={quiz} onClick={() => { stop(); setQuiz(!quiz); }} label="Quiz mode" hint="pause to recall the meaning" />
          <Toggle on={shuffle} onClick={() => { stop(); setShuffle(!shuffle); setPos(0); }} label="Shuffle" />
          <div className="flex items-center gap-1 rounded-full border border-line p-1">
            {[0.8, 0.95, 1.15].map((r) => (
              <button key={r} type="button" onClick={() => { stop(); setRate(r); }} className={["pressable rounded-full px-3 py-1", rate === r ? "bg-ink text-white" : "text-ink-soft"].join(" ")}>
                {r === 0.8 ? "Slow" : r === 0.95 ? "Normal" : "Fast"}
              </button>
            ))}
          </div>
        </div>
      </div>
      {!heVoice && (
        <p className="mt-4 text-center text-xs text-muted">
          Your device has no Hebrew voice, so the meaning is shown on screen and the English definition is read where there is one.
        </p>
      )}
    </div>
  );
}

function Toggle({ on, onClick, label, hint }: { on: boolean; onClick: () => void; label: string; hint?: string }) {
  return (
    <button type="button" onClick={onClick} aria-pressed={on} title={hint} className={["pressable rounded-full border px-4 py-1.5", on ? "border-ink bg-ink text-white" : "border-line text-ink-soft hover:border-faint"].join(" ")}>
      {label}
    </button>
  );
}
