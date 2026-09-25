import type { Config } from "tailwindcss";

export default {
  darkMode: "class",
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Warmed off pure neutrals so text/borders sit comfortably against the paper-toned surfaces below.
        ink: "#211c15",
        muted: "#6b6255",
        hair: "#e4ddd1",
        ok: "#0a7f33",
        bad: "#c02626",
        // Brand palette — a warm clay/terracotta primary (replaces a generic SaaS indigo),
        // amber accent kept for "focus here" callouts since it already reads warm alongside it.
        brand: {
          50: "#fdf4ef",
          100: "#fbe6da",
          200: "#f5c9ab",
          300: "#eda374",
          400: "#e07d47",
          500: "#c96130",
          600: "#ad4a21",
          700: "#8c3a1b",
          800: "#6f2f19",
          900: "#5b2818",
          950: "#311209",
        },
        accent: {
          50: "#fffbeb",
          100: "#fef3c7",
          400: "#fbbf24",
          500: "#f59e0b",
          600: "#d97706",
        },
        // Dark-mode surfaces, referenced via dark: variants.
        surface: {
          DEFAULT: "#fffdfa",
          dark: "#1c1811",
        },
        canvas: {
          DEFAULT: "#faf7f2",
          dark: "#15120e",
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "Inter",
          "Segoe UI",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
        display: ["var(--font-display)", "ui-serif", "Georgia", "serif"],
      },
      boxShadow: {
        soft: "0 1px 2px 0 rgb(0 0 0 / 0.04), 0 1px 3px 0 rgb(0 0 0 / 0.06)",
        card: "0 1px 3px 0 rgb(0 0 0 / 0.06), 0 4px 12px -2px rgb(0 0 0 / 0.06)",
        "card-hover": "0 4px 10px -2px rgb(0 0 0 / 0.08), 0 10px 24px -4px rgb(0 0 0 / 0.10)",
        glow: "0 0 0 1px rgb(99 102 241 / 0.15), 0 8px 24px -4px rgb(99 102 241 / 0.25)",
      },
      backgroundImage: {
        "grid-pattern":
          "linear-gradient(to right, rgb(0 0 0 / 0.035) 1px, transparent 1px), linear-gradient(to bottom, rgb(0 0 0 / 0.035) 1px, transparent 1px)",
      },
      animation: {
        "fade-in": "fade-in 0.4s ease-out",
        "slide-up": "slide-up 0.4s ease-out",
      },
      keyframes: {
        "fade-in": { from: { opacity: "0" }, to: { opacity: "1" } },
        "slide-up": {
          from: { opacity: "0", transform: "translateY(8px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
