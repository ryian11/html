# project_rules.json 최종 검증 — "현재 프로젝트에서 됨" ≠ "프로젝트 독립적"

구현 결과 보고서(`project_rules.json-구현결과.md`)를 그대로 인정하지 않고, 실제 코드를 다시 열어 한 줄씩 확인했습니다. 결론부터 말씀드리면 **F: 2번(일부 프로젝트 종속성이 남아 있음)** 입니다. 7·8단원 생성 결과가 기준본과 같다는 테스트는 사실이지만, 그건 "지금 이 프로젝트에서 안 깨졌다"는 것만 증명하고 "새 프로젝트가 코드 수정 없이 된다"는 것은 증명하지 않습니다. 아래는 그 둘을 구분해서 쓴 결과입니다.

---

## A. 현재 실제 데이터 흐름

```
① 사용자가 화면에서 [프로젝트 폴더] 를 고름
   → POST /api/settings  { recipe, slots:{root:"E:\...2026_cj_midd3_eng"} }
   → settings.json 에 저장 (app.py → runner.save_settings)

② 화면이 GET /api/recipe/cj_reading 을 부름
   → app.py:_recipe_info()
      → recipes/cj_reading.py:setup(ctx)
          - project_rules_io.ensure_migrated() : project_rules.json 이 없으면
            LEGACY_PATHS/LEGACY_PATTERNS 로 딱 한 번 만듦. 있으면 그대로 읽음.
          - P.SB_DIR/SND/WORDDIC/CONTENTS 를 project_rules.json["paths"] 로 채움
          - project_rules_io.units() 로 단원을 읽어 read_paths.UNITS 에 등록(_register)
      → recipes/cj_reading.py:units(ctx)
          - project_rules_io.units() 를 기준(have)으로 삼고
          - discover(ctx) 결과로 "빈 자리만" 채움  ← project_rules.json 우선, discover() 는 보조
          - 합친 결과를 project_rules_io.put_units() 로 다시 저장
      → recipes/cj_reading.py:unit_labels(ctx) → project_rules_io.units() 그대로 이름표

③ 화면 JS(app_page.py) 가 응답의 R.units / R.unitLabels 로 단원 <select> 와
   체크박스 목록을 그림  ← 여기는 실제로 project_rules.json 기준 (검증됨, 아래 B)

④ 사용자가 "프로토 단원" 칸에 **직접 숫자를 타이핑**
   (project_rules.json 에서 "고를 수 있는 프로토 후보 목록"을 만들어 보여주는 절차 없음)
   → GET /api/proto?recipe=cj_reading&lesson=N
      → recipes/cj_reading.py:proto_pages(ctx) → proto_scan.pages_in(ops, pattern=PR.pattern('pageFilename', …))
      → 화면이 그 페이지 체크박스를 그림

⑤ 사용자가 페이지를 고르고 [규칙 분석]
   → POST /api/analyze → runner.analyze → cj_reading.py:analyze(ctx, pages)
      → proto_lesson(ctx) 가 **문자열이 숫자일 때만** 동작 (아래 C-1)
      → proto_scan.scan(...) 이 rules/cj_reading/proto_L<N>.json 을 씀
        (이 안에서 scan_sound() 가 시트 이름을 **project_rules.json 과 무관하게**
         '%d과' 로 직접 구성함 — 아래 C-2)

⑥ [승격] → POST /api/promote → rules_io.promote() 가 proto_L<N>.json 을
   rules/cj_reading/rules.json 에 합침 (project_rules.json 과는 전혀 다른 파일)

⑦ 사용자가 단원/페이지 고르고 [만들기]
   → POST /api/run → app.py:_run_one → recipe.setup(ctx) 를 다시 부른 뒤
      extract → read_import.load_rules(rid) 로 rules.json 값을 읽고
                read_import.assemble(unit) 이 실제 자료(엑셀/PDF)를 읽어 data<N>.py 를 씀
                (엑셀 시트 이름은 project_rules.json["units"][i]["sheet"] 가 최우선,
                 없으면 rules.json 의 sound.sheet, 그것도 없으면 코드 기본값 '%d과')
      build   → read_gen.load_rules(rid) 로 rules.json 값을 읽고 HTML/CSS/JS 를 씀
      measure → Playwright 로 스크롤 여백을 재서 다시 build
      verify  → read_verify.verify()
   → 결과를 _backup/산출물 에 백업하고, preview 묶음을 만들어 화면에 돌려줌
```

**요약**: project_rules.json 이 실제로 기준이 되는 것은 ②③(경로·단원 목록) 단계뿐입니다. ④~⑥(프로토타입 선택·분석)은 project_rules.json 과 사실상 분리되어 있고, ⑦(추출·생성)은 project_rules.json(단원별 경로)과 rules.json(생성 규칙)이 같이 관여합니다.

---

## B. 완료된 부분 (프로젝트 독립화 관점에서 실제로 해결됨)

이건 코드를 직접 읽어 확인했습니다 — 사실입니다.

1. **경로 4종**(storyboardDir/soundXlsx/wordDicDir/contentsDir) — `setup()` 이 `project_rules.json["paths"]` 를 먼저 읽고, 없을 때만 LEGACY_PATHS 를 씀. (`recipes/cj_reading.py:59-97`)
2. **단원 목록/이름/시트/경로** — `units()`/`unit_labels()`/`_register()` 모두 `project_rules_io.units()` 를 기준으로 함. 화면의 단원 드롭다운·체크박스(`app_page.py:254-258`)도 이 값을 그대로 씀. **실제로 JSON 기준으로 동작함을 코드로 확인**.
3. **discover() 의 순서** — `units()` 에서 `have = {u['id']: u for u in PR.units()}` 를 먼저 만들고 `discover()` 결과는 빈 칸만 채움(`cur.setdefault`). JSON 에 있는 값을 discover() 가 덮어쓰는 코드는 없음 — 확인됨.
4. **이름 규칙(정규식) 4종**(storyboardFilename/specialUnitFilename/contentsFolder/pageFilename) — `discover()`/`proto_pages()`/`analyze()` 가 `PR.pattern(key, 기본값)` 으로 읽음. JSON 에 있으면 그 값, 없으면 CJ 기본값.
5. **rules.json 연결** — `read_import.py`/`read_gen.py` 가 각각 독립적으로 `R(key, 기본값)` 을 통해 `rules.json` 값을 우선 쓰고 없으면 코드 기본값을 씀. 결과가 그대로임을 diff 로 확인(7·8단원 바이트 단위 동일).
6. **project.json → project_rules.json 마이그레이션** — 최초 1회만 일어나고, 그 뒤로 `project_io.put_units()`/`save_all()` 은 코드 어디에서도 다시 호출되지 않음(읽기 전용으로 남음) — grep 으로 확인.
7. **/api/project 화면 편집** — GET·POST 모두 `project_rules_io` 를 씀. 화면에서 고친 값이 생성 로직이 보는 파일과 일치함(이전엔 project.json 과 어긋날 뻔했던 문제).

---

## C. 아직 남은 문제 (프로젝트 종속성이 실제로 남아 있는 부분)

우선순위가 다른 문제들이 섞여 있어 순서를 나눴습니다. **1번이 가장 심각**합니다 — 이건 "값이 없으면 CJ 값으로 대체"가 아니라 "새 프로젝트에서 기능 자체가 안 먹는" 코드 구조 문제입니다.

### C-1. 프로토타입(견본) 선택이 "단원 id 가 숫자일 때만" 동작함 (심각)

```python
# recipes/cj_reading.py
def proto_lesson(ctx):
    v = str(ctx.get('proto_lesson') or '').strip()
    return int(v) if v.isdigit() else None      # 숫자가 아니면 무조건 None

def analyze(ctx, pages=None):
    ...
    n = proto_lesson(ctx)
    if not n:
        raise RuntimeError('프로토 단원을 정해 주세요.')   # proto_ops 를 직접 채워도 여기서 막힘
```
`proto_ops` 슬롯을 사용자가 폴더로 직접 채워도, `analyze()` 는 `proto_lesson(ctx)` 가 정수가 아니면 무조건 막습니다. 즉 **단원 id 에 숫자가 하나도 없는 새 프로젝트(예: UnitA, UnitB … 전부 문자 id)에서는 "규칙 분석" 기능 자체를 쓸 수 없습니다.** JSON 을 아무리 잘 만들어도 코드가 막습니다. 이건 project_rules.json 으로 해결되는 문제가 아니라, `proto_lesson`/`proto_ops`/`analyze()` 가 "적어도 하나는 int 로 캐스팅 가능한 단원 id" 를 전제하는 코드 자체의 문제입니다.

지금 CJ 프로젝트는 special_lesson 하나만 문자 id 이고 나머지 8개가 숫자라 이 문제가 드러나지 않습니다.

### C-2. "%d과" (음원 시트 이름) 가 세 곳에 따로따로 박혀 있고, 그중 하나는 JSON 을 아예 안 봄

| 위치 | 방식 |
|---|---|
| `recipes/cj_reading.py:discover()` | `PR.pattern('soundSheet', '%d과')` — JSON 을 봄 ✅ |
| `read_import.py:sound()` | 단원별 `P.unit(n)['sheet']` 최우선, 없으면 `R('sound.sheet','%d과')`(rules.json) — JSON/rules.json 을 봄 ✅ |
| `proto_scan.py:scan_sound()` (100번째 줄) | `want = '%d과' % int(lesson)` — **project_rules.json 도 rules.json 도 안 보고 무조건 '%d과'** ❌ |

세 번째(`proto_scan.scan_sound`)는 "프로토 분석"(견본 페이지에서 규칙을 뽑는 단계)에 쓰이는데, 여기서 시트 이름을 잘못 구성하면 새 프로젝트의 음원 엑셀에서 아예 시트를 못 찾고 `notes.append('음원 엑셀: %s 시트가 없습니다')` 로 조용히 넘어갑니다 — **분석 결과에 음원 관련 규칙이 통째로 비게 됩니다.** `%d과` 같은 CJ 관례가 새 프로젝트에서 작동하지 않는 대표적인 지점입니다.

### C-3. read_paths.py 의 "값이 없을 때" 폴백이 여전히 CJ 이름을 스스로 만들어 씀 (원칙 4 위반)

```python
# read_paths.py
SB_NAME = '3학년 전자저작물_지시문_딕테이션_미니 단어장_구문 해설_Lesson %d.xlsx'

def storyboard(n):
    u = unit(n).get('storyboard')
    if u:
        return u
    return os.path.join(SB_DIR, SB_NAME % int(n))     # ← JSON 에 없으면 CJ 파일명을 "추측"

def ops(n):
    u = unit(n).get('ops')
    if u:
        return u
    return os.path.join(CONTENTS, 'lesson%02d' % int(n), 'ops')   # ← 마찬가지

def guide_pdf(n):
    ...
    if GUIDE_DIR:
        g = sorted(glob.glob(os.path.join(GUIDE_DIR, '*각론%d*.pdf' % n)))   # ← project_rules.json["patterns"]["guidePdf"] 를 안 읽음. 하드코딩.
        return g[0] if g else None
    for pat in (os.path.join(ROOT, '03_PDF', '**', '*각론%d*.pdf' % n),      # ← '03_PDF' 폴더명도 하드코딩
                os.path.join(ROOT, '**', '*각론%d*.pdf' % n)):
```
지금 CJ 프로젝트는 모든 단원의 storyboard/ops 가 project_rules.json 에 다 채워져 있어서(`_register()` 가 항상 절대경로로 넣어 줌) 이 폴백은 **지금은 실행되지 않습니다.** 하지만 새 프로젝트에서 Claude 의 분석이 어느 한 단원의 storyboard/ops 를 빠뜨리면(혹은 화면에서 사람이 단원을 새로 추가만 하고 경로를 안 채우면), 이 함수들이 **오류를 내는 대신 CJ 전용 파일명을 조용히 만들어서 찾습니다.** 지시하신 원칙 4("추측하지 않는다 — 없으면 오류/경고로 알린다")와 정면으로 어긋나는 지점이 아직 남아 있습니다. 게다가 `int(n)` 이라 단원 id 가 숫자가 아니면 이 폴백 자체가 파이썬 에러(`ValueError`)로 죽습니다 — C-1 과 같은 종류의 "숫자 id 전제".

특히 `guidePdf` 패턴은 **project_rules.json 스키마에는 있지만 코드가 아예 읽지 않는 죽은 설정값**입니다. `project_rules.json["patterns"]["guidePdf"]` 를 아무리 고쳐도 실제 PDF 찾기 동작은 전혀 안 바뀝니다.

### C-4. project_rules.json 의 `"prototype"` 항목이 스키마에만 있고 실제로 쓰이지 않음

`project_rules_io.py` 에 `prototype()` 함수가 있고 스키마 설명에도 "프로토타입(견본 단원) 정보" 라고 적혀 있지만, 코드 전체에서 이 함수를 부르는 곳이 **한 군데도 없습니다** (grep 으로 확인). 실제 "이미 분석해 둔 프로토타입 목록"은 `rules_io.list_protos(rid)` 가 `rules/cj_reading/proto_L*.json` 파일 존재 여부를 훑어서 만드는데, 이 값(`/api/proto` 응답의 `protos` 필드)조차 화면(app_page.py)에서 **한 번도 쓰이지 않습니다**(그려주는 코드가 없음). 처음 설계하신 "⑤ JSON에서 prototype 목록 생성 → ⑥ prototype 선택"은 지금 코드에 구현되어 있지 않고, 여전히 "사용자가 프로토 단원 번호를 손으로 입력"하는 방식입니다.

### C-5. 주석과 코드의 불일치 (오해 소지)

`recipes/cj_reading.py` 130~131번째 줄 주석:
```python
# 단원 수·이름은 교재마다 다르다. 코드에 박지 않고 **사용자가 지정한 두 폴더 안에서만**
# 찾아 project.json 에 적어 둔다. 그 뒤로는 그 파일이 기준이고, 사람이 고칠 수 있다.
```
실제로는 `project_rules.json` 이 기준인데 주석은 여전히 `project.json` 이라고 설명합니다. 동작에는 영향 없지만, 나중에 이 파일을 다시 여는 사람(또는 Claude)이 잘못 이해할 수 있습니다.

### C-6. project_rules.json 에 기록된 `project.root` 값이 지금 잘못돼 있음 (데이터 오염, 기능엔 무영향)

오늘 검증 과정에서 클라우드 샌드박스로 서버를 띄워 테스트하면서, `project_rules.json["project"]["root"]` 값이 실제 경로(`E:\00_works\2026\2026_cj_midd3_eng`)가 아니라 테스트용 샌드박스 경로(`/sessions/.../mnt/2026_cj_midd3_eng`)로 남아 있는 것을 발견했습니다. 코드 전체를 grep 해 보면 이 필드는 **쓰기만 하고 어디서도 읽지 않는** 표시용 값이라(실제 경로는 항상 `settings.json` 의 `root` 에서 새로 옴) 생성 결과에는 영향이 없지만, JSON 을 사람이 다시 볼 때 헷갈릴 수 있어 다음에 손볼 때 바로잡는 게 좋겠습니다. (이건 코드 문제가 아니라 데이터 값 문제라 이번 "코드 수정 금지" 지시와는 별개로, 원하시면 이 값만 따로 고쳐 드릴 수 있습니다.)

### C-7. check(ctx) 의 오류 메시지가 여전히 뭉뚱그려져 있음

지난번 지시하신 "단원별로 구체적인 오류"(`[project_rules.json 오류]\n3단원에 storyboard 정보가 없습니다.`) 형식은 아직 구현되지 않았습니다. 지금 `check(ctx)` 는 SND/SB_DIR/CONTENTS 세 개의 **프로젝트 전체 경로**만 보고, 단원별 누락은 검사하지 않습니다(예: 특정 단원만 storyboard 가 비어 있어도 여기서 걸리지 않고, 나중에 `read_import.sound()`/`syntax_sentences()` 안에서야 자료를 못 찾아 실패합니다).

---

## D. 추가 수정이 필요한 파일 (다음 작업 후보 — 지금은 코드를 고치지 않았습니다)

| 파일 | 수정 이유 | 수정 방향 |
|---|---|---|
| `recipes/cj_reading.py` | C-1: `proto_lesson()`/`proto_ops()`/`analyze()` 가 단원 id 를 int 로만 다룸 | 단원 id 를 문자열 그대로 다루도록 바꾸고, `project_rules.json["units"]` 에 실제로 있는 id 인지로 판단하게 바꿔야 함 |
| `proto_scan.py` | C-2: `scan_sound()` 의 `want = '%d과' % int(lesson)` 이 JSON/rules.json 을 무시함 | `scan()` 호출부에서 이미 구한 sheet 이름(단원별 `P.unit(n)['sheet']` 또는 `R('sound.sheet', …)`)을 인자로 받아 쓰도록 바꿔야 함 — `read_import.sound()` 와 같은 우선순위를 따르게 |
| `read_paths.py` | C-3: `storyboard()`/`ops()`/`guide_pdf()` 의 "없으면 CJ 이름으로 추측" 폴백이 원칙 4 와 충돌 | JSON 에 값이 없으면 조용히 만들지 말고, 단원별로 무엇이 빠졌는지 명시하는 오류/경고로 바꿔야 함. `guide_pdf()` 는 `project_rules_io.pattern('guidePdf', …)` 를 실제로 읽도록 연결해야 함 |
| `recipes/cj_reading.py` (check) | C-7: 단원별 누락 정보를 미리 알려주지 않음 | `check(ctx)` 를 단원 등록부(`P.UNITS`) 순회로 확장해, 어느 단원에 무엇이 비었는지 미리 알려주는 구조로 — 지시하신 오류 형식 참고 |
| `project_rules_io.py` / `app.py` / `app_page.py` | C-4: `prototype` 스키마가 죽어 있고, 프로토 선택이 JSON 기준 "목록"이 아님 | 이건 설계가 필요한 작업입니다 — project_rules.json 에 "프로토 후보로 쓸 만한 단원" 정보를 어떻게 기록하고, 화면이 그걸 어떻게 드롭다운으로 보여줄지부터 다시 정해야 합니다. 지금 바로 코드 방향을 정하기보다, 이 부분만 먼저 상의드리고 싶습니다 |
| `recipes/cj_reading.py` (주석) | C-5: 주석이 project.json 이라고 말함 | 주석만 project_rules.json 으로 고치면 됨(동작 변화 없음, 사소) |
| `project_rules.json` (데이터) | C-6: root 값 오염 | 코드가 아니라 데이터라, 원하시면 이 값만 바로 고쳐드릴 수 있음 |

---

## E. 수정하지 않아도 되는 파일 (그대로 둬도 되는 이유)

- **`read_gen.py`** — 이미 있던 `R()`/`load_rules()` 패턴이 오늘 추가한 `read_import.py` 의 것과 똑같은 모양으로 잘 동작 중. rules.json 연결이 이미 프로젝트 독립적(값이 없으면 코드 기본값).
- **`project_io.py`** — 이제 읽기 전용(마이그레이션 소스)으로만 쓰이고, 새로 쓰는 곳이 없음. 지우지 않고 둔 것 자체가 맞는 선택(사용자가 예전 project.json 을 직접 열어볼 수도 있고, 마이그레이션 소스로도 필요).
- **`rules_io.py`/`rules/<recipe>/rules.json`** — "생성 규칙"(팝업 번호, 파일명 틀, 측정 여백 등)을 다루는 책임이 명확히 분리돼 있고, project_rules.json 과 섞이지 않음. `values()` 공용 함수 추가도 적절함.
- **`read_import.py` 의 자료-해석 로직 자체**(PDF `'본문 해석'` 태그 찾기, 화자 표시 제거 정규식 등)와 **`proto_scan.py` 의 페이지 뼈대 스캔 로직**(`data-pop-idx`, `js-openPopBtn` 등) — 이건 "프로젝트마다 다른 정보"가 아니라 "CJ Reading 이라는 교재 형식 자체의 구조"이므로, 말씀하신 recipe 경계 안에 있는 게 맞습니다. 완전히 다른 교재 형식이 오면 project_rules.json 이 아니라 새 recipe 파일이 필요한 부분이고, 이건 처음부터 그렇게 설계하신 부분입니다.
- **`layout_edit.py`/`layout_io.py`/`read_measure.py`/`read_verify.py`/`regress.py`/`runner.py`/`app_page.py`(단원 목록 렌더링 부분)** — 오늘 범위에서 project.json/project_rules.json 관련 로직이 없고, 확인해 봐도 프로젝트 구조를 가정하는 하드코딩이 없음.

---

## F. 최종 목표 달성 여부

**2. 일부 프로젝트 종속성이 남아 있음.**

**이렇게 판단한 근거** — "현재 CJ 프로젝트에서 테스트 통과"가 아니라 "새 폴더 구조 + 새 단원 구조에서 코드 수정 없이 되는가"를 기준으로 봤습니다.

- 경로 4종 + 이름 패턴 4종 + 단원 목록은 실제로 project_rules.json 기준으로 동작합니다(B). 이 부분만 보면 상당히 잘 옮겨졌습니다.
- 하지만 **단원 id 가 전부 문자(비숫자)인 새 프로젝트**는 "프로토타입 분석" 기능을 아예 못 씁니다(C-1) — 이건 project_rules.json 을 아무리 정성껏 만들어도 코드 수정 없이는 피할 수 없는, 명백한 코드 종속성입니다.
- **음원 시트 이름 관례(`%d과`)가 다른 프로젝트**는 프로토타입 분석 단계에서 시트를 못 찾아 관련 규칙이 통째로 비게 됩니다(C-2) — 이것도 project_rules.json 으로 못 고치는 코드 문제입니다.
- 값이 빠졌을 때의 폴백(C-3)이 "오류로 알린다"가 아니라 "CJ 이름으로 추측한다"로 남아 있어, 지시하신 4번 원칙(추측 금지)이 완전히 지켜지지는 않았습니다.
- 처음 설계하신 "JSON에서 prototype 목록을 만들어 고른다"는 흐름(C-4)은 실제로는 구현되어 있지 않고, 여전히 사람이 프로토 단원 번호를 손으로 입력하는 방식입니다.

즉, **"경로·단원 정보"는 project_rules.json 화가 잘 됐지만, "프로토타입 선택·분석" 쪽은 아직 project_rules.json 과 분리되어 있고 CJ 전용 가정(숫자 id, `%d과`)이 코드에 남아 있습니다.** 새 프로젝트가 CJ 와 똑같이 "숫자 단원 + `N과` 시트" 관례를 따른다면 지금 상태로도 대체로 동작하겠지만, 말씀하신 "Unit 구조가 다르고 Special Lesson 도 없는, 완전히 다른 프로젝트"라면 최소 C-1·C-2 두 가지에서 코드 수정 없이는 막힙니다.

다음에 어느 것부터 손볼지는 상의가 필요합니다. 특히 C-4(프로토타입을 JSON 기준으로 만드는 것)는 설계를 다시 정해야 하는 부분이라, 코드를 만지기 전에 먼저 방향을 여쭙고 싶습니다.
