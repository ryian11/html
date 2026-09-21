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


# 단원 등록부 — 레시피가 project.json 을 읽어 채운다.
# 비어 있으면 아래 기본 규칙(Lesson <숫자> / lesson<두자리>)을 그대로 쓴다.
UNITS = {}


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


def storyboard(n):
    u = unit(n).get('storyboard')
    if u:
        return u
    return os.path.join(SB_DIR, SB_NAME % int(n))


def ops(n):
    u = unit(n).get('ops')
    if u:
        return u
    return os.path.join(CONTENTS, 'lesson%02d' % int(n), 'ops')


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


def guide_pdf(n):
    """지도서 각론<N> PDF. 없으면 None. GUIDE_DIR 이 있으면 거기만 본다."""
    import glob
    g = unit(n).get('guide')            # 단원 등록부가 콕 집어 준 파일
    if g and os.path.isfile(g):
        return g
    if GUIDE_DIR:
        g = sorted(glob.glob(os.path.join(GUIDE_DIR, '*각론%d*.pdf' % n)))
        return g[0] if g else None
    for pat in (os.path.join(ROOT, '03_PDF', '**', '*각론%d*.pdf' % n),
                os.path.join(ROOT, '**', '*각론%d*.pdf' % n)):
        g = sorted(glob.glob(pat, recursive=True))
        if g:
            return g[0]
    return None
