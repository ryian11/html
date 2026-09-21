# -*- coding: utf-8 -*-
"""생성기 껍데기 — 레시피를 불러 ① 추출 → ② 생성 → ③ 측정 → ④ 검증 을 돌린다.

  py runner.py                       레시피 목록
  py runner.py cj_reading            그 레시피가 받는 자료와 고를 수 있는 단원
  py runner.py cj_reading 7          7단원 전체 실행
  py runner.py cj_reading 7 8        여러 단원
  py runner.py cj_reading 7 --steps build,verify    일부 단계만
  py runner.py cj_reading 7 --out DIR                딴 데 뽑기(실기 안 건드림)
  py runner.py cj_reading --set root=E:\\...         자료 경로 지정(저장됨)

이 파일은 Reading 도 딕테이션도 모른다. 레시피가 선언한 것만 실행한다.
"""
import io, os, sys, json, time, shutil, importlib, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
RECIPE_DIR = os.path.join(HERE, 'recipes')
DATA_DIR = os.path.join(HERE, '단원자료')      # data<N>.py · 잰 값 · layout<N>.json
SETTINGS = os.path.join(HERE, 'settings.json')
os.makedirs(DATA_DIR, exist_ok=True)
if DATA_DIR not in sys.path:
    sys.path.insert(0, DATA_DIR)               # read_gen 이 이름으로 불러 쓴다
STEPS = ('extract', 'build', 'measure', 'verify')

# 고친 .py 가 실제로 불리도록 — 아래 '묵은 껍데기' 설명을 보라.
GEN_MODULES = ('read_gen', 'read_import', 'read_measure', 'layout_io')
KEEP_BACKUPS = 5        # 백업은 단원마다 최근 몇 벌만 남긴다
sys.dont_write_bytecode = True


# ---------------------------------------------------------------- 묵은 껍데기
# 파이썬은 .py 를 처음 읽을 때 __pycache__ 에 .pyc 를 만들어 두고,
# 다음부터는 원본의 (수정시각, 크기) 가 그때와 같으면 .py 를 아예 읽지 않는다.
#
# 이 폴더는 연결된 폴더라 수정시각이 오갈 때 흔들린다. 그래서 원본을 고쳐도
# 파이썬이 '그대로네' 하고 묵은 .pyc 를 계속 쓰는 일이 생긴다.
# 실제로 read_gen.py 에 only 를 넣었는데도 예전 build() 가 불려서
# "build() got an unexpected keyword argument 'only'" 가 났다.
#
# 그래서 시작할 때 어긋난 .pyc 를 치운다. 지울 수 없으면 앞머리를 지워
# 파이썬이 못 알아보게 만든다 — 그러면 원본에서 다시 읽는다.
def purge_pyc(verbose=False):
    import struct
    out = []
    for d in (os.path.join(HERE, '__pycache__'),
              os.path.join(DATA_DIR, '__pycache__'),
              os.path.join(RECIPE_DIR, '__pycache__')):
        if not os.path.isdir(d):
            continue
        srcdir = os.path.dirname(d)
        for f in sorted(os.listdir(d)):
            if not f.endswith('.pyc'):
                continue
            p = os.path.join(d, f)
            src = os.path.join(srcdir, f.split('.')[0] + '.py')
            if not os.path.isfile(src):
                continue
            try:
                head = io.open(p, 'rb').read(16)
                if len(head) < 16:
                    continue
                _magic, flags, mt, sz = struct.unpack('<IIII', head)
                if _magic == 0:                # 이미 못 알아보게 해 둔 것
                    continue
                if flags:                      # 해시로 검사하는 것은 건드리지 않는다
                    continue
                st = os.stat(src)
                if int(st.st_mtime) == mt and st.st_size == sz:
                    continue
            except Exception:
                continue
            try:
                os.remove(p)
                out.append('지움 ' + f)
            except OSError:
                try:
                    with io.open(p, 'r+b') as fh:
                        fh.write(b'\0\0\0\0')
                    out.append('앞머리 지움 ' + f)
                except Exception as e:
                    out.append('못 치움 %s (%s)' % (f, e))
    if out:
        importlib.invalidate_caches()
        if verbose:
            for x in out:
                print('  [pyc] ' + x)
    return out


def refresh_modules():
    """이미 올라온 생성 모듈을 원본에서 다시 읽는다.

    화면(서버)이 계속 떠 있는 동안 .py 를 고쳐도 예전 것이 남기 때문이다.
    read_paths 는 다시 읽지 않는다 — setup() 이 꽂아 둔 경로가 날아간다.
    """
    importlib.invalidate_caches()
    done = []
    for n in GEN_MODULES:
        m = sys.modules.get(n)
        if m is None:
            continue
        try:
            importlib.reload(m)
            done.append(n)
        except Exception:
            pass
    return done


purge_pyc()


# ---------------------------------------------------------------- 설정
def load_settings():
    if os.path.isfile(SETTINGS):
        return json.loads(io.open(SETTINGS, encoding='utf-8').read())
    return {}


def save_settings(d):
    io.open(SETTINGS, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(d, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- 레시피
def list_recipes():
    if not os.path.isdir(RECIPE_DIR):
        return []
    out = []
    for f in sorted(os.listdir(RECIPE_DIR)):
        if f.endswith('.py') and not f.startswith('_'):
            out.append(f[:-3])
    return out


def load_recipe(rid):
    if rid not in list_recipes():
        raise SystemExit('그런 레시피가 없습니다: %s\n있는 것: %s'
                         % (rid, ', '.join(list_recipes()) or '없음'))
    if RECIPE_DIR not in sys.path:
        sys.path.insert(0, RECIPE_DIR)
    purge_pyc()
    refresh_modules()
    m = importlib.import_module(rid)
    m = importlib.reload(m)
    m.ID = rid
    return m


class Ctx(object):
    """레시피에 넘기는 살림살이 — 자료 경로와 작업 폴더."""

    def __init__(self, recipe, slots, out=None, pages=None):
        self.recipe = recipe
        self.slots = slots or {}
        self._out = out
        self.pages = list(pages) if pages else None   # 고른 쪽. None 이면 단원 전체

    def __getitem__(self, k):
        return self.slots.get(k)

    def get(self, k, default=None):
        return self.slots.get(k, default)

    def out_dir(self, unit):
        if self._out:
            return os.path.join(self._out, str(unit)) if self._multi else self._out
        return self.recipe.out_dir(self, unit)

    _multi = False


# ---------------------------------------------------------------- 백업
def backup_root(ctx, unit):
    """백업이 쌓이는 곳 — **생성기 폴더 안**.

    예전에는 산출 폴더(개발물) 안에 _backup 을 두었는데,
    개발물에는 완성본만 남는 것이 맞아서 작업 영역으로 옮겼다.
    """
    return os.path.join(HERE, '_backup', '산출물', ctx.recipe.ID, str(unit))


def backup(ctx, unit):
    """레시피가 알려 준 산출물만 _backup/산출물/<레시피>/<단원>/<날짜시각>/ 로 떠 둔다."""
    if not hasattr(ctx.recipe, 'outputs'):
        return None
    root = ctx.recipe.out_dir(ctx, unit)
    rels = [r for r in ctx.recipe.outputs(ctx, unit)
            if os.path.isfile(os.path.join(root, r))]
    if not rels:
        return None
    dst = os.path.join(backup_root(ctx, unit), time.strftime('%Y%m%d_%H%M%S'))
    for r in rels:
        d = os.path.join(dst, r)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(root, r), d)
    prune_dirs(backup_root(ctx, unit), KEEP_BACKUPS)
    return dst


def prune_dirs(root, keep):
    """날짜시각 폴더가 쌓이지 않게 — 최근 것만 남기고 지운다.

    지우는 동작이라 실패해도 그냥 넘어간다(지우기가 막힌 곳도 있다).
    """
    if not os.path.isdir(root):
        return []
    names = sorted((n for n in os.listdir(root)
                    if os.path.isdir(os.path.join(root, n))), reverse=True)
    gone = []
    for n in names[keep:]:
        try:
            shutil.rmtree(os.path.join(root, n))
            gone.append(n)
        except Exception:
            pass
    return gone


def prune_files(root, keep, stem=lambda n: n.split('_2026')[0]):
    """같은 갈래의 백업 파일이 쌓이지 않게 — 갈래마다 최근 것만 남긴다."""
    if not os.path.isdir(root):
        return []
    byk = {}
    for n in sorted(os.listdir(root), reverse=True):
        if os.path.isfile(os.path.join(root, n)):
            byk.setdefault(stem(n), []).append(n)
    gone = []
    for k, names in byk.items():
        for n in names[keep:]:
            try:
                os.remove(os.path.join(root, n))
                gone.append(n)
            except Exception:
                pass
    return gone


def restore(ctx, unit, stamp):
    """[되돌리기] — 백업 하나를 제자리로 되돌린다."""
    root = ctx.recipe.out_dir(ctx, unit)
    src = os.path.join(backup_root(ctx, unit), stamp)
    if not os.path.isdir(src):                       # 예전에 산출 폴더에 뜬 것도 받아 준다
        old = os.path.join(root, '_backup', stamp)
        if os.path.isdir(old):
            src = old
        else:
            raise SystemExit('그런 백업이 없습니다: %s' % src)
    n = 0
    for dirpath, _, files in os.walk(src):
        for f in files:
            s = os.path.join(dirpath, f)
            d = os.path.join(root, os.path.relpath(s, src))
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            n += 1
    return n


# ---------------------------------------------------------------- 실행
def run(recipe, unit, slots, steps=STEPS, out=None, verbose=True, pages=None):
    """한 단원을 돌리고 결과를 dict 로 돌려준다 (UI 가 그대로 쓴다).

    pages 를 주면 그 쪽만 산출 폴더에 쓴다. 나머지 쪽 파일은 건드리지 않는다.
    """
    ctx = Ctx(recipe, slots, out, pages)
    if hasattr(recipe, 'setup'):
        recipe.setup(ctx)
    res = {'recipe': recipe.ID, 'unit': unit, 'steps': [], 'ok': True,
           'out': None, 'backup': None, 'preview': [], 'pages': ctx.pages}
    try:
        res['out'] = ctx.out_dir(unit)
    except Exception:
        pass

    if 'build' in steps and not out:
        try:
            res['backup'] = backup(ctx, unit)
        except Exception as e:
            res['steps'].append(dict(name='backup', ok=False, msg=str(e)))

    for name in STEPS:
        if name not in steps:
            continue
        fn = getattr(recipe, name, None)
        if fn is None:
            res['steps'].append(dict(name=name, ok=True, skipped=True,
                                     msg='이 레시피에는 없는 단계'))
            continue
        t0 = time.time()
        try:
            r = fn(ctx, unit)
            ok = (r is not False)
            msg = r if isinstance(r, str) else ''
        except SkipStep as e:
            res['steps'].append(dict(name=name, ok=True, skipped=True, msg=str(e)))
            if verbose:
                print('  건너뜀 %-8s %s' % (name, e))
            continue
        except Exception:
            ok, msg = False, traceback.format_exc(limit=3)
        dt = time.time() - t0
        res['steps'].append(dict(name=name, ok=ok, msg=msg, sec=round(dt, 1)))
        if verbose:
            print('  %-8s %s  %.1fs%s' % (name, 'OK' if ok else '!!', dt,
                                          '' if ok else '\n' + str(msg)))
        if not ok:
            res['ok'] = False
            break

    if hasattr(recipe, 'preview'):
        try:
            res['preview'] = recipe.preview(ctx, unit)
        except Exception:
            pass
    return res


class SkipStep(Exception):
    """레시피가 '이번엔 이 단계 건너뜀' 을 알릴 때 쓴다."""


# ---------------------------------------------------------------- 프로토
# 네 단계(STEPS)와 따로 돈다. 생성 결과에 손대지 않는다.
def make_ctx(recipe, slots, out=None, pages=None):
    ctx = Ctx(recipe, slots, out, pages)
    if hasattr(recipe, 'setup'):
        recipe.setup(ctx)
    return ctx


def proto_pages(recipe, slots):
    ctx = make_ctx(recipe, slots)
    if not hasattr(recipe, 'proto_pages'):
        return []
    try:
        return recipe.proto_pages(ctx)
    except Exception:
        return []


def analyze(recipe, slots, pages=None):
    """견본 쪽을 읽어 proto_L<N>.json 을 만든다."""
    if not hasattr(recipe, 'analyze'):
        raise SystemExit('이 레시피에는 프로토 분석이 없습니다.')
    return recipe.analyze(make_ctx(recipe, slots), pages)


def promote(rid, lesson, keys=None, fresh=False):
    import rules_io
    return rules_io.promote(rid, lesson, keys, fresh)


def compare(rid):
    import rules_io
    return rules_io.report(rid)


# ---------------------------------------------------------------- CLI
def _proto_cli(args, st):
    """--proto / --promote / --compare — 생성과 따로 도는 갈래."""
    rid = args[0]
    recipe = load_recipe(rid)
    slots = st.get(rid, {})
    if '--compare' in args:
        print(compare(rid))
        return True
    if '--proto' in args:
        n = args[args.index('--proto') + 1]
        slots = dict(slots, proto_lesson=n)
        pages = None
        if '--pages' in args:
            pages = [x for x in args[args.index('--pages') + 1].split(',') if x]
        if '--list' in args:
            print('\n'.join(proto_pages(recipe, slots)) or '견본 쪽이 없습니다')
            return True
        r = analyze(recipe, slots, pages)
        print('%s\n항목 %d개, 쪽 %s' % (r['path'], r['items'], ', '.join(r['pages'])))
        for x in r['notes']:
            print('  · %s' % x)
        return True
    if '--promote' in args:
        n = args[args.index('--promote') + 1]
        r = promote(rid, n, fresh='--fresh' in args)
        print('rules.json 으로 %d항목 옮김 (그대로 %d)' % (len(r['moved']), len(r['same'])))
        print()
        print(compare(rid))
        return True
    return False


def main():
    args = [a for a in sys.argv[1:]]
    st = load_settings()

    if args and args[0] in list_recipes() and any(
            a in args for a in ('--proto', '--promote', '--compare')):
        if _proto_cli(args, st):
            return

    if not args:
        print('레시피:')
        for r in list_recipes():
            m = load_recipe(r)
            print('  %-18s %s' % (r, getattr(m, 'NAME', '')))
        print('\n사용법:  py runner.py <레시피> <단원…> [--steps a,b] [--out DIR]')
        return 0

    rid = args.pop(0)
    recipe = load_recipe(rid)
    slots = dict(st.get(rid, {}))

    while '--set' in args:
        i = args.index('--set')
        k, v = args[i + 1].split('=', 1)
        slots[k] = v
        del args[i:i + 2]
        st[rid] = slots
        save_settings(st)
        print('저장:', k, '=', v)

    steps = STEPS
    if '--steps' in args:
        i = args.index('--steps')
        steps = tuple(x.strip() for x in args[i + 1].split(','))
        del args[i:i + 2]
    out = None
    if '--out' in args:
        i = args.index('--out')
        out = args[i + 1]
        del args[i:i + 2]

    units = [int(a) if a.isdigit() else a for a in args if not a.startswith('-')]

    ctx = Ctx(recipe, slots, out)
    if hasattr(recipe, 'setup'):
        recipe.setup(ctx)

    if '--restore' in args:
        i = args.index('--restore')
        stamp = args[i + 1]
        del args[i:i + 2]
        units = [int(a) if a.isdigit() else a for a in args if not a.startswith('-')]
        for u in units:
            print('되돌림 %d개  %s단원 ← %s' % (restore(ctx, u, stamp), u, stamp))
        return 0

    if not units:
        print(getattr(recipe, 'NAME', rid))
        print('\n받는 자료')
        for s in getattr(recipe, 'SLOTS', []):
            key, label, kind = s[0], s[1], s[2]
            opt = (len(s) > 3 and s[3].get('optional'))
            print('  %-14s %-24s %-5s %s%s' % (
                key, label, kind, slots.get(key, '(안 정함)'),
                '  (선택)' if opt else ''))
        if hasattr(recipe, 'units'):
            print('\n고를 수 있는 단원:', ', '.join(str(u) for u in recipe.units(ctx)))
        print('\n고칠 수 있는 파일:', ', '.join(
            '%s(%s)' % (a, b) for a, b in getattr(recipe, 'EDIT', [])) or '없음')
        return 0

    Ctx._multi = len(units) > 1
    bad = 0
    for u in units:
        print('\n=== %s  %s단원 ===' % (getattr(recipe, 'NAME', rid), u))
        r = run(recipe, u, slots, steps, out)
        if not r['ok']:
            bad += 1
        if r['backup']:
            print('  백업:', os.path.basename(r['backup']))
        if r['preview']:
            print('  미리보기 %d개' % len(r['preview']))
    print('\n%s' % ('끝.' if not bad else '%d단원에서 문제가 있습니다.' % bad))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
