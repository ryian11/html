# project_rules.json 스키마 확정안 (최종)

> 코드 수정 없음. 이 문서는 이전 두 조사(`prototype-이후-전수분석.md`, 이번 문서의 1차 초안)를
> 이어받아 **project_rules.json 계약(schema)만** 확정한다. Python/UI 코드는 이 문서가 확정된
> 뒤에 별도로 진행한다.
>
> **문서 갱신 방침**: 새 파일을 만들지 않고 이 문서(`claude/project_rules.json-스키마-확정안.md`)를
> 그대로 갱신했다. `claude/project_rules.json-설계안.md`·`-구현결과.md`·`-최종검증.md`는 이전
> 구현 단계(문자열 patterns 도입 이전)의 기록이라 건드리지 않았다 — 이번 결정과 섞이면 오히려
> "무엇이 최신 결정인지" 헷갈리게 된다. 이후 이 스키마로 실제 코드를 구현하면
> `-구현결과.md` 계열 새 문서가 그때 다시 필요하다(지금은 아님).

---

## 1. 최종 구조 — 필드별 역할

```
project_rules.json
├── project     프로젝트 전체를 식별하는 공통 정보
├── paths       프로젝트 root 기준 상대경로 (자료 폴더 4종)
├── units[]     단원별 경로·자료 (기준 그대로 유지)
├── prototype   견본으로 쓸 단원·페이지 (참조만, 얇게)
├── patterns    Claude가 실제로 확인해서 "런타임에 쓰는" 확정값
└── discovery   최초 탐색 때만 쓰는 "보조 추측" (없어도 동작해야 함)

rules/<recipe>/rules.json   ← project_rules.json 밖의 별도 파일 (아래 1-7 참고)
```

| 필드 | 담는 것 | 누가 채우는가 | 없으면? |
|---|---|---|---|
| `project` | 이 프로젝트의 이름·식별자·사용 recipe | Claude가 최초 분석 때 1회 기록 | 생성기가 이 프로젝트를 다른 프로젝트와 구별 못함 |
| `paths` | storyboard/sound/contents/guide 폴더의 **root 기준 상대경로** | Claude가 실제 폴더를 열어 확인 | `units[]`에 개별 경로를 다 적지 않는 한 자료를 못 찾음 |
| `units[]` | 단원마다 다른 경로·시트명·id·이름 | Claude가 단원별로 실제 파일을 열어 확인 | 생성기가 어떤 단원이 있는지 전혀 모름 |
| `prototype` | 견본으로 분석에 쓴 단원 id + 그 페이지 목록만 | Claude가 "이 단원·이 페이지를 견본으로 쓰겠다"고 확인한 뒤 기록 | 프로토 분석 화면에 후보가 안 뜸(생성 자체는 영향 없음) |
| `patterns` | 실제로 확인해서 **런타임 내내 쓰는** 값(페이지 파일명 규칙, mp3 접두사, 스토리보드 시트명 3종) | Claude가 실제 파일 1개 이상을 열어 "이게 맞다"고 확인 | 코드가 그 값을 대신 리터럴로 쓰게 됨 = 하드코딩 재발 |
| `discovery` | **최초 탐색 보조용** 정규식·템플릿(단원 자동 발견용) | Claude가 새 단원을 찾는 규칙을 유추해서 적음(선택) | discover()가 새 단원을 자동으로 못 찾을 뿐, `units[]`를 Claude가 다 적어주면 **전혀 문제 없음** |
| *(참고)* `rules` | recipe가 "HTML을 만드는 방법"(팝업 번호, 조립 뼈대, 측정값 등) | Claude가 프로토 페이지를 분석해 채움(`proto_scan`) | — project_rules.json에는 없음. 아래 1-7 참고 |

### 1-7. `rules`는 왜 project_rules.json 안에 없는가

프로젝트 지침 8번의 기본 방향(`{project, paths, units, prototype, rules}`)에는 `rules`가 들어 있었지만, 실제 코드 분석 결과 **`rules`는 별도 파일(`rules/<recipe>/rules.json`)로 두는 것이 더 적절하다** — 지침 8번이 허용하는 예외("실제 코드 분석 결과 더 적절한 구조가 있으면 설명") 조건에 해당한다.

이유: `rules.json`은 **recipe 단위**로 재사용되는 값이다. "CJ Reading"이라는 recipe로 만드는 프로젝트가 나중에 하나 더 생기면(예: 같은 출판사의 다른 학년 교재), 그 프로젝트도 같은 `rules/cj_reading/rules.json`을 그대로 쓸 수 있어야 한다. `rules`를 `project_rules.json` 안에 인라인으로 넣으면 프로젝트마다 규칙이 따로 복제되어 이 재사용이 깨진다. 그래서 `project_rules.json`은 `project.recipe` 필드로 "이 프로젝트가 어떤 recipe를 쓰는지"만 가리키고, 실제 규칙은 그 recipe의 파일에서 읽는다 — **역할 분리이지 누락이 아니다.**

---

## 2. `patterns` vs `discovery` — 정의 검증

사용자가 제안한 구분:
> `patterns`: Claude가 실제 자료를 분석해서 확인한 값이며 런타임에서 사용하는 값
> `discovery`: 최초 분석 시 자료를 찾기 위한 보조 정보

**이 구분은 맞다.** 다만 `discovery`의 성격을 한 가지 더 분명히 해 둘 필요가 있다:

* `patterns`는 **"이 값이 맞다"고 Claude가 실물을 보고 확인한 사실**이다. 예: 실제로 열어 본 엑셀에 `'구문 해설'` 탭이 있었다, 실제 mp3 파일 이름이 `3_1_read_...`로 시작했다. → **항상 옳아야 하고, 코드는 이 값을 무조건 신뢰한다.**
* `discovery`는 **Claude가 확인한 사실이 아니라, "새 단원을 자동으로 더 찾아낼 때 시도해 볼 규칙"**이다. 정규식이나 `%d` 템플릿 형태라 애초에 100% 확신을 담보하지 않는다(예: `Lesson\s*0*(\d+)\.xlsx$`는 "이런 모양이면 단원 파일일 것이다"라는 추측이지, 확인된 사실이 아니다). → **틀려도 된다.** `units[]`에 이미 적힌 단원은 `discovery`가 절대 덮지 않는다(현재도 `cj_reading.py:147-151` 주석에 이 원칙이 명시돼 있음, 코드도 그렇게 동작함).

그래서 실질적인 차이는 "확인 여부"보다 **"없어도 시스템이 정상 동작하는가"**에 있다:

| | `patterns` | `discovery` |
|---|---|---|
| 없으면 | 코드가 하드코딩 리터럴로 대체(퇴행) → **문제** | discover()가 새 단원을 못 찾을 뿐, Claude가 `units[]`를 전부 적어주면 **문제 없음** |
| 틀리면 | 잘못된 값으로 그대로 생성됨(위험) | 엉뚱한 후보를 잘못 찾아도 `units[]`를 덮지 않으므로 최악의 경우 "후보 미발견"에 그침(상대적으로 안전) |
| 3장 가상 프로젝트에서 | 반드시 채워야 함 | **비워도 된다**(3장에서 실제로 빈 채로 검증함) |

**결론**: 사용자의 구분이 정확하고, 이번 문서는 그 구분을 그대로 최종 채택한다. 이름도 `patterns`/`discovery` 그대로 유지한다(현재 CJ의 `patterns.soundSheet`·`patterns.guidePdf`는 성격상 discovery로 옮긴다 — 1차 초안과 동일 결정).

---

## 3. 가상 프로젝트 검증

가상 프로젝트: 단원 `UnitA`/`UnitB`/`Review`/`Special`(숫자 없음), CJ와 전혀 다른 폴더 구조, 다른 엑셀 시트명, 다른 mp3 파일명 규칙.

| 검증 항목 | 결과 | 근거 |
|---|---|---|
| 숫자 아닌 단원 ID(UnitA 등) | **통과** | `units[].id`가 원래 문자열. `special_lesson`으로 이미 실증됨(직전 작업) |
| 서로 다른 폴더 구조 | **통과** | `paths.*`가 전부 root 기준 **상대경로**라 폴더 이름·깊이가 달라도 그대로 적으면 됨. `units[].ops`/`storyboard`도 마찬가지로 자유 경로 |
| 서로 다른 Excel 시트명 | **통과** | 음원 시트는 `units[].sheet`(단원별), 스토리보드 시트는 `patterns.storyboardSheets.{syntax,miniVocab,dictation}`(프로젝트 공통) — 둘 다 이번에 JSON화한 값으로 임의 이름을 그대로 담을 수 있음 |
| 서로 다른 mp3 파일명 규칙 | **부분 통과 — 한계 있음** | `patterns.mp3Prefix`로 "접두사가 다른 경우"(CJ의 `3_`)는 해결된다. 하지만 실제 코드(`read_gen.py:226` 등)는 `'{prefix}_{unit}_{corner}_{id}'`라는 **고정된 조립 순서** 자체를 리터럴로 짜 놓았다. 접두사가 아니라 **순서·구분자·코너 표기 자체가 다른 프로젝트**(예: `read_L{unit}_{id}.mp3`처럼 아예 다른 모양)라면 `mp3Prefix` 하나로는 못 덮는다. 이건 "프로젝트 사실"이 아니라 "recipe가 파일명을 조립하는 방식" 쪽에 가까운 문제라, **project_rules.json의 몫이 아니라 recipe의 `rules.json`이 템플릿 문자열(`sound.mp3.template` 같은)을 갖도록 확장해야 하는 부분**이다. 이번 스키마 확정 범위 밖이므로 5장에 "부족한 점"으로 정리한다 |
| `discovery`를 완전히 비워도 되는가 | **통과** | 위 표 구조 자체가 `discovery: {}`로도 동작하도록 설계됨(2장) |

**요약**: 6개 중 5개는 이번 스키마로 완전히 통과, mp3 파일명 규칙은 "접두사"까지는 통과하지만 "조립 방식 자체가 다른 경우"는 스키마가 아니라 recipe 쪽(`rules.json`) 확장이 필요하다 — 정직하게 미해결로 남긴다.

---

## 4. 반드시 필요한 필드 / 제거 가능한 필드 / 기존 파일과의 중복 해소

### 4-1. 기존 파일과 중복되는 정보 — 기준 결정

| 정보 | `project.json` | `settings.json` | `rules.json` | `project_rules.json` | **기준으로 삼을 곳** |
|---|---|---|---|---|---|
| 단원 목록(units) | 있음(9개 완전 중복) | 없음 | 없음 | 있음 | **project_rules.json.** `project.json`은 더 이상 기준이 아님(파일 자체는 4-2에서 폐기 대상) |
| 프로젝트 root(로컬 절대경로) | 없음 | 있음(`E:\00_works\...`) | 없음 | 있음(지금 값, 안 읽힘) | **settings.json.** root는 PC마다 다른 "이 프로젝트를 지금 어디 풀어놨는가"라 로컬 설정이지 프로젝트 사실이 아니다. `project_rules.json`에서 `project.root` 제거 |
| 스토리보드 시트명(구문 해설 등 3종) | 없음 | 없음 | 있음(키 불일치로 죽어 있음) | 있음(신규 `patterns.storyboardSheets`) | **project_rules.json.** `rules.json`의 해당 4개 키(`storyboard.sheet.*`) 제거 대상 |
| 음원 시트 템플릿(`%d과`) | 없음 | 없음 | 있음(`sound.sheet`) | 있음(`discovery.soundSheetGuess`) | **project_rules.json.** `rules.json`의 `sound.sheet` 제거 대상(중복) |
| recipe id | 최상위 키로 암시 | 최상위 키로 암시 | `recipe` 필드로 있음 | `project.recipe`로 있음 | **project_rules.json이 "프로젝트 사실"로서 기준.** `settings.json`/`project.json`이 recipe를 키로 쓰는 건 저장 방식일 뿐, 프로젝트가 recipe를 "선택"했다는 사실 자체는 project_rules.json에 있어야 함 |
| popup 번호·조립 뼈대·측정값 | 없음 | 없음 | 있음 | 없음(의도적) | **rules.json 그대로.** recipe 고유 규칙(1-7 참고) |

### 4-2. 제거 가능한 필드(D)

* `project.root` — settings.json이 기준이므로 project_rules.json에서 제거
* `paths.wordDicDir` — 코드 어디에서도 읽지 않는 완전한 죽은 값(확인됨), 제거
* `project.json` 파일 자체 — units[]가 project_rules.json에 완전히 있으므로 더 이상 역할 없음. (파일 삭제는 코드 단계에서, 지금은 "기준에서 제외"만 결정)
* `rules.json`의 `storyboard.sheet.Dictation`/`.구문 해설`/`.미니 단어장`/`.Lesson 3_전자저작물용 지시문 모음` 4개 키 — `patterns.storyboardSheets`로 이관되므로 제거 대상
* `rules.json`의 `sound.sheet` 키 — `discovery.soundSheetGuess`와 중복, 제거 대상

### 4-3. 반드시 필요한 필드(C)

```
project.id, project.recipe
paths.storyboardDir, paths.soundXlsx, paths.contentsDir, paths.guideDir
patterns.pageFilename, patterns.mp3Prefix, patterns.storyboardSheets.{syntax,miniVocab,dictation}
units[].id, units[].name, units[].storyboard, units[].ops, units[].sheet
  (units[].guide, units[].kr — 각론이 있는 단원만 필요, 선택)
prototype.units[]  — 값이 비어 있어도(신규 프로젝트 최초 상태) 키 자체는 있어야 함
```

`discovery.*`는 전부 선택(3장에서 빈 채로 검증됨). `project.name`은 화면 표시용으로만 쓰이므로 "필수는 아니지만 있으면 좋음"(코드가 실제로 읽지는 않지만, 사람이 JSON만 보고 프로젝트를 구별하는 데 필요).

---

## 5. "이 파일 하나만 다른 PC에 넣으면 충분한가" — 재검토

이 질문은 사실 두 가지를 섞어서 묻는 것이라 나눠서 답한다.

**(1) 스키마 내용 자체가 충분한가?** — 대체로 그렇다. 3장에서 5개 항목은 완전히 통과했고, mp3 조립 방식(순서 자체가 다른 경우)만 스키마 밖의 recipe 확장이 필요하다고 정직하게 남겨 뒀다.

**(2) `project_rules.json` "파일 한 개"만 있으면 되는가?** — **아니다, 원래 설계상 한 개만으로는 안 되고, 그럴 필요도 없다.** 새 PC에서 이 recipe로 이 프로젝트를 만들려면 실제로는:

* `project_rules.json` — **프로젝트마다** 새로 필요 (Claude가 매번 분석해서 만드는 것)
* `rules/<recipe>/rules.json` — **recipe마다** 필요하지만, 같은 recipe(CJ Reading)를 쓰는 다른 프로젝트라면 **이미 있는 걸 그대로 재사용**한다(1-7의 이유)
* `settings.json`의 root 한 줄 — PC마다 새로 필요하지만, 이건 Claude 분석이 아니라 **사람이 UI에서 폴더 한 번 지정**하면 되는 값(자연스러운 로컬 설정, 결함 아님)

즉 "project_rules.json 하나로 충분해야 한다"는 목표는 **"Claude가 프로젝트마다 새로 분석해서 만들어야 하는 파일이 이것 하나여야 한다"**는 뜻으로 읽는 게 맞고, 그 기준으로는 **이번 스키마가 맞다.** recipe rules.json은 "프로젝트마다"가 아니라 "recipe마다" 한 번만 있으면 되는 것이라 같은 목표를 위반하지 않는다.

**아직 부족한 점(구체적으로)**:
1. mp3 파일명이 접두사가 아니라 조립 순서 자체가 다른 프로젝트 — 3장에서 확인, recipe(rules.json) 쪽 템플릿화가 필요
2. `project_rules.json`이 지금은 생성기 폴더에 있어 프로젝트와 함께 안 옮겨감 — **스키마 문제가 아니라 저장 위치 문제**(코드 단계, 6장 1순위로 이미 알려짐)
3. 이번에 새로 정의한 `patterns.storyboardSheets`/`mp3Prefix`/`discovery.*`를 코드가 아직 안 읽음 — **스키마 문제가 아니라 연결 문제**(코드 단계)

2·3번은 "스키마가 부족해서"가 아니라 "코드가 아직 이 스키마를 안 따라서" 생기는 문제라, 이번 단계(스키마 확정)의 책임 밖이다. 1번만 순수하게 스키마/recipe 설계의 한계로 남는다.

---

## 6. 최종 JSON 예시 (일반화 — CJ 값 복사 아님)

가상의 "OO출판사 중2 영어" 프로젝트를 가정한다. 폴더 구조·시트명·mp3 규칙·단원 ID 체계를 CJ와 의도적으로 다르게 만들어 이 스키마가 특정 프로젝트에 묶여 있지 않음을 보인다.

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

`discovery`에 `specialUnitFilename`을 안 넣은 것도 의도적이다 — 이 프로젝트는 파일명 규칙 하나(`Unit\s*0*(\d+|[A-Za-z]+)\.xlsx$`)로 숫자·문자 단원을 모두 찾을 수 있어서, CJ처럼 "숫자용/이름용" 정규식을 굳이 둘로 나눌 필요가 없다는 걸 보여준다 — **discovery는 프로젝트마다 있는 만큼만 채우면 되고, 스키마가 특정 키 조합을 강제하지 않는다.**

---

## 7. 정리

**최종 확정 JSON 구조**: 1장의 트리 그대로 — `project`, `paths`, `units[]`, `prototype`, `patterns`, `discovery` 6개 최상위 키(+ `schema` 버전 숫자). `rules`는 프로젝트당이 아니라 recipe당 별도 파일로 존재(1-7).

**각 필드의 의미**: 1장·4장 표 참고.

**Claude 최초 분석 단계에서 누가/어떻게 채우는가**:
1. `paths`/`units[]` — Claude가 프로젝트 폴더를 직접 열어, 실제로 존재하는 파일·폴더 경로를 확인하고 root 기준 상대경로로 적는다(추측 금지 — 지침 4번).
2. `patterns` — Claude가 실제 엑셀/HTML 파일을 최소 1개 이상 열어서 시트명·파일명 규칙이 그 모양인지 **확인한 뒤** 적는다.
3. `discovery` — Claude가 파일명 나열을 보고 "이런 규칙이면 자동으로 더 찾을 수 있겠다"고 판단되면 적는다(선택, 없어도 무방).
4. `prototype` — 사람이 "이 단원·이 페이지를 견본으로 쓰겠다"고 화면에서 고르면(또는 Claude가 제안하고 사람이 승인하면) 그 id·페이지만 기록한다(현재 UI 흐름과 동일).

**일반 HTML 생성기가 읽어야 하는 값**: 위 "반드시 필요한 필드"(4-3) 전부 + `discovery`(있으면 참고, 없어도 정상 동작). `rules`는 project_rules.json이 아니라 `project.recipe`가 가리키는 `rules/<recipe>/rules.json`에서 따로 읽는다.

**기존 `project.json`/`settings.json`/recipe `rules.json`과의 관계**: 4-1 표가 최종 결정이다 — 단원 목록은 project_rules.json이 이기고 project.json은 폐기 대상, root는 settings.json이 이기고 project_rules.json의 project.root는 제거, 스토리보드 시트명은 project_rules.json이 이기고 rules.json의 해당 키는 제거, recipe의 생성 규칙(popup·skeleton·측정값)은 그대로 rules.json 소관.

---

# 최종 답변 요약

## A. 최종 스키마
```
project_rules.json
├ project   {id, name, recipe}
├ paths     {storyboardDir, soundXlsx, contentsDir, guideDir}
├ units[]   [{id, name, storyboard, ops, sheet, guide?, kr?}]
├ prototype {units: [{id, pages}]}
├ patterns  {pageFilename, mp3Prefix, storyboardSheets:{syntax,miniVocab,dictation}}
└ discovery {storyboardFilename?, specialUnitFilename?, contentsFolder?, soundSheetGuess?, guidePdfGuess?}  (전부 선택)

rules/<recipe>/rules.json  — project_rules.json 밖, recipe 단위로 재사용(의도적 분리)
```

## B. 실제 JSON 예시
→ 6장 참고(가상의 "OO출판사 중2 영어" 예시, CJ 값 아님).

## C. 반드시 필요한 필드
`project.id/recipe`, `paths.*` 4종, `units[].{id,name,storyboard,ops,sheet}`, `patterns.pageFilename/mp3Prefix/storyboardSheets.*`. (`units[].guide/kr`는 각론 있는 단원만, `prototype`/`discovery`는 값은 비어도 되지만 키는 존재)

## D. 제거 가능한 필드
`project.root`(→settings.json이 기준), `paths.wordDicDir`(죽은 값), `project.json` 파일 전체(→units[]와 중복), `rules.json`의 `storyboard.sheet.*` 4개 키·`sound.sheet` 키(→patterns/discovery로 이관, 지금은 키 이름이 안 맞아 죽어 있음).

## E. 기존 파일들과의 관계
`project.json`은 폐기 대상(4-1), `settings.json`은 **root(로컬 경로)의 기준**으로 그대로 유지, `rules/<recipe>/rules.json`은 **recipe의 생성 규칙**(popup·skeleton·측정값·mp3 sep/case)만 남기고 프로젝트 고유 정보(시트명 4종·%d과 템플릿)는 project_rules.json으로 이관. 셋 다 폐기되는 게 아니라 **역할이 겹치던 부분만 정리**된다.

## F. 다음 구현 단계
스키마는 이번으로 확정. 다음 단계(아직 착수 안 함)는 이전 문서(`prototype-이후-전수분석.md` 9장)에 정리된 순서를 따른다 — 1) project_rules.json을 프로젝트 폴더 안으로 이동, 2) `patterns.storyboardSheets`/`mp3Prefix`/`paths.guideDir`를 코드가 실제로 읽게 연결, 3) `patterns.pageFilename`을 생성 경로까지 연결, 4) `read_paths.py`의 추측 폴백을 "없으면 오류"로 전환, 5) `proto_scan.py`에 남은 `'%d과'` 2곳 정리, 6) `project.json`/`rules.json`의 이관 대상 키 제거. **사용자 확인 전에는 착수하지 않는다.**
