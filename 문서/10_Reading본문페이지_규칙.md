# Reading 본문 페이지(pNNN_NN.html) 규칙 — 3단원 원본 분석

분석 대상: `lesson03/ops/` 의 p050_01 / p050_02 / p051_01 / p052_01 / p053_01 과
그 css·js·popup, `include/js/components.js`, `include/js/pageManager.js`.

> **주의**: `p050_01` 은 Reading **본문 페이지가 아니다.** Read Smart(읽기 전략) 도입 페이지다.
> 실제 지문 본문은 **p050_02 / p051_01 / p052_01 / p053_01** 4쪽이다.

---

## 0. 한 지문 = 몇 개의 파일인가

| 파일 | 개수 | 비고 |
|---|---|---|
| `ops/pNNN_NN.html` | 본문 쪽마다 1개 | p050_02, p051_01, p052_01, p053_01 |
| `ops/css/pNNN_NN.css` | 쪽마다 1개 | 배경 이미지 높이·문단 배치 |
| `ops/js/pNNN_NN.js` | 쪽마다 1개 | `wordData`(미니 단어장) + `syntaxData`(구문 해설) |
| `ops/images/pNNN_NN/read_bg.png` | 쪽마다 1개 | **첫 쪽만** `title.png` `title_h.png` `title_b.png` `line.png` 추가 |
| `ops/popup/pNNN_NN_kor1.html` | 쪽마다 1개 | 해석 |
| `ops/popup/pNNN_NN_dic1.html` | 쪽마다 1개 | 딕테이션 — **이미 만든 것** |
| `ops/popup/p050_02_all.html` | **지문 전체에 1개** | 4쪽 모두 이 파일을 iframe 으로 참조 |

Read Smart 도입 페이지(`p050_01`)는 css/js/images 가 **없다**.
`include/css/read_smart.css` 만 쓰고 `<style>.Header{height:136px}` 인라인 한 줄이 전부.

---

## 1. 본문 페이지 HTML 뼈대 (4쪽 모두 동일, 본문만 다름)

```html
<link rel="stylesheet" href="include/contentsUI/css/index.css">
<link rel="stylesheet" href="include/css/common.css">
<link rel="stylesheet" href="include/css/reading.css">
<link rel="stylesheet" href="css/pNNN_NN.css">
<title>pNNN_NN</title>
```

```
#wrap.js-scale[data-snd-ctl=true]
└ #container[data-use="read"]
  └ .js-scrollContainer.scrollContainer.mainContent[data-style="custom"][data-scroll-idx="0"]
    └ .js-scrollBox.scrollBox.readingBox[data-scroll-idx="0"]
      └ .js-player.Player.js-selectChangePlayer.readingCont
           [data-ply-type="language"][data-ply-idx="1"]
           [data-ply-controls="play, pause, stop, progress"]
           [data-ply-opts="speed, again"][data-speed-btn="0.8,1.0,1.2,1.5"][data-ply-mode="basic"]
        ├ .readingBtnBox.Top      영상(pop1) / 전체듣기(pop2) / bgCover
        ├ .js-languageContainer.languageContainer.js-readHide[data-ply-idx="1"]   ← 본문
        ├ .js-languageContainer.languageContainer.js-readShow[data-ply-idx="1"]   ← 빈 div (그대로)
        └ .readingBtnBox.Bot.direcR   questionBtn(pop7), <span>Q1</span> / <span>Q2~Q3</span>
```

### 팝업 인덱스는 고정이다

| data-pop-idx | 내용 | 만드는 법 |
|---|---|---|
| 1 | 영상 | 페이지 안에 직접 (`l3_read.mp4` / `l3_read_script.mp4` / `l3_read.vtt`) |
| 2 | 본문 전체 듣기 | `<iframe src="popup/p050_02_all.html">` — **모든 쪽이 첫 쪽 것을 가리킨다** |
| 3 | 해석 | `<iframe src="popup/pNNN_NN_kor1.html">` |
| 4 | 딕테이션 | `<iframe src="popup/pNNN_NN_dic1.html">` |
| 5 | 구문 해설 | `<comp-syntax></comp-syntax>` 한 줄 (components.js 가 생성) |
| 6 | 미니 단어장 | `<comp-mini-word></comp-mini-word>` 한 줄 |
| 7 | readingQuiz | 페이지 안에 직접 |
| 10 | (전체듣기 팝업 안) readAloud | `_all` 파일 내부 |

`data-ply-idx`: **1 = 본문 language 플레이어, 2 = 영상**. 하단 `botEleBox` 는 세 덩어리
(main / popup1 / popup7) 로 4쪽 모두 똑같다. main 에는
`repeatReadBtn · korBtn(3) · dictationBtn(4) · readHideBtn` 순.

---

## 2. ★ 본문 마크업 — `comp-language-target`

**mp3 1개 = 문장 1개 = `comp-language-target` 1개.** 예외 없다.

```html
<comp-language-target [class] [scrollTop] src="media/mp3/3_050_read_01.mp3"
  text="|1|Everyone in the [mark:2: whole] world has an [mark:3: invisible] bucket. ">
</comp-language-target>
```

`components.js` 의 치환 규칙(순수 정규식):

| 원본 | 변환 결과 | 뜻 |
|---|---|---|
| `\|n\|` | `<button class="js-openPopBtn sentenceBtn" data-syntax="n" data-pop-idx="5">` | 구문 해설 버튼. **문장 맨 앞**에 둔다 |
| `[mark:n: 단어]` | `<mark><button class="js-openPopBtn" data-word="n" data-pop-idx="6"></button>단어</mark>` | 미니 단어장 |
| `<mark>…</mark>` 직접 | 그대로 | 버튼 없는 강조 (아래 참고) |
| `<br>` | 그대로 | 강제 줄바꿈 (p052_01 에서 사용) |

최종 DOM:
```html
<span class="js-languageTarget readText {class}" data-scroll-top="{scrollTop}"
      data-scroll-move="false" data-mp3="{src}"> {text} </span>
```

### 세부 규칙

- **번호는 쪽마다 1부터 리셋**한다. `[mark:n]` 과 `|n|` 은 서로 독립된 번호열이고,
  각각 그 쪽 `js/pNNN_NN.js` 의 `wordData.index` / `syntaxData.index` 와 1:1 이다.
- **`.Paragraph`** = 시각적 문단. 한 쪽에 1~2개.
- **`class="indent"`** = 문단 첫 문장 들여쓰기. (p051_01 의 두 문단 첫 문장)
  단, p050_02 는 `indent` 를 안 쓰고 css `padding-left:400px` 로 처리했다.
- **`<div class="emptyBox"></div>`** = 배경 그림을 피해 본문을 흘리기 위한 빈 블록.
  `comp-language-target` 사이에 끼워 넣는다.
- **어구가 둘로 갈라질 때**: p051_01 의 `take ... out of` 는
  `[mark:7: taking] good feelings <mark>out of</mark> a bucket` —
  앞쪽만 버튼 달린 mark, 뒤쪽은 버튼 없는 `<mark>`.
- **지문 제목**은 첫 쪽에만, `class="mainTitle"` + `text="[mark:1: ]"` (내용이 공백인 mark).
  제목은 이미지라서 글자가 없고, 단어 버튼만 css 로 이미지 위에 절대 배치한다
  (`button[data-word="1"]{top:70px;left:50px}`).
- **출처 표기**는 마지막 쪽 `ParagraphBox` 안 `.minText` 블록.
  `comp-language-target` 이 아니라 `js-narrationBtn narrText` 다 (3_053_read_09/10).

---

## 3. `scrollTop` — 손으로 맞춘 화면 묶음 값

- 문장마다가 아니라 **화면 묶음마다 같은 값**. (딕테이션과 동일한 개념)
- **첫 묶음은 속성을 아예 안 쓴다**(=0).
- `pageManager.moveScroll` 이 `[0, contentSize−visibleSize]` 로 클램프한다
  → `scrollTop="2000"` 은 사실상 **"끝까지 내려라"** 라는 뜻이다.
- 3단원 실제 값: p050_02 `-,-,-,100 / 2000×6`, p051_01 `-×5,300,300 / 1100×3,2000,2000`,
  p052_01 `300×8,700×3`, p053_01 `-×6,446 / 2000`.
  → **렌더링 실측값이 아니라 눈으로 맞춘 어림수**다(446 만 예외).
  딕테이션 팝업처럼 `build3.py` 로 정밀 측정할 필요는 없지만,
  같은 방식으로 재서 넣으면 더 정확해진다.
- 탭이 없으므로 값은 문장당 **하나뿐**이다.

---

## 4. `css/pNNN_NN.css` — 배경 이미지가 레이아웃을 지배한다

```css
@charset "utf-8";
.readingCont {
  width: 100%;
  height: calc(2614px/2);          /* ← read_bg.png 원본 높이 ÷ 2 */
  padding-top: 70px;
  background: url(../images/pNNN_NN/read_bg.png) top center / 100% no-repeat;
}
.mainContent .ParagraphBox { margin-top: 50px; }         /* 쪽마다 다름 */
.mainContent .ParagraphBox .Paragraph:nth-of-type(1) { padding-left: 400px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 40px; }
```

- 이미지는 **2배 해상도**로 만들고 css 에서 `calc(원본/2)` 로 줄인다.
- 쪽 높이(2614 / 497k / 2526 / 2357 …)와 `ParagraphBox margin-top`,
  `Paragraph` 별 `width · margin-left · padding-left` 는 **그림에 맞춰 손으로 잡은 수치**다.
  → 신규 단원은 **배경 이미지가 나와야 이 값을 정할 수 있다.**
- 첫 쪽 추가분:
```css
.mainTitle { width: calc(1186px/2); height: calc(344px/2); margin: 0 auto 50px;
             background: url(../images/p050_02/title.png) top center/100% no-repeat; }
.mainTitle.on { background-image: url(.../title_h.png); }        /* 재생 중 */
.isPlayAgaing .mainTitle.on { background-image: url(.../title_b.png); }  /* 반복 재생 */
.mainTitle::before { content:""; position:absolute; top:153px; left:362px;
  width:calc(554px/2); height:calc(60px/2); background:url(.../line.png) center/100% no-repeat; }
button[data-word="1"] { top:70px; left:50px; }
.popup[data-use="readingQuiz"] .readingAnswer .inputBox { width:100%; }
```
- 마지막 쪽: `.minText{font-size:30px;margin-top:50px;margin-left:450px;font-family:var(--gothic_B);line-height:1.5}`
  와 `.readingCont.HIDE .minText{visibility:hidden}` (본문 숨김 모드 대응).

---

## 5. `js/pNNN_NN.js` — 원고에서 기계적으로 만들 수 있다

```js
var wordData = [{ index:1, wordArr:"bucket", wordMp3Arr:"media/mp3/3_050_word_01.mp3",
  wordClassArr:"명", wordMeanArr:"양동이",
  wordExEgArr:"He filled the <b>bucket</b> with cold water.",
  wordExMp3Arr:"media/mp3/bucket_ex.mp3", wordExKoArr:"그는 양동이를 차가운 물로 채웠다." }, …]

var syntaxData = [{ index:1, syntaxArr:"문장 전체",
  syntaxMp3Arr:"media/mp3/3_050_read_01.mp3",   // ← 그 문장의 본문 mp3 재사용
  syntaxCmtArr:"해설…" }, …]
```

### 원고 → js 매핑 (스토리보드 xlsx)

**`미니 단어장` 시트** (단어 / 뜻 / 예문 / 예문뜻 / 단어음성 / 예문음성)
- **빈 행이 쪽 구분자**다. 3단원: 6개(p050) · 8개(p051) · 4개(p052) · 3개(p053)
  → 각 쪽 `[mark:n]` 개수와 정확히 일치한다.
- `뜻` 의 `명) 양동이` → `wordClassArr:"명"` + `wordMeanArr:"양동이"`.
  `형) 못된 동) 의미하다` 처럼 둘이면 템플릿에 `wordClass/wordMean` 칸이 2쌍 있으니 그대로 나눠 넣는다.
- `예문` 의 해당 단어를 `<b>…</b>` 로 감싼다 (원고는 밑줄로 표시).
- **예문 mp3** = 단어를 소문자·공백→`_`, `...` 제거 + `_ex.mp3`
  (`take ... out of` → `take_out_of_ex.mp3`, `in order to` → `in_order_to_ex.mp3`)
- **단어 mp3** = 사운드 대본의 `3-0NN-Word-0k` **순번을 따른다. 원고 순번이 아니다.**
  ★ 3단원 p051: 원고엔 `treat` 가 2번째로 있는데 대본엔 없다 →
  `treat` 만 `media/mp3/treat.mp3`(단어사전), 나머지는 `3_051_word_01~07`.
  ★ 대본의 p052 단어 파일명이 `3-051-Word-01~04` 로 **오타**인데 실제 파일은 `3_052_word_0k` 다.
  → **단어 mp3 번호는 반드시 대본과 대조**할 것.

**`구문 해설` 시트** (쪽 / 교과서 문장 / 설명)
- 빈 행이 쪽 구분자. 쪽 열 값이 그대로 페이지다. 3단원: 50→3개, 51→4개, 52→4개, 53→3개
  → 각 쪽 `|n|` 개수와 일치.
- `syntaxMp3Arr` 은 그 문장과 같은 본문 mp3 를 찾아 넣는다.
- 설명 안의 `「」` 는 `<span class='cursiveB'>「</span>` 로 감싼다.

---

## 6. mp3 이름 규칙 (사운드 대본 `3과` 시트)

| 대본 파일명 | 실제 파일 | 쓰이는 곳 |
|---|---|---|
| `3-050-Read-Smart-01~03` | `3_050_read_smart_01.mp3` | p050_01 `comp-translate` |
| `3-050-Read-00` | `3_050_read_00.mp3` | 지문 제목 `.mainTitle` |
| `3-0NN-Read-01…` | `3_0NN_read_01.mp3` | 본문 문장 (순서 = 화면 순서) |
| `3-0NN-Question-01` | (쓰지 않음) | "Question 1" 안내 음성 |
| `3-0NN-Question-02` | `3_0NN_question_02.mp3` | 리딩 퀴즈 질문 |
| `3-050-Question-03` | `3_050_question_03.mp3` | 주관식 정답 읽기 |
| `3-0NN-Word-0k` | `3_0NN_word_0k.mp3` | 미니 단어장 표제어 |
| (대본에 없음) | `단어.mp3` / `단어_ex.mp3` | 단어사전 폴더 |

규칙은 딕테이션과 같다: **대시→언더바, 전부 소문자.**

---

## 7. readingQuiz (pop 7)

쪽마다 문항 수가 다르다. 3단원: p050 Q1(1개), p051 Q2~Q3(2개), p052 Q4, p053 Q5.
`.readingBtnBox.Bot` 의 `<span>` 라벨도 거기 맞춘다(`Q1`, `Q2~Q3`).

**주관식형** (p050_02)
```html
<div class="js-quizContainer quizBox arrayV" data-quiz-type="input"
     data-quiz-opts="noAlert, noSound, noSolve, noRemoveSpace, noReset">
  <div class="quizTitBox">
    <span class="marker read">Q1</span>
    <div class="listTxt readingQuestion" data-include="interpretText">
      <p class="js-narrationBtn narrText" data-narr-idx="1" data-narr-src="…question_02.mp3">질문</p>
      <span class="js-interpretTarget interpretText" data-interpret-idx="1">질문 해석</span>
    </div>
  </div>
  <div class="readingAnswer">
    <div class="js-quizInputBox inputBox writingBox Br">
      <textarea rows="3" class="js-quizItem quizInput pen" placeholder=" " data-answer=" "></textarea>
      <div class="js-quizTarget quizTarget Answer">
        <span class="js-narrationBtn narrText" data-narr-idx="2" data-narr-src="…question_03.mp3"
              data-include="interpretText">정답 문장
          <span class="js-interpretTarget interpretText" data-interpret-idx="1">정답 해석</span>
        </span>
      </div>
    </div>
  </div>
</div>
```
하단 핸들러의 korBtn 에 `data-disabled="true" data-hdl-idx="0"` 이 붙는다.

**T/F형** (p051_01)
```html
<div class="js-quizContainer quizBox arrayV" data-quiz-type="choice" data-quiz-name="trueFalse"
     data-quiz-opts="noAlert, noSound, noSolve, noRemoveSpace, toggleChoice, noReset">
  … quizTitBox 안에 <div class="js-quizItem quizItem arrayH" data-answer="1">   (1=T, 2=F)
      체크박스 id 는 quiz1_check1, quiz1_check2, quiz1_check3 … 문항을 넘어 연번
      <button class="js-quizHandlerItemBtn itemBtn answer Circle" data-item-index="0" data-handler="0">
```

---

## 8. 해석 팝업 `pNNN_NN_kor1.html`

```html
<link … index.css> <link … common.css>
<style>.scriptContainer .scriptBox:not(.titBox, .subTitBox, .list) .Script:first-of-type{margin-left:20px}</style>
<div class="js-scale iframePopup" data-use="kor"> … data-ply-idx="1", data-scroll-idx="1"
  <comp-script-box class="titBox">  ← 첫 쪽만, 지문 제목
  <comp-script-box>
    <script-cont [scrollTop] src="../media/mp3/3_050_read_01.mp3" en="영문" kr="해석"></script-cont>
```

- `comp-script-box` = 본문의 `.Paragraph` 하나에 대응.
- **★ kr 칸의 `left:` 꼼수**: 영어 문장 단위와 한국어 어순이 안 맞아서,
  한국어를 앞 문장에 몰아 쓰고 `<span style='left:-1085px'>…</span>` 로 왼쪽으로 끌어당긴다.
  밀린 문장의 `kr` 은 빈 문자열(`kr=""`)로 둔다.
  → 이 픽셀값은 **렌더링해서 재야 하는 값**이다. (handover 10장의 "kr 안의 레이아웃 수치")
- `scrollTop` 은 본문 페이지와 **다른 값**이다(팝업 높이가 달라서). `_all` 과도 다르다.
  예: 같은 문단이 본문 2000 / kor1 1000 / all 400.

## 9. 전체 듣기 팝업 `p050_02_all.html`

- 지문 4쪽을 **한 파일**에 이어 붙인다. `listen_total.css` + `listenTotal.js`, 타이머·readAloud 포함.
- `<title>` 이 `p015_01_all` 로 남아 있다(다른 단원에서 복사한 흔적). 신규 단원은 제대로 넣을 것.
- 하단 `js-scrollMoveBtn data-script-idx="시작,끝"` 이 쪽 단위 점프다.
  3단원: 전체 `0,41` / 51~53쪽 `11,41` / 52~53쪽 `23,41` / 53쪽 `34,41`
  → **전체 `script-cont` 통짜 인덱스**(제목 포함 0부터)가 필요하다.
  3단원 = 제목1 + 10 + 12 + 11 + 10(출처 2줄 포함) = 42개 → 마지막 인덱스 41.
- `class="titBox"` = 지문 제목, `class="subTitBox"` = 소제목 (3단원엔 소제목 없음).

---

## 10. 신규 단원에 없는 것 = 막히는 지점

| | 상태 | 대책 |
|---|---|---|
| ① `images/pNNN_NN/read_bg.png`, title 3종, line.png | **없음** | 디자인 산출물 필요. 이게 없으면 css 수치(쪽 높이·문단 위치)를 못 정한다 |
| ② 한글 해석 (kor1 / _all / 퀴즈 interpretText) | **두 엑셀에 없음** | 지도서 PDF 또는 편집자 확보 |
| ③ kr `left:` 픽셀값 | 실측 필요 | 딕테이션 `build3.py` 와 같은 방식으로 자동화 가능 |
| ④ 미니 단어장 · 구문 해설 원고 | **있음** (스토리보드 xlsx 시트) | js 자동 생성 가능 |
| ⑤ 리딩 퀴즈 질문·정답 | **일부 있음** (사운드 대본 Question 행) | 한글 해석과 T/F 정답은 원고 확인 필요 |
| ⑥ `scrollTop` | 손으로 맞춘 값 | 렌더링 실측으로 대체 가능 |

**결론**: 배경 이미지(①)와 한글 해석(②)만 들어오면
`js/pNNN_NN.js`(④)·`kor1`·`_all`·본문 마크업은 생성기로 자동화할 수 있다.
그림 없이 지금 바로 만들 수 있는 것은 **본문 마크업 + js 데이터 + _all 팝업(해석 제외)** 까지다.
