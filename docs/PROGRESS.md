# 진행 기록

> 프로젝트 전반은 `PROJECT.md`, 규칙은 `RULES.md`, 문제는 `ISSUES.md`.
> 여기에는 **무엇을 했고 무엇이 확인되었는지**만 적는다.
> 이 파일에 적힌 것은 코드나 기존 문서에서 확인된 것뿐이다.

---

## 1. 지금까지 구현된 것

| 덩어리 | 상태 | 확인 방법 |
|---|---|---|
| 4단계 파이프라인 (추출→생성→측정→검증) | 동작 | 7·8·Special Lesson 실제 생성 |
| 레시피 구조 (`runner.py` + `recipes/`) | 동작 | 레시피 1개(`cj_reading`) |
| 단원 등록부 (`project.json`) | 동작 | 1~8 + `special_lesson` 등록됨 |
| 쪽만 골라 생성 (`build(only=…)`) | 동작 | `Ctx.pages` → `read_gen.build` |
| 백업·되돌리기 (`_backup/산출물`) | 동작 | 단원마다 최근 5벌 |
| 회귀 검사 (`regress.py` + `_기준본`) | 동작 | 기준본은 **7·8단원만** |
| 프로토 분석 (`proto_scan` → `proto_L<N>.json`) | 동작 | 3단원 38항목 · 6단원 52항목 |
| 규칙 승격 (`rules_io.promote`) | 동작 | 현재 `rules.json` = 3단원 것 |
| **`rules.json` 을 실제 생성에 사용** | **19항목** | 아래 3장 |
| 각론 해석 자동 추출 (`guide_stream`) | Special Lesson 만 | 52/52 일치 |
| 설정 패널(지면 다듬기) | 동작 | `layout<N>.json` 편집 |

## 2. 생성에 쓰이는 단원

| 단원 | `layout<N>.json` | 해석 원천 | 기준본 | 비고 |
|---|---|---|---|---|
| 1~5 | 없음 | 없음(전부 `해석x`) | 없음 | `data<N>.py` 는 옛 초안. 이 방식으로 만든 적 없음 |
| 6 | 없음 | `korean_stream` | 없음 | 실기 lesson06 은 이 생성기 결과 |
| 7 | 있음 | layout 의 `kr`(손입력) | **있음** | |
| 8 | 있음 | layout 의 `kr`(손입력) | **있음 — 합격선** | |
| Special Lesson | 있음 | `guide_stream` (각론9 자동) | 없음(실기와 대조) | |

## 3. `rules.json` → 생성 연결 (2026-09-17)

- `read_gen.load_rules(rid)` · `R(key, default)` · `_fill()` · `head_fill()` · `imgdir()` 추가 (165줄)
- `recipes/cj_reading.py build()` 에 `read_gen.load_rules(ctx.recipe.ID)` 한 줄
- 옮긴 항목 19개 (`RULES.md` 1장)
- **검증**
  - 7단원 19개 파일 기준본과 바이트 동일
  - 8단원 19개 파일 기준본과 바이트 동일
  - Special Lesson 25개 파일 실기와 바이트 동일
  - 규칙을 일부러 바꾸면(`speedBtn`·`korBtn`) 생성 HTML 이 따라 바뀜 → 진짜로 읽고 있음
  - 3단원 규칙 vs 코드 대조: `같음 26 · 다름 0 · 규칙에만 4 · 코드에만 3 · 프로토로는 모름 3`

## 4. 프로토 분석 관련

- 프로토는 **3단원**. 6·7·8단원은 이 생성기가 만든 페이지라 견본으로 쓰면 순환이 된다.
- `proto_L3.json` 38항목 (2026-09-17 재분석), `proto_L6.json` 52항목(남겨 둠).
- 3↔6 차이 16항목은 전부 **자료 차이**로 확인: 소제목 이미지 12개, Read Smart 들머리 3개, 시트 이름 1개.
- 프로토에서 못 뽑는 항목은 측정 여백 3개뿐.

## 5. 각론 해석 자동 추출 (2026-09-17)

- `read_import.guide_stream(n, d)` · `apply_guide_kr(d, gkr, check)` · `GuideError` 추가
- `recipes/cj_reading.py extract()` 에서 `P.unit(unit).get('kr') == 'guide'` 일 때만 탄다
- `project.json` 의 Special Lesson 에 `"kr": "guide"` 한 줄
- 손으로 넣어 둔 `layoutspecial_lesson.json` 의 `kr` 52개와 **글자 단위로 견주고, 다르면 멈춘다**(덮어쓰지 않음)
- 검증: 52/52 일치. 일부러 틀리게 하면 `GuideError` 로 생성 중단, `data` 파일 그대로.

## 6. 쪽 번호 정규화 · 이음매 (2026-09-17)

- `read_paths.pgkey()` 추가 — `'014'` 와 `'14'` 를 같은 쪽으로 본다
- `read_gen.load_syntax()`·`build()`, `read_import.syntax_sentences()`·`assemble()` 4곳이 쓴다
- 효과: 1~5단원 `KeyError: '014'` 사라짐. 0이던 `|n|` 구문 번호가 13~15개로 채워짐
- `read_import.clear_joins(d)` 추가 + `extract()` 에서 호출 → `⌇` 이음매 표시가 `data<N>.py` 에 남지 않음
- 검증: 7·8·Special Lesson 초안 해시 변화 없음. 1~6단원은 `|n|`·`⌇` 두 가지만 달라지고 나머지 0줄

## 7. 확인된 것 / 아직 확인하지 않은 것

**확인됨**
- 7·8단원 생성 결과가 기준본과 바이트 동일 (여러 차례)
- Special Lesson 25개 파일이 실기와 동일
- `rules.json` 이 실제로 생성에 영향을 준다
- 1~6단원 build 가 `KeyError` 없이 끝난다 (기존 `data<N>.py` 기준)

**확인 안 됨**
- 1~6단원 생성 결과의 옳고 그름 (기준본 없음 · 만들 계획 없음)
- `measure` 단계를 `rules.json` 변경 뒤 끝까지 돌려 본 적 없음 (2026-09-17 이후)
- 다른 교재(두 번째 레시피)에서의 동작 — **한 번도 해 본 적 없음**

**정정(2026-09-22)** 이전 기록 "`read_import` 가 `rules.json` 을 읽는 경로 — 아직 없음"은 틀렸다. `read_import.py:129`(`sound.sheet`)·`159`(`storyboard.sheet.syntax`)가 이미 `R()`을 거쳐 `rules.json`을 읽는다. 다만 `159`가 찾는 키 이름(`storyboard.sheet.syntax`)과 `rules.json`에 실제로 적힌 키(`storyboard.sheet.구문 해설` 등)가 달라 **읽어도 영원히 매칭되지 않는다** — "안 읽는다"가 아니라 "읽어도 항상 기본값만 나온다"가 정확하다(`ISSUES.md` #14 항목 3).

## 8. 지금 하고 있는 것

2026-09-21: 프로젝트 방향을 다시 확정했다.

- Claude는 프로젝트를 **최초 1회 분석**한다.
- 최초 분석에서 프로젝트의 **경로·단원·페이지·자료 연결·prototype·생성 규칙**을 모두 찾아 JSON으로 기록한다.
- 일반 HTML 생성기는 이후 **그 JSON을 읽어서** 동작한다.
- 일반 생성기가 프로젝트 폴더를 다시 탐색해서 구조를 추측하는 방식은 주된 설계가 아니다.
- 기존 `docs/` 4종은 유지하고, 새 문서를 늘리기보다 기존 문서의 역할을 이 방향에 맞게 정리한다.

**코드는 아직 수정하지 않았다.**

## 9. 다음 작업 순서

1. 현재 코드에서 **프로젝트별 정보가 하드코딩된 모든 지점**을 다시 목록화한다.
2. Claude 최초 분석 결과에 들어갈 **프로젝트 JSON 스키마**를 확정한다.
3. `project.json` / `rules.json` / 프로젝트 분석 JSON의 역할을 겹치지 않게 정한다.
4. JSON을 기준으로 단원/프로토/페이지 선택이 가능하도록 일반 생성기의 입력 흐름을 바꾼다.
5. JSON에 없는 프로젝트 구조를 추측하는 `discover()`/fallback을 보조 검증 기능으로 축소한다.
6. 그 다음 `read_gen`/`read_import`의 프로젝트 종속 규칙을 단계적으로 데이터화한다.
7. 기존 7·8·Special Lesson 결과를 기준으로 회귀 검증한다.

기존 문제 `ISSUES.md` #5, #1은 별도 이슈로 유지한다. 이번 구조 작업과 섞어서 한 번에 고치지 않는다.

## 10. 2026-09-22 작업 — prototype JSON화 + 스키마 확정 + 정리 착수

### prototype을 project_rules.json 기준으로 (구현 완료, 상세는 `claude/archive/prototype-구현결과.md`)

- `project_rules_io.py`에 `proto_units()`·`proto_pages(unit_id)` 추가 — `project_rules.json["prototype"]["units"]`를 읽는 공용 창구
- `recipes/cj_reading.py`의 `proto_lesson()`이 더는 `int()` 강제 변환을 하지 않음 — 문자열 단원 id(`special_lesson` 등)가 그대로 통과
- `proto_pages(ctx)`가 폴더 재탐색(`proto_scan.pages_in()`)을 그만두고 JSON에 등록된 페이지만 돌려줌 — **JSON에 없는 페이지는 화면에 안 보인다**(검증됨: special_lesson 실제 폴더에 6쪽이 있지만 JSON에 등록한 `p152_03` 하나만 노출)
- `proto_scan.scan_sound()`의 `'%d과' % int(lesson)` 무조건 실행 제거 — `sheet` 인자를 우선 쓰고, 없을 때만 숫자 단원에 한해 시도. 문자열 단원이면 크래시 대신 "시트 이름을 모릅니다" 오류
- 화면의 프로토 단원 입력칸을 자유 입력에서 드롭다운(`protoUnits`)으로 교체
- **검증**: 문자열 id(`special_lesson`) 프로토 분석이 끝까지 성공(26항목), 7·8단원 `POST /api/run`이 기준본과 바이트 단위로 동일 — extract/build 파이프라인은 이번 변경의 영향을 받지 않음
- 의도적으로 건드리지 않은 것: `read_paths.py`의 `storyboard()`/`ops()`/`guide_pdf()` 폴백, `rules.json` 구조 전체, extract/build 파이프라인, `read_import.py`의 자료 해석 로직

### project_rules.json 스키마 확정 (schema 2, `docs/SCHEMA.md`)

- 최상위 키: `project`/`paths`/`units[]`/`prototype`/`patterns`/`discovery` 6개 + `schema` 버전 번호
- `patterns`(없으면 시스템이 못 도는 확정값) vs `discovery`(없어도 동작하는 최초 탐색 보조)를 구분 — `discovery: {}`로도 정상 동작하도록 설계, 가상 프로젝트로 검증
- `rules/<recipe>/rules.json`은 `project_rules.json` 안에 넣지 않고 **별도 파일로 유지**하기로 결정 — recipe 단위로 여러 프로젝트가 재사용해야 하기 때문(프로젝트 지침 8번이 허용한 예외 조건에 해당, 이유는 `SCHEMA.md` 1-7절)
- 가상 프로젝트(다른 폴더 구조·다른 시트명·문자열 단원 id·다른 mp3 규칙)로 재검증: 5개 항목 통과, **mp3 파일명의 "조립 순서 자체가 다른 경우"만 스키마 밖의 recipe(`rules.json`) 템플릿 확장이 필요**하다고 정직하게 남김(`PROJECT.md` 12장에도 기록)
- **코드는 아직 수정하지 않았다** — 남은 작업은 `ISSUES.md` #14의 12개 항목

### 문서·정리 작업 착수

- 사용자 승인: 문서 정리 → root 교정 → 파일 정리 → `_옛도구/` 삭제 → `read_run.py` 정리 → 스키마 코드 반영(+ project_rules.json 다중 프로젝트 분리 포함) → 이름 변경 → 회귀 테스트 → git 정리, 총 9단계 순서로 실제 수정을 진행하기로 확정
- 1단계(문서 정리)부터 실행: `docs/SCHEMA.md` 신설, `PROJECT.md`·`RULES.md`·`ISSUES.md`에 이번 결정 반영, Cowork Project의 과거 분석 문서 11건을 `claude/archive/`로, 딕테이션 관련 2건을 `claude/dictation/`으로 이동(내용은 그대로, 경로만 이동)
- 이후 새 분석 MD를 계속 만들지 않고, 확정 사항은 기존 5개 문서(`PROJECT`/`RULES`/`PROGRESS`/`ISSUES`/`SCHEMA`)에 반영하는 것으로 전환

## 11. 옛 문서 (`_딕테이션_생성기/문서/`)

과거 작업 기록으로 **그대로 둔다.** 코드가 참조하지 않는다.

| 파일 | 내용 | 지금 지위 |
|---|---|---|
| `10_Reading본문페이지_규칙.md` | 3단원 원본 분석 — 팝업 번호·마크업·mp3 규칙 | `RULES.md` 의 원 근거. 참고용 보존 |
| `HTML생성기-진행기록.md` | 8장짜리 진행 기록 | 이 파일의 앞선 판. 보존 |
| `11_6단원_Reading본문_작업결과.md` | 6단원 적용 결과 | 과거 기록 |
| `00_작업인수인계.md` | 컨테이너/CMD 시절 절차 | 과거 기록. **지금 절차와 다름** |
| `README_Reading파이프라인.md` | `data<N>.py` 를 손으로 쓰던 시절 사용설명서 | 과거 기록. 일부 낡음 |
| `../README_runner.md` | runner·app 사용법 | `PROJECT.md` 와 겹침. 보존 |

## 12. 2026-09-23 작업 — Step 5(`read_run.py` 삭제) + Step 6(`project_rules.json` 프로젝트 루트 기준 전환)

### 저장 위치 확정

`project_rules.json`은 **프로젝트 루트**(`E:\00_works\2026\2026_cj_midd3_eng\project_rules.json`)에 둔다. 생성기 설치 폴더(`_딕테이션_생성기/`)에 두는 공통 파일 방식은 쓰지 않는다 — 프로젝트마다 자기 것을 가지며, 서로 섞이지 않아야 하기 때문이다. `rules/<recipe>/rules.json`(recipe 공통 생성 규칙)·`settings.json`(실행 환경 설정)과의 역할 구분은 그대로 유지한다. `settings.json`의 `root`와 `project_rules.json` 위치의 중복 정리는 **이번 단계에서 손대지 않았다**(6번 항목, 아래 참고).

### Step 5 — `read_run.py` 삭제

- 사용처 전수 확인 결과 다른 코드·API·정상 실행 경로 어디에서도 참조하지 않음을 확인 → 삭제 확정.
- 삭제 전 `문서/README_Reading파이프라인.md`의 `python read_run.py 7` 류 사용 예시를 전부 현재 UI/API(`[생성]` 버튼 → `POST /api/run`) 기준 설명으로 교체(7곳). `--show` 옵션은 UI에 대응 기능이 없어 복구하지 않고 제거.
- `read_run.py` 삭제 완료. 파일 목적 표에서도 해당 행 제거.

### Step 6 — `project_rules.json` 프로젝트 루트 기준 전환

- `project_rules_io.py`: 고정 경로(`PATH`) 대신 `set_root(root)` / `_path()`로 변경 — root가 정해지지 않은 채 호출되면 조용히 넘어가지 않고 에러를 낸다. 프로젝트마다 다른 파일을 자동으로 섞어 읽는 일을 막기 위해 **레거시 위치 자동 이관은 만들지 않았다**(다른 프로젝트가 들어왔을 때 예전 데이터가 새 프로젝트로 새어 들어갈 수 있어서). 대신 기존 CJ 파일은 한 번 수동으로 새 위치로 옮겼다.
- `recipes/cj_reading.py`의 `setup(ctx)`: 요청마다 항상 `PR.set_root(...)`을 호출하고, root가 유효하지 않으면 `read_paths.py`의 기존 상태(`ROOT`/`SB_DIR`/`SND`/`WORDDIC`/`CONTENTS`/`GUIDE_DIR`/`STORYBOARD_SHEETS`/`UNITS`)를 비운다 — 이전 요청의 값이 다음 요청에 남아있지 않도록.
- `read_paths.py`: 단원 id가 숫자가 아닐 때 `int()`가 그대로 죽는 대신 "등록되지 않은 단원입니다" 오류로 명확히 안내(`storyboard()`/`ops()`). `guide_pdf()`는 `patterns.guidePdf` 패턴을 실제로 읽어 쓰도록 연결하고, 숫자가 아닌 단원이면 크래시 대신 `None` 반환(추측하지 않음).
- `patterns.storyboardSheets`(syntax/miniVocab/dictation 시트 이름) 신설·연결: `read_import.py`의 `syntax_sentences()`, `read_gen.py`의 `load_words()`/`load_syntax()` 3곳이 하드코딩된 시트 이름 대신 이 값을 우선 사용(값이 없으면 기존 기본값으로 폴백, 동작 변화 없음). `rules.json`의 `storyboard.sheet.*` 키와 이름이 겹쳐 보이던 부분 — 실제로는 별개 기능(하나는 코드-대조용 진단, 하나는 실행용 조회)임을 확인하고, 실행용 쪽만 `project_rules.json` 경유로 정리.
- `'%d과'`류 프로젝트 종속 하드코딩 재확인: mp3 파일명 접두어 `'3_'`이 `read_gen.py`(4곳)·`read_import.py`(1곳)에 여전히 남아있음을 재확인했다. 이번 단계 범위가 아니라 **고치지 않고 남겨둠** — 다음 단계 후보.
- `project.json`: 실사용처 확인 결과 `project_rules_io.ensure_migrated()`의 과거 데이터 이관용 폴백에서만 읽음 → 이번 단계에서 삭제하지 않음.
- `settings.json`과 `project_rules.json`의 root 역할 중복은 **정리하지 않고 이번 단계 밖으로 미룸** — 기존 기능이 깨질 위험이 있어 단계적으로 다루기로 함.

### 테스트

기존 CJ 프로젝트 로드, `project_rules.json` 로드(프로젝트 루트에서), 단원 목록, prototype 목록·페이지·분석, 7·8단원 `extract`+`build`(기준본과 바이트 단위 동일), Special Lesson, `/api/project`·`/api/proto`·`/api/pages`·`/api/analyze`·`/api/compare`·`/api/promote` 모두 정상 동작 확인. `regress.py`로 7·8단원 바이트 동일성 재확인. Special Lesson 회귀에서 기준본(`_기준본/cj_reading/special_lesson/`)과 8개 파일이 다르게 나왔으나, 이번 변경 전 코드로 동일 테스트를 재현해도 같은 차이가 나는 것을 확인 — **이번 작업과 무관한, 기존에 있던 기준본 오래됨 문제**로 판단하고 별도로 남겨둠.

테스트 중 바꾼 `settings.json`·`rules/cj_reading/rules.json`은 모두 원상 복구했고(`git diff` 무변화 확인), 테스트 과정에서 옛 코드 경로에 실수로 재생성된 불완전한 `project_rules.json`(빈 `prototype`)은 발견 즉시 삭제했다.

### 변경 파일

- 삭제: `read_run.py`
- 수정: `project_rules_io.py`, `recipes/cj_reading.py`, `read_paths.py`, `read_import.py`, `read_gen.py`, `문서/README_Reading파이프라인.md`, `docs/ISSUES.md`, `docs/SCHEMA.md`, `docs/PROGRESS.md`(이 절)
- 이동: `project_rules.json` (`_딕테이션_생성기/` → 프로젝트 루트), `patterns.storyboardSheets` 추가
