# -*- coding: utf-8 -*-
"""프로토 분석 — 견본으로 삼은 페이지에서 '다른 단원에도 그대로 쓰는 것' 만 뽑는다.

사용자가 고른 것만 읽는다.
  · 프로토 ops 폴더 안, 고른 페이지의 html 과 그 css
  · 사용자가 지정한 음원 엑셀의 그 과 시트
  · 사용자가 지정한 스토리보드 파일의 시트 이름
그 밖의 폴더는 들여다보지 않는다.

뽑은 것은 rules/<레시피>/proto_L<N>.json 으로 간다.
이 단계에서는 생성에 쓰지 않는다. 코드와 견주어 보여 줄 뿐이다.

  py proto_scan.py cj_reading 6 p105_01 p106_01
  py proto_scan.py cj_reading 6              (ops 안 p*.html 전부)
"""
import io, os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import rules_io


def pages_in(ops):
    """프로토 ops 폴더에 있는 본문 페이지 이름. 고를 거리를 보여 주려는 것뿐."""
    if not os.path.isdir(ops):
        return []
    out = []
    for f in sorted(os.listdir(ops)):
        m = re.match(r'^(p\d{3}_\d{2})\.html$', f)
        if m:
            out.append(m.group(1))
    return out


def _read(path):
    return io.open(path, encoding='utf-8', errors='replace').read()


def _pageno(page):
    m = re.match(r'^p(\d+)', page)
    return int(m.group(1)) if m else 0


# ---------------------------------------------------------------- 뼈대·팝업
def scan_page(html):
    """페이지 하나에서 본 것들."""
    d = {}
    d['css'] = re.findall(r'<link rel="stylesheet" href="([^"]+)"', html)
    d['js'] = re.findall(r'<script src="([^"]+)"', html)
    m = re.search(r'data-speed-btn="([^"]+)"', html)
    d['speedBtn'] = m.group(1) if m else ''
    # 팝업: data-use 가 붙은 것
    d['use'] = {}
    for a, b in re.findall(r'data-pop-idx="(\d+)" data-use="([a-zA-Z]+)"', html):
        d['use'][b] = int(a)
    for b, a in re.findall(r'data-use="([a-zA-Z]+)" data-pop-idx="(\d+)"', html):
        d['use'].setdefault(b, int(a))
    # 여는 단추
    d['btn'] = {}
    for cls, idx in re.findall(r'js-openPopBtn ([\w]+)" data-pop-idx="(\d+)"', html):
        d['btn'][cls] = int(idx)
    for idx, cls in re.findall(r'data-pop-idx="(\d+)"[^>]*class="[^"]*js-openPopBtn ([\w]+)"', html):
        d['btn'].setdefault(cls, int(idx))
    d['mp4'] = re.findall(r'<source src="([^"]+\.mp4)"', html)
    d['vtt'] = re.findall(r'track kind="captions" src="([^"]+)"', html)
    d['mp3'] = re.findall(r'src="[^"]*media/mp3/([^"/]+\.mp3)"', html)
    # 쪽의 갈래 — 본문인지 들머리(Read Smart)인지. 뼈대가 서로 다르다.
    d['kind'] = 'intro' if any('read_smart' in c for c in d['css']) else 'body'
    return d


def scan_css(css):
    d = {}
    for m in re.finditer(r'url\(\.\./images/(p\d{3}_\d{2})/([\w]+)\.png\)', css):
        d.setdefault(m.group(2), 'images/{page}/%s.png' % m.group(2))
    return d


# ---------------------------------------------------------------- 자료 시트
def scan_sound(xlsx, lesson):
    """지정한 음원 엑셀에서 그 과 시트만 본다. 열 자리와 ID 모양을 확인한다."""
    import openpyxl
    out = {'sheet': '', 'colId': None, 'colText': None, 'ids': [], 'corner': []}
    if not xlsx or not os.path.isfile(xlsx):
        out['error'] = '음원 엑셀을 찾지 못했습니다'
        return out
    wb = openpyxl.load_workbook(xlsx, data_only=True, read_only=True)
    want = '%d과' % int(lesson)
    if want not in wb.sheetnames:
        out['error'] = '%s 시트가 없습니다' % want
        return out
    out['sheet'] = want
    pat = re.compile(r'^\d+-\d{3}-[^-]+(?:-[^-]+)*?-\d+(?:-\d+)*$')
    hit = {}
    rows = []
    for i, r in enumerate(wb[want].iter_rows(values_only=True)):
        rows.append(r)
        if i > 400:
            break
    for r in rows:
        for c, v in enumerate(r):
            s = str(v).strip() if v else ''
            if s and pat.match(s):
                hit[c] = hit.get(c, 0) + 1
    if hit:
        out['colId'] = max(hit, key=lambda k: hit[k])
        # 글은 ID 바로 왼쪽에서 가장 자주 채워진 열
        left = {}
        for r in rows:
            for c in range(out['colId']):
                if c < len(r) and r[c] and str(r[c]).strip():
                    left[c] = left.get(c, 0) + 1
        if left:
            out['colText'] = max(left, key=lambda k: left[k])
        for r in rows:
            if out['colId'] < len(r) and r[out['colId']]:
                s = str(r[out['colId']]).strip()
                if pat.match(s):
                    out['ids'].append(s)
    for s in out['ids']:
        m = re.match(r'^\d+-\d{3}-(.+?)-\d+(?:-\d+)*$', s)
        if m and m.group(1) not in out['corner']:
            out['corner'].append(m.group(1))
    return out


def scan_storyboard(xlsx):
    import openpyxl
    if not xlsx or not os.path.isfile(xlsx):
        return {'error': '스토리보드 파일을 찾지 못했습니다', 'sheets': []}
    wb = openpyxl.load_workbook(xlsx, data_only=True, read_only=True)
    return {'sheets': list(wb.sheetnames)}


# ---------------------------------------------------------------- 모으기
def scan(rid, lesson, ops, pages, sound_xlsx=None, sb_xlsx=None, write=True):
    """고른 페이지만 읽어 proto_L<N>.json 을 만든다.

    write=False 면 파일로 쓰지 않고 dict 만 돌려준다 (대조할 때 쓴다).
    """
    if not os.path.isdir(ops):
        raise RuntimeError('프로토 ops 폴더를 찾지 못했습니다: %s' % ops)
    pages = list(pages or [])
    if not pages:
        pages = pages_in(ops)
    if not pages:
        raise RuntimeError('프로토 페이지가 없습니다: %s' % ops)

    d = rules_io.blank(rid, 'proto')
    d['proto'] = {'lesson': lesson, 'ops': ops, 'pages': pages}
    notes = []
    seen, quiz = [], {}
    assets = {}
    for pg in pages:
        hp = os.path.join(ops, '%s.html' % pg)
        if not os.path.isfile(hp):
            notes.append('%s.html 없음 — 건너뜀' % pg)
            continue
        s = scan_page(_read(hp))
        s['page'] = pg
        # 그 쪽만의 css/js 는 이름을 {page} 로 돌려 놓는다. 쪽마다 다른 건 당연하다.
        for key in ('css', 'js'):
            s[key] = [v.replace(pg, '{page}') for v in s[key]]
        seen.append(s)
        if s['kind'] == 'body' and 'readingQuiz' in s['use']:
            quiz[pg] = s['use']['readingQuiz']
        cp = os.path.join(ops, 'css', '%s.css' % pg)
        if os.path.isfile(cp):
            assets.update(scan_css(_read(cp)))
    if not seen:
        raise RuntimeError('읽을 수 있는 프로토 페이지가 없습니다')

    # --- 뼈대: 쪽의 갈래(본문/들머리)마다 따로 본다. 갈래 안에서는 같아야 한다.
    kinds = {}
    for s in seen:
        kinds.setdefault(s['kind'], []).append(s)
    for kind, group in sorted(kinds.items()):
        for key in ('css', 'js', 'speedBtn'):
            vals = [json.dumps(g[key], ensure_ascii=False) for g in group]
            k = 'skeleton.%s.%s' % (kind, key)
            if len(set(vals)) == 1:
                rules_io.put(d, k, group[0][key], 'html', '%d쪽 모두 같음' % len(group))
            else:
                rules_io.put(d, k, group[0][key], 'html',
                             '쪽마다 다름 — %s 기준' % group[0]['page'])
                notes.append('%s 가 쪽마다 다릅니다' % k)
    rules_io.put(d, 'info.pageKinds',
                 {k: [g['page'] for g in v] for k, v in sorted(kinds.items())},
                 'html', '들머리는 뼈대가 본문과 다릅니다')
    body = kinds.get('body', [])
    if not body:
        notes.append('고른 쪽에 본문 페이지가 없습니다 — 팝업·이름 틀을 뽑지 못했습니다')

    # --- 팝업 번호 (본문 쪽에서)
    for s in body:
        for use, idx in s['use'].items():
            if use == 'readingQuiz':
                continue
            k = 'popup.%s' % use
            was = d['items'].get(k)
            if was and was['value'] != idx:
                notes.append('%s 가 쪽마다 다릅니다 (%s vs %s)' % (k, was['value'], idx))
            rules_io.put(d, k, idx, 'html')
    # 여는 단추 — 쪽마다 값이 같은 것만 규칙으로 삼는다
    btn = {}
    for s in body:
        for cls, idx in s['btn'].items():
            btn.setdefault(cls, {})[s['page']] = idx
    for cls, per in sorted(btn.items()):
        vals = set(per.values())
        if len(vals) == 1:
            rules_io.put(d, 'popup.btn.%s' % cls, vals.pop(), 'html')
        else:
            rules_io.put(d, 'info.btn.%s' % cls, per, 'html',
                         '쪽마다 다름 — 규칙은 popup.quiz 쪽을 보세요')
    for s in kinds.get('intro', []):
        for use, idx in s['use'].items():
            rules_io.put(d, 'popup.intro.%s' % use, idx, 'html', s['page'])
    if quiz:
        vals = sorted(set(quiz.values()))
        if len(vals) == 1:
            rules_io.put(d, 'popup.quiz.other', vals[0], 'html',
                         '고른 %d쪽이 모두 %d — 마지막 쪽을 함께 골라야 예외가 보입니다'
                         % (len(quiz), vals[0]))
        else:
            last = max(quiz, key=_pageno)
            rules_io.put(d, 'popup.quiz.last', quiz[last], 'html', '마지막 쪽 %s' % last)
            other = [v for p, v in quiz.items() if p != last]
            rules_io.put(d, 'popup.quiz.other', max(set(other), key=other.count), 'html',
                         '나머지 %d쪽' % len(other))

    # --- 파일 이름 틀
    for name, tpl in sorted(assets.items()):
        key = {'read_bg': 'assets.bg', 'title': 'assets.title'}.get(name, 'info.img.%s' % name)
        rules_io.put(d, key, tpl, 'css')
    ln = str(lesson)
    for s in body:
        for v in s['mp4']:
            g = re.sub(r'l%s_' % ln, 'l{lesson}_', v)
            key = 'assets.videoScript' if 'script' in v else 'assets.video'
            rules_io.put(d, key, g, 'html')
        for v in s['vtt']:
            rules_io.put(d, 'assets.vtt', re.sub(r'l%s_' % ln, 'l{lesson}_', v), 'html')

    # --- 음원 엑셀
    snd = scan_sound(sound_xlsx, lesson)
    if snd.get('error'):
        notes.append('음원 엑셀: %s' % snd['error'])
    else:
        rules_io.put(d, 'sound.sheet', '%d과', 'xlsx', '본 것: %s' % snd['sheet'])
        rules_io.put(d, 'sound.col.id', snd['colId'], 'xlsx')
        rules_io.put(d, 'sound.col.text', snd['colText'], 'xlsx')
        if snd['corner']:
            rules_io.put(d, 'sound.corner', snd['corner'], 'xlsx')
        # mp3 이름 규칙을 페이지에 박힌 파일 이름으로 확인한다
        want = set()
        for s in body:
            want |= set(os.path.splitext(x)[0] for x in s['mp3'])
        made = set(i.replace('-', '_').lower() for i in snd['ids'])
        if want:
            miss = sorted(want - made)
            rules_io.put(d, 'sound.mp3', {'sep': '_', 'case': 'lower'}, 'xlsx',
                         '페이지 mp3 %d개 중 %d개가 시트 ID 와 맞음'
                         % (len(want), len(want) - len(miss)))
            if miss:
                notes.append('시트에서 못 찾은 mp3: %s' % ', '.join(miss[:5]))
        if snd['ids']:
            import read_import
            bad = [i for i in snd['ids'] if not read_import.IDPAT.match(i)]
            rules_io.put(d, 'sound.idPattern', read_import.IDPAT.pattern, 'xlsx',
                         'ID %d개 중 %d개가 이 모양' % (len(snd['ids']), len(snd['ids']) - len(bad)))
            if bad:
                notes.append('모양이 다른 ID: %s' % ', '.join(bad[:5]))

    # --- 스토리보드 시트
    sb = scan_storyboard(sb_xlsx)
    if sb.get('error'):
        notes.append('스토리보드: %s' % sb['error'])
    else:
        for name in sb['sheets']:
            rules_io.put(d, 'storyboard.sheet.%s' % name, True, 'xlsx')

    # --- 프로토에서 볼 수 없는 것은 솔직히 적어 둔다
    for key in ('measure.safeBody', 'measure.safePop', 'measure.gapKr'):
        rules_io.put(d, key, None, 'none', '프로토 HTML 로는 알 수 없음 — 코드 값 유지')

    d['notes'] = notes
    if not write:
        return d
    path = rules_io.save(d, rules_io.proto_path(rid, lesson))
    return {'path': path, 'items': len(d['items']), 'pages': pages, 'notes': notes}


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__)
        return
    rid, lesson, pages = a[0], a[1], a[2:]
    import runner, read_paths
    recipe = runner.load_recipe(rid)
    ctx = runner.Ctx(recipe, runner.load_settings().get(rid, {}))
    if hasattr(recipe, 'setup'):
        recipe.setup(ctx)
    ops = recipe.out_dir(ctx, int(lesson))
    r = scan(rid, int(lesson), ops, pages,
             sound_xlsx=read_paths.SND, sb_xlsx=read_paths.storyboard(int(lesson)))
    print('%s\n항목 %d개, 쪽 %s' % (r['path'], r['items'], ', '.join(r['pages'])))
    for n in r['notes']:
        print('  · %s' % n)


if __name__ == '__main__':
    main()
