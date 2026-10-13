"""Apply approved narration overlays, retaining original layout and recording indices.

cue_phrases supports the earlier small phrase-level audit. cue_anchors supports
the subsequent human-reviewed five-lesson batches, by original cue index. Neither
can change a target, cue action, graphic, handwriting plan, or slide/paragraph.
The separately approved counterexample audit may supply reviewed_cues plus
original_cues to remove obsolete tests and align immediate choice elimination.
These changes retain the original item styles and slide/paragraph indices.
"""
import json
from pathlib import Path
_PATH=Path(__file__).with_suffix('.json')
def apply(videos):
    for vid,entries in json.loads(_PATH.read_text())['lessons'].items():
        if vid not in videos:continue
        for change in entries:
            line=videos[vid]['slides'][change['slide']]['lines'][change['paragraph']]
            if line['say']!=change['revised']:
                if line['say']!=change['original']:
                    raise ValueError(f"{vid}: spoken source changed at slide {change['slide']+1}, paragraph {change['paragraph']+1}. Reconcile the clarity overlay before regenerating this lesson.")
                line['say']=change['revised']
            if 'reviewed_cues' in change:
                current=json.loads(json.dumps(line.get('cues',[])))
                if current not in (change['original_cues'],change['reviewed_cues']):
                    raise ValueError(f"{vid}: board cues changed; reconcile the counterexample audit before regenerating.")
                line['cues']=[tuple(c) for c in change['reviewed_cues']]
                continue
            replacements=change.get('cue_phrases',{})
            for ci,cue in enumerate(line.get('cues',[])):
                fi=3 if cue[0]=='mark'else 2
                if cue[fi]in replacements:
                    cue=list(cue);cue[fi]=replacements[cue[fi]];line['cues'][ci]=tuple(cue)
            for anchor in change.get('cue_anchors',[]):
                ci=anchor['index'];cue=list(line['cues'][ci]);fi=3 if cue[0]=='mark'else 2
                if cue[fi]not in (anchor['original'],anchor['revised']):
                    raise ValueError(f"{vid}: cue {ci} changed; reconcile its reviewed narration anchor before regenerating.")
                cue[fi]=anchor['revised'];line['cues'][ci]=tuple(cue)
