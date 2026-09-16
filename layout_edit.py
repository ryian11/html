# -*- coding: utf-8 -*-
"""설정 패널의 살림 — layout<N>.json 을 화면에서 고칠 수 있게 풀고 다시 묶는다.

화면에 보여 줄 것은 두 군데서 온다.
  · data<N>.py     이미 뽑아 놓은 문장 (번호 · 원문 · 해석) — 지금 실제로 쓰는 값
  · layout<N>.json 사람이 정한 것 (문단 나눔 · 갈아끼운 글자 · 뺀 문장 · CSS)

고친 값은 layout<N>.json 에만 쓴다. data<N>.py 는 다음 [추출] 때 다시 만들어진다.
"""
import io, os, re, sys, json, time, shutil, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import layout_io                                   # noqa: E402

LEAD = re.compile(r'^((?:\|\d+\|)+)')              # 문장 앞에 붙은 구문 번호


def layout_path(unit):
    return os.path.join(HERE, 'layout%s.json' % unit)


def data_mod(unit):
    """data<N>.py 를 불러온다. 없으면 None."""
    name = 'data%s' % unit
    if not os.path.isfile(os.path.join(HERE, name + '.py')):
        return None
    m = importlib.import_module(name)
    return importlib.reload(m)


def _split_lead(en):
    """'|3|The JWST was …' → ('|3|', 'The JWST was …')"""
    m = LEAD.match(en or '')
    return (m.group(1), en[m.end():]) if m else ('', en or '')


# ---------------------------------------------------------------- 읽기
def form(unit):
    """화면이 그릴 수 있는 꼴로 내놓는다."""
    p = layout_path(unit)
    lay = layout_io.load(p) if os.path.isfile(p) else layout_io.Layout()
    d = data_mod(unit)
    out = {'unit': str(unit), 'path': p, 'exists': os.path.isfile(p),
           'speaker': lay.SPEAKER, 'pages': [], 'dropped': [],
           'hasData': bool(d)}
    if not d:
        out['error'] = ('data%s.py 가 없습니다 — [추출] 을 먼저 돌리세요.' % unit)
        return out

    text_of = {k: v for k, v in lay.TEXT.items()}
    for page in d.ORDER:
        pg = d.PAGES[page]
        num = pg['num']
        paras, sents = [], []
        for kind, b in pg['blocks']:
            if kind != 'para':
                continue
            paras.append([sq for sq, _, _ in b])
            for sq, en, kr in b:
                over = (num, sq) in text_of
                if over:
                    # 갈아끼운 글자는 적힌 그대로 보여 준다.
                    # 앞의 |n| 이 손수 붙인 것일 수 있어 벗기면 안 된다.
                    lead, body = '', text_of[(num, sq)]
                else:
                    lead, body = _split_lead(en)
                sents.append({'seq': sq, 'lead': lead, 'en': body, 'kr': kr,
                              'over': over})
        out['pages'].append({
            'page': page, 'num': num,
            'paras': [','.join(g) for g in paras],
            'sents': sents,
            'prefix': {g[0]: lay.PREFIX.get((num, g[0]), '')
                       for g in paras if g},
            'css': (lay.CSS or {}).get(page, ''),
            'img': {k: list(v) for k, v in (lay.IMG or {}).get(page, {}).items()},
        })
    for (n2, sq) in sorted(lay.DROP):
        out['dropped'].append({'num': n2, 'seq': sq,
                               'kr': lay.KR.get((n2, sq), '')})
    return out


# ---------------------------------------------------------------- 쓰기
def backup_layout(unit):
    """고치기 전 layout 파일을 _backup/ 에 날짜시각으로 남긴다."""
    p = layout_path(unit)
    if not os.path.isfile(p):
        return None
    d = os.path.join(HERE, '_backup', 'layout')
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, 'layout%s_%s.json' % (unit, time.strftime('%Y%m%d_%H%M%S')))
    shutil.copy2(p, dst)
    return dst


def save(unit, body):
    """화면이 보낸 값을 layout<N>.json 에 되돌려 쓴다.

    body = {speaker, pages:[{num, page, paras:[...], css, prefix:{seq:kind},
                             sents:[{seq, en, kr, over}]}],
            undrop:[ '123/01', ... ]}
    고친 것만 적는다. 손대지 않은 항목은 원래 값을 그대로 둔다.
    """
    p = layout_path(unit)
    lay = layout_io.load(p) if os.path.isfile(p) else layout_io.Layout()
    before = io.open(p, encoding='utf-8').read() if os.path.isfile(p) else ''

    if 'speaker' in body:
        lay.SPEAKER = (body.get('speaker') or '').strip()

    for pinfo in body.get('pages') or []:
        num, page = str(pinfo['num']), pinfo['page']

        # 문단 나눔 — 빈 줄은 버린다
        groups = []
        for line in (pinfo.get('paras') or []):
            g = [x.strip() for x in str(line).replace('\t', ',').split(',') if x.strip()]
            if g:
                groups.append(g)
        if groups:
            lay.PARAS[num] = groups

        # 문단 첫머리
        for seq, kind in (pinfo.get('prefix') or {}).items():
            k = (num, seq)
            if kind:
                lay.PREFIX[k] = kind
            else:
                lay.PREFIX.pop(k, None)

        # 쪽 CSS — 빈 값이면 항목을 없앤다
        css = pinfo.get('css')
        if css is not None:
            css = css.rstrip() + '\n' if css.strip() else ''
            if css:
                lay.CSS[page] = css
            else:
                lay.CSS.pop(page, None)

        # 문장 — 글자와 해석
        for s in (pinfo.get('sents') or []):
            k = (num, s['seq'])
            en = (s.get('en') or '').strip()
            if s.get('over') and en:
                lay.TEXT[k] = en
            elif not s.get('over'):
                lay.TEXT.pop(k, None)
            kr = s.get('kr')
            if kr is not None:
                lay.KR[k] = kr.strip()

    for key in (body.get('undrop') or []):
        lay.DROP.discard(layout_io._k(key))
    for key in (body.get('drop') or []):
        lay.DROP.add(layout_io._k(key))

    bak = backup_layout(unit)
    layout_io.save(lay, p, lesson=int(unit) if str(unit).isdigit() else None)
    after = io.open(p, encoding='utf-8').read()
    return {'path': p, 'backup': bak, 'changed': before != after,
            'size': len(after)}


# ---------------------------------------------------------------- 쪽 단위 재생성
def page_files(recipe, ctx, unit, pages):
    """고른 쪽에 딸린 산출 파일 (상대 경로).  ops 안에서만."""
    rel = []
    for pg in pages:
        rel += ['%s.html' % pg, 'css/%s.css' % pg, 'js/%s.js' % pg,
                'popup/%s_kor1.html' % pg]
    return rel


def common_files(recipe, ctx, unit):
    """단원 공통 파일 — 들머리 쪽, 전체듣기 팝업, 예시답안.

    한 쪽만 고쳐도 이것들은 단원 전체에서 나오므로 함께 새로 써야
    앞뒤가 맞는다. 되돌리지 않는다.
    """
    d = data_mod(unit)
    order = list(getattr(d, 'ORDER', [])) if d else []
    mine = set(page_files(recipe, ctx, unit, order))
    return [r for r in recipe.outputs(ctx, unit) if r not in mine]


def regen(rid, unit, pages=None, steps=('extract', 'build', 'measure', 'verify')):
    """고른 쪽만 다시 뽑는다.

    막는 것이 두 겹이다.
      · 생성 단계가 고른 쪽만 쓴다 (read_gen.build 의 only)
      · 그래도 달라진 것이 있으면 방금 뜬 백업에서 되돌린다 (안전망)

    측정은 늘 실기 폴더(P.ops)를 재므로 진짜 이미지·글꼴 위에서 잰 값이 나온다.
    재는 것은 단원 전체다 — write_scrolls 가 ORDER 전체를 새로 쓰기 때문에
    한 쪽만 재면 나머지 쪽의 스크롤값이 지워진다.
    """
    import runner
    recipe = runner.load_recipe(rid)
    slots = runner.load_settings().get(rid, {})
    u = int(unit) if str(unit).isdigit() else unit
    ctx = runner.make_ctx(recipe, slots)
    live = recipe.out_dir(ctx, u)

    bak = runner.backup(ctx, u)                 # 되돌릴 자리 (안전망)
    res = runner.run(recipe, u, slots, steps=steps, verbose=False, pages=pages)
    log = ['  %-8s %s%s' % (s2['name'], '건너뜀' if s2.get('skipped')
                            else ('OK' if s2.get('ok') else '!!'),
                            ('  ' + str(s2['msg']).strip().splitlines()[0])
                            if s2.get('msg') else '')
           for s2 in res['steps']]

    keep = (set(page_files(recipe, ctx, u, pages)) | set(common_files(recipe, ctx, u))
            if pages else None)
    back, kept, changed = [], [], []
    if keep is not None and bak:
        for r in recipe.outputs(ctx, u):
            src = os.path.join(bak, r.replace('/', os.sep))
            dst = os.path.join(live, r.replace('/', os.sep))
            if r in keep:
                old = io.open(src, 'rb').read() if os.path.isfile(src) else None
                new_ = io.open(dst, 'rb').read() if os.path.isfile(dst) else None
                (changed if old != new_ else kept).append(r)
                continue
            if not os.path.isfile(src):
                continue                        # 예전에 없던 파일은 그대로 둔다
            old = io.open(src, 'rb').read()
            if os.path.isfile(dst) and io.open(dst, 'rb').read() == old:
                continue                        # 애초에 안 바뀜
            io.open(dst, 'wb').write(old)
            back.append(r)
    elif bak:
        for r in recipe.outputs(ctx, u):
            src = os.path.join(bak, r.replace('/', os.sep))
            dst = os.path.join(live, r.replace('/', os.sep))
            old = io.open(src, 'rb').read() if os.path.isfile(src) else None
            new_ = io.open(dst, 'rb').read() if os.path.isfile(dst) else None
            (changed if old != new_ else kept).append(r)

    return {'ok': res['ok'], 'log': log, 'out': live, 'backup': bak,
            'changed': changed, 'same': kept, 'restored': back,
            'pages': list(pages or [])}


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    else:
        print(json.dumps(form(a[0]), ensure_ascii=False, indent=1)[:2000])
