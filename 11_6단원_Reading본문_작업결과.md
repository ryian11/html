# 6단원 Reading 본문 페이지 — 작업 결과와 남은 일

작업일 2026-09-15 · 대상 `lesson06/ops/`
3단원 p050_01 / p050_02 / p051_01 / p052_01 / p053_01 에 대응하는
**p104_01 / p104_02 / p105_01 / p106_01 / p107_01**

---

## 1. 한눈에 보기

| | 상태 |
|---|---|
| 본문 5쪽 (html) | **완료** — 실기 렌더링 확인 |
| css 4개 | **완료** — 배경 이미지 기준 실측, 화면 보고 조정 |
| js 4개 (미니 단어장·구문 해설) | **완료** — 팝업 동작 확인 |
| 단어 예문 음원 23개 | **완료** — 단어사전에서 복사해 넣음 |
| scrollTop | **완료** — 실기에서 재서 주입 |
| 해석 팝업 `_kor1` 4개 | **완료** — 줄 배치(`left:`)·scrollTop 주입, 실기 확인 |
| 전체 듣기 팝업 `_all` | **완료** — 동일 |
| Think About This 예시 답안 팝업 | 틀 완성 — 한글 해석 자리에 `해석x` |
| 영상 팝업 | 마크업만 — **mp4·vtt 파일 자체가 없음** |
| 리딩 퀴즈 한글 해석 | **원고 없음** → 자리에 `해석x` 넣어 둠 |

---

## 2. 넣은 파일

```
lesson06/ops/
├ p104_01.html            Read Smart 도입
├ p104_02.html            Reading 1  (제목 "Easy and Fast, but Be Careful!")
├ p105_01.html            Reading 2  (소제목 "Why Are Headlines So Dramatic?")
├ p106_01.html            Reading 3  (소제목 "Different Opinions from Different Sources")
├ p107_01.html            Reading 4  (소제목 "Real News vs. Fake News" + "How to Be a Smart Reader")
├ css/  p104_02 · p105_01 · p106_01 · p107_01 .css
├ js/   p104_02 · p105_01 · p106_01 · p107_01 .js
├ popup/ p104_02_all.html · pNNN_NN_kor1.html ×4 · p107_01_think_ans1.html
└ media/mp3/ *_ex.mp3 23개 (02_사운드\단어사전\lesson06 에서 복사)
```

생성기는 `_딕테이션_생성기\` 에 넣었습니다.
`gen6.py`(본체) · `data6.py`(원고) · `scrolls6.py`(본문 scrollTop) ·
`krlayout6.py`(해석 줄 배치) · `popscroll6.py`(팝업 scrollTop)

---

## 3. 이번에 확정한 규칙 (3단원 분석 + 6단원 적용)

### ★ 미니 단어장 번호 = 제목·소제목 이미지를 포함한 첫 등장 순서

3단원 p050_02 가 제목 이미지에 `[mark:1: ]`(내용 빈 mark)을 달고 css 로 버튼 위치를 잡은
방식이 6단원에도 그대로 맞습니다. 이 규칙으로 보면 원고 단어 순서와 정확히 일치합니다.

| 쪽 | 제목/소제목 이미지 위 | 본문 안 |
|---|---|---|
| p104_02 | (없음) | access1 · convenience2 · absorb3 |
| p105_01 | **Headlines**1 · **Dramatic**2 | shocking3 … unnecessary11 |
| p106_01 | **Opinions**1 | issue2 · present3 · various4 · compare5 · balanced6 |
| p107_01 | **Fake**1 | judge2 · official3 |

버튼 위치는 `css/pNNN_NN.css` 의 `button[data-word="n"]{top;left}` 로 잡았고,
실기 화면에서 해당 단어 위에 오는 것을 확인했습니다.

### 소제목도 `comp-language-target` 이다

3단원엔 소제목이 없어 전례가 없었습니다. 6단원은 지문 제목과 똑같이
**이미지 + `class` 로 배경 지정** 방식으로 처리했습니다.

```html
<comp-language-target class="subTitle sTit01" src="media/mp3/3_105_read_01.mp3"
  text="[mark:1: ][mark:2: ]"></comp-language-target>
```
```css
.readingCont .subTitle { display: block; cursor: pointer; }
.subTitle.sTit01 { width: calc(1764px/2); height: calc(144px/2); margin: 0 0 20px;
  background: url(../images/p105_01/s_title01.png) top left / 100% no-repeat; }
.subTitle.sTit01.on          { background-image: url(.../s_title01_h.png); }   /* 재생 중 */
.isPlayAgaing .subTitle.sTit01.on { background-image: url(.../s_title01_b.png); } /* 반복 재생 */
```
`.subTitle` 클래스 이름은 제가 정한 것입니다. 다른 이름을 쓰시려면 css·html 양쪽만 바꾸면 됩니다.

### 소제목이 2개인 쪽(p107_01)은 `.ParagraphBox` 를 2개로

`reading.css` 의 `.ParagraphBox{position:absolute}` 때문에 상자가 2개면 겹칩니다.
p107_01.css 에서 `position: relative` 로 풀어 흐름대로 쌓이게 했습니다.

### 단어 mp3 번호

6단원은 **사운드 대본 `3-1NN-Word-0k` 순서 = 미니 단어장 원고 순서**로 완전히 일치했습니다.
(3단원은 p051 의 `treat` 가 대본에 빠져 어긋났었는데, 6단원은 그런 경우가 없습니다.)

### scrollBox 높이 633px · 위아래 여유 40px

딕테이션 팝업(548px)과 다릅니다. Reading 본문 페이지는 **633px** 기준으로 묶음을 나눴습니다.
상단에 고정된 `본문 전체 듣기`·`배경 가리기` 버튼(y 50~95)에 첫 문장이 가리지 않도록
**여유를 3단원(20px)보다 20px 더 준 40px** 으로 잡았습니다.

| 쪽 | 쪽 높이 | 최대 스크롤 | 묶음 |
|---|---|---|---|
| p104_02 | 1508 | 875 | `제목+01` / `02~04`=478 / `05~06`=838 |
| p105_01 | 1586 | 953 | `소제목+02~04` / `05~08`=632 / `09~10`=953 |
| p106_01 | 1636 | 1003 | `소제목` / `02~05`=564 / `06~08`=1003 |
| p107_01 | 1732 | 1099 | `소제목+02~06` / `07+소제목2`=504 / `09~17`=1002 |

### p107_01 소제목2·팁 박스는 배경 태블릿 화면 안에 절대 배치

`How to Be a Smart Reader` 는 흐름대로 두면 태블릿 **위쪽 바깥**에 놓입니다.
교과서 지면처럼 태블릿 화면 안 가운데로 올렸습니다.

```css
.subTitle.sTit04 { position: absolute; left: 172px; top: 868px; margin: 0; }   /* 지면 x212 y938 */
.mainContent .ParagraphBox.Tip { margin-top: 362px; height: 600px; }
/* 팁 제목 문장은 한 줄을 독차지한다 (교과서 지면과 동일) */
.mainContent .ParagraphBox.Tip .Paragraph .readText:first-of-type { display: block; }
```
팁 3개는 배경의 원형 아이콘(NEWS / 안경 / FAKE!) **중심에 세로를 맞췄습니다**
(아이콘 중심 y 1109 / 1316 / 1523, 간격 207px).
각 팁의 **첫 문장(제목)은 `display:block` 으로 줄을 따로** 쓰고, 뒤 문장들은 이어 흐릅니다.
`.readText` 는 기본이 `display:inline` 이라 그냥 두면 제목과 본문이 한 줄에 붙습니다.

---

## 4. 없는 것 / 남은 일 (중요한 순서대로)

### ① 리딩 퀴즈 한글 해석 — **원고에 없음 → `해석x` 로 표시**

한글이 들어갈 자리에 전부 `해석x` 를 넣어 두었습니다. 화면의 한글 버튼을 누르면
`해석x` 가 뜨므로 어디를 채워야 하는지 바로 보입니다. 아래 9개 문장의 한글만 받으면
`data6.py` 의 `qkr` / `akr` 값만 바꿔 다시 돌리면 됩니다.

| | 영문 | 넣을 자리 |
|---|---|---|
| Q1 질문 | What should we do when we read articles online? | p104_02.html |
| Q1 정답 | We should take our time and think carefully. | p104_02.html |
| Q2 질문 | What should we do before we trust a headline? | p105_01.html |
| Q2 정답 | We should read the full article. | p105_01.html |
| Q3 | The same topic can be shown differently by different news sources. | p106_01.html |
| Q4 | News A agrees with the idea of building more parks. | p106_01.html |
| Q5 질문 | What does fake news make people do? | p107_01.html |
| Q5 정답 | It makes people believe things that aren’t true. | p107_01.html |
| Think About This | Have you ever read fake news? | p107_01.html · think_ans1 |

**Q3·Q4 정답도 확인 필요합니다.** 지도서 지면으로는 둘 다 **T** 로 보여 `data-answer="1"` 로
넣어 두었는데, 두 문제가 모두 참이라 한 번 확인해 주시는 게 좋겠습니다.

### ② 해석 팝업 `_kor1` · 전체 듣기 `_all` — **완료**

한글 해석은 **지도서 각론6 PDF(234~235쪽) 본문 해석** 그대로입니다.

**배치 규칙**: 한 문장의 해석은 **그 문장의 영어가 시작하는 x 아래**에서 시작한다.
그 줄에 다 들어가지 않을 때만 남는 부분을 다음 줄 왼쪽에 이어 붙인다.
(영어가 다음 줄로 넘어갔다고 해서 해석을 통째로 내리지 않는다)

작동 원리 (3단원 분석으로 확인):
- `.kor` 은 `position:absolute; white-space:nowrap` 이고, **그 문장의 영어가 시작한 x 아래**에 놓인다.
- `.kor span` 은 `position:absolute; display:block` 이라 **한 겹마다 100px 씩 아래 줄**로 내려가고
  `left` 로 가로 위치를 바꾼다. 겹쳐 쓰면 두 줄, 세 줄까지 내려간다.
- 그래서 넘치는 부분만 `left: -(그 문장의 시작 x)` 로 다음 줄 왼쪽 끝에 붙인다.

이 계산을 자동화해서 넣었습니다 (`krlayout6.py`).
- 팝업 본문 폭 **1177px**, 한 줄 **100px**, 조각 사이 여백 26px
- 같은 줄에 앞 문장의 이어진 부분과 다음 문장 시작이 겹치지 않도록 자리 계산
- 4쪽 42개 문장 전부 **겹침·폭 초과 0** (자동 검사) · 실기 화면 확인 완료
- `_kor1` 과 `_all` 의 영어 줄바꿈이 같아 **두 파일의 값이 동일**합니다

팝업 `scrollTop` 도 실기에서 재서 넣었습니다 (`popscroll6.py`).
`_kor1` 은 scrollBox **589px**, `_all` 은 **549px** 기준입니다.

**원고가 바뀌면**: `data6.py` 의 한글을 고친 뒤 브라우저에서 팝업을 열고
배치 계산을 다시 돌려 `krlayout6.py` 값을 갱신해야 합니다
(영어 줄바꿈이 바뀌면 `left` 값도 바뀝니다).

### ③ 영상 팝업 — mp4·vtt 없음

3단원과 같은 이름 규칙으로 마크업만 넣었습니다.
```
media/mp4/l6_read.mp4 · l6_read_script.mp4 · l6_read.vtt
```
`lesson06/ops/media` 에 `mp4` 폴더 자체가 없습니다. 파일이 들어오면 그대로 동작합니다.
(이름이 다르면 4개 html 의 `<source>`·`<track>` 만 고치면 됩니다.)

### ④ Think About This 예시 답안

`p107_01_think_ans1.html` 의 한글 자리에는 `해석x` 를 넣었습니다.
또 대본에 같은 내용이 두 벌(`3-107-Think-about-This-02/03` 남자, `…-ex-01/02` 여자) 있어
예시 답안 팝업에는 `ex_01/ex_02` 를 썼습니다. 어느 쪽이 맞는지 확인이 필요합니다.
지도서에는 예시 답안이 2개 제시돼 있는데(➊ Yes, I have. … ➋ Yes, but I usually check …)
녹음은 ➊ 하나뿐입니다.

### ⑤ 미니 단어장 위치 — 스토리보드 빨간 네모와 대조 완료

스토리보드 `미니 단어장` 시트에 묻혀 있던 **교과서 지면 이미지 2장**(빨간 네모 표시)을 꺼내
22개 단어 위치를 전부 대조했습니다.

- **수정**: p105_01 의 `dramatic` — 소제목 이미지가 아니라 **본문 첫 문장**에 있습니다.
  (`Online news often uses **dramatic** headlines …`) 소제목에서 빼고 본문으로 옮겼습니다.
- 소제목 이미지 위에 오는 단어는 **p105 Headlines · p106 Opinions · p107 Fake** 세 개뿐입니다.
- 버튼 위치는 이미지 픽셀을 재서 `(단어 시작 x) − 15 − 40` 으로 잡았습니다
  (본문 mark 버튼의 기본 간격 `left:-15px` 과 같게).
  **p107 의 `Fake` 는 사용자가 실기에서 조정한 값(`top:0; left:320`)을 그대로 두었습니다.**
- 나머지 19개(p104 3개, p105 나머지 9개, p106 5개, p107 2개)는 원래 위치가 맞았습니다.

### ⑥ p107_01 팁 박스 배치는 눈으로 한 번 봐 주세요


"How to Be a Smart Reader" 아래 3개 팁은 배경의 태블릿 화면 안, 왼쪽 원형 아이콘
(NEWS / 안경 / FAKE!) 옆에 계단식으로 배치했습니다. 글자 크기 30px, 각 팁의 첫 문장은
굵게 + 색(교과서 지면에서 뽑은 `#A45E7B` / `#4585B1` / `#2190AC`)으로 넣었습니다.
**이 세 색은 저해상도 스캔에서 추출한 근삿값**이라 디자인 원본과 대조가 필요합니다.
(재생 중 하이라이트 색은 `:not(.on)` 으로 가리지 않게 처리했습니다.)

### ⑦ 원고 오류 2건 (고치지 않고 그대로 넣음)

스토리보드 `미니 단어장` 시트의 예문에 품사 기호가 섞여 있습니다. 녹음된 예문 음원과
맞추기 위해 **원고 그대로** 두었으니 편집자 확인이 필요합니다.

| 단어 | 원고 예문 | 맞는 문장으로 보임 |
|---|---|---|
| present | `The teacher presented a picture on the scree명)` | … on the screen. |
| official | `The official announcement was made on T동)` | … made on TV. |

(`unnecessary` 의 예문 뜻 끝에 쉼표가 하나 더 붙어 있는 것도 그대로 두었습니다.)

---

## 5. 작업 환경 메모

- `device_bash` 는 여전히 죽어 있고, `contents` 폴더가 깊어 `device_stage_files` 도 거부됩니다.
  → **로컬 puppeteer 로 `file://` 를 직접 열어** 읽고·렌더링하고·스크린샷까지 찍었습니다.
  `--allow-file-access-from-files` 로 띄우면 `fetch('상대경로')` 로 소스도 그대로 읽힙니다.
  실기(Windows)에서 도는 브라우저라 **측정값이 곧 실기 값**입니다 — 딕테이션의 14px 보정이
  필요 없습니다.
- `device_commit_files` 는 깊이 제한 없이 쓸 수 있습니다. 다만 **같은 경로에 두 번째로 쓸 때
  조용히 무시되는 경우**가 있었습니다. 덮어쓸 때는 `force: true` 를 쓰고, 쓴 뒤에는
  브라우저에서 다시 읽어 확인하세요.
