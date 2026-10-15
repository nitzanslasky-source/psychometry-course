"""Hand-written board items for AI-narrated videos (2026-10-10 handwriting test).

An item {'k': 'hw', 't': <text>, 'size', 'x', 'y', 'w', 'hw': {...}} is drawn on the board as single-line pen strokes in the
teacher's pen colour (red #d62d48, like her pen in the studio) instead of typeset text. In auto-narrate a WRITE line
({'appear': i, 'write': 1}) draws its strokes one by one at pen speed, timed to the voice (studio_autonarrate.py);
anywhere else (teacher's manual clicks, layout checks, the final state) the item is simply the finished strokes.

Font: the Hershey "Simplex Roman" single-stroke font (futural), converted to coordinates. Data from the Hershey-Fonts
package (MIT, (c) 2020 apshu). Hershey font use condition (USENET distribution, kept here as required):
  - The Hershey Fonts were originally created by Dr. A. V. Hershey while working at the U.S. National Bureau of Standards.
  - The format of the Font data in this distribution was originally created by James Hurt, Cognition, Inc., 900
    Technology Park Drive, Billerica, MA 01821.
  - The font data may be converted into any other format EXCEPT the format distributed by the U.S. NTIS.
The glyphs are made to look written (not typeset) here at build time: per-glyph jitter in size, baseline, slant and
rotation, narrower letters, smoothed curves with a slight pen wobble; operators, arrows, the diamond and fractions are
own pen strokes. Deterministic (seeded by the text), so a rebuild gives the same handwriting.

Text syntax (write(...)):   {a/b} stacked fraction (hand-drawn bar)   ^{..} or ^c power   √{..} root
                            \hl{name}{..} a part POINT / mark cues can target ('item N: name'), like in TeX items
Characters: A-Z a-z 0-9 space + - − × ÷ = ( ) / , . : ? ! ' < > ≤ ≥ ≠ ✓ ✗ | · ↑ ↓ → ← ⇒ ◆ ° π
Output (item['hw']): strokes in an em-100 box (size 100 -> cap height 72): {'s': [[x,y,x,y,...], ...], 'w', 'h', 'n'
(glyph count, for the writing speed), 'parts': {name: [first stroke, end stroke]}}.
"""
import math, random, re, hashlib

# Hershey Simplex Roman (futural): char -> (left, right, 'x,y x,y;x,y ...')  y down, baseline 9, cap line -12
HERSHEY = {
    ' ': (-8, 8, ''),
    '!': (-5, 5, '0,-12 0,2;0,7 -1,8 0,9 1,8 0,7'),
    '"': (-8, 8, '-4,-12 -4,-5;4,-12 4,-5'),
    '#': (-10, 11, '1,-16 -6,16;7,-16 0,16;-6,-3 8,-3;-7,3 7,3'),
    '$': (-10, 10, '-2,-16 -2,13;2,-16 2,13;7,-9 5,-11 2,-12 -2,-12 -5,-11 -7,-9 -7,-7 -6,-5 -5,-4 -3,-3 3,-1 5,0 6,1 7,3 7,6 5,8 2,9 -2,9 -5,8 -7,6'),
    '%': (-12, 12, '9,-12 -9,9;-4,-12 -2,-10 -2,-8 -3,-6 -5,-5 -7,-5 -9,-7 -9,-9 -8,-11 -6,-12 -4,-12 -2,-11 1,-10 4,-10 7,-11 9,-12;5,2 3,3 2,5 2,7 4,9 6,9 8,8 9,6 9,4 7,2 5,2'),
    '&': (-13, 13, '10,-3 10,-4 9,-5 8,-5 7,-4 6,-2 4,3 2,6 0,8 -2,9 -6,9 -8,8 -9,7 -10,5 -10,3 -9,1 -8,0 -1,-4 0,-5 1,-7 1,-9 0,-11 -2,-12 -4,-11 -5,-9 -5,-7 -4,-4 -2,-1 3,6 5,8 7,9 9,9 10,8 10,7'),
    "'": (-5, 5, '0,-10 -1,-11 0,-12 1,-11 1,-9 0,-7 -1,-6'),
    '(': (-7, 7, '4,-16 2,-14 0,-11 -2,-7 -3,-2 -3,2 -2,7 0,11 2,14 4,16'),
    ')': (-7, 7, '-4,-16 -2,-14 0,-11 2,-7 3,-2 3,2 2,7 0,11 -2,14 -4,16'),
    '*': (-8, 8, '0,-6 0,6;-5,-3 5,3;5,-3 -5,3'),
    '+': (-13, 13, '0,-9 0,9;-9,0 9,0'),
    ',': (-4, 4, '1,5 0,6 -1,5 0,4 1,5 1,7 -1,9'),
    '-': (-13, 13, '-9,0 9,0'),
    '.': (-4, 4, '0,4 -1,5 0,6 1,5 0,4'),
    '/': (-11, 11, '9,-16 -9,16'),
    '0': (-10, 10, '-1,-12 -4,-11 -6,-8 -7,-3 -7,0 -6,5 -4,8 -1,9 1,9 4,8 6,5 7,0 7,-3 6,-8 4,-11 1,-12 -1,-12'),
    '1': (-10, 10, '-4,-8 -2,-9 1,-12 1,9'),
    '2': (-10, 10, '-6,-7 -6,-8 -5,-10 -4,-11 -2,-12 2,-12 4,-11 5,-10 6,-8 6,-6 5,-4 3,-1 -7,9 7,9'),
    '3': (-10, 10, '-5,-12 6,-12 0,-4 3,-4 5,-3 6,-2 7,1 7,3 6,6 4,8 1,9 -2,9 -5,8 -6,7 -7,5'),
    '4': (-10, 10, '3,-12 -7,2 8,2;3,-12 3,9'),
    '5': (-10, 10, '5,-12 -5,-12 -6,-3 -5,-4 -2,-5 1,-5 4,-4 6,-2 7,1 7,3 6,6 4,8 1,9 -2,9 -5,8 -6,7 -7,5'),
    '6': (-10, 10, '6,-9 5,-11 2,-12 0,-12 -3,-11 -5,-8 -6,-3 -6,2 -5,6 -3,8 0,9 1,9 4,8 6,6 7,3 7,2 6,-1 4,-3 1,-4 0,-4 -3,-3 -5,-1 -6,2'),
    '7': (-10, 10, '7,-12 -3,9;-7,-12 7,-12'),
    '8': (-10, 10, '-2,-12 -5,-11 -6,-9 -6,-7 -5,-5 -3,-4 1,-3 4,-2 6,0 7,2 7,5 6,7 5,8 2,9 -2,9 -5,8 -6,7 -7,5 -7,2 -6,0 -4,-2 -1,-3 3,-4 5,-5 6,-7 6,-9 5,-11 2,-12 -2,-12'),
    '9': (-10, 10, '6,-5 5,-2 3,0 0,1 -1,1 -4,0 -6,-2 -7,-5 -7,-6 -6,-9 -4,-11 -1,-12 0,-12 3,-11 5,-9 6,-5 6,0 5,5 3,8 0,9 -2,9 -5,8 -6,6'),
    ':': (-4, 4, '0,-3 -1,-2 0,-1 1,-2 0,-3;0,4 -1,5 0,6 1,5 0,4'),
    ';': (-4, 4, '0,-3 -1,-2 0,-1 1,-2 0,-3;1,5 0,6 -1,5 0,4 1,5 1,7 -1,9'),
    '<': (-12, 12, '8,-9 -8,0 8,9'),
    '=': (-13, 13, '-9,-3 9,-3;-9,3 9,3'),
    '>': (-12, 12, '-8,-9 8,0 -8,9'),
    '?': (-9, 9, '-6,-7 -6,-8 -5,-10 -4,-11 -2,-12 2,-12 4,-11 5,-10 6,-8 6,-6 5,-4 4,-3 0,-1 0,2;0,7 -1,8 0,9 1,8 0,7'),
    '@': (-13, 14, '5,-4 4,-6 2,-7 -1,-7 -3,-6 -4,-5 -5,-2 -5,1 -4,3 -2,4 1,4 3,3 4,1;-1,-7 -3,-5 -4,-2 -4,1 -3,3 -2,4;5,-7 4,1 4,3 6,4 8,4 10,2 11,-1 11,-3 10,-6 9,-8 7,-10 5,-11 2,-12 -1,-12 -4,-11 -6,-10 -8,-8 -9,-6 -10,-3 -10,0 -9,3 -8,5 -6,7 -4,8 -1,9 2,9 5,8 7,7 8,6;6,-7 5,1 5,3 6,4'),
    'A': (-9, 9, '0,-12 -8,9;0,-12 8,9;-5,2 5,2'),
    'B': (-11, 10, '-7,-12 -7,9;-7,-12 2,-12 5,-11 6,-10 7,-8 7,-6 6,-4 5,-3 2,-2;-7,-2 2,-2 5,-1 6,0 7,2 7,5 6,7 5,8 2,9 -7,9'),
    'C': (-10, 11, '8,-7 7,-9 5,-11 3,-12 -1,-12 -3,-11 -5,-9 -6,-7 -7,-4 -7,1 -6,4 -5,6 -3,8 -1,9 3,9 5,8 7,6 8,4'),
    'D': (-11, 10, '-7,-12 -7,9;-7,-12 0,-12 3,-11 5,-9 6,-7 7,-4 7,1 6,4 5,6 3,8 0,9 -7,9'),
    'E': (-10, 9, '-6,-12 -6,9;-6,-12 7,-12;-6,-2 2,-2;-6,9 7,9'),
    'F': (-10, 8, '-6,-12 -6,9;-6,-12 7,-12;-6,-2 2,-2'),
    'G': (-10, 11, '8,-7 7,-9 5,-11 3,-12 -1,-12 -3,-11 -5,-9 -6,-7 -7,-4 -7,1 -6,4 -5,6 -3,8 -1,9 3,9 5,8 7,6 8,4 8,1;3,1 8,1'),
    'H': (-11, 11, '-7,-12 -7,9;7,-12 7,9;-7,-2 7,-2'),
    'I': (-4, 4, '0,-12 0,9'),
    'J': (-8, 8, '4,-12 4,4 3,7 2,8 0,9 -2,9 -4,8 -5,7 -6,4 -6,2'),
    'K': (-11, 10, '-7,-12 -7,9;7,-12 -7,2;-2,-3 7,9'),
    'L': (-10, 7, '-6,-12 -6,9;-6,9 6,9'),
    'M': (-12, 12, '-8,-12 -8,9;-8,-12 0,9;8,-12 0,9;8,-12 8,9'),
    'N': (-11, 11, '-7,-12 -7,9;-7,-12 7,9;7,-12 7,9'),
    'O': (-11, 11, '-2,-12 -4,-11 -6,-9 -7,-7 -8,-4 -8,1 -7,4 -6,6 -4,8 -2,9 2,9 4,8 6,6 7,4 8,1 8,-4 7,-7 6,-9 4,-11 2,-12 -2,-12'),
    'P': (-11, 10, '-7,-12 -7,9;-7,-12 2,-12 5,-11 6,-10 7,-8 7,-5 6,-3 5,-2 2,-1 -7,-1'),
    'Q': (-11, 11, '-2,-12 -4,-11 -6,-9 -7,-7 -8,-4 -8,1 -7,4 -6,6 -4,8 -2,9 2,9 4,8 6,6 7,4 8,1 8,-4 7,-7 6,-9 4,-11 2,-12 -2,-12;1,5 7,11'),
    'R': (-11, 10, '-7,-12 -7,9;-7,-12 2,-12 5,-11 6,-10 7,-8 7,-6 6,-4 5,-3 2,-2 -7,-2;0,-2 7,9'),
    'S': (-10, 10, '7,-9 5,-11 2,-12 -2,-12 -5,-11 -7,-9 -7,-7 -6,-5 -5,-4 -3,-3 3,-1 5,0 6,1 7,3 7,6 5,8 2,9 -2,9 -5,8 -7,6'),
    'T': (-8, 8, '0,-12 0,9;-7,-12 7,-12'),
    'U': (-11, 11, '-7,-12 -7,3 -6,6 -4,8 -1,9 1,9 4,8 6,6 7,3 7,-12'),
    'V': (-9, 9, '-8,-12 0,9;8,-12 0,9'),
    'W': (-12, 12, '-10,-12 -5,9;0,-12 -5,9;0,-12 5,9;10,-12 5,9'),
    'X': (-10, 10, '-7,-12 7,9;7,-12 -7,9'),
    'Y': (-9, 9, '-8,-12 0,-2 0,9;8,-12 0,-2'),
    'Z': (-10, 10, '7,-12 -7,9;-7,-12 7,-12;-7,9 7,9'),
    '[': (-7, 7, '-3,-16 -3,16;-2,-16 -2,16;-3,-16 4,-16;-3,16 4,16'),
    '\\': (-7, 7, '-7,-12 7,12'),
    ']': (-7, 7, '2,-16 2,16;3,-16 3,16;-4,-16 3,-16;-4,16 3,16'),
    '^': (-8, 8, '0,-14 -8,0;0,-14 8,0'),
    '_': (-9, 9, '-9,16 9,16'),
    '`': (-4, 4, '1,-7 -1,-5 -1,-3 0,-2 1,-3 0,-4 -1,-3'),
    'a': (-9, 10, '6,-5 6,9;6,-2 4,-4 2,-5 -1,-5 -3,-4 -5,-2 -6,1 -6,3 -5,6 -3,8 -1,9 2,9 4,8 6,6'),
    'b': (-10, 9, '-6,-12 -6,9;-6,-2 -4,-4 -2,-5 1,-5 3,-4 5,-2 6,1 6,3 5,6 3,8 1,9 -2,9 -4,8 -6,6'),
    'c': (-9, 9, '6,-2 4,-4 2,-5 -1,-5 -3,-4 -5,-2 -6,1 -6,3 -5,6 -3,8 -1,9 2,9 4,8 6,6'),
    'd': (-9, 10, '6,-12 6,9;6,-2 4,-4 2,-5 -1,-5 -3,-4 -5,-2 -6,1 -6,3 -5,6 -3,8 -1,9 2,9 4,8 6,6'),
    'e': (-9, 9, '-6,1 6,1 6,-1 5,-3 4,-4 2,-5 -1,-5 -3,-4 -5,-2 -6,1 -6,3 -5,6 -3,8 -1,9 2,9 4,8 6,6'),
    'f': (-5, 7, '5,-12 3,-12 1,-11 0,-8 0,9;-3,-5 4,-5'),
    'g': (-9, 10, '6,-5 6,11 5,14 4,15 2,16 -1,16 -3,15;6,-2 4,-4 2,-5 -1,-5 -3,-4 -5,-2 -6,1 -6,3 -5,6 -3,8 -1,9 2,9 4,8 6,6'),
    'h': (-9, 10, '-5,-12 -5,9;-5,-1 -2,-4 0,-5 3,-5 5,-4 6,-1 6,9'),
    'i': (-4, 4, '-1,-12 0,-11 1,-12 0,-13 -1,-12;0,-5 0,9'),
    'j': (-5, 5, '0,-12 1,-11 2,-12 1,-13 0,-12;1,-5 1,12 0,15 -2,16 -4,16'),
    'k': (-9, 8, '-5,-12 -5,9;5,-5 -5,5;-1,1 6,9'),
    'l': (-4, 4, '0,-12 0,9'),
    'm': (-15, 15, '-11,-5 -11,9;-11,-1 -8,-4 -6,-5 -3,-5 -1,-4 0,-1 0,9;0,-1 3,-4 5,-5 8,-5 10,-4 11,-1 11,9'),
    'n': (-9, 10, '-5,-5 -5,9;-5,-1 -2,-4 0,-5 3,-5 5,-4 6,-1 6,9'),
    'o': (-9, 10, '-1,-5 -3,-4 -5,-2 -6,1 -6,3 -5,6 -3,8 -1,9 2,9 4,8 6,6 7,3 7,1 6,-2 4,-4 2,-5 -1,-5'),
    'p': (-10, 9, '-6,-5 -6,16;-6,-2 -4,-4 -2,-5 1,-5 3,-4 5,-2 6,1 6,3 5,6 3,8 1,9 -2,9 -4,8 -6,6'),
    'q': (-9, 10, '6,-5 6,16;6,-2 4,-4 2,-5 -1,-5 -3,-4 -5,-2 -6,1 -6,3 -5,6 -3,8 -1,9 2,9 4,8 6,6'),
    'r': (-7, 6, '-3,-5 -3,9;-3,1 -2,-2 0,-4 2,-5 5,-5'),
    's': (-8, 9, '6,-2 5,-4 2,-5 -1,-5 -4,-4 -5,-2 -4,0 -2,1 3,2 5,3 6,5 6,6 5,8 2,9 -1,9 -4,8 -5,6'),
    't': (-5, 7, '0,-12 0,5 1,8 3,9 5,9;-3,-5 4,-5'),
    'u': (-9, 10, '-5,-5 -5,5 -4,8 -2,9 1,9 3,8 6,5;6,-5 6,9'),
    'v': (-8, 8, '-6,-5 0,9;6,-5 0,9'),
    'w': (-11, 11, '-8,-5 -4,9;0,-5 -4,9;0,-5 4,9;8,-5 4,9'),
    'x': (-8, 9, '-5,-5 6,9;6,-5 -5,9'),
    'y': (-8, 8, '-6,-5 0,9;6,-5 0,9 -2,13 -4,15 -6,16 -7,16'),
    'z': (-8, 9, '6,-5 -5,9;-5,-5 6,-5;-5,9 6,9'),
    '{': (-7, 7, '2,-16 0,-15 -1,-14 -2,-12 -2,-10 -1,-8 0,-7 1,-5 1,-3 -1,-1;0,-15 -1,-13 -1,-11 0,-9 1,-8 2,-6 2,-4 1,-2 -3,0 1,2 2,4 2,6 1,8 0,9 -1,11 -1,13 0,15;-1,1 1,3 1,5 0,7 -1,8 -2,10 -2,12 -1,14 0,15 2,16'),
    '|': (-4, 4, '0,-16 0,16'),
    '}': (-7, 7, '-2,-16 0,-15 1,-14 2,-12 2,-10 1,-8 0,-7 -1,-5 -1,-3 1,-1;0,-15 1,-13 1,-11 0,-9 -1,-8 -2,-6 -2,-4 -1,-2 3,0 -1,2 -2,4 -2,6 -1,8 0,9 1,11 1,13 0,15;1,1 -1,3 -1,5 0,7 1,8 2,10 2,12 1,14 0,15 -2,16'),
    '~': (-12, 12, '-9,3 -9,1 -8,-2 -6,-3 -4,-3 -2,-2 2,1 4,2 6,2 8,1 9,-1;-9,1 -8,-1 -6,-2 -4,-2 -2,-1 2,2 4,3 6,3 8,2 9,-1 9,-3'),
    '\x7f': (-8, 8, '-8,-12 -8,9 -7,9 -7,-12 -6,-12 -6,9 -5,9 -5,-12 -4,-12 -4,9 -3,9 -3,-12 -2,-12 -2,9 -1,9 -1,-12 0,-12 0,9 1,9 1,-12 2,-12 2,9 3,9 3,-12 4,-12 4,9 5,9 5,-12 6,-12 6,9 7,9 7,-12 8,-12 8,9'),
}

INK = '#d62d48'          # the studio pen's red (the teacher's pen colour in her takes)
# 2026-10-15 teacher decision: the pen colour follows the subject - ALGEBRA (topics 1-20) keeps the red pen; every other
# topic (word problems 21-29, geometry 30-38, 51 psychometric thinking, 52 charts) writes in dark blue. Red keeps its
# other meanings everywhere (crosses on wrong choices, wrong paths, traps). Studio side: hwInk(v) below.
INK_BLUE = '#1e3a8a'


def ink_for_topic(topic):
    try: t = int(topic)
    except (TypeError, ValueError): return INK_BLUE
    return INK if 1 <= t <= 20 else INK_BLUE
UNIT = 72 / 21           # Hershey units -> em-100 px (cap height 21 units = 72)
OPS = set('+=-−×÷<>')

# own pen strokes (baseline 0, left edge 0, y down): char -> (advance, [[(x, y), ...], ...])
def _diamond():
    out = [[(8, -19), (15.2, -9.5), (8, 0), (0.8, -9.5), (8.3, -19.3)]]
    zz = []
    for k, y in enumerate((-15.5, -13, -10.5, -8, -5.5, -3.5)):
        h = 7 * (1 - abs(y + 9.5) / 9.5) * .8
        zz += [(8 - h, y), (8 + h, y)] if k % 2 == 0 else [(8 + h, y), (8 - h, y)]
    return out + [zz]
CUSTOM = {
    '×': (17, [[(4, -14), (13, -5)], [(13, -14), (4, -5)]]),
    '÷': (19, [[(2, -9), (17, -9)], [(9.4, -14.2), (9.8, -13.4)], [(9.4, -4.6), (9.8, -3.8)]]),
    '−': (19, [[(2, -9), (17, -9)]]),
    '-': (19, [[(2, -9), (17, -9)]]),
    '+': (19, [[(9.5, -16), (9.5, -2)], [(2.5, -9), (16.5, -9)]]),
    '=': (19, [[(2.5, -11.5), (16.5, -11.5)], [(2.5, -6.2), (16.5, -6.2)]]),
    '→': (26, [[(2, -9), (24, -9)], [(17, -14), (24, -9), (17, -4)]]),
    '←': (26, [[(24, -9), (2, -9)], [(9, -14), (2, -9), (9, -4)]]),
    '↑': (14, [[(7, 1), (7, -21)], [(2, -15), (7, -21), (12, -15)]]),
    '↓': (14, [[(7, -21), (7, 1)], [(2, -6), (7, 1), (12, -6)]]),
    '⇒': (26, [[(2, -12), (19, -12)], [(2, -6), (19, -6)], [(15, -17), (24, -9), (15, -1)]]),
    '◆': (17, _diamond()),
    '.': (7, [[(3, -1.6), (3.3, -0.2)]]),
    ',': (7, [[(3.6, -1.8), (3.8, -0.2), (2.2, 3.6)]]),
    ':': (7, [[(3, -12.6), (3.3, -11.4)], [(3, -1.6), (3.3, -0.2)]]),
    '°': (10, [[(5, -21), (3, -19.5), (3.2, -17), (5.2, -16), (7.2, -17.2), (7.2, -19.8), (5, -21)]]),
    # 2026-10-11 (topic 13: inequalities, the "it works" check): own pen strokes like the operators above
    '≤': (19, [[(16, -19), (3, -12.5), (16, -6)], [(3, -1.5), (16, -1.5)]]),
    '≥': (19, [[(3, -19), (16, -12.5), (3, -6)], [(3, -1.5), (16, -1.5)]]),
    '≠': (19, [[(2.5, -11.5), (16.5, -11.5)], [(2.5, -6.2), (16.5, -6.2)], [(13, -17), (6, -0.5)]]),
    '|': (11, [[(5.5, -23), (5.5, 4)]]),        # absolute-value bar: upright, a little air on both sides; stretched to the line (_lay)
    '·': (8, [[(3.8, -9.6), (4.1, -8.6)]]),
    '✗': (19, [[(3, -17), (16, -1)], [(16, -17), (3, -1)]]),
    '✓': (21, [[(2, -9), (7.5, -1.5), (19, -19)]]),
    'π': (17, [[(2, -12), (4.5, -14), (15, -14)], [(6.5, -14), (5.5, -5), (3.5, 0)], [(11.5, -14), (11.8, -3), (13.5, 0)]]),
    ' ': (11, []),
}
NARROW = .86             # handwritten letters are narrower than Hershey's


def _glyph(ch):
    if ch in CUSTOM: return CUSTOM[ch]
    if ch not in HERSHEY: raise ValueError('handwriting: no glyph for %r' % ch)
    L, R, d = HERSHEY[ch]
    st = [[(float(x) - L, float(y) - 9) for x, y in (p.split(',') for p in s.split())] for s in d.split(';') if s.strip()]
    return R - L, st


# ------------------------------------------------------------------------------------------------ parse
def _parse(t, i=0, stop=None, pos=None):
    """-> (nodes, index). nodes: ('c', ch) ('frac', num, den) ('sup', nodes) ('sqrt', nodes) ('hl', name, nodes)"""
    out = []
    while i < len(t):
        c = t[i]
        if stop and c == stop: return out, i
        if pos is not None: pos.append(i)
        if t.startswith('\\hl{', i):
            j = t.index('}', i + 4); name = t[i + 4:j]
            assert t[j + 1] == '{', 'handwriting: \\hl{name}{...}'
            body, k = _parse(t, j + 2, '}'); out.append(('hl', name, body)); i = k + 1; continue
        if c == '{':                                    # {a/b}: a fraction
            num, k = _parse(t, i + 1, '/'); den, k2 = _parse(t, k + 1, '}')
            out.append(('frac', num, den)); i = k2 + 1; continue
        if c == '^':
            if t[i + 1] == '{': body, k = _parse(t, i + 2, '}'); out.append(('sup', body)); i = k + 1
            else: out.append(('sup', [('c', t[i + 1])])); i += 2
            continue
        if c == '√':
            assert t[i + 1] == '{', 'handwriting: √{...}'
            body, k = _parse(t, i + 2, '}'); out.append(('sqrt', body)); i = k + 1; continue
        out.append(('c', c)); i += 1
    return out, i


# ------------------------------------------------------------------------------------------------ layout (Hershey units)
class Box:
    def __init__(self): self.strokes, self.w, self.asc, self.desc, self.parts, self.n = [], 0.0, 0.0, 0.0, {}, 0

    def add(self, other, dx, dy, s=1.0):
        k0 = len(self.strokes)
        for st in other.strokes: self.strokes.append([(dx + x * s, dy + y * s) for x, y in st])
        for name, (a, b) in other.parts.items(): self.parts[name] = [a + k0, b + k0]
        self.asc = max(self.asc, -dy + other.asc * s); self.desc = max(self.desc, dy + other.desc * s); self.n += other.n


def _lay(nodes, rng, starts=None):
    B = Box(); x = 0.0; bars = []
    for nd in nodes:
        if starts is not None: starts.append(len(B.strokes))
        if nd[0] == 'c':
            ch = nd[1]; adv, st = _glyph(ch)
            if ch == ' ': x += adv * (1 + max(-.1, min(.15, rng.gauss(0, .07)))); continue
            op = ch in OPS; nar = 1 if (op or ch in CUSTOM) else NARROW
            sc = 1 + max(-.1, min(.1, rng.gauss(0, .045))); rot = math.radians(rng.gauss(0, 2.2))
            dy = rng.gauss(0, .65); slant = math.tan(math.radians((1.5 if ch == '|' else 7) + rng.gauss(0, 1.8)))
            cx, cy = adv * nar / 2, -9.0
            g = []
            for s in st:
                pts = []
                for px, py in s:
                    px = px * nar - cx; py = py - cy
                    px, py = px * math.cos(rot) - py * math.sin(rot), px * math.sin(rot) + py * math.cos(rot)
                    px, py = px * sc + cx, py * sc + cy + dy
                    pts.append((x + px - (py + 4) * slant, py))
                g.append(pts)
            k0 = len(B.strokes); B.strokes += g
            if ch == '|': bars.append(k0)
            ys = [p[1] for s in g for p in s] or [0]
            B.asc = max(B.asc, -min(ys)); B.desc = max(B.desc, max(ys)); B.n += 1
            x += adv * nar * (1 + rng.gauss(0, .03)) + rng.gauss(0, .4) - (1.5 if op else 0)
        elif nd[0] == 'hl':
            sub = _lay(nd[2], rng); k0 = len(B.strokes); B.add(sub, x, 0); B.parts[nd[1]] = [k0, len(B.strokes)]; x += sub.w
        elif nd[0] == 'sup':
            sub = _lay(nd[1], rng); B.add(sub, x + 1, -12, .62); x += sub.w * .62 + 2
        elif nd[0] == 'frac':
            num, den = _lay(nd[1], rng), _lay(nd[2], rng); s = .9
            W = max(num.w, den.w) * s + 8; ax = -9 + rng.gauss(0, .3)
            B.add(num, x + (W - num.w * s) / 2 + 1, ax - 4.6 - num.desc * s, s)
            B.strokes.append([(x + .5, ax + .5 + rng.gauss(0, .2)), (x + W / 2, ax + rng.gauss(0, .3)), (x + W + .5, ax - .6 + rng.gauss(0, .2))])
            B.n += 1
            B.add(den, x + (W - den.w * s) / 2 + 1, ax + 4.6 + den.asc * s, s)
            x += W + 3
        elif nd[0] == 'sqrt':
            sub = _lay(nd[1], rng); top = -max(sub.asc, 21) - 3.5
            B.strokes.append([(x, -9), (x + 3, -10.5), (x + 6.5, 1.5), (x + 11, top), (x + 15 + sub.w, top + rng.gauss(0, .4))]); B.n += 1
            B.add(sub, x + 13, 0); B.asc = max(B.asc, -top + 1); x += sub.w + 17
    # absolute-value bars reach over everything on the line (a fraction between bars gets tall bars, like |-3/8|)
    if bars and any(nd[0] in ('frac', 'sqrt', 'sup') for nd in nodes):
        top, bot = -max(B.asc, 21) - 1.5, max(B.desc, 2) + 1.5
        for k in bars:
            (x0, y0), (x1, y1) = B.strokes[k][0], B.strokes[k][-1]
            B.strokes[k] = [(x0 + (y0 - top) * .03, top), (x1 - (bot - y1) * .03, bot)]
        B.asc = max(B.asc, -top); B.desc = max(B.desc, bot)
    B.w = x
    return B


# ------------------------------------------------------------------------------------------------ pen look
def _chaikin(pts, it=2):
    for _ in range(it):
        if len(pts) < 3: return pts
        q = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            q += [(.75 * a[0] + .25 * b[0], .75 * a[1] + .25 * b[1]), (.25 * a[0] + .75 * b[0], .25 * a[1] + .75 * b[1])]
        q.append(pts[-1]); pts = q
    return pts


def _smooth(pts):
    """round the polygon curves but keep sharp corners (the top of a 7, the point of a 1)"""
    if len(pts) < 3: return pts
    runs, cur = [], [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        t1, t2 = math.atan2(b[1] - a[1], b[0] - a[0]), math.atan2(c[1] - b[1], c[0] - b[0])
        d = abs((t2 - t1 + math.pi) % (2 * math.pi) - math.pi)
        cur.append(b)
        if d > math.radians(62): runs.append(cur); cur = [b]
    cur.append(pts[-1]); runs.append(cur)
    out = []
    for r in runs:
        r = _chaikin(r) if len(r) > 2 else r
        out += r if not out else r[1:]
    return out


def _resample(pts, step):
    if len(pts) < 2: return pts
    cum = [0.0]
    for a, b in zip(pts, pts[1:]): cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    L = cum[-1]
    if L < step: return [pts[0], pts[-1]]
    n = max(2, int(round(L / step))); out = []; j = 0
    for i in range(n + 1):
        d = L * i / n
        while j < len(cum) - 2 and cum[j + 1] < d: j += 1
        seg = cum[j + 1] - cum[j] or 1; u = (d - cum[j]) / seg
        out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * u, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * u))
    return out


def _wobble(pts, rng, amp):
    p1, p2, f1, f2 = rng.uniform(0, 6.3), rng.uniform(0, 6.3), rng.uniform(.035, .06), rng.uniform(.09, .14)
    out = []; s = 0.0
    for i, (x, y) in enumerate(pts):
        if i: s += math.hypot(x - pts[i - 1][0], y - pts[i - 1][1])
        out.append((x + amp * math.sin(f1 * s + p1), y + amp * .8 * math.sin(f2 * s + p2)))
    return out


_CACHE = {}


def write(text, seed=None):
    """text -> item['hw'] (see the module doc)"""
    key = (text, seed)
    if key in _CACHE: return _CACHE[key]
    rng = random.Random(int(hashlib.md5(('%s|%s' % (text, seed)).encode()).hexdigest()[:8], 16))
    pos = []; nodes, _ = _parse(text, pos=pos)
    starts = []; B = _lay(nodes, rng, starts)
    # gentle baseline drift across the line (a hand never writes perfectly straight)
    ph, fr = rng.uniform(0, 6.3), rng.uniform(.012, .02)
    st = [[(x * UNIT, (y + .9 * math.sin(fr * x + ph)) * UNIT) for x, y in s] for s in B.strokes]
    st = [_wobble(_resample(_smooth(s), 3.2), rng, .55) if len(s) > 1 else s for s in st]
    xs = [p[0] for s in st for p in s]; ys = [p[1] for s in st for p in s]
    x0, y0 = min(xs) - 4, min(min(ys), -21 * UNIT) - 6
    out = {'s': [[round(v, 1) for p in s for v in (p[0] - x0, p[1] - y0)] for s in st],
           'w': round(max(xs) - x0 + 4, 1), 'h': round(max(max(ys), 4 * UNIT) - y0 + 6, 1), 'n': B.n,
           'parts': B.parts,
           # 2026-10-11: [character index in the text, first stroke] of each top-level piece - so the pen can write a
           # line in chunks timed to her words (reading_to_video.py write chunks, studio_autonarrate anWrites)
           'ix': [[a, b] for a, b in zip(pos, starts)]}
    _CACHE[key] = out
    return out


def item(text, size=40, x=None, y=None, w=None, **k):
    """a hand-written board item (like dsl.T)"""
    d = dict(k='hw', t=text, size=size, hw=write(text), **k)
    if x is not None: d['x'] = x
    if y is not None: d['y'] = y
    if w is not None: d['w'] = w
    return d


# ------------------------------------------------------------------------------------------------ studio (renderer)
JS = r"""
/* ---- hand-written items (studio_handwrite.py): single-line pen strokes in the subject's pen colour ---- */
/* 2026-10-15 teacher: algebra (topics 1-20) red pen, every other topic dark blue; crosses stay red (red = wrong).
   hybridSvg sets window.__hwInk for the video being drawn; auto-narrate marks use hwInk(v). Her live pen is separate. */
const HW_INK_RED='#d62d48',HW_INK_BLUE='#1e3a8a';
function hwInk(v){const t=+(v&&v.topic);return t>=1&&t<=20?HW_INK_RED:HW_INK_BLUE}
function hwItem(it,x,y,w){const H=it.hw,W=it.w||w;let k=(it.size||46)/100;if(H.w*k>W)k=W/H.w;
 const sw=Math.max(3,Math.min(5.2,(it.size||46)*.1)).toFixed(1),P=H.parts||{},A={},B={};for(const [n,[a,b]] of Object.entries(P)){(A[a]=A[a]||[]).push(n);(B[b]=B[b]||[]).push(n)}
 let s=`<g fill="none" stroke="${it.color||window.__hwInk||HW_INK_RED}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round" data-hw="${k.toFixed(4)}">`;
 H.s.forEach((p,i)=>{for(const n of B[i]||[])s+=`<g class="hlb-${n}"/>`;for(const n of A[i]||[])s+=`<g class="hla-${n}"/>`;let d='';for(let j=0;j<p.length;j+=2)d+=(j?'L':'M')+(x+p[j]*k).toFixed(1)+' '+(y+p[j+1]*k).toFixed(1);if(p.length===2)d+='l.4 .4';s+=`<path d="${d}"/>`});
 for(const n of B[H.s.length]||[])s+=`<g class="hlb-${n}"/>`;
 return {svg:s+'</g>',h:H.h*k}}
"""

REPL = [
    # 2026-10-15: the pen colour of the video being drawn (hwInk: algebra red, other topics dark blue)
    ("function hybridSvg(v,bi,step){const b=v.beats[bi];", "function hybridSvg(v,bi,step){const b=v.beats[bi];window.__hwInk=hwInk(v);"),
    ("function hyItem(it,x,y,w){const INK=PAL.ink;", "function hyItem(it,x,y,w){const INK=PAL.ink;"
     # 2026-10-11 layered figures (a number line BUILT step by step at the spoken words): an item with over:1 is drawn at
     # the y of the last item before it and takes no room (h 0; its gap is 0), so its layers stack exactly on the base;
     # data-over tells the layout check that the overlap is meant
     # 2026-10-13: a layer with `of` (its figure's id; the base has the same `fig`) is drawn at its OWN figure's place and
     # scale, even when other items were shown in between (e.g. the topic-18 column figures, built at the words)
     "if(it.over&&(window.__hyBaseY!=null||it.of)){const F=it.of&&window.__hyFig&&window.__hyFig[it.of],sv=window.__hyBaseY,sc=F?F.s:(window.__hyBaseScale||1);"
     "const o=Object.assign({},it,{over:0,fig:null});if(sc!==1&&o.w){o.w=Math.round(o.w*sc);o.h=Math.round((o.h||300)*sc)}"
     "const r=hyItem(o,F?F.x:x,F?F.y:window.__hyBaseY,w);window.__hyBaseY=sv;return {svg:'<g data-over=\"1\">'+r.svg+'</g>',h:0}}"
     "window.__hyBaseY=y;window.__hyBaseScale=1;if(it.fig)(window.__hyFig=window.__hyFig||{})[it.fig]={x:x,y:y,s:1};if(it.k==='hw')return hwItem(it,x,y,w);"),
    # a positioned hand-written item takes part in the overlap push-down / shrink-to-fit like a text item
    ("if(it.y!=null&&it.k==='t'){const x1=it.w?", "if(it.y!=null&&(it.k==='t'||it.k==='hw')){const x1=it.w?"),
    # 2026-10-13: a positioned figure (k 'vis', e.g. a right-column column layout) is pushed below what is already placed
    # (the question, earlier items) and scaled down to fit above the answer choices, like a positioned text item; its
    # layers follow its place and scale (`of` above)
    ("placed.push({x0:x,x1,y0:y,y1:y+r.h})}if(it.k==='q')",
     "placed.push({x0:x,x1,y0:y,y1:y+r.h})}else if(it.y!=null&&it.k==='vis'&&!it.over){const iw=it.w||W,ih=it.h||300;let mv=false;"
     "for(const p of placed)if(x<p.x1&&x+iw>p.x0&&y<p.y1+10&&y+ih>p.y0){y=p.y1+14;mv=true}let sc=1;while(y+ih*sc>ctop-10&&sc>.5)sc-=.05;"
     "if(mv||sc<1){r=hyItem(Object.assign({},it,{w:Math.round(iw*sc),h:Math.round(ih*sc)}),x,y,W);window.__hyBaseScale=sc;if(it.fig&&window.__hyFig)window.__hyFig[it.fig].s=sc}"
     "placed.push({x0:x,x1:x+iw*sc,y0:y,y1:y+ih*sc})}if(it.k==='q')"),
    # 2026-10-11: a math question item reports where its answer choices start (ctop), so board items that would run
    # into the choices can be fitted above them (slide_style.py shrink-to-fit; before, only text-layout questions did)
    ("svgText('Figure not necessarily drawn to scale.',x+w,top-6,15,PAL.muted,400,'end')}\n  return {svg:s,h:r.height}}",
     "svgText('Figure not necessarily drawn to scale.',x+w,top-6,15,PAL.muted,400,'end')}\n  return {svg:s,h:r.height,ctop:ch.length?top:900}}"),
]


def apply(html):
    for old, new in REPL:
        assert html.count(old) == 1, ('studio_handwrite anchor', html.count(old), old[:60])
        html = html.replace(old, new)
    k = html.find('function hyItem(')
    return html[:k] + JS.lstrip() + html[k:]
