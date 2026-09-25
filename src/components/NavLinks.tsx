"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/#contents", match: (p: string) => p === "/" || p.startsWith("/topic"), label: "Course" },
  { href: "/review", match: (p: string) => p.startsWith("/review"), label: "Review" },
  { href: "/simulations", match: (p: string) => p.startsWith("/simulation"), label: "Simulations" },
  { href: "/rules", match: (p: string) => p.startsWith("/rules"), label: "Rules" },
  { href: "/dictionary", match: (p: string) => p.startsWith("/dictionary"), label: "Dictionary" },
  { href: "/listen", match: (p: string) => p.startsWith("/listen"), label: "Listen" },
  { href: "/mental-math", match: (p: string) => p.startsWith("/mental-math"), label: "Mental math" },
];

export function NavLinks() {
  const path = usePathname() || "/";
  return (
    <nav className="flex items-center gap-0.5 overflow-x-auto text-sm [scrollbar-width:none] md:justify-end [&::-webkit-scrollbar]:hidden" aria-label="Main">
      {LINKS.map((l) => {
        const active = l.match(path);
        return (
          <Link
            key={l.href}
            href={l.href}
            aria-current={active ? "page" : undefined}
            className={["pressable whitespace-nowrap rounded-full px-3 py-1.5 transition-colors", active ? "bg-ink text-white" : "text-ink-soft hover:bg-paper-deep"].join(" ")}
          >
            {l.label}
          </Link>
        );
      })}
    </nav>
  );
}
