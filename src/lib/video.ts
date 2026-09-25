import "server-only";

import { createHash } from "node:crypto";
import type { VideoSource } from "./fullCourseTypes";

/** What the player needs: an embeddable page (Bunny) or a plain file URL. */
export type VideoEmbed = { kind: "iframe"; src: string } | { kind: "file"; src: string };

/**
 * Build the player URL for a recorded video. With BUNNY_TOKEN_KEY set, the link is signed and expires after
 * a few hours, so it can't be shared or embedded elsewhere (Bunny → Stream library → Security → Token authentication).
 * Server only (reads the secret); returns null for videos not recorded yet.
 */
export function videoEmbed(src: VideoSource | undefined): VideoEmbed | null {
  if (!src) return null;
  if (src.provider === "url") return { kind: "file", src: src.url };
  const base = `https://iframe.mediadelivery.net/embed/${src.libraryId}/${src.videoGuid}`;
  const params = new URLSearchParams({ autoplay: "false", preload: "true", responsive: "true" });
  const secret = process.env.BUNNY_TOKEN_KEY;
  if (secret) {
    const expires = Math.floor(Date.now() / 1000) + 6 * 3600;
    params.set("token", createHash("sha256").update(secret + src.videoGuid + expires).digest("hex"));
    params.set("expires", String(expires));
  }
  return { kind: "iframe", src: `${base}?${params}` };
}
