# -*- coding: utf-8 -*-
"""대화형 Dictation(dic1) 생성 — Listen and Talk A/B, Enjoy the Clip"""
import re, sys, openpyxl
sys.path.insert(0, '/home/claude/cj')
import src, gen

# 대본 파일명 → 실제 파일명 교정이 필요한 경우에만 등록.
# 주의: 빨간 글씨 파일명은 "추가 녹음분, 아직 폴더에 없음" 이라는 뜻이므로 이름을 바꾸면 안 된다.
MP3_ALIAS = {}

NUMWORD = {'one':1,'two':2,'three':3,'four':4,'five':5,'six':6}
SPK = re.compile(r'^\s*(Q\.|[A-Za-z][A-Za-z.\' ]{0,14}:)\s*')
NUMHEAD = re.compile(r'^\s*(\d+)\.\s*')


def sound_rows(lesson, prefix):
    """[(mp3, 문장)] — prefix 예: '3-136-LnT-A'. 파일명 없는 행은 앞에 이어붙임"""
    wb = openpyxl.load_workbook(src.SND, data_only=True)
    ws = wb['%d과' % lesson]
    pat = re.compile(r'^%s-(\d+(?:-\d+)?)$' % re.escape(prefix))
    out, started = [], False
    for r in ws.iter_rows(values_only=True):
        fn = str(r[2] or '').strip()
        txt = str(r[1] or '')
        m = pat.match(fn)
        if m:
            started = True
            mp3 = (prefix + '-' + m.group(1)).replace('-', '_').lower() + '.mp3'
            mp3 = MP3_ALIAS.get(mp3, mp3)
            out.append([mp3, src.norm(SPK.sub('', txt))])
        elif started and not fn and txt.strip():
            out[-1][1] = src.norm(out[-1][1] + ' ' + SPK.sub('', txt))
        elif started and fn:
            break
    return [tuple(x) for x in out]


def dict_lines(lesson, section, level):
    """[(번호 or None, 화자, 마킹된 본문)] — 원고 한 줄 = 화자 발화 하나"""
    wb = openpyxl.load_workbook(src.SB % lesson, data_only=True, rich_text=True)
    ws = wb['Dictation']
    rr = None
    for row in range(2, ws.max_row + 1):
        if str(ws.cell(row=row, column=1).value or '').strip() == section \
           and str(ws.cell(row=row, column=2).value or '').strip() == level:
            rr = src.runs(ws.cell(row=row, column=3).value); break
    if rr is None:
        raise SystemExit('원고 없음: %s / %s' % (section, level))
    # 줄 단위로 나누되 빨강 정보 유지
    lines, cur = [], []
    for text, red in rr:
        parts = text.split('\n')
        for k, piece in enumerate(parts):
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
        marked = src.to_marked(ln)
        num = None
        m = NUMHEAD.match(marked)
        if m:
            num = int(m.group(1)); marked = marked[m.end():]
        ms = SPK.match(marked)
        spk = ms.group(1) if ms else ''
        if ms:
            marked = marked[ms.end():]
        out.append((num, spk, marked.strip()))
    return out


import difflib

def _words(t):
    return [w for w in re.findall(r"[A-Za-z0-9\u2019']+", t)]

def _key(t):
    return re.sub(r"[^a-z0-9]", '', t.lower().replace('\u2019', "'"))

def cut_words(marked, sentence):
    """marked 앞에서 sentence 의 단어 수만큼 잘라낸다(마킹 유지). (조각, 나머지, 유사도)"""
    n = len(_words(sentence))
    if n == 0:
        return None, marked, 0.0
    WC = re.compile(r"[A-Za-z0-9\u2019']")
    best = None
    for delta in (0, 1, -1, 2, -2):
        k = n + delta
        if k <= 0:
            continue
        out, cnt, i, inword = [], 0, 0, False
        while i < len(marked):
            if marked[i] == '‖':          # 정답 묶음(‖…‖)은 통째로 — 중간에서 자르면 안 됨
                e = marked.find('‖', i + 1)
                if e < 0:
                    break
                e += 1
                if cnt >= k:
                    break
                cnt += len(_words(marked[i:e]))
                out.append(marked[i:e]); i = e; inword = False
                continue
            if marked.startswith('||', i):
                j = marked.index('||', i + 2) + 2
                w = len(_words(marked[i:j]))
                if cnt >= k:
                    break
                cnt += w; out.append(marked[i:j]); i = j; inword = False
                continue
            ch = marked[i]
            isw = bool(WC.match(ch))
            if isw and not inword:
                if cnt >= k:
                    break
                cnt += 1
            inword = isw
            out.append(ch); i += 1
        tail = ''.join(out)
        mm = re.search(r'[\s([{\u201c\u2018]+$', tail)
        if mm:                      # 여는 괄호·따옴표는 다음 조각으로 넘긴다
            i -= len(mm.group(0)); tail = tail[:mm.start()]
        take = tail.strip()
        r = difflib.SequenceMatcher(None, _key(src.strip_marks(take)), _key(sentence)).ratio()
        if best is None or r > best[2]:
            best = (take, marked[i:], r)
        if r > 0.97:
            break
    return best


def align(lines, sentences, thresh=0.72):
    """[(번호, 화자, [(mp3, marked)])] — 단어 수 기준 순차 소비. 원고에 없는 음원은 건너뜀"""
    si = 0
    first = src.strip_marks(lines[0][2])
    while si < len(sentences):
        _, rest, r = cut_words(lines[0][2], sentences[si][1])
        if r >= thresh: break
        si += 1
    if si == len(sentences):
        raise SystemExit('시작 문장을 못 찾음: %s' % first[:60])
    out, skipped = [], []
    for num, spk, marked in lines:
        rest, grp = marked, []
        while si < len(sentences) and rest.strip():
            mp3, sent = sentences[si]
            take, rest2, r = cut_words(rest, sent)
            if r < thresh:
                # 원고에 없는 음원(제목/라벨/번호 안내)인지 확인: 다음 음원이 맞으면 건너뛴다
                if si + 1 < len(sentences):
                    _, _, r2 = cut_words(rest, sentences[si + 1][1])
                    if r2 >= thresh:
                        skipped.append(mp3); si += 1; continue
                break
            grp.append((mp3, take)); rest = rest2; si += 1
        if rest.strip():
            print('  [경고] 매칭 실패: %r' % src.strip_marks(rest)[:60])
        out.append((num, spk, grp))
    if skipped:
        print('  [건너뜀] 원고에 없는 음원:', ' '.join(skipped))
    return out


IND = '\t' * 11
BIND = '\t' * 10


def boxes(groups, tab_i, sticker_mode=False, start_idx=0):
    """groups: [(번호, 화자, [(mp3, marked)])]  -> Paragraph 여러 개"""
    paras, cur, n = [], [], start_idx
    for num, spk, g in groups:
        if num is not None and cur:
            paras.append(cur); cur = []
        attrs = ' speaker="%s"' % gen.esc(spk) if spk else ''
        if num is not None:
            attrs += ' number="%d" numberSrc="../include/media/common/num%d.mp3" numberScrollTop="0"' % (num, num)
        lines = [BIND + '<comp-script-box%s>' % attrs]
        for mp3, marked in g:
            if sticker_mode:
                plain = src.strip_marks(marked)
                lines.append(IND + '<script-cont src="../media/mp3/%s" sticker="%s"></script-cont>'
                             % (mp3, gen.esc(gen.sticker(plain))))
            else:
                en, sizes = src.split_groups(marked)
                a = 'src="../media/mp3/%s" en="%s"' % (mp3, gen.esc(en))
                if sizes:
                    idx, n = src.item_idx(sizes, n)
                    a += ' handler="%d" itemIdx="%s"' % (tab_i, idx)
                lines.append(IND + '<script-cont %s></script-cont>' % a)
        lines.append(BIND + '</comp-script-box>')
        cur.append('\n'.join(lines))
    if cur:
        paras.append(cur)
    return '\n\n'.join(
        '\t' * 9 + '<!-- Paragraph -->\n' + '\t' * 9 + '<div class="Paragraph">\n'
        + '\n\n'.join(p) + '\n' + '\t' * 9 + '</div>'
        for p in paras)


HEAD = gen.HEAD          # style 블록은 build3 가 다시 씀


LESSONS = {
 8: [dict(page='p136_03', sec='Listen and Talk A', pre='3-136-LnT-A'),
     dict(page='p137_01', sec='Listen and Talk B', pre='3-137-LnT-B-1'),
     dict(page='p138_02', sec='Enjoy the Clip',    pre='3-138-EtC-A')],
 7: [dict(page='p118_03', sec='Listen and Talk A', pre='3-118-LnT-A'),
     dict(page='p119_01', sec='Listen and Talk B', pre='3-119-LnT-B-1'),
     dict(page='p120_02', sec='Enjoy the Clip',    pre='3-120-EtC-A'),
     dict(page='p122_02', sec='Reading 1', pre='3-122-Read', dialog=True, spkgroup='L7read'),
     dict(page='p123_01', sec='Reading 2', pre='3-123-Read', dialog=True, spkgroup='L7read'),
     dict(page='p124_01', sec='Reading 4'.replace('4','3'), pre='3-124-Read', dialog=True, spkgroup='L7read'),
     dict(page='p125_01', sec='Reading 4', pre='3-125-Read', dialog=True, spkgroup='L7read')],
}
PAGES = LESSONS[8]

STYLE_ONE = '''\t<style>
\t\t.iframePopup[data-use="dictation"] .inputBox {
\t\t\twidth: 200px;
\t\t}
\t</style>'''

STYLE_SPK = '''\t<style>
\t\t.scriptContainer .scriptBox .Speaker {
\t\t\twidth: __SPKW__px;
\t\t}

\t\t.iframePopup[data-use="dictation"] .inputBox {
\t\t\twidth: 200px;
\t\t}
\t</style>'''

HEAD_T = '''<!DOCTYPE html>
<html lang="ko">

<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0">
\t<link rel="stylesheet" href="../include/contentsUI/css/index.css">
\t<link rel="stylesheet" href="../include/css/common.css">
\t<link rel="stylesheet" href="../include/css/dictation.css">
\t<link rel="stylesheet" href="../include/css/font.css">

\t<title>{page}_dic1</title>
{style}
</head>

<body>
\t<div class="js-iframePopupContainer js-scale iframePopup" data-use="dictation"{onel}>
'''


QUIZ_TAB = """\t\t\t\t\t<!-- 탭{n} -->
\t\t\t\t\t<div class="js-sliderContent js-quizContainer tabContent" data-sld-cont="{n}" data-quiz-type="input" data-quiz-opts="noAlert, noSound, noSolve, noRemoveSpace">
\t\t\t\t\t\t<div class="js-scrollContainer scrollContainer tabActBox" data-scroll-idx="{i}">
\t\t\t\t\t\t\t<div class="js-player Player js-scrollBox scrollBox" data-ply-type="language" data-ply-controls="play, pause, stop, progress" data-ply-opts="speed" data-speed-btn="0.8,1.0,1.2,1.5" data-ply-idx="{i}" data-scroll-idx="{i}">
\t\t\t\t\t\t\t\t<!-- scriptContainer -->
\t\t\t\t\t\t\t\t<div class="js-languageContainer scriptContainer" data-ply-idx="{i}">
{paras}
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<!-- btnHandlerBox -->
\t\t\t\t\t\t<div class="btnHandlerBox selected" data-include="player">
\t\t\t\t\t\t\t<div class="btnBundle">
\t\t\t\t\t\t\t\t<div class="controlsBox" data-use="ui">
\t\t\t\t\t\t\t\t\t<div class="js-controlBoxContainer mediaControl" data-ply-type="language" data-ply-idx="{i}"></div>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<comp-btn-group hdlQuiz="{i}"></comp-btn-group>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

"""

def build(page, tabs, one_line):
    style = STYLE_ONE if one_line else STYLE_SPK
    html = HEAD_T.format(page=page, style=style, onel=' data-type="oneLine"' if one_line else '')
    html += gen.HEAD.split('data-use="dictation" data-type="oneLine">\n')[1]
    for k, groups in enumerate(tabs):
        html += QUIZ_TAB.format(n=k+1, i=k, paras=boxes(groups, k))
    t4 = gen.TAB4
    a = t4.index('\t'*9 + '<!-- Paragraph -->')
    b = t4.index('\t'*9 + '</div>', a) + len('\t'*9 + '</div>')
    html += t4[:a] + boxes(tabs[0], 3, sticker_mode=True) + t4[b:]
    html += gen.FOOT
    return html


if __name__ == '__main__':
    import os
    OUT = '/home/claude/cj/measure/work/popup'
    os.makedirs(OUT, exist_ok=True)
    import json
    groups = {}
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    for p in LESSONS[L]:
        snd = sound_rows(L, p['pre'])
        tabs, spks = [], set()
        for lv in ('보충', '기본', '심화'):
            g = align(dict_lines(L, p['sec'], lv), snd)
            tabs.append(g); spks |= {s for _, s, _ in g if s}
        one = len(spks) <= 1 and not p.get('dialog')
        html = build(p['page'], tabs, one)
        assert '‖' not in html, '%s: 정답 묶음 표시(‖)가 남았다' % p['page']
        assert 'itemIdx=""' not in html, '%s: 빈 itemIdx' % p['page']
        open(os.path.join(OUT, p['page'] + '_dic1.html'), 'w', encoding='utf-8').write(html)
        if p.get('spkgroup'): groups[p['page'] + '_dic1.html'] = p['spkgroup']
        print(p['page'], '화자', sorted(spks), 'oneLine' if one else '대화형',
              'script-cont', html.count('<script-cont'),
              'div', html.count('<div'), html.count('</div>'),
              'Paragraph', html.count('class="Paragraph"'))
    json.dump(groups, open(os.path.join(OUT, '..', 'spkgroup.json'), 'w'))
