"""Display-only notation and sentence grouping. Never used for spoken take text."""
import json,re
from pathlib import Path

UNIT={w:i for i,w in enumerate('zero one two three four five six seven eight nine'.split())}
ORD=dict(first=1,second=2,third=3,fourth=4,fifth=5,sixth=6,seventh=7,eighth=8,ninth=9,tenth=10)
SUP=str.maketrans('0123456789−-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁻')
N=r'(?:\d+(?:\.\d+)?(?:/\d+)?|'+'|'.join(UNIT)+r')'
V=r'[A-HJ-Za-hj-z]'
OPERAND_V=r'(?:[B-HJ-Zb-hj-z]|(?-i:A)|a(?=\s*(?:[,.!?;:+−×÷=/<>²³⁴⁵⁶⁷⁸⁹⁰ⁿ^)]|$|squared\b|cubed\b|to the\b|times\b|plus\b|minus\b|over\b|equals\b|is\b)))'
# Every operand has token boundaries, so words such as "an" are never variables.
SIMPLE=rf'(?:−?{N}|{OPERAND_V})'
GROUP=r'\([^(),.;!?]+\)'
BASE=rf'(?:{GROUP}|\|[^|]+\||{SIMPLE})'
POWER=r'(?:[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+|\^\([−\d/]+\))?'
ATOM=rf'(?<![\w/])(?:[²³⁴⁵⁶⁷⁸⁹]?√)?(?:−?(?:\d+{V})|{BASE}){POWER}(?![\w/])'

def number(s):
    return str(UNIT[s.lower()]) if s.lower() in UNIT else s

def _spoken_group_power(m,e,power):
    """2026-10-15: a spoken comma before squared/cubed squares everything before it: "x minus y, squared" is (x − y)²,
    so after an operator the words stay; "three a, squared" is (3a)², never 3a²."""
    if ',' in m[0][len(m[1]):]:
        if re.search(r'(?:[+−×÷/]|\b(?:plus|minus|times|over|divided by))\s*$',m.string[:m.start()]):return m[0]
        if re.fullmatch(r'\d+[A-Za-z]',m[1]):return '('+m[1]+')'+e.translate(SUP)
    return power(m[1],e)

def notation(text,legacy,digits=False):
    # Only explicitly spoken bracket boundaries are collapsed. We never guess
    # the scope of a sum or the intended location of a negative sign.
    if digits:
        # Fixed digit patterns in these puzzles. Do not infer a digit number
        # from prose such as "A three-digit number" or "make A one".
        patterns={'two A six':'2A6','three A four':'3A4','six B A':'6BA',
                  'B eight':'B8','A three':'A3','B seven':'B7'}
        for words,value in patterns.items():
            text=re.sub(r'\b'+words+r'\b(?!-digit)',lambda m:''.join(c+'\u0305'for c in value),text)
    # "the negative one" sometimes means the negative member of a pair,
    # rather than the numerical value -1. Preserve that spoken description.
    text=re.sub(r'\bthe negative one\b',lambda m:'the NEGATIVE_MEMBER',text)
    descriptions={}
    def description(m):
        key='DESCRIPTIVEVALUE'+str(len(descriptions));descriptions[key]=m[0];return key
    text=re.sub(r'\bnegative [a-hj-z]\b',description,text)
    s=legacy(text)
    s=re.sub(rf'\b(?:the )?absolute value of ({OPERAND_V})(?![A-Za-z0-9_’\'])(?!\s+(?:plus|minus|times|over|divided)\b|\s*[+−×÷/])',lambda m:'|'+m[1]+'|',s,flags=re.I)
    s=re.sub(r'\b(zero|one|two|three|four|five|six|seven|eight|nine|\d+) point ((?:zero|one|two|three|four|five|six|seven|eight|nine)(?: (?:zero|one|two|three|four|five|six|seven|eight|nine))*)\b',
        lambda m:number(m[1])+'.'+''.join(number(w) for w in m[2].split()),s,flags=re.I)
    # This is digit concatenation, not multiplication. Uppercase separated
    # letters are how the digit-puzzle scripts spell the barred numbers.
    if digits:s=re.sub(r'\b[A-Z](?: [A-Z]){1,3}\b',lambda m:''.join(c+'\u0305' for c in m[0] if c!=' '),s)
    def bracket(m):
        inner=notation(m[1],lambda x:x)
        # Retain words if the inside is not a purely mathematical expression.
        if re.fullmatch(r'[\w\d\s+−×÷/=²³⁴⁵⁶⁷⁸⁹⁰√().^⁻]+',inner) and not re.search(r'[A-Za-z]{2,}',inner):
            suffix=',' if m[0].endswith(',')and not re.match(r'\s+(?:squared|cubed)\b',m.string[m.end():])else''
            return '('+inner+')'+suffix
        return m[0]
    s=re.sub(r'\b(?:the )?whole bracket, ([^,.;!?]+),?',bracket,s,flags=re.I)
    s=re.sub(r'\bin brackets, ([^,.;!?]+)',bracket,s,flags=re.I)
    # Numeric coefficients are unambiguous: "four a" means 4a, not an article.
    # 2026-10-15: never "one b" -> "1b" ("one b cancels" = one factor b)
    s=re.sub(rf'(?<![\w])(?!one\b)({N}) ({OPERAND_V})(?![A-Za-z0-9_’\']|\.[A-Za-z])',lambda m:number(m[1])+m[2],s,flags=re.I)   # 2026-10-21 Claude: not '7 a.m.'
    # A coefficient, barred digit sequence, explicit bracket or lone variable
    # may be the base of a spoken power.
    barred=r'(?:[A-Z0-9]\u0305){2,4}'
    atom=rf'(?:{barred}|{ATOM})'
    def power(b,e):
        b=number(b);e=e.lower()
        e=str(ORD[e]) if e in ORD else number(e)
        if b.startswith('−') or '/' in b:
            if not b.startswith('('):b='('+b+')'
        return b+(e.translate(SUP) if re.fullmatch(r'[−\d]+',e) else '^('+e+')')
    # The old formatter already converted many numeric bases; this fills its
    # gaps, especially variable a, ordinal powers and fractional exponents.
    for suffix,e in [('squared','2'),('cubed','3')]:
        s=re.sub(rf'({atom}),? {suffix}\b',lambda m,e=e:_spoken_group_power(m,e,power),s)
    ex=rf'(?:−?\d+(?:/\d+)?|negative (?:'+ '|'.join(UNIT)+r')|'+ '|'.join(UNIT)+r'|'+ '|'.join(ORD)+r')'
    def exponent(m):
        e=m[2]
        if e.startswith('negative '):e='−'+number(e[9:])
        return power(m[1],e)
    s=re.sub(rf'({atom}) to the (?:power of )?({ex})\b(?!-digit)',exponent,s,flags=re.I)
    # Non-square roots are not handled by the original formatter.
    s=re.sub(rf'\b(?:the )?(square|cube|third|fourth|fifth|sixth|seventh|eighth|ninth) root of ({ATOM})',
        lambda m:('√' if m[1].lower()=='square'else'∛' if m[1].lower()in('cube','third')else str(ORD[m[1].lower()]).translate(SUP)+'√')+('('+number(m[2])+')'if m[2].startswith('−')or'/'in m[2]else number(m[2])),s,flags=re.I)
    # Unary minus on a variable is distinct from a negative power/base.
    s=re.sub(rf'\b[Mm]inus ({OPERAND_V})(?![\w])',r'−\1',s)
    s=re.sub(r"(?<![A-Za-z0-9'’])(\d*[a-hj-z][²³⁴⁵⁶⁷⁸⁹⁰ⁿ]*) ([b-hj-z][²³⁴⁵⁶⁷⁸⁹⁰ⁿ]*)(?![A-Za-z0-9'’])",r'\1 × \2',s)
    ops=[(r'times',' × '),(r'plus',' + '),(r'minus',' − '),(r'divided by',' ÷ '),(r'over','/'),
         (r'(?:is equal to|equals)',' = '),
         (r'is (?:smaller|less) than',' < '),(r'is (?:larger|greater|bigger) than',' > ')]
    for _ in range(5):
        before=s
        for op,symbol in ops:
            s=re.sub(rf'({atom}) {op},? ({atom})',lambda m:number(m[1])+symbol+number(m[2]),s,flags=re.I)
        if before==s:break
    def equality(m):
        left=m[1];before=s[:m.start()]
        after=s[m.end():]
        if re.match(r'\s+[A-Za-z]',after)and not re.match(r'\s+(?:and|or|too|times|plus|minus|over|squared|cubed|to the|divided by)\b',after):return m[0]
        # Do not turn "the remainder when dividing by 6 is 5" into 6=5,
        # or an article in "x is a whole number" into a variable.
        # 2026-10-15: "the angle at B is ninety" is about the angle, not B = 90
        if re.fullmatch(r'[A-Za-z]',left) and re.search(r'\b(?:at|point|vertex|angle)\s+$',before,re.I):return m[0]
        numeric=re.fullmatch(rf'−?{N}',left,re.I)
        if numeric and not re.search(r'(?:^|[.!?:]\s*|[+−×÷=/]\s*|\b(?:So|Then|Now),?\s+)$',before,re.I):
            return m[0]
        return number(left)+' = '+number(m[2])
    s=re.sub(rf'({atom}) is ({atom})',equality,s)
    for _ in range(6):
        s=re.sub(rf'({atom}\s*[<>]\s*{atom}(?: [×+−] {atom})*), which is (smaller|less|bigger|larger|greater) than ({atom})',
            lambda m:m[1]+(' < 'if m[2]in('smaller','less')else' > ')+number(m[3]),s)
    contexts=r'(?:divisible by|divides? by|divided by|ends? in|remainder (?:is|of)|last digit is|digit sum (?:is|of)|carry|at most|at least)'
    s=re.sub(rf'\b({contexts}) ({N})\b',lambda m:m[1]+' '+number(m[2]),s,flags=re.I)
    # Digits alone at sentence starts followed by a calculation are maths too.
    s=s.replace('NEGATIVE_MEMBER','negative one')
    for key,value in descriptions.items():s=s.replace(key,value)
    # A slash fraction used as the divisor needs explicit grouping.
    s=re.sub(r'÷ (−?\d+/\d+)',r'÷ (\1)',s)
    # 2026-10-13 (Codex review standard 9): a minus between two operands is binary ("a² −4a" -> "a² − 4a",
    # "A −C" -> "A − C"), and a negative factor after a times sign gets brackets ("a × −4" -> "a × (−4)").
    # Only reached by paragraphs without a cached registry display (cached and recorded paragraphs are unchanged).
    s=re.sub(r"(?<![A-Za-z'’])(\d*[A-Za-z][²³⁴⁵⁶⁷⁸⁹⁰ⁿ]*|\d+|[²³⁴⁵⁶⁷⁸⁹)|π]) −(?=[A-Za-z0-9(√|π])",r'\1 − ',s)   # 2026-10-18 Claude: not after an apostrophe ("that's −4")
    s=re.sub(r'× −(\d+|[A-Za-z])(?![\w²³⁴⁵⁶⁷⁸⁹])',r'× (−\1)',s)
    return s

def reading_display(text,legacy,digits=False):
    s=notation(text,legacy,digits)
    # Line breaks are only between full sentences. They do not create new
    # paragraphs, timing markers, pauses, or audio-segmentation positions.
    sentences=re.split(r'(?<=[.!?])\s+(?=[A-Za-z−\d(])',s)
    groups=[];current=[];words=0
    for sentence in sentences:
        count=len(sentence.split())
        if current and words+count>24:
            groups.append(' '.join(current));current=[];words=0
        current.append(sentence);words+=count
    if current:groups.append(' '.join(current))
    return '\n'.join(groups)

def display_for(video_id,paras,reading_root,legacy):
    path=Path(__file__).with_name('_codex_reading_display_20261012.json')
    registry=json.loads(path.read_text())if path.exists()else{'lessons':{}}
    item=registry['lessons'].get(video_id)
    if item and item['paras']==paras:return item['disp']
    recorded=any((Path(reading_root)/video_id).glob('*.wav'))
    out=[]
    for si,slide in enumerate(paras):
        result=[]
        for pi,p in enumerate(slide):
            if item and si<len(item['paras'])and pi<len(item['paras'][si])and item['paras'][si][pi]==p:
                result.append(item['disp'][si][pi]);continue
            # 2026-10-15 (teacher): recorded lessons get the full formatter too (display only), so the math is consistent
            prepared=p
            for old,new in (item or{}).get('scope_replacements',{}).get(f'{si+1}.{pi+1}',[]):
                if prepared.count(old)==1:prepared=prepared.replace(old,new,1)
            result.append(reading_display(prepared,legacy,video_id in registry.get('digit_puzzle_ids',[])))
        out.append(result)
    return out
