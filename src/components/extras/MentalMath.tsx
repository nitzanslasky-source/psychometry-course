"use client";

import { useCallback, useEffect, useRef, useState } from "react";

/* ------------------------------------------------------------------ games */

interface Prob {
  q: string;
  a: string;
}
interface Game {
  id: string;
  title: string;
  blurb: string;
  make: () => Prob;
}

const ri = (a: number, b: number) => a + Math.floor(Math.random() * (b - a + 1));
const pick = <T,>(xs: T[]) => xs[Math.floor(Math.random() * xs.length)];
const fmt = (n: number) => String(Math.round(n * 1000) / 1000);

const FRACS: [number, number][] = [
  [1, 2], [1, 4], [3, 4], [1, 5], [2, 5], [3, 5], [4, 5], [1, 8], [3, 8], [5, 8], [1, 10], [1, 20], [1, 25], [1, 50],
];

const GAMES: Game[] = [
  {
    id: "times",
    title: "Times tables",
    blurb: "Up to 12 × 12 — the foundation of fast arithmetic.",
    make: () => {
      const a = ri(2, 12), b = ri(2, 12);
      return { q: `${a} × ${b}`, a: String(a * b) };
    },
  },
  {
    id: "times20",
    title: "Big times tables",
    blurb: "Up to 20 × 20. For when 12 × 12 is automatic.",
    make: () => {
      const a = ri(6, 20), b = ri(11, 20);
      return { q: `${a} × ${b}`, a: String(a * b) };
    },
  },
  {
    id: "divide",
    title: "Division",
    blurb: "Exact division — the times tables in reverse.",
    make: () => {
      const b = ri(2, 12), a = b * ri(2, 15);
      return { q: `${a} ÷ ${b}`, a: String(a / b) };
    },
  },
  {
    id: "squares",
    title: "Squares & roots",
    blurb: "Squares to 25², square roots, and cubes to 10³.",
    make: () => {
      const k = ri(0, 2);
      if (k === 0) {
        const n = ri(2, 25);
        return { q: `${n}²`, a: String(n * n) };
      }
      if (k === 1) {
        const n = ri(2, 25);
        return { q: `√${n * n}`, a: String(n) };
      }
      const n = ri(2, 10);
      return { q: `${n}³`, a: String(n ** 3) };
    },
  },
  {
    id: "fractions",
    title: "Fractions, decimals, %",
    blurb: "Switch instantly between ¼, 0.25 and 25%.",
    make: () => {
      const [n, d] = pick(FRACS);
      const k = ri(0, 1);
      return k === 0 ? { q: `${n}/${d} = ? %`, a: fmt((100 * n) / d) } : { q: `${n}/${d} = 0.?`, a: fmt(n / d) };
    },
  },
  {
    id: "mixed",
    title: "Mixed",
    blurb: "A bit of everything, like the real exam.",
    make: () => pick(GAMES.filter((g) => g.id !== "mixed" && g.id !== "times20")).make(),
  },
];

const ROUND = 60;
const bestKey = (id: string) => `mm.best.${id}`;
function readBest(id: string) {
  try {
    return Number(localStorage.getItem(bestKey(id)) || 0);
  } catch {
    return 0;
  }
}

/* ------------------------------------------------------------------ component */

export function MentalMath() {
  const [game, setGame] = useState<Game | null>(null);
  const [bests, setBests] = useState<Record<string, number>>({});
  useEffect(() => setBests(Object.fromEntries(GAMES.map((g) => [g.id, readBest(g.id)]))), [game]);

  if (!game)
    return (
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {GAMES.map((g, i) => (
          <button
            key={g.id}
            type="button"
            onClick={() => setGame(g)}
            className="pressable card group p-6 text-left transition-shadow hover:shadow-lift"
            style={{ animationDelay: `${i * 40}ms` }}
          >
            <div className="flex items-baseline justify-between">
              <div className="display text-[28px]">{g.title}</div>
              {bests[g.id] > 0 && <div className="text-xs text-muted">best {bests[g.id]}</div>}
            </div>
            <p className="mt-2 text-sm text-muted">{g.blurb}</p>
            <div className="mt-5 text-sm font-medium text-ink">
              Play 60 seconds <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
            </div>
          </button>
        ))}
      </div>
    );
  return <Round key={game.id} game={game} onExit={() => setGame(null)} />;
}

function Round({ game, onExit }: { game: Game; onExit: () => void }) {
  const [phase, setPhase] = useState<"ready" | "play" | "done">("ready");
  const [left, setLeft] = useState(ROUND);
  const [prob, setProb] = useState<Prob>(() => game.make());
  const [input, setInput] = useState("");
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [tries, setTries] = useState(0);
  const [missed, setMissed] = useState<Prob[]>([]);
  const [flash, setFlash] = useState<"ok" | "bad" | null>(null);
  const [best, setBest] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => setBest(readBest(game.id)), [game.id]);

  const next = useCallback(() => {
    let p = game.make();
    for (let i = 0; i < 5 && p.q === prob.q; i++) p = game.make();
    setProb(p);
    setInput("");
  }, [game, prob.q]);

  // clock
  useEffect(() => {
    if (phase !== "play") return;
    const t0 = Date.now();
    const id = setInterval(() => {
      const l = Math.max(0, ROUND - Math.floor((Date.now() - t0) / 1000));
      setLeft(l);
      if (l === 0) setPhase("done");
    }, 200);
    return () => clearInterval(id);
  }, [phase]);

  useEffect(() => {
    if (phase === "done" && score > best) {
      try {
        localStorage.setItem(bestKey(game.id), String(score));
      } catch {}
    }
  }, [phase]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (phase === "play") inputRef.current?.focus();
  }, [phase, prob]);

  const show = (f: "ok" | "bad") => {
    setFlash(f);
    setTimeout(() => setFlash(null), 260);
  };

  const type = (v: string) => {
    if (phase !== "play") return;
    const clean = v.replace(/[^0-9.]/g, "").slice(0, 8);
    setInput(clean);
    if (clean === prob.a) {
      // correct → count it and move on immediately (no Enter needed)
      setScore((s) => s + 1);
      setStreak((s) => s + 1);
      setTries((t) => t + 1);
      show("ok");
      next();
    }
  };
  const skip = () => {
    if (phase !== "play") return;
    setTries((t) => t + 1);
    setStreak(0);
    setMissed((m) => [...m, prob]);
    show("bad");
    next();
  };

  if (phase === "ready")
    return (
      <div className="rise-in mx-auto max-w-xl py-10 text-center">
        <div className="eyebrow">{game.title}</div>
        <p className="mt-4 text-ink-soft">{game.blurb}</p>
        <p className="mt-2 text-sm text-muted">Type the answer — correct answers move on by themselves. Press Enter to skip.</p>
        <div className="mt-8 flex justify-center gap-3">
          <button type="button" className="btn px-8 py-3 text-base" onClick={() => setPhase("play")} autoFocus>
            Start
          </button>
          <button type="button" className="btn-ghost" onClick={onExit}>
            Back
          </button>
        </div>
      </div>
    );

  if (phase === "done") {
    const record = score > best;
    return (
      <div className="rise-in mx-auto max-w-xl py-10 text-center">
        <div className="eyebrow">{game.title} · time’s up</div>
        <div className="display mt-6 text-[96px] leading-none">{score}</div>
        <div className="mt-2 text-muted">
          correct in 60 seconds{record ? " — a new personal best!" : best ? ` · your best is ${best}` : ""}
        </div>
        {tries > 0 && <div className="mt-1 text-sm text-faint">{Math.round((100 * score) / tries)}% accuracy</div>}
        {missed.length > 0 && (
          <div className="card mx-auto mt-8 max-w-sm p-5 text-left">
            <div className="eyebrow mb-3">Worth another look</div>
            <ul className="space-y-1.5 text-[15px] tabular-nums">
              {missed.slice(0, 8).map((m, i) => (
                <li key={i} className="flex justify-between">
                  <span>{m.q.replace(" = ? %", "").replace(" = 0.?", "")}</span>
                  <span className="font-medium">{m.q.includes("%") ? `${m.a}%` : m.a}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        <div className="mt-8 flex justify-center gap-3">
          <button
            type="button"
            className="btn px-8"
            onClick={() => {
              setScore(0);
              setStreak(0);
              setTries(0);
              setMissed([]);
              setLeft(ROUND);
              next();
              setPhase("play");
            }}
            autoFocus
          >
            Play again
          </button>
          <button type="button" className="btn-ghost" onClick={onExit}>
            All games
          </button>
        </div>
      </div>
    );
  }

  const shownQ = prob.q.replace(" = ? %", " = ").replace(" = 0.?", " = ");
  return (
    <div className="mx-auto max-w-xl py-6">
      <div className="flex items-center justify-between text-sm text-muted">
        <button type="button" onClick={onExit} className="pressable hover:text-ink">
          ← All games
        </button>
        <span className="tabular-nums">
          {score} correct {streak >= 3 && <span className="ml-2 text-gold">· {streak} in a row</span>}
        </span>
      </div>
      <div className="mt-3 h-1 overflow-hidden rounded-full bg-line">
        <div className="h-full rounded-full bg-ink transition-[width] duration-200 ease-linear" style={{ width: `${(left / ROUND) * 100}%` }} />
      </div>
      <div className="mt-1 text-right text-xs tabular-nums text-faint">{left}s</div>

      <div
        className={[
          "card mt-6 px-6 py-14 text-center transition-colors duration-200",
          flash === "ok" ? "anim-land border-ok bg-[#f1f8f4]" : "",
          flash === "bad" ? "anim-nope border-bad bg-[#fbf1f0]" : "",
        ].join(" ")}
      >
        <div className="display text-[64px] leading-none tabular-nums sm:text-[80px]">
          {shownQ}
          {prob.q.includes("= ? %") ? <span className="text-faint"> ?%</span> : prob.q.includes("0.?") ? <span className="text-faint"> ?</span> : null}
        </div>
        <input
          ref={inputRef}
          value={input}
          inputMode="decimal"
          autoComplete="off"
          aria-label="Your answer"
          onChange={(e) => type(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              skip();
            }
          }}
          className="mx-auto mt-8 block w-48 border-b-2 border-ink bg-transparent pb-2 text-center text-[40px] tabular-nums outline-none"
        />
        <button type="button" onClick={skip} className="mt-6 text-sm text-muted underline decoration-line underline-offset-4 hover:text-ink">
          Skip (Enter)
        </button>
      </div>
    </div>
  );
}
