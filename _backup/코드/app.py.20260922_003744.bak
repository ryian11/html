# -*- coding: utf-8 -*-
"""HTML 생성기 — 로컬 화면.

  py app.py            브라우저에서 http://127.0.0.1:8765 열기
  py app.py --port 9000

파이썬 기본 모듈만 씁니다. 따로 설치할 것이 없습니다.
"""
import io, os, sys, json, html, time, threading, mimetypes, posixpath, traceback
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import runner                                    # noqa: E402

JOBS = {}          # id -> {state, log, result}
JOB_SEQ = [0]
LAST_OUT = {}      # (레시피, 단원) -> 마지막으로 쓴 폴더


# ---------------------------------------------------------------- 일감
def start_job(rid, units, steps, out, pages=None):
    JOB_SEQ[0] += 1
    jid = str(JOB_SEQ[0])
    job = {'id': jid, 'state': 'running', 'log': [], 'results': [], 'done': 0,
           'total': len(units)}
    JOBS[jid] = job

    def say(s):
        job['log'].append(s)

    def work():
        try:
            recipe = runner.load_recipe(rid)
            slots = runner.load_settings().get(rid, {})
            for u in units:
                say('=== %s단원 ===' % u)
                r = _run_one(recipe, u, slots, steps, out, say, pages)
                job['results'].append(r)
                job['done'] += 1
            job['state'] = 'done'
        except Exception:
            say(traceback.format_exc(limit=4))
            job['state'] = 'error'
    threading.Thread(target=work, daemon=True).start()
    return jid


def start_task(title, fn):
    """생성과 상관없는 일 (프로토 분석·회귀 검사) 을 같은 기록창에 흘려 보낸다."""
    JOB_SEQ[0] += 1
    jid = str(JOB_SEQ[0])
    job = {'id': jid, 'state': 'running', 'log': [title], 'results': [],
           'done': 0, 'total': 1, 'kind': 'task'}
    JOBS[jid] = job

    def work():
        try:
            for line in (fn() or '').splitlines():
                job['log'].append(line)
            job['state'] = 'done'
        except Exception as e:
            job['log'].append(str(e))
            job['log'].append(traceback.format_exc(limit=4))
            job['state'] = 'error'
        job['done'] = 1
    threading.Thread(target=work, daemon=True).start()
    return jid


def _run_one(recipe, unit, slots, steps, out, say, pages=None):
    """runner.run 과 같되 진행 상황을 화면으로 흘려 보낸다."""
    ctx = runner.Ctx(recipe, slots, out, pages)
    if hasattr(recipe, 'setup'):
        recipe.setup(ctx)
    res = {'unit': unit, 'steps': [], 'ok': True, 'preview': [], 'backup': None,
           'pages': ctx.pages}
    try:
        res['out'] = ctx.out_dir(unit)
    except Exception:
        res['out'] = None

    say('  범위: %s' % ('고른 쪽 ' + ', '.join(pages) if pages else '단원 전체'))
    bakdir = None
    if 'build' in steps and not out:
        try:
            bakdir = runner.backup(ctx, unit)
            res['backup'] = os.path.basename(bakdir) if bakdir else None
            if bakdir:
                say('  백업 → _backup/%s' % res['backup'])
        except Exception as e:
            say('  백업 실패: %s' % e)

    for name in runner.STEPS:
        if name not in steps:
            continue
        fn = getattr(recipe, name, None)
        if fn is None:
            continue
        t0 = time.time()
        try:
            r = fn(ctx, unit)
            ok, msg = (r is not False), (r if isinstance(r, str) else '')
        except runner.SkipStep as e:
            say('  %-8s 건너뜀 (%s)' % (name, e))
            res['steps'].append(dict(name=name, ok=True, skipped=True, msg=str(e)))
            continue
        except Exception:
            ok, msg = False, traceback.format_exc(limit=3)
        dt = round(time.time() - t0, 1)
        res['steps'].append(dict(name=name, ok=ok, msg=msg, sec=dt))
        say('  %-8s %s  %.1fs%s' % (name, 'OK' if ok else '!!', dt,
                                    ('\n' + msg) if not ok else
                                    (('  — ' + msg) if msg else '')))
        if not ok:
            res['ok'] = False
            break

    if res['out']:
        LAST_OUT[(recipe.ID, str(unit))] = res['out']
    # 검증이 걸렸을 때야말로 무엇이 쓰였는지 봐야 하므로, 성패와 상관없이 알려 준다.
    if bakdir:
        try:
            wrote = []
            for rel in recipe.outputs(ctx, unit):
                a = os.path.join(bakdir, rel.replace('/', os.sep))
                b = os.path.join(res['out'] or '', rel.replace('/', os.sep))
                old_ = io.open(a, 'rb').read() if os.path.isfile(a) else None
                new_ = io.open(b, 'rb').read() if os.path.isfile(b) else None
                if old_ != new_:
                    wrote.append(rel)
            res['wrote'] = wrote
            say('')
            say('  이번 생성에서 바뀐 파일 %d개' % len(wrote))
            for rel in wrote:
                say('    - ' + rel)
            if not wrote:
                say('    (없음 — 앞서 만든 것과 내용이 같습니다)')
        except Exception as e:
            say('  견주기 실패: %s' % e)

    if hasattr(recipe, 'preview'):
        try:
            root = res['out'] or ''
            pv = recipe.preview(ctx, unit)
            if isinstance(pv, dict):          # 묶음 (이미 상대 경로) — 그대로
                res['preview'] = pv
            else:                             # 옛 모양 (절대 경로 목록)
                res['preview'] = [os.path.relpath(p, root).replace('\\', '/')
                                  for p in pv]
        except Exception:
            pass
    return res


def out_root(rid, unit):
    hit = LAST_OUT.get((rid, str(unit)))
    if hit:
        return hit
    recipe = runner.load_recipe(rid)
    slots = runner.load_settings().get(rid, {})
    ctx = runner.Ctx(recipe, slots)
    if hasattr(recipe, 'setup'):
        recipe.setup(ctx)
    u = str(unit)
    return recipe.out_dir(ctx, int(u) if u.isdigit() else unit)


# ---------------------------------------------------------------- 서버
class H(BaseHTTPRequestHandler):
    server_version = 'HtmlGen/1'

    def log_message(self, *a):
        pass

    # ---- 보내기
    def _send(self, code, body, ctype='application/json; charset=utf-8'):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode('utf-8')
        elif isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    # ---- GET
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        p = u.path
        try:
            if p in ('/', '/index.html'):
                return self._send(200, PAGE, 'text/html; charset=utf-8')
            if p == '/api/recipes':
                out = []
                for r in runner.list_recipes():
                    m = runner.load_recipe(r)
                    out.append({'id': r, 'name': getattr(m, 'NAME', r)})
                return self._send(200, out)
            if p.startswith('/api/recipe/'):
                return self._send(200, self._recipe_info(p.rsplit('/', 1)[-1]))
            if p == '/api/job':
                j = JOBS.get(q.get('id', [''])[0])
                return self._send(200, j or {'state': 'none'})
            if p == '/api/backups':
                rid, unit = q.get('recipe', [''])[0], q.get('unit', [''])[0]
                names = []
                for d in (os.path.join(runner.HERE, '_backup', '산출물', rid, str(unit)),
                          os.path.join(out_root(rid, unit), '_backup')):   # 예전 자리도 본다
                    if os.path.isdir(d):
                        names += [n for n in os.listdir(d) if n not in names]
                names.sort(reverse=True)
                return self._send(200, {'list': names[:20], 'total': len(names)})
            if p == '/api/proto':
                return self._send(200, self._proto_info(
                    q.get('recipe', [''])[0], q.get('lesson', [''])[0]))
            if p == '/api/project':
                return self._send(200, self._project(q.get('recipe', ['cj_reading'])[0]))
            if p == '/api/pages':
                rid, unit = q.get('recipe', [''])[0], q.get('unit', [''])[0]
                m = runner.load_recipe(rid)
                ctx = runner.make_ctx(m, runner.load_settings().get(rid, {}))
                u = int(unit) if unit.isdigit() else unit
                try:
                    lst = m.pages(ctx, u) if hasattr(m, 'pages') else []
                except Exception:
                    lst = []
                return self._send(200, {'unit': unit, 'pages': lst})
            if p == '/api/layout':
                import layout_edit
                return self._send(200, layout_edit.form(q.get('unit', [''])[0]))
            if p == '/api/compare':
                import rules_io
                rid = q.get('recipe', ['cj_reading'])[0]
                return self._send(200, {'text': rules_io.report(rid)})
            if p == '/api/ls':
                return self._send(200, self._ls(q.get('path', [''])[0]))
            if p.startswith('/files/'):
                return self._files(p)
            return self._send(404, {'error': 'not found'})
        except Exception:
            return self._send(500, {'error': traceback.format_exc(limit=4)})

    # ---- POST
    def do_POST(self):
        u = urlparse(self.path)
        n = int(self.headers.get('Content-Length') or 0)
        body = json.loads(self.rfile.read(n) or b'{}')
        try:
            if u.path == '/api/settings':
                st = runner.load_settings()
                st[body['recipe']] = body['slots']
                runner.save_settings(st)
                return self._send(200, {'ok': True})
            if u.path == '/api/run':
                jid = start_job(body['recipe'],
                                [int(x) if str(x).isdigit() else x for x in body['units']],
                                tuple(body.get('steps') or runner.STEPS),
                                body.get('out') or None,
                                body.get('pages') or None)
                return self._send(200, {'job': jid})
            if u.path == '/api/project':
                import project_io
                rid = body['recipe']
                cur = {x['id']: x for x in project_io.units(rid)}
                n = 0
                for e in (body.get('units') or []):
                    row = cur.get(e.get('id'))
                    if not row:
                        continue
                    for k in ('name', 'sheet', 'guide'):
                        if k in e:
                            v = (e[k] or '').strip()
                            if v:
                                if row.get(k) != v:
                                    n += 1
                                row[k] = v
                            elif k in row:
                                row.pop(k)
                                n += 1
                project_io.put_units(rid, [cur[k] for k in sorted(
                    cur, key=lambda i: (0, int(i), '') if i.isdigit() else (1, 0, i))])
                runner.load_recipe(rid)          # 등록부를 다시 올린다
                return self._send(200, {'ok': True, 'changed': n})
            if u.path == '/api/analyze':
                rid = body['recipe']
                lesson = str(body.get('lesson') or '').strip()
                pages = body.get('pages') or None

                def go():
                    recipe = runner.load_recipe(rid)
                    slots = dict(runner.load_settings().get(rid, {}),
                                 proto_lesson=lesson)
                    if body.get('ops'):
                        slots['proto_ops'] = body['ops']
                    r = runner.analyze(recipe, slots, pages)
                    L = ['%d항목을 %s 에 적었습니다.' % (r['items'],
                                                  os.path.basename(r['path'])),
                         '본 쪽: %s' % ', '.join(r['pages'])]
                    L += ['  · %s' % x for x in r['notes']]
                    L.append('')
                    L.append('확인한 뒤 [승격] 을 누르면 rules.json 으로 옮깁니다.')
                    return '\n'.join(L)
                return self._send(200, {'job': start_task('프로토 분석 — %s단원' % lesson, go)})
            if u.path == '/api/promote':
                rid, lesson = body['recipe'], str(body.get('lesson') or '').strip()
                fresh = bool(body.get('fresh'))

                def go():
                    r = runner.promote(rid, lesson, body.get('keys') or None, fresh)
                    kept = r.get('kept') or []
                    L = ['rules.json 에 합쳤습니다 — 새로 쓴 것 %d · 값 같음 %d · 그대로 둔 예전 규칙 %d'
                         % (len(r['moved']), len(r['same']), len(kept))]
                    if kept:
                        L.append('  이번 분석에 없어 건드리지 않은 규칙:')
                        L += ['    - %s' % k for k in kept]
                    L += ['', runner.compare(rid)]
                    return '\n'.join(L)
                return self._send(200, {'job': start_task('승격 — %s단원' % lesson, go)})
            if u.path == '/api/regress':
                rid = body.get('recipe') or 'cj_reading'
                units = [str(x) for x in (body.get('units') or [])]
                mode = body.get('mode') or 'check'

                def go():
                    import regress
                    if mode == 'save':
                        return regress.save(rid, units)
                    ok, msg = regress.check(rid, units or None)
                    return msg + ('\n\n달라진 곳이 없습니다.' if ok
                                  else '\n\n!! 결과가 달라졌습니다. 되돌리거나 까닭을 찾으세요.')
                return self._send(200, {'job': start_task(
                    '회귀 검사 (%s)' % ('기준본 저장' if mode == 'save' else '견주기'), go)})
            if u.path == '/api/layout':
                import layout_edit
                r = layout_edit.save(body['unit'], body)
                return self._send(200, r)
            if u.path == '/api/regen':
                rid = body.get('recipe') or 'cj_reading'
                unit = body['unit']
                pages = body.get('pages') or None
                steps = tuple(body.get('steps') or runner.STEPS)

                def go():
                    import layout_edit
                    r = layout_edit.regen(rid, unit, pages, steps)
                    L = list(r['log'])
                    L.append('')
                    if pages:
                        L.append('고친 쪽: %s' % ', '.join(pages))
                    L.append('새로 쓴 파일 %d개' % len(r['changed']))
                    L += ['  ' + x for x in r['changed']]
                    if r['restored']:
                        L.append('되돌린 파일 %d개 (고르지 않은 쪽)' % len(r['restored']))
                    L.append('그대로인 파일 %d개' % len(r['same']))
                    if r['backup']:
                        L.append('백업: %s' % os.path.basename(r['backup']))
                    if not r['ok']:
                        L.append('')
                        L.append('!! 검증에서 걸린 것이 있습니다. 위 기록을 보세요.')
                    return '\n'.join(L)
                return self._send(200, {'job': start_task(
                    '재생성 — %s단원%s' % (unit, (' / %d쪽' % len(pages)) if pages else ' 전체'),
                    go)})
            if u.path == '/api/quit':
                self._send(200, {'ok': True})
                threading.Thread(target=lambda: (time.sleep(0.4),
                                                 os._exit(0)), daemon=True).start()
                return
            if u.path == '/api/restore':
                recipe = runner.load_recipe(body['recipe'])
                slots = runner.load_settings().get(body['recipe'], {})
                ctx = runner.Ctx(recipe, slots)
                if hasattr(recipe, 'setup'):
                    recipe.setup(ctx)
                k = runner.restore(ctx, int(body['unit']), body['stamp'])
                return self._send(200, {'ok': True, 'n': k})
            return self._send(404, {'error': 'not found'})
        except Exception:
            return self._send(500, {'error': traceback.format_exc(limit=4)})

    # ---- 도우미
    def _recipe_info(self, rid):
        m = runner.load_recipe(rid)
        slots = runner.load_settings().get(rid, {})
        ctx = runner.Ctx(m, slots)
        if hasattr(m, 'setup'):
            try:
                m.setup(ctx)
            except Exception:
                pass
        try:
            units = [str(x) for x in m.units(ctx)] if hasattr(m, 'units') else []
        except Exception:
            units = []
        try:
            labels = m.unit_labels(ctx) if hasattr(m, 'unit_labels') else {}
        except Exception:
            labels = {}
        return {'id': rid, 'name': getattr(m, 'NAME', rid), 'unitLabels': labels,
                'slots': [{'key': s[0], 'label': s[1], 'kind': s[2],
                           'optional': bool(len(s) > 3 and s[3].get('optional')),
                           'hint': (s[3].get('hint', '') if len(s) > 3 else ''),
                           'value': slots.get(s[0], '')} for s in getattr(m, 'SLOTS', [])],
                'units': units,
                'edit': [{'path': a, 'ui': b} for a, b in getattr(m, 'EDIT', [])]}

    def _project(self, rid):
        """단원별 자료 — 시트 이름 · 지도서 PDF 는 교재마다 다르다."""
        import project_io
        m = runner.load_recipe(rid)
        ctx = runner.make_ctx(m, runner.load_settings().get(rid, {}))
        try:
            m.units(ctx)                          # 새 단원이 있으면 찾아 적어 둔다
        except Exception:
            pass
        import read_paths as P
        out = []
        for u in project_io.units(rid):
            g = project_io.abspath(P.ROOT, u.get('guide', ''))
            out.append({'id': u['id'], 'name': u.get('name', u['id']),
                        'sheet': u.get('sheet', ''), 'guide': u.get('guide', ''),
                        'guideOk': bool(u.get('guide')) and os.path.isfile(g),
                        'storyboard': u.get('storyboard', ''), 'ops': u.get('ops', '')})
        return {'recipe': rid, 'root': P.ROOT, 'units': out}

    def _proto_info(self, rid, lesson):
        """고를 수 있는 견본 쪽과, 이미 뽑아 둔 분석 결과."""
        import rules_io
        m = runner.load_recipe(rid)
        slots = dict(runner.load_settings().get(rid, {}))
        if lesson:
            slots['proto_lesson'] = lesson
        out = {'lesson': lesson, 'pages': [], 'ops': '', 'items': {}, 'notes': [],
               'hasRules': os.path.isfile(rules_io.rules_path(rid)),
               'protos': rules_io.list_protos(rid)}
        try:
            ctx = runner.make_ctx(m, slots)
            out['ops'] = m.proto_ops(ctx) if hasattr(m, 'proto_ops') else ''
            out['pages'] = m.proto_pages(ctx) if hasattr(m, 'proto_pages') else []
        except Exception as e:
            out['error'] = str(e)
        d = rules_io.load(rules_io.proto_path(rid, lesson)) if lesson else None
        if d:
            out['items'] = d.get('items', {})
            out['notes'] = d.get('notes', [])
            out['made'] = d.get('made', '')
            out['done'] = (d.get('proto') or {}).get('pages', [])
            # 지금 쓰는 규칙(rules.json)과 견줘 본다 — 읽기만 한다.
            # info.* 는 '프로토에서 본 사실' 이라 rules_io.compare() 도 견주지 않는다.
            cur = rules_io.load(rules_io.rules_path(rid)) or {}
            ci, pi = (cur.get('items') or {}), out['items']
            keep = lambda k: not k.startswith('info.')
            out['applied'] = len(ci)
            out['newKeys'] = sorted(k for k in pi if keep(k) and k not in ci)
            out['diffKeys'] = sorted(k for k in pi if keep(k) and k in ci
                                     and (ci[k] or {}).get('value') != (pi[k] or {}).get('value'))
            out['noneKeys'] = sorted(k for k in pi if (pi[k] or {}).get('source') == 'none')
        return out

    def _ls(self, path):
        """사용자가 고른 폴더 **한 단계만** 보여 준다. 재귀 없음."""
        if not path:
            return {'path': '', 'dirs': [], 'files': []}
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            return {'path': path, 'error': '폴더가 아닙니다', 'dirs': [], 'files': []}
        dirs, files = [], []
        for name in sorted(os.listdir(path)):
            (dirs if os.path.isdir(os.path.join(path, name)) else files).append(name)
        return {'path': path, 'up': os.path.dirname(path), 'dirs': dirs, 'files': files}

    def _files(self, p):
        """/files/<레시피>/<단원>/<상대경로> — 산출 폴더 안만 서빙."""
        parts = p[len('/files/'):].split('/', 3)
        if len(parts) < 3:
            return self._send(404, {'error': 'bad path'})
        rid, unit = parts[0], parts[1]
        # components.js 가 location.pathname 에서 'ops' 를 찾아 include 경로를 잡는다.
        # 그래서 미리보기 URL 에도 /ops/ 를 한 칸 끼워 넣는다.
        if parts[2] == 'ops':
            rel = unquote(parts[3]) if len(parts) > 3 else ''
        else:
            rel = unquote('/'.join(parts[2:]))
        root = os.path.abspath(out_root(rid, unit))
        target = os.path.abspath(os.path.join(root, rel.replace('/', os.sep)))
        if not target.startswith(root + os.sep) and target != root:
            return self._send(403, {'error': '밖으로 나갈 수 없습니다'})
        if not os.path.isfile(target):
            return self._send(404, {'error': rel})
        ctype = mimetypes.guess_type(target)[0] or 'application/octet-stream'
        if ctype.startswith('text/') or ctype.endswith(('javascript', 'json')):
            ctype += '; charset=utf-8'
        with open(target, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)


def _log_env():
    """어느 파일이 실제로 불려 왔는지 적어 둔다.

    묵은 .pyc 를 물고 있으면 고친 코드가 안 돌아 엉뚱한 오류가 난다.
    나중에 따질 수 있게 시작할 때 한 줄 남긴다.
    """
    try:
        for x in runner.purge_pyc():
            _log('  껍데기 치움: %s' % x)
        import inspect
        import read_gen
        _log('  read_gen %s  build%s'
             % (read_gen.__file__, inspect.signature(read_gen.build)))
    except Exception as e:
        _log('  살핌 실패: %s' % e)


def _log(msg):
    try:
        with io.open(os.path.join(HERE, 'app.log'), 'a', encoding='utf-8') as f:
            f.write('%s  %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
    except Exception:
        pass


def main():
    port = 8765
    if '--port' in sys.argv:
        port = int(sys.argv[sys.argv.index('--port') + 1])
    url = 'http://127.0.0.1:%d' % port
    try:
        srv = ThreadingHTTPServer(('127.0.0.1', port), H)
    except OSError as e:
        # 이미 떠 있으면 그냥 물러난다 (두 번 눌러도 창이 두 개 안 뜬다)
        _log('포트 %d 가 이미 쓰이고 있습니다 — 기존 창을 쓰세요. (%s)' % (port, e))
        print('이미 떠 있습니다: %s' % url)
        return 0
    _log('시작 %s' % url)
    _log_env()
    print('HTML 생성기 — %s' % url)
    print('(끄려면 화면 오른쪽 위 [끝내기] 또는 Ctrl+C)')
    if '--no-open' not in sys.argv:
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    _log('끝')
    print('\n끝냅니다.')
    return 0


PAGE = ''   # 아래 app_page.py 에서 채운다
try:
    from app_page import PAGE          # noqa: E402
except Exception:
    PAGE = '<h1>app_page.py 가 없습니다</h1>'

if __name__ == '__main__':
    sys.exit(main())
