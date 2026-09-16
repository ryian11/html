# -*- coding: utf-8 -*-
"""Reading 본문 페이지 검증.   python read_verify.py 6

조용히 틀리느니 시끄럽게 세운다. 하나라도 걸리면 종료코드 1.
"""
import os, re, sys, html
import read_paths as P
import read_gen

OK, NG = '  OK   ', '  !!   '
bad = []


def fail(msg):
    bad.append(msg)
    print(NG + msg)


def ok(msg):
    print(OK + msg)


def strip_marks(t):
    t = re.sub(r'\|\d+\|', '', t)
    t = re.sub(r'\[mark:\d+:\s*([^\]]*)\]', r'\1', t)
    t = re.sub(r'<br>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def strip_kr(t):
    # 태그 자리는 공백으로 (조각 경계에서 단어가 붙지 않도록)
    return re.sub(r'\s+', ' ', re.sub(r'</?span[^>]*>', ' ', t)).strip()


def verify(n, out=None):
    global bad
    bad = []
    read_gen.load_lesson(n, out)
    OUTDIR = read_gen.OUT
    pages = read_gen.ORDER
    print('[verify] lesson%02d  <- %s' % (n, OUTDIR))

    # ---------- 1. 파일 형식 ----------
    files = []
    for root, _, fs in os.walk(OUTDIR):
        for f in fs:
            if f.endswith(('.html', '.js', '.css')) and not os.path.basename(root) in ('include',):
                files.append(os.path.join(root, f))
    files = [f for f in files if 'include' not in f.replace(OUTDIR, '')]
    made = set()
    for page in pages:
        made |= {page + '.html', page + '.css', page + '.js', page + '_kor1.html'}
    made |= {read_gen.intro_page() + '.html', read_gen.all_popup() + '.html'}
    tp = read_gen.think_page()
    if tp:
        made.add(tp + '_think_ans1.html')
    files = [f for f in files if os.path.basename(f) in made]

    nbad = 0
    for f in sorted(files):
        d = open(f, 'rb').read()
        e = []
        if d.count(b'\r\n') != d.count(b'\n'):
            e.append('CRLF 아님')
        if d.endswith(b'\n'):
            e.append('끝 개행 있음')
        if f.endswith('.html') and d.count(b'<div') != d.count(b'</div>'):
            e.append('<div> 짝 안 맞음 %d/%d' % (d.count(b'<div'), d.count(b'</div>')))
        if e:
            fail('%s : %s' % (os.path.basename(f), ', '.join(e)))
            nbad += 1
    if not nbad:
        ok('파일 형식 %d개 (CRLF · 끝개행 없음 · div 짝)' % len(files))

    # ---------- 2. 본문 문장 / 번호 ----------
    for page in pages:
        p = read_gen.PAGES[page]
        h = open(os.path.join(OUTDIR, page + '.html'), encoding='utf-8').read()
        js = open(os.path.join(OUTDIR, 'js', page + '.js'), encoding='utf-8').read()

        want = (1 if p['title'] else 0) + sum(1 if k in ('subtit', 'label') else len(b) for k, b in p['blocks'])
        got = len(re.findall(r'<comp-language-target', h))
        if got != want:
            fail('%s 문장 수 %d (원고 %d)' % (page, got, want))

        marks = sorted(int(x) for x in re.findall(r'\[mark:(\d+):', h))
        syns = sorted(int(x) for x in re.findall(r'\|(\d+)\|', h))
        wi = [int(x) for x in re.findall(r'index: (\d+),\s*\n\s*wordArr', js)]
        si = [int(x) for x in re.findall(r'index: (\d+),\s*\n\s*syntaxArr', js)]
        if len(marks) != len(set(marks)):
            fail('%s mark 번호 중복 %s' % (page, marks))
        if marks != wi:
            fail('%s mark %s ≠ wordData %s' % (page, marks, wi))
        if syns != si:
            fail('%s |n| %s ≠ syntaxData %s' % (page, syns, si))
        if wi and wi != list(range(1, len(wi) + 1)):
            fail('%s wordData index 가 1부터 연속이 아님 %s' % (page, wi))

        # 본문 영어가 원고와 같은가
        ens = re.findall(r'text="([^"]*)"', h)
        want_en = [p['title']['mark']] if p['title'] else []
        for k, b in p['blocks']:
            want_en += [b['mark'] if k == 'subtit' else b['en']] if k in ('subtit', 'label') else [e for _, e, _ in b]
        if [html.unescape(x) for x in ens] != want_en:
            for i, (a, b2) in enumerate(zip(ens, want_en)):
                if html.unescape(a) != b2:
                    fail('%s 문장 %d 본문 불일치\n         html: %s\n         원고: %s' % (page, i, a, b2))
                    break
    if not bad:
        ok('본문 문장 수 · mark/구문 번호 · 원고 대조')

    # ---------- 3. 해석 팝업 ----------
    for page in pages:
        p = read_gen.PAGES[page]
        want_kr = [p['title']['kr']] if p['title'] else []
        for k, b in p['blocks']:
            want_kr += [b['kr']] if k in ('subtit', 'label') else [kr for _, _, kr in b]
        h = open(os.path.join(OUTDIR, 'popup', page + '_kor1.html'), encoding='utf-8').read()
        got = [html.unescape(x) for x in re.findall(r'\skr="([^"]*)"', h)]
        if len(got) != len(want_kr):
            fail('%s_kor1 script-cont %d개 (원고 %d)' % (page, len(got), len(want_kr)))
            continue
        a = strip_kr(' '.join(got))
        b2 = re.sub(r'\s+', ' ', ' '.join(want_kr)).strip()
        if a != b2:
            fail('%s_kor1 해석 글자가 원고와 다름' % page)
            for i in range(min(len(a), len(b2))):
                if a[i] != b2[i]:
                    print('         …%s' % a[max(0, i - 30):i + 30])
                    print('         …%s' % b2[max(0, i - 30):i + 30])
                    break
    if not [x for x in bad if 'kor1' in x]:
        ok('해석 팝업 글자 = 원고 (span 제거 후 대조)')

    # ---------- 4. mp3 존재 ----------
    if not os.path.isdir(P.ops(n)):
        print('  건너뜀  mp3·이미지 검사 (실제 ops 폴더가 없는 환경)')
        _media_check = False
    else:
        _media_check = True
    mp3dir = os.path.join(P.ops(n), 'media', 'mp3')
    have = set(os.listdir(mp3dir)) if os.path.isdir(mp3dir) else set()
    miss = set()
    for f in files:
        t = open(f, encoding='utf-8').read()
        for m in re.findall(r'media/mp3/([A-Za-z0-9_\-]+\.mp3)', t):
            if have and m not in have:
                miss.add(m)
    if not _media_check:
        pass
    elif not have:
        fail('media/mp3 폴더를 못 찾음: %s' % mp3dir)
    elif miss:
        fail('없는 mp3 %d개: %s' % (len(miss), ', '.join(sorted(miss)[:8])))
    else:
        ok('참조하는 mp3 전부 있음')

    # ---------- 5. 배경 이미지 ----------
    for page in (pages if _media_check else []):
        d = os.path.join(P.ops(n), 'images', page)
        if not os.path.isdir(d):
            fail('images/%s 폴더 없음' % page)
            continue
        need = ['read_bg.png']
        for cls, img in _titles(page):
            need += [img, img.replace('.png', '_h.png'), img.replace('.png', '_b.png')]
        for f in need:
            if not os.path.isfile(os.path.join(d, f)):
                fail('images/%s/%s 없음' % (page, f))
    if _media_check and not [x for x in bad if 'images/' in x]:
        ok('배경·제목 이미지 전부 있음')

    # ---------- 6. scrollTop ----------
    for page in pages:
        h = open(os.path.join(OUTDIR, page + '.html'), encoding='utf-8').read()
        tot = len(re.findall(r'<comp-language-target', h))
        nsc = len(re.findall(r'scrollTop="', h))
        if nsc == 0 and tot > 6:
            fail('%s scrollTop 이 하나도 없음 — read_measure.py 를 돌렸나?' % page)
    if not [x for x in bad if 'scrollTop' in x]:
        ok('scrollTop 주입됨')

    # ---------- 7. 해석 비어 있는 곳 ----------
    holes = []
    for page in pages:
        h = open(os.path.join(OUTDIR, page + '.html'), encoding='utf-8').read()
        for m in re.findall(r'interpretText[^>]*>([^<]*)<', h):
            if m.strip() in ('', '해석x'):
                holes.append(page)
                break
    if holes:
        print('  알림  한글 해석이 비었거나 `해석x` 인 쪽: %s' % ', '.join(sorted(set(holes))))

    print('\n[verify] %s' % ('통과' if not bad else '%d건 확인 필요' % len(bad)))
    return not bad


def _titles(page):
    p = read_gen.PAGES[page]
    fname = {'mainTitle': 'title', 'sTit01': 's_title01', 'sTit02': 's_title02',
             'sTit03': 's_title03', 'sTit04': 's_title04'}
    out = ([(p['title']['cls'].split()[-1], fname[p['title']['cls'].split()[-1]] + '.png')]
           if p['title'] else [])
    for k, b in p['blocks']:
        if k == 'subtit':
            c = b['cls'].split()[-1]
            out.append((c, fname[c] + '.png'))
    return out


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(0 if verify(n, out) else 1)
