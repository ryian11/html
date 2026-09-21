# -*- coding: utf-8 -*-
"""규칙 파일 살림 — 프로토 분석 결과와 확정 규칙을 다룬다.

  rules/<레시피>/proto_L6.json   프로토 분석 결과.  기계가 쓴다. 사람이 고치지 않는다.
  rules/<레시피>/rules.json      확정된 생성 규칙.  사람이 승격시킨 것만 들어간다.

이 단계에서 rules.json 은 **생성에 쓰이지 않는다**. 코드와 견주어 보여 줄 뿐이다.
항목을 하나씩 확인하고 옮기는 것은 다음 단계 일이다.

규칙은 점 찍힌 이름표 하나에 값 하나로 납작하게 둔다. 항목별로 승격·대조하기 쉽다.

  {"schema":1, "kind":"proto"|"rules", "recipe":"cj_reading",
   "proto":{"lesson":6,"pages":[...]},
   "items":{"popup.video":{"value":1,"source":"html","note":"videoPopBtn"}, ...}}
"""
import io, os, re, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'rules')

# 이 단계에서 뽑는 항목. 여기 없는 것은 일부러 코드에 남긴다.
GROUPS = [
    ('popup',      '팝업 번호'),
    ('skeleton',   '페이지 뼈대'),
    ('assets',     '파일 이름 틀'),
    ('sound',      '음원·시트 읽기'),
    ('storyboard', '스토리보드 시트'),
    ('measure',    '측정 여백'),
]


def dir_of(rid):
    return os.path.join(ROOT, rid)


def proto_path(rid, lesson):
    return os.path.join(dir_of(rid), 'proto_L%s.json' % lesson)


def rules_path(rid):
    return os.path.join(dir_of(rid), 'rules.json')


def blank(rid, kind):
    return {'schema': 1, 'kind': kind, 'recipe': rid,
            'made': time.strftime('%Y-%m-%d %H:%M'), 'items': {}}


def load(path):
    if not os.path.isfile(path):
        return None
    return json.loads(io.open(path, encoding='utf-8').read())


def save(d, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d['made'] = time.strftime('%Y-%m-%d %H:%M')
    io.open(path, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True))
    return path


def put(d, key, value, source, note=''):
    """항목 하나 적기. source 는 어디서 봤는지 — html / css / xlsx / code."""
    d['items'][key] = {'value': value, 'source': source}
    if note:
        d['items'][key]['note'] = note


def list_protos(rid):
    p = dir_of(rid)
    if not os.path.isdir(p):
        return []
    out = []
    for f in sorted(os.listdir(p)):
        m = re.match(r'^proto_L(.+)\.json$', f)
        if m:
            out.append(m.group(1))
    return out


# ---------------------------------------------------------------- 승격
def promote(rid, lesson, keys=None, fresh=False):
    """프로토 분석 결과를 rules.json 에 **합친다**.

    key 를 기준으로 합친다 — 이번 분석에 없는 예전 규칙은 지우지 않는다.
      예전 A B C D E  +  이번 A B C   →   A B C D E   (A B C 는 새 값으로 갱신)
    이렇게 하지 않으면 견본 쪽을 몇 장만 골라 분석했을 때
    그 쪽에 안 나오는 규칙이 통째로 사라진다.

    keys 가 없으면 이번 분석 결과 전부. 같은 key 는 새 값으로 갱신하고
    예전 값을 was 로 남긴다. 항목마다 어느 단원에서 왔는지 fromLesson 에 적는다.
    fresh=True 면 예전 것을 버리고 이번 결과만 남긴다 (명령줄 --fresh 전용).
    """
    proto = load(proto_path(rid, lesson))
    if not proto:
        raise RuntimeError('프로토 분석 결과가 없습니다 — 먼저 [프로토 분석] 하세요.')
    cur = blank(rid, 'rules') if fresh else (load(rules_path(rid)) or blank(rid, 'rules'))
    before = set(cur['items'])
    cur['from'] = {'lesson': lesson, 'pages': (proto.get('proto') or {}).get('pages', [])}
    moved, same = [], []
    for k, v in sorted(proto['items'].items()):
        if keys and k not in keys:
            continue
        old = cur['items'].get(k)
        nv = dict(v)
        nv['fromLesson'] = str(lesson)
        if old and old.get('value') == v.get('value'):
            cur['items'][k] = nv          # 값은 같고 출처만 새로 적는다
            same.append(k)
            continue
        if old:
            nv['was'] = old.get('value')
        cur['items'][k] = nv
        moved.append(k)
    kept = sorted(before - set(proto['items']))   # 이번 분석에 없어서 그대로 둔 예전 규칙
    save(cur, rules_path(rid))
    return {'moved': moved, 'same': same, 'kept': kept, 'path': rules_path(rid)}


# ---------------------------------------------------------------- 코드 쪽 값
def _src(name):
    p = os.path.join(HERE, name)
    return io.open(p, encoding='utf-8').read() if os.path.isfile(p) else ''


def _baseline(rid):
    """회귀 검사 기준본 — 지금 생성기가 실제로 뽑아 놓은 페이지. 읽기만 한다."""
    base = os.path.join(HERE, '_기준본', rid)
    if not os.path.isdir(base):
        return None, None
    for unit in sorted(os.listdir(base), key=lambda x: (len(x), x)):
        d = os.path.join(base, unit)
        if os.path.isdir(d) and any(f.endswith('.html') for f in os.listdir(d)):
            return d, unit
    return None, None


def code_rules(rid='cj_reading'):
    """지금 생성 로직이 실제로 내놓는 값 — 읽기만 한다. 대조의 한쪽 편이다.

    뼈대·팝업·이름 틀은 소스를 뜯지 않고 **생성기가 뽑아 놓은 기준본 페이지**를
    프로토와 똑같은 잣대로 읽는다. 그래야 견주는 두 쪽이 같은 자로 잰 값이 된다.
    자료를 읽는 규칙(시트·ID·여백)은 HTML 에 안 나오므로 소스에서 집어 온다.
    """
    d = blank(rid, 'code')
    gen, imp, mea = _src('read_gen.py'), _src('read_import.py'), _src('read_measure.py')

    # --- 산출물에서: 뼈대 · 팝업 · 이름 틀
    base, unit = _baseline(rid)
    if base:
        import proto_scan
        got = proto_scan.scan(rid, unit, base, [], write=False)
        for k, v in got['items'].items():
            if k.split('.')[0] in ('skeleton', 'popup', 'assets', 'info'):
                nv = dict(v)
                nv['source'] = 'gen'
                nv['note'] = '기준본 %s단원' % unit
                d['items'][k] = nv
        d['from'] = {'baseline': unit}
    else:
        put(d, 'skeleton', None, 'none', '기준본이 없습니다 — regress.py save 하세요')

    # --- 소스에서: 마지막 쪽 예외
    m = re.search(r'popidx = (\d+) if page == ORDER\[-1\] else (\d+)', gen)
    if m:
        put(d, 'popup.quiz.last', int(m.group(1)), 'code')
        put(d, 'popup.quiz.other', int(m.group(2)), 'code')

    # --- 소스에서: 음원·시트
    m = re.search(r"IDPAT = re\.compile\(r'([^']+)'\)", imp)
    if m:
        put(d, 'sound.idPattern', m.group(1), 'code')
    if re.search(r"replace\('-', '_'\).*?\.lower\(\)", imp, re.S):
        put(d, 'sound.mp3', {'sep': '_', 'case': 'lower'}, 'code')
    m = re.search(r"sheet = '(%d과)'", imp)
    if m:
        put(d, 'sound.sheet', m.group(1), 'code')
    m = re.search(r"fid, txt = str\(r\[(\d+)\].*?norm\(r\[(\d+)\]\)", imp)
    if m:
        put(d, 'sound.col.id', int(m.group(1)), 'code')
        put(d, 'sound.col.text', int(m.group(2)), 'code')

    # --- 소스에서: 생성기가 실제로 여는 스토리보드 시트
    for name in re.findall(r"data_only=True\)\['([^']+)'\]", imp) + \
                re.findall(r"wb_?\['([^']+)'\]", gen):
        put(d, 'storyboard.sheet.%s' % name, True, 'code')

    # --- 소스에서: 측정 여백
    for key, var in (('measure.safeBody', 'SAFE_BODY'), ('measure.safePop', 'SAFE_POP'),
                     ('measure.gapKr', 'GAP_KR')):
        m = re.search(r'^%s = (\d+)' % var, mea, re.M)
        if m:
            put(d, key, int(m.group(1)), 'code')
    return d


# ---------------------------------------------------------------- 대조
def compare(rid='cj_reading'):
    """rules.json 과 코드 값을 견준다. 고치지는 않는다.

    돌려주는 값: {'same':[...], 'diff':[{key,rules,code}], 'onlyRules':[], 'onlyCode':[]}
    """
    r = load(rules_path(rid))
    c = code_rules(rid)
    if not r:
        return {'error': 'rules.json 이 없습니다 — 프로토 분석 뒤 승격하세요.',
                'code': c['items']}
    ri, ci = r['items'], c['items']
    out = {'same': [], 'diff': [], 'onlyRules': [], 'onlyCode': [],
           'unknown': [], 'info': []}
    for k in sorted(set(ri) | set(ci)):
        if k.startswith('info.'):
            out['info'].append(k)           # 본 것을 적어 둔 것. 규칙이 아니다.
        elif ri.get(k, {}).get('source') == 'none':
            out['unknown'].append(k)        # 프로토로는 알 수 없는 것 — 코드 값을 쓴다
        elif k not in ci:
            out['onlyRules'].append(k)
        elif k not in ri:
            out['onlyCode'].append(k)
        elif ri[k].get('value') == ci[k].get('value'):
            out['same'].append(k)
        else:
            out['diff'].append({'key': k, 'rules': ri[k].get('value'),
                                'code': ci[k].get('value'),
                                'source': ri[k].get('source', '')})
    return out


def report(rid='cj_reading'):
    """대조 결과를 사람이 읽는 글로."""
    c = compare(rid)
    if 'error' in c:
        return c['error']
    L = ['같음 %d  다름 %d  규칙에만 %d  코드에만 %d  프로토로는 모름 %d'
         % (len(c['same']), len(c['diff']), len(c['onlyRules']),
            len(c['onlyCode']), len(c.get('unknown', [])))]
    if c['diff']:
        L.append('')
        L.append('[다름] — 프로토에서 본 값과 지금 코드가 다릅니다. 눈으로 확인하세요.')
        for d in c['diff']:
            L.append('  %-28s 프로토 %s   코드 %s'
                     % (d['key'], json.dumps(d['rules'], ensure_ascii=False),
                        json.dumps(d['code'], ensure_ascii=False)))
    if c['onlyCode']:
        L.append('')
        L.append('[코드에만] — 프로토에서 찾지 못한 것. 아직 코드에 남겨 둡니다.')
        L += ['  ' + k for k in c['onlyCode']]
    if c['onlyRules']:
        L.append('')
        L.append('[규칙에만] — 프로토에서 새로 본 것.')
        L += ['  ' + k for k in c['onlyRules']]
    if c.get('info'):
        L.append('')
        L.append('[적어 둔 것] — 규칙이 아니라 프로토에서 본 사실. 대조하지 않습니다.')
        L += ['  ' + k for k in c['info']]
    if c.get('unknown'):
        L.append('')
        L.append('[프로토로는 모름] — HTML 에 나타나지 않는 값. 코드 값을 그대로 씁니다.')
        L += ['  ' + k for k in c['unknown']]
    L.append('')
    L.append('※ 이 단계에서 rules.json 은 생성에 쓰이지 않습니다. 결과는 그대로입니다.')
    return '\n'.join(L)


if __name__ == '__main__':
    import sys
    print(report(sys.argv[1] if len(sys.argv) > 1 else 'cj_reading'))
