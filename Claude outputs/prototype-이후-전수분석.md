# prototype 작업 이후 — 프로젝트 종속성 전수 분석

> 조사 기준: device 상 실제 파일, git `HEAD = a65e9a2` (audit 대상 소스/JSON은 `git diff` 결과 **변경 없음** 확인).
> 조사 방식: 읽기 전용(cat / sed / grep / git). **코드·JSON·UI 를 하나도 수정하지 않았음.**
> 조사 범위: `read_paths.py`, `project_io.py`, `project_rules_io.py`, `recipes/cj_reading.py`, `proto_scan.py`,
> `read_import.py`, `read_gen.py`, `read_measure.py`, `read_verify.py`, `layout_edit.py`, `rules_io.py`,
> `runner.py`, `app.py`, `app_page.py`, `project_rules.json`, `project.json`, `settings.json`, `rules/cj_reading/rules.json`.

---

## 1. 현재 상태 요약

**현재 목표 달성도: C**

(A = 프로젝트 종속성 거의 없음 … F = 최종 구조와 상당히 다름)

**C 로 본 이유 — 두 층이 서로 다른 상태다.**

| 층 | 상태 | 평가 |
|---|---|---|
| **바깥층** (프로젝트 선택 · 단원 목록 · prototype 선택 · 경로 주입) | project_rules.json 이 실제로 기준이 됨. prototype 은 이번 작업으로 완전히 JSON 기반이 됨 | **A~B** |
| **가운데층** (discover / patterns / rules.json 역할 분리) | patterns 는 일부만 실제로 쓰이고, discover() 가 여전히 JSON 을 "덮진 않지만 늘린다". rules.json 에 프로젝트 고유값이 섞여 있음 | **C** |
| **안층** (read_import.py · read_gen.py — 실제 자료를 읽고 HTML 을 찍는 곳) | 시트 이름 · mp3 접두사 `3_` · 페이지 파일명 `p%s_%02d` · 지도서 PDF 좌표 등이 **코드에 직접 박혀 있음**. JSON 으로 못 바꿈 | **D~F** |

즉 "프로젝트를 고르고 단원을 고르는 데까지"는 목표 구조에 가깝지만,
"그 다음 실제로 자료를 읽고 HTML 을 찍는 부분"은 아직 2026 CJ 중3 전용 코드다.
**새 프로젝트를 넣으면 extract 단계에서 반드시 코드 수정이 필요하다.**

> 이 평가는 진단용이며, 이번 작업에서 **코드는 한 줄도 수정하지 않았다.**

---

## 2. 이미 해결된 것

| 영역 | 현재 상태 | 근거 |
|---|---|---|
| prototype 단원 목록 | project_rules.json `prototype.units[].id` 만 UI 드롭다운에 나옴. 폴더를 뒤져 후보를 늘리지 않음 | `recipes/cj_reading.py:428-435 prototype_units()` → `project_rules_io.py:126-133 proto_units()` → `app.py:406 _recipe_info()` → `app_page.py:255-261` (select 태그) |
| prototype 페이지 목록 | JSON `prototype.units[].pages` 만 노출. 폴더에 더 있어도 화면에 안 나옴 | `recipes/cj_reading.py:415-425 proto_pages()` → `project_rules_io.py:136-145 proto_pages(unit_id)` (폴더 접근 코드 없음) → `app.py:451` → `app_page.py:418-423` |
| 문자열 단원 id 지원 (prototype) | `proto_lesson()` 이 `int()` 변환 없이 문자열 그대로 돌려줌. JSON 에 없는 id 는 `None` | `recipes/cj_reading.py:401-412` — `ids = {u.get('id') for u in PR.proto_units()}; return v if v in ids else None` |
| prototype ops 폴더 | `read_paths.ops()` 의 `lesson%02d` 추측 폴백을 **타지 않고** 단원 등록부(JSON) 에서 직접 가져옴 | `recipes/cj_reading.py:384-398 proto_ops()` — `P.unit(n).get('ops')` |
| proto_scan 의 `'%d과'` 생성 제거(부분) | `scan()` 이 `sound_sheet` 를 인자로 받고, 호출자가 JSON/rules 에서 구해 넘김 | `recipes/cj_reading.py:453-463` → `proto_scan.py:161-162, 276` |
| 자료 경로(4종) JSON 화 | storyboardDir / soundXlsx / wordDicDir / contentsDir 를 project_rules.json 에서 읽어 read_paths 전역에 주입 | `recipes/cj_reading.py:71-83 setup()` → `read_paths.py:15-21` 전역 덮어쓰기 |
| 단원 목록·단원별 sheet·guide PDF | project_rules.json `units[]` 이 기준. UI 에서 수정도 가능 | `recipes/cj_reading.py:194-227 units()/_register()` → `read_paths.UNITS` → `app.py:267-289 POST /api/project` |
| 단원 id 정렬이 문자열 id 를 견딤 | `_sortkey()` 가 숫자/문자 분기 | `recipes/cj_reading.py:189-191`, `app.py:286-287` |
| 마이그레이션 안전장치 | project_rules.json 이 없을 때만 코드 기본값으로 1회 생성. 이후엔 JSON 이 기준 | `project_rules_io.py:149-170 ensure_migrated()` |

---

## 3. 아직 남은 프로젝트 종속성

> ★ = 새 프로젝트에서 **거의 확실히** 터지는 것

| 파일 | 위치(줄번호) | 문제 | 새 프로젝트에서 발생할 문제 | 해결 방향 |
|---|---|---|---|---|
| ★ `read_gen.py` | `105` `ws = wb_['미니 단어장']` (`load_words()`) | 스토리보드 시트 이름이 코드에 박힘. `R()` 도 안 거침 | 시트명이 다르면 `KeyError: '미니 단어장'` 로 build 실패 | `R('storyboard.sheet.miniVocab', …)` 경유 + project_rules.json `patterns` 또는 rules.json 에 등재 |
| ★ `read_gen.py` | `133` `openpyxl…['구문 해설']` (`load_syntax()`) | 위와 동일 | `KeyError: '구문 해설'` | 동일 |
| ★ `read_gen.py` | `226`, `737`, `762`, `909` `'3_%s_read_%s'`, `'3_%s_word_%02d'` | mp3 파일명의 **학년 접두사 `3_` 이 리터럴** | 다른 교재(중2, 고1 등)는 mp3 를 전부 못 찾음. **오류 없이 잘못된 파일명으로 생성됨(조용한 실패)** | `sound.mp3` 규칙을 접두사까지 포함하도록 확장하거나 `units[].mp3Prefix` 신설 |
| ★ `read_import.py` | `824` `'3_%s_read_%s'` | 위와 동일(label 블록) | 동일 | 동일 |
| ★ `read_import.py` | `129` `P.unit(n).get('sheet') or (R('sound.sheet','%d과') % int(n))` | JSON 에 `sheet` 가 없고 단원 id 가 문자열이면 `int(n)` 이 `ValueError` | 문자열 단원(UnitA)에서 extract 크래시 | `str.isdigit()` 분기 + "시트 이름을 모른다" 오류로 안내 (proto_scan.py:106-112 이 이미 그렇게 함) |
| ★ `read_import.py` | `159` `R('storyboard.sheet.syntax', '구문 해설')` | rules.json 의 키는 `storyboard.sheet.구문 해설` 이라 **절대 매칭되지 않음** → 항상 코드 기본값 사용 | 시트명이 다르면 `KeyError` | rules.json 키 이름 체계와 코드 키를 일치시켜야 함 (4번 항목 참조) |
| ★ `read_import.py` | `856-872` `GUIDE_LABEL='본문 해석'`, `GUIDE_MID=341.0`, `GUIDE_NEAR/GAP/MINSZ/INDENT/ROW` | 지도서 PDF 의 **지면 좌표·칼럼 위치**가 코드 상수 | 다른 출판사 PDF 는 해석 추출 전부 실패(`GuideError`) | 이 값 묶음을 project_rules.json `guide` 블록으로 이동 |
| ★ `read_import.py` | `557-566 guide_kr()` — `wb[wb.sheetnames[0]]`, `r[4]`, `r[2]` | 지시문 시트를 "첫 시트"로 가정하고 **열 번호를 리터럴로** 사용 | 열 구성이 다르면 조용히 빈 값/오류 | `R('storyboard.dir.col*', …)` 로 빼기 |
| ★ `read_import.py` | `279` `'p%s_%02d' % (pg, 2 if pi==0 else 1)`, `585` `'p%s_01' % firstpg` | 페이지 파일명 규칙 `p###_##` 이 코드에 박힘 | `patterns.pageFilename` 을 JSON 에 넣어도 **이 경로는 안 읽음** → 파일명 불일치 | `patterns.pageFilename` 을 생성 쪽에서도 쓰게 통일 |
| ★ `read_gen.py` | `1193` `ORDER[0][:4] + '_01'`, `1197` `ORDER[0] + '_all'` | `p###` 4글자 고정 슬라이스 | 페이지명 길이가 다르면 잘못된 파일명 | 동일 |
| `read_gen.py` | `36` `'dictation' in n.lower()` | 딕테이션 유무를 시트명 문자열로 판정 | 다른 프로젝트의 딕테이션 시트명이 다르면 단추·팝업이 통째로 빠짐 | `R('storyboard.sheet.dictation', …)` |
| `read_import.py` | `394,428,488,512,549,550,570` `'read' / 'word' / 'mission' / 'question' / 'thinkaboutthis' / 'readsmart'` | 음원 코너 키가 코드 리터럴 | 코너 이름 체계가 다르면 Reading 쪽을 **하나도 못 찾아** `SystemExit('Reading 쪽을 못 찾았습니다')` | rules.json `sound.corner` 를 실제로 쓰도록(지금은 죽은 값) |
| `read_import.py` | `291-293 img_sizes()` — `read_bg.png`, `title.png`, `s_title01~04.png` | 이미지 파일명 리터럴. rules.json `assets.bg/title` 를 **안 읽음** | 이미지명이 다르면 제목 유무 판정이 틀림 | `R('assets.bg'/'assets.title')` 경유 |
| ★ `read_paths.py` | `5` `ROOT = r'E:\00_works\2026\2026_cj_midd3_eng'` | 특정 PC·특정 프로젝트 절대경로가 모듈 최상단 | `setup()` 이 안 불린 경로(예: `proto_scan.py` 를 CLI 로 직접 실행)에서는 이 값이 그대로 쓰임 | 기본값을 `None` 으로 두고 미설정 시 오류 |
| ★ `read_paths.py` | `15-20` `SB_DIR`, `SB_NAME`, `SND`, `WORDDIC`, `CONTENTS` | CJ 폴더명·파일명이 모듈 상수 | `setup()` 전에 import 되는 모든 경로에서 CJ 값이 유효한 것처럼 보임 | 동일 |
| ★ `read_paths.py` | `49` `SB_NAME % int(n)`, `56` `'lesson%02d' % int(n)` | 단원 등록부에 없으면 **숫자 단원을 가정해 경로를 추측** | 문자열 단원 id 에서 `ValueError`, 또는 엉뚱한 폴더 접근 | 지침 4번(추측 금지) 위반 — 등록부에 없으면 오류로 알려야 함 |
| ★ `read_paths.py` | `81` `'*각론%d*.pdf' % n`, `83-84` `ROOT/'03_PDF'` | 지도서 PDF 이름 규칙·폴더명이 코드에 박힘. **`patterns.guidePdf` 를 아무도 안 읽음** | 문자열 단원이면 `TypeError`(%d 에 str), 새 프로젝트는 PDF 를 못 찾음 | `PR.pattern('guidePdf')` 를 실제로 읽게 연결 |
| `read_import.py` | `186` `'지도서 각론%d PDF …' % n` | 경고문에 `%d` — 문자열 단원이면 `TypeError` | 문자열 단원 + PDF 없음 조합에서 크래시 | `%s` 로 |
| ★ `recipes/cj_reading.py` | `43-56` `LEGACY_PATHS`, `LEGACY_PATTERNS` | CJ 전용 폴더명·파일명·정규식이 **레시피 코드**에 상수로 존재 | 마이그레이션용이라 해도, `setup()` 76-79 줄에서 `pp.get(...) or LEGACY_PATHS[...]` 로 **상시 폴백**됨 → JSON 에 키가 없으면 조용히 CJ 값 사용 | 폴백 대신 "JSON 에 없음" 오류/경고 |
| ★ `recipes/cj_reading.py` | `83` `P.GEN = os.path.join(root, '_딕테이션_생성기')` | 생성기 폴더 이름이 리터럴 | 폴더명을 바꾸면 틀린 경로. (실제로 `P.GEN` 은 아무 데서도 안 읽힘 — 죽은 대입) | 제거 또는 `GEN` 전역 사용 |
| `recipes/cj_reading.py` | `166` `'%d단원' % int(...)`, `179` `os.path.join(P.CONTENTS, d, 'ops')` | 단원 이름 형식과 `ops` 하위폴더명이 리터럴 | `ops` 가 아닌 구조면 discover 가 단원을 하나도 못 찾음 | `patterns.opsFolder` 신설 |
| `proto_scan.py` | `112` `want = '%d과' % int(s)` | **`'%d과'` 하드코딩이 아직 남아 있음** (sheet 인자가 없고 id 가 숫자일 때의 폴백) | CJ 외 프로젝트에서 숫자 단원이면 없는 시트를 찾게 됨 | 폴백 제거(바로 위 106-111 줄의 오류 경로로 통일) |
| `proto_scan.py` | `283` `rules_io.put(d,'sound.sheet','%d과', …)` | 분석 결과에 **CJ 고유 시트명 템플릿을 rules.json 으로 써 넣음** | 다른 프로젝트의 rules.json 이 `'%d과'` 로 오염됨 | project_rules.json 쪽으로 (5번·E 항목) |
| `proto_scan.py` | `86` `url\(\.\./images/(p\d{3}_\d{2})/…\)`, `52` `^p(\d+)` | `page_pattern` 인자를 받아 놓고 CSS/페이지번호 파싱은 여전히 `p###_##` 고정 | 페이지 이름 규칙이 다르면 이미지 규칙을 못 뽑음 | 전달받은 패턴을 여기서도 사용 |
| `proto_scan.py` | `341-343 main()` | CLI 경로가 `int(lesson)` 강제 | 문자열 단원을 CLI 로 분석 불가 (UI 경로는 정상) | `isdigit()` 분기 |
| `rules_io.py` | `153,214,245,281` `rid='cj_reading'` 기본 인자 | 레시피 id 기본값이 리터럴 | 레시피가 늘면 엉뚱한 레시피 규칙을 읽음 | 기본값 제거 |
| `app.py` | `223,239,326,344` `q.get('recipe',['cj_reading'])` / `body.get('recipe') or 'cj_reading'` | API 기본 레시피가 리터럴 | 동일 | 동일 |
| ★ `project_rules_io.py` | `36` `PATH = os.path.join(HERE,'project_rules.json')` | **생성기 설치당 project_rules.json 이 딱 하나** | 두 번째 프로젝트를 열면 `exists()` 가 True 라 `ensure_migrated()` 가 **이전 프로젝트 JSON 을 그대로 반환** → 경로·단원·prototype 이 전부 옛 프로젝트 것 | `<root>/project_rules.json` 또는 `rules/<recipe>/<projectId>.json` 로 프로젝트별 분리 |
| ★ `recipes/cj_reading.py` | `71-83 setup()` | `project_rules.json` 의 `project.root` 와 현재 `ctx['root']` 가 **다른지 검사하지 않음** | 프로젝트를 바꿔도 조용히 옛 JSON 을 씀 (위 항목과 세트) | root 불일치 시 경고/재생성 |

---

## 4. JSON에 있는데 사용되지 않는 설정 (dead configuration)

### 4-1. `project_rules.json`

| JSON 위치 | 코드 사용 여부 | 문제 |
|---|---|---|
| `project.name` | **안 읽음** (쓰기만: `project_rules_io.py:97,163`) | 표시용으로도 안 쓰임 |
| `project.root` | **안 읽음** | 지금 값이 `/sessions/rcw-…/mnt/…`(리눅스 컨테이너 경로)인데 `settings.json` 의 root 는 `E:\00_works\…` — **이미 서로 어긋나 있는데 아무도 눈치채지 못함**. 실제 root 는 settings.json 이 결정한다 |
| `project.recipe` | **안 읽음** | 레시피는 UI/CLI 인자로 결정됨 |
| `paths.wordDicDir` | `cj_reading.py:78` 에서 `P.WORDDIC` 에 대입하지만 **`P.WORDDIC` 을 읽는 코드가 어디에도 없음** | 완전한 죽은 설정. 단어사전 폴더는 실제로 안 쓰임 |
| `patterns.guidePdf` (`*각론%d*.pdf`) | **어느 코드도 안 읽음** | `read_paths.py:81` 이 같은 문자열을 **코드에 따로 박아** 쓰고 있음. JSON 을 고쳐도 아무 효과 없음 |
| `patterns.pageFilename` | 읽음 — 단, `cj_reading.py:449`(프로토 분석) 한 곳뿐 | 정작 **HTML 생성/추출 쪽 페이지 이름**(`read_import.py:279`, `read_gen.py:1193`)은 이 값을 안 봄 |
| `patterns.storyboardFilename` / `specialUnitFilename` / `contentsFolder` / `soundSheet` | 읽음 — 단, `discover()` 내부에서만 (`cj_reading.py:155-158`) | 실제 자료 읽기(`read_import.sound()` 등)는 `units[].sheet` 를 쓰므로, `soundSheet` 는 "새 단원을 처음 찾을 때"만 의미 있음 |
| `paths.guideDir` | 읽음(`cj_reading.py:80-82`) | **현재 project_rules.json 에는 이 키 자체가 없음** → `read_paths.guide_pdf()` 가 `ROOT/03_PDF` 추측 경로로 떨어짐 |

### 4-2. `rules/cj_reading/rules.json`

| JSON 위치 | 코드 사용 여부 | 문제 |
|---|---|---|
| `storyboard.sheet.Dictation` / `.구문 해설` / `.미니 단어장` / `.Lesson 3_전자저작물용 지시문 모음` | **안 읽음** | 코드가 찾는 키는 `storyboard.sheet.syntax` (`read_import.py:159`) — 이름 체계가 달라 **영원히 매칭 안 됨**. `read_gen.py:105,133` 은 `R()` 조차 안 거치고 리터럴 사용 |
| `sound.corner` (26개 코너명) | **안 읽음** | 코드는 `'read'`, `'word'`, `'question'` … 을 리터럴로 씀 (`read_import.py:394,428,488,512,549,570`) |
| `measure.safeBody` / `safePop` / `gapKr` | **안 읽음** (값도 `null`) | `read_measure.py` 에는 `load_rules()`/`R()` 이 아예 없음 (`read_measure.py:22-24` 상수) |
| `info.pageKinds`, `info.img.line/title_b/title_h` | **안 읽음** (의도된 기록용) | `rules_io.compare()` 도 `info.*` 는 제외 — 설계상 OK |
| `popup.intro.*` | 코드에 소비처 없음 (`read_gen.py` 는 `skeleton.body.*` 만 읽음) | 들머리(Read Smart) 쪽 뼈대는 rules.json 으로 못 바꿈 |
| `skeleton.intro.*` | `proto_scan.py:210` 이 쓸 수는 있으나 **현재 rules.json 에 없고, read_gen 도 안 읽음** | 동일 |
| `assets.bg` / `assets.title` | 생성(`read_gen.py:562,812`)에서는 읽음. **추출(`read_import.py:291-293 img_sizes`)에서는 안 읽음** | 같은 파일명을 두 곳이 서로 다른 출처로 씀 → drift 위험 |

### 4-3. `project.json` (레거시)

| 항목 | 상태 |
|---|---|
| `project.json` 전체 | `project_rules_io.ensure_migrated()`(최초 1회)와 `cj_reading.setup():92-93`(project_rules.json 이 비었을 때의 폴백)에서만 읽힘 |
| 내용 | `project_rules.json` 의 `units[]` 과 **완전히 중복**(9개 단원 전부 동일). 한쪽만 고치면 조용히 어긋남 |

---

## 5. 코드에는 있는데 JSON으로 이동해야 하는 값

| 파일 | 값 | 현재 위치 | 이동 필요성 | 이유 |
|---|---|---|---|---|
| `read_gen.py` | `'미니 단어장'` | `105` 리터럴 | **필수** | 프로젝트마다 시트명이 다름 |
| `read_gen.py` | `'구문 해설'` | `133` 리터럴 | **필수** | 동일 |
| `read_gen.py` | `'dictation'` | `36` 리터럴 | 높음 | 시트명 판정 기준 |
| `read_gen.py` / `read_import.py` | mp3 접두사 `3_` | `read_gen.py:226,737,762,909`, `read_import.py:824` | **필수** | 학년/교재 코드. 틀려도 오류가 안 나 더 위험 |
| `read_import.py` | 페이지 파일명 `p%s_%02d`, `p%s_01` | `279`, `585` | **필수** | `patterns.pageFilename` 이 이미 JSON 에 있는데 여기서 안 씀 |
| `read_gen.py` | `ORDER[0][:4]` 4글자 슬라이스 | `1193` | 필수 | 위와 같은 규칙의 다른 표현 |
| `read_import.py` | 지도서 PDF 좌표 6종 (`GUIDE_MID=341.0` 등) | `856-872` | **필수** | 출판사별 지면 규격 |
| `read_import.py` | 지시문 시트 = 첫 시트, 열 `r[2]`,`r[4]` | `557-566` | 필수 | 엑셀 열 구성은 프로젝트마다 다름 |
| `read_import.py` | 코너 키 `read/word/question/thinkaboutthis/mission/readsmart` | `394,428,488,512,549,570` | 높음 | rules.json `sound.corner` 와 이어야 함 |
| `read_import.py` | 이미지 파일명 `read_bg.png` 등 | `291-293` | 중간 | rules.json `assets.*` 에 이미 있음 |
| `read_paths.py` | `ROOT`, `SB_DIR`, `SB_NAME`, `SND`, `WORDDIC`, `CONTENTS` | `5,15-21` | **필수** | 프로젝트 절대경로가 모듈 상수 |
| `read_paths.py` | `'*각론%d*.pdf'`, `'03_PDF'` | `81,83-84` | 필수 | `patterns.guidePdf` 가 JSON 에 있는데 연결 안 됨 |
| `read_paths.py` | `'lesson%02d'`, `'ops'` | `56` | 필수 | 추측 폴백 — 지침 4번 위반 |
| `recipes/cj_reading.py` | `'ops'` 하위폴더명 | `179` | 높음 | 산출 폴더 구조 가정 |
| `recipes/cj_reading.py` | `'_딕테이션_생성기'` | `83` | 낮음 | 실제로 쓰이지 않는 죽은 대입 |
| `recipes/cj_reading.py` | `LEGACY_PATHS` / `LEGACY_PATTERNS` | `43-56` | 중간 | 마이그레이션 전용이어야 하는데 상시 폴백으로 쓰임(`76-79`) |
| `read_measure.py` | `SAFE_BODY=40`, `SAFE_POP=20`, `GAP_KR=26` | `22-24` | 중간 | rules.json 에 자리는 있으나 값이 `null` 이고 코드가 안 읽음 |
| `proto_scan.py` | `'%d과'` | `112`, `283` | **필수** | 이번 작업의 목표였으나 두 군데가 남아 있음 |
| `app.py` / `rules_io.py` | `'cj_reading'` 기본값 | `app.py:223,239,326,344` / `rules_io.py:153,214,245,281` | 낮음 | 레시피가 하나뿐이라 지금은 무해 |

---

## 6. read_import.py 분석

### 6-1. sheet 이름

| 대상 | 현재 값의 출처 | 새 프로젝트에서 |
|---|---|---|
| 음원 시트 | `read_import.py:129` — ① `P.unit(n)['sheet']`(**project_rules.json `units[].sheet`**) → ② `R('sound.sheet','%d과') % int(n)`(rules.json) → ③ 코드 기본값 `'%d과'` | ①이 JSON 에 있으면 정상. **없고 단원 id 가 문자열이면 `int(n)` 에서 `ValueError` 크래시** |
| 구문 해설 시트 | `read_import.py:159` — `R('storyboard.sheet.syntax','구문 해설')`. rules.json 에 `storyboard.sheet.syntax` 키가 **존재하지 않으므로 항상 코드 기본값** | 시트명이 다르면 `KeyError`. JSON 을 고쳐도 키 이름이 달라 반영 안 됨 |
| 지시문 시트 | `read_import.py:560` — `wb[wb.sheetnames[0]]` (**첫 시트 가정**) | 시트 순서가 다르면 엉뚱한 시트를 읽고 조용히 빈 값 |
| (참고) 미니 단어장 시트 | read_import 가 아니라 `read_gen.py:105` 에서 리터럴 | `KeyError` |

### 6-2. column 위치 · row 구조

| 대상 | 출처 | 새 프로젝트에서 |
|---|---|---|
| 음원 ID 열 | `read_import.py:132` `R('sound.col.id', 2)` — **rules.json 에 값 2 존재, 실제로 읽힘** | rules.json 을 고치면 반영됨 (양호) |
| 음원 글 열 | `read_import.py:133` `R('sound.col.text', 1)` — 실제로 읽힘 | 양호 |
| 구문 해설 행 구조 | `read_import.py:161-166` — 1행은 머리글, `r[0]`=쪽, `r[1]`=문장 (**리터럴**) | 열 구성이 다르면 오동작 |
| 지시문 행 구조 | `read_import.py:563-565` — `len(r)>=5`, `r[4]`=음원명, `r[2]`=우리말 (**리터럴**) | 동일 |

### 6-3. mp3 ID 규칙

* ID 패턴: `read_import.py:134` `R('sound.idPattern', IDPAT.pattern)` → rules.json 에 값 있음 → **JSON 기반 (양호)**
* 파일명 변환: `read_import.py:59-65 mp3name()` → `R('sound.mp3', {'sep':'_','case':'lower'})` → **JSON 기반 (양호)**
* **그러나** 실제 생성되는 mp3 이름은 `read_gen.py:226,737,762,909` 와 `read_import.py:824` 에서 `'3_%s_read_%s'` 처럼 **접두사 `3_` 을 코드가 직접 붙인다.** 이 `3` 은 어떤 JSON 에도 없다.
  → 새 프로젝트에서 **오류 없이 전부 잘못된 mp3 경로**가 생성된다. (read_verify 의 "없는 mp3" 검사에서야 뒤늦게 드러남)

### 6-4. 페이지 key 생성 규칙

* `read_import.py:264-279 page_key()` — 먼저 `ops/images/` 안의 실제 폴더(`p<쪽>_NN` + `read_bg.png`)를 보고 정한다(자료 기반, 좋은 설계).
* 못 찾으면 `'p%s_%02d' % (pg, 2 if pi==0 else 1)` **추측 폴백** → 페이지 이름 규칙이 `p###_##` 이 아닌 프로젝트에서는 잘못된 이름을 만든다.
* `patterns.pageFilename` 이 project_rules.json 에 있지만 **이 함수는 그것을 안 읽는다.**

### 6-5. storyboard sheet 접근

`P.storyboard(n)` (`read_paths.py:45-49`) → ① `units[].storyboard`(JSON) → ② `SB_DIR + SB_NAME % int(n)` **추측**.
JSON 에 경로가 있으면 안전하지만, 없으면 CJ 파일명 규칙(`3학년 전자저작물_…_Lesson %d.xlsx`)으로 추측하고 문자열 단원에서는 `ValueError`.

### 6-6. guide PDF 접근

`P.guide_pdf(n)` (`read_paths.py:74-87`) → ① `units[].guide`(JSON, special_lesson 만 등록됨) → ② `GUIDE_DIR + '*각론%d*.pdf'` → ③ `ROOT/03_PDF/**/*각론%d*.pdf` → ④ `ROOT/**/*각론%d*.pdf`.
②③④ 는 모두 **코드에 박힌 이름 규칙**이고 `patterns.guidePdf` 를 무시한다. 문자열 단원이면 `'%d' % 'UnitA'` 로 `TypeError`.

### 6-7. 각론 문장 추출

`read_import.py:851-1051` — `GUIDE_LABEL='본문 해석'`, `GUIDE_MID=341.0`(칼럼 분할 x좌표), `GUIDE_NEAR=40`, `GUIDE_GAP=20`, `GUIDE_MINSZ=6.0`, `GUIDE_INDENT=4.0`, `GUIDE_ROW=6.0`.
**이 7개 값은 특정 출판사 지도서의 지면 규격**이며 어떤 JSON 에도 없다. 다른 PDF 에서는 `GuideError` 로 extract 가 멈춘다(조용히 넘어가지 않는 점은 좋은 설계).

### 6-8. Dictation 처리

read_import 는 딕테이션을 만들지 않는다. `read_gen.py:25-41 has_dictation()` 이 **스토리보드 시트명에 `dictation` 이 들어있는지**로 판정하고, `read_gen.py:713-718` 이 `popup/<page>_dic1.html` iframe·버튼만 붙인다(팝업 파일 자체는 다른 작업이 만듦).
→ 시트명 규칙이 다르면 딕테이션 단추가 통째로 사라진다. rules.json 의 `storyboard.sheet.Dictation` 은 읽히지 않는다.

### 6-9. Mini Vocabulary 처리

* 낱말 목록: `read_gen.py:103-124 load_words()` → **`wb_['미니 단어장']` 리터럴**.
* 낱말 위치 표시: `read_import.py:307-378 wordpat()/place_words()` — 영어 어형 변화 규칙(`-e`, 구동사 등). 이건 **언어 규칙이라 일반 로직**으로 봐도 된다.
* 낱말 mp3: `read_gen.py:737` `'3_%s_word_%02d'` — 접두사 문제 재발.

### 6-10. rules.json 에 정의는 있으나 코드가 안 쓰는 값

`sound.corner`, `storyboard.sheet.<한글/영문 시트명 4종>`, `measure.safeBody/safePop/gapKr`, `popup.intro.*`, `info.*`.
(상세는 4-2 표)

---

## 7. UI → API → Generator 데이터 흐름

### 7-1. 프로젝트 선택

```
사용자: [자료] 에서 '프로젝트 폴더' 입력 → [저장]
  ↓ app_page.py:520-521  saveSlots()
POST /api/settings
  ↓ app.py:255-259        H.do_POST  → runner.save_settings()
settings.json   {"cj_reading": {"root": "E:\\00_works\\..."}}      ← ★ 프로젝트 root 의 실제 출처
  ↓
사용자: 레시피 선택 / 화면 새로고침
  ↓ app_page.py:237       loadRecipe()
GET /api/recipe/cj_reading
  ↓ app.py:205-206 → app.py:388  H._recipe_info()
runner.load_recipe('cj_reading')            (runner.py:136)
runner.load_settings()['cj_reading']        (runner.py:114)  → slots
runner.Ctx(m, slots)                        (runner.py:150)
recipes/cj_reading.setup(ctx)               (cj_reading.py:59)
      ├ P.ROOT = ctx['root']                             ← settings.json 값
      ├ project_rules_io.ensure_migrated()   (project_rules_io.py:149)
      │     └ project_rules.json 이 있으면 그대로 load()   ★ root 일치 검사 없음
      ├ P.SB_DIR / P.SND / P.WORDDIC / P.CONTENTS = PR.abspath(root, paths.*)
      │                                       (cj_reading.py:76-79)  ← project_rules.json
      └ _register(ctx, PR.units())           (cj_reading.py:214-227) → read_paths.UNITS
cj_reading.units(ctx)                        (cj_reading.py:194)
      ├ have = PR.units()                    ← project_rules.json (기준)
      ├ discover(ctx)                        (cj_reading.py:144) ← 폴더 스캔(보조)
      ├ PR.put_units(lst)                    ★ 스캔 결과가 JSON 에 다시 저장됨
      └ return [u['id'] …]
  ↓
app.py:410-413  {'units': [...], 'unitLabels': {...}, 'protoUnits': [...]}
  ↓ app_page.py:264-266
#unit  드롭다운 / #units 체크박스
```

**판정:** 단원 목록은 project_rules.json 이 source of truth 다 **(○)**.
다만 **프로젝트 root 는 settings.json 이 결정**하고, project_rules.json 의 `project.root` 는 읽지 않는다 **(△)**.
그리고 project_rules.json 이 생성기 폴더에 **하나뿐**이라 프로젝트를 바꿔도 옛 JSON 이 그대로 쓰인다 **(×)**.

### 7-2. prototype 선택

```
사용자: '프로토 단원' 드롭다운 열기
  ↓ 목록은 이미 loadRecipe() 가 받아 둔 R.protoUnits
    app.py:406  m.prototype_units(ctx)
      → cj_reading.py:428-435  prototype_units()
      → project_rules_io.py:126  proto_units()
      → project_rules.json  prototype.units[].id            ★ 폴더 스캔 없음
  ↓ app_page.py:255-261  <select id="sl_proto_lesson">
사용자: 단원 고름 → protoChanged() (app_page.py:431) → loadProto() (413)
GET /api/proto?recipe=&lesson=
  ↓ app.py:219-221 → app.py:438  H._proto_info()
runner.make_ctx(m, slots{proto_lesson: 고른 값})   (runner.py:325)
  ├ m.proto_ops(ctx)     (cj_reading.py:384)
  │     └ proto_lesson(ctx) (401) : PR.proto_units() 에 있는 id 만 통과
  │     └ P.unit(n)['ops']        ← project_rules.json units[].ops
  └ m.proto_pages(ctx)   (cj_reading.py:415)
        └ PR.proto_pages(n) (project_rules_io.py:136)
              → project_rules.json prototype.units[].pages   ★ 폴더 스캔 없음
  ↓ app_page.py:418-423  #ppages 체크박스
사용자: [규칙 분석]  → app_page.py:468-473
POST /api/analyze {lesson, pages, ops}
  ↓ app.py:290-308 → runner.analyze() (runner.py:342)
cj_reading.analyze(ctx, pages)   (cj_reading.py:438)
  ├ pat   = PR.pattern('pageFilename', …)              ← project_rules.json
  ├ sheet = P.unit(n)['sheet']  or  R('sound.sheet') % int(n)   ← JSON → rules.json
  └ proto_scan.scan(...)        (proto_scan.py:161)
        └ rules_io.save() → rules/cj_reading/proto_L<N>.json
사용자: [규칙으로 올리기] → POST /api/promote → rules_io.promote() (rules_io.py:97)
        → rules/cj_reading/rules.json
```

**판정:** prototype 목록·페이지 모두 project_rules.json 이 source of truth 다 **(○ — 직전 작업 결과 확인됨)**.
단, `proto_scan.py:283` 이 분석 결과에 `sound.sheet = '%d과'` 라는 **CJ 고유값을 rules.json 쪽으로 다시 써 넣는다** → 두 JSON 의 역할이 섞인다 **(△)**.

### 7-3. target unit 선택 → 생성

```
사용자: #unit 드롭다운에서 단원 선택
  ↓ app_page.py:341  loadPages()
GET /api/pages?recipe=&unit=
  ↓ app.py:224-233
u = int(unit) if unit.isdigit() else unit           ← 숫자/문자 분기 (OK)
cj_reading.pages(ctx, u)          (cj_reading.py:328)
  └ read_gen.load_lesson(unit, out_dir)   (read_gen.py:59)
        └ importlib.import_module('data%s' % n)  ← 단원자료/data<N>.py
        └ return read_gen.ORDER
  ↓ app_page.py:343-350  #pages 체크박스
   ★ 쪽 목록은 project_rules.json 이 아니라 data<N>.py 에서 온다.
     아직 extract 안 한 단원은 "[단원 준비]" 버튼이 뜬다 (app_page.py:349-350)

사용자: [생성]  → app_page.py:531-538
POST /api/run {units, steps, pages}
  ↓ app.py:260-266  start_job()  (app.py:24)
  ↓ app.py:73       _run_one()
runner.Ctx(recipe, slots, out, pages)  → recipe.setup(ctx)
  ↓ 단계별
extract : cj_reading.py:259
    read_import.load_rules(rid)              ← rules.json
    read_import.assemble(unit)   (read_import.py:380)
        ├ sound(n)            (119)  P.SND + units[].sheet          ← project_rules.json
        ├ syntax_sentences(n) (156)  P.storyboard(n) + '구문 해설'   ★ 코드 리터럴
        ├ korean_stream(n)    (174)  P.guide_pdf(n) + GUIDE_* 상수   ★ 코드 리터럴
        ├ page_key(n,pg,pi)   (264)  ops/images 스캔 → 'p%s_%02d'    ★ 폴백 리터럴
        └ img_sizes(n,page)   (290)  read_bg.png / title.png …       ★ 코드 리터럴
    → 단원자료/data<N>.py
build   : cj_reading.py:312
    read_gen.load_rules(rid)                 ← rules.json
    read_gen.build(unit, out, only)  (read_gen.py:1207)
        ├ load_lesson  → data<N>.py
        ├ load_words   (105) SB['미니 단어장']                       ★ 코드 리터럴
        ├ load_syntax  (133) SB['구문 해설']                         ★ 코드 리터럴
        ├ has_dictation(25)  'dictation' in sheetnames               ★ 코드 리터럴
        ├ head_fill    (566) R('skeleton.*','assets.*','popup.*')    ← rules.json (양호)
        └ body/js/css  (226,737,762,909)  '3_%s_read_%s' …           ★ 코드 리터럴
    → ops/*.html, css/, js/, popup/
measure : cj_reading.py:339 → read_measure.measure()  (SAFE_* 는 코드 상수)
verify  : cj_reading.py:378 → read_verify.verify()
preview : cj_reading.py:466 → layout_edit.page_files()/common_files()
```

**판정:** 단원 선택까지는 JSON 기반 **(○)**, 그 뒤 실제 자료 읽기·HTML 생성은 **코드 리터럴이 source of truth (×)**.

---

## 8. 완전히 다른 프로젝트를 넣었을 때 예상되는 실패 지점

가상 프로젝트 ProjectA (`storyboard/lesson_plan.xlsx`, `audio/recording.xlsx`, `materials/{UnitA,UnitB,Review}`, `guide/{A.pdf,B.pdf}`, 단원 = UnitA/UnitB/Review/Special, 음원 시트명 = UnitA/UnitB/Special)로 코드를 추적한 결과, **실패 가능성이 높은 순서**:

### ① project_rules.json 자체를 만들 수 없다 — `project_rules_io.py:36`
```python
PATH = os.path.join(HERE, 'project_rules.json')     # 생성기 폴더에 딱 하나
```
`ensure_migrated()`(`project_rules_io.py:158`)가 `exists()` → True 이므로 **CJ 프로젝트의 JSON 을 그대로 돌려준다.**
`setup()`(`cj_reading.py:71-83`)은 root 만 ProjectA 로 바꾸고 `paths.storyboardDir='01_스토리보드/…'` 같은 **CJ 값을 ProjectA root 에 이어 붙인다.**
→ `check()`(`cj_reading.py:113-126`)에서 `RuntimeError: 자료 경로를 찾을 수 없습니다`.
**이 시점에서 이미 멈춘다.** CJ 의 project_rules.json 을 손으로 지우거나 생성기를 통째로 복사해야 한다.

### ② 단원 id 불일치로 단원이 두 벌 생긴다 — `recipes/cj_reading.py:183`
①을 우회해 Claude 가 `units[].id = "UnitA"` 로 JSON 을 새로 썼다고 해도,
`discover()` 가 `materials/UnitA` 폴더를 보고 `_slug('UnitA')` → **`'unita'`**(소문자) 를 만든다(`cj_reading.py:140-141, 183`).
`units()`(194-211)의 `have.setdefault('unita', …)` 로 **"UnitA" 와 "unita" 가 둘 다** 목록에 들어가고, `PR.put_units()`(209)로 **JSON 에 저장까지 된다.**
→ UI 드롭다운에 유령 단원이 생기고, 그 단원을 고르면 경로가 비어 실패.

### ③ ops 하위 폴더가 없어 단원을 못 찾는다 — `recipes/cj_reading.py:179`
```python
opsdir = os.path.join(P.CONTENTS, d, 'ops')
if not os.path.isdir(opsdir): continue
```
ProjectA 의 `materials/UnitA` 아래에 `ops` 폴더가 없으면 discover 는 **아무 단원도 못 찾는다.**
(JSON 에 직접 `ops` 경로를 적어 두면 우회 가능 — `_register()` 는 JSON 값을 그대로 씀)

### ④ 구문 해설 시트가 없어 extract 가 죽는다 — `read_import.py:159-160`
```python
sheet = R('storyboard.sheet.syntax', '구문 해설')     # rules.json 에 이 키가 없음 → 항상 '구문 해설'
ws = openpyxl.load_workbook(P.storyboard(n), data_only=True)[sheet]
```
ProjectA `lesson_plan.xlsx` 에 `'구문 해설'` 시트가 없음 → **`KeyError: '구문 해설'`**.
rules.json 에 `storyboard.sheet.구문 해설` 이 있어도 **키 이름이 달라 절대 반영되지 않는다.**

### ⑤ 지도서 PDF 를 못 찾거나 TypeError — `read_paths.py:81, 83-84` / `read_import.py:186`
`units[].guide` 를 JSON 에 안 적으면 `'*각론%d*.pdf' % 'UnitA'` → **`TypeError: %d format requires a number`**.
찾아도 `read_import.py:1011 guide_stream()` 이 `GUIDE_LABEL='본문 해석'` 과 `GUIDE_MID=341.0` 좌표로 파싱하므로 ProjectA PDF 에서는 **`GuideError`**.

### ⑥ 음원 시트 이름 — `read_import.py:129`
```python
sheet = P.unit(n).get('sheet') or (R('sound.sheet','%d과') % int(n))
```
JSON `units[].sheet='UnitA'` 를 적어 두면 통과(양호).
**적지 않으면 `int('UnitA')` → `ValueError`.**

### ⑦ 미니 단어장 / 딕테이션 시트 — `read_gen.py:105, 133, 36`
build 단계에서 `wb_['미니 단어장']` → **`KeyError`**.
`load_syntax()` 도 `['구문 해설']` → **`KeyError`**.
`has_dictation()` 은 예외 대신 `False` 를 돌려주므로 **딕테이션 단추가 조용히 사라진다**(더 위험).

### ⑧ mp3 파일명이 전부 틀린다 (조용한 실패) — `read_gen.py:226,737,762,909`
`'3_%s_read_%s'` 의 `3` 은 CJ 중3 학년 코드. ProjectA 에서는 **오류 없이 존재하지 않는 mp3 경로**가 생성된다.
`read_verify.verify()`(`read_verify.py:144-157`)의 "없는 mp3" 검사에서야 드러난다.

### ⑨ 페이지 파일명 규칙 — `read_import.py:279`, `read_gen.py:1193,1197`
`ops/images/` 에 실제 폴더가 있으면 그것을 따르므로(양호) 대부분 넘어가지만,
없으면 `'p%s_%02d'` 로 만들고, `intro_page()` 는 `ORDER[0][:4]+'_01'` 로 **앞 4글자를 자른다.**
`patterns.pageFilename` 을 JSON 에 넣어도 이 세 곳은 읽지 않는다.

### ⑩ 코너 이름 — `read_import.py:394`
`pglist = [p for p in order if 'read' in snd[p]]` (`read_import.py:386`).
ProjectA 음원 ID 의 코너명이 `Read` 가 아니면 `SystemExit('Reading 쪽을 못 찾았습니다')`.

### ⑪ 프로토 분석 CLI — `proto_scan.py:341-343`
`recipe.out_dir(ctx, int(lesson))` — 문자열 단원은 `ValueError`.
(UI 경로는 `app.py:290-301` → `cj_reading.analyze()` 로 문자열을 그대로 넘기므로 정상)

### ⑫ preview / measure
`read_measure.py:22-24` 의 `SAFE_*` 는 CJ 화면 규격 상수. 다른 디자인에서는 스크롤 값이 어긋나지만 **오류는 안 난다**(품질 저하만).

---

## 9. 다음 수정 작업 우선순위

> 이번 작업에서는 **코드를 수정하지 않았다.** 아래는 제안 순서일 뿐이다.

### 1순위 — project_rules.json 을 프로젝트별로 분리
* **왜 필요한가**: 지금은 생성기 폴더에 JSON 이 하나뿐이라 **두 번째 프로젝트를 여는 순간 첫 프로젝트의 경로·단원·prototype 이 그대로 적용된다.** 다른 모든 개선의 전제 조건이다.
* **수정 파일**: `project_rules_io.py`(`PATH` 상수 → 함수화), `recipes/cj_reading.py:setup()`(root 일치 검사 추가)
* **수정 범위**: 작음(`PATH` 를 `path_for(root)` 로 바꾸고 `load/save/exists` 가 그것을 쓰게)
* **기존 기능 영향**: 기존 `project_rules.json` 을 새 위치로 한 번 옮기는 이전 처리가 필요. UI 변경 없음.

### 2순위 — rules.json 의 키 이름 체계를 코드와 일치시키기
* **왜 필요한가**: `storyboard.sheet.구문 해설`(JSON) vs `storyboard.sheet.syntax`(코드) 가 **영원히 안 맞는다.** JSON 을 아무리 고쳐도 반영되지 않는 상태 = 사용자가 가장 속기 쉬운 버그.
* **수정 파일**: `proto_scan.py:317`(무엇을 키로 쓸지), `read_import.py:159`, `read_gen.py:105,133,36`
* **수정 범위**: 중간. `storyboard.sheet.<역할>` (syntax / miniVocab / dictation / direction) 로 통일하고, 실제 시트 이름은 값으로 저장.
* **기존 기능 영향**: 기존 rules.json 의 해당 4개 키가 무의미해짐 → 재분석·재승격 필요. 생성 결과는 동일(기본값이 현재 값과 같음).

### 3순위 — mp3 접두사 `3_` 를 JSON 으로
* **왜 필요한가**: **오류 없이 잘못된 결과**를 내는 유일한 항목. 가장 발견이 늦다.
* **수정 파일**: `read_gen.py:226,737,762,909`, `read_import.py:824`
* **수정 범위**: 작음(5곳). `R('sound.mp3.prefix', '3')` 같은 키 하나 추가.
* **기존 기능 영향**: 기본값을 `'3'` 으로 두면 현재 결과 동일.

### 4순위 — `read_paths.py` 의 모듈 상수를 "미설정"으로
* **왜 필요한가**: `ROOT`/`SB_DIR`/`SB_NAME`/`SND`/`CONTENTS` 가 CJ 값으로 살아 있어, `setup()` 을 안 거친 경로에서 **틀린 값이 유효한 것처럼 동작**한다. 지침 4번(추측 금지) 위반.
* **수정 파일**: `read_paths.py:5-21,45-56,74-87`, `recipes/cj_reading.py:43-79`
* **수정 범위**: 중간. 상수를 `None` 으로 두고, `storyboard()/ops()/guide_pdf()` 가 등록부에 없으면 **오류**를 내도록.
* **기존 기능 영향**: `setup()` 을 반드시 거치는 UI/CLI 경로는 그대로. `proto_scan.py main()` 등 직접 실행 경로는 손봐야 함.

### 5순위 — 죽은 설정 정리 / 연결
* **왜 필요한가**: `patterns.guidePdf`·`paths.wordDicDir`·`project.*`·`sound.corner`·`measure.*` 는 JSON 에 있지만 아무도 안 읽는다. 사용자가 "고쳤는데 안 바뀐다"고 느끼는 원인.
* **수정 파일**: `read_paths.py:81`(guidePdf 연결), `read_measure.py:22-24`(R() 도입), `project_rules_io.py`(wordDicDir 제거 여부 판단)
* **수정 범위**: 작음~중간. **연결할 것과 삭제할 것을 먼저 구분**해야 한다.
* **기존 기능 영향**: 기본값을 유지하면 결과 동일.

### 6순위 — `discover()` 를 "검증 전용"으로 축소
* **왜 필요한가**: 지금은 `units()`(`cj_reading.py:194-211`)가 discover 결과를 **JSON 에 저장까지 한다**(209줄 `PR.put_units`). 지침 9번의 "구조를 결정하는 주된 방법이 되어선 안 된다"에 걸린다.
* **수정 파일**: `recipes/cj_reading.py:194-211`
* **수정 범위**: 작음. "JSON 에 없는 단원을 찾으면 **경고만** 하고 자동 추가하지 않는다" 로 바꾸고, 추가는 사용자 확인 후.
* **기존 기능 영향**: 새 단원이 자동으로 안 뜨게 됨 → UI 에 "새로 찾은 단원 N개 — 추가하시겠습니까" 같은 안내 필요. **기존 사용자 흐름이 바뀌므로 사전 합의 필요.**

### 7순위 — 지도서 PDF 파싱 상수 · 엑셀 열 번호
* **왜 필요한가**: 다른 출판사 자료를 받으려면 필수지만, 지금 당장 CJ 작업에는 지장 없음.
* **수정 파일**: `read_import.py:856-872`, `557-566`, `291-293`
* **수정 범위**: 큼(파서 구조 변경)
* **기존 기능 영향**: 회귀 위험이 가장 큰 구간 → `regress.py` 기준본 대조를 반드시 함께.

### 8순위 — `project.json` 폐기 여부 결정
* **왜 필요한가**: `project_rules.json` 의 `units[]` 과 내용이 완전히 중복. 한쪽만 고치면 조용히 어긋남.
* **수정 파일**: `project_io.py`, `project_rules_io.py:160-161`, `recipes/cj_reading.py:90-93`
* **수정 범위**: 작음
* **기존 기능 영향**: 마이그레이션 폴백이 사라지므로 **기존 설치본에서 project_rules.json 이 이미 만들어졌는지 확인 후** 진행.

---

## 10. 최종 목표까지 남은 문제 vs 지금 당장 수정하지 않아도 되는 문제

### A. 최종 목표("코드 수정 없이 새 프로젝트") 달성에 **반드시** 해결해야 하는 것

| # | 문제 | 위치 |
|---|---|---|
| 1 | project_rules.json 이 생성기당 1개 — 두 번째 프로젝트 불가 | `project_rules_io.py:36`, `cj_reading.py:71-83` |
| 2 | 스토리보드 시트 이름 3종이 코드 리터럴 (`미니 단어장`/`구문 해설`/`dictation`) | `read_gen.py:105,133,36` |
| 3 | rules.json 의 `storyboard.sheet.*` 키가 코드 키와 불일치 → 영구 미반영 | `read_import.py:159` vs `rules.json:181-196` |
| 4 | mp3 접두사 `3_` 리터럴 (조용한 실패) | `read_gen.py:226,737,762,909`, `read_import.py:824` |
| 5 | 지도서 PDF 지면 좌표 7종이 코드 상수 | `read_import.py:856-872` |
| 6 | 지시문 시트를 "첫 시트"로 가정 + 열 번호 리터럴 | `read_import.py:560-565` |
| 7 | 페이지 파일명 `p###_##` 가 생성 경로에서 리터럴 (`patterns.pageFilename` 미연결) | `read_import.py:279,585`, `read_gen.py:1193,1197` |
| 8 | `read_paths` 의 경로 추측 폴백 (`SB_NAME % int(n)`, `lesson%02d`, `*각론%d*.pdf`) | `read_paths.py:49,56,81,83-84` |
| 9 | 음원 코너 키 리터럴 (`'read'` 없으면 단원 전체 실패) | `read_import.py:386,394,428,488,512,549,570` |
| 10 | `int(n)` / `%d` 로 인한 문자열 단원 크래시 (5곳) | `read_import.py:129,186`, `read_paths.py:49,56,81`, `proto_scan.py:112,341` |
| 11 | `ops` 하위폴더명·`_slug()` 소문자화로 인한 단원 id 중복 | `cj_reading.py:179,183` |
| 12 | `patterns.guidePdf` 미연결 (JSON 을 고쳐도 효과 없음) | `read_paths.py:81` |

### B. 지금 당장 수정하지 않아도 되는 것

| # | 항목 | 이유 |
|---|---|---|
| 1 | `read_measure.py` 의 `SAFE_BODY/SAFE_POP/GAP_KR` | 화면 규격 값. 틀려도 오류 없이 품질만 달라짐. **recipe 고유 규칙(②)에 가까움** |
| 2 | `rules.json` 의 `popup.*`, `skeleton.body.*`, `assets.*` | **이것들은 recipe 고유 규칙(②)이 맞다.** CJ Reading 이라는 "만드는 방법" 자체이므로 rules.json 에 있는 게 옳다 |
| 3 | `read_import.py` 의 `wordpat()`, `place_words()`, `is_title_line()`, `hangul_ratio()` | **일반 프로그램 로직(③)** — 영어 어형·한글 비율 등 언어 규칙. 프로젝트가 바뀌어도 그대로 |
| 4 | `app.py`/`rules_io.py` 의 `'cj_reading'` 기본 인자 | 레시피가 하나뿐이라 지금은 무해. 두 번째 레시피가 생길 때 처리 |
| 5 | `cj_reading.py:83` `P.GEN = …'_딕테이션_생성기'` | `P.GEN` 을 읽는 코드가 없는 **죽은 대입**. 정리 대상이지 위험 요소는 아님 |
| 6 | `project.json` 중복 | 지금은 `project_rules.json` 이 우선이라 실동작에 영향 없음. 단, **혼동 방지를 위해 언젠가는 정리 필요** |
| 7 | `info.*` / `popup.intro.*` 미사용 | `info.*` 는 설계상 "본 것을 적어 둔 기록"이라 의도된 것 |
| 8 | `_기준본` 기반 `rules_io.code_rules()` 가 기본 페이지 패턴 사용 | 대조 전용 기능. 생성 결과에 영향 없음 |
| 9 | UI 의 `u+'단원'` 라벨 | 표시용 문자열. `unitLabels` 가 있으면 그쪽이 우선 (`app_page.py:252,310`) |

### C. 참고 — 하드코딩 3분류 요약

**① 반드시 제거해야 하는 프로젝트 종속 하드코딩**
`read_paths.py:5,15-21,49,56,81,83-84` / `cj_reading.py:43-56,83,179` /
`read_import.py:129,159,186,279,560-565,585,824,856-872,291-293` /
`read_gen.py:36,105,133,226,737,762,909,1193,1197` / `proto_scan.py:112,283,341`

**② recipe 고유 규칙 (CJ Reading 의 "만드는 방법" — rules.json 에 두는 것이 맞음)**
`read_gen.py` 의 HTML 템플릿(`HEAD`, `ALL_HEAD`, `THINK_ANS`), 팝업 번호 체계(`popup.*`),
페이지 뼈대 css/js 목록(`skeleton.body.*`, `CSS_DEF`/`JS_DEF`/`SPEED_DEF`),
`read_measure.py:22-24` 의 여백값, `proto_scan.py:57-88 scan_page()/scan_css()` 의 마크업 파싱 규칙

**③ 일반 프로그램 로직 (프로젝트가 바뀌어도 변하지 않음)**
`runner.py` 전체(레시피 로딩·백업·단계 실행), `app.py` 서버/잡 관리,
`project_rules_io.py`/`project_io.py`/`rules_io.py` 의 읽기·쓰기·승격·대조,
`read_paths.pgkey()`, `read_import.norm()/keytxt()/seqkey()/wordpat()/place_words()`,
`read_gen.split_mean()/bold_word()`, `layout_edit.py`, `read_verify.py` 의 검사 뼈대

---

### 부록 — 이번 조사에서 확인한 "직전 작업 보고와 실제 코드가 다른 점"

| 직전 작업에서 주장된 것 | 실제 코드 |
|---|---|
| `proto_scan.py` 의 `'%d과'` 하드코딩 제거 | **부분적으로만 맞다.** `scan()`→`scan_sound()` 의 인자 경로는 정리됐으나, `proto_scan.py:112` 에 폴백으로 `'%d과' % int(s)` 가 남아 있고, `proto_scan.py:283` 은 여전히 `'%d과'` 를 **rules.json 에 써 넣는다** |
| 문자열 단원 id 지원 | **prototype 경로만 맞다.** `proto_lesson()/proto_ops()/proto_pages()` 는 문자열 안전. 그러나 `read_import.py:129,186`, `read_paths.py:49,56,81`, `proto_scan.py:341` 은 여전히 `int()`/`%d` 를 쓴다 |
| prototype 을 project_rules.json 기준으로 관리 | **맞다.** 코드로 재확인함(2번 표 참조). 폴더 스캔으로 후보를 늘리는 경로는 없다 |
