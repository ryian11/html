# 정리 감사 (raw) — `_딕테이션_생성기`

- 대상: `E:\00_works\2026\2026_cj_midd3_eng\_딕테이션_생성기` (Windows, git 저장소)
- 조사일: 2026-09-22 / **읽기 전용** (수정·삭제·이동 없음)
- git 커밋 2개뿐: `04068ad` 2026-09-21 16:08 "현재 작업 버전 전체 업로드", `a65e9a2` 2026-09-22 12:43 "project_rules 구조 개선 및 문서 업데이트"
- `git status` 수정분은 `_backup/measure/*.py` 뿐 (과거 스냅샷, 본 코드 아님)
- **`.gitignore` 없음** → `__pycache__`, `app.log`, `_backup/` 까지 전부 git 추적 중 (추적 파일 514개)

---

## 0. 한눈에 보는 수치

| 항목 | 수 |
|---|---|
| 추적 파일 전체 | 514 |
| `.py` 전체 | **98** |
| ├ 실제 실행 코드 | 16 |
| ├ 레거시 코드 | 13 (`_옛도구/` 12 + `read_run.py`) |
| ├ 생성 결과물(GENERATED) | 21 (`단원자료/`) |
| └ 백업 스냅샷 | 48 (`_backup/`) |
| 비-`.py` 추적 파일 | 452 (대부분 `_backup/산출물` 244 + `_기준본` 63) |

폴더 용량: `_backup` 2.9M(352개) · `_기준본` 412K(63개) · `단원자료` 288K(34개) · `_옛도구` 104K(15개) · `__pycache__` 192K(11개) · `문서` 96K(5개) · `docs` 56K(4개) · `recipes` 44K · `rules` 24K

---

## 1. 작업 1 — 전체 인벤토리

### 1-1. 최상위 구조

```
_딕테이션_생성기/
├ app.py app_page.py                 화면(로컬 HTTP 서버 + HTML 문자열)
├ runner.py  recipes/cj_reading.py   일반 파이프라인 껍데기 + 레시피
├ read_paths.py read_import.py read_gen.py read_measure.py read_verify.py
├ read_run.py                        (옛 CLI 한 방 실행 — 지금은 아무도 안 부름)
├ layout_io.py layout_edit.py        layout<N>.json 읽기/쓰기 + 설정 패널
├ rules_io.py proto_scan.py          프로토 분석 → rules/
├ project_io.py project_rules_io.py  project.json / project_rules.json
├ regress.py                         _기준본 과 바이트 비교
├ project.json project_rules.json settings.json   설정 3종
├ readsmart.tpl                      Read Smart 도입 페이지 템플릿
├ HTML생성기.vbs                     app.py 실행 런처(Windows, UTF-16)
├ app.log                            실행 로그(추적 중)
├ README_runner.md                   runner 사용설명서(루트에 홀로)
├ docs/        PROJECT·RULES·PROGRESS·ISSUES (2026-09-21, 현행 기준 문서)
├ 문서/        2026-09-15~17 옛 인수인계/규칙/진행 문서 5개
├ .claude/skills/html-generator/SKILL.md
├ rules/cj_reading/  proto_L3·L6·Lspecial_lesson.json + rules.json
├ 단원자료/     data<N>.py · scrolls/popscroll/krlayout<N>.py · layout<N>.json (+__pycache__)
├ _기준본/cj_reading/{7,8,special_lesson}/  회귀 기준본 (HTML/CSS/JS/popup)
├ _backup/     .지움시험 · layout/ · measure/ · 코드/ · 산출물/ · 개발물에서_옮김/
├ _옛도구/     딕테이션 초기 도구 + 옛 측정/검증/레이아웃 (읽어주세요.txt 있음)
└ __pycache__/ .pyc 11개 (추적 중)
```

### 1-2. 폴더별 내용

| 폴더 | 내용 | 대표 파일 | 판단 |
|---|---|---|---|
| `_backup/코드/` | 50개 `.bak` — 코드/JSON 수동 백업(2026-09-16~22). **코드가 만들지 않는다**(`.bak` 를 쓰는 코드 없음) = 사람/세션이 손으로 떠 둔 것 | `app.py.20260922_015655.bak`, `_patch_app.py.bak`, `project_rules.json.stale1.bak` | DELETE 후보(단, 09-21 이전 것은 git 이전 시기) |
| `_backup/산출물/` | 244개 — 단원 7/8/special 의 타임스탬프 출력 스냅샷. `runner.backup()` 이 자동 생성 | `cj_reading/7/20260917_095746/p122_02.html` | GENERATED / DELETE 후보(오래된 것) |
| `_backup/measure/` | 45개 — 측정값(`scrolls/popscroll/krlayout`) 스냅샷. `cj_reading._backup_measured()` 가 자동 생성 | `krlayout8_20260922_004834.py` | GENERATED |
| `_backup/layout/` | 9개 `layout<N>_<시각>.json` — `layout_edit._backup()` 자동 생성 | `layout7_20260916_071146.json` | GENERATED |
| `_backup/개발물에서_옮김/` | 3개 — 개발물 폴더에 있던 lesson06 측정값을 옮겨 둔 것 | `lesson06-krlayout6.py` | LEGACY |
| `_backup/.지움시험` | 0바이트 빈 파일 | — | DELETE 후보(확신 높음) |
| `_기준본/` | 63개 — 단원 7/8/special 의 회귀 기준본. `regress.py save` 가 만들고 `check` 가 비교 | `_기준본/cj_reading/8/p140_02.html` | KEEP (정리 대상 아님) |
| `단원자료/` | 34개 — 추출 결과 `data<N>.py`(1~8, special), 측정 결과 `scrolls/popscroll/krlayout<N>.py`, 사람이 고치는 `layout<N>.json`(7·8·special) | `data7.py`(“read_import.py 가 만든 초안입니다”) | GENERATED(+ layout*.json 만 KEEP) |
| `문서/` | 5개 md(09-15~09-17). 딕테이션 인수인계·Reading 규칙·6단원 결과·진행기록·파이프라인 설명서 | `00_작업인수인계.md` | LEGACY / MOVE |
| `docs/` | 4개 md(09-21). SKILL.md 가 “먼저 읽으라”고 지정한 현행 기준 문서 | `PROJECT.md` | KEEP |
| `.claude/` | `skills/html-generator/SKILL.md` 1개 | — | KEEP |
| `recipes/` | `cj_reading.py` + `__pycache__/cj_reading.cpython-310.pyc` | — | KEEP(+pyc DELETE) |
| `rules/cj_reading/` | `proto_L3/L6/Lspecial_lesson.json`(프로토 분석 결과) + `rules.json`(승격된 확정 규칙) | — | KEEP |
| `__pycache__/` | 11개 `.pyc` (310 / 313 혼재) | `runner.cpython-313.pyc` | DELETE 후보(확신 매우 높음) |

### 1-3. `.gitignore`

**없음.** 그래서 `__pycache__/*.pyc` 22개(루트 11 + `recipes` 1 + `단원자료` 10), `app.log`, `_backup/` 352개가 전부 버전관리 안에 들어와 있다. 추적 파일 514개 중 **약 420개가 산출물/백업/캐시**다.

---

## 2. 작업 2 — Python 파일 전수표 (98개)

### 2-1. 루트 + recipes (17개)

| 파일 | 사용 | 호출하는 곳 | 역할 | 분류 | 삭제 가능 |
|---|---|---|---|---|---|
| `app.py` | O | `HTML생성기.vbs`(`app.py --port 8765 --no-open`), CLI `py app.py` | 로컬 HTTP 서버 · 화면 API 전부 | 실제 실행 코드 | X |
| `app_page.py` | O | `app.py:573 from app_page import PAGE` | 화면 HTML/JS 문자열 1개 | 실제 실행 코드 | X |
| `runner.py` | O | `app.py:16`, `layout_edit.py:100,208`, `regress.py:47,95,125`, `proto_scan.py:336`, `cj_reading.py:340,372` + 자체 CLI | 레시피 로드/단계 실행/백업/설정 | 실제 실행 코드 | X |
| `recipes/cj_reading.py` | O | `runner.load_recipe()` 가 `importlib` 로 (`runner.py:144`) | CJ Reading 레시피: setup/discover/units/extract/build/measure/verify/analyze/preview | 실제 실행 코드 | X |
| `read_paths.py` | O | `read_gen:11`, `read_import:21`, `read_measure:19`, `read_verify:7`, `read_run:11`, `app.py:428`, `proto_scan:336`, `cj_reading:67,115,153,197,236,262,397` | 경로 상수(ROOT/SB_DIR/SND/CONTENTS…). 레시피 `setup()` 이 값을 덮어씀 | 실제 실행 코드 | X |
| `read_import.py` | O | `cj_reading.py:261` (① 추출), `proto_scan.py:304` | 원고(엑셀/PDF) → `data<N>.py` | 실제 실행 코드 | X |
| `read_gen.py` | O | `cj_reading.py:243,315,330,354`, `read_measure:20`, `read_verify:8`, `read_run:12`, `app.py:525`(버전 로그) | `data<N>.py` → HTML/CSS/JS/팝업 | 실제 실행 코드 | X |
| `read_measure.py` | O | `cj_reading.py:342,349`, `read_run:60`, `regress.py:127` | Playwright 로 재서 `scrolls/popscroll/krlayout<N>.py` 생성 | 실제 실행 코드 | X |
| `read_verify.py` | O | `cj_reading.py:379`, `read_run:78` | 산출물 검증(실패 시 종료코드 1) | 실제 실행 코드 | X |
| `read_run.py` | **X** | 저장소 전체에서 **아무도 import 하지 않음**. 유일한 언급이 `_옛도구/gen6.py:4` (그 자체가 구버전 안내문) | 백업→생성→측정→재생성→검증 CLI. `runner.py` + `recipes/cj_reading.py` 가 같은 일을 함 | **레거시 코드** | △ (기능 중복, `runner.py` 로 완전 대체됨. 단 `ops/_backup/<시각>` 옛 백업 방식이 여기만 남아 있음) |
| `layout_io.py` | O | `layout_edit.py:18`, `read_import.py:745,783`, `runner.GEN_MODULES` 재로드 목록 | `layout<N>.json`(+옛 `.py`) 읽기/쓰기 | 실제 실행 코드 | X |
| `layout_edit.py` | O | `app.py:235,340,350`, `cj_reading.py:478`(preview) | 설정 패널 살림, layout 저장/부분 재생성 | 실제 실행 코드 | X |
| `rules_io.py` | O | `app.py:238,440,454,462`, `proto_scan.py:21` | `rules/` 파일 살림 + 코드와 규칙 대조 리포트 | 실제 실행 코드 | X |
| `proto_scan.py` | O | `rules_io.py:166`, `cj_reading.py:440,462` + 자체 CLI | 견본 페이지 분석 → `proto_L<N>.json` | 실제 실행 코드 | X |
| `project_rules_io.py` | O | `app.py:268,421`, `cj_reading.py` 9곳 | `project_rules.json` 읽기/쓰기 + 마이그레이션 | 실제 실행 코드 | X |
| `project_io.py` | △ | `project_rules_io.py:160`(ensure_migrated 안), `cj_reading.py:90`(project_rules 비었을 때 폴백) | `project.json` 읽기/쓰기 | **향후 필요하지만 현재 직접 호출 안 됨**(마이그레이션·폴백 전용) | △ (`project.json` 과 한 쌍으로만 의미 있음) |
| `regress.py` | O | `app.py:331,333,334` (`/api/regress`), 화면 버튼 “기준본과 견주기/지금 결과를 기준본으로”(`app_page.py:193,491`) + 자체 CLI | `_기준본` 과 sha1 비교 | 실제 실행 코드 | X |

**엔트리포인트 도달 경로**
```
HTML생성기.vbs → pythonw app.py --port 8765
  app.py ── runner.load_recipe('cj_reading') → recipes/cj_reading.py
            └ 단계 실행: extract(read_import) → build(read_gen) → measure(read_measure) → verify(read_verify)
            └ /api/layout,/api/regen → layout_edit → layout_io
            └ /api/analyze,/api/promote,/api/compare → proto_scan / rules_io
            └ /api/project → project_rules_io (→ project_io 는 최초 마이그레이션 때만)
            └ /api/regress → regress → _기준본
```
`read_run.py` 는 이 그림 어디에도 들어오지 않는다.

`if __name__ == '__main__'` 보유: `app.py`, `runner.py`, `read_import.py`, `read_gen.py`, `read_measure.py`, `read_verify.py`, `read_run.py`, `layout_edit.py`, `proto_scan.py`, `rules_io.py`, `regress.py`. 이 중 문서(`README_runner.md`)에 CLI 사용례가 실제로 적힌 것은 `runner.py`·`regress.py`·`app.py` 뿐이다.

### 2-2. `_옛도구/` (12개 .py + geo.js + txt 2)

`_옛도구/읽어주세요.txt` 가 직접 “여기 있는 것은 지금 생성기가 부르지 않는 파일입니다 … 지우지 않고 남겨 둡니다. 딕테이션 레시피를 만들 때 참고할 수 있습니다.” 라고 밝히고 있다. 전수 확인 결과 실제로 **저장소 어디에서도 import 되지 않는다.**

| 파일 | 사용 | 호출하는 곳 | 역할 | 분류 | 삭제 가능 |
|---|---|---|---|---|---|
| `build3.py` | X | 없음 | lesson08 dic1 input 폭/scrollTop 계산. `exec(open('/home/claude/cj/measure/opt.py'))` — **컨테이너 절대경로**라 지금 PC 에서 실행 불가 | 레거시 코드 | △(딕테이션 레시피 참고용) |
| `dlg.py` | X | 없음 | 대화형 Dictation 생성. `sys.path.insert('/home/claude/cj')` | 레거시 코드 | △ |
| `gen.py` | X | 없음 | Dictation 팝업 생성기(lesson03 기준) | 레거시 코드 | △ |
| `rd.py` | X | 없음 | Reading형 Dictation 생성 | 레거시 코드 | △ |
| `src.py` | X | 없음 | 원고 추출 공통(위 3개가 씀). 엑셀 경로가 `/mnt/user-data/uploads/...` 하드코딩 | 레거시 코드 | △ |
| `opt.py` | X | 없음 | 옛 측정(Playwright async) → 지금은 `read_measure.py` | 레거시 코드 | O |
| `verify.py` | X | 없음 | 옛 검증 → 지금은 `read_verify.py` | 레거시 코드 | O |
| `gen6.py` | X | 없음 | 13줄짜리 안내 스텁. “gen6.py 는 read_gen.py 로 대체되었습니다” 를 출력할 뿐 | 레거시 코드 | **O (확신 높음)** |
| `layout7.py` | X | 없음 | 7단원 지면 구조 → `단원자료/layout7.json` 이 대신함 | 레거시 코드 | △(원본 근거 자료) |
| `layout8.py` | X | 없음 | 8단원 지면 구조 → `layout8.json` 이 대신함 | 레거시 코드 | △ |
| `kr7_해석.py` | X | 없음 | 7단원 해석 → `layout7.json` 의 `kr` 로 흡수 | 레거시 코드 | △(사람이 쓴 번역 원본) |
| `kr8_해석.py` | X | 없음 | 8단원 해석 → `layout8.json` 의 `kr` 로 흡수 | 레거시 코드 | △ |
| (`geo.js`, `kr6_확인.txt`, `읽어주세요.txt`) | X | 없음 | 딕테이션 보조 스크립트 · 6단원 확인 메모 · 폴더 설명 | 레거시 | △ |

### 2-3. `단원자료/` (21개 .py) — 전부 생성 결과물

| 파일군 | 사용 | 누가 읽나 / 누가 만드나 | 분류 |
|---|---|---|---|
| `data1.py` `data2.py` `data3.py` `data4.py` `data5.py` `data6.py` `data7.py` `data8.py` `dataspecial_lesson.py` | O(읽힘) | 만드는 쪽: `read_import.py`(파일 머리에 “read_import.py 가 만든 초안입니다”) · 읽는 쪽: `read_gen.load_lesson()` 이 `importlib.import_module('data%s')` 로 (`read_gen.py:64`) | **GENERATED**(소스 아님. 단, `# ???` 를 사람이 손보는 반(半)수작업 산출물) |
| `scrolls6/7/8/special_lesson.py` | O | 만드는 쪽 `read_measure.py`, 읽는 쪽 `read_gen.py:80` | GENERATED |
| `popscroll6/7/8/special_lesson.py` | O | 〃 | GENERATED |
| `krlayout6/7/8/special_lesson.py` | O | 〃 (머리에 “직접 고치면 다음 측정 때 덮어쓴다”) | GENERATED |

※ `layout7.json` `layout8.json` `layoutspecial_lesson.json` 은 **사람이 정하는 입력값**이라 GENERATED 가 아니다(KEEP). 단원 6 에는 `layout6.json` 이 없고 `krlayout6.py` 만 있다 — 6단원은 layout 편집 UI 이전 시기 산출물.

### 2-4. `_backup/` (48개 .py)

| 파일군 | 개수 | 만든 주체 | 분류 |
|---|---|---|---|
| `_backup/measure/krlayout7_*.py` (6) `krlayout8_*.py` (6) `krlayoutspecial_lesson_*.py` (3) | 15 | `recipes/cj_reading.py:361 _backup_measured()` | 백업(자동) |
| `_backup/measure/popscroll7_*.py` (6) `popscroll8_*.py` (6) `popscrollspecial_lesson_*.py` (3) | 15 | 〃 | 백업(자동) |
| `_backup/measure/scrolls7_*.py` (6) `scrolls8_*.py` (6) `scrollsspecial_lesson_*.py` (3) | 15 | 〃 | 백업(자동) |
| `_backup/개발물에서_옮김/lesson06-{krlayout6,popscroll6,scrolls6}.py` | 3 | 사람이 개발물 폴더에서 옮김 | 백업(수동)/LEGACY |

---

## 3. 작업 3 — 파일 정리 대상 분류

### KEEP
- 코드 16개(§2-1 의 `read_run.py` 제외 전부) + `recipes/cj_reading.py`
- `project_rules.json`, `settings.json`, `readsmart.tpl`, `HTML생성기.vbs`
- `rules/cj_reading/*.json` 4개
- `단원자료/layout7.json` `layout8.json` `layoutspecial_lesson.json`
- `docs/*.md` 4개, `.claude/skills/html-generator/SKILL.md`
- `_기준본/` 63개 — **정리 대상 아님.** 용도: `regress.py check` 가 “지금 생성 결과 = 기준본” 을 sha1 로 확인하는 회귀 기준. 코드를 고칠 때마다 안전망이 되므로 유지.

### MOVE
| 대상 | 어디로 | 이유 |
|---|---|---|
| `README_runner.md` (14KB) | `docs/RUNNER.md` 또는 `docs/` 아래 | 루트에 문서가 하나만 떠 있고, SKILL.md 는 `docs/` 4종만 “먼저 읽을 문서”로 지정. 내용은 여전히 유효(runner CLI·API 목록) |
| `문서/*.md` 5개 | `docs/archive/` (또는 `문서/`를 `docs/archive/` 로 통째 개명) | 09-15~17 판. 현행 `docs/` 와 두 벌이 공존해 어느 쪽이 기준인지 안 보임 |
| `단원자료/layout*.json` | (선택) `설정/` 같은 입력 전용 폴더 | 사람이 고치는 입력값이 기계 생성물과 같은 폴더에 섞여 있음 |

### MERGE
| 대상 | 무엇과 | 이유 |
|---|---|---|
| `project.json` | `project_rules.json` | `project_rules.json.units` 가 `project.json.units` 를 **글자 하나까지 그대로** 담고 있다(1~8 + special_lesson, storyboard/ops/sheet/guide 전부 동일). `project_io` 는 `ensure_migrated()` 와 폴백에서만 쓰임 → 마이그레이션 완료 선언 후 한 벌로 합치는 것이 맞음 |
| `문서/README_Reading파이프라인.md` + `문서/HTML생성기-진행기록.md` | `docs/PROJECT.md` / `docs/PROGRESS.md` | 같은 주제가 두 벌 |
| `문서/10_Reading본문페이지_규칙.md` | `docs/RULES.md` | 3단원 프로토 분석 규칙 — 현행 RULES.md 의 근거 문서 |

### DELETE 후보
| 대상 | 개수/용량 | 이유 | 확신 |
|---|---|---|---|
| `__pycache__/`, `recipes/__pycache__/`, `단원자료/__pycache__/` | .pyc 22개 추적, 192K+ | 실행 시 자동 재생성. 310/313 두 버전이 섞여 있어 오히려 혼란. `.gitignore` 에 넣어야 함 | **매우 높음** |
| `app.log` | 12KB | 실행 로그. `app.py:534` 가 append 만 함. 추적할 이유 없음 | **매우 높음** |
| `_backup/.지움시험` | 0바이트 | 삭제 권한 시험용 빈 파일 | **매우 높음** |
| `_backup/코드/_patch_*.bak` | 6개 | 2026-09-22 00:34~00:37 에 만든 패치 작업 임시본. 같은 날 커밋(`a65e9a2`)으로 대체됨 | 높음 |
| `_backup/코드/project_rules.json.stale1.bak`, `.stale2.bak` | 2개 | 파일 이름 자체가 “stale” | 높음 |
| `_backup/산출물/` 오래된 타임스탬프 | 244개 중 각 단원 최신 1개만 남기면 ~200개 / 1.2M 절감 | `runner.backup()` 이 실행할 때마다 쌓임. 같은 내용을 `_기준본` 이 이미 보관 | 중간(최신 1~2벌은 남길 것) |
| `_backup/measure/` 오래된 스냅샷 | 45개 중 단원별 최신 1개만 남기면 36개 절감 | 〃 (`_backup_measured()` 자동) | 중간 |
| `_backup/코드/` 나머지 42개 `.bak` | 1MB | git 이 같은 역할을 함 | **낮음 — 주의**: git 최초 커밋이 **2026-09-21 16:08** 이라, 그 이전 날짜(`*.20260916_*`, `*.20260917_*`) 백업은 **git 에 없는 유일본**이다. 09-21 이후 것만 지워야 안전 |
| `_옛도구/gen6.py` | 13줄 | 안내문만 출력하는 스텁. 게다가 그 안내가 가리키는 `read_run.py` 도 이미 안 쓰임 | 높음 |
| `read_run.py` | 91줄 | `runner.py`+레시피가 완전 대체. 아무도 import 안 함 | 중간(먼저 LEGACY 표시 → 한 사이클 뒤 삭제 권장) |
| `project.json` + `project_io.py` | 3.5KB + 62줄 | 위 MERGE 참고. 마이그레이션이 끝났음을 확인한 뒤 | 중간 |

### LEGACY (지우진 않되 명확히 표시)
- `_옛도구/` 전체 15개 — 이미 `읽어주세요.txt` 로 표시돼 있음. **다만 폴더명이 아닌 코드 쪽에는 표시가 없다**: `read_run.py` 가 루트에 그대로 있어 신규 작업자가 진입점으로 오해할 수 있음.
- `read_run.py` — 파일 머리에 “(구버전) runner.py 를 쓰세요” 한 줄이 필요.
- `project.json` / `project_io.py` — “마이그레이션 전용” 표시 필요.
- `_backup/개발물에서_옮김/` 3개.
- `문서/` 5개.

### GENERATED (다시 만들 수 있음, 소스 아님)
- `단원자료/data<N>.py` 9개 ← `read_import.py`
- `단원자료/{scrolls,popscroll,krlayout}<N>.py` 12개 ← `read_measure.py`
- `_backup/measure/` 45개, `_backup/layout/` 9개, `_backup/산출물/` 244개
- `__pycache__` 22개, `app.log`
- `rules/cj_reading/proto_L*.json` 3개 ← `proto_scan.py` (단 `rules.json` 은 사람이 승격시킨 것 = KEEP)
- `_기준본/` 63개 ← `regress.py save` (재생성 가능하지만 **기준**이므로 KEEP)

### USER DATA
- 이 폴더 안에는 없음. 실제 교재 자료는 한 단계 위 `2026_cj_midd3_eng/` 의 `01_스토리보드/`, `02_사운드/`, `03_PDF/`, `00_개발물/EBOOK/.../contents/` 에 있고, 생성기는 그곳을 **읽고 `contents/lessonNN/ops` 에 쓴다**. 정리 대상 아님. 존재만 기록.

---

## 4. 작업 4 — 이름 정리 후보

### 4-1. `read_*.py` 접두사
`read_` 는 “**Read**ing 지문 페이지”라는 뜻인데, 프로그래밍에서 `read_` 는 보통 “읽기”를 뜻한다. 그래서 `read_gen.py`(읽기 생성?) `read_import.py`(읽기 가져오기?) 처럼 **접두사와 동사가 충돌**한다. 특히 `read_paths.py` 는 “경로를 읽는 모듈”로 오해되기 쉽지만 실제로는 **경로 상수 테이블**이다.

| 지금 | 실제 역할 | 이름이 맞나 | 제안 |
|---|---|---|---|
| `read_paths.py` | 경로 상수(ROOT·SB_DIR·SND·CONTENTS…). 레시피 `setup()` 이 런타임에 값을 덮어씀 | **X** — “읽는다”로 읽힘 + 실제로는 “현재 프로젝트 경로 레지스터” | `reading_paths.py` 또는 `paths_registry.py` |
| `read_import.py` | 엑셀·PDF → `data<N>.py` 추출 | △ | `reading_extract.py` (레시피 단계 이름 `extract` 와도 일치) |
| `read_gen.py` | `data<N>.py` → HTML/CSS/JS | O(비교적) | `reading_build.py` (단계 이름 `build` 와 일치) |
| `read_measure.py` | Playwright 실측 | O | `reading_measure.py` |
| `read_verify.py` | 산출물 검증 | O | `reading_verify.py` |
| `read_run.py` | **안 쓰는 옛 CLI** | **X** — 이름만 보면 “표준 실행 진입점” | 지우거나 `_옛도구/read_run.py` 로 이동 |

> 우선순위: 이름 일괄 변경은 `importlib` 로 부르는 곳(`runner.GEN_MODULES`, `read_gen.load_lesson`)까지 건드리므로 **`read_run.py` 처리만 먼저** 하는 것이 안전하다.

### 4-2. `proto_*`
- `proto_scan.py` — 하는 일(견본 페이지 HTML/CSS + 엑셀 시트를 읽어 규칙 후보를 뽑음)과 이름이 **대체로 맞다**. 다만 `scan` 이 “폴더를 훑는다”로 읽혀 `discover()` 와 혼동된다. `proto_analyze.py` 가 화면 버튼(`/api/analyze`, 레시피 `analyze()`)과도 일치해 더 낫다.
- `proto_lesson()` / `proto_pages()` / `proto_ops()` / `prototype_units()` (`recipes/cj_reading.py:384~437) — `proto_*` 와 `prototype_*` 이 한 파일에 섞여 있다. 하나로 통일 권장(`prototype_*`).
- `rules/cj_reading/proto_L<N>.json` 의 `L` 은 Lesson 뜻인데, 단원 id 가 `special_lesson` 일 때 `proto_Lspecial_lesson.json` 이 되어 **`L` 이 의미를 잃는다**. `proto_<단원id>.json` 이 맞다.

### 4-3. `project.json` vs `project_rules.json` vs `rules.json` — **가장 심각**
세 파일 모두 “프로젝트”와 “규칙”이라는 말만 쓰고 있어, 이름만으로는 차이를 전혀 알 수 없다.

| 파일 | 실제 내용 | 누가 쓰나 |
|---|---|---|
| `project.json` | 단원 목록만. **`project_rules.json` 과 내용 중복**(units 배열이 동일) | `project_io.py` — 마이그레이션·폴백 전용 |
| `project_rules.json` | 프로젝트 이름/root + paths + patterns + units + prototype = **프로젝트 구조의 기준(SSOT)** | `project_rules_io.py` — 화면·레시피가 상시 사용 |
| `rules/cj_reading/rules.json` | HTML **생성 규칙**(팝업 유무·id 패턴 등). 프로젝트 구조와 무관 | `rules_io.py` — 지금은 코드와 대조 표시용 |
| `rules/cj_reading/proto_L*.json` | 프로토 분석 **원자료** | `proto_scan.py` |
| `settings.json` | `{"cj_reading": {"root": "E:\\..."}}` — 사용자가 고른 슬롯 값 | `runner.load_settings()` |

제안: `project_rules.json` → **`project_structure.json`** (구조·경로·단원), `rules/<레시피>/rules.json` → **`html_rules.json`** 또는 `gen_rules.json`. 그러면 “구조 = structure / 생성규칙 = rules” 로 갈린다. `project.json` 은 병합 후 제거.

### 4-4. `recipe` / `recipes/cj_reading.py`
“recipe” 는 코드 안에서 **“한 교재 종류의 생성 절차 선언 모듈”** 을 뜻한다 — `NAME`, `SLOTS`(사용자가 고를 자료 경로), `PROTO`, `EDIT`, 그리고 `setup/units/extract/build/measure/verify/preview` 함수 묶음. `runner.py` 가 `importlib` 로 불러 있는 함수만 실행한다(`runner.py:126 list_recipes`, `:144 import_module`). 즉 사실상 **플러그인/어댑터**다.

- “recipe”(조리법)라는 비유는 “한 번 실행할 작업 지시서”를 연상시키는데, 실제로는 **교재별 어댑터 모듈**이라 수명이 훨씬 길다.
- 다만 이미 화면·문서·API(`/api/recipes`, `/api/recipe/<id>`) 전반에 박혀 있어 **바꾸는 비용이 크다.** 이름을 바꾸기보다 `docs/PROJECT.md` 에 “recipe = 교재별 어댑터 모듈” 한 줄 정의를 두는 편이 실효적. 굳이 바꾼다면 `adapters/` 또는 `교재별/`.

### 4-5. `discover()`
`recipes/cj_reading.py:144` 한 곳에만 있다(다른 파일엔 없음).
- 이름은 “발견한다” = **구조를 결정하는 주체**로 읽힌다.
- 실제 동작은 docstring 이 밝히듯 “`project_rules.json` 에 이미 적힌 것은 절대 덮지 않고, **빈 자리만 채우는 보조**”. `units()`(:194)가 `PR.units()` 를 먼저 깔고 그 위에 `discover()` 결과를 얹는다.
- 즉 **이름이 실제보다 세게 들린다.** 프로젝트 지침 9항(“구조를 결정하는 주된 방법이 자동 탐색이 되면 안 된다”)과 이름이 정면으로 충돌해, 코드를 처음 보는 사람이 “아직 자동 추측을 하고 있다”고 오해하기 쉽다.
- 제안: `scan_for_new_units()` / `probe_units()` / `verify_units_on_disk()`.

### 4-6. UI/API 핸들러 이름
| 지금 | 문제 | 제안 |
|---|---|---|
| `GET /api/project` · `POST /api/project` · `app.py:419 _project()` | **`project.json` 이 아니라 `project_rules.json` 을 읽고 쓴다.** 이름과 실제 파일이 어긋남 | `/api/units` 또는 `/api/structure` |
| `GET /api/proto` (`_proto_info`) vs `POST /api/analyze` vs `POST /api/promote` | 셋 다 프로토 관련인데 동사 체계가 다름(명사/동사/동사) | `/api/proto`(조회) · `/api/proto/scan` · `/api/proto/promote` |
| `app_page.py:356 prepUnit()` | 이름만으로 “단원 준비”가 무엇인지 안 보임 | `loadUnitPages()` 등 |
| `app_page.py:329 oneUnit()` / `:312 pickedUnits()` / `:320 unitPicked()` / `:325 multiPicked()` | `unitPicked` 와 `pickedUnits` 가 한 글자 순서만 다른데 뜻이 다름(이벤트 핸들러 vs 조회) | 핸들러는 `onUnitPick()` 처럼 `on-` 접두 통일 |
| `app.py:24 start_job()` vs `:51 start_task()` | job/task 구분이 이름에 안 드러남(실제로는 job=생성 실행, task=분석 등 단발 작업) | `start_run()` / `start_side_task()` |
| `cj_reading.py:100 fresh(unit)` | 무엇을 fresh 하게 하는지 안 보임(모듈 재로드) | `reload_unit_modules()` |

### 4-7. 최상위 폴더 이름 `_딕테이션_생성기`
**맞지 않는다.**
- 지금 이 폴더의 코드가 실제로 하는 일은 **Reading 본문 페이지 생성**이다. 레시피도 `cj_reading.py` 하나뿐이고, 파이프라인 전체가 `read_*`, `docs/RULES.md` 도 Reading 규칙이다.
- 딕테이션 관련 코드는 **전부 `_옛도구/`** 에 들어가 있고(`dlg.py` `gen.py` `rd.py` `src.py` `build3.py`), 어느 것도 현재 파이프라인에서 불리지 않는다. `README_runner.md` 는 `cj_dictation.py` 를 “(다음)” 으로 적어 두었을 뿐 아직 없다.
- 즉 폴더 이름은 **이 도구의 출발점(딕테이션 팝업 작업)** 의 흔적이고, 현재 내용과는 어긋난다.
- 제안: `_HTML생성기` 또는 `_교재생성기` / `_generator`. 실행 런처 파일 이름이 이미 `HTML생성기.vbs` 이고 화면 제목도 “HTML 생성기” 라서 일관된다.
- **주의**: `read_paths.py:21 GEN = os.path.join(ROOT, '_딕테이션_생성기')` 에 폴더명이 박혀 있고, `project_rules.json` 의 경로들과 `_backup`/`_기준본` 상대경로도 이 폴더 기준이다. 폴더를 바꾸려면 최소한 `read_paths.py:21` 을 함께 고쳐야 한다.

---

## 5. 정리 중 눈에 띈 문제 (참고)

1. **`project_rules.json` 의 root 가 리눅스 세션 경로다.**
   ```
   "root": "/sessions/rcw-01ugds2gmjl7ze6nfm4ezz9b/mnt/2026_cj_midd3_eng"
   ```
   반면 `settings.json` 은 `"E:\\00_works\\2026\\2026_cj_midd3_eng"`. 컨테이너에서 한 번 실행하면서 덮어써진 것으로 보인다(`app.log` 에도 같은 세션 경로로 `read_gen` 이 로드된 기록이 09-22 01:58 에 남아 있고, 12:55 Windows 실행 기록이 그 뒤). 세션 id 가 포함된 경로라 **다음 세션에서는 존재하지 않는다.** 정리 작업과 별개로 먼저 확인할 값.
2. `git` 최초 커밋이 2026-09-21 이라, `_backup/코드/` 의 09-16~09-20 `.bak` 은 git 에 없는 유일본이다. 백업 폴더를 지우기 전 이 시기 파일부터 확인해야 한다.
3. `.gitignore` 가 없어 추적 파일 514개 중 400개 이상이 산출물·백업·캐시다. 정리 효과가 가장 큰 단일 조치는 `.gitignore` 추가(`__pycache__/`, `*.pyc`, `app.log`, `_backup/`)다.
4. `단원자료/` 에 **기계 생성물과 사람 입력값이 섞여** 있다(`data*.py`/`*scroll*.py`/`krlayout*.py` = 생성물, `layout*.json` = 입력). “다시 만들 수 있는 것”과 “다시 만들 수 없는 것”의 경계가 폴더에서 안 보인다.
5. 문서가 `docs/`(09-21) · `문서/`(09-15~17) · 루트 `README_runner.md` 세 군데로 흩어져 있고, SKILL.md 는 `docs/` 만 가리킨다.
