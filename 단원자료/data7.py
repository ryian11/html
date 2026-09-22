# -*- coding: utf-8 -*-
# 7단원 Reading 본문 페이지 데이터
# read_import.py 가 만든 초안입니다. `# ???` 가 붙은 곳을 확인하세요.
# 출처: 녹음 대본 7과 / 스토리보드 3학년 전자저작물_지시문_딕테이션_미니 단어장_구문 해설_Lesson 7.xlsx / 지도서 각론

PAGES = {
 'p122_02': dict(
   num='122', qbtn='Q1',
   paracls={0: 'mic'},
   title=dict(src='3_122_read_00', en='James Webb Space Telescope', kr='제임스 웹 우주 망원경',
              cls='mainTitle', mark=''),
   blocks=[
     ('para', [
       ('01','|1|Today, I’m here to meet Dr. Jane Roman, a space scientist, to talk about the James Webb Space Telescope',
             '오늘 저는 우주 과학자인 Jane Roman 박사를 만나 제임스 웹 우주 망원경(JWST)에 대해 이야기하기 위해 이곳에 왔습니다.'),
       ('02','(JWST).',
             '해석x'),
       ('03','|2|Dr. Roman, I heard that it was [mark:1: launched] on December 25, 2021.',
             'Roman 박사님, 저는 그것이 2021년 12월 25일에 발사되었다고 들었습니다.'),
       ('04','Can you introduce the JWST?',
             'JWST를 소개해 주실 수 있나요?'),
     ]),
   ],
   quiz=dict(kind='input', label='Q1',
     q='When was the James Webb Space Telescope launched?', qkr='해석x',
     a='It was launched on December 25, 2021.', akr='해석x',
     qsrc='3_122_question_02', asrc='3_122_question_03'),
 ),

 'p123_01': dict(
   num='123', qbtn='Q2',
   paracls={0: 'spk', 1: 'mic', 2: 'spk'},
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('02','The JWST is the most powerful telescope in history.',
             'JWST는 역사상 가장 강력한 망원경입니다.'),
       ('03','|1|It’s as wide as a tennis [mark:1: court] and as tall as a three-story building.',
             '그것은 테니스 코트만큼 넓고, 3층 건물만큼 높습니다.'),
       ('04','|2|If a person stood next to the telescope, the person would look like a tiny [mark:2: ant].',
             '만약 어떤 사람이 그 망원경 옆에 선다면, 그 사람은 아주 작은 개미처럼 보일 것입니다.'),
       ('05','To observe [mark:3: deep] into space, it has 18 [mark:4: golden] mirrors that work like one big eye.',
             '우주 깊은 곳을 관측하기 위해, 그것은 하나의 큰 눈처럼 작동하는 18개의 금빛 거울을 가지고 있습니다.'),
     ]),
     ('para', [
       ('06','How did scientist launch such a large telescope into space?',
             '과학자들은 어떻게 그렇게 큰 망원경을 우주로 발사했나요?'),
     ]),
     ('para', [
       ('07','We found the answer in paper folding.',
             '우리는 종이접기에서 답을 찾았습니다.'),
       ('08','|3|The JWST was folded twelve times so that it could [mark:5: fit into] a space rocket.',
             'JWST는 우주 로켓에 꼭 들어맞도록 열두 번 접혔습니다.'),
       ('09','Then the telescope traveled 1.5 [mark:6: million] kilometers away from Earth.',
             '그 후 망원경은 지구에서 150만 킬로미터 떨어진 곳까지 이동했습니다.'),
       ('10','|4|After the JWST was launched, it spent about a month traveling to its [mark:7: final] location.',
             'JWST가 발사된 후에, 최종 위치까지 도달하는 데 약 한 달이 걸렸습니다.'),
       ('11','During this time, it was slowly [mark:8: unfolded], [mark:9: piece by piece], like a [mark:10: blooming] flower.',
             '이 시간 동안 망원경은 피어나는 꽃처럼, 조금씩 천천히 펼쳐졌습니다.'),
     ]),
   ],
   quiz=dict(kind='tf', label=['Q2'],
     # ??? 정답(ans) 은 1=True, 2=False 입니다. 원고를 보고 확인하세요.
     items=[dict(q='The scientists folded the James Webb Space Telescope to launch it into space.', qkr='해석x', ans='1', src='3_123_question_02')]),
 ),

 'p124_01': dict(
   num='124', qbtn='Q3',
   paracls={0: 'mic', 1: 'spk'},
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','Interesting',
             '흥미롭네요.'),
       ('02','I heard that the JWST uses [mark:1: infrared] cameras.',
             '저는 JWST가 적외선 카메라를 사용한다고 들었습니다.'),
       ('03','How does it work?',
             '그것은 어떻게 작동하나요?'),
     ]),
     ('para', [
       ('04','|1|Using infrared cameras is the special point of this telescope.',
             '적외선 카메라를 사용하는 것이 이 망원경의 특별한 점입니다.'),
       ('05','We cannot see infrared light, but we can feel it as heat.',
             '우리는 적외선을 볼 수 없지만, 우리는 그것을 열로 느낄 수 있습니다.'),
       ('06','With infrared cameras, the telescope can observe the infrared light from stars and planets far from Earth.',
             '적외선 카메라로 망원경은 지구에서 멀리 떨어진 별과 행성에서 나오는 적외선을 관측할 수 있습니다.'),
       ('07','|2|It can even see through space [mark:2: dust] or [mark:3: space clouds], which [mark:4: block] visible light from deep space.',
             '그것은 심지어 우주 먼지나 성운도 뚫어 볼 수 있는데, 그것들은 깊은 우주에서 오는 가시광선을 가로막습니다.'),
       ('08','|3|After the JWST takes photos, it sends them to scientists who study the [mark:5: universe].',
             'JWST는 사진을 찍은 후에, 우주를 연구하는 과학자들에게 그것들을 보내 줍니다.'),
     ]),
   ],
   quiz=dict(kind='input', label='Q3',
     q='With the infrared cameras, what can the James Webb Space Telescope observe?', qkr='해석x',
     a='It can observe the infrared light from stars and planets far from Earth.', akr='해석x',
     qsrc='3_124_question_02', asrc='3_124_question_03'),
   think=dict(q='Have you ever watched the night sky for a long time?', qkr='해석x', src='3_124_think_about_this_01',
              ex=[('3_124_think_about_this_ex_01','Yes, I have.','해석x'),
                  ('3_124_think_about_this_ex_02','The stars looked so bright, and I felt happy and peaceful.','해석x'),
                  ('3_124_think_about_this_ex_03','Yes, I have.','해석x'),
                  ('3_124_think_about_this_ex_04','The sky was very dark, and I felt amazed because the stars were like diamonds.','해석x'),
                  ('3_124_think_about_this_ex_05','Yes, I have.','해석x'),
                  ('3_124_think_about_this_ex_06','The moon was very big, and I felt so curious about space.','해석x')]),
 ),

 'p125_01': dict(
   num='125', qbtn='Q4',
   paracls={0: 'mic', 1: 'spk', 2: 'mic', 3: 'spk', 4: 'mic'},
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','|1|Scientists use the JWST to observe and [mark:1: investigate] deep space.',
             '과학자들은 깊은 우주를 관측하고 연구하기 위해 JWST를 사용하는군요.'),
       ('02','Why is exploring deep space important?',
             '깊은 우주를 탐사하는 것이 왜 중요한가요?'),
     ]),
     ('para', [
       ('03','|2|Exploring deep space [mark:2: allows] us to study the beginning of the early universe, and find planets with life.',
             '깊은 우주를 탐사하는 것은 우리가 초기 우주의 시작을 연구하고, 생명이 있는 행성을 찾을 수 있게 해 줍니다.'),
       ('04','Observing stars in deep space is like looking back in time with a [mark:3: time machine].',
             '깊은 우주의 별들을 관측하는 것은 타임머신으로 시간을 되돌아보는 것과 같습니다.'),
       ('05','Space is so large, and light from stars takes a very long time to get to Earth.',
             '우주는 매우 크고, 별빛이 지구에 도달하는 데에는 매우 오랜 시간이 걸립니다.'),
       ('06','So, when you look at those stars, you see them as they were a long time ago — even billions of years ago!',
             '그래서 당신이 그 별들을 볼 때, 당신은 오래전, 심지어 수십억 년 전의 그 별들의 모습을 보고 있는 것입니다!'),
     ]),
     ('para', [
       ('07_1','|3|Studying deep space will help scientists solve the mysteries of the universe.',
             '깊은 우주를 연구하는 것은 과학자들이 우주의 신비를 푸는 것을 도울 것입니다.'),
       ('08','I wonder whether there is a planet like Earth in space.',
             '저는 우주에 지구와 같은 행성이 있을지 궁금합니다.'),
       ('09','|4|If I were an astronaut, I would like to visit that planet.',
             '만약 제가 우주 비행사라면, 그 행성에 가 보고 싶을 텐데요.'),
     ]),
     ('para', [
       ('10','The JWST might help us find that planet someday.',
             'JWST가 언젠가 그런 행성을 찾도록 도와줄지도 모릅니다.'),
       ('11','It’s like a bridge between the past, the present, and the future.',
             '그것은 과거, 현재, 그리고 미래 사이의 다리와 같습니다.'),
       ('12','With this telescope, we are taking one step closer to understanding the mysteries of the universe.',
             '이 망원경으로, 우리는 우주의 신비를 이해하는 데 한 걸음 더 다가가고 있습니다.'),
     ]),
     ('para', [
       ('13','Thank you, Dr. Roman.',
             '감사합니다, Roman 박사님.'),
     ]),
   ],
   quiz=dict(kind='tf', label=['Q4'],
     # ??? 정답(ans) 은 1=True, 2=False 입니다. 원고를 보고 확인하세요.
     items=[dict(q='Light from stars takes a short time to get to Earth.', qkr='해석x', ans='1', src='3_125_question_02')]),
   mission=dict(kr='해석x',
                en='Did reading the text with pictures related to the James Webb Space Telescope help you understand it?',
                src='3_125_mission_01'),
 ),

}

ORDER = ['p122_02','p123_01','p124_01','p125_01']

# 배경 이미지 원본 크기 (png 에서 읽음). 비어 있으면 크기 CSS 를 넣지 않는다.
IMG = {
 'p122_02': dict(bg=(2560, 1918), title=(1422, 396)),
 'p123_01': dict(bg=(2560, 3388)),
 'p124_01': dict(bg=(2560, 3504)),
 'p125_01': dict(bg=(2560, 4369)),
}

# ============ 레이아웃 (사람이 눈으로 맞추는 값) ============

# 제목 이미지 위 단어 버튼 (left, top).
# read_measure.py 가 찍어 주는 "WORDBTN left 후보" 를 넣으세요.
WORDBTN = {
 'p122_02': [],
 'p123_01': [],
 'p124_01': [],
 'p125_01': [],
}

# 배경 그림 위 글자 자리. --layout 파일에서 온다.
CSS_LAYOUT = {
 'p122_02': '''
.readingCont { position: relative; }
/* 문단 첫머리 — 말하는 이와 마이크 아이콘 (본문 글자가 아니라 꾸밈이라 CSS 로 붙인다) */
.mainContent .ParagraphBox .Paragraph.spk .readText:first-of-type::before {
	content: 'Dr. Roman'; color: #2E6DB4; font-family: var(--gothic_EB); margin-right: 18px; }
.mainContent .ParagraphBox .Paragraph.mic .readText:first-of-type::before {
	content: ''; display: inline-block; width: 26px; height: 26px; margin-right: 10px;
	vertical-align: -5px; background: url(../images/p122_02/icon_mic.png) center/contain no-repeat; }
.readingCont .label { position: absolute; margin: 0; font-family: var(--gothic_EB); }

.mainContent .ParagraphBox { margin-top: 250px; }
.mainContent .ParagraphBox .Paragraph { width: 880px; margin-left: 350px; }
''',
 'p123_01': '''
.readingCont { position: relative; }
/* 문단 첫머리 — 말하는 이와 마이크 아이콘 (본문 글자가 아니라 꾸밈이라 CSS 로 붙인다) */
.mainContent .ParagraphBox .Paragraph.spk .readText:first-of-type::before {
	content: 'Dr. Roman'; color: #2E6DB4; font-family: var(--gothic_EB); margin-right: 18px; }
.mainContent .ParagraphBox .Paragraph.mic .readText:first-of-type::before {
	content: ''; display: inline-block; width: 26px; height: 26px; margin-right: 10px;
	vertical-align: -5px; background: url(../images/p123_01/icon_mic.png) center/contain no-repeat; }
.readingCont .label { position: absolute; margin: 0; font-family: var(--gothic_EB); }

.mainContent .ParagraphBox { margin-top: 395px; }
.mainContent .ParagraphBox .Paragraph { width: 1000px; margin-left: 170px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(3) { margin-top: 26px; }
''',
 'p124_01': '''
.readingCont { position: relative; }
/* 문단 첫머리 — 말하는 이와 마이크 아이콘 (본문 글자가 아니라 꾸밈이라 CSS 로 붙인다) */
.mainContent .ParagraphBox .Paragraph.spk .readText:first-of-type::before {
	content: 'Dr. Roman'; color: #2E6DB4; font-family: var(--gothic_EB); margin-right: 18px; }
.mainContent .ParagraphBox .Paragraph.mic .readText:first-of-type::before {
	content: ''; display: inline-block; width: 26px; height: 26px; margin-right: 10px;
	vertical-align: -5px; background: url(../images/p124_01/icon_mic.png) center/contain no-repeat; }
.readingCont .label { position: absolute; margin: 0; font-family: var(--gothic_EB); }

.mainContent .ParagraphBox { margin-top: 430px; }
.mainContent .ParagraphBox .Paragraph { width: 1020px; margin-left: 140px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(1) { width: 600px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
''',
 'p125_01': '''
.readingCont { position: relative; }
/* 문단 첫머리 — 말하는 이와 마이크 아이콘 (본문 글자가 아니라 꾸밈이라 CSS 로 붙인다) */
.mainContent .ParagraphBox .Paragraph.spk .readText:first-of-type::before {
	content: 'Dr. Roman'; color: #2E6DB4; font-family: var(--gothic_EB); margin-right: 18px; }
.mainContent .ParagraphBox .Paragraph.mic .readText:first-of-type::before {
	content: ''; display: inline-block; width: 26px; height: 26px; margin-right: 10px;
	vertical-align: -5px; background: url(../images/p125_01/icon_mic.png) center/contain no-repeat; }
.readingCont .label { position: absolute; margin: 0; font-family: var(--gothic_EB); }

.mainContent .ParagraphBox { margin-top: 80px; }
/* 오른쪽 사진 두 장을 비켜 가도록 띄움 상자를 둔다 */
.mainContent .ParagraphBox::before { content: ''; float: right; width: 600px; height: 520px; }
.mainContent .ParagraphBox .Paragraph { width: 1080px; margin-left: 140px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(3) { margin-top: 26px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(4) { margin-top: 26px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(5) { margin-top: 26px; }
''',
}

# ---------- Read Smart 도입 페이지 ----------
READSMART = '''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=1280, height=720, initial-scale=1.0">

  <link rel="stylesheet" href="include/contentsUI/css/index.css">
  <link rel="stylesheet" href="include/css/common.css">
  <link rel="stylesheet" href="include/css/read_smart.css">

  <title>p122_01</title>
  <style>
    .Header { height: 136px; }
    </style>
</head>
<body>
<div id="wrap" class="js-scale" data-snd-ctl="true">
  <div id="container" data-use="main">
    <!-- contContainer -->
    <div class="contContainer">
      <!-- Header -->
      <header class="Header Type2 Read">
        <div class="headerInner Main">
          <span class="headerIcon">
            <span class="js-narrationBtn narrText" data-narr-idx="0" data-narr-src="include/media/common/read_smart.mp3">Read Smart</span>
          </span>
          <div class="headerText">
            <comp-translate kr="시각 자료를 활용하며 읽기" en="Reading with visual aids" src="media/mp3/3_122_read_smart_01.mp3" narrIdx="3" clickIdx="1"></comp-translate>
          </div>
        </div>

        <div class="headerInner Sub">
          <div class="headerText">
            <comp-translate kr="시각 자료를 보며 글을 읽으면 내용을 더 잘 이해할 수 있습니다." en="You can understand better if you read the text with visual aids." src="media/mp3/3_122_read_smart_02.mp3" narrIdx="3" clickIdx="2"></comp-translate>
          </div>
        </div>
      </header>

      <div class="mainContent">
        <div class="missionBox">
          <span class="missionTit">
            <b class="js-narrationBtn narrText" data-narr-idx="3" data-narr-src="include/media/common/missoin.mp3">Mission!</b>
          </span>

          <div class="missionTxt">
            <comp-translate kr="본문 속 제임스 웹 우주 망원경과 관련된 사진을 보며 글을 읽어 봅시다." en="Read the text while looking at the pictures related to the James Webb Space Telescope." src="media/mp3/3_122_read_smart_03.mp3" narrIdx="3" clickIdx="3"></comp-translate>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

  <script src="include/contentsUI/js/config.js"></script>
  <script src="include/contentsUI/js/index.js"></script>
  <script src="include/contentsUI/js/contentUI.js"></script>
  <script src="include/js/config.js"></script>
  <script src="include/js/pageManager.js"></script>
  <script src="include/js/components.js"></script>
  <script src="include/js/common.js"></script>
</body>
</html>'''