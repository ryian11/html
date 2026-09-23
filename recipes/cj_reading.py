# -*- coding: utf-8 -*-
"""CJ 중3 영어(소영순) — Reading 본문 페이지.

검증된 기존 스크립트를 부르기만 한다. 그 안은 이 파일이 모른다.
  read_import.py → data<N>.py        ① 추출
  read_gen.py    → ops/*.html …      ② 생성
  read_measure.py→ scrolls/krlayout  ③ 측정
  read_verify.py                     ④ 검증
"""
import os, re, sys, glob

GEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if GEN not in sys.path:
    sys.path.insert(0, GEN)
DATA = os.path.join(GEN, '단원자료')       # 단원마다 달라지는 것은 여기 모은다
os.makedirs(DATA, exist_ok=True)
if DATA not in sys.path:
    sys.path.insert(0, DATA)

NAME = 'CJ 중3 Reading 본문'

SLOTS = [
    ('root',          '프로젝트 폴더',        'dir'),
    ('script_xlsx',   '녹음 대본 엑셀',       'file', {'optional': True}),
    ('storyboard_dir', '스토리보드 폴더',     'dir',  {'optional': True}),
    ('guide_dir',     '지도서 각론 PDF 폴더', 'dir',  {'optional': True}),
    ('contents_dir',  '출력 폴더 (contents)', 'dir',  {'optional': True}),
    ('proto_lesson',  '프로토 단원',          'text', {'optional': True,
                                                   'hint': '견본으로 삼을 단원 번호 (예: 6)'}),
    ('proto_ops',     '프로토 ops 폴더',      'dir',  {'optional': True,
                                                   'hint': '비우면 프로토 단원의 실기 폴더'}),
]

# 프로토 분석은 본 생성과 따로 돈다. 생성 결과에 손대지 않는다.
PROTO = True

# UI 에서 고칠 수 있는 파일 (경로는 생성기 폴더 기준)
EDIT = [('layout{n}.json', 'layout')]


# 지금까지 코드에 박혀 있던 값 — project_rules.json 이 아직 없을 때 딱 한 번만
# 옮겨 적는 데 쓴다(마이그레이션). 그 뒤로는 project_rules.json 이 기준이다.
LEGACY_PATHS = {
    'storyboardDir': '01_스토리보드/전자저작물 추가 원고_20260716_아이스캔디 전달',
    'soundXlsx': '02_사운드/중3(소영순) 전자저작물 녹음 대본_최종_20260806 아이스캔디 전달.xlsx',
    'wordDicDir': '02_사운드/단어사전/lesson%02d',
    'contentsDir': '00_개발물/EBOOK/중학교 영어 3_소영순/app/resource/contents',
}
LEGACY_PATTERNS = {
    'storyboardFilename': r'Lesson\s*0*(\d+)\s*\.xlsx$',
    'specialUnitFilename': r'_([A-Za-z][A-Za-z ]*Lesson)\s*\.xlsx$',
    'contentsFolder': r'^lesson0*(\d+)$',
    'pageFilename': r'^(p\d{3}_\d{2})\.html$',
    'guidePdf': '*각론%d*.pdf',
    'soundSheet': '%d과',
}


def setup(ctx):
    """project_rules.json(프로젝트 root 바로 아래)을 프로젝트 구조의 기준으로 삼아
    read_paths 에 꽂는다.

    project_rules.json 이 없으면(첫 실행) 지금까지 코드에 박혀 있던 값 그대로
    한 번 만들어 두고(ensure_migrated), 있으면 그 값을 읽는다. UI 슬롯
    (script_xlsx 등)이 있으면 그 값이 항상 마지막에 이긴다 — 예전과 같다.
    `GEN`(생성기 자기 위치)은 자료가 아니라서 JSON 에 넣지 않고 그대로 계산한다.

    project_rules_io.set_root() 를 매번 다시 불러서 이번 요청의 root 로 맞춘다 —
    그래야 프로젝트 A 를 보던 중에 프로젝트 B 를 열어도 project_rules.json 이
    섞이지 않는다. root 가 없거나 실제 폴더가 아니면(프로젝트 미선택) 이전 요청의
    값이 남아 다른 프로젝트로 새지 않도록 read_paths 쪽 값도 함께 비운다.
    """
    import read_paths as P
    import project_rules_io as PR
    root = ctx.get('root')
    rid = getattr(ctx.recipe, 'ID', 'cj_reading')
    ok_root = bool(root) and os.path.isdir(root)
    PR.set_root(root if ok_root else None)
    if ok_root:
        P.ROOT = root
        pr, _made = PR.ensure_migrated(rid, root,
                                        {'paths': LEGACY_PATHS, 'patterns': LEGACY_PATTERNS})
        pp = pr.get('paths') or {}
        P.SB_DIR = PR.abspath(root, pp.get('storyboardDir') or LEGACY_PATHS['storyboardDir'])
        P.SND = PR.abspath(root, pp.get('soundXlsx') or LEGACY_PATHS['soundXlsx'])
        P.WORDDIC = PR.abspath(root, pp.get('wordDicDir') or LEGACY_PATHS['wordDicDir'])
        P.CONTENTS = PR.abspath(root, pp.get('contentsDir') or LEGACY_PATHS['contentsDir'])
        gd = pp.get('guideDir')
        P.GUIDE_DIR = PR.abspath(root, gd) if gd else None
        P.STORYBOARD_SHEETS = dict((pr.get('patterns') or {}).get('storyboardSheets') or {})
        P.GEN = os.path.join(root, '_딕테이션_생성기')
    else:
        P.ROOT = ''
        P.SB_DIR = P.SND = P.WORDDIC = P.CONTENTS = ''
        P.GUIDE_DIR = None
        P.STORYBOARD_SHEETS = {}
        P.UNITS = {}
    for key, attr in (('script_xlsx', 'SND'), ('storyboard_dir', 'SB_DIR'),
                      ('guide_dir', 'GUIDE_DIR'), ('contents_dir', 'CONTENTS')):
        v = ctx.get(key)
        if v:
            setattr(P, attr, v)
    try:                       # project_rules.json 에 적힌 단원을 read_paths 에 꽂는다
        import project_io
        lst = PR.units()
        if not lst:            # project_rules.json 이 아직 비어 있으면(root 없이 불렸을 때 등)
            lst = project_io.units(rid)
        _register(ctx, lst)
    except Exception:
        pass
    ctx.P = P


def fresh(unit):
    """data<N>.py 를 다시 읽는다.

    read_gen.load_lesson 은 import_module 로 불러오므로, 화면(서버)이 계속 떠 있으면
    [추출] 이 새로 쓴 data<N>.py 가 아니라 예전에 올라온 것을 계속 쓴다.
    그래서 쓰는 쪽에서 먼저 다시 읽어 준다.
    """
    import importlib
    m = 'data%d' % unit if isinstance(unit, int) else 'data%s' % unit
    if m in sys.modules:
        importlib.reload(sys.modules[m])


def check(ctx):
    """자료 경로가 말이 되는지 먼저 본다. 없는 곳에 조용히 만들어 쓰지 않도록."""
    import read_paths as P
    bad = []
    if not os.path.isfile(P.SND):
        bad.append('녹음 대본 엑셀: %s' % P.SND)
    if not os.path.isdir(P.SB_DIR):
        bad.append('스토리보드 폴더: %s' % P.SB_DIR)
    if not os.path.isdir(P.CONTENTS):
        bad.append('출력 폴더(contents): %s' % P.CONTENTS)
    if bad:
        raise RuntimeError('자료 경로를 찾을 수 없습니다 —\n  ' + '\n  '.join(bad)
                           + '\n[자료] 에서 경로를 정하고 저장하세요.')
    return ''


# ------------------------------------------------- 단원 찾기
# 단원 수·이름은 교재마다 다르다. 코드에 박지 않고 **사용자가 지정한 두 폴더 안에서만**
# 찾아 project.json 에 적어 둔다. 그 뒤로는 그 파일이 기준이고, 사람이 고칠 수 있다.
# 아래 두 정규식은 project_rules.json 의 patterns 에 없을 때 쓰는 기본값이다
# (지금까지 CJ 프로젝트에 써 온 값과 같다). discover() 안에서 패턴을 고를 때 쓴다.
_NUM_DEFAULT = r'Lesson\s*0*(\d+)\s*\.xlsx$'
_NAMED_DEFAULT = r'_([A-Za-z][A-Za-z ]*Lesson)\s*\.xlsx$'
_CONTENTS_DEFAULT = r'^lesson0*(\d+)$'
_SHEET_DEFAULT = '%d과' 


def _slug(name):
    return re.sub(r'[^a-z0-9]+', '_', name.strip().lower()).strip('_')


def discover(ctx):
    """스토리보드 폴더와 산출 폴더에서 단원을 찾는다. 다른 곳은 보지 않는다.

    project_rules.json 에 이미 적힌 단원 정보는 이 함수 결과로 절대 덮이지 않는다
    (units() 가 project_rules.json 을 먼저 채우고, 여기 결과는 빈 자리만 채우는
    보조로만 쓴다). 이름 규칙(정규식)도 project_rules.json 의 patterns 에 있으면
    그걸 쓰고, 없으면 지금까지 CJ 프로젝트에 써 온 기본값을 그대로 쓴다 — 그래서
    이 함수 자체는 '구조를 결정'하지 않고 '있는지 확인/보조'만 한다(진단·검증 용도).
    """
    import read_paths as P
    import project_rules_io as PR
    num_pat = re.compile(PR.pattern('storyboardFilename', _NUM_DEFAULT), re.I)
    named_pat = re.compile(PR.pattern('specialUnitFilename', _NAMED_DEFAULT), re.I)
    contents_pat = PR.pattern('contentsFolder', _CONTENTS_DEFAULT)
    sheet_tpl = PR.pattern('soundSheet', _SHEET_DEFAULT)
    found = {}
    if os.path.isdir(P.SB_DIR):
        for f in sorted(os.listdir(P.SB_DIR)):
            if f.startswith('~$') or not f.lower().endswith(('.xlsx', '.xlsm')):
                continue
            m = num_pat.search(f)
            if m:
                uid, name = str(int(m.group(1))), '%d단원' % int(m.group(1))
            else:
                m2 = named_pat.search(f)
                if not m2:
                    continue
                name = m2.group(1).strip()
                uid = _slug(name)
            e = found.setdefault(uid, {'id': uid, 'name': name})
            e['storyboard'] = os.path.join(P.SB_DIR, f)
            if uid.isdigit():
                e.setdefault('sheet', sheet_tpl % int(uid))   # 녹음 대본의 시트 이름
    if os.path.isdir(P.CONTENTS):
        for d in sorted(os.listdir(P.CONTENTS)):
            opsdir = os.path.join(P.CONTENTS, d, 'ops')
            if not os.path.isdir(opsdir):
                continue
            m = re.match(contents_pat, d, re.I)
            uid = str(int(m.group(1))) if m else _slug(d)
            e = found.setdefault(uid, {'id': uid, 'name': d})
            e['ops'] = opsdir
    return found


def _sortkey(u):
    i = u.get('id', '')
    return (0, int(i), '') if i.isdigit() else (1, 0, i)


def units(ctx):
    """고를 수 있는 단원. project_rules.json 을 기준으로 하되 새로 생긴 것은 더해 준다."""
    import project_rules_io as PR
    import read_paths as P
    root = P.ROOT
    have = {u['id']: u for u in PR.units()}
    for uid, e in discover(ctx).items():
        cur = have.setdefault(uid, {'id': uid, 'name': e.get('name', uid)})
        for k in ('storyboard', 'ops'):
            if e.get(k) and not cur.get(k):
                cur[k] = PR.relpath(root, e[k])
        if e.get('sheet') and not cur.get('sheet'):
            cur['sheet'] = e['sheet']
    lst = sorted(have.values(), key=_sortkey)
    if lst:
        PR.put_units(lst, name=os.path.basename(root))
    _register(ctx, lst)
    return [u['id'] for u in lst]


def _register(ctx, lst):
    """read_paths 에 단원 등록부를 꽂는다. 이게 있어야 숫자가 아닌 단원도 길을 찾는다."""
    import project_rules_io as PR
    import read_paths as P
    P.UNITS = {}
    for u in lst:
        P.UNITS[u['id']] = {
            'name': u.get('name', u['id']),
            'sheet': u.get('sheet', ''),
            'guide': PR.abspath(P.ROOT, u.get('guide', '')),
            'kr': u.get('kr', ''),          # 'guide' 면 해석을 각론에서 뽑는다
            'storyboard': PR.abspath(P.ROOT, u.get('storyboard', '')),
            'ops': PR.abspath(P.ROOT, u.get('ops', '')),
        }


def unit_labels(ctx):
    import project_rules_io as PR
    return {u['id']: u.get('name', u['id']) for u in PR.units()}


def out_dir(ctx, unit):
    import read_paths as P
    return P.ops(unit)


def outputs(ctx, unit):
    """이 레시피가 만드는 파일 (백업 대상). 상대 경로."""
    fresh(unit)
    import read_gen
    read_gen.load_lesson(unit, out_dir(ctx, unit))
    rel = []
    for page in read_gen.ORDER:
        rel += ['%s.html' % page, 'css/%s.css' % page, 'js/%s.js' % page,
                'popup/%s_kor1.html' % page]
    if read_gen.intro_page():
        rel.append('%s.html' % read_gen.intro_page())
    rel.append('popup/%s.html' % read_gen.all_popup())
    tp = read_gen.think_page()
    if tp:
        rel.append('popup/%s_think_ans1.html' % tp)
    return rel


# ---------------------------------------------------------------- 네 단계
def extract(ctx, unit):
    check(ctx)
    import read_import
    import read_paths as P
    read_import.load_rules(ctx.recipe.ID)   # 프로토에서 뽑아 둔 자료-읽기 규칙을 추출에 쓴다
    d = read_import.assemble(unit)
    # 각론에서 해석을 뽑는 단원 — 지면 구조를 입히기 전에 뽑아 둔다.
    # apply_layout 이 그림 라벨·출처를 문단 안으로 접어 넣으면 구분이 사라진다.
    gkr = None
    if P.unit(unit).get('kr') == 'guide':
        gkr = read_import.guide_stream(unit, d)
    lay = os.path.join(DATA, 'layout%s.json' % unit)
    if os.path.isfile(lay):
        read_import.apply_layout(d, lay)
        if d.get('_KR_IN_LAYOUT'):
            read_import.apply_kr(d, d['_KR_IN_LAYOUT'])
    if gkr is not None:
        # 손으로 넣어 둔 해석과 견주고, 다르면 여기서 멈춘다(덮어쓰지 않는다)
        read_import.apply_guide_kr(d, gkr, check=d.get('_KR_IN_LAYOUT'))
    d['READSMART'] = read_import.build_readsmart(unit, d['READSMART'])
    read_import.clear_joins(d)      # 줄 이음매 표시는 data<N>.py 로 넘기지 않는다
    text = read_import.render(unit, d)
    open(os.path.join(DATA, 'data%s.py' % unit), 'w',
         encoding='utf-8', newline='').write(text)
    fresh(unit)
    notes = list(read_import.WARN) + list(d['NOTES'])
    miss = read_import.missed_rules() if hasattr(read_import, 'missed_rules') else []
    if miss:
        notes.append('rules.json 에 없어 코드 기본값을 쓴 자료-읽기 규칙 %d개: %s'
                      % (len(miss), ', '.join(miss)))
    return ('확인할 것 %d건' % len(notes)) if notes else ''


def need_only(read_gen):
    """불려 온 read_gen 이 쪽 고르기를 아는지 본다.

    묵은 .pyc 를 물고 있으면 only 를 모르는 예전 build() 가 불려
    "unexpected keyword argument 'only'" 가 난다. 그때 어느 파일을 물고 있는지
    바로 알 수 있게, 조용한 TypeError 대신 여기서 밝혀 둔다.
    """
    import inspect
    if 'only' in inspect.signature(read_gen.build).parameters:
        return
    raise RuntimeError(
        '쪽 고르기를 모르는 예전 read_gen 이 불려 있습니다.\n'
        '  불려 온 파일 : %s\n'
        '  껍데기       : %s\n'
        '  본 모양      : build%s\n'
        '생성기를 끝내고 다시 여세요. 그래도 같으면 __pycache__ 를 지우세요.'
        % (getattr(read_gen, '__file__', '?'), getattr(read_gen, '__cached__', '?'),
           inspect.signature(read_gen.build)))


def build(ctx, unit):
    check(ctx)
    fresh(unit)
    import read_gen
    need_only(read_gen)
    read_gen.load_rules(ctx.recipe.ID)   # 프로토에서 뽑아 둔 규칙을 생성에 쓴다
    read_gen.build(unit, out=ctx.out_dir(unit), only=getattr(ctx, 'pages', None))
    # 규칙이 조용히 빠지지 않도록, 기본값으로 메운 것을 적어 둔다 (결과는 그대로)
    miss = read_gen.missed_rules() if hasattr(read_gen, 'missed_rules') else []
    if miss:
        return ('rules.json 에 없어 코드 기본값을 쓴 규칙 %d개\n' % len(miss)
                + '\n'.join('      - %s' % k for k in miss)
                + '\n      → [규칙 분석] 에서 그 규칙이 있는 견본 쪽을 함께 골라 분석하세요.')
    return ''


def pages(ctx, unit):
    """고를 수 있는 본문 쪽. 이미 뽑아 둔 data<N>.py 에서 온다."""
    import read_gen
    try:
        fresh(unit)
        read_gen.load_lesson(unit, out_dir(ctx, unit))
        return list(read_gen.ORDER)
    except Exception:
        return []


def measure(ctx, unit):
    import runner
    try:
        import read_measure
    except ImportError as e:
        raise runner.SkipStep('playwright 가 없습니다 (%s)' % e)
    # 잰 값은 **생성기 폴더**에 써야 한다. read_gen 이 scrolls<N> 을 모듈로 읽기 때문에
    # 산출 폴더에 쓰면 아무 데서도 읽히지 않는다.
    # 재는 곳은 언제나 실기 폴더(P.ops)라, 임시 폴더로 뽑을 때도 진짜 이미지·글꼴 위에서 잰다.
    _backup_measured(unit)
    read_measure.measure(unit, gen_dir=DATA)
    import importlib
    for m in ('scrolls%s' % unit, 'krlayout%s' % unit, 'popscroll%s' % unit):
        if m in sys.modules:
            importlib.reload(sys.modules[m])
    import read_gen
    need_only(read_gen)
    read_gen.build(unit, out=ctx.out_dir(unit),     # 잰 값을 넣어 다시
                   only=getattr(ctx, 'pages', None))
    return ''


def _backup_measured(unit):
    """잰 값 파일을 덮어쓰기 전에 남겨 둔다. 측정이 흔들리면 되돌릴 수 있게."""
    import shutil, time
    d = os.path.join(GEN, '_backup', 'measure')
    os.makedirs(d, exist_ok=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    for name in ('scrolls%s.py', 'krlayout%s.py', 'popscroll%s.py'):
        src = os.path.join(DATA, name % unit)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(d, (name % unit)[:-3] + '_' + stamp + '.py'))
    try:
        import runner
        runner.prune_files(d, runner.KEEP_BACKUPS)
    except Exception:
        pass


def verify(ctx, unit):
    import read_verify
    return read_verify.verify(unit, ctx.out_dir(unit))


# ------------------------------------------------- 프로토 (생성과 따로 도는 곳)
def proto_ops(ctx):
    """견본 페이지가 있는 폴더. 사용자가 고른 것만 본다.

    단원 등록부(project_rules.json 에서 올라온 P.UNITS)에서 바로 ops 경로를 찾는다.
    read_paths.ops() 의 'lesson%02d 폴더일 것이다' 식 폴백(단원 id 를 int 로 바꿔야
    함)을 타지 않는다 — 문자열 단원 id(UnitA 등)에서도 그대로 동작해야 하기 때문이다.
    """
    v = ctx.get('proto_ops')
    if v:
        return v
    n = proto_lesson(ctx)
    if not n:
        return ''
    import read_paths as P
    return P.unit(n).get('ops') or ''


def proto_lesson(ctx):
    """프로토로 고른 단원 id. 문자열 그대로 돌려준다 — 숫자 단원만 되던 제약을 없앤다.

    project_rules.json 의 prototype.units 에 적힌 id 만 고를 수 있다. 폴더를 다시
    뒤져 추측하지 않는다 — 거기 없으면(오타 포함) None 을 돌려준다.
    """
    v = str(ctx.get('proto_lesson') or '').strip()
    if not v:
        return None
    import project_rules_io as PR
    ids = {u.get('id') for u in PR.proto_units()}
    return v if v in ids else None


def proto_pages(ctx):
    """고를 수 있는 견본 쪽 목록 — project_rules.json 의 prototype.units[].pages 가 기준.

    폴더를 다시 훑어 후보를 임의로 늘리지 않는다(추측 금지). 폴더에 더 있어도
    여기 없으면 화면에 보여주지 않는다 — 등록된 페이지만 보여준다는 원칙을 지킨다.
    """
    import project_rules_io as PR
    n = proto_lesson(ctx)
    if not n:
        return []
    return PR.proto_pages(n)


def prototype_units(ctx):
    """화면 드롭다운에 보여줄 '프로토로 고를 수 있는 단원 id' 목록.

    project_rules.json 의 prototype.units 에 적힌 것만 — 폴더를 다시 뒤져 후보를
    추측해서 늘리지 않는다.
    """
    import project_rules_io as PR
    return [u['id'] for u in PR.proto_units() if u.get('id')]


def analyze(ctx, pages=None):
    """고른 견본 쪽만 읽어 proto_L<N>.json 을 만든다. 생성물은 건드리지 않는다."""
    import proto_scan, read_paths as P, project_rules_io as PR
    n = proto_lesson(ctx)
    if not n:
        raise RuntimeError('프로토 단원을 정해 주세요.')
    ops = proto_ops(ctx)
    if not os.path.isdir(ops):
        raise RuntimeError('프로토 ops 폴더가 없습니다: %s' % ops)
    sb = P.storyboard(n) if os.path.isfile(P.storyboard(n)) else None
    snd = P.SND if os.path.isfile(P.SND) else None
    pat = PR.pattern('pageFilename', proto_scan.PAGE_PATTERN_DEFAULT)
    # 음원 시트 이름 — 이 단원에 project_rules.json 이 적어 둔 값이 최우선(예전과 같은
    # 우선순위, read_import.sound() 와 동일), 없으면 rules.json 의 sound.sheet.
    # proto_scan.py 는 이제 이 값을 그대로 받아 쓰고, '%d과' 를 스스로 만들지 않는다.
    sheet = P.unit(n).get('sheet') or ''
    if not sheet:
        import read_import
        read_import.load_rules(ctx.recipe.ID)
        sheet = read_import.R('sound.sheet', None)
        if sheet and '%' in str(sheet) and str(n).isdigit():
            sheet = sheet % int(n)
        elif sheet and '%' in str(sheet):
            sheet = None       # 단원 id 가 숫자가 아니면 '%d' 템플릿을 적용할 수 없다
    return proto_scan.scan(ctx.recipe.ID, n, ops, pages, sound_xlsx=snd, sb_xlsx=sb,
                            page_pattern=pat, sound_sheet=sheet or None)


def preview(ctx, unit):
    """미리보기에 보일 파일 — 고른 쪽 / 단원 공통 / 그 밖. 상대 경로로 돌려준다.

    읽기만 한다. 산출물을 만들지도 고치지도 않는다.
    팝업을 어느 쪽에 딸린 것으로 볼지는 **새로 정하지 않는다** —
    layout_edit.page_files(쪽별) 와 common_files(단원 공통) 가 이미 쓰는
    이름 규칙을 그대로 쓴다. 그래서 이 생성기가 만들지 않는 파일
    (딕테이션 팝업 _dic1 등) 은 저절로 '그 밖' 으로 간다.

    옛 모양(절대 경로 목록)을 바라는 곳을 위해, 못 가릴 때는
    예전처럼 폴더 전체를 '그 밖' 에 담아 돌려준다.
    """
    import layout_edit
    d = ctx.out_dir(unit)
    rel = lambda q: os.path.relpath(q, d).replace('\\', '/')
    allhtml = ([rel(q) for q in sorted(glob.glob(os.path.join(d, 'p*.html')))]
               + [rel(q) for q in sorted(glob.glob(os.path.join(d, 'popup', '*.html')))])
    have = set(allhtml)
    try:
        dmod = layout_edit.data_mod(unit)
        order = list(getattr(dmod, 'ORDER', []) or [])
        if not order:
            raise RuntimeError('ORDER 를 찾지 못했습니다')
        want = list(getattr(ctx, 'pages', None) or order)
        picked = []
        for pg in order:                      # 차례는 늘 ORDER 를 따른다
            if pg not in want:
                continue
            for r in layout_edit.page_files(ctx.recipe, ctx, unit, [pg]):
                if r.endswith('.html') and r in have and r not in picked:
                    picked.append(r)
        common = [r for r in layout_edit.common_files(ctx.recipe, ctx, unit)
                  if r.endswith('.html') and r in have and r not in picked]
        other = [r for r in allhtml if r not in picked and r not in common]
        return {'picked': picked, 'common': common, 'other': other}
    except Exception:
        return {'picked': [], 'common': [], 'other': allhtml}
