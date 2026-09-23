# -*- coding: utf-8 -*-
"""프로젝트 경로. 다른 PC로 옮기면 ROOT 만 고치면 된다."""
import os, re

ROOT = r'E:\00_works\2026\2026_cj_midd3_eng'

# 컨테이너(리눅스)에서 돌릴 때를 위한 대체 경로
if not os.path.isdir(ROOT):
    for alt in ('/mnt/user-data/uploads/2026_cj_midd3_eng',
                os.path.expanduser('~/mnt/2026_cj_midd3_eng')):
        if os.path.isdir(alt):
            ROOT = alt
            break

SB_DIR = os.path.join(ROOT, '01_스토리보드', '전자저작물 추가 원고_20260716_아이스캔디 전달')
SB_NAME = '3학년 전자저작물_지시문_딕테이션_미니 단어장_구문 해설_Lesson %d.xlsx'
SND = os.path.join(ROOT, '02_사운드', '중3(소영순) 전자저작물 녹음 대본_최종_20260806 아이스캔디 전달.xlsx')
WORDDIC = os.path.join(ROOT, '02_사운드', '단어사전', 'lesson%02d')
CONTENTS = os.path.join(ROOT, '00_개발물', 'EBOOK', '중학교 영어 3_소영순',
                        'app', 'resource', 'contents')
GEN = os.path.join(ROOT, '_딕테이션_생성기')


# 단원 등록부 — 레시피가 project_rules.json 을 읽어 채운다.
# 비어 있으면 아래 기본 규칙(Lesson <숫자> / lesson<두자리>)을 그대로 쓴다.
UNITS = {}

# 스토리보드 시트 이름 3종(구문 해설/미니 단어장/Dictation) — project_rules.json 의
# patterns.storyboardSheets 를 레시피가 읽어 꽂는다. 비어 있으면 각 read_*.py 가
# 자기 기본값을 쓴다(지금까지의 CJ 값과 같다).
STORYBOARD_SHEETS = {}


def pgkey(v):
    """쪽 번호를 견주기용 하나로 고른다 — '014' 도 '14' 도 '14'.

    쪽 이름은 세 자리로 채워 쓰고(p014_02) 원고 시트에는 두 자리로 적힌 곳이 있다.
    (1~5단원 '구문 해설' 은 14·32·50·68·86, 6~8단원은 104·122·140)
    둘을 견줄 때는 반드시 이 함수를 거쳐 앞자리 0 을 떼고 본다.
    """
    m = re.search(r'\d+', str(v or ''))
    s = m.group(0) if m else str(v or '').strip()
    return s.lstrip('0') or s


def unit(n):
    return UNITS.get(str(n)) or {}


def _need_numeric(n, what):
    """등록 안 된 단원은 폴더명을 숫자로 추측해서 짓는다 — 그 마지막 방어선.

    단원 id 가 숫자가 아니면(예: 처음 보는 문자 단원) 추측 자체가 말이 안 되므로,
    알 수 없는 ValueError 대신 무엇을 등록해야 하는지 바로 알려 준다.
    """
    try:
        return int(n)
    except (TypeError, ValueError):
        raise SystemExit(
            '등록되지 않은 단원입니다: %r — project_rules.json 의 units 에 %s 경로를 '
            '먼저 등록하세요(숫자가 아닌 단원 id 는 폴더명을 추측할 수 없습니다).'
            % (n, what))


def storyboard(n):
    u = unit(n).get('storyboard')
    if u:
        return u
    return os.path.join(SB_DIR, SB_NAME % _need_numeric(n, 'storyboard'))


def ops(n):
    u = unit(n).get('ops')
    if u:
        return u
    return os.path.join(CONTENTS, 'lesson%02d' % _need_numeric(n, 'ops'))


def file_url(path):
    """file:/// URL (한글·공백 인코딩). 윈도우 드라이브 문자 경로도 그대로 받는다."""
    import re
    from urllib.parse import quote
    p = path.replace('\\', '/')
    if not (p.startswith('/') or re.match(r'^[A-Za-z]:/', p)):
        p = os.path.abspath(path).replace('\\', '/')
    if not p.startswith('/'):
        p = '/' + p
    return 'file://' + quote(p, safe='/:')


GUIDE_DIR = None        # 레시피가 지정하면 그 폴더만 본다


GUIDE_PDF_PATTERN_DEFAULT = '*각론%d*.pdf'


def guide_pdf(n):
    """지도서 각론<N> PDF. 없으면 None. GUIDE_DIR 이 있으면 거기만 본다.

    파일명 규칙은 project_rules.json 의 patterns.guidePdf 를 따른다(없으면
    지금까지 CJ 프로젝트에 써 온 기본값). 여기서 CJ 전용 모양을 그대로
    쓰지 않는다 — 다른 교재는 각론 PDF 이름이 다를 수 있다.
    """
    import glob
    g = unit(n).get('guide')            # 단원 등록부가 콕 집어 준 파일
    if g and os.path.isfile(g):
        return g
    import project_rules_io as PR
    try:
        pat = PR.pattern('guidePdf', GUIDE_PDF_PATTERN_DEFAULT)
    except RuntimeError:                # set_root() 전이면(프로젝트 미선택) 기본값
        pat = GUIDE_PDF_PATTERN_DEFAULT
    try:                        # 패턴은 단원 번호(숫자)를 전제한다 — 문자 단원은 못 짓는다
        needle = pat % int(n)
    except (TypeError, ValueError):
        return None              # 여기까지 왔으면(등록부에도 없으면) 추측할 수 없다
    if GUIDE_DIR:
        g = sorted(glob.glob(os.path.join(GUIDE_DIR, needle)))
        return g[0] if g else None
    for base in (os.path.join(ROOT, '03_PDF'), ROOT):
        g = sorted(glob.glob(os.path.join(base, '**', needle), recursive=True))
        if g:
            return g[0]
    return None
