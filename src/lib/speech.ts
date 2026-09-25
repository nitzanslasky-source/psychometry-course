"use client";

/**
 * Text-to-speech with the browser's built-in voices (no audio files, works offline).
 * English words in an English voice; Hebrew meanings in a Hebrew voice when the device has one.
 */

let voices: SpeechSynthesisVoice[] = [];
function loadVoices() {
  if (typeof window === "undefined" || !window.speechSynthesis) return;
  voices = window.speechSynthesis.getVoices();
}
if (typeof window !== "undefined" && window.speechSynthesis) {
  loadVoices();
  window.speechSynthesis.onvoiceschanged = loadVoices;
}

const PREFERRED_EN = ["Samantha", "Google US English", "Karen", "Daniel", "Alex"];

export function pickVoice(lang: "en" | "he"): SpeechSynthesisVoice | null {
  if (!voices.length) loadVoices();
  const list = voices.filter((v) => v.lang.toLowerCase().startsWith(lang === "he" ? "he" : "en"));
  if (lang === "en") {
    for (const name of PREFERRED_EN) {
      const v = list.find((x) => x.name.includes(name));
      if (v) return v;
    }
  }
  return list[0] ?? null;
}

export function canSpeak() {
  return typeof window !== "undefined" && "speechSynthesis" in window;
}

export function hasHebrewVoice() {
  return !!pickVoice("he");
}

/** Speak one text; resolves when finished (or immediately if unsupported / cancelled). */
export function speak(text: string, lang: "en" | "he" = "en", rate = 1): Promise<void> {
  return new Promise((resolve) => {
    if (!canSpeak() || !text) return resolve();
    const u = new SpeechSynthesisUtterance(text);
    const v = pickVoice(lang);
    if (v) u.voice = v;
    u.lang = v?.lang || (lang === "he" ? "he-IL" : "en-US");
    u.rate = rate;
    u.onend = () => resolve();
    u.onerror = () => resolve();
    window.speechSynthesis.speak(u);
  });
}

export function stopSpeaking() {
  if (canSpeak()) window.speechSynthesis.cancel();
}

export const wait = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));
