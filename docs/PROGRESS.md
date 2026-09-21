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
- `read_import` 가 `rules.json` 을 읽는 경로 — 아직 없음

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

## 10. 옛 문서 (`_딕테이션_생성기/문서/`)

과거 작업 기록으로 **그대로 둔다.** 코드가 참조하지 않는다.

| 파일 | 내용 | 지금 지위 |
|---|---|---|
| `10_Reading본문페이지_규칙.md` | 3단원 원본 분석 — 팝업 번호·마크업·mp3 규칙 | `RULES.md` 의 원 근거. 참고용 보존 |
| `HTML생성기-진행기록.md` | 8장짜리 진행 기록 | 이 파일의 앞선 판. 보존 |
| `11_6단원_Reading본문_작업결과.md` | 6단원 적용 결과 | 과거 기록 |
| `00_작업인수인계.md` | 컨테이너/CMD 시절 절차 | 과거 기록. **지금 절차와 다름** |
| `README_Reading파이프라인.md` | `data<N>.py` 를 손으로 쓰던 시절 사용설명서 | 과거 기록. 일부 낡음 |
| `../README_runner.md` | runner·app 사용법 | `PROJECT.md` 와 겹침. 보존 |
