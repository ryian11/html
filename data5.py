# -*- coding: utf-8 -*-
# 5단원 Reading 본문 페이지 데이터
# read_import.py 가 만든 초안입니다. `# ???` 가 붙은 곳을 확인하세요.
# 출처: 녹음 대본 5과 / 스토리보드 Lesson 5 / 지도서 각론5

PAGES = {
 'p086_02': dict(
   num='086', qbtn='Q1',
   title=dict(src='3_086_read_00', en='A Journey into Korean Culture', kr='해석x',
              cls='mainTitle', mark=''),
   blocks=[
     ('para', [
       ('01','Three students, Diego from Mexico, Chloé from France, and Bao from Vietnam, recently visited a Korean cultural festival.',
             '해석x'),
       ('02','They enjoyed different [mark:1: aspects] of Korean culture, from a traditional game to a unique performance.',
             '해석x'),
       ('03','They had a great time and wrote about their experiences.',
             '해석x'),
       ('04','Here are their online posts from the festival.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q1',
     q='Who visited a Korean cultural festival?', qkr='해석x',
     a='Three students, Diego from Mexico, Chloé from France, and Bao from Vietnam, visited a Korean cultural festival.', akr='해석x',
     qsrc='3_086_question_02', asrc='3_086_question_03'),
 ),

 'p087_01': dict(
   num='087', qbtn='Q2~Q3',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','Diego',
             '해석x'),
       ('02','Today, I saw some people playing with paper [mark:1: squares].',
             '해석x'),
       ('03','After I watched them [mark:2: closely], I tried the game, too.',
             '해석x'),
       ('04','The game was called ddakjichigi, a traditional Korean game.',
             '해석x'),
       ('05','I folded two pieces of paper into a thick, square shape.',
             '해석x'),
       ('06','This is a ddakji.',
             '해석x'),
       ('07','The rule is simple.',
             '해석x'),
       ('08','You try to [mark:3: flip] the other players’ ddakji by throwing your own.',
             '해석x'),
       ('09','However, it was harder than I expected, and I couldn’t even hit a ddakji [mark:4: properly].',
             '해석x'),
       ('10','I wondered if I could flip a ddakji, but I got better with practice.',
             '해석x'),
       ('11','I was excited when I flipped someone else’s ddakji.',
             '해석x'),
       ('12','I realized that it wasn’t just a simple paper game but a fun [mark:5: challenge].',
             '해석x'),
       ('13','The game gave me an exciting experience, and it connected me with Korean culture.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='tf', label=['Q2', 'Q3'],
     # ??? 정답(ans) 은 1=True, 2=False 입니다. 원고를 보고 확인하세요.
     items=[dict(q='Diego folded four pieces of paper to make a ddakji.', qkr='해석x', ans='1', src='3_087_question_02'),
            dict(q='Diego was able to flip a ddakji without practice.', qkr='해석x', ans='1', src='3_087_question_04')]),
 ),

 'p088_01': dict(
   num='088', qbtn='Q4',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','Chloé',
             '해석x'),
       ('02','I love Hangeul, the Korean writing system, so I joined a Hangeul [mark:1: calligraphy] class today!',
             '해석x'),
       ('03','I practiced drawing lines and writing Korean letters with a [mark:2: handwriting] brush and black [mark:3: ink].',
             '해석x'),
       ('04','At first, I wasn’t sure if I was holding the brush [mark:4: correctly], but the [mark:5: instructor] kindly helped me [mark:6: step by step].',
             '해석x'),
       ('05','Focusing on the tip of the brush, I learned how to draw [mark:7: thin] and thick lines on paper.',
             '해석x'),
       ('06','I felt calm when I practiced writing.',
             '해석x'),
       ('07','Later, I wrote my name in Korean.',
             '해석x'),
       ('08','It was really special to write my name in Korean with a brush.',
             '해석x'),
       ('09','The class was a great way to enjoy the beauty of Hangeul.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q4',
     q='What class did Chloé join?', qkr='해석x',
     a='She joined a Hangeul calligraphy class.', akr='해석x',
     qsrc='3_088_question_02', asrc='3_088_question_03'),
   think=dict(q='What language are you interested in?', qkr='해석x', src='3_088_think_about_this_01',
              ex=[]),
 ),

 'p089_01': dict(
   num='089', qbtn='Q5~Q6',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','Bao',
             '해석x'),
       ('02','This afternoon, I watched jultagi, a traditional Korean [mark:1: tightrope] walking performance.',
             '해석x'),
       ('03','Holding a hand fan, a tightrope walker showed amazing skills on a rope high in the air.',
             '해석x'),
       ('04','He walked, jumped, sat, and even lay down on it.',
             '해석x'),
       ('05','The [mark:2: audience] was amazed when he performed [mark:3: thrilling] moves on the rope.',
             '해석x'),
       ('06','Below the rope, other [mark:4: teammates] [mark:5: supported] him.',
             '해석x'),
       ('07','They played music, [mark:6: responded] to the walker’s [mark:7: jokes], and [mark:8: entertained] the audience.',
             '해석x'),
       ('08','The walker’s moves made me nervous [mark:9: at times], but watching the performance was really fun.',
             '해석x'),
       ('09','Everything about the performance was really amazing.',
             '해석x'),
       ('10','Later, I found out that jultagi became a UNESCO Cultural [mark:10: Heritage] in 2011.',
             '해석x'),
       ('11','I would like to watch jultagi again with my friends someday.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input2', label=['Q5', 'Q6'],
     items=[dict(label='Q5', q='What was the tightrope walker holding?', qkr='해석x', a='He was holding a hand fan.', akr='해석x', qsrc='3_089_question_02', asrc='3_089_question_03'),
            dict(label='Q6', q='When did jultagi become a UNESCO Cultural Heritage?', qkr='해석x', a='It became a UNESCO Cultural Heritage in 2011.', akr='해석x', qsrc='3_089_question_05', asrc='3_089_question_06')]),
   mission=dict(kr='해석x',
                en='Did thinking about your own experiences with the traditional culture help you enjoy reading the text more?',
                src='3_089_mission_01'),
 ),

}

ORDER = ['p086_02','p087_01','p088_01','p089_01']

# 배경 이미지 원본 크기 (png 에서 읽음). 비어 있으면 크기 CSS 를 넣지 않는다.
IMG = {
 'p086_02': dict(bg=(2560, 3611), title=(1834, 622)),
 'p087_01': dict(bg=(2560, 4589)),
 'p088_01': dict(bg=(2560, 4589)),
 'p089_01': dict(bg=(2560, 4589)),
}

# ============ 레이아웃 (사람이 눈으로 맞추는 값) ============

# 제목 이미지 위 단어 버튼 (left, top).
# read_measure.py 가 찍어 주는 "WORDBTN left 후보" 를 넣으세요.
WORDBTN = {
 'p086_02': [],
 'p087_01': [],
 'p088_01': [],
 'p089_01': [],
}

# 배경 그림 위 글자 자리. --layout 파일에서 온다.
CSS_LAYOUT = {
 'p086_02': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p087_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p088_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p089_01': '''
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

  <title>p086_01</title>
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
            <comp-translate kr="경험을 떠올리며 읽기" en="Recalling experiences while reading" src="media/mp3/3_086_read_smart_01.mp3" narrIdx="3" clickIdx="1"></comp-translate>
          </div>
        </div>

        <div class="headerInner Sub">
          <div class="headerText">
            <comp-translate kr="글의 내용과 관련된 경험을 떠올리며 읽으면 글을 흥미롭게 읽을 수 있습니다." en="You can enjoy reading more if you think about your own experiences related to the text." src="media/mp3/3_086_read_smart_02.mp3" narrIdx="3" clickIdx="2"></comp-translate>
          </div>
        </div>
      </header>

      <div class="mainContent">
        <div class="missionBox">
          <span class="missionTit">
            <b class="js-narrationBtn narrText" data-narr-idx="3" data-narr-src="include/media/common/missoin.mp3">Mission!</b>
          </span>

          <div class="missionTxt">
            <comp-translate kr="본문에 등장하는 전통문화와 관련된 경험을 떠올리며 글을 읽어 봅시다." en="Read the text while thinking about your own experiences with the traditional culture mentioned in the text." src="media/mp3/3_086_read_smart_03.mp3" narrIdx="3" clickIdx="3"></comp-translate>
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