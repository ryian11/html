# 알려진 문제

> 이번(2026-09-20) 조사에서는 **아무것도 고치지 않았다.** 기록만 한다.
> 원인을 확인하지 못한 것은 "원인 미확인" 이라고 적는다.

---

## #1. 미리보기가 고른 쪽과 상관없이 전체를 보여 준다

- **발생 위치** `recipes/cj_reading.py preview()` → `app.py _run_one()` → `app_page.py showFiles()`
- **재현** ④ 쪽에서 2개만 체크 → [생성] → 오른쪽 파일 목록에 고르지 않은 쪽과 그 팝업까지 나온다
- **현재 상태** 확인됨. 생성 자체는 고른 쪽만 쓴다(문제 아님)
- **원인** (확인됨)
  ```python
  def preview(ctx, unit):
      d = ctx.out_dir(unit)
      return sorted(glob.glob(os.path.join(d, 'p*.html'))) + \
             sorted(glob.glob(os.path.join(d, 'popup', '*.html')))
  ```
  `ctx.pages`(고른 쪽)를 **아예 보지 않는다.** 산출 폴더를 통째로 glob 한다.
  산출 폴더에는 예전에 만든 쪽이 남아 있으므로 전부 나온다.
  화면 쪽(`showFiles`)은 `r.pages[0]` 을 **첫 항목으로 선택**만 할 뿐 목록을 거르지 않는다.
- **팝업이 함께 나오는 것** 은 의도가 아니라 같은 glob 의 결과다. 팝업과 본 쪽을 잇는
  표나 데이터는 **코드 어디에도 없다.** 연결은 오직 파일 이름 규칙이다
  (`<쪽>_kor1.html` · `<쪽>_dic1.html` · `<쪽>_think_ans1.html`, 단원 공통은 `<첫쪽>_all.html`)
- **해결 방향** `preview()` 가 `ctx.pages` 를 받아 거르거나, `layout_edit.page_files()`
  (이미 쪽→파일 목록을 만든다)를 재사용. **이번에는 수정하지 않음**
- **추가 확인** 필요 없음

## #2. 첫 생성 전에는 ④ 쪽 목록이 비어 있다

- **발생 위치** `recipes/cj_reading.py pages()` → `read_gen.load_lesson()`
- **재현** 새 단원을 고르면 "먼저 한 번 생성해야 쪽이 보입니다"
- **현재 상태** 확인됨
- **원인** (확인됨) `pages()` 가 `단원자료/data<N>.py` 를 import 해서 `ORDER` 를 읽는다.
  추출을 한 번도 안 한 단원은 그 파일이 없다
- **해결 방향** 원고(녹음 대본)에서 쪽을 미리 읽어 보여 주기. **이번에는 수정하지 않음**

## #3. 1~5단원은 스토리보드 쪽 번호가 두 자리라 예전에 build 가 죽었다

- **발생 위치** `read_gen.load_syntax()` / `build()`
- **현재 상태** **고쳐짐**(2026-09-17, `read_paths.pgkey()`). 기록으로 남김
- **원인** 쪽 이름은 세 자리(`p014_02` → `'014'`), 스토리보드 `구문 해설` 시트는 두 자리(`14`)
- **곁가지** `read_import.syntax_sentences()` 는 `.get()` 이라 터지지 않고 조용히 비었다
  → 1~5단원에 `|n|` 구문 번호가 하나도 안 붙고 있었다. 같이 고침

## #4. 1~6단원 `data<N>.py` 가 지금 코드의 결과와 다르다

- **발생 위치** `단원자료/data1~6.py`
- **현재 상태** 확인됨. **고치지 않기로 함**(2026-09-17 결정 — 이 방식으로 만든 적 없는 단원)
- **원인** (확인됨) 각론이 물리기 전의 옛 초안. 본문 해석이 전부 `해석x`
- **근거** 실기 `lesson06` 의 해석 42개가 지금 추출 결과와 (띄어쓰기 빼고) 완전 일치.
  `data6.py` 는 0개. 즉 실기 HTML 이 `data6.py` 보다 나중 상태

## #5. ★ [기준본과 견주기] 가 잰 값 파일을 망가뜨린다

- **발생 위치** `regress.check()` → `regress.measure_ready(unit)`
- **재현** `python regress.py check cj_reading` (= UI 의 [기준본과 견주기])
- **현재 상태** **실제로 일어났다.** 2026-09-17 07:51(UTC) 에
  `단원자료/scrolls8.py` 와 `popscroll8.py` 가 덮였다.
  내용이 8단원(`p140_02`…)이 아니라 **Special Lesson 쪽 이름**(`p152_03`…)에 값은 전부 빈 채였다.
  `_backup/measure/*_20260917_165105.py` 에서 되돌렸고, 지금은 정상
- **원인** **원인 미확인.**
  `measure_ready()` 는 `RM.measure(unit, gen_dir=tmp)` 로 임시 폴더만 쓰게 돼 있고,
  `read_measure` 는 `gen_dir` 밖에 쓰지 않는다. 그런데 `단원자료` 가 덮였다.
  `krlayout8.py` 는 멀쩡해서 앞뒤가 맞지 않는다. 추측으로 고치지 않았다
- **해결 방향** 미정. 먼저 재현 조건을 좁혀야 한다
- **추가 확인 필요** **예 — 우선순위 높음.** 사용자 데이터가 실제로 깨진다.
  당분간 [기준본과 견주기] 를 누르면 `단원자료/scrolls*.py`·`popscroll*.py` 를 확인할 것

## #6. `_기준본` 이 7·8단원만 덮는다

- **발생 위치** `_기준본/cj_reading/` (7, 8 두 폴더뿐)
- **현재 상태** 확인됨
- **영향** 1~6단원과 Special Lesson 은 회귀 검사가 아무것도 못 잡는다
- **해결 방향** Special Lesson 은 기준본을 박을 만하다. 1~6단원은 계획 없음

## #7. `runner.run()` 에 단원 번호를 문자열로 넘기면 터진다

- **발생 위치** `read_paths.guide_pdf()` → `'*각론%d*.pdf' % n`
- **재현** `runner.run(recipe, '6', …)` → `TypeError: %d format: a real number is required, not str`
- **현재 상태** 확인됨. **지금은 안 터진다** — UI 경로(`layout_edit.regen`)가
  `int(unit) if str(unit).isdigit() else unit` 로 바꿔 넘기기 때문
- **원인** (확인됨) 숫자 단원을 문자열로 받는 자리가 남아 있다
- **해결 방향** `guide_pdf` 안에서 `%s` 로 바꾸거나 `pgkey` 처럼 정규화. **이번에는 수정하지 않음**

## #8. `read_paths.WORDDIC` 이 쓰이지 않는다

- **발생 위치** `read_paths.py:18`, `recipes/cj_reading.py:51`
- **현재 상태** 확인됨 — 정의만 있고 읽는 코드가 없다
- **영향** 없음(죽은 설정)
- **해결 방향** 지우거나, 단어사전을 실제로 쓰게 하거나. 판단 필요

## #9. `sound.corner` 와 `EDIT` 의 쓰임을 못 찾았다

- **현재 상태** **원인 미확인** — `rules.json` 의 `sound.corner` 를 읽는 코드,
  레시피의 `EDIT = [('layout{n}.json','layout')]` 를 화면이 쓰는 곳을 찾지 못했다
- **추가 확인 필요** 예 (낮은 우선순위)

## #10. UI 에 개발용 기능이 섞여 있다

- **발생 위치** `app_page.py` — ② 프로토 3단추, 회귀 검사 2단추, 설정 탭
- **현재 상태** 확인됨. 분류는 `PROJECT.md` 9장
- **영향** 사용자가 무엇을 눌러야 하는지 헷갈린다
- **해결 방향** `PROJECT.md` 11장의 "없애거나 합쳐야 할 것". **이번에는 수정하지 않음**

## #11. 생성 규칙이 아직 대부분 코드에 있다

- **현재 상태** `rules.json` 19항목만 생성에 쓰인다 (`RULES.md` 1장)
- **영향** 다른 교재의 프로토를 넣어도 CJ 모양 HTML 이 나온다
- **해결 방향** 항목을 하나씩 옮기고 8단원으로 바이트 확인. **이번에는 수정하지 않음**

## #12. `⌇`(줄 이음매)가 산출물에 섞이던 문제

- **현재 상태** **고쳐짐**(2026-09-17, `read_import.clear_joins()`). 기록으로 남김
- **원인** `read_import.main()` 은 지우는데 레시피 `extract()` 경로에는 그 단계가 없었다

## #13. CLI 의 "미리보기 N개" 가 늘 3 으로 나온다

- **발생 위치** `runner.py:472-473` — `print('  미리보기 %d개' % len(r['preview']))`
- **재현** `python runner.py` 로 명령줄에서 한 단원을 돌린다
- **현재 상태** 확인됨. **고치지 않기로 함**(2026-09-21, 4단계 범위 밖)
- **원인** (확인됨) 3단계에서 `recipes/cj_reading.py preview()` 가 파일 목록 대신
  `{picked, common, other}` 묶음을 돌려주게 바뀌었다. `len()` 이 묶음 수(3)를 센다
- **영향** 명령줄 출력 글자만 틀린다. **화면(app.py)·생성 결과에는 영향 없음** —
  `app.py _run_one()` 은 dict 와 list 를 둘 다 받도록 돼 있다
- **해결 방향** `len(r['preview'])` 를 묶음이면 값들의 합으로 세도록. `runner.py` 한 줄
- **추가 확인** 필요 없음


---

## #14. 프로젝트별 구조가 코드에 남아 있어 새 프로젝트 일반화가 어렵다

- **현재 상태 (2026-09-23 갱신)** `project_rules.json` 스키마는 확정됐다(schema 1, `SCHEMA.md`). 아래 12개 항목 중 **1·3·12번은 이번에 코드로 연결했고, 3번은 read_gen.py 쪽도 같이 잡았다.** 나머지(2 중 Dictation 검사는 원래 일반적이라 문제 아님, 4·5·6·7·8 일부·9·11)는 남아 있다. 원 조사(줄번호 근거 포함)는 `claude/archive/prototype-이후-전수분석.md` 3·8·9·10장에 그대로 있다.
- **핵심 문제** 단순히 `rules.json` 항목을 늘리는 문제가 아니다. **프로젝트의 경로·단원·페이지·자료 연결 관계 자체가 데이터로 관리되어야 한다.**
- **최종 해결 방향** Claude가 프로젝트를 최초 1회 분석하여 `project_rules.json`에 프로젝트 지도와 규칙을 기록하고, 일반 생성기는 이 JSON을 읽어 동작하도록 구조를 변경한다. `rules/<recipe>/rules.json`은 recipe의 생성 규칙 저장소로 별도 유지한다(`SCHEMA.md` 1-7절).
- **중요** `discover()`는 필요할 경우 파일 존재 여부 검증 등에 사용할 수 있지만, 프로젝트 구조를 결정하는 주된 방법이 되어서는 안 된다. 지금은 `units()`(`cj_reading.py:194-211`)가 discover 결과를 JSON에 저장까지 한다 — 이 부분도 "검증 전용"으로 축소해야 한다(원 조사 9장 6순위).

### 반드시 해결해야 하는 것 (최종 목표 — 코드 수정 없이 새 프로젝트 — 달성 조건)

| # | 문제 | 위치(대표) |
|---|---|---|
| 1 | ~~`project_rules.json`이 생성기 설치당 1개뿐~~ **해결(2026-09-23)** — `project_rules_io.set_root()` 로 프로젝트 root 마다 `<root>/project_rules.json` 을 따로 읽고 쓴다. `recipes/cj_reading.py:setup()` 이 요청마다 다시 부른다(안 섞임). CJ 프로젝트 실제 파일도 `_딕테이션_생성기/project_rules.json` → `<root>/project_rules.json` 로 옮겼다 | `project_rules_io.py:set_root/_path`, `cj_reading.py:setup()` |
| 2 | 스토리보드 시트 이름 3종(`미니 단어장`/`구문 해설`/`dictation`)이 코드 리터럴 | `read_gen.py:36,105,133` |
| 3 | ~~`rules.json`의 `storyboard.sheet.*` 키 이름 불일치~~ **해결(2026-09-23)** — `rules.json` 키는 그대로 두되(하위 호환), `patterns.storyboardSheets.{syntax,miniVocab,dictation}` 를 새로 만들어 `read_paths.STORYBOARD_SHEETS` 로 꽂고 `read_import.py:syntax_sentences()` 와 `read_gen.py:load_words()/load_syntax()` 가 이 값을 먼저 보게 했다(JSON에 없으면 지금까지 쓰던 CJ 기본값) | `read_paths.py:STORYBOARD_SHEETS`, `read_import.py:syntax_sentences`, `read_gen.py:load_words/load_syntax` |
| 4 | mp3 접두사 `3_`이 리터럴 — **오류 없이 잘못된 파일명으로 생성됨(조용한 실패)**. 이번에 재확인했고 실제로 존재함을 확인(줄번호도 맞음). 아직 `patterns.mp3Prefix` 연결은 안 했다 — schema 에는 있는데 코드가 안 읽는 상태 그대로다 | `read_gen.py:226,737,762,909`, `read_import.py:824` |
| 5 | 지도서 PDF 지면 좌표 7종(`GUIDE_MID=341.0` 등)이 코드 상수 | `read_import.py:856-872` |
| 6 | 지시문 시트를 "첫 시트"로 가정 + 열 번호(`r[2]`,`r[4]`) 리터럴 | `read_import.py:557-566` |
| 7 | 페이지 파일명 `p###_##`가 생성 경로에서 리터럴 — `patterns.pageFilename`을 JSON에 넣어도 이 경로는 안 읽음 | `read_import.py:279,585`, `read_gen.py:1193,1197` |
| 8 | `read_paths.py`의 경로 추측 폴백 — **부분 해결(2026-09-23)**: 등록 안 된 단원이 숫자가 아니면(`int(n)` 실패) 조용히 크래시하는 대신 무엇을 등록해야 하는지 알려 주게 고쳤다(`storyboard/ops/guide_pdf` 3곳). **폴백 자체(숫자 단원의 경로를 패턴으로 추측하는 동작)는 의도된 최후 수단이라 그대로 남겨 뒀다** — 이미 등록된 9개 단원에는 영향이 없다 | `read_paths.py:_need_numeric,storyboard,ops,guide_pdf` |
| 9 | 음원 코너 키가 리터럴(`'read'`/`'word'`/…) — 코너 이름 체계가 다르면 단원 전체가 `SystemExit`로 실패 | `read_import.py:386,394,428,488,512,549,570` |
| 10 | `int(n)`/`%d`로 인한 문자열 단원 크래시 (5곳 — proto_lesson 등 일부는 2026-09-22에 이미 고침, 나머지는 남음) | `read_import.py:129,186`, `read_paths.py:49,56,81`, `proto_scan.py:112,341` |
| 11 | `ops` 하위폴더명 고정 + `_slug()` 소문자화로 단원 id 중복 등록 위험 | `cj_reading.py:179,183` |
| 12 | ~~`patterns.guidePdf`가 코드에 연결 안 됨~~ **해결(2026-09-23)** — `read_paths.guide_pdf()` 가 `project_rules_io.pattern('guidePdf', 기본값)` 을 실제로 읽는다 | `read_paths.py:guide_pdf` |

### 지금 당장 수정하지 않아도 되는 것 (recipe 고유 규칙 또는 일반 로직이라 문제 아님)

`read_measure.py`의 여백 상수, `rules.json`의 `popup.*`/`skeleton.body.*`/`assets.*`(recipe 고유 규칙), `read_import.py`의 언어 처리 로직(`wordpat()` 등), `app.py`/`rules_io.py`의 `'cj_reading'` 기본 인자(레시피가 하나뿐이라 무해), `cj_reading.py:83`의 죽은 대입 `P.GEN`, `info.*`/`popup.intro.*` 미사용(설계상 의도됨). 근거는 `claude/archive/prototype-이후-전수분석.md` 10장 B·C.

- **추가 확인 필요** 없음 — 위 12개 항목이 "6. project_rules.json 스키마 코드 반영" 단계의 실제 작업 목록이다.
