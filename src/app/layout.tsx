import type { Metadata } from "next";
import Link from "next/link";
import { MathJaxProvider } from "@/components/MathJaxProvider";
import "./globals.css";


export const metadata: Metadata = {
  title: "Psychometry Course — the complete English course",
  description:
    "The complete English course for the NITE psychometric entrance test: Quantitative and Verbal Reasoning, from the first lesson to exam level.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <MathJaxProvider>
          <header className="material-bar sticky top-0 z-30">
            <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-5 py-3">
              <Link href="/" className="pressable flex items-center gap-2 rounded-lg">
                <span className="flex h-8 w-8 items-center justify-center rounded-[10px] bg-brand-600 text-lg font-bold text-white shadow-soft">
                  Ψ
                </span>
                <span className="font-semibold">Psychometry Course</span>
              </Link>
              <nav className="text-sm">
                <Link href="/" className="link-subtle">
                  All topics
                </Link>
              </nav>
            </div>
          </header>
          {children}
        </MathJaxProvider>
      </body>
    </html>
  );
}
