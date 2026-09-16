# -*- coding: utf-8 -*-
"""지면 구조 파일(layout<N>) 읽고 쓰기.

  · layout<N>.json  — UI 가 편집하는 본체 (권장)
  · layout<N>.py    — 예전 형식. 그대로 읽힌다.

JSON 은 열쇠에 튜플을 못 쓰므로 `"쪽/뒷번호"` 한 줄짜리 문자열로 적는다.
  ("123", "01")  ↔  "123/01"
"""
import io, json, os


class Layout(object):
    """읽어 들인 지면 구조. 예전 모듈과 같은 이름의 속성을 가진다."""
    __slots__ = ('PARAS', 'LABELS', 'DROP', 'PREFIX', 'SPEAKER',
                 'TEXT', 'CSS', 'IMG', 'KR', 'path')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))
        self.PARAS = self.PARAS or {}
        self.LABELS = self.LABELS or {}
        self.DROP = self.DROP or set()
        self.PREFIX = self.PREFIX or {}
        self.SPEAKER = self.SPEAKER or ''
        self.TEXT = self.TEXT or {}
        self.CSS = self.CSS or {}
        self.IMG = self.IMG or {}
        self.KR = self.KR or {}


def _k(s):
    """'123/01' → ('123', '01')"""
    a, b = s.split('/', 1)
    return (a, b)


def _s(t):
    """('123', '01') → '123/01'"""
    return '%s/%s' % (t[0], t[1])


def load(path):
    """layout<N>.json 또는 layout<N>.py 를 읽는다."""
    if path.lower().endswith('.json'):
        return _load_json(path)
    return _load_py(path)


def _load_json(path):
    d = json.loads(io.open(path, encoding='utf-8').read())
    return Layout(
        path=path,
        PARAS=d.get('paras') or {},
        LABELS={_k(k): v for k, v in (d.get('labels') or {}).items()},
        DROP=set(_k(k) for k in (d.get('drop') or [])),
        PREFIX={_k(k): v for k, v in (d.get('prefix') or {}).items()},
        SPEAKER=d.get('speaker') or '',
        TEXT={_k(k): v for k, v in (d.get('text') or {}).items()},
        CSS=d.get('css') or {},
        IMG={p: {k: tuple(v) for k, v in im.items()}
             for p, im in (d.get('img') or {}).items()},
        KR={_k(k): v for k, v in (d.get('kr') or {}).items()},
    )


def _load_py(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location('_lay', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return Layout(
        path=path,
        PARAS=getattr(m, 'PARAS', {}),
        LABELS=getattr(m, 'LABELS', {}),
        DROP=getattr(m, 'DROP', set()),
        PREFIX=getattr(m, 'PREFIX', {}),
        SPEAKER=getattr(m, 'SPEAKER', ''),
        TEXT=getattr(m, 'TEXT', {}),
        CSS=getattr(m, 'CSS', {}),
        IMG=getattr(m, 'IMG', {}),
        KR=getattr(m, 'KR', {}),
    )


def load_kr(path):
    """해석만 든 파일(kr<N>_해석.py / .json) → {(쪽, 뒷번호): 해석}"""
    if path.lower().endswith('.json'):
        d = json.loads(io.open(path, encoding='utf-8').read())
        d = d.get('kr', d)
        return {_k(k): v for k, v in d.items()}
    import importlib.util
    spec = importlib.util.spec_from_file_location('_kr', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return getattr(m, 'KR', {})


def save(lay, path, lesson=None):
    """Layout → JSON 파일. UI 가 고친 값을 되돌려 쓸 때 쓴다."""
    d = {}
    if lesson is not None:
        d['lesson'] = lesson
    d['paras'] = lay.PARAS
    if lay.labels_any():
        d['labels'] = {_s(k): v for k, v in lay.LABELS.items()}
    if lay.DROP:
        d['drop'] = sorted(_s(k) for k in lay.DROP)
    if lay.PREFIX:
        d['prefix'] = {_s(k): v for k, v in sorted(lay.PREFIX.items())}
    if lay.SPEAKER:
        d['speaker'] = lay.SPEAKER
    if lay.TEXT:
        d['text'] = {_s(k): v for k, v in sorted(lay.TEXT.items())}
    if lay.CSS:
        d['css'] = lay.CSS
    if lay.IMG:
        d['img'] = {p: {k: list(v) for k, v in im.items()} for p, im in lay.IMG.items()}
    if lay.KR:
        d['kr'] = {_s(k): v for k, v in sorted(lay.KR.items())}
    txt = json.dumps(d, ensure_ascii=False, indent=1)
    txt = _compact(txt)
    os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(txt)
    return path


def _compact(txt):
    """문자열·숫자만 든 배열은 한 줄로 붙여 사람이 읽기 쉽게 한다."""
    import re
    pat = re.compile(r'\[\s*\n\s*((?:(?:"(?:[^"\\]|\\.)*"|-?\d+)\s*,?\s*\n?\s*)+)\]')
    def one(m):
        items = re.findall(r'"(?:[^"\\]|\\.)*"|-?\d+', m.group(1))
        return '[' + ', '.join(items) + ']'
    prev = None
    while prev != txt:
        prev = txt
        txt = pat.sub(one, txt)
    return txt


Layout.labels_any = lambda self: bool(self.LABELS)
