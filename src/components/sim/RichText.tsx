/**
 * Renders text that may contain simple <b>...</b> markup, as used throughout the
 * exam corpus (question stems, options, and cluster intros).
 *
 * Kept deliberately minimal: the corpus only ever uses <b>, and rendering via
 * split/strong avoids dangerouslySetInnerHTML on content that is authored data.
 */
export function RichText({ text }: { text: string }) {
  const parts = text.split(/(<\/?b>)/g);
  let bold = false;
  return (
    <>
      {parts.map((p, i) => {
        if (p === "<b>") {
          bold = true;
          return null;
        }
        if (p === "</b>") {
          bold = false;
          return null;
        }
        return bold ? <strong key={i}>{p}</strong> : <span key={i}>{p}</span>;
      })}
    </>
  );
}
