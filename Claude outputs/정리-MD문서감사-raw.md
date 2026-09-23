# MD 문서 전수 감사 (raw) — 2026-09-22

> 읽기 전용 조사. 어떤 문서도 수정·삭제·이동하지 않았다.
> 대상: Cowork Project "퍼플리셔" 문서 14개 + device(`.../2026_cj_midd3_eng/_딕테이션_생성기`) 로컬 MD 11개 = **총 25개**
> 기준 문서(가장 최신·정확): `claude/prototype-이후-전수분석.md`(09-22 04:00), `claude/project_rules.json-스키마-확정안.md`(09-22 08:07)

---

## 0. 목록 검증 결과

`project_info` 실제 목록은 **14개**였다(의뢰서의 13개 목록에 `claude/project_rules.json-스키마-확정안.md`가 실제로 존재함을 확인). 누락·추가 없음.

device `find . -name "*.md" -not -path "./.git/*"` 결과 **11개**:
`.claude/skills/html-generator/SKILL.md`, `docs/{ISSUES,PROGRESS,PROJECT,RULES}.md`, `README_runner.md`,
`문서/{00_작업인수인계, 10_Reading본문페이지_규칙, 11_6단원_Reading본문_작업결과, HTML생성기-진행기록, README_Reading파이프라인}.md`

---

## 1. 분류표 — Cowork Project (14개)

분류: ①목적 ②방향/구조 ③기술설계 ④작업/진행 ⑤문제/이슈

| 문서 | 위치 | 분류(비중 순) | 핵심 내용(2줄 이내) | 다른 문서와 겹치는 부분 | 판정 |
|---|---|---|---|---|---|
| `claude/prototype-이후-전수분석.md` (09-22 04:00) | Project | **③**(주) + ⑤ + ④ | 실제 코드 줄번호까지 열어 확인한 프로젝트 종속성 전수 목록. 달성도 C, 층별(바깥 A~B / 가운데 C / 안층 D~F) 평가와 9장 우선순위. | 최종검증.md·구현결과.md의 주장을 **재검증해 정정**(부록에 "직전 보고와 다른 점" 표). docs/ISSUES #14와 주제 동일하나 이쪽이 훨씬 정밀. | **유지 — 기술설계/이슈 기준 문서** |
| `claude/project_rules.json-스키마-확정안.md` (09-22 08:07) | Project | **③**(주) + ② | project_rules.json 최종 스키마(schema 2) 확정: project/paths/units/prototype/patterns/discovery + rules는 recipe별 별도 파일. | `-설계안.md`의 schema 1 초안을 **대체**(project.root 제거, prototype 구조 변경). 문서 머리에 "설계안·구현결과·최종검증은 건드리지 않았다"고 스스로 명시. | **유지 — 스키마 기준 문서** |
| `claude/prototype-구현결과.md` (09-22 02:03) | Project | **④**(주) + ③ | prototype을 project_rules.json 기준으로 바꾼 코드 수정 결과(6파일) + HTTP 테스트 결과. | 이 결과가 전수분석 2장 "이미 해결된 것" 표에 요약 흡수됨. | **통합** → `docs/PROGRESS.md`에 09-22 섹션으로 |
| `claude/prototype-구조-설계안.md` (09-22 01:48) | Project | **③**(주) | 위 구현 직전의 설계안. 변경 전 흐름 A / 변경 후 흐름 B / JSON 예시 C / 파일별 변경표 D. | `-구현결과.md`가 실제 결과로 대체. 설계 질문 3개는 이미 답이 나옴. | **보관(archive)** |
| `claude/project_rules.json-최종검증.md` (09-22 01:15) | Project | **⑤**(주) + ③ | 구현결과.md를 인정하지 않고 재검증 → "F:2 일부 종속성 남음". C-1~C-7 문제 목록. | C-1(문자 id 프로토 불가)·C-2(`%d과`)·C-4(prototype 스키마 죽음)는 **이후 해결됨**. 지금 이 문서만 읽으면 오판한다. | **보관(archive)** — 유효 내용은 전수분석이 승계 |
| `claude/project_rules.json-구현결과.md` (09-22 00:50) | Project | **④**(주) | project_rules.json 도입 구현 보고. "CJ 전용 하드코딩 제거", 7·8단원 바이트 동일 테스트. | 35분 뒤 최종검증.md가 같은 작업을 뒤집음(모순 사례 A). | **보관(archive)** |
| `claude/project_rules.json-설계안.md` (09-22 00:05) | Project | ③ + ② | schema 1 초안, 하드코딩 인벤토리, UI 15기능↔코드 매핑, 단계별 계획. | 스키마는 확정안이 대체. 인벤토리·데이터흐름은 전수분석이 더 정확하게 대체. UI 매핑은 docs/PROJECT.md 9장과 중복. | **보관(archive)** |
| `claude/HTML생성기-진행기록.md` (09-17) | Project | **④**(주) + ② | 09-17 시점 전체 진행 기록(끝난 것/버그 7건/폴더 지도/앞으로 할 일). | device `문서/HTML생성기-진행기록.md`와 **내용 동일**. `docs/PROGRESS.md`가 후속판. 3중 중복(모순 사례 B). | **보관(archive)** |
| `claude/HTML생성기-구조.md` (09-16) | Project | **②**(주) + ③ | 3층 구조(자료/규칙/단원), rules.json 역할, 회귀 검사, 설정 패널 A·쪽 선택 B. | `docs/PROJECT.md`가 같은 내용을 더 정확하게 대체(실제 코드 조사 기반). | **보관(archive)** |
| `claude/1차-HTML생성기-구성안.md` (09-16) | Project | **①** + ② | runner + recipes 껍데기 구조 최초 제안. "세 생성기를 합치지 말고 껍데기만". | 이미 전부 구현됨(runner.py·recipes/·app.py). `README_runner.md`가 실물 버전. | **보관(archive)** |
| `claude/범용-HTML생성도구-설계안.md` (09-16) | Project | **①**(주) + ② | 2판. 왜 layout<N>.json이 핵심 자료구조인지, 왜 골든만으로 부족하고 불변식 검사가 필요한지, 없앨 수 없는 한계 3가지. | 결론 일부는 PROJECT.md 1장에 흡수됐으나 **"왜"를 설명하는 유일한 문서**. 다른 문서에 대체물 없음. | **통합** → `docs/PROJECT.md` 1장(목적·근거·한계)으로 흡수 후 원본 보관 |
| `claude/cj-딕테이션-작업인수인계.md` (09-15) | Project | ④ + ③ | **딕테이션 팝업(별개 작업)** 인수인계. dlg.py/rd.py/build3.py 절차, 14px 보정, 함정 10가지. | device `문서/00_작업인수인계.md`와 **동일 문서**. 생성기 프로젝트 문서 아님(다른 트랙). | **유지 — 단, 딕테이션 트랙으로 분리 표시** |
| `claude/cj-중3-딕테이션-변환규칙.md` (09-15) | Project | **③** | 딕테이션 팝업 변환 규칙(빨간 글씨=빈칸, itemIdx, 입력칸 폭, scrollTop 산출식). | 위 인수인계 4~6장과 상당 부분 중복(인수인계가 요약본). | **유지 — 딕테이션 트랙 기술 기준** |
| `claude/listening-dictation-변환규칙.md` (09-09) | Project | **③** | **동아 AIDT(또 다른 별개 작업)** HWP→index.html 변환 규칙. Lesson2~8 완료·검증 통과. | 이 생성기 프로젝트와 무관. 작업 자체가 종료됨. | **보관(archive)** — 완료된 별개 트랙 |

---

## 2. 분류표 — device 로컬 (11개)

| 문서 | 위치 | 분류 | 핵심 내용(2줄 이내) | 겹치는 부분 | 판정 |
|---|---|---|---|---|---|
| `.claude/skills/html-generator/SKILL.md` | device | **②**(주) | 작업 원칙 5가지 + 7단계 작업 절차. "먼저 docs/ 4개를 읽어라"라고 지시. | Cowork Project instructions(프로젝트 지침 14개 항목)와 **내용이 거의 동일**. 하나는 claude.ai 쪽, 하나는 코드 쪽에 있어 둘 다 필요. | **유지 — 진입점 겸 절차서** |
| `docs/PROJECT.md` | device | **①②③** 혼합 | "이 문서가 기준 문서다". 목적·설계원칙·폴더구조·8단계 데이터흐름·기능 A/B/C 분류·종속/공통 구분·최종 목표 흐름. | 1장은 `범용-HTML생성도구-설계안`·`1차-구성안`과, 3장은 `HTML생성기-구조`와, 10장은 전수분석 3장과 겹침(전수분석이 더 정밀). | **유지 — 목적/방향 기준 문서** |
| `docs/RULES.md` | device | **③**(주) | 규칙 P/C/D/? 4분류. rules.json 19항목(생성에 실제 사용) vs 16항목(미사용). 코드 고정 규칙·각론 좌표 상수. | 2장(미사용 16항목)은 전수분석 4-2와 동일 결론. 4-4 GUIDE_* 상수는 전수분석 6-7과 중복. | **유지 — 생성 규칙 기준 문서** |
| `docs/PROGRESS.md` | device | **④**(주) | 구현된 것 표, rules.json 연결 검증, 확인됨/확인 안 됨, 다음 작업 7단계. 10장에 옛 문서 지위 정리. | 09-17까지는 `claude/HTML생성기-진행기록.md`와 동일 사건. 09-22 작업(prototype·project_rules) **미반영**. | **유지 — 진행 기준 문서** (갱신 필요) |
| `docs/ISSUES.md` | device | **⑤**(주) | #1~#14. #5(기준본 견주기가 잰 값 파일 손상, 원인 미확인)가 최우선. #14는 프로젝트 일반화 이슈. | #14는 전수분석 전체와 주제 동일(전수분석이 상세판). #7·#8·#9는 전수분석 3장·4장에 더 정확히 재기술됨. | **유지 — 문제 기준 문서** |
| `README_runner.md` | device | **③** | runner.py CLI 사용법, app.py 화면 설명, 레시피 만드는 법, API 목록. | `docs/PROGRESS.md` 10장이 스스로 "`PROJECT.md`와 겹침"이라 적어 둠. 레시피 인터페이스는 `1차-구성안` 2장과도 중복. | **통합** → `docs/PROJECT.md` 부록(사용법) 또는 `docs/USAGE.md` 단일화 |
| `문서/00_작업인수인계.md` | device | ④+③ | 딕테이션 팝업 인수인계 — Cowork `cj-딕테이션-작업인수인계.md`와 동일 문서. | 완전 중복(위치만 다름). PROGRESS 10장이 "지금 절차와 다름"이라 명시. | **보관(archive)** |
| `문서/10_Reading본문페이지_규칙.md` | device | **③** | 3단원 원본 HTML 전수 분석 — 팝업 번호·마크업·파일 구성. | `docs/RULES.md`가 "이 문서의 원 근거"라고 명시. RULES.md 1·4장이 요약본. | **보관(archive)** — RULES.md의 1차 근거로 보존 |
| `문서/11_6단원_Reading본문_작업결과.md` | device | **④** | 6단원 적용 결과·확정 규칙·남은 일(09-15). | 그때 확정한 규칙은 RULES.md로 승계. 진행 상황은 PROGRESS.md가 승계. | **보관(archive)** |
| `문서/HTML생성기-진행기록.md` | device | **④** | Cowork `claude/HTML생성기-진행기록.md`와 **같은 문서**(동일 내용). | 같은 진행 기록이 ①Cowork ②device 문서/ ③docs/PROGRESS.md 3곳에 존재. | **삭제 후보** — Cowork 사본 + PROGRESS.md가 이미 승계, 세 번째 사본은 혼동만 유발 |
| `문서/README_Reading파이프라인.md` | device | **③** | `data<N>.py`를 손으로 쓰던 시절 사용설명서. `read_paths.py`를 직접 열어 고치라고 안내. | 현재 흐름(UI·runner·project_rules.json)과 **정면 배치**. PROGRESS 10장도 "일부 낡음"이라 표기. | **보관(archive)** — 삭제 후보에 가까우나 과거 규칙 근거가 일부 있어 보관 |

---

## 3. 판정 집계

| 판정 | 개수 | 문서 |
|---|---|---|
| **유지** | 9 | prototype-이후-전수분석 / project_rules.json-스키마-확정안 / cj-중3-딕테이션-변환규칙 / cj-딕테이션-작업인수인계 / SKILL.md / docs/PROJECT.md / docs/RULES.md / docs/PROGRESS.md / docs/ISSUES.md |
| **통합** | 4 | prototype-구현결과(→PROGRESS) / project_rules.json-구현결과(→PROGRESS) / 범용-HTML생성도구-설계안(→PROJECT 1장) / README_runner(→PROJECT 부록 or USAGE) |
| **보관** | 11 | prototype-구조-설계안 / project_rules.json-최종검증 / project_rules.json-설계안 / HTML생성기-진행기록(Cowork) / HTML생성기-구조 / 1차-HTML생성기-구성안 / listening-dictation-변환규칙 / 문서/00_작업인수인계 / 문서/10_Reading본문페이지_규칙 / 문서/11_6단원 / 문서/README_Reading파이프라인 |
| **삭제 후보** | 1 | 문서/HTML생성기-진행기록.md (Cowork 사본과 동일 + PROGRESS.md가 승계 = 3중 중복) |
| 합계 | **25** | |

※ `project_rules.json-구현결과.md`는 "통합"으로 분류했지만, 내용이 최종검증에서 반박된 부분이 많아 **통합 시 "이 시점의 주장"이라고 날짜를 붙여 옮기고 원본은 보관**해야 한다.

---

## 4. 심각한 중복·모순 사례

### A. 같은 코드 상태에 "완료도" 평가가 3개 (가장 심각)

같은 날 8시간 안에 세 문서가 같은 코드를 두고 서로 다른 말을 한다.

| 시각 | 문서 | 평가 |
|---|---|---|
| 09-22 00:50 | `project_rules.json-구현결과.md` | "CJ 전용 하드코딩 제거", 7·8단원 바이트 동일 → **사실상 완료** |
| 09-22 01:15 | `project_rules.json-최종검증.md` | "구현 보고서를 그대로 인정하지 않고 다시 확인" → **F:2, 일부 종속성 남음** |
| 09-22 04:00 | `prototype-이후-전수분석.md` | 층별로 나눠 **달성도 C** (바깥 A~B / 안층 D~F) |

세 문서 중 어느 것을 열었느냐에 따라 "다 됐다 / 안 됐다 / 반쯤 됐다"가 갈린다.
추가로 최종검증의 **C-1(문자 id에서 프로토 분석 불가)·C-2(`%d과` 하드코딩)·C-4(prototype 스키마가 죽어 있음)는 이미 해결됐는데**, 그 문서에는 해결 표시가 없다. 최종검증만 읽은 사람은 이미 고친 것을 다시 고치려 든다.

### B. "진행 기록"이 3벌 (서로 다른 시점에서 멈춰 있음)

| 파일 | 시점 | 상태 |
|---|---|---|
| `claude/HTML생성기-진행기록.md` (Cowork) | 09-17 | 멈춤 |
| `문서/HTML생성기-진행기록.md` (device) | 09-17 | 위와 **내용 동일**, 멈춤 |
| `docs/PROGRESS.md` (device) | 09-21 | 최신이지만 **09-22 작업 2건(prototype JSON화·스키마 확정) 미반영** |

결과적으로 **"지금 어디까지 왔는가"를 한 파일로 답할 수 없다.** 09-22 진행 상황은 진행 문서가 아니라 `prototype-구현결과.md`/`스키마-확정안.md` 같은 일회성 보고서에만 남아 있다. 새 분석을 할 때마다 새 MD를 만든 것이 이 상태의 직접적 원인이다.

### C. (부차) project_rules.json 스키마가 2판 병존

`-설계안.md`의 schema 1(`project.root` 포함, `prototype.lesson` 단수, `patterns.guidePdf` 포함) vs `-스키마-확정안.md`의 schema 2(`project.root` 제거, `prototype.units[]`, guidePdf는 discovery로 이동). 필드가 서로 충돌하는데 두 문서 모두 "설계안"이라는 이름을 달고 있다.

### D. (부차) 원칙 문서 2벌

Cowork Project instructions(14개 항목)와 `.claude/skills/html-generator/SKILL.md`가 같은 원칙을 각각 서술. 지금은 내용이 일치하지만, 한쪽만 고치면 조용히 어긋난다.

---

## 5. 제안 — 최종 문서 체계

### 5-1. 기준 문서는 device `docs/` 4개 + 스킬 1개로 고정

이미 `docs/` 4종이 역할 분리가 잘 돼 있고(PROJECT/RULES/PROGRESS/ISSUES), SKILL.md가 "먼저 이 4개를 읽어라"라고 지시하고 있다. **새 체계를 만들 게 아니라 이 4개를 기준으로 삼고 나머지를 여기로 모으는 것**이 최소 변경이다.

| # | 문서 | 역할(분류) | 여기로 흡수할 것 |
|---|---|---|---|
| 1 | `docs/PROJECT.md` | **① 목적 + ② 방향/구조** | `범용-HTML생성도구-설계안`의 "왜"(1장에), `README_runner`의 사용법(부록에), `HTML생성기-구조`의 3층 설명 |
| 2 | `docs/RULES.md` | **③ 기술설계 — 생성 규칙** | 현행 유지. 1차 근거는 `문서/10_Reading본문페이지_규칙.md` 링크로만 |
| 3 | `docs/SCHEMA.md` *(신설 1개만)* | **③ 기술설계 — project_rules.json 계약** | `project_rules.json-스키마-확정안.md` 전문을 이쪽으로 이전 |
| 4 | `docs/PROGRESS.md` | **④ 진행 상황** | 진행 기록 3벌 + 구현결과 보고서 2개를 날짜 섹션으로 |
| 5 | `docs/ISSUES.md` | **⑤ 문제/이슈** | `prototype-이후-전수분석.md`의 3장·8장(남은 종속성·실패 지점)을 #14의 하위 항목으로 |

**4~5개**로 줄어든다. `prototype-이후-전수분석.md`는 분량이 커서 통째로 넣기보다, 3·8·9장을 ISSUES #14 아래로 옮기고 원문은 **한 번만** archive에 남기는 방식을 권한다.

딕테이션/동아 트랙(`cj-딕테이션-*`, `listening-dictation-*`)은 **이 생성기 프로젝트 문서가 아니다.** 섞지 말고 Cowork Project 안에서 `claude/dictation/` 같은 별도 경로로 구분만 해 두면 된다.

### 5-2. 앞으로 새 MD를 만들지 않는 규칙

> **원칙: 분석 1회 = 새 파일 0개. 기존 5개 중 어느 섹션을 고칠지 먼저 정한다.**

| 이번 작업이 무엇인가 | 새 파일 대신 이렇게 | 금지 |
|---|---|---|
| 코드/구조를 분석만 했다 | 결과가 **사실**이면 `PROJECT.md` 해당 장을 **교체**, **문제**면 `ISSUES.md`에 `#N` 추가 | `XX-분석.md`, `XX-전수분석.md` 신설 |
| 설계안을 만들었다 | `SCHEMA.md` 또는 `RULES.md`의 해당 절을 **"확정 / 검토 중" 표시와 함께 갱신** | `XX-설계안.md` 신설 |
| 코드를 고쳤다 | `PROGRESS.md` 맨 위에 `## 2026-MM-DD — 제목` 섹션 추가(수정 파일·근거·테스트 결과). 관련 ISSUES 항목의 상태 줄만 `**고쳐짐**`으로 수정 | `XX-구현결과.md` 신설 |
| 앞 보고를 재검증했다 | **새 파일 금지.** 원래 문서의 그 문장을 고치고, 바뀐 이유를 `PROGRESS.md` 날짜 섹션에 한 줄 | `XX-최종검증.md` 신설 |
| 진행 상황을 정리했다 | `PROGRESS.md` 1·2장 표를 **갱신**(누적 아님) | 진행 기록 새 판 |

추가 규칙 3가지:
1. **같은 내용을 두 문서에 적지 않는다** — `PROJECT.md`가 이미 선언한 원칙. 이번 감사에서 깨진 게 확인됐으니 다시 못박을 것.
2. **평가·완료도는 `PROGRESS.md` 한 곳에서만 말한다.** 여러 문서가 "달성도 C / F:2 / 완료"를 각자 말하는 상태를 금지.
3. **모든 문서 머리에 `> 최종 갱신: YYYY-MM-DD · 이 문서가 담당하는 것: ①~⑤ 중 무엇` 한 줄**을 둔다. 역할이 겹치는 문서가 새로 생기는 것을 육안으로 막는다.

### 5-3. 보관(archive) 처리 — 실제로 어디로 (이동하지 않음, 제안만)

| 대상 | 제안 위치 | 이유 |
|---|---|---|
| Cowork 보관 대상 7개 (`prototype-구조-설계안`, `project_rules.json-{설계안,구현결과,최종검증}`, `HTML생성기-{진행기록,구조}`, `1차-HTML생성기-구성안`) | **`claude/archive/` 신설** (예: `claude/archive/2026-09-22_project_rules-설계안.md`) | 파일명 앞에 날짜를 붙이면 "언제 시점의 판단인지"가 제목만으로 드러나 모순 사례 A가 재발하지 않는다 |
| Cowork 딕테이션/동아 3개 | **`claude/dictation/`**(cj 2개) / **`claude/archive/`**(listening-dictation, 작업 종료) | 이 생성기 프로젝트와 다른 트랙임을 경로로 구분 |
| device `문서/` 4개 (00_작업인수인계, 10_Reading본문페이지_규칙, 11_6단원, README_Reading파이프라인) | **`문서/` 그대로 둔다** | 이미 archive 역할이고 `PROGRESS.md` 10장이 지위 표를 관리 중. 옮기면 그 표가 깨진다 |
| device `문서/HTML생성기-진행기록.md` | 삭제 후보 — 지우기 전 **Cowork `claude/archive/`에 사본이 있는지 확인** | 3중 중복 해소 |
| `README_runner.md` | 통합 후 `문서/`로 이동 | `PROGRESS.md` 10장이 이미 "PROJECT.md와 겹침"으로 분류 |

**archive의 유일한 규칙**: archive 안의 문서는 새 작업에서 **참조하지 않는다.** 필요하면 그 내용을 기준 문서 5개 중 하나로 끌어올린 뒤에 참조한다. 이 한 줄을 `docs/PROJECT.md` 맨 앞과 `SKILL.md`에 적어 두면 "옛 문서를 읽고 이미 고친 것을 다시 고치는" 사고(모순 사례 A)가 막힌다.

---

## 6. 즉시 처리 권고 (우선순위)

1. **`docs/PROGRESS.md`에 09-22 작업 2건을 날짜 섹션으로 추가** — 지금 "어디까지 왔는가"에 답하는 문서가 없다.
2. **`project_rules.json-최종검증.md`의 C-1·C-2·C-4에 "해결됨(09-22)" 표시** 또는 archive 이동 — 잘못된 재작업을 유발하는 가장 위험한 상태.
3. **스키마-확정안 → `docs/SCHEMA.md`로 이전**, `-설계안.md`의 schema 1은 archive로.
4. 진행 기록 3벌 정리(삭제 후보 1개 처리).
5. 문서 머리 한 줄(최종 갱신일 + 담당 분류) 일괄 추가.
