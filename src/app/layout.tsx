import type { Metadata } from "next";
import Link from "next/link";
import { Inter, Instrument_Serif } from "next/font/google";
import { MathJaxProvider } from "@/components/MathJaxProvider";
import "./globals.css";

const sans = Inter({ subsets: ["latin"], variable: "--font-sans", display: "swap" });
const serif = Instrument_Serif({
  subsets: ["latin"],
  weight: "400",
  style: ["normal", "italic"],
  variable: "--font-serif",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Psychometry — the complete course",
  description:
    "The complete English course for the NITE psychometric entrance test: Quantitative and Verbal Reasoning, from the first lesson to exam level.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${sans.variable} ${serif.variable}`}>
      <body>
        <MathJaxProvider>
          <header className="material edge-bottom sticky top-0 z-40">
            <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-6 px-6">
              <Link href="/" className="pressable flex items-baseline gap-2">
                <span className="font-serif text-[26px] leading-none tracking-tight">Psychometry</span>
                <span className="eyebrow hidden sm:inline">The complete course</span>
              </Link>
              <nav className="flex items-center gap-1 text-sm">
                <Link href="/#contents" className="pressable rounded-full px-3 py-1.5 text-ink-soft hover:bg-paper-deep">
                  All topics
                </Link>
              </nav>
            </div>
          </header>
          {children}
          <footer className="mt-24 border-t border-line">
            <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-8 text-xs text-muted">
              <span className="font-serif text-base text-ink">Psychometry</span>
              <span>Quantitative &amp; Verbal Reasoning · English edition</span>
            </div>
          </footer>
        </MathJaxProvider>
      </body>
    </html>
  );
}
