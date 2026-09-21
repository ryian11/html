# HTML 생성 규칙

> 근거: `rules/cj_reading/rules.json` (3단원 프로토에서 승격, 2026-09-17) + 실제 코드.
> 프로젝트 전반은 `PROJECT.md`. 여기에는 **규칙 자체**만 적는다.

규칙을 네 갈래로 나눈다.

| 갈래 | 뜻 | 바꾸는 법 |
|---|---|---|
| **P** 프로토에서 뽑는다 | `proto_scan` 이 프로토 HTML/CSS/엑셀에서 읽어 `rules.json` 에 적고, `read_gen` 이 그걸 쓴다 | 프로토 다시 분석 → 승격 |
| **C** 코드에 고정 | `read_gen`·`read_import` 안에 박혀 있다 | 코드 수정 |
| **D** 데이터가 정한다 | `data<N>.py` · `layout<N>.json` · 잰 값이 정한다 | 원고/설정 패널 |
| **?** 불명확 | 근거를 아직 못 찾았다 | 조사 필요 |

---

## 0. 최종 규칙 관리 원칙

현재 `P/C/D/?` 분류는 **현재 코드 상태를 설명하기 위한 분류**다. 최종 설계에서는 프로젝트마다 달라지는 정보를 코드에 고정하지 않고, Claude가 최초 분석하여 JSON으로 만든다.

### Claude 최초 분석에서 JSON으로 추출해야 하는 것

- 프로젝트 구조/경로: project root, storyboard, sound/script Excel, guide/PDF, image/audio, contents/output, 단원별 실제 경로
- 자료 구조: 실제 Excel sheet 이름, 필요한 열과 의미, 파일명/ID 패턴, 단원 ↔ 자료 연결 관계, 페이지 ↔ storyboard/Excel/audio/image 연결 관계
- Prototype 구조: prototype 단원, 페이지 파일 경로, 순서, 타입, 페이지별 HTML/CSS/JS, popup, 이미지/오디오 연결
- 생성 규칙: HTML 뼈대, CSS/JS 연결, popup/버튼, 파일명, 페이지별 예외, 특수 단원 규칙

### 중요한 구분

`project_rules.json`은 **프로젝트를 찾아가는 지도 + 그 프로젝트에서 발견한 규칙**이다.

`rules.json`은 현재 레시피의 생성 규칙 저장소로 이미 존재하므로, 당장 삭제하거나 이름을 바꾸지 않는다. 최종 구조를 확정하기 전까지는 기존 호환성을 유지하면서 역할을 정리한다.

### 금지

- 현재 CJ의 폴더명을 다른 프로젝트의 공통 규칙으로 승격하지 않는다.
- `Lesson %d`, `lesson%02d`, `p\\d{3}_\\d{2}` 등을 일반 규칙으로 가정하지 않는다.
- JSON에 없는 프로젝트 정보를 코드가 조용히 추측하지 않는다.
- 단순히 하드코딩을 `rules.json`으로 옮기는 것만으로 "일반화 완료"라고 판단하지 않는다.

---

## 1. P — 프로토에서 뽑아 실제 생성에 쓰는 규칙 (19항목)

읽는 곳은 `read_gen.load_rules()` 하나, 쓰는 곳은 `read_gen.R(key, default)`.
**규칙이 없으면 괄호 안 기본값**을 쓴다 → `rules.json` 을 지워도 결과가 같다.

| 규칙 이름 | 값(현재) | 생성 코드 | 프로토에서 본 곳 |
|---|---|---|---|
| `skeleton.body.css` | index.css · common.css · reading.css · `css/{page}.css` | `read_gen.head_fill()` → `{bodyCss}` | `<link rel="stylesheet" href="…">` |
| `skeleton.body.js` | contentsUI 3개 + include 5개 + `js/{page}.js` | `head_fill()` → `{bodyJs}` | `<script src="…">` |
| `skeleton.body.speedBtn` | `0.8,1.0,1.2,1.5` | `{speedBtn}` (HEAD 2곳) | `data-speed-btn` |
| `assets.bg` | `images/{page}/read_bg.png` | `make_css()` 본문 배경 | `css/<쪽>.css` 의 `url(../images/…)` |
| `assets.title` | `images/{page}/title.png` | `imgdir()` → 제목/소제목 배경 · `_h` · `_b` | 같은 곳 |
| `assets.video` | `media/mp4/l{lesson}_read.mp4` | `{video}` | `<source src>` |
| `assets.videoScript` | `media/mp4/l{lesson}_read_script.mp4` | `{videoScript}` | `<source src>` |
| `assets.vtt` | `media/mp4/l{lesson}_read.vtt` | `{vtt}` (2곳) | `<track kind="captions">` |
| `popup.video` | 1 | `{pVideo}` (팝업 + 손잡이) | `data-pop-idx + data-use="video"` |
| `popup.btn.videoPopBtn` | 1 | `{pVideoBtn}` | `js-openPopBtn videoPopBtn` |
| `popup.btn.listenTotalBtn` | 2 | `{pListenBtn}` · `{pListen}` | 같은 방식 |
| `popup.btn.korBtn` | 3 | `{pKorBtn}` · `{pKor}` | 같은 방식 |
| `popup.btn.dictationBtn` | 4 | `make_page()` dicpop·dicbtn | 같은 방식 |
| `popup.quiz.other` | 7 | `popidx` (마지막 쪽이 아닌 쪽) | `readingQuiz` 팝업 번호 |
| `popup.quiz.last` | 9 | `popidx` (마지막 쪽) | 같은 곳 |
| `popup.thinkabout` | 8 | thinkabout 팝업 · 손잡이 | `data-use="thinkabout"` |
| `popup.btn.thinkAboutBtn` | 8 | 아래 단추 | `js-openPopBtn thinkAboutBtn` |
| `popup.btn.exAnswerBtn` | 11 | 예시답안 팝업 · `data-pop-inner` | `js-openPopBtn exAnswerBtn` |
| `popup.missionclear` / `popup.btn.missionClearBtn` | 10 | missionclear 팝업 · 아래 단추 | `data-use="missionclear"` |

> **검증됨**: 이 19항목을 옮긴 뒤 7·8단원이 기준본과 바이트 동일, Special Lesson 도 실기와 동일.
> 규칙 값을 일부러 바꾸면(`speedBtn=0.5,2.0`, `korBtn=33`) 생성 HTML 이 따라 바뀌는 것도 확인.

## 2. rules.json 에 있으나 **아직 생성에 쓰이지 않는** 항목 (16항목)

`read_import` 는 `rules.json` 을 읽지 않는다. 아래는 적혀만 있고 코드가 진짜 기준이다.

| 규칙 | 값 | 실제로 정하는 코드 |
|---|---|---|
| `sound.sheet` | `%d과` | `read_import.sound()` — `P.unit(n)['sheet']` 우선, 없으면 `'%d과'` |
| `sound.col.id` / `sound.col.text` | 2 / 1 | `read_import.sound()` 열 번호 고정 |
| `sound.idPattern` | `^\d+-(\d{3})-(.+?)-(\d+(?:-\d+)*)$` | `read_import.IDPAT` |
| `sound.mp3` | `{sep:'_', case:'lower'}` | `read_import.mp3name()` |
| `sound.corner` | 코너 이름 목록 | 쓰지 않음 (적어 둔 것) |
| `storyboard.sheet.*` | Dictation · 구문 해설 · 미니 단어장 · Lesson 3_… | `read_import`/`read_gen` 이 시트 이름을 직접 연다 |
| `measure.gapKr` · `measure.safeBody` · `measure.safePop` | (null) | `read_measure.py` 의 `GAP_KR`·`SAFE_BODY`·`SAFE_POP` — **프로토로는 알 수 없음** |

## 3. `info.*` — 규칙이 아니라 "프로토에서 본 사실"

`rules_io.compare()` 가 대조에서 제외한다. 쪽 이름이 들어 있어 단원마다 다르기 때문.
`info.pageKinds` · `info.btn.questionBtn` · `info.img.title_b` · `info.img.title_h` · `info.img.icon_mic` · `info.img.line`

---

## 4. C — 코드에 고정된 규칙

### 4-1. HTML 뼈대 (read_gen.py)

- `HEAD` : 본문 쪽 전체 골격. `{page}`·`{lesson}`·`{allpop}`·`{dicpop}`·`{dicbtn}`·`{quizpop}`·`{extrapop}`·`{bothdl}`·`{botbtn}`·`{body}` + 위 P 규칙 자리.
- `ALL_HEAD` : 전체 듣기 팝업(`<첫쪽>_all.html`).
- 해석 팝업 `<쪽>_kor1.html`, 딕테이션 팝업 `<쪽>_dic1.html`, 예시답안 `<쪽>_think_ans1.html`.
- 본문 마크업 `comp-language-target` / `comp-script-box` / `script-cont` / `comp-syntax` / `comp-mini-word`.
- 퀴즈 3종 `quiz_input` · `quiz_input2` · `quiz_tf`.

### 4-2. 이름 규칙 (read_gen.py)

| 무엇 | 규칙 |
|---|---|
| 전체 듣기 팝업 | `ORDER[0] + '_all'` |
| 들머리(Read Smart) 쪽 | `ORDER[0][:4] + '_01'` — `READSMART` 가 비면 만들지 않음 |
| Think About 쪽 | `PAGES[p]['think']` 가 있는 첫 쪽 |
| 해석/딕테이션 팝업 | `<쪽>_kor1.html` · `<쪽>_dic1.html` |
| 예시답안 팝업 | `<쪽>_think_ans1.html` |
| mp3 | `3_<쪽번호>_read_<번호>.mp3` (녹음 대본 ID 에서) |

> **팝업과 본 쪽의 연결 정보는 어디에도 표로 없다. 파일 이름 규칙이 전부다.**

### 4-3. 자료 읽기 규칙 (read_import.py)

- 녹음 대본 시트 = `P.unit(n)['sheet']` 또는 `'%d과'`; ID 패턴 `IDPAT`; 열 1=글, 2=파일명.
- 스토리보드 시트: 첫 시트(지시문) · `Dictation` · `미니 단어장` · `구문 해설`.
- 쪽 이름: `ops/images/` 에서 `read_bg.png` 가 든 `p<쪽>_<nn>` 폴더 → `page_key()`.
  못 찾으면 첫 쪽 `_02`, 나머지 `_01`.
- 한글 해석: `korean_stream()`(옛길) 또는 `guide_stream()`(각론 좌표 기반, `project.json` 에 `"kr":"guide"` 인 단원만).
- 쪽 번호 대조는 반드시 `P.pgkey()` 로 앞자리 0 을 떼고 본다.

### 4-4. 각론 해석 추출 규칙 (read_import.py, `GUIDE_*`)

| 상수 | 값 | 뜻 |
|---|---|---|
| `GUIDE_LABEL` | `본문 해석` | 토막을 찾는 딱지 |
| `GUIDE_MID` | 341.0 | 왼/오 칼럼 가르는 x |
| `GUIDE_NEAR` | 40 | 딱지에서 첫 줄까지 |
| `GUIDE_GAP` | 20 | 줄 간격이 이보다 벌어지면 끝 |
| `GUIDE_MINSZ` | 6.0 | 이보다 작은 글자는 장식(드러냄표) |
| `GUIDE_INDENT` | 4.0 | 들여쓰기 = 새 문단 |
| `GUIDE_ROW` | 6.0 | 같은 줄로 묶는 y 폭 |

문장 나누기는 한글 문장부호만으로는 안 되고, **영어 문장 길이 비례에 맞춰 DP 로 자른다**(`_guide_align`).
`해석x` 판별 = 스토리보드가 `subtit` 로 준 것 + 같은 쪽 다른 문장과 80% 이상 겹치는 것.
Special Lesson 52문장 중 52개 일치로 검증됨.

### 4-5. 측정 규칙 (read_measure.py — 이번 조사에서 수정 금지 대상)

`SAFE_BODY` · `SAFE_POP` · `GAP_KR` 상수. 본문 scrollBox 기준 위아래 여유 40px.

---

## 5. D — 데이터가 정하는 값

| 값 | 어디서 |
|---|---|
| 쪽 차례·본문 문장·제목·퀴즈·think·mission | `data<N>.py` (원고에서 추출) |
| 배경/제목 이미지 원본 크기 | `data<N>.py IMG` (png 헤더에서 잼) |
| 제목 이미지 위 단어 단추 자리 | `data<N>.py WORDBTN` — **사람이 채움(`# ???`)** |
| 문단 위치·너비·여백 | `data<N>.py CSS_LAYOUT` — **사람이 채움(`# ???`)** |
| 문단 나눔·라벨·말하는 이·지면 글자·해석 | `단원자료/layout<N>.json` (7·8·SL 만 있음) |
| 스크롤 묶음 값 · 해석 줄 배치 | `scrolls<N>.py` · `krlayout<N>.py` · `popscroll<N>.py` (측정 결과) |

## 6. ? — 불명확

- `sound.corner` 목록을 무엇이 쓰는지 — 코드에서 읽는 곳을 못 찾았다.
- `read_paths.WORDDIC` (`02_사운드/단어사전/lesson%02d`) — **정의만 있고 읽는 코드가 없다.**
- `EDIT = [('layout{n}.json', 'layout')]` 이 UI 어디에 쓰이는지 — `_recipe_info` 가 내려보내지만 화면이 쓰는 곳을 못 찾았다.
