# -*- coding: utf-8 -*-
"""project_rules.json — 프로젝트마다 달라지는 '구조·경로·단원' 정보를 한 곳에 모은다.

project.json 이 단원 목록만 적어 두던 것을, 여기서는
  · 프로젝트 이름/루트
  · 자료 폴더 경로(스토리보드/음원/각론/출력)
  · 단원을 찾을 때 쓰는 이름 규칙(패턴) — Lesson N.xlsx 같은 CJ 관례
  · 단원 목록(경로 포함)
  · 프로토타입(견본 단원) 정보
까지 함께 적어 둔다. 생성기는 이 파일을 프로젝트 구조의 기준으로 삼는다.

이 프로젝트에만 있는 값(폴더명·파일명·정규식)은 여기 JSON 에만 있고,
Python 코드에는 "JSON 에 없으면 쓸 안전한 기본값"으로만 남는다. 그 기본값은
지금(2026 CJ 중3) 프로젝트의 실제 값과 같아서, 이 파일이 아직 없는 상태에서도
지금까지와 똑같이 동작한다 — 처음 실행될 때 이 파일을 자동으로 한 번
만들어 둔다(마이그레이션, ensure_migrated 참고).

`GEN`(생성기 자기 설치 위치)은 여기 넣지 않는다 — 프로젝트 자료가 아니라
생성기 프로그램 자신이 어디 깔려 있는지이기 때문이다(지금처럼 코드에서 계산).

  {"schema": 1,
   "project": {"name": "...", "root": "...", "recipe": "cj_reading"},
   "paths": {"storyboardDir": "...", "soundXlsx": "...", "wordDicDir": "...",
             "contentsDir": "...", "guideDir": null},
   "patterns": {"storyboardFilename": "...", "specialUnitFilename": "...",
                "contentsFolder": "...", "pageFilename": "...",
                "guidePdf": "...", "soundSheet": "..."},
   "units": [{"id": "1", "name": "1단원", "storyboard": "...", "ops": "...", "sheet": "1과"}, ...],
   "prototype": {"lesson": "3", "analyzedPages": [...], "rulesFile": "rules/cj_reading/rules.json"}}

경로는 project.json 과 같은 관례로, 프로젝트 폴더(root) 기준 상대 경로로 적는다.
"""
import io, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'project_rules.json')

SCHEMA = 1


def load():
    """project_rules.json 을 읽는다. 없으면 None."""
    if not os.path.isfile(PATH):
        return None
    try:
        return json.loads(io.open(PATH, encoding='utf-8').read())
    except Exception:
        return None


def save(d):
    d['schema'] = SCHEMA
    io.open(PATH, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(d, ensure_ascii=False, indent=1, sort_keys=False))
    return PATH


def exists():
    return os.path.isfile(PATH)


def blank():
    return {'schema': SCHEMA, 'project': {}, 'paths': {}, 'patterns': {},
            'units': [], 'prototype': {}}


def abspath(root, rel):
    if not rel:
        return ''
    return rel if os.path.isabs(rel) else os.path.normpath(os.path.join(root, rel))


def relpath(root, path):
    try:
        r = os.path.relpath(path, root)
        return path if r.startswith('..') else r.replace(os.sep, '/')
    except Exception:
        return path


def units():
    d = load()
    return (d or {}).get('units') or []


def put_units(lst, name=''):
    d = load()
    if d is None and exists():
        # 방금 막 쓴 파일이 마운트 지연으로 아직 안 읽힐 때가 드물게 있다 — 한 번 더 읽어
        # 본다. 그냥 blank() 로 넘어가면 이미 있던 paths/patterns 을 지워 버리게 된다.
        import time
        time.sleep(0.3)
        d = load()
    d = d or blank()
    d['units'] = lst
    if name:
        d.setdefault('project', {})['name'] = name
    return save(d)


def paths():
    d = load()
    return (d or {}).get('paths') or {}


def patterns():
    d = load()
    return (d or {}).get('patterns') or {}


def path(key, default=''):
    v = paths().get(key)
    return v if v else default


def pattern(key, default=''):
    v = patterns().get(key)
    return v if v else default


def prototype():
    d = load()
    return (d or {}).get('prototype') or {}


def proto_units():
    """prototype.units — Claude 가 분석에서 '이 단원을 견본으로 쓴다'고 확인해 둔 목록.

    project_rules.json 에 없으면 빈 목록을 돌려준다. 이 함수는 폴더를 뒤지지 않는다 —
    project_rules.json 에 적힌 것만 본다(추측 금지). 화면의 프로토 드롭다운과
    recipes/cj_reading.py 의 proto_lesson()/proto_pages() 가 이 값을 기준으로 삼는다.
    """
    return prototype().get('units') or []


def proto_pages(unit_id):
    """그 단원 id 의 프로토 견본 페이지 목록. 등록돼 있지 않으면 빈 목록.

    폴더에 실제로 더 있는 페이지가 있어도 여기 없으면 돌려주지 않는다 — 화면에는
    project_rules.json 에 적힌 페이지만 보여준다는 원칙을 이 함수에서 지킨다.
    """
    for u in proto_units():
        if u.get('id') == unit_id:
            return list(u.get('pages') or [])
    return []


# ---------------------------------------------------------------- 마이그레이션
def ensure_migrated(recipe_id, root, defaults):
    """project_rules.json 이 없으면, 지금 쓰던 값(project.json + 코드 기본값)으로 한 번 만든다.

    defaults 는 {'paths': {...}, 'patterns': {...}} — 지금까지 코드에 박혀 있던 값을
    부르는 쪽(recipes/<레시피>.py)에서 그대로 건네준다. 이 함수는 그 값을 그대로
    옮겨 적을 뿐, 새로 추측하지 않는다. project.json 은 지우지 않고 그대로 둔다.

    돌려주는 값: (project_rules.json 내용, 이번에 새로 만들었는가)
    """
    if exists():
        return load(), False
    import project_io
    old = project_io.load_all().get(recipe_id) or {}
    d = blank()
    d['project'] = {'name': old.get('name') or os.path.basename(root), 'root': root,
                     'recipe': recipe_id}
    d['paths'] = dict(defaults.get('paths') or {})
    d['patterns'] = dict(defaults.get('patterns') or {})
    d['units'] = old.get('units') or []
    d['prototype'] = {}
    save(d)
    return d, True
