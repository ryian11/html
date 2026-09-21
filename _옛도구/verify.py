# -*- coding: utf-8 -*-
"""산출물 일괄 검증 — python3 verify.py <검증할 html 폴더>

검사 항목
 1) ‖ (내부 표시) 잔존 · 빈 itemIdx
 2) itemIdx 연속성(0,1,2…) 과 ||빈칸|| 개수 일치
 3) 모든 문장이 자기 scrollTop 위치에서 잘리지 않는지 (input 칸 삐져나옴 포함)
 4) 모든 입력칸에 정답이 들어가는지
 5) 같은 comp-script-box 안에서 scrollTop 이 바뀌는 곳(발화 중간 끊김)
"""
import sys, os, re, asyncio, shutil
from playwright.async_api import async_playwright

REF = '/mnt/user-data/uploads/resource--contents/lesson03/ops/popup'   # include/ 가 있는 폴더
CALIB = '.iframePopup[data-use="dictation"] .tabActBox{padding-right:1px !important;}'

JS = """() => [...document.querySelectorAll('.tabContent')].map(t => {
  const box = t.querySelector('.scrollBox');
  const br = box.getBoundingClientRect();
  const o = box.scrollTop - br.top;
  const c = document.createElement('canvas').getContext('2d');
  const inputs = [...t.querySelectorAll('.js-quizItem')].map(inp => {
    const a = inp.getAttribute('data-answer') || '';
    const cs = getComputedStyle(inp);
    c.font = cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    return { a: a,
      need: Math.ceil(c.measureText(a).width) + parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight),
      box: Math.round(inp.parentElement.getBoundingClientRect().width) };
  });
  return {
    maxScroll: box.scrollHeight - box.clientHeight, boxH: box.clientHeight, inputs: inputs,
    items: [...t.querySelectorAll('.scriptTarget')].map(el => {
      const rs = [...el.getClientRects()];
      let top = Math.min(...rs.map(r => r.top)), bot = Math.max(...rs.map(r => r.bottom));
      el.querySelectorAll('.inputBox').forEach(ib => {
        const r2 = ib.getBoundingClientRect();
        top = Math.min(top, r2.top); bot = Math.max(bot, r2.bottom);
      });
      return { top: Math.round(top + o), bot: Math.round(bot + o),
               st: el.getAttribute('data-scroll-top'),
               txt: el.textContent.replace(/\\s+/g, ' ').trim().slice(0, 36) };
    })
  };
})"""


async def main(src_dir):
    names = sorted(n for n in os.listdir(src_dir) if n.endswith('.html'))
    bad = cut = tot = nin = 0
    wmin, edge, split, mark, idxerr = [], [], [], [], []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1280, 'height': 720})
        for name in names:
            src = open(os.path.join(src_dir, name), encoding='utf-8').read()
            shutil.copy(os.path.join(src_dir, name), os.path.join(REF, name))
            if '‖' in src or 'itemIdx=""' in src:
                mark.append(name)
            for ti, t in enumerate(re.split(r'js-quizContainer|attachSticker', src)[1:], 1):
                cur = None
                for m in re.finditer(r'<comp-script-box|<script-cont\b([^>]*)>', t):
                    if m.group(0).startswith('<comp'):
                        cur = None; continue
                    v = re.search(r'scrollTop="(\d+)"', m.group(1))
                    v = v.group(1) if v else '0'
                    if cur is None: cur = v
                    elif v != cur:
                        split.append('%s t%d %s→%s' % (name[:7], ti, cur, v)); cur = v
                if ti > 3: continue
                idxs, blanks = [], 0
                for m in re.finditer(r'<script-cont\b([^>]*)>', t):
                    a = m.group(1)
                    en = re.search(r'\ben="([^"]*)"', a)
                    if en: blanks += len(re.findall(r'\|\|', en.group(1))) // 2
                    ii = re.search(r'itemIdx="([^"]*)"', a)
                    if ii:
                        for g in ii.group(1).split('|'):
                            idxs += [int(x) for x in g.split(',') if x.strip().isdigit()]
                if idxs != list(range(len(idxs))) or len(idxs) != blanks:
                    idxerr.append('%s t%d' % (name[:7], ti))
            html = src.replace('</head>', '<style>.tabContent{display:grid !important;}' + CALIB + '</style></head>')
            tmp = os.path.join(REF, '__verify.html')
            open(tmp, 'w', encoding='utf-8', newline='').write(html)
            await pg.goto('file://' + tmp)
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(320)
            r = await pg.evaluate(JS)
            os.remove(tmp)
            for t in r:
                for x in t['inputs']:
                    nin += 1; wmin.append(x['box'] - x['need'])
                    if x['need'] > x['box']:
                        cut += 1; print('  칸부족 %s %s (필요 %d > 칸 %d)' % (name, x['a'], x['need'], x['box']))
                for it in t['items']:
                    tot += 1
                    st = min(int(it['st'] or 0), t['maxScroll'])
                    ot, ob = st - it['top'], it['bot'] - (st + t['boxH'])
                    edge.append(min(-ot, -ob))
                    if ot > 0 or ob > 0:
                        bad += 1
                        print('  잘림 %s st=%s 위%+d 아래%+d %s' % (name, it['st'], ot, ob, it['txt']))
        await b.close()
    print('\n파일 %d개' % len(names))
    print('  ‖ · 빈 itemIdx : %s' % (mark or '없음'))
    print('  itemIdx 오류   : %s' % (idxerr or '없음'))
    print('  문장 %d개 중 잘림 %d개 (가장자리 여유 최소 %+dpx)' % (tot, bad, min(edge)))
    print('  입력칸 %d개 중 폭부족 %d개 (여백 최소 %dpx)' % (nin, cut, min(wmin)))
    print('  발화 중간 끊김 %d곳 %s' % (len(split), '— 독백/긴 문단이면 정상' if split else ''))
    for s in split: print('     ', s)

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else '.'))
