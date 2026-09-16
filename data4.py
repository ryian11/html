# -*- coding: utf-8 -*-
# 4단원 Reading 본문 페이지 데이터
# read_import.py 가 만든 초안입니다. `# ???` 가 붙은 곳을 확인하세요.
# 출처: 녹음 대본 4과 / 스토리보드 Lesson 4 / 지도서 각론4

PAGES = {
 'p068_02': dict(
   num='068', qbtn='Q1',
   title=dict(src='3_068_read_00', en='How We Measure Everything', kr='해석x',
              cls='mainTitle', mark='[mark:1: ]'),
   blocks=[
     ('para', [
       ('01','Hello, I’m Dr. Mathimus.',
             '해석x'),
       ('02','Did you know that a [mark:2: huge] rocket blew up in 1999?',
             '해석x'),
       ('03','Why did it happen?',
             '해석x'),
       ('04','Actually, it happened because of a [mark:4: confusion] between different measurement [mark:5: units].',
             '해석x'),
       ('05','When the scientists made the rocket, some scientists used “meter,” but the others used “feet.”',
             '해석x'),
       ('06','This accident shows why using the same measurement unit is important.',
             '해석x'),
       ('07','We use measurement units to measure things.',
             '해석x'),
       ('08','What about in the past?',
             '해석x'),
       ('09','In ancient times, there were no [mark:6: tools] like [mark:7: scales] or [mark:8: rulers], but measurement units [mark:9: existed].',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='tf', label=['Q1'],
     # ??? 정답(ans) 은 1=True, 2=False 입니다. 원고를 보고 확인하세요.
     items=[dict(q='The rocket blew up because the scientists used different measurement units.', qkr='해석x', ans='1', src='3_068_question_02')]),
 ),

 'p069_01': dict(
   num='069', qbtn='Q2',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','Many ancient people used parts of their bodies as units of measurement.',
             '해석x'),
       ('02','For example, in China, people used the [mark:1: length] of a hand, and they called it a “chi.”',
             '해석x'),
       ('03','In Egypt, a “cubit,” the length of a lower arm and a hand, was used.',
             '해석x'),
       ('04','In Greece, people used the length of a foot as a unit, and it was called a “foot.”',
             '해석x'),
       ('05','But there was a problem.',
             '해석x'),
       ('06','The [mark:2: actual] length of the same unit was different [mark:3: from place to place].',
             '해석x'),
       ('07','For example, in one town in Greece, a “foot” was about 27 centimeters, but in another town, a “foot” was about 35 centimeters.',
             '해석x'),
       ('08','Let’s say a man bought a foot of [mark:4: cloth] outside his town.',
             '해석x'),
       ('09','When he got home, he found out that it was much shorter than a foot in his town.',
             '해석x'),
       ('10','He felt very upset.',
             '해석x'),
       ('11','People had [mark:5: struggled] with differences in the same measurement unit until the [mark:6: metric system] was created.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q2',
     q='What was the problem with using body parts as units of measurement?', qkr='해석x',
     a='The actual length of the same unit was different from place to place.', akr='해석x',
     qsrc='3_069_question_02', asrc='3_069_question_03'),
 ),

 'p070_01': dict(
   num='070', qbtn='Q3',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','As people began to [mark:1: trade] a lot with other countries, they needed a more [mark:2: universal] measurement system.',
             '해석x'),
       ('02','Finally, in the late 1700s, French scientists [mark:3: developed] the metric system in order to use the same [mark:4: standards].',
             '해석x'),
       ('03','It took about 7 years for them to make a meter ruler and introduce the meter as the [mark:5: basic] unit of length.',
             '해석x'),
       ('04','The ruler was made of a special metal that doesn’t change much when the temperature changes.',
             '해석x'),
       ('05','The scientists also created a measurement unit for [mark:6: weight], the gram, with the metric system.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q3',
     q='When was the metric system developed?', qkr='해석x',
     a='It was developed in the late 1700s.', akr='해석x',
     qsrc='3_070_question_02', asrc='3_070_question_03'),
   think=dict(q='When do you use measurement units in your everyday life?', qkr='해석x', src='3_070_think_about_this_01',
              ex=[('3_070_think_about_this_ex_01','I use measurement units when I cook.','해석x'),
                  ('3_070_think_about_this_ex_02','I measure sugar, flour, or milk to make food.','해석x')]),
 ),

 'p071_01': dict(
   num='071', qbtn='Q4',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','Today, the metric system is widely used all over the world.',
             '해석x'),
       ('02','One meter is the same everywhere, so all people can measure things in the same way.',
             '해석x'),
       ('03','Especially, people working in science or [mark:1: engineering] need the metric system because it gives standard units for measurements.',
             '해석x'),
       ('04','Standard measurement units keep us from getting [mark:2: confused] when we measure things.',
             '해석x'),
       ('05','The next time you use tools like a ruler or a scale, remember how wonderful it is to measure things with clear standards!',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='tf', label=['Q4'],
     # ??? 정답(ans) 은 1=True, 2=False 입니다. 원고를 보고 확인하세요.
     items=[dict(q='The metric system gives standard units for measurements.', qkr='해석x', ans='1', src='3_071_question_02')]),
   mission=dict(kr='해석x',
                en='Was scanning to find the units of length and weight helpful to understand the whole text?',
                src='3_071_mission_01'),
 ),

}

ORDER = ['p068_02','p069_01','p070_01','p071_01']

# 배경 이미지 원본 크기 (png 에서 읽음). 비어 있으면 크기 CSS 를 넣지 않는다.
IMG = {
 'p068_02': dict(bg=(2560, 2910), title=(1106, 546)),
 'p069_01': dict(bg=(2560, 6100)),
 'p070_01': dict(bg=(2560, 2908)),
 'p071_01': dict(bg=(2560, 2815)),
}

# ============ 레이아웃 (사람이 눈으로 맞추는 값) ============

# 제목 이미지 위 단어 버튼 (left, top).
# read_measure.py 가 찍어 주는 "WORDBTN left 후보" 를 넣으세요.
WORDBTN = {
 'p068_02': [(0, 0)],   # ??? 측정값을 넣으세요
 'p069_01': [],
 'p070_01': [],
 'p071_01': [],
}

# 배경 그림 위 글자 자리. --layout 파일에서 온다.
CSS_LAYOUT = {
 'p068_02': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p069_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p070_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p071_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
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

  <title>p068_01</title>
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
            <comp-translate kr="필요한 정보 찾아 읽기" en="Finding the necessary information while reading" src="media/mp3/3_068_read_smart_01.mp3" narrIdx="3" clickIdx="1"></comp-translate>
          </div>
        </div>

        <div class="headerInner Sub">
          <div class="headerText">
            <comp-translate kr="글을 빠르게 훑어 읽으며 필요한 정보를 찾을 수 있습니다." en="You can scan the text to find necessary information." src="media/mp3/3_068_read_smart_02.mp3" narrIdx="3" clickIdx="2"></comp-translate>
          </div>
        </div>
      </header>

      <div class="mainContent">
        <div class="missionBox">
          <span class="missionTit">
            <b class="js-narrationBtn narrText" data-narr-idx="3" data-narr-src="include/media/common/missoin.mp3">Mission!</b>
          </span>

          <div class="missionTxt">
            <comp-translate kr="글을 빠르게 훑어 읽으며 길이와 무게를 나타내는 단위를 찾아 동그라미 해 봅시다." en="Scan the text and circle the units of length and weight." src="media/mp3/3_068_read_smart_04.mp3" narrIdx="3" clickIdx="3"></comp-translate>
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