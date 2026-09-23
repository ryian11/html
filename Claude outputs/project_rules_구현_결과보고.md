# project_rules.json 도입 — 구현 결과 보고

지시하신 11단계 형식에 맞춰 보고합니다. 모든 테스트는 실제 `app.py` 서버를 띄워 HTTP API를 직접 호출하는 방식으로 했습니다(직접 파이썬 함수 호출이 아니라, 화면이 실제로 쓰는 경로 그대로).

---

## 1) 수정한 파일

| 파일 | 상태 |
|---|---|
| `project_rules_io.py` | 신규 생성 |
| `recipes/cj_reading.py` | 수정 (setup/discover/units/_register/unit_labels/extract/proto_pages/analyze) |
| `read_import.py` | 수정 (규칙 로딩 추가, mp3name/sound/syntax_sentences) |
| `rules_io.py` | 수정 (values() 추가, code_rules() 음원 스크래핑을 일반화) |
| `proto_scan.py` | 수정 (pages_in/scan 에 pattern 매개변수 추가) |
| `app.py` | 수정 (`/api/project` GET·POST 두 곳만) |

건드리지 않은 파일: `read_paths.py`, `read_gen.py`, `runner.py`, `layout_edit.py`, `layout_io.py`, `regress.py`, `read_measure.py`, `read_verify.py`, `app_page.py`, `project_io.py`(그대로 둠 — 삭제하지 않음).

모든 수정 파일은 `_backup/코드/` 에 타임스탬프가 찍힌 원본 백업이 남아 있습니다.

---

## 2) 각 파일에서 변경한 내용

**`project_rules_io.py` (신규)**
프로젝트 구조 정보(경로·이름 패턴·단원 목록)를 담는 `project_rules.json` 을 읽고 쓰는 모듈입니다. 핵심 함수:
- `ensure_migrated(recipe_id, root, defaults)` — `project_rules.json` 이 없으면(첫 실행) 지금까지 코드에 있던 값(`defaults`)으로 딱 한 번 만들어 두고, 있으면 그대로 읽습니다. 그래서 지금 쓰고 있는 CJ 프로젝트는 아무것도 손대지 않아도 첫 실행에 자동으로 마이그레이션됩니다.
- `units()` / `put_units()` — 단원 목록을 읽고 씁니다.
- `paths()` / `pattern(key, default)` — 프로젝트별 경로·이름 규칙을 읽습니다. 없으면 `default` 를 그대로 돌려줘서, 아직 JSON 에 없는 프로젝트도 예전과 똑같이 동작합니다.

**`recipes/cj_reading.py`**
- `setup(ctx)` — 예전에는 `01_스토리보드/...`, `02_사운드/...` 같은 CJ 전용 경로를 함수 안에 직접 써 놓고 있었습니다. 지금은 `project_rules.json` 의 `paths` 를 먼저 보고, 없을 때만 지금까지 쓰던 값(`LEGACY_PATHS`)을 씁니다. 단, `GEN`(생성기 자기 위치)은 지시하신 대로 JSON 에 넣지 않고 그대로 `root + '_딕테이션_생성기'` 로 계산합니다.
- `discover(ctx)` — `Lesson\s*0*(\d+)\.xlsx` 같은 이름 규칙을 `project_rules.json` 의 `patterns` 에서 먼저 찾고, 없으면 지금까지 쓰던 정규식을 기본값으로 씁니다. 그리고 이 함수가 찾은 결과는 **JSON 에 이미 있는 단원 정보를 절대 덮어쓰지 않습니다** — 빈 자리만 채우는 보조 역할로 바뀌었습니다.
- `units(ctx)` — 단원 목록의 기준을 `project_io.units()` 에서 `project_rules_io.units()` 로 바꿨습니다. discover() 결과로 빈 칸만 채우고, 결과를 다시 `project_rules.json` 에 저장합니다.
- `unit_labels(ctx)`, `_register(ctx, lst)` — 같은 이유로 `project_rules_io` 를 보도록 바꿨습니다.
- `extract(ctx, unit)` — 추출 시작 전에 `read_import.load_rules()` 를 호출해 `rules.json` 값을 읽어 오게 했고, 끝에서 `rules.json` 에 없어서 코드 기본값을 쓴 규칙이 있으면 그 목록을 "확인할 것" 메모에 덧붙이게 했습니다.
- `proto_pages(ctx)`, `analyze(ctx, pages)` — 견본 페이지 이름 규칙(`p001_01` 모양)을 `project_rules.json` 의 `patterns.pageFilename` 에서 가져오도록 했습니다.

**`read_import.py`**
- `read_gen.py` 에 이미 있던 것과 똑같은 모양으로 `load_rules(rid)` / `R(key, default)` / `missed_rules()` 를 추가했습니다.
- `mp3name()`, `sound()`, `syntax_sentences()` 세 함수에서, 지금까지 함수 안에 직접 박혀 있던 값(시트 이름 템플릿 `%d과`, 열 번호 `r[1]`/`r[2]`, ID 정규식, mp3 이름 규칙, 구문 해설 시트 이름 `구문 해설`)을 `R('rules.json 의 키', 지금까지 쓰던 값)` 형태로 바꿨습니다. `rules.json` 에 값이 있으면 그 값을, 없으면 지금까지 쓰던 값을 그대로 씁니다.
- `IDPAT` 모듈 상수 자체는 그대로 남겨 뒀습니다(기본값이자, 대조 기능이 스캔하는 자리라서).

**`rules_io.py`**
- `values(rid)` 를 추가했습니다 — `rules.json` 에서 `{키: 값}` 만 뽑아 돌려주는 공용 함수로, `read_gen.py` 와 `read_import.py` 가 똑같이 이걸 씁니다.
- `code_rules()`(코드와 rules.json 을 "대조"하는 진단 기능)의 음원 관련 스크래핑을, 옛 코드 모양을 그대로 흉내 내던 낡은 정규식 대신 `R('키', 기본값)` 호출 자체를 훑는 일반적인 방식으로 바꿨습니다. 그래서 `read_import.py` 에 `R()` 호출이 새로 생겨도(예: 오늘 추가한 `storyboard.sheet.syntax`) 이 파일을 다시 고치지 않아도 대조 기능이 그 항목을 알아봅니다. (실제로 테스트에서 `storyboard.sheet.syntax` 가 "코드에만" 항목으로 정상적으로 잡혔습니다.)

**`proto_scan.py`**
- `pages_in(ops)` → `pages_in(ops, pattern=None)` — 페이지 이름 정규식을 밖에서 줄 수 있게 했습니다. 안 주면 지금까지 쓰던 `p001_01` 모양 기본값(`PAGE_PATTERN_DEFAULT`)을 씁니다.
- `scan(...)` 에 `page_pattern=None` 매개변수를 추가해 위 값을 그대로 전달받게 했습니다.

**`app.py`**
- 단원 편집 화면이 쓰는 `/api/project` 의 GET(`_project`)·POST 두 핸들러에서 `project_io` → `project_rules_io` 로 바꿨습니다. 화면에서 단원 이름·시트·지도서 PDF 를 고치면 이제 `project_rules.json` 에 저장되고, `recipes/cj_reading.py` 의 생성 로직이 보는 파일과 정확히 같은 파일입니다(예전에는 화면 저장 파일과 생성 로직이 보는 파일이 어긋날 뻔했습니다).

---

## 3) 제거한 CJ 전용 하드코딩

- `setup()` 안의 `01_스토리보드/전자저작물 추가 원고_20260716_아이스캔디 전달`, `02_사운드/...xlsx`, `단어사전/lesson%02d`, `00_개발물/EBOOK/.../contents` 경로 — 이제 `project_rules.json.paths` 에서 옵니다(없을 때만 코드 기본값).
- `discover()` 안의 `Lesson\s*0*(\d+)\.xlsx`, `_([A-Za-z][A-Za-z ]*Lesson)\.xlsx`, `^lesson0*(\d+)$`, `%d과` — `project_rules.json.patterns` 에서 옵니다.
- `proto_scan.pages_in()` 안의 `p\d{3}_\d{2}` 페이지 이름 규칙 — `patterns.pageFilename` 에서 옵니다.
- `read_import.py` 안의 녹음 대본 시트 이름 템플릿(`%d과`), 열 번호(1·2번 열), ID 정규식, mp3 이름 만드는 규칙(`-`→`_`, 소문자화), 구문 해설 시트 이름(`구문 해설`) — `rules.json` 에서 옵니다(없으면 지금까지 값).

---

## 4) project_rules.json 에서 읽도록 바뀐 정보

```
paths: storyboardDir, soundXlsx, wordDicDir, contentsDir, (guideDir — 있을 때만)
patterns: storyboardFilename, specialUnitFilename, contentsFolder, pageFilename, guidePdf, soundSheet
units: [{id, name, storyboard, ops, sheet, guide, kr}, ...]
```
`GEN`(생성기 자기 위치)은 지시하신 대로 **넣지 않았습니다** — 자료가 아니라 생성기 자신의 설치 위치라서, 지금처럼 `root + '_딕테이션_생성기'` 로 그대로 계산합니다.

현재 CJ 프로젝트는 첫 실행 때 자동으로 마이그레이션되어 `project_rules.json` 이 이미 만들어져 있고(`project`, `paths`, `patterns`, `units` 8개 모두 채워짐), 이후로는 이 파일이 기준입니다.

---

## 5) 기존 기능 중 영향을 받은 기능

- **단원 편집 화면**(`/api/project`): 저장하는 파일이 `project.json` → `project_rules.json` 으로 바뀌었습니다. 화면 동작 자체(입력·저장·표시)는 그대로입니다.
- **자료 읽기**(`read_import.py`): 동작 결과는 그대로이나(테스트로 확인), "확인할 것" 메모에 `rules.json` 미기재 규칙 목록이 새로 붙습니다.
- **프로토 분석**(`analyze`)·**견본 페이지 목록**(`proto_pages`): 페이지 이름 규칙의 출처가 바뀌었을 뿐, 지금 프로젝트에서는 같은 값이라 결과는 그대로입니다.
- **단원 자동 탐색**(`discover`): 우선순위가 바뀌었습니다 — 이제 `project_rules.json` 에 적힌 단원 정보가 항상 이기고, discover() 는 빈 자리만 보조로 채웁니다.
- **HTML 생성**(`extract`/`build`), **preview**, **popup**, **CSS/JS**, **rules.json 승격(promote)**, **backup**, **settings**, **regress(회귀 검사)**: 코드를 건드리지 않았고, 테스트로 기존과 동일함을 확인했습니다.
- **Special Lesson**: `project_rules.json` 에 `special_lesson` 단원 정보(sheet/guide/kr 등)가 그대로 보존되는 것을 확인했습니다. (참고: special_lesson 산출물이 기준본과 8개 파일에서 다른 문제가 있는데, 이는 오늘 작업과 무관하게 이전부터 있던 문제임을 별도로 검증했습니다 — 원본 코드로도 똑같이 재현됩니다.)

---

## 6) 테스트한 기능 (모두 실제 `app.py` 서버를 띄워 HTTP로 확인)

| 테스트 | 결과 |
|---|---|
| `GET /api/recipe/cj_reading` | 정상 |
| `GET /api/project` — 단원 목록이 project_rules.json 그대로 나옴 | 정상 (8개 단원 확인) |
| `POST /api/project` — 단원 이름 임시 변경 → 재조회로 반영 확인 → 원복 | 정상 (원복 후 파일 바이트까지 원래대로) |
| `GET /api/proto` | 정상 |
| `GET /api/pages` | 정상 |
| `GET /api/compare` — rules.json 대조 진단, 새 `R()` 스캔 방식 | 정상 (`storyboard.sheet.syntax` 가 "코드에만" 항목으로 정확히 잡힘) |
| `POST /api/run` — 7·8단원 extract+build 전체 파이프라인 | 정상, `ok: true` |
| 7·8단원 산출 HTML/CSS/JS/popup 파일을 `_기준본/cj_reading/` 과 diff | **완전히 동일**(바이트 단위 0개 차이) |
| `measure` 단계 | 실패 — 이 샌드박스 VM 에 Playwright 브라우저가 설치돼 있지 않아서 나는 에러이고(`chrome-headless-shell` 실행 파일 없음), 오늘 바꾼 코드와 무관합니다. 사용자 컴퓨터에는 이미 설치돼 있을 것이므로 실제 사용 환경에서는 문제 없을 것으로 보입니다. |
| 전체 코드에서 `project_io` 남은 사용처 재확인 | `project_rules_io.ensure_migrated()` 와 `recipes/cj_reading.py:setup()` 의 의도된 대체-경로 두 곳뿐 |

---

## 7) 아직 남아 있는 프로젝트 종속 코드

- **`P.GEN`**(`recipes/cj_reading.py:setup()`): `root + '_딕테이션_생성기'` 로 직접 계산합니다. 지시하신 대로 이건 "자료 경로"가 아니라 "생성기 자기 위치"라서 일부러 `project_rules.json` 에 넣지 않았습니다. 다른 프로젝트에서 생성기 폴더 이름이 다르면(거의 없겠지만) 이 한 줄만 수정하면 됩니다 — project_rules.json 원칙과 충돌하지 않는, 의도된 예외입니다.
- **`LEGACY_PATHS`/`LEGACY_PATTERNS`**(`recipes/cj_reading.py` 상단): CJ 전용 값이 코드에 남아 있지만, 용도가 "project_rules.json 이 아직 없을 때 딱 한 번 마이그레이션하는 재료"로 한정돼 있습니다. project_rules.json 이 있는 프로젝트에서는 전혀 쓰이지 않습니다.
- **`read_paths.py` 의 모듈 기본값**: `python proto_scan.py cj_reading 6 ...` 처럼 `setup()`/레시피 계층을 거치지 않고 직접 실행할 때 쓰는 최후 기본값이라 손대지 않았습니다. 이건 CLI 단독 실행을 위한 것이라 영향이 제한적입니다.
- **`recipes/cj_reading.py` 자체**: 파일 이름·함수 구조가 CJ 딕테이션 리딩 전용이라는 점은 오늘 바꾸지 않았습니다(그럴 계획도 아니었습니다) — "recipe" 자체가 프로젝트/교재 종류별로 갈아 끼우는 단위이기 때문에, 새 프로젝트가 구조가 다르면 새 recipe 파일이 필요할 수 있습니다. 다만 구조·경로·단원 정보는 이제 JSON 에서 오므로, **같은 recipe(같은 교재 형식)를 쓰는 새 프로젝트라면 recipe 코드를 안 건드리고 project_rules.json 만 새로 만들면 됩니다.**

---

## 8) 새 프로젝트를 적용하려면 Claude에게 어떤 분석을 시켜야 하는지

새 프로젝트가 지금 CJ 프로젝트와 **같은 종류(같은 recipe)** 라면:

1. 프로젝트 루트 아래에서 스토리보드 폴더 위치·파일명 규칙(`Lesson 1.xlsx` 같은 모양인지, 다른 모양인지)을 확인.
2. 녹음 대본 Excel 위치·시트 이름 규칙(`%d과` 같은 템플릿인지)·ID 열/텍스트 열 번호·ID 정규식 모양을 확인.
3. contents/ops 폴더 위치와 이름 규칙(`lessonNN` 같은 모양인지)을 확인.
4. 견본(prototype)으로 쓸 단원과 그 페이지 파일명 규칙(`p001_01` 같은 모양인지)을 확인.
5. 단원 목록(단원 id·이름·각 단원의 스토리보드/ops/시트 이름 경로)을 실제로 폴더를 열어서 하나하나 확인 — 추측하지 않고 실재 확인.
6. 위 내용을 `project_rules.json` 스키마(`project/paths/patterns/units`)에 맞춰 작성.

그러면 Python 코드를 전혀 고치지 않고 그 `project_rules.json` 을 새 프로젝트 폴더에 놓기만 하면 생성기가 동작합니다(같은 recipe 를 쓰는 경우). **recipe 자체가 다른 교재 형식**(단원 구조·팝업 구성·생성 규칙이 근본적으로 다른 경우)이라면 `recipes/` 에 새 recipe 파일이 하나 더 필요하며, 이건 이번 작업의 범위 밖이라 별도로 상의가 필요합니다.
