# -*- coding: utf-8 -*-
"""Reading형 Dictation(dic1) 생성 — 화자 없는 산문. 소제목(subTitBox) 지원"""
import re, sys, os, openpyxl
sys.path.insert(0, '/home/claude/cj')
import src, gen, dlg

SPKMARK = re.compile(r'^\s*([A-Z])\s*:\s*')


def sound_rows(lesson, page):
    """[(mp3, 문장, 화자표시)] — 화자표시는 'M'/'W'/'' """
    wb = openpyxl.load_workbook(src.SND, data_only=True)
    ws = wb['%d과' % lesson]
    pat = re.compile(r'^3-%s-Read-(\d+(?:-\d+)?)$' % page)
    out, started = [], False
    for r in ws.iter_rows(values_only=True):
        fn = str(r[2] or '').strip()
        txt = str(r[1] or '')
        m = pat.match(fn)
        if m:
            started = True
            sm = SPKMARK.match(txt)
            out.append(['3_%s_read_%s.mp3' % (page, m.group(1)),
                        src.norm(SPKMARK.sub('', txt)), sm.group(1) if sm else ''])
        elif started and not fn and txt.strip():
            out[-1][1] = src.norm(out[-1][1] + ' ' + SPKMARK.sub('', txt))
        elif started and fn:
            break
    return [tuple(x) for x in out]


def paras(lesson, section, level):
    """원고 한 줄 = 문단 하나. 소문자로 시작하는 줄만 앞 줄에 이어붙인다(칸 폭 때문에 끊긴 경우)."""
    wb = openpyxl.load_workbook(src.SB % lesson, data_only=True, rich_text=True)
    ws = wb['Dictation']
    rr = None
    for row in range(2, ws.max_row + 1):
        if str(ws.cell(row=row, column=1).value or '').strip() == section \
           and str(ws.cell(row=row, column=2).value or '').strip() == level:
            rr = src.runs(ws.cell(row=row, column=3).value); break
    if rr is None:
        raise SystemExit('원고 없음: %s / %s' % (section, level))
    lines, cur = [], []
    for text, red in rr:
        for k, piece in enumerate(text.split('\n')):
            if k:
                lines.append(cur); cur = []
            if piece:
                cur.append((piece, red))
    if cur:
        lines.append(cur)
    out = []
    for ln in lines:
        raw = ''.join(t for t, _ in ln)
        if not raw.strip():
            continue
        first = raw.strip()[0]
        if out and first.islower():        # 문장 중간에서 끊긴 줄 -> 앞 문단에 이어붙임
            out[-1].append((' ', False)); out[-1].extend(ln)
        else:
            out.append(list(ln))
    return [src.to_marked(p) for p in out]


def align(marked_paras, rows, thresh=0.72):
    """문단별로 mp3 순차 소비. 반환 [(문단, [(mp3, marked)], 소제목여부)]"""
    si = 0
    while si < len(rows):
        _, _, r = dlg.cut_words(marked_paras[0], rows[si][1])
        if r >= thresh: break
        si += 1
    if si == len(rows):
        raise SystemExit('시작 문장을 못 찾음')
    res = []
    for mp in marked_paras:
        rest, grp = mp, []
        while si < len(rows) and rest.strip():
            mp3, sent, spk = rows[si]
            take, rest2, r = dlg.cut_words(rest, sent)
            if r < thresh:
                if si + 1 < len(rows):
                    _, _, r2 = dlg.cut_words(rest, rows[si + 1][1])
                    if r2 >= thresh:
                        si += 1; continue
                break
            grp.append((mp3, take, spk)); rest = rest2; si += 1
        if rest.strip():
            print('  [경고] 매칭 실패: %r' % src.strip_marks(rest)[:60])
        # 소제목 = mp3 하나짜리 문단이고 그 음원이 M: 로 시작
        sub = len(grp) == 1 and grp[0][2] == 'M'
        res.append((mp, [(m, k) for m, k, _ in grp], sub))
    return res


IND = '\t' * 10
BIND = '\t' * 9


def boxes(groups, tab_i, sticker_mode=False):
    out, n = [], 0
    for _, g, sub in groups:
        cls = ' class="subTitBox"' if sub else ''
        lines = [BIND + ('<!-- subTitBox -->' if sub else '<!-- scriptBox -->'),
                 BIND + '<comp-script-box%s>' % cls]
        for mp3, marked in g:
            if sticker_mode:
                lines.append(IND + '<script-cont src="../media/mp3/%s" sticker="%s"></script-cont>'
                             % (mp3, gen.esc(gen.sticker(src.strip_marks(marked)))))
            else:
                en, sizes = src.split_groups(marked)
                a = 'src="../media/mp3/%s" en="%s"' % (mp3, gen.esc(en))
                if sizes:
                    idx, n = src.item_idx(sizes, n)
                    a += ' handler="%d" itemIdx="%s"' % (tab_i, idx)
                lines.append(IND + '<script-cont %s></script-cont>' % a)
        lines.append(BIND + '</comp-script-box>')
        out.append('\n'.join(lines))
    return '\n'.join(out)


def build(page, tabs):
    html = gen.HEAD.format(page=page)
    for k, g in enumerate(tabs):
        html += gen.QUIZ_TAB.format(n=k + 1, i=k, boxes=boxes(g, k))
    html += gen.TAB4.format(boxes=boxes(tabs[0], 3, sticker_mode=True))
    html += gen.FOOT
    return html


LESSONS = {6: [('p104_02', 'Reading 1', '104'), ('p105_01', 'Reading 2', '105'),
               ('p106_01', 'Reading 3', '106'), ('p107_01', 'Reading 4', '107')]}

if __name__ == '__main__':
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    OUT = '/home/claude/cj/measure/work/popup'
    os.makedirs(OUT, exist_ok=True)
    for page, sec, pg in LESSONS[L]:
        rows = sound_rows(L, pg)
        tabs = [align(paras(L, sec, lv), rows) for lv in ('보충', '기본', '심화')]
        html = build(page, tabs)
        assert '‖' not in html, page
        assert 'itemIdx=""' not in html, page
        open(os.path.join(OUT, page + '_dic1.html'), 'w', encoding='utf-8').write(html)
        print('%s 문단 %d개(소제목 %d) script-cont %d  div %d/%d'
              % (page, len(tabs[0]), sum(1 for x in tabs[0] if x[2]),
                 html.count('<script-cont'), html.count('<div'), html.count('</div>')))
