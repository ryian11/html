# -*- coding: utf-8 -*-
"""data<N>.py 초안 만들기 — 원고에서 자동으로 긁어온다.

  python read_import.py 7 --out data7.py
  python read_import.py 6 --diff data6.py      손으로 만든 것과 대조 (자기시험)
  python read_import.py 7 --pages 122,123      그 쪽만

긁어오는 곳
  · 녹음 대본 <N>과 시트    영어 문장 · mp3 이름 · 단어 차례 · 퀴즈 · Think About · Read Smart
  · 스토리보드 Lesson <N>   구문 해설(|n| 자리)
  · 지도서 각론<N> PDF      한글 해석 · 문단 나눔
  · lesson<NN>/ops/images/  배경·제목 이미지 원본 크기

사람이 봐야 하는 것 — 초안에 `# ???` 로 적어 둔다
  · 같은 낱말이 한 쪽에 여러 번 나올 때 어느 자리에 팝업이 붙는지
  · 배경 그림 위 문단 위치(CSS_LAYOUT) · 제목 이미지 위 버튼 위치(WORDBTN)

※ 음원 파일은 열지 않는다. 시트의 파일명을 규칙대로 바꾸기만 한다.
"""
import os, re, sys, struct, unicodedata
import read_paths as P
import rules_io

WARN = []

# ------------------------------------------------------------ rules.json 연결
# read_gen.py 의 load_rules()/R() 과 같은 모양이다 — 없으면 지금까지 쓰던 값
# (default) 그대로 돌려주고, 무엇이 없었는지만 적어 둔다. 그래서 rules.json 이
# 아직 비어 있어도(또는 이 키가 없어도) 추출 결과는 지금까지와 같다.
RULES = {}
MISSED = []


def load_rules(rid):
    global RULES
    RULES = rules_io.values(rid) if rid else {}
    del MISSED[:]
    return RULES


def R(key, default):
    v = RULES.get(key)
    if v is None:
        if key not in MISSED:
            MISSED.append(key)
        return default
    return v


def missed_rules():
    return list(MISSED)


def warn(m):
    WARN.append(m)


# ------------------------------------------------------------------ 공통
def mp3name(sheet_id):
    """시트 파일명 → mp3 이름.  '3-125-Read-07-1' → '3_125_read_07_1'"""
    cfg = R('sound.mp3', {'sep': '_', 'case': 'lower'}) or {}
    sep = cfg.get('sep', '_')
    s = sheet_id.strip().replace('-', sep).replace(' ', sep)
    return s.lower() if cfg.get('case', 'lower') == 'lower' else s


def norm(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    return re.sub(r'\s+', ' ', s).strip()


def keytxt(s):
    """비교용: 따옴표·대시 차이를 없앤다"""
    s = norm(s).lower()
    for a, b in (('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'),
                 ('–', '-'), ('—', '-')):
        s = s.replace(a, b)
    return s


def hangul_ratio(s):
    ch = [c for c in s if not c.isspace()]
    return sum(1 for c in ch if '가' <= c <= '힣') / len(ch) if ch else 0.0


def is_title_line(s):
    """제목·소제목인가 — 끝에 마침표가 없고 대문자 낱말이 많다"""
    s = norm(s)
    if not s or s.endswith('.'):
        return False
    w = [x for x in re.findall(r"[A-Za-z][A-Za-z'’]*", s) if len(x) >= 3]
    if len(w) < 2:
        return False
    return sum(1 for x in w if x[0].isupper()) / len(w) >= 0.6


def seqkey(s):
    return tuple(int(x) for x in s.split('-'))


# ------------------------------------------------------------ 1. 녹음 대본
SPEAK = re.compile(r'^[MWGB]\s*\d?\s*:\s*')
# 녹음 대본의 화자 표기 — 성우에게 주는 말이지 교과서 글이 아니다.
#   'W1(Teacher): “Good morning!”'         → '“Good morning!”'
#   '… said, W1(Teacher): “Diana has …'    → '… said, “Diana has …'
#   '“Am I a dancer?” W: thought Diana.'   → '“Am I a dancer?” thought Diana.'
SPEAK_ROLE = re.compile(r'\b[MWGB]\s*\d?\s*\([^)]{1,24}\)\s*:\s*')
SPEAK_MID = re.compile('(?<=[\u201d\u2019"\'])\\s*[MWGB]\\s*\\d?\\s*:\\s+')


def unspeak(t):
    t = SPEAK.sub('', t)
    t = SPEAK_ROLE.sub('', t)
    t = SPEAK_MID.sub(' ', t)
    return t.strip()
IDPAT = re.compile(r'^\d+-(\d{3})-(.+?)-(\d+(?:-\d+)*)$')


def sound(n):
    """<N>과 시트 → (쪽 차례, {쪽: {코너: [(seq, 글, 파일명), ...]}})

    시트 이름·열 자리·ID 모양은 rules.json 에 있으면 그 값을, 없으면 지금까지
    코드에 있던 기본값(IDPAT 등)을 그대로 쓴다 — 그래서 rules.json 이 비어
    있어도 결과가 달라지지 않는다. project.json/project_rules.json 이 단원별로
    정해 둔 시트 이름(P.unit(n)['sheet'])이 있으면 그게 항상 우선이다(예전과 같다).
    """
    import openpyxl
    wb = openpyxl.load_workbook(P.SND, data_only=True, read_only=True)
    sheet = P.unit(n).get('sheet') or (R('sound.sheet', '%d과') % int(n))
    if sheet not in wb.sheetnames:
        raise SystemExit('녹음 대본에 %s 시트가 없습니다' % sheet)
    idcol = R('sound.col.id', 2)
    txtcol = R('sound.col.text', 1)
    idpat = re.compile(R('sound.idPattern', IDPAT.pattern))
    pages, order = {}, []
    for r in wb[sheet].iter_rows(values_only=True):
        fid, txt = str(r[idcol] or '').strip(), norm(r[txtcol])
        if not fid or not txt:
            continue
        m = idpat.match(fid)
        if not m:
            continue
        pg, corner, seq = m.group(1), m.group(2), m.group(3)
        key = corner.replace('-', '').lower()
        if pg not in pages:
            pages[pg] = {}
            order.append(pg)
        pages[pg].setdefault(key, []).append((seq, unspeak(txt), fid))
    for pg in pages:
        for k in pages[pg]:
            pages[pg][k].sort(key=lambda x: seqkey(x[0]))
    return order, pages


# ------------------------------------------------------------ 2. 스토리보드
def syntax_sentences(n):
    """구문 해설 시트 → {쪽: [교과서 문장, ...]}  (차례 = |n| 번호)"""
    import openpyxl
    # project_rules.json 의 patterns.storyboardSheets.syntax 가 최우선(프로젝트마다
    # 시트 이름이 다를 수 있다). rules.json 의 storyboard.sheet.syntax 는 지금까지
    # 아무 데서도 채워진 적이 없는 이름이라 사실상 항상 기본값으로 빠졌던 자리다 —
    # 그 자리는 그대로 두고(하위 호환), 그 앞에 프로젝트별 값을 먼저 본다.
    sheet = P.STORYBOARD_SHEETS.get('syntax') or R('storyboard.sheet.syntax', '구문 해설')
    ws = openpyxl.load_workbook(P.storyboard(n), data_only=True)[sheet]
    out = {}
    for i, r in enumerate(ws.iter_rows(values_only=True), 1):
        if i == 1 or not r[0] or not r[1]:
            continue
        out.setdefault(P.pgkey(r[0]), []).append(norm(r[1]))
    return out


# ------------------------------------------------------------ 3. 지도서 PDF
JOIN = '\u2307'          # 줄 이음매 표시 (나중에 지운다)
KR_SPLIT = re.compile(r'(?<=[다요라오]\.)\s+|(?<=[?!])\s+')


def korean_stream(n, need=None):
    """'본문 해석' 덩어리 → [(문단시작?, 문장), ...]  차례 = 본문 차례"""
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            warn('pymupdf 가 없어 한글 해석을 못 읽었습니다 (pip install pymupdf)')
            return None
    path = P.guide_pdf(n)
    if not path:
        warn('지도서 각론%d PDF 를 못 찾아 한글 해석을 비웠습니다' % n)
        return None
    doc = pymupdf.open(path)

    start = None
    for i in range(doc.page_count):
        for b in doc[i].get_text('blocks'):
            if '본문 해석' in b[4]:
                start = (i, b[0], b[1])
                break
        if start:
            break
    if not start:
        warn("지도서에서 '본문 해석' 딱지를 못 찾았습니다")
        return None
    pi, lx, ly = start

    # 쪽마다 칸의 x 가 다르므로 들여쓰기 기준을 쪽별로 잡는다
    marked = []                      # (문단시작?, 줄)
    for i in range(pi, min(pi + 3, doc.page_count)):
        bs = [b for b in doc[i].get_text('blocks') if hangul_ratio(b[4]) > 0.55]
        if i == pi:
            bs = [b for b in bs if b[1] > ly and abs(b[0] - lx) < 60]
        else:
            if not bs:
                continue
            xs = sorted(b[0] for b in bs)
            base0 = xs[len(xs) // 2]
            bs = [b for b in bs if abs(b[0] - base0) < 60]
        rows = []
        band = (min(x[0] for x in bs) - 40, max(x[0] for x in bs) + 60)
        for bl in doc[i].get_text('dict')['blocks']:
            for ln in bl.get('lines', []):
                t = ''.join(sp['text'] for sp in ln['spans']).strip()
                x0, y0 = ln['bbox'][0], ln['bbox'][1]
                if not t or hangul_ratio(t) <= 0.55:
                    continue
                if not (band[0] <= x0 <= band[1]):
                    continue
                if i == pi and y0 <= ly:
                    continue
                rows.append((round(y0), round(x0), round(ln['bbox'][2]), t))
        rows.sort()
        if not rows:
            continue
        base = min(x for _, x, _, _ in rows)
        rmax = max(x1 for _, _, x1, _ in rows)
        pitches = [rows[k][0] - rows[k - 1][0] for k in range(1, len(rows))]
        pitch = sorted(pitches)[len(pitches) // 2] if pitches else 0
        prev_y, prev_full = None, False
        for y, x, x1, ln in rows:
            gap = bool(prev_y is not None and pitch and (y - prev_y) > pitch * 1.6)
            newline = (not prev_full) or gap or (x - base > 4)
            marked.append((newline, gap or (x - base > 4), ln))
            prev_y, prev_full = y, (x1 >= rmax - 12)
    if not marked:
        return None

    # 줄 잇기: 앞줄이 오른쪽 끝까지 찼을 때만 이어 붙인다
    paras = []
    for newline, pstart, ln in marked:
        if newline or not paras:
            paras.append([pstart, ln])
        else:
            t = paras[-1][1]
            paras[-1][1] = t + (' ' if t[-1:] in '.?!' else JOIN) + ln

    out = []
    for pstart, t in paras:
        t = norm(t)
        for k, sent in enumerate([x.strip() for x in KR_SPLIT.split(t) if x and x.strip()]):
            out.append((pstart and k == 0, sent))
    if need and len(out) > need:
        out = out[:need]
    return out


# ------------------------------------------------------------ 4. 이미지 크기
def page_key(n, pg, pi):
    """그 쪽의 파일 이름.

    본문이 몇 번째 칸에서 시작하는지는 단원마다 다르다
    (1~8단원은 들머리 쪽 다음이라 _02, Special Lesson 은 Intro·BWR 다음이라 _03).
    산출 폴더의 images/ 가 그 답을 이미 갖고 있으므로 거기서 읽는다.
    못 찾으면 예전 규칙(첫 쪽 _02, 나머지 _01)을 그대로 쓴다.
    """
    base = os.path.join(P.ops(n), 'images')
    if os.path.isdir(base):
        cand = sorted(d for d in os.listdir(base)
                      if re.match(r'^p%s_\d{2}$' % pg, d)
                      and os.path.isfile(os.path.join(base, d, 'read_bg.png')))
        if cand:
            return cand[0]
    return 'p%s_%02d' % (pg, 2 if pi == 0 else 1)


def png_size(path):
    with open(path, 'rb') as f:
        h = f.read(24)
    if h[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    return struct.unpack('>II', h[16:24])


def img_sizes(n, page):
    d = os.path.join(P.ops(n), 'images', page)
    keys = [('read_bg.png', 'bg'), ('title.png', 'title'), ('s_title01.png', 's1'),
            ('s_title02.png', 's2'), ('s_title03.png', 's3'), ('s_title04.png', 's4')]
    out = {}
    if not os.path.isdir(d):
        return out
    for f, k in keys:
        p = os.path.join(d, f)
        if os.path.isfile(p):
            s = png_size(p)
            if s:
                out[k] = s
    return out


# ------------------------------------------------------------ 5. 조립
def wordpat(w):
    e = re.escape(w)
    yield r'\b%s\b' % e
    yield r'\b%s\w*\b' % e
    if w.endswith('e'):
        yield r'\b%s\w*\b' % re.escape(w[:-1])
    if len(w) > 4:
        yield r'\b%s\w*\b' % re.escape(w[:-1])
    # 구동사(turn on, take on …)는 앞말이 변한다 — 'turn on' 이 'turned on' 으로.
    parts = w.split()
    if len(parts) > 1:
        head, rest = parts[0], r'\s+'.join(re.escape(x) for x in parts[1:])
        h = re.escape(head)
        yield r'\b%s\w*\s+%s\b' % (h, rest)
        if len(head) > 3:
            yield r'\b%s\w*\s+%s\b' % (re.escape(head[:-1]), rest)


def place_words(units, words):
    """units = [{'text':..,'title':bool}, ...] 에 [mark:n: w] 를 차례대로 박는다.
    돌려주는 것: 제목에 붙는 번호 목록, 애매한 낱말 메모"""
    ins = [[] for _ in units]        # (start, end, idx) — 나중에 뒤에서부터 넣는다
    titlemark, notes = {}, []
    ui, pos = 0, 0
    for idx, w in enumerate(words, 1):
        # 여러 표기(단수/복수/어미변화) 가운데 "가장 앞에 나오는" 자리를 고른다.
        # 제목(그림)은 버튼을 하나만 받는다 — 이미 찼으면 본문에서 다음 자리를 찾는다.
        cands = []
        for pat in wordpat(w):
            rx = re.compile(pat, re.I)
            j, k = ui, pos
            while j < len(units):
                m = rx.search(units[j]['text'], k)
                if m:
                    cands.append((j, m.start(), m.end(), rx))
                    break
                j += 1; k = 0
        if not cands:
            notes.append('%d:%s 를 본문에서 못 찾음' % (idx, w))
            continue
        cands.sort(key=lambda c: c[:2])
        pick = None
        for j, a_, b_, rx in cands:
            if units[j]['title'] and j in titlemark:
                continue                 # 제목은 이미 찼다 — 본문 쪽을 본다
            pick = (j, a_, b_, rx); break
        if pick is None:                 # 본문에 없으면 제목 뒤에서 다시 찾는다
            j0 = cands[0][0]
            rx = cands[0][3]
            for j in range(j0 + 1, len(units)):
                m = rx.search(units[j]['text'])
                if m:
                    pick = (j, m.start(), m.end(), rx); break
        if pick is None:
            notes.append('%d:%s 를 넣을 자리를 못 정했습니다 — 확인' % (idx, w))
            continue
        j, a_, b_, rx = pick
        in_title = any(u['title'] and rx.search(u['text']) for u in units)
        if units[j]['title']:
            titlemark[j] = idx           # 제목은 그림이라 글자 없는 버튼
        else:
            ins[j].append((a_, b_, idx))
        if in_title:
            notes.append('%d:%s 가 제목에도 나옴 — 엑셀 빨간 네모와 맞는지 확인 (지금은 %s)'
                         % (idx, w, '제목' if units[j]['title'] else '본문'))
        ui, pos = j, b_
    for j, lst in enumerate(ins):
        for a, b, idx in sorted(lst, reverse=True):
            t = units[j]['text']
            units[j]['text'] = '%s[mark:%d: %s]%s' % (t[:a], idx, t[a:b], t[b:])
    return titlemark, notes


def assemble(n, only=None):
    order, snd = sound(n)
    syn = syntax_sentences(n)

    # Reading 쪽 = read 코너가 있는 쪽
    pglist = [p for p in order if 'read' in snd[p]]
    if only:
        pglist = [p for p in pglist if p in only]
    if not pglist:
        raise SystemExit('Reading 쪽을 못 찾았습니다')

    # ---- 전체 단원(unit) 목록 : 한글 붙이기용
    units = []            # {'page','seq','text','title'}
    for pi, pg in enumerate(pglist):
        for si, (seq, txt, fid) in enumerate(snd[pg]['read']):
            units.append(dict(page=pg, seq=seq, fid=fid, text=txt,
                              title=is_title_line(txt) and (si == 0 or True)))
    # 첫 줄이 아니면서 제목꼴이 아닌 것은 본문
    for u in units:
        u['title'] = is_title_line(u['text'])

    # ---- 한글 붙이기
    kr = korean_stream(n, need=len(units))
    if kr and len(kr) == len(units):
        odd = sum(1 for u, (_, t) in zip(units, kr)
                  if not (0.25 <= len(t) / max(len(u['text']), 1) <= 1.6))
        if odd > len(units) * 0.3:
            warn('뽑아낸 한글이 본문 길이와 너무 다릅니다(%d/%d) — 다른 칸을 잡은 것 같아 '
                 '전부 해석x 로 두었습니다. 지도서 해석은 손으로 넣으세요.' % (odd, len(units)))
            kr = None
    if kr and len(kr) == len(units):
        for u, (st, s) in zip(units, kr):
            u['kr'], u['pstart'] = s, st
    else:
        if kr:
            warn('한글 해석 %d개 ≠ 본문 %d개 — 전부 해석x 로 두었습니다' % (len(kr), len(units)))
        for u in units:
            u['kr'], u['pstart'] = '해석x', False

    # ---- 쪽별 조립
    PAGES, ORDER, IMG, WORDBTN, NOTES = {}, [], {}, {}, []
    sub = 0
    for pi, pg in enumerate(pglist):
        key = page_key(n, pg, pi)
        ORDER.append(key)
        us = [u for u in units if u['page'] == pg]

        # 낱말 박기 (제목 포함, 차례대로)
        words = [t for _, t, _ in snd[pg].get('word', [])]
        tmark, notes = place_words(us, words)
        for m in notes:
            NOTES.append('%s  %s' % (key, m))

        # 제목이 있는 쪽인가 — 이미지 폴더에 제목 png 가 있으면 그것이 근거,
        # 없으면 첫 줄이 제목꼴인지로 판단한다.
        im = img_sizes(n, key)
        if im:
            has_title = any(k in im for k in ('title', 's1', 's2', 's3', 's4'))
        else:
            has_title = us[0]['title']

        title, start = None, 0
        if has_title:
            head = us[0]; start = 1
            if pi == 0:
                cls = 'mainTitle'
            else:
                sub += 1; cls = 'subTitle sTit%02d' % sub
            title = dict(src=mp3name(head['fid']), en=head['text'], kr=head['kr'],
                         cls=cls, mark='[mark:%d: ]' % tmark[0] if 0 in tmark else '')
        else:
            NOTES.append('%s  제목·소제목이 없는 쪽으로 보았습니다 (제목 이미지 없음)' % key)

        blocks, para = [], []
        for i, u in enumerate(us[start:], start):
            if u['title']:
                if para:
                    blocks.append(('para', para)); para = []
                sub += 1
                blocks.append(('subtit', dict(
                    src=mp3name(u['fid']), en=u['text'], kr=u['kr'],
                    cls='subTitle sTit%02d' % sub,
                    mark='[mark:%d: ]' % tmark[i] if i in tmark else '')))
                continue
            if u['pstart'] and para:
                blocks.append(('para', para)); para = []
            para.append((u['seq'].replace('-', '_'), u['text'], u['kr']))
        if para:
            blocks.append(('para', para))

        # 구문 번호 |n|
        for k, sent in enumerate(syn.get(P.pgkey(pg), []), 1):
            tgt = keytxt(sent)
            done = False
            for bi, (kind, b) in enumerate(blocks):
                if kind != 'para':
                    continue
                for si, (sq, en, kk) in enumerate(b):
                    plain = keytxt(re.sub(r'\[mark:\d+:\s*([^\]]*)\]', r'\1', en))
                    head = tgt[:25]
                    if plain == tgt or tgt in plain or plain.startswith(head) or head in plain:
                        b[si] = (sq, '|%d|%s' % (k, en), kk)
                        done = True; break
                if done:
                    break
            if not done:
                NOTES.append('%s  구문 %d 을 본문에서 못 찾음: %s' % (key, k, sent[:40]))

        ms = snd[pg].get('mission', [])
        PAGES[key] = dict(num=pg, title=title, blocks=blocks,
                          quiz=make_quiz(snd[pg]), think=make_think(snd[pg]),
                          mission=(dict(kr='해석x', en=ms[0][1], src=mp3name(ms[0][2]))
                                   if ms else None))
        IMG[key] = im
        WORDBTN[key] = [] if not tmark else [(0, 0)] * len(tmark)

    return dict(PAGES=PAGES, ORDER=ORDER, IMG=IMG, WORDBTN=WORDBTN,
                READSMART=readsmart(n, snd, pglist[0]), NOTES=NOTES)


LBL = re.compile(r'^Question\s*(\d+)\s*[.:]?$', re.I)


def make_quiz(pgsnd):
    """질문 묶음을 만든다.

    'Question N' 머리줄로 묶는다. 한 쪽에 여러 개일 수 있다.
      · True/False 줄이 따로 있음      → T/F   (6단원 꼴)
      · 머리줄 다음이 질문 하나뿐       → T/F   (7단원 꼴 — 정답 음원이 없다)
      · 머리줄 다음에 질문+정답         → 입력형
      · 입력형이 둘 이상               → 슬라이더(input2)
    """
    rows = pgsnd.get('question', [])
    if not rows:
        return None
    grp, cur = [], None
    for r in rows:
        m = LBL.match(r[1])
        if m:
            cur = dict(label='Q%s' % m.group(1), rows=[])
            grp.append(cur)
        elif cur is not None:
            cur['rows'].append(r)
    grp = [g for g in grp if g['rows']]
    if not grp:
        return None

    explicit_tf = any(r[1].strip() in ('True', 'False') for r in rows)
    items, kinds = [], []
    for g in grp:
        rs = g['rows']
        tf = explicit_tf or len(rs) < 2
        kinds.append('tf' if tf else 'input')
        if tf:
            items.append(dict(label=g['label'], q=rs[0][1], qkr='해석x',
                              ans='1', src=mp3name(rs[0][2])))
        else:
            items.append(dict(label=g['label'], q=rs[0][1], qkr='해석x',
                              a=rs[1][1], akr='해석x',
                              qsrc=mp3name(rs[0][2]), asrc=mp3name(rs[1][2])))

    if all(k == 'tf' for k in kinds):
        return dict(kind='tf', label=[i['label'] for i in items], items=items)
    if len(items) == 1:
        return dict(kind='input', **items[0])
    return dict(kind='input2', label=[i['label'] for i in items], items=items)


def make_think(pgsnd):
    rows = pgsnd.get('thinkaboutthis', [])
    ex = pgsnd.get('thinkaboutthisex', [])
    if not rows:
        return None
    return dict(q=rows[0][1], qkr='해석x', src=mp3name(rows[0][2]),
                ex=[(mp3name(f), t, '해석x') for _, t, f in ex])


def guide_kr(n):
    """지시문 시트 → {음원 파일명: 우리말 지시문}"""
    import openpyxl
    wb = openpyxl.load_workbook(P.storyboard(n), data_only=True)
    ws = wb[wb.sheetnames[0]]
    out = {}
    for r in ws.iter_rows(values_only=True):
        if r and len(r) >= 5 and r[4]:
            out[str(r[4]).strip()] = norm(r[2])
    return out


def readsmart(n, snd, firstpg):
    rows = snd[firstpg].get('readsmart', [])
    krmap = guide_kr(n)
    if len(rows) < 3:
        warn('Read Smart 줄이 %d개뿐입니다 — 도입 페이지를 확인하세요' % len(rows))
    def g(i):
        if i >= len(rows):
            return ('', '', '')
        seq, en, fid = rows[i]
        kr = krmap.get(fid, '')
        if not kr:
            warn('지시문 시트에서 %s 의 우리말을 못 찾았습니다' % fid)
        return (kr, en, mp3name(fid))
    if not rows:
        # Read Smart 들머리 쪽이 없는 단원(Special Lesson)도 있다. 그러면 안 만든다.
        return None
    return dict(page='p%s_01' % firstpg, tit=g(0), sub=g(1), mission=g(len(rows) - 1))


def strip_join(t):
    return t.replace(JOIN, '')


def clear_joins(d):
    """줄 이음매 표시(JOIN)를 본문·제목·해석에서 지운다.

    main() 은 확인 파일을 쓴 뒤 같은 일을 하지만(아래), 레시피 경로에는
    그 단계가 없어 표시가 data<N>.py 까지 따라갔다. 두 곳이 같은 뜻이 되게
    이 함수로 묶어 둔다. strip_join() 자체는 그대로다.
    """
    for page in d['ORDER']:
        p = d['PAGES'][page]
        if p['title']:
            p['title']['kr'] = strip_join(p['title']['kr'])
        for i, (k, b) in enumerate(p['blocks']):
            if k in ('subtit', 'label'):
                b['kr'] = strip_join(b['kr'])
            else:
                p['blocks'][i] = (k, [(s, e, strip_join(kr)) for s, e, kr in b])
    return d


def join_report(units, path):
    """줄 이음매가 든 해석만 모아 확인용 파일로 쓴다"""
    rows = [u for u in units if JOIN in u.get('kr', '')]
    if not rows:
        return 0
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# PDF 줄바꿈에서 띄어쓰기가 사라진 자리입니다. %s 앞뒤를 보고\n'
                '# 붙여야 하면 그대로, 띄어야 하면 공백을 넣어 data 파일을 고치세요.\n\n' % JOIN)
        for u in rows:
            f.write('%s  %s\n    %s\n\n' % (u['page'], u['seq'], u['kr']))
    return len(rows)


# ------------------------------------------------------------ 6. 파일로 쓰기
def q(s):
    return "'" + str(s).replace('\\', '\\\\').replace("'", "\\'") + "'"


def render(n, d):
    L = ['# -*- coding: utf-8 -*-',
         '# %s단원 Reading 본문 페이지 데이터' % n,
         '# read_import.py 가 만든 초안입니다. `# ???` 가 붙은 곳을 확인하세요.',
         '# 출처: 녹음 대본 %s / 스토리보드 %s / 지도서 각론' % (
            P.unit(n).get('sheet') or ('%s과' % n), os.path.basename(P.storyboard(n))),
         '', 'PAGES = {']
    for page in d['ORDER']:
        p = d['PAGES'][page]
        t = p['title']
        qb = p['quiz']['label'] if p['quiz'] else ''
        if isinstance(qb, list):
            qb = '%s~%s' % (qb[0], qb[-1]) if len(qb) > 1 else (qb[0] if qb else '')
        L.append(" %s: dict(" % q(page))
        L.append("   num=%s, qbtn=%s," % (q(p['num']), q(qb)))
        if p.get('paracls'):
            L.append("   paracls=%r," % p['paracls'])
        if t:
            L.append("   title=dict(src=%s, en=%s, kr=%s," % (q(t['src']), q(t['en']), q(t['kr'])))
            L.append("              cls=%s, mark=%s)," % (q(t['cls']), q(t['mark'])))
        else:
            L.append("   title=None,   # 제목·소제목 이미지가 없는 쪽")
        L.append("   blocks=[")
        for kind, b in p['blocks']:
            if kind in ('subtit', 'label'):
                L.append("     (%s, dict(src=%s, en=%s, kr=%s," % (q(kind), q(b['src']), q(b['en']), q(b['kr'])))
                L.append("                      cls=%s, mark=%s))," % (q(b['cls']), q(b['mark'])))
            else:
                L.append("     ('para', [")
                for seq, en, kr in b:
                    L.append("       (%s,%s," % (q(seq), q(en)))
                    L.append("             %s)," % q(kr))
                L.append("     ]),")
        L.append("   ],")
        z = p['quiz']
        if z and z['kind'] == 'input':
            L.append("   quiz=dict(kind='input', label=%s," % q(z['label']))
            L.append("     q=%s, qkr=%s," % (q(z['q']), q(z['qkr'])))
            L.append("     a=%s, akr=%s," % (q(z['a']), q(z['akr'])))
            L.append("     qsrc=%s, asrc=%s)," % (q(z['qsrc']), q(z['asrc'])))
        elif z and z['kind'] == 'input2':
            L.append("   quiz=dict(kind='input2', label=[%s]," % ', '.join(q(x) for x in z['label']))
            L.append("     items=[" + ',\n            '.join(
                "dict(label=%s, q=%s, qkr=%s, a=%s, akr=%s, qsrc=%s, asrc=%s)"
                % (q(i['label']), q(i['q']), q(i['qkr']), q(i['a']), q(i['akr']),
                   q(i['qsrc']), q(i['asrc'])) for i in z['items']) + "]),")
        elif z:
            L.append("   quiz=dict(kind='tf', label=[%s]," % ', '.join(q(x) for x in z['label']))
            L.append("     # ??? 정답(ans) 은 1=True, 2=False 입니다. 원고를 보고 확인하세요.")
            L.append("     items=[" + ',\n            '.join(
                "dict(q=%s, qkr=%s, ans=%s, src=%s)"
                % (q(i['q']), q(i['qkr']), q(i['ans']), q(i['src'])) for i in z['items']) + "]),")
        ms = p.get('mission')
        if ms:
            L.append("   mission=dict(kr=%s," % q(ms['kr']))
            L.append("                en=%s," % q(ms['en']))
            L.append("                src=%s)," % q(ms['src']))
        th = p.get('think')
        if th:
            L.append("   think=dict(q=%s, qkr=%s, src=%s," % (q(th['q']), q(th['qkr']), q(th['src'])))
            L.append("              ex=[" + ',\n                  '.join(
                "(%s,%s,%s)" % (q(a), q(b2), q(c)) for a, b2, c in th['ex']) + "]),")
        L.append(" ),")
        L.append("")
    L.append('}')
    L.append('')
    L.append('ORDER = [%s]' % ','.join(q(x) for x in d['ORDER']))
    L.append('')
    L.append('# 배경 이미지 원본 크기 (png 에서 읽음). 비어 있으면 크기 CSS 를 넣지 않는다.')
    L.append('IMG = {')
    for page in d['ORDER']:
        im = d['IMG'].get(page) or {}
        body = ', '.join('%s=%r' % (k, v) for k, v in im.items())
        L.append(' %s: dict(%s),' % (q(page), body))
    L.append('}')
    L.append('')
    L.append('# ============ 레이아웃 (사람이 눈으로 맞추는 값) ============')
    L.append('')
    L.append('# 제목 이미지 위 단어 버튼 (left, top).')
    L.append('# read_measure.py 가 찍어 주는 "WORDBTN left 후보" 를 넣으세요.')
    L.append('WORDBTN = {')
    for page in d['ORDER']:
        v = d['WORDBTN'].get(page) or []
        L.append(' %s: %r,%s' % (q(page), v, '   # ??? 측정값을 넣으세요' if v else ''))
    L.append('}')
    L.append('')
    L.append('# 배경 그림 위 글자 자리. --layout 파일에서 온다.')
    L.append('CSS_LAYOUT = {')
    css = d.get('CSS') or {}
    for page in d['ORDER']:
        body = css.get(page) or '\n.mainContent .ParagraphBox { margin-top: 30px; }\n'
        L.append(" %s: '''%s''',"  % (q(page), body))
    L.append('}')
    L.append('')
    rs = d['READSMART']
    L.append("# ---------- Read Smart 도입 페이지 ----------")
    L.append("READSMART = '''%s'''" % rs)
    return '\r\n'.join(L)


def build_readsmart(n, rs):
    if not rs:                       # 들머리 쪽이 없는 단원
        return ''
    tpl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'readsmart.tpl')
    if not os.path.isfile(tpl):
        warn('readsmart.tpl 이 없어 도입 페이지를 비웠습니다')
        return ''
    t = open(tpl, encoding='utf-8', newline='').read()
    f = {}
    for k in ('tit', 'sub', 'mission'):
        f['%s_kr' % k], f['%s_en' % k], f['%s_src' % k] = rs[k]
    return t.format(page=rs['page'], **f)


def apply_kr(d, path):
    """{(쪽, seq): 해석} 을 담은 파이썬 파일을 읽어 해석을 채운다"""
    import layout_io
    KR = layout_io.load_kr(path) if isinstance(path, str) else path
    used, miss = set(), []
    for page in d['ORDER']:
        p = d['PAGES'][page]
        num = p['num']
        if p['title']:
            sq = p['title']['src'].rsplit('_', 1)[-1]
            k = (num, sq)
            if k in KR:
                p['title']['kr'] = KR[k]; used.add(k)
            else:
                miss.append('%s 제목' % page)
        for bi, (kind, b) in enumerate(p['blocks']):
            if kind in ('subtit', 'label'):
                sq = b['src'].split('_read_')[-1] if '_read_' in b['src'] else b['src'].rsplit('_', 1)[-1]
                if (num, sq) in KR:
                    b['kr'] = KR[(num, sq)]; used.add((num, sq))
                else:
                    miss.append('%s 소제목' % page)
                continue
            new = []
            for sq, en, kr in b:
                if (num, sq) in KR:
                    kr = KR[(num, sq)]; used.add((num, sq))
                else:
                    miss.append('%s %s' % (page, sq))
                new.append((sq, en, kr))
            p['blocks'][bi] = (kind, new)
    for k in sorted(set(KR) - used):
        warn('해석 파일의 %s-%s 를 쓸 자리가 없습니다' % k)
    for m2 in miss:
        warn('해석 파일에 %s 가 없습니다' % m2)
    return len(used)


def apply_layout(d, path):
    """지면 구조(문단 나눔·라벨·머리표)를 입힌다"""
    import layout_io
    m = layout_io.load(path)
    PARAS, LABELS, PREFIX = m.PARAS, m.LABELS, m.PREFIX
    TEXT, SPK, DROP = m.TEXT, m.SPEAKER, m.DROP
    d['CSS'] = m.CSS
    d['_KR_IN_LAYOUT'] = m.KR           # 해석이 layout 안에 들어 있으면 여기서 받는다
    for k, v in (m.IMG or {}).items():
        if not d['IMG'].get(k):
            d['IMG'][k] = v

    for page in d['ORDER']:
        p = d['PAGES'][page]
        num = p['num']
        flat, subs = {}, []
        for kind, b in p['blocks']:
            if kind in ('subtit', 'label'):
                sq = b['src'].split('_read_')[-1]
                if (num, sq) in DROP:        # 그림에 이미 있는 낱말 — 아예 뺀다
                    continue
                inparas = any(sq in g for g in PARAS.get(num, []))
                if (num, sq) in LABELS or inparas:   # 라벨이거나, 실은 본문 문단
                    flat[sq] = [b['en'], b['kr']]
                else:
                    subs.append((kind, b))
            else:
                for sq, en, kr in b:
                    if (num, sq) in DROP:
                        continue
                    flat[sq] = [en, kr]
        # 지면대로 고친 본문 (앞에 붙은 |n| 구문 번호는 그대로 살린다)
        for (n2, sq), t in TEXT.items():
            if n2 == num and sq in flat:
                m2 = re.match(r'^((?:\|\d+\|)+)', flat[sq][0])
                flat[sq][0] = (m2.group(1) if m2 else '') + t
        # 문단 첫머리(마이크 아이콘 · 말하는 이)는 본문 글자가 아니라 CSS 로 붙인다
        # 라벨
        blocks = []
        for (n2, sq), cls in sorted(LABELS.items(), key=lambda x: x[0][1]):
            if n2 != num or sq not in flat:
                continue
            en, kr = flat.pop(sq)
            blocks.append(('label', dict(src='3_%s_read_%s' % (num, sq), en=en, kr=kr,
                                         cls='readText label %s' % cls, mark='')))
        # 문단
        groups = PARAS.get(num)
        if groups:
            for g in groups:
                items = [(sq, flat[sq][0], flat[sq][1]) for sq in g if sq in flat]
                if items:
                    blocks.append(('para', items))
        else:
            blocks.append(('para', [(sq, v[0], v[1]) for sq, v in flat.items()]))
        blocks += subs
        p['blocks'] = blocks
        # 문단마다 덧클래스 (mic / spk)
        pc, pi = {}, 0
        for kind, b in blocks:
            if kind != 'para':
                continue
            first = b[0][0] if b else None
            k = PREFIX.get((num, first))
            if k:
                pc[pi] = 'mic' if k == 'mic' else 'spk'
            pi += 1
        p['paracls'] = pc
    return True


# --------------------------------------------- 지도서 각론에서 해석 뽑기(guide)
# korean_stream() 과 별개의 길이다. project.json 에서 그 단원에 "kr": "guide"
# 라고 적어 둔 단원만 이리로 온다. 기존 단원은 이 함수를 아예 부르지 않는다.
#
# 각론 지면에서 본 규칙 (각론9 / 중3 Special Lesson 기준)
#   · '본문 해석' 딱지는 한 칼럼에 하나씩, 글자 크기가 본문보다 크다.
#   · 해석은 딱지 바로 아래 같은 칼럼에서 시작해 줄 간격 13 으로 이어지고,
#     다음 덩어리(•설정 취지·그림 설명·활동 지시문)와는 26 이상 벌어진다.
#   · 줄 끝 공백이 원본에 그대로 살아 있다 → 그냥 이어 붙이면 띄어쓰기가 맞다.
#   · 문단 첫 줄은 8~9px 들여쓴다. 문단 마지막 줄에는 줄 끝 공백이 없으므로
#     들여쓰기로 문단을 끊어 주지 않으면 앞뒤 문장이 붙어 버린다.
#   · 드러냄표(작은 ●)는 본문보다 훨씬 작은 글자로 본문 사이에 끼어 있다.
GUIDE_LABEL  = '본문 해석'
GUIDE_MID    = 341.0    # 왼/오 칼럼을 가르는 x
GUIDE_NEAR   = 40       # 딱지에서 첫 줄까지 벌어져도 되는 거리
GUIDE_GAP    = 20       # 줄 사이가 이보다 벌어지면 해석 토막이 끝난 것
GUIDE_MINSZ  = 6.0      # 이보다 작은 글자는 드러냄표·장식 — 버린다
GUIDE_INDENT = 4.0      # 칼럼 기준 x 보다 이만큼 들어가면 새 문단
GUIDE_ROW    = 6.0      # y 를 이 폭으로 묶어 같은 줄로 본다

GUIDE_CUT = re.compile(r'[.!?][”"\'’]?(?=\s|$)')


class GuideError(Exception):
    """각론에서 해석을 못 뽑았다. 조용히 넘어가지 않고 생성을 멈춘다."""


def _guide_plain(s):
    """구문 번호 |n| 과 낱말 표시 [mark:n: ] 를 걷어낸 영어 원문"""
    s = re.sub(r'\|\d+\|', '', s or '')
    return re.sub(r'\[mark:\d+:\s*([^\]]*)\]', r'\1', s).strip()


def _guide_lines(page):
    out = []
    for bl in page.get_text('dict')['blocks']:
        if 'lines' not in bl:
            continue
        for ln in bl['lines']:
            sp = ln['spans'][0]
            t = ''.join(s['text'] for s in ln['spans'])
            if not t.strip() or sp['size'] < GUIDE_MINSZ:
                continue
            out.append((ln['bbox'][0], ln['bbox'][1], t))
    return out


def _guide_sections(path):
    """'본문 해석' 토막을 책 차례대로 [(pdf쪽, 칼럼, [(x, y, 줄), …]), …]"""
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            raise GuideError('pymupdf 가 없어 각론 해석을 못 읽습니다 (pip install pymupdf)')
    doc = pymupdf.open(path)
    out = []
    for i in range(doc.page_count):
        lns = _guide_lines(doc[i])
        for x0, y0, t in lns:
            if t.strip() != GUIDE_LABEL:
                continue
            col = 0 if x0 < GUIDE_MID else 1
            body = sorted([l for l in lns
                           if (0 if l[0] < GUIDE_MID else 1) == col and l[1] > y0 + 5],
                          key=lambda l: (round(l[1] / GUIDE_ROW), l[0]))
            grp, prev = [], None
            for bx, by, bt in body:
                if prev is None:
                    if by - y0 > GUIDE_NEAR:
                        break
                elif by - prev > GUIDE_GAP:
                    break
                grp.append((bx, by, bt))
                prev = by if prev is None else max(prev, by)
            if grp:
                out.append((i, col, grp))
    out.sort(key=lambda s: (s[0], s[1]))
    return out


def _guide_glue(grp):
    """줄을 원본 그대로 이어 붙이되, 문단 경계(들여쓰기)는 \\n 으로 남긴다"""
    base = min(bx for bx, by, bt in grp)
    paras, cur, seen = [], [], set()
    for bx, by, bt in grp:
        row = round(by / GUIDE_ROW)
        if row not in seen and bx > base + GUIDE_INDENT and cur:
            paras.append(''.join(cur))
            cur = []
        seen.add(row)
        cur.append(bt)
    if cur:
        paras.append(''.join(cur))
    return '\n'.join(re.sub(r'[ \t]+', ' ', p).strip() for p in paras)


def _guide_cuts(s):
    """자를 수 있는 자리 — 문장 끝 다음, 그리고 문단 경계"""
    pos = set()
    for m in GUIDE_CUT.finditer(s):
        e = m.end()
        pos.add(e + 1 if e < len(s) and s[e] == ' ' else e)
    for m in re.finditer('\n', s):
        pos.add(m.start() + 1)
    return sorted(p for p in pos if 0 < p < len(s))


def _guide_align(s, ens):
    """영어 문장 길이 비례에 가장 가깝게 s 를 len(ens) 조각으로 나눈다.

    한글 문장부호만으로는 못 나눈다. 이를테면
      영어  The counselor coughed a little and said, “Your daughter is fine.  (한 문장)
      한글  상담사가 약간 기침을 한 뒤 말했다. “당신의 딸은 괜찮아요.        (마침표 두 개)
    그래서 자를 수 있는 자리 가운데 영어 길이 비례와 가장 덜 어긋나는 조합을 고른다.
    """
    n = len(ens)
    pos = sorted(set([0] + _guide_cuts(s) + [len(s)]))
    if len(pos) - 1 < n:
        return None
    tot_e = float(sum(len(e) for e in ens)) or 1.0
    want, acc = [], 0.0
    for e in ens[:-1]:
        acc += len(e) / tot_e * len(s)
        want.append(acc)
    INF, m = float('inf'), len(pos)
    best = [[INF] * m for _ in range(n)]
    back = [[-1] * m for _ in range(n)]
    best[0][0] = 0.0
    for k in range(1, n):
        run, ri = INF, -1
        for j in range(1, m):
            if best[k - 1][j - 1] < run:
                run, ri = best[k - 1][j - 1], j - 1
            if run < INF:
                best[k][j] = run + abs(pos[j] - want[k - 1])
                back[k][j] = ri
    bb, bj = INF, -1
    for j in range(1, m):
        if best[n - 1][j] < bb:
            bb, bj = best[n - 1][j], j
    if bj < 0:
        return None
    chain, j = [], bj
    for k in range(n - 1, 0, -1):
        chain.append(pos[j])
        j = back[k][j]
    chain.reverse()
    b = [0] + chain + [len(s)]
    return [re.sub(r'\s+', ' ', s[b[i]:b[i + 1]]).strip() for i in range(n)]


def guide_stream(n, d):
    """각론 '본문 해석' → {(쪽, seq): 해석}. 못 뽑으면 GuideError.

    d 는 assemble() 이 막 돌려준 것이어야 한다 — 지면 구조(apply_layout)를
    입히기 전이라야 그림 라벨·출처가 아직 subtit 로 남아 있다.
    """
    import difflib
    path = P.guide_pdf(n)
    if not path:
        raise GuideError('지도서 각론 PDF 를 못 찾았습니다')
    secs = _guide_sections(path)
    pages = [pg for pg in d['ORDER']
             if any(k == 'para' for k, b in d['PAGES'][pg]['blocks'])]
    if len(secs) != len(pages):
        raise GuideError("각론의 '본문 해석' 토막 %d개 ≠ 본문 쪽 %d개 (%s)"
                         % (len(secs), len(pages), os.path.basename(path)))
    out = {}
    for pg, (pi, col, grp) in zip(pages, secs):
        p = d['PAGES'][pg]
        num = p['num']
        items, seen = [], []
        if p['title']:
            items.append(('00', _guide_plain(p['title']['en']), True))
        for kind, b in p['blocks']:
            if kind == 'para':
                for sq, en, kr in b:
                    k = re.sub(r'[^a-z]', '', _guide_plain(en).lower())
                    # 같은 쪽에 이미 나온 문장의 되풀이(말풍선)는 본문이 아니다
                    dup = any(difflib.SequenceMatcher(None, k, o).ratio() > .8
                              for o in seen)
                    items.append((sq, _guide_plain(en), not dup))
                    seen.append(k)
            else:
                # 제목·그림 라벨·출처 — 각론 본문 해석에 없는 것들
                src = b.get('src') or ''
                sq = src.split('_read_')[-1] if '_read_' in src else src.rsplit('_', 1)[-1]
                items.append((sq, _guide_plain(b.get('en')), False))
        keep = [j for j, it in enumerate(items) if it[2]]
        got = _guide_align(_guide_glue(grp), [items[j][1] for j in keep])
        if got is None:
            raise GuideError('%s쪽 — 나눌 자리가 본문 %d문장보다 모자랍니다'
                             % (num, len(keep)))
        for it in items:
            out[(num, it[0])] = '해석x'
        for j, g in zip(keep, got):
            out[(num, items[j][0])] = g
    return out


def apply_guide_kr(d, gkr, check=None):
    """각론에서 뽑은 해석을 넣는다. 손으로 넣어 둔 것과 다르면 멈춘다.

    check 가 있으면(= layout<N>.json 의 kr) 개수·차례·글자까지 견준다.
    하나라도 다르면 GuideError — 기존 해석을 조용히 덮어쓰지 않는다.
    """
    if check:
        miss = [k for k in check if k not in gkr]
        extra = [k for k in gkr if k not in check]
        diff = [k for k in check if k in gkr and check[k] != gkr[k]]
        if miss or extra or diff:
            msg = ['각론에서 뽑은 해석이 손으로 넣어 둔 것과 다릅니다 '
                   '— 덮어쓰지 않고 멈춥니다.',
                   '  뽑음 %d개 / 기준 %d개' % (len(gkr), len(check))]
            for k in sorted(miss)[:5]:
                msg.append('  없음 %s-%s' % k)
            for k in sorted(extra)[:5]:
                msg.append('  남음 %s-%s' % k)
            for k in sorted(diff)[:5]:
                msg.append('  다름 %s-%s\n    뽑음: %s\n    기준: %s'
                           % (k[0], k[1], gkr[k], check[k]))
            raise GuideError('\n'.join(msg))
    return apply_kr(d, gkr)


def _beside(name):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    return p if os.path.isfile(p) else None


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    n = int(sys.argv[1])
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    only = None
    if '--pages' in sys.argv:
        only = set(x.strip() for x in sys.argv[sys.argv.index('--pages') + 1].split(','))

    d = assemble(n, only)
    # --layout 을 안 줘도 layout<N>.json 이 있으면 쓴다
    lay = (sys.argv[sys.argv.index('--layout') + 1] if '--layout' in sys.argv
           else _beside('layout%d.json' % n))
    if lay:
        apply_layout(d, lay)
        print('지면 구조 적용:', os.path.basename(lay))
    if '--kr' in sys.argv:
        cnt = apply_kr(d, sys.argv[sys.argv.index('--kr') + 1])
        print('해석 %d개를 채웠습니다' % cnt)
    elif d.get('_KR_IN_LAYOUT'):
        cnt = apply_kr(d, d['_KR_IN_LAYOUT'])
        print('해석 %d개를 채웠습니다 (layout 안)' % cnt)
    d['READSMART'] = build_readsmart(n, d['READSMART'])

    # 이음매 확인 파일
    units = []
    for page in d['ORDER']:
        p = d['PAGES'][page]
        if p['title']:
            units.append(dict(page=page, seq='제목', kr=p['title']['kr']))
        for k, b in p['blocks']:
            if k in ('subtit', 'label'):
                units.append(dict(page=page, seq=k, kr=b['kr']))
            else:
                units += [dict(page=page, seq=s, kr=kr) for s, _, kr in b]
    rep = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kr%d_확인.txt' % n)
    njoin = join_report(units, rep)

    # 이음매 표시는 빼고 쓴다
    for page in d['ORDER']:
        p = d['PAGES'][page]
        if p['title']:
            p['title']['kr'] = strip_join(p['title']['kr'])
        for i, (k, b) in enumerate(p['blocks']):
            if k in ('subtit', 'label'):
                b['kr'] = strip_join(b['kr'])
            else:
                p['blocks'][i] = (k, [(s, e, strip_join(kr)) for s, e, kr in b])

    text = render(n, d)
    if out:
        open(out, 'w', encoding='utf-8', newline='').write(text)
        print('썼습니다:', out)
    else:
        sys.stdout.write(text)

    print('\n--- 확인할 것 ---')
    for w in WARN:
        print('  !', w)
    for m in d['NOTES']:
        print('  ?', m)
    if njoin:
        print('  ? 한글 %d줄에 줄바꿈 이음매가 있습니다 — %s 를 보고 띄어쓰기를 확인하세요'
              % (njoin, os.path.basename(rep)))
    print('  ? CSS_LAYOUT(문단 위치) 과 WORDBTN(버튼 자리) 은 돌려 보고 채우세요')


if __name__ == '__main__':
    main()
