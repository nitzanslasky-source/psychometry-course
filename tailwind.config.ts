import type { Config } from "tailwindcss";

/**
 * Psychometry Course — visual identity.
 * Deep ink navy + warm paper, one restrained gold accent, and a quiet colour per subject
 * (used only as small markers: numerals, rules, dots — never as big fills).
 */
export default {
  darkMode: "class",
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: { DEFAULT: "#101826", soft: "#2b3445" },
        muted: "#6e7481",
        faint: "#9aa0ab",
        line: "#e7e3da",
        paper: { DEFAULT: "#fbfaf7", deep: "#f4f1ea" },
        gold: { DEFAULT: "#a8812e", soft: "#f3ead3", deep: "#7d5f1f" },
        // aliases used by the exam-simulation components (copied from the elite project)
        hair: "#e7e3da",
        brand: { 50: "#f3ead3", 300: "#d9bf80", 500: "#a8812e", 700: "#7d5f1f" },
        ok: "#1f7a4d",
        bad: "#b3261e",
        subj: {
          algebra: "#3d5a99",
          words: "#2f7d74",
          geometry: "#b0662b",
          verbal: "#8a4a6b",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "-apple-system", "Segoe UI", "Arial", "sans-serif"],
        serif: ["var(--font-serif)", "Georgia", "serif"],
      },
      boxShadow: {
        soft: "0 1px 2px rgb(16 24 38 / 0.04), 0 2px 8px rgb(16 24 38 / 0.04)",
        lift: "0 2px 4px rgb(16 24 38 / 0.04), 0 12px 32px -8px rgb(16 24 38 / 0.14)",
      },
      maxWidth: { read: "44rem" },
    },
  },
  plugins: [],
} satisfies Config;
