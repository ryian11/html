"""lesson08 dic1: input 폭 최적화 + scrollTop 산출"""
import re, os, json, asyncio, sys
from playwright.async_api import async_playwright

REF = '/mnt/user-data/uploads/resource--contents/lesson03/ops/popup'
SRC = '/home/claude/cj/measure/work/popup'
BOXH = 548

def bucket(w):
    L = len(w)
    if L <= 4: return 140
    if L <= 9: return 200
    if L <= 11: return 250
    return 350
MINW = lambda w: 140 if len(w) <= 8 else (200 if len(w) <= 11 else 250)

TAG = re.compile(r'<script-cont\b([^>]*)></script-cont>')

def parse(path):
    """returns html, list of (span, attrs, tabidx, answers)"""
    html = open(path, encoding='utf-8').read()
    # tab index by counting quizContainer / attachSticker before position
    marks = [m.start() for m in re.finditer(r'js-quizContainer|attachSticker', html)]
    items = []
    for m in TAG.finditer(html):
        a = m.group(1)
        en = re.search(r'\ben="([^"]*)"', a)
        ans = re.findall(r'\|\|(.*?)\|\|', en.group(1)) if en else []
        ans = [x for grp in ans for x in grp.split('::')]
        t = max(0, sum(1 for k in marks if k < m.start()) - 1)
        items.append({'span': m.span(), 'attrs': a, 'tab': t, 'ans': ans})
    return html, items

def inject(html, items, widths, extra_style=''):
    """widths: dict idx -> list of px per input; add uid class + style"""
    rules = []
    out = []
    last = 0
    for i, it in enumerate(items):
        s, e = it['span']
        out.append(html[last:s])
        a = it['attrs']
        uid = 'u%d' % i
        if re.search(r'\bclass="', a):
            a = re.sub(r'\bclass="', 'class="%s ' % uid, a, count=1)
        else:
            a = ' class="%s"' % uid + a
        out.append('<script-cont%s></script-cont>' % a)
        last = e
        for k, px in enumerate(widths.get(i, [])):
            rules.append('.%s .inputBox:nth-of-type(%d){width:%dpx !important;}' % (uid, k+1, px))
    out.append(html[last:])
    h = ''.join(out)
    st = '<style id="__opt">.tabContent{display:grid !important;}' + ''.join(rules) + extra_style + '</style>'
    return h.replace('</head>', st + '</head>')

MEASURE = """() => [...document.querySelectorAll('.tabContent')].map(t=>{
  const box=t.querySelector('.scrollBox'); const br=box.getBoundingClientRect();
  return {scrollH:box.scrollHeight, boxH:box.clientHeight,
    items:[...t.querySelectorAll('.scriptTarget')].map(el=>{
      const rs=[...el.getClientRects()];
      return {top:rs.length?Math.round(Math.min(...rs.map(r=>r.top))-br.top+box.scrollTop):0,
              bot:rs.length?Math.round(Math.max(...rs.map(r=>r.bottom))-br.top+box.scrollTop):0};
    })};
})"""

async def render(pg, path, html):
    tmp = os.path.join(REF, '__opt.html')
    open(tmp, 'w', encoding='utf-8').write(html)
    await pg.goto('file://' + tmp)
    await pg.evaluate("document.fonts.ready")
    await pg.wait_for_timeout(120)
    r = await pg.evaluate(MEASURE)
    return r

def grouping(items, boxH=BOXH):
    out=[0]; origin=items[0]['top']; i=1
    while i < len(items):
        it=items[i]
        if it['bot'] > origin + boxH:
            j=i
            while j>out[-1] and items[j-1]['top']==it['top']: j-=1
            if j<=out[-1]: j=i
            out.append(j); origin=items[j]['top']; i=j+1
        else: i+=1
    return out

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1280,'height':720})
        result = {}
        for name in sorted(os.listdir(SRC)):
            path = os.path.join(SRC, name)
            html, items = parse(path)
            widths = {i: [bucket(w) for w in it['ans']] for i, it in enumerate(items) if it['ans']}
            base = await render(pg, path, inject(html, items, widths))
            H = [t['scrollH'] for t in base]
            # greedy shrink
            improved = True
            while improved:
                improved = False
                for i, it in enumerate(items):
                    if i not in widths: continue
                    t = it['tab']
                    for k, w in enumerate(it['ans']):
                        cur = widths[i][k]; mn = MINW(w)
                        if cur <= mn: continue
                        nxt = mn
                        old = widths[i][k]; widths[i][k] = nxt
                        r = await render(pg, path, inject(html, items, widths))
                        if r[t]['scrollH'] < H[t]:
                            H = [x['scrollH'] for x in r]; improved = True
                        else:
                            widths[i][k] = old
            final = await render(pg, path, inject(html, items, widths))
            result[name] = {
                'widths': {str(k): v for k, v in widths.items()},
                'tabs': [{'scrollH': t['scrollH'], 'boxH': t['boxH'],
                          'tops': [x['top'] for x in t['items']],
                          'bots': [x['bot'] for x in t['items']]} for t in final],
                'base_scrollH': [t['scrollH'] for t in base],
                'items': [{'tab': it['tab'], 'ans': it['ans']} for it in items],
            }
            print(name, 'scrollH', [t['scrollH'] for t in base], '->', [t['scrollH'] for t in final])
        await b.close()
        json.dump(result, open('/home/claude/cj/measure/opt.json','w'), ensure_ascii=False, indent=1)

asyncio.run(main())
