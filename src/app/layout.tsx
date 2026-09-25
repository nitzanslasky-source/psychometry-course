import type { Metadata } from "next";
import Link from "next/link";
import { Inter, Instrument_Serif } from "next/font/google";
import { MathJaxProvider } from "@/components/MathJaxProvider";
import { NavLinks } from "@/components/NavLinks";
import { Search } from "@/components/Search";
import { AccountButton } from "@/components/AccountButton";
import { SyncProvider } from "@/components/SyncProvider";
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
            <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-x-6 px-6 pt-3 md:h-16 md:flex-nowrap md:pt-0">
              <Link href="/" className="pressable flex shrink-0 items-baseline gap-2">
                <span className="font-serif text-[26px] leading-none tracking-tight">Psychometry</span>
                <span className="eyebrow hidden xl:inline">The complete course</span>
              </Link>
              <div className="order-last -mx-6 w-[calc(100%+3rem)] min-w-0 px-4 py-2 md:order-none md:mx-0 md:w-auto md:flex-1 md:px-0 md:py-0">
                <NavLinks />
              </div>
              <div className="flex items-center gap-2">
                <Search />
                <AccountButton />
              </div>
            </div>
          </header>
          <SyncProvider />
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
