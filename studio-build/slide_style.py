"""Slide look (theme B 'teal + amber' + layout): applied to the built studio HTML by text replacement.

Layout changes (hybrid slides only):
  1. a label at the start of a line ("First step:", "Arrow phrases:") is drawn bold in the accent colour;
  2. example sentences (starting with a quote, or a tick/cross + quote) sit in a light panel, templates (with
     [slots]) in a light accent panel;
  3. on slides made only of text, everything is enlarged (up to 25%) when it still fits on the board.
"""

PAL0 = "const PAL={ink:'#0B1220',muted:'#64748B',accent:'#2F6BFF',accentSoft:'#EAF0FF',rule:'#E2E8F0',strike:'#E5484D',pop:'#0F9D58',gold:'#D97706',panel:'#F6F8FC'};"
PAL_B = "const PAL={ink:'#0F172A',muted:'#5B6B7A',accent:'#0F766E',accentSoft:'#E6F4F1',rule:'#D8E6E3',strike:'#E5484D',pop:'#0F9D58',gold:'#B45309',panel:'#F4F7F6'};"
FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif"

# richSvg: words between \u0001 and \u0002 are drawn bold in the accent colour
RICH_OLD_HEAD = "function richSvg(text,x,y,width,size=34){"
RICH_NEW_HEAD = "function richSvg(text,x,y,width,size=34){let _b=0;"
RICH_TOK_OLD = "tokens.push({text:w,w:textWidth(w,size),h:size*1.1})"
RICH_TOK_NEW = (r"{let ww=w;if(ww[0]==='\u0001'){_b=1;ww=ww.slice(1)}const end=ww.endsWith('\u0002');if(end)ww=ww.slice(0,-1);"
                r"const bb=_b&&ww.trim();if(end)_b=0;tokens.push({text:ww,b:bb,w:textWidth(ww,size,bb?700:400),h:size*1.1})}")
RICH_OUT_OLD = "out+=svgText(t.text,cx,cy+r.h/2+size*.34,size)"
RICH_OUT_NEW = "out+=t.b?svgText(t.text,cx,cy+r.h/2+size*.34,size,PAL.accent,700):svgText(t.text,cx,cy+r.h/2+size*.34,size,PAL.ink)"

T_OLD = "if(it.k==='t'){const r=richSvg(it.t,x,y,it.w||w,it.size||46);return {svg:r.svg,h:r.height}}"
T_NEW = (r"if(it.k==='t'){const t0=String(it.t),"
         r"t=t0.split('\n').map(ln=>ln.replace(/^(\s*)([A-Z0-9][^:$\n\"“\[]{0,30}:)(?=\s)/,'$1\u0001$2\u0002')).join('\n'),"
         r"box=/^(✓|✗)?\s*[\"“]/.test(t0)?'ex':(/\[[^\]]+\]/.test(t0)?'tpl':null),W0=it.w||w,"
         r"r=richSvg(t,x,y,W0,it.size||46);let s=r.svg;const h=r.height;"
         # the panel is drawn around the text (never moves or re-wraps it): 16px to the left/right, 4px above/below
         r"if(box)s=`<rect x=\"${x-16}\" y=\"${y-4}\" width=\"${W0+32}\" height=\"${h+4}\" rx=\"12\" fill=\"${box==='ex'?PAL.panel:PAL.accentSoft}\"/>"
         r"<rect x=\"${x-16}\" y=\"${y-4}\" width=\"6\" height=\"${h+4}\" rx=\"3\" fill=\"${box==='ex'?PAL.muted:PAL.accent}\" fill-opacity=\"0.55\"/>`+s;"
         r"return {svg:s,h}}")

HY_OLD = ("const shown=(b.pre||0)+Math.max(0,step|0);let yL=HY.top;\n"
          " const placed=[];let ctop=900;b.items.forEach((it,i)=>{")
HY_NEW = ("const shown=(b.pre||0)+Math.max(0,step|0);\n"
          " const _lay=sc=>{let yL=HY.top,o='',bot=0;const placed=[];let ctop=900;b.items.forEach((it0,i)=>{"
          "const it=sc===1?it0:Object.assign({},it0,{size:(it0.size||(it0.k==='h'?60:46))*sc,y:it0.y!=null?HY.top+(it0.y-HY.top)*sc:it0.y,gap:(it0.gap??44)*sc});")
HY_OLD_END = "if(it.y==null)yL=y+r.h+(it.gap??44);if(i<shown)out+=`<g data-i=\"${i}\">${r.svg}</g>`});\n return out+'</svg>'}"
HY_NEW_END = ("if(it.y==null)yL=y+r.h+(it.gap??44);bot=Math.max(bot,y+r.h);if(i<shown)o+=`<g data-i=\"${i}\">${r.svg}</g>`});return {o,bot}};\n"
              " let best=_lay(1);if(b.items.length&&b.items.every(it=>it.k==='t'||it.k==='h'))for(const sc of [1.25,1.15,1.08]){const t=_lay(sc);if(t.bot<=820){best=t;break}}\n"
              " return out+best.o+'</svg>'}")


def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:60])
    return s.replace(old, new)


def apply(s, layout=True):
    s = rep(s, PAL0, PAL_B)
    a = s.find('function hySidebar'); b = s.find('function hyItem', a); f = s[a:b]
    f = f.replace('#122442', '#0F3D3A').replace('#f0b64a', '#F5A524').replace('#a9b8d3', '#A7CFC8')
    s = s[:a] + f + s[b:]
    s = rep(s, 'font-family="Arial,Helvetica,sans-serif"', 'font-family="%s"' % FONT)
    s = rep(s, "measure.font=weight+' '+size+'px Arial'", "measure.font=weight+' '+size+'px \"Helvetica Neue\"'")
    # camera bubble: right in the corner (6px from the edges instead of 26), top right by default
    s = rep(s, "function camRect(){const d=CAM_D[camSize]||250,m=26;", "function camRect(){const d=CAM_D[camSize]||250,m=6;")
    s = rep(s, "camPos=(()=>{try{return localStorage.getItem('hy-cam-pos')||'br'}catch{return 'br'}})()",
            "camPos=(()=>{try{return localStorage.getItem('hy-cam-pos')||'tr'}catch{return 'tr'}})()")
    s = rep(s, '<select id="cam-pos"><option value="br">Bottom right</option><option value="bl">Bottom left</option><option value="tr">Top right</option></select>',
            '<select id="cam-pos"><option value="tr">Top right</option><option value="br">Bottom right</option><option value="bl">Bottom left</option></select>')
    if layout:
        s = rep(s, RICH_OLD_HEAD, RICH_NEW_HEAD)
        s = rep(s, RICH_TOK_OLD, RICH_TOK_NEW)
        s = rep(s, RICH_OUT_OLD, RICH_OUT_NEW)
        s = rep(s, T_OLD, T_NEW)
        s = rep(s, HY_OLD, HY_NEW)
        s = rep(s, HY_OLD_END, HY_NEW_END)
    return s
