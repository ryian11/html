# -*- coding: utf-8 -*-
"""project.json — 이 프로젝트에 어떤 단원이 있는지 적어 두는 곳.

단원 수와 이름은 교재마다 다르다(1~5단원, 1~8단원 + Special Lesson, …).
그래서 코드에 박지 않고, **사용자가 지정한 폴더 안에서만** 찾아 여기 적어 둔다.
한 번 적힌 뒤로는 이 파일이 기준이다 — 사람이 고칠 수 있다.

  {"cj_reading": {"units": [
      {"id": "7",       "name": "7단원",        "storyboard": "…/Lesson 7.xlsx", "ops": "…/lesson07/ops"},
      {"id": "special", "name": "Special Lesson", …}
  ]}}

경로는 프로젝트 폴더(root) 기준 상대 경로로 적는다. 다른 PC 로 옮겨도 그대로 쓴다.
"""
import io, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'project.json')


def load_all():
    if os.path.isfile(PATH):
        try:
            return json.loads(io.open(PATH, encoding='utf-8').read())
        except Exception:
            return {}
    return {}


def save_all(d):
    io.open(PATH, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(d, ensure_ascii=False, indent=1))
    return PATH


def units(rid):
    """적혀 있는 단원 목록. 없으면 빈 목록."""
    return (load_all().get(rid) or {}).get('units') or []


def put_units(rid, lst, name=''):
    d = load_all()
    cur = d.get(rid) or {}
    cur['units'] = lst
    if name:
        cur['name'] = name
    d[rid] = cur
    return save_all(d)


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
