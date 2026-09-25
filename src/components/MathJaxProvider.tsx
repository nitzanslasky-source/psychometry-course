"use client";

import Script from "next/script";
import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";

/**
 * MathJax config MUST use \( ... \) delimiters ONLY.
 *
 * Do NOT enable `$...$`: some NITE questions define a custom operator with a literal
 * "$" symbol (e.g. Autumn 2021 §2 Q6, `$(a,b) = b²/a + a²/b`). Enabling `$` as a
 * delimiter swallows those and corrupts the question.
 */
const MATHJAX_CONFIG = {
  tex: { inlineMath: [["\\(", "\\)"]] },
  svg: { fontCache: "global" },
  options: { enableMenu: false },
};

declare global {
  interface Window {
    MathJax?: {
      typesetPromise?: (els?: unknown[]) => Promise<void>;
      typesetClear?: (els?: unknown[]) => void;
      startup?: { promise: Promise<void> };
    };
  }
}

const MathJaxContext = createContext<{ ready: boolean }>({ ready: false });

export function MathJaxProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false);
  return (
    <MathJaxContext.Provider value={{ ready }}>
      <Script id="mathjax-config" strategy="beforeInteractive">
        {`window.MathJax = ${JSON.stringify(MATHJAX_CONFIG)};`}
      </Script>
      <Script
        id="mathjax"
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"
        strategy="afterInteractive"
        onReady={() => setReady(true)}
        onLoad={() => setReady(true)}
      />
      {children}
    </MathJaxContext.Provider>
  );
}

/**
 * Typesets a subtree whenever its dependencies change. Returns a ref to attach.
 * Re-typesetting is required because questions swap in/out client-side.
 */
export function useTypeset<T extends HTMLElement>(deps: unknown[] = []) {
  const ref = useRef<T | null>(null);
  const { ready } = useContext(MathJaxContext);

  const run = useCallback(() => {
    const el = ref.current;
    if (!el || !window.MathJax?.typesetPromise) return;
    window.MathJax.typesetClear?.([el]);
    void window.MathJax.typesetPromise([el]).catch(() => {
      /* a malformed expression must not break the page */
    });
  }, []);

  useEffect(() => {
    if (!ready) return;
    run();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready, run, ...deps]);

  return ref;
}
