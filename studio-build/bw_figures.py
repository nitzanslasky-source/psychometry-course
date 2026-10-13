"""Question figures in black and white, like the real NITE exam (teacher-approved 2026-10-14).

Every QUESTION figure (q['questionVisual']['svg'] and every copy of it on a board / hybrid slide: a k:'q' item's 'fig')
is rewritten here, once, at the end of the build: lines, marks, highlights and labels -> black; shaded regions -> greys;
axes / dashed helper lines -> mid grey. Stroke widths are kept (the thick orange highlight becomes a thick black line).
TEACHING visuals keep their colours: k:'vis' items (method visuals, shaded number lines ...), handwriting, marks,
PAL slide chrome, the pen, overlays. Charts (topic 52) are left coloured for now (SKIP_TOPICS).

    apply(D)      -> stats dict; idempotent (black stays black), called by math_api.apply_patches (math topics) and by
                     build_verbal.py right before the write (also topic 51, built from modulesV51.py)
    unmapped(D)   -> ['colour  (where)', ...] colours in a question figure that the table does not know (must be empty)
    convert(svg, tint_white=None) -> the black-and-white svg

Shades (the "fill" column): the main shade #d9d9d9, a darker band / highlighted part #a6a6a6, a second shaded region
#bfbfbf, a light face of a 3D solid #eeeeee, very light tints -> white. The pale blue BLUE #e8eefb is a region of its
own next to other shading (3D top faces, t36 globe / sectors) -> #eeeeee, but when it is the ONLY tint of a question's
figure it is just a background tint of a plain shape (t38 polygons, spheres) -> white, as on the exam.
"""
import re

SKIP_TOPICS = {52, '52'}
BLACK, MID, LIGHTLINE = '#000000', '#808080', '#bfbfbf'
SHADE, DARK, SHADE2, FACE, WHITE = '#d9d9d9', '#a6a6a6', '#bfbfbf', '#eeeeee', '#ffffff'

# source colour -> (as a fill, as a stroke).  Every colour found in a question figure must be here.
TABLE = {
    # ink, teal marks, orange highlights (lines, arcs, dots, labels)
    '#203344': (BLACK, BLACK),      # ink
    '#087f83': (BLACK, BLACK),      # teal marks / angle arcs / teal labels
    '#bb6821': (BLACK, BLACK),      # orange highlight (stroke-width 6 arcs, orange labels)
    '#c8691c': (BLACK, BLACK),      # orange (t38 dashed circle)
    '#0f766e': (BLACK, BLACK),      # dark teal
    # axis / dashed helper / grid greys
    '#71818d': (MID, '#000000'),   # axis -> black stroke like the exam (dashes stay dashed);, dashes (t17 _AX, t34/t36 GREY, t35 DASH, t37 AXIS)
    '#9aa8c0': (MID, MID),          # t38 GRAY dashed
    '#5b6b7a': (MID, MID),          # muted label
    '#d6b88f': (SHADE2, MID),       # t33 sector outline
    '#c6d4dd': (SHADE, LIGHTLINE),  # t32 grid
    '#b0c4ce': (SHADE, LIGHTLINE),  # t32 grid
    '#b9c6cf': (SHADE, LIGHTLINE),  # t32 grid
    '#e8eef3': (FACE, LIGHTLINE),   # t37 GRID
    # shaded regions
    '#d5f1ed': (SHADE, LIGHTLINE),  # FILL / BAND - the shade
    '#d9efed': (SHADE, LIGHTLINE),  # t31 shaded triangle
    '#dae7f3': (SHADE, LIGHTLINE),  # t31 shaded kite (geo31-g037)
    '#e6f4f1': (SHADE, LIGHTLINE),
    '#5bb8ae': (DARK, MID),         # darker overlap band (_shaded_nl DARK)
    '#efc58b': (DARK, MID),         # t35 HL - the highlighted cube
    '#bfe6e0': (SHADE2, MID),       # t35 water / darker teal face
    '#7fb8ae': (DARK, MID),
    '#f6e3d2': (SHADE2, MID),       # orange-tinted second region (t38)
    '#ffefdc': (SHADE2, MID),       # t32 OFILL
    '#fbe7d6': (SHADE2, MID),       # t37 orange tint
    '#e8eefb': (FACE, LIGHTLINE),   # BLUE: 3D top face / second region (white when it is the only tint, see above)
    '#e8edf8': (FACE, LIGHTLINE),   # t31 second triangle
    # very light tints -> white
    '#f8fbfd': (WHITE, WHITE),      # 3D front face / light
    '#edf3f7': (WHITE, WHITE),      # t35 SQ
    '#eef4fb': (WHITE, WHITE),      # t38 FILL2
    '#eef8f7': (WHITE, WHITE),
    '#e7f4f3': (WHITE, WHITE),
    '#fff8eb': (WHITE, WHITE),
    '#ffffff': (WHITE, WHITE),
    '#000000': (BLACK, BLACK),
    # the targets themselves (idempotent)
    MID: (MID, MID), LIGHTLINE: (LIGHTLINE, LIGHTLINE), SHADE: (SHADE, SHADE), DARK: (DARK, DARK), FACE: (FACE, FACE),
}
TINTS = {'#e8eefb', '#e8edf8'}           # white when they are the only tint of the figure
KEEP = {'none', 'white', 'black', 'transparent', 'currentcolor'}

_ATTR = re.compile(r'\b(fill|stroke|stop-color|color)(\s*=\s*")([^"]*)(")')
_STYLE = re.compile(r'\b(fill|stroke|stop-color)(\s*:\s*)([^;"]+)')


def _norm(c):
    c = c.strip().lower()
    if re.fullmatch(r'#[0-9a-f]{3}', c): c = '#' + ''.join(ch * 2 for ch in c[1:])
    return c


def colours(svg):
    """{normalised colour: set of attribute kinds} used in svg"""
    out = {}
    for rx in (_ATTR, _STYLE):
        for m in rx.finditer(svg):
            out.setdefault(_norm(m.group(3)), set()).add(m.group(1))
    return out


def tint_only(svg):
    """True if the only coloured (non-white, non-ink) fills of the figure are the pale tints of plain shapes"""
    fills = set()
    for el in re.finditer(r'<(\w+)\b([^>]*)>', svg):
        if el.group(1) in ('text', 'tspan'): continue
        m = re.search(r'\bfill\s*=\s*"([^"]*)"', el.group(2))
        if m:
            c = _norm(m.group(1))
            if c in TABLE and TABLE[c][0] not in (BLACK, WHITE, MID): fills.add(c)
    return bool(fills) and fills <= TINTS


def convert(svg, tint_white=None):
    if tint_white is None: tint_white = tint_only(svg)

    def sub(m):
        kind, c = m.group(1), _norm(m.group(3))
        if c in KEEP or c.startswith('url('): return m.group(0)
        if c not in TABLE: return m.group(0)            # reported by unmapped()
        new = TABLE[c][0 if kind in ('fill', 'stop-color', 'color') else 1]
        if tint_white and c in TINTS and kind == 'fill': new = WHITE
        return m.group(1) + m.group(2) + new + m.group(4) if m.re is _ATTR else m.group(1) + m.group(2) + new
    return _STYLE.sub(sub, _ATTR.sub(sub, svg))


def _figs(D):
    """(where, qid, holder dict with 'svg') for every question figure and every board copy of one"""
    for q in D['questions'].values():
        v = q.get('questionVisual')
        if v and v.get('svg') and q.get('topic') not in SKIP_TOPICS: yield 'q:' + q['id'], q['id'], v
    for vid, v in D['videos'].items():
        if v.get('topic') in SKIP_TOPICS: continue
        for bn, b in enumerate(v.get('beats', []), 1):
            for it in b.get('items', []):
                if it.get('k') == 'q' and isinstance(it.get('fig'), dict) and it['fig'].get('svg'):
                    q = D['questions'].get(it.get('qid')) or {}
                    if q.get('topic') in SKIP_TOPICS: continue
                    yield '%s #%d' % (vid, bn), it.get('qid'), it['fig']


def apply(D):
    # tint rule per QUESTION (decided on the question's own figure), so the board copies match the question page
    tw = {}
    for q in D['questions'].values():
        v = q.get('questionVisual')
        if v and v.get('svg'): tw[q['id']] = tint_only(v['svg'])
    n = changed = 0
    for where, qid, h in list(_figs(D)):
        new = convert(h['svg'], tw.get(qid))
        n += 1
        if new != h['svg']: h['svg'] = new; changed += 1
    return dict(figures=n, changed=changed)


def unmapped(D):
    out = []
    for where, qid, h in _figs(D):
        for c in colours(h['svg']):
            if c not in TABLE and c not in KEEP and not c.startswith('url('): out.append('%s  (%s)' % (c, where))
    return out
