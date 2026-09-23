# project_rules.json 구조 (schema 2)

> 확정: 2026-09-22. 프로젝트 전반은 `PROJECT.md`, 규칙은 `RULES.md`.
> 여기에는 **지금 규칙이 무엇인가**만 적는다 — "왜 이렇게 정했는가"의 근거·검증 과정·초안 이력은
> `claude/archive/project_rules.json-설계안.md`·`-구현결과.md`·`-최종검증.md`·`prototype-이후-전수분석.md`에 있다.
>
> **코드는 아직 이 스키마를 전부 따르지 않는다.** 남은 작업 목록은 `ISSUES.md` #14.
>
> **2026-09-23 갱신** — 저장 위치(프로젝트 root 기준으로 분리), `patterns.storyboardSheets`,
> `patterns.guidePdf` 를 코드에 연결했다. `project.root` 제거나 `discovery` 로의 전환 같은
> schema 2 로의 구조 변경은 이번 라운드에서 하지 않았다(지금도 schema 1 그대로) — 아래
> 표들 중 "제거 대상"·"discovery" 관련 내용은 여전히 **방향 제안**이지 실행된 것이 아니다.

---

## 역할 분리 (가장 중요한 한 문장)

> **`project_rules.json` = 이 프로젝트의 구조·경로·단원·prototype 정보. 프로젝트마다 1개, Claude(또는 사람)가 분석해서 만든다.**
> **`rules/<recipe>/rules.json` = 이 recipe가 HTML을 만드는 방법. recipe마다 1개, 여러 프로젝트가 재사용한다.**

`rules`를 `project_rules.json` 안에 인라인으로 넣지 않는 이유: `rules.json`은 recipe 단위로 재사용되는 값이다. 같은 recipe(`cj_reading`)로 다른 프로젝트(같은 출판사의 다른 학년 등)를 만들면 그 프로젝트도 같은 `rules/cj_reading/rules.json`을 그대로 쓸 수 있어야 한다. 인라인으로 넣으면 프로젝트마다 규칙이 복제되어 이 재사용이 깨진다.

---

## `project_rules.json` 구조

```
project    { id, name, recipe }
paths      { storyboardDir, soundXlsx, contentsDir, guideDir }   ← root 기준 상대경로
units[]    [{ id, name, storyboard, ops, sheet, guide?, kr? }]
prototype  { units: [{ id, pages }] }                             ← name/type 등 중복 저장 안 함(units[]/proto_scan이 대신 제공)
patterns   { pageFilename, mp3Prefix, storyboardSheets:{syntax,miniVocab,dictation} }   ← 확인된 런타임 값
discovery  { storyboardFilename?, specialUnitFilename?, contentsFolder?,
             soundSheetGuess?, guidePdfGuess? }                   ← 최초 탐색 보조, 전부 선택, 없어도 정상 동작
```

| 필드 | 담는 것 | 누가 채우는가 | 없으면? |
|---|---|---|---|
| `project` | 이 프로젝트의 이름·식별자·사용 recipe | Claude가 최초 분석 때 1회 기록 | 생성기가 이 프로젝트를 다른 프로젝트와 구별 못함 |
| `paths` | storyboard/sound/contents/guide 폴더의 root 기준 **상대경로** | Claude가 실제 폴더를 열어 확인 | `units[]`에 개별 경로를 다 적지 않는 한 자료를 못 찾음 |
| `units[]` | 단원마다 다른 경로·시트명·id·이름 | Claude가 단원별로 실제 파일을 열어 확인 | 생성기가 어떤 단원이 있는지 전혀 모름 |
| `prototype` | 견본으로 분석에 쓴 단원 id + 그 페이지 목록만 | Claude가 "이 단원·이 페이지를 견본으로 쓰겠다"고 확인한 뒤 기록 | 프로토 분석 화면에 후보가 안 뜸(생성 자체는 영향 없음) |
| `patterns` | 실제로 확인해서 **런타임 내내 쓰는** 값(페이지 파일명 규칙, mp3 접두사, 스토리보드 시트명 3종) | Claude가 실제 파일 1개 이상을 열어 "이게 맞다"고 확인 | 코드가 그 값을 대신 리터럴로 쓰게 됨 = 하드코딩 재발 |
| `discovery` | **최초 탐색 보조용** 정규식·템플릿(단원 자동 발견용) | Claude가 새 단원을 찾는 규칙을 유추해서 적음(선택) | `discover()`가 새 단원을 자동으로 못 찾을 뿐, `units[]`를 Claude가 다 적어주면 **전혀 문제 없음** |

### `patterns` vs `discovery`

- **없으면 시스템이 못 도는 값 = `patterns`.** 틀리면 잘못된 값으로 그대로 생성된다(위험) — 그래서 반드시 Claude가 실물을 보고 확인한 값만 적는다.
- **없어도 `units[]`를 다 적으면 그만인 추측 = `discovery`.** 틀려도 `units[]`에 이미 적힌 단원을 덮지 않으므로 최악의 경우 "새 단원 후보 미발견"에 그친다.

### 반드시 필요한 필드 (C)

```
project.id, project.recipe
paths.storyboardDir, paths.soundXlsx, paths.contentsDir, paths.guideDir
patterns.pageFilename, patterns.mp3Prefix, patterns.storyboardSheets.{syntax,miniVocab,dictation}
units[].id, units[].name, units[].storyboard, units[].ops, units[].sheet
  (units[].guide, units[].kr — 각론이 있는 단원만 필요, 선택)
prototype.units[]  — 값이 비어 있어도(신규 프로젝트 최초 상태) 키 자체는 있어야 함
```

`discovery.*`는 전부 선택. `project.name`은 화면 표시용(코드가 읽지는 않지만 사람이 JSON을 구별하는 데 필요).

### 제거 대상 (D — 코드 반영 단계에서 실행)

| 값 | 있던 곳 | 이유 | 처리 |
|---|---|---|---|
| `project.root` | project_rules.json | settings.json과 이미 어긋나 있고 아무도 안 읽음 | 제거 — **settings.json이 root의 기준** |
| `paths.wordDicDir` | project_rules.json | 읽는 코드 없음(완전한 죽은 값) | 제거 |
| `storyboard.sheet.Dictation`/`.구문 해설`/`.미니 단어장`/`.Lesson 3_전자저작물용 지시문 모음` | `rules.json` | 코드가 찾는 키(`storyboard.sheet.syntax` 등)와 이름이 달라 영원히 안 먹음 | **연결 완료(2026-09-23)** — `patterns.storyboardSheets.{syntax,miniVocab,dictation}` 를 코드가 실제로 읽는다. `rules.json` 의 이 키들은 하위 호환으로 아직 안 지웠다(죽은 값인 채로 남음) |
| `sound.sheet`(`%d과`) | `rules.json` | `discovery.soundSheetGuess`와 중복 | 제거(project_rules.json 쪽이 기준) |
| `project.json` 파일 전체 | 별도 파일 | `units[]`와 완전 중복 | 폐기 대상(코드 단계에서 삭제) |

---

## `rules/<recipe>/rules.json`이 담는 것 (project_rules.json엔 절대 안 넣음)

```
popup.*                버튼 번호 등 HTML 조립 규칙
skeleton.*              페이지 css/js 조립 뼈대
assets.*                배경/제목 이미지 파일명 규칙
sound.col.* / idPattern / mp3.{sep,case}    엑셀 열 위치·ID 패턴·mp3 이름 변환 규칙(recipe 공통 처리 방식)
measure.*                여백 등 측정 규칙
```

---

## 새 프로젝트 검증 결과 (가상 프로젝트로 재확인)

| 검증 항목 | 결과 |
|---|---|
| 숫자 아닌 단원 ID(`UnitA` 등) | 통과 — `units[].id`가 원래 문자열. `special_lesson`으로 이미 실증됨 |
| 서로 다른 폴더 구조 | 통과 — `paths.*`가 전부 root 기준 상대경로 |
| 서로 다른 Excel 시트명 | 통과 — 음원 시트는 `units[].sheet`(단원별), 스토리보드 시트는 `patterns.storyboardSheets.*`(프로젝트 공통) |
| 서로 다른 mp3 파일명 규칙 | **부분 통과** — `patterns.mp3Prefix`로 "접두사 차이"는 해결. **조립 순서·구분자·코너 표기 자체가 다른 경우**는 스키마가 아니라 recipe(`rules.json`) 쪽 템플릿화가 별도로 필요(미해결로 정직하게 남김) |
| `discovery`를 완전히 비워도 되는가 | 통과 |

---

## 최종 JSON 예시 (일반화 — CJ 값 아님)

가상의 "OO출판사 중2 영어" 프로젝트. 폴더 구조·시트명·mp3 규칙·단원 ID 체계를 CJ와 의도적으로 다르게 만들어, 이 스키마가 특정 프로젝트에 묶여 있지 않음을 보인다.

```json
{
 "schema": 2,
 "project": {
  "id": "sample_publisher_mid2_eng",
  "name": "OO출판사 중2 영어",
  "recipe": "cj_reading"
 },
 "paths": {
  "storyboardDir": "scripts/storyboard",
  "soundXlsx": "audio/recording_master.xlsx",
  "contentsDir": "build/contents",
  "guideDir": "teacher_guide/pdf"
 },
 "patterns": {
  "pageFilename": "^(pg\\d{3}-\\d{2})\\.html$",
  "mp3Prefix": "M2",
  "storyboardSheets": {
   "syntax": "Grammar Notes",
   "miniVocab": "Word List",
   "dictation": "Listening Fill-in"
  }
 },
 "discovery": {
  "storyboardFilename": "Unit\\s*0*(\\d+|[A-Za-z]+)\\s*\\.xlsx$",
  "contentsFolder": "^unit[_-]?([A-Za-z0-9]+)$"
 },
 "units": [
  { "id": "1", "name": "Unit 1",
    "storyboard": "scripts/storyboard/unit1.xlsx",
    "ops": "build/contents/unit1/ops",
    "sheet": "Unit1" },
  { "id": "2", "name": "Unit 2",
    "storyboard": "scripts/storyboard/unit2.xlsx",
    "ops": "build/contents/unit2/ops",
    "sheet": "Unit2" },
  { "id": "review", "name": "Review",
    "storyboard": "scripts/storyboard/review.xlsx",
    "ops": "build/contents/review/ops",
    "sheet": "Review" },
  { "id": "special", "name": "Special Lesson",
    "storyboard": "scripts/storyboard/special.xlsx",
    "ops": "build/contents/special/ops",
    "sheet": "SP",
    "guide": "teacher_guide/pdf/special_guide.pdf",
    "kr": "guide" }
 ],
 "prototype": {
  "units": [
   { "id": "1", "pages": ["pg010-01"] },
   { "id": "special", "pages": ["pg090-01", "pg090-02"] }
  ]
 }
}
```

`discovery`에 `specialUnitFilename`을 안 넣은 것도 의도적이다 — 이 프로젝트는 파일명 규칙 하나로 숫자·문자 단원을 모두 찾을 수 있어서, CJ처럼 "숫자용/이름용" 정규식을 둘로 나눌 필요가 없다. **discovery는 프로젝트마다 있는 만큼만 채우면 되고, 스키마가 특정 키 조합을 강제하지 않는다.**

---

## Claude 최초 분석 단계에서 누가/어떻게 채우는가

1. `paths`/`units[]` — Claude가 프로젝트 폴더를 직접 열어, 실제로 존재하는 파일·폴더 경로를 확인하고 root 기준 상대경로로 적는다(추측 금지).
2. `patterns` — Claude가 실제 엑셀/HTML 파일을 최소 1개 이상 열어서 시트명·파일명 규칙이 그 모양인지 **확인한 뒤** 적는다.
3. `discovery` — Claude가 파일명 나열을 보고 "이런 규칙이면 자동으로 더 찾을 수 있겠다"고 판단되면 적는다(선택, 없어도 무방).
4. `prototype` — 사람이 "이 단원·이 페이지를 견본으로 쓰겠다"고 화면에서 고르면(또는 Claude가 제안하고 사람이 승인하면) 그 id·페이지만 기록한다.

---

## 기존 `project.json`/`settings.json`/`rules.json`과의 관계 (최종 결정)

| 정보 | 기준으로 삼을 곳 |
|---|---|
| 단원 목록(units) | **project_rules.json.** `project.json`은 폐기 대상 |
| 프로젝트 root(로컬 절대경로) | **settings.json.** root는 PC마다 다른 로컬 설정이지 프로젝트 사실이 아니다 |
| 스토리보드 시트명 3종 | **project_rules.json**(`patterns.storyboardSheets`). `rules.json`의 해당 키는 제거 대상 |
| 음원 시트 템플릿(`%d과`) | **project_rules.json**(`discovery.soundSheetGuess`). `rules.json`의 `sound.sheet`는 제거 대상(중복) |
| recipe id | **project_rules.json**(`project.recipe`)이 "프로젝트 사실"로서 기준 |
| popup 번호·조립 뼈대·측정값 | **`rules.json` 그대로.** recipe 고유 규칙 |

---

## 아직 부족한 점 (스키마가 아니라 코드/recipe 쪽 한계로 정직하게 남긴 것)

1. mp3 파일명이 접두사가 아니라 조립 순서 자체가 다른 프로젝트 — recipe(`rules.json`) 쪽 템플릿화(`sound.mp3.template` 같은 필드)가 필요. 이번 스키마 확정 범위 밖.
2. ~~`project_rules.json`이 지금은 생성기 폴더에 있어 프로젝트와 함께 안 옮겨감~~ **해결(2026-09-23)** — `<프로젝트 root>/project_rules.json` 으로 옮겼고, `project_rules_io.set_root()` 로 프로젝트마다 따로 읽는다(`ISSUES.md` #14 항목 1).
3. **부분 해결(2026-09-23)** — `patterns.storyboardSheets`·`patterns.guidePdf` 는 코드가 이제 읽는다.
   `patterns.mp3Prefix` 는 재확인 결과 실제로 필요한 자리(`read_gen.py` 의 mp3 파일명 조립 4곳,
   `3_%s_...` 리터럴)가 있음을 확인했지만 **아직 연결하지 않았다** — 전체 목록은 `ISSUES.md` #14 (4번).
