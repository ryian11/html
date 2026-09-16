# -*- coding: utf-8 -*-
"""회귀 검사 — 생성 결과가 기준본과 바이트 단위로 같은지 본다.

생성기를 고칠 때마다 돌린다. 실기 폴더는 건드리지 않는다.
임시 폴더에 다시 뽑아서 기준본과 견줄 뿐이다.

  py regress.py save  cj_reading 7 8     지금 결과를 기준본으로 저장
  py regress.py check cj_reading 7 8     기준본과 견주기
  py regress.py check cj_reading         기준본이 있는 단원 전부

기준본은 _기준본/<레시피>/<단원>/ 에 쌓인다.
"""
import io, os, sys, shutil, tempfile, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '_기준본')
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def _digest(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def _tree(root):
    """{상대경로: sha1} — _backup 은 뺀다."""
    out = {}
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('_backup', '_기준본')]
        for f in files:
            p = os.path.join(dirpath, f)
            out[os.path.relpath(p, root).replace('\\', '/')] = _digest(p)
    return out


def as_unit(u):
    """명령줄이나 폴더 이름에서 온 '7' 을 레시피가 아는 7 로."""
    s = str(u)
    return int(s) if s.isdigit() else u


def rebuild(rid, unit):
    """임시 폴더에 생성 단계만 다시 돌린다. 실기는 건드리지 않는다."""
    import runner
    unit = as_unit(unit)
    recipe = runner.load_recipe(rid)
    slots = runner.load_settings().get(rid, {})
    tmp = tempfile.mkdtemp(prefix='regress_')
    res = runner.run(recipe, unit, slots, steps=('build',), out=tmp, verbose=False)
    if not res['ok']:
        msgs = [s.get('msg', '') for s in res['steps'] if not s.get('ok')]
        shutil.rmtree(tmp, ignore_errors=True)
        raise RuntimeError('다시 뽑기 실패 — %s' % ('\n'.join(msgs) or '까닭 모름'))
    return tmp


def base_dir(rid, unit):
    return os.path.join(BASE, rid, str(unit))


def save(rid, units):
    """지금 생성 결과를 기준본으로 박아 둔다. 실기와 다른 곳도 함께 알려 준다."""
    lines = []
    for unit in units:
        tmp = rebuild(rid, unit)
        try:
            dst = base_dir(rid, unit)
            # 지우지 않고 덮어쓴다 — 지우기가 막힌 곳에서도 되게.
            os.makedirs(dst, exist_ok=True)
            stale = set(_tree(dst))
            for rel in _tree(tmp):
                s2 = os.path.join(tmp, rel.replace('/', os.sep))
                d2 = os.path.join(dst, rel.replace('/', os.sep))
                os.makedirs(os.path.dirname(d2), exist_ok=True)
                shutil.copyfile(s2, d2)
                stale.discard(rel)
            for rel in sorted(stale):
                try:
                    os.remove(os.path.join(dst, rel.replace('/', os.sep)))
                except OSError:
                    lines.append('  예전 기준본 파일이 남음: %s' % rel)
            n = len(_tree(tmp))
            lines.append('%s단원 기준본 %d개 저장' % (unit, n))
            lines += ['  ' + s for s in _vs_live(rid, unit, tmp)]
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return '\n'.join(lines)


def _vs_live(rid, unit, tmp):
    """방금 뽑은 것과 실기 폴더를 견준다 (손으로 고친 자국 찾기)."""
    import runner
    recipe = runner.load_recipe(rid)
    slots = runner.load_settings().get(rid, {})
    ctx = runner.Ctx(recipe, slots)
    if hasattr(recipe, 'setup'):
        recipe.setup(ctx)
    live = recipe.out_dir(ctx, as_unit(unit))
    if not os.path.isdir(live):
        return ['실기 폴더가 없어 견주지 못함']
    diff = []
    for rel, h in sorted(_tree(tmp).items()):
        p = os.path.join(live, rel.replace('/', os.sep))
        if not os.path.isfile(p):
            diff.append('실기에 없음  %s' % rel)
        elif _digest(p) != h:
            diff.append('실기와 다름  %s' % rel)
    return diff or ['실기와 같음']


def check(rid, units=None):
    """기준본과 견준다. 돌려주는 값: (탈 없음?, 알림글)"""
    root = os.path.join(BASE, rid)
    if not os.path.isdir(root):
        return True, '기준본이 없습니다 — 먼저 save 하세요.'
    if not units:
        units = sorted(os.listdir(root), key=lambda s: (len(s), s))
    ok, lines = True, []
    for unit in units:
        dst = base_dir(rid, unit)
        if not os.path.isdir(dst):
            lines.append('%s단원: 기준본 없음 — 건너뜀' % unit)
            continue
        tmp = rebuild(rid, unit)
        try:
            want, got = _tree(dst), _tree(tmp)
            bad = []
            for rel in sorted(set(want) | set(got)):
                if rel not in got:
                    bad.append('사라짐  %s' % rel)
                elif rel not in want:
                    bad.append('새로 생김  %s' % rel)
                elif want[rel] != got[rel]:
                    bad.append('달라짐  %s' % rel)
            if bad:
                ok = False
                lines.append('%s단원  !! %d곳 달라짐 (전체 %d개)' % (unit, len(bad), len(want)))
                lines += ['   ' + b for b in bad[:20]]
                if len(bad) > 20:
                    lines.append('   … 그 밖 %d곳' % (len(bad) - 20))
            else:
                lines.append('%s단원  그대로 (%d개)' % (unit, len(want)))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return ok, '\n'.join(lines)


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ('save', 'check'):
        print(__doc__)
        return
    cmd, rid = a[0], (a[1] if len(a) > 1 else 'cj_reading')
    units = a[2:]
    if cmd == 'save':
        if not units:
            print('어느 단원을 기준본으로 삼을지 적어 주세요.')
            return
        print(save(rid, units))
    else:
        ok, msg = check(rid, units)
        print(msg)
        sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
