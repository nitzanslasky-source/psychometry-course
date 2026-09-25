"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { ReactNode } from "react";
import { IconRotateCcw } from "@/components/icons";

interface Point {
  x: number;
  y: number;
}

/** Points are stored normalized (0..1 of the canvas box) so strokes stay put across resizes. */
type Stroke = Point[];

const INK = "#dc2626";
const RULED_LINE = "rgba(148,163,184,0.35)";

// iOS treats a long-press on an <img> as a "save/copy image" gesture even when a covering
// canvas should own the touch — these two properties are the standard way to suppress that.
const NO_CALLOUT_STYLE: React.CSSProperties = {
  WebkitTouchCallout: "none",
  WebkitUserSelect: "none",
  userSelect: "none",
};

interface Props {
  /** Relative to public/, e.g. "practice-figures/geo_001.png". Drawn under the canvas so marks land directly on them. */
  figurePaths?: string[];
  /** The question stem (and any number/flag chrome around it) — rendered under the canvas so it can be marked up directly (circling, underlining). */
  children: ReactNode;
  /** Rendered above the ink layer, top-right — e.g. a bookmark or flag toggle that must stay clickable. */
  topRightSlot?: ReactNode;
  /** Shrinks the figure and ruled strip so more of the question fits on screen at once. */
  compact?: boolean;
}

/**
 * A freehand annotation layer covering the stem and figures (if any) plus a blank ruled strip
 * below, so marks can land directly on the question — circling a number, underlining a phrase,
 * drawing on a diagram — while the answer options stay outside it and fully clickable.
 * `topRightSlot` is raised above the ink layer so its control stays clickable too. Deliberately
 * not persisted — clears when the question changes, same as scratch paper.
 *
 * Touch handling: a stylus (Apple Pencil etc.) always draws. A bare finger draws only once
 * "Draw with finger" is toggled on; otherwise it scrolls the page. touch-action is "none" on the
 * canvas *unconditionally* — letting WebKit's own touch-action/preventDefault interaction decide
 * scroll-vs-draw per gesture proved unreliable (it inverted which state drew, then let scrolling
 * and drawing both fire at once) — so scrolling when not drawing is done manually here via
 * window.scrollBy, fully sidestepping the browser's native gesture heuristics.
 */
export function QuestionScratchpad({ figurePaths, children, topRightSlot, compact }: Props) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const strokesRef = useRef<Stroke[]>([]);
  // Keyed by pointerId rather than a single shared ref, so a late/out-of-order event from one
  // gesture can never stomp on a second stroke started right after it.
  const activeStrokesRef = useRef<Map<number, Stroke>>(new Map());
  // Tracks the last clientY per pointerId for touches that are scrolling rather than drawing.
  const scrollTouchesRef = useRef<Map<number, number>>(new Map());
  const sizeRef = useRef({ width: 0, height: 0 });
  const [hasMarks, setHasMarks] = useState(false);
  const [fingerDraw, setFingerDraw] = useState(false);

  // Only touched on an actual size change (mount + ResizeObserver) — setting canvas.width/height
  // reallocates the whole bitmap, so it must never run on every pointermove (that was the cause
  // of dropped/laggy strokes: the browser was busy resizing instead of tracking the next touch).
  const resizeCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    const wrap = wrapRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !wrap || !ctx) return;

    const { width, height } = wrap.getBoundingClientRect();
    sizeRef.current = { width, height };
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.max(1, Math.round(width * dpr));
    canvas.height = Math.max(1, Math.round(height * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    paint();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Cheap: just clears and replays strokes onto the already-sized canvas. Safe to call on
  // every pointermove.
  const paint = useCallback(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    const { width, height } = sizeRef.current;
    if (!canvas || !ctx || width === 0) return;

    ctx.clearRect(0, 0, width, height);
    ctx.strokeStyle = INK;
    ctx.lineWidth = 2.5;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.globalAlpha = 0.85;

    const all = [...strokesRef.current, ...activeStrokesRef.current.values()];
    for (const stroke of all) {
      if (stroke.length < 2) continue;
      ctx.beginPath();
      ctx.moveTo(stroke[0].x * width, stroke[0].y * height);
      for (const p of stroke.slice(1)) ctx.lineTo(p.x * width, p.y * height);
      ctx.stroke();
    }
  }, []);

  useEffect(() => {
    resizeCanvas();
    const wrap = wrapRef.current;
    if (!wrap || typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(() => resizeCanvas());
    ro.observe(wrap);
    return () => ro.disconnect();
  }, [resizeCanvas, compact]);

  function toPoint(e: React.PointerEvent<HTMLCanvasElement>): Point {
    const rect = canvasRef.current!.getBoundingClientRect();
    return {
      x: (e.clientX - rect.left) / rect.width,
      y: (e.clientY - rect.top) / rect.height,
    };
  }

  function canDraw(e: React.PointerEvent<HTMLCanvasElement>): boolean {
    return e.pointerType !== "touch" || fingerDraw;
  }

  function handlePointerDown(e: React.PointerEvent<HTMLCanvasElement>) {
    if (!canDraw(e)) {
      // A scrolling touch — touch-action is "none" so the browser won't pan on its own;
      // track its position so handlePointerMove can scroll the page manually instead.
      if (e.pointerType === "touch") scrollTouchesRef.current.set(e.pointerId, e.clientY);
      return;
    }
    e.preventDefault();
    // Deliberately not calling setPointerCapture: it's only a nicety (keeps tracking a pointer
    // that drifts outside the canvas mid-stroke), and it's known to throw on rapid successive
    // touches on WebKit — that was silently dropping the second stroke entirely before this was
    // wrapped in try/catch, and it's simpler and safer to just not depend on it at all.
    activeStrokesRef.current.set(e.pointerId, [toPoint(e)]);
  }

  function handlePointerMove(e: React.PointerEvent<HTMLCanvasElement>) {
    const stroke = activeStrokesRef.current.get(e.pointerId);
    if (stroke) {
      stroke.push(toPoint(e));
      paint();
      return;
    }
    const lastY = scrollTouchesRef.current.get(e.pointerId);
    if (lastY !== undefined) {
      window.scrollBy(0, lastY - e.clientY);
      scrollTouchesRef.current.set(e.pointerId, e.clientY);
    }
  }

  function endStroke(e: React.PointerEvent<HTMLCanvasElement>) {
    scrollTouchesRef.current.delete(e.pointerId);
    const stroke = activeStrokesRef.current.get(e.pointerId);
    activeStrokesRef.current.delete(e.pointerId);
    if (stroke && stroke.length > 1) {
      strokesRef.current.push(stroke);
      setHasMarks(true);
    }
    paint();
  }

  function handleClear() {
    strokesRef.current = [];
    activeStrokesRef.current.clear();
    setHasMarks(false);
    paint();
  }

  return (
    <div className="relative">
      <div ref={wrapRef} className="relative overflow-hidden rounded border border-hair dark:border-white/10">
        <div className="p-3 pr-10">{children}</div>
        {figurePaths?.map((f) => (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            key={f}
            src={`/${f}`}
            alt="figure"
            draggable={false}
            style={NO_CALLOUT_STYLE}
            className={[
              "mx-auto block w-full bg-white object-contain",
              compact ? "max-h-[24vh]" : "max-h-[38vh]",
            ].join(" ")}
          />
        ))}
        <div
          className={["w-full bg-white dark:bg-white/5", compact ? "h-16" : "h-28"].join(" ")}
          style={{
            backgroundImage: `linear-gradient(to right, ${RULED_LINE} 1px, transparent 1px), linear-gradient(to bottom, ${RULED_LINE} 1px, transparent 1px)`,
            backgroundSize: "20px 20px",
          }}
        />
        <canvas
          ref={canvasRef}
          className="absolute inset-0 h-full w-full"
          // Always "none" — the browser never handles touch gestures on this element at all.
          // Scrolling when not drawing is done manually in handlePointerMove instead.
          style={{ touchAction: "none", ...NO_CALLOUT_STYLE }}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={endStroke}
          onPointerLeave={endStroke}
          onPointerCancel={endStroke}
        />
        {topRightSlot && (
          <div className="absolute right-1.5 top-1.5 z-10 rounded-md bg-white/90 dark:bg-black/60">{topRightSlot}</div>
        )}
        <button
          type="button"
          onClick={() => setFingerDraw((v) => !v)}
          aria-pressed={fingerDraw}
          className={[
            "absolute bottom-1.5 left-1.5 z-10 inline-flex items-center gap-1 rounded-md border px-2 py-1 text-xs font-medium shadow-soft",
            fingerDraw
              ? "border-brand-300 bg-brand-50 text-brand-700 dark:border-brand-500/40 dark:bg-brand-500/15 dark:text-brand-300"
              : "border-hair bg-white/90 text-muted hover:text-ink dark:border-white/15 dark:bg-black/60 dark:text-neutral-300 dark:hover:text-neutral-100",
          ].join(" ")}
        >
          {fingerDraw ? "Finger: drawing" : "Draw with finger"}
        </button>
        {hasMarks && (
          <button
            type="button"
            onClick={handleClear}
            className="absolute bottom-1.5 right-1.5 z-10 inline-flex items-center gap-1 rounded-md border border-hair bg-white/90 px-2 py-1 text-xs font-medium text-muted shadow-soft hover:text-ink dark:border-white/15 dark:bg-black/60 dark:text-neutral-300 dark:hover:text-neutral-100"
          >
            <IconRotateCcw width={12} height={12} /> Clear marks
          </button>
        )}
      </div>
      <p className="mt-1 text-[11px] text-muted dark:text-neutral-500">
        A stylus always draws. On touch, tap &ldquo;Draw with finger&rdquo; first — otherwise a
        finger swipe just scrolls the page.
      </p>
    </div>
  );
}
