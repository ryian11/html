# -*- coding: utf-8 -*-
"""CJ 중3 영어(소영순) — Reading 본문 페이지.

검증된 기존 스크립트를 부르기만 한다. 그 안은 이 파일이 모른다.
  read_import.py → data<N>.py        ① 추출
  read_gen.py    → ops/*.html …      ② 생성
  read_measure.py→ scrolls/krlayout  ③ 측정
  read_verify.py                     ④ 검증
"""
import os, sys, glob

GEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if GEN not in sys.path:
    sys.path.insert(0, GEN)

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


def setup(ctx):
    """슬롯에 적힌 경로를 기존 read_paths 에 꽂는다. 없으면 root 기준 기본값."""
    import read_paths as P
    root = ctx.get('root')
    if root and os.path.isdir(root):
        P.ROOT = root
        P.SB_DIR = os.path.join(root, '01_스토리보드',
                                '전자저작물 추가 원고_20260716_아이스캔디 전달')
        P.SND = os.path.join(root, '02_사운드',
                             '중3(소영순) 전자저작물 녹음 대본_최종_20260806 아이스캔디 전달.xlsx')
        P.WORDDIC = os.path.join(root, '02_사운드', '단어사전', 'lesson%02d')
        P.CONTENTS = os.path.join(root, '00_개발물', 'EBOOK', '중학교 영어 3_소영순',
                                  'app', 'resource', 'contents')
        P.GEN = os.path.join(root, '_딕테이션_생성기')
    for key, attr in (('script_xlsx', 'SND'), ('storyboard_dir', 'SB_DIR'),
                      ('guide_dir', 'GUIDE_DIR'), ('contents_dir', 'CONTENTS')):
        v = ctx.get(key)
        if v:
            setattr(P, attr, v)
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


def units(ctx):
    import read_paths as P
    out = []
    for n in range(1, 13):
        if os.path.isfile(P.storyboard(n)):
            out.append(n)
    return out or list(range(1, 9))


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
    d = read_import.assemble(unit)
    lay = os.path.join(GEN, 'layout%d.json' % unit)
    if os.path.isfile(lay):
        read_import.apply_layout(d, lay)
        if d.get('_KR_IN_LAYOUT'):
            read_import.apply_kr(d, d['_KR_IN_LAYOUT'])
    d['READSMART'] = read_import.build_readsmart(unit, d['READSMART'])
    text = read_import.render(unit, d)
    open(os.path.join(GEN, 'data%d.py' % unit), 'w',
         encoding='utf-8', newline='').write(text)
    fresh(unit)
    notes = list(read_import.WARN) + list(d['NOTES'])
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
    read_gen.build(unit, out=ctx.out_dir(unit), only=getattr(ctx, 'pages', None))
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
    read_measure.measure(unit, gen_dir=GEN)
    import importlib
    for m in ('scrolls%d' % unit, 'krlayout%d' % unit, 'popscroll%d' % unit):
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
    for name in ('scrolls%d.py', 'krlayout%d.py', 'popscroll%d.py'):
        src = os.path.join(GEN, name % unit)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(d, (name % unit)[:-3] + '_' + stamp + '.py'))


def verify(ctx, unit):
    import read_verify
    return read_verify.verify(unit, ctx.out_dir(unit))


# ------------------------------------------------- 프로토 (생성과 따로 도는 곳)
def proto_ops(ctx):
    """견본 페이지가 있는 폴더. 사용자가 고른 것만 본다."""
    v = ctx.get('proto_ops')
    if v:
        return v
    n = proto_lesson(ctx)
    return out_dir(ctx, n) if n else ''


def proto_lesson(ctx):
    v = str(ctx.get('proto_lesson') or '').strip()
    return int(v) if v.isdigit() else None


def proto_pages(ctx):
    """고를 수 있는 견본 쪽 목록."""
    import proto_scan
    return proto_scan.pages_in(proto_ops(ctx))


def analyze(ctx, pages=None):
    """고른 견본 쪽만 읽어 proto_L<N>.json 을 만든다. 생성물은 건드리지 않는다."""
    import proto_scan, read_paths as P
    n = proto_lesson(ctx)
    if not n:
        raise RuntimeError('프로토 단원을 정해 주세요.')
    ops = proto_ops(ctx)
    if not os.path.isdir(ops):
        raise RuntimeError('프로토 ops 폴더가 없습니다: %s' % ops)
    sb = P.storyboard(n) if os.path.isfile(P.storyboard(n)) else None
    snd = P.SND if os.path.isfile(P.SND) else None
    return proto_scan.scan(ctx.recipe.ID, n, ops, pages, sound_xlsx=snd, sb_xlsx=sb)


def preview(ctx, unit):
    d = ctx.out_dir(unit)
    return sorted(glob.glob(os.path.join(d, 'p*.html'))) + \
           sorted(glob.glob(os.path.join(d, 'popup', '*.html')))
