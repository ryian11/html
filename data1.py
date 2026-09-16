# -*- coding: utf-8 -*-
# 1단원 Reading 본문 페이지 데이터
# read_import.py 가 만든 초안입니다. `# ???` 가 붙은 곳을 확인하세요.
# 출처: 녹음 대본 1과 / 스토리보드 Lesson 1 / 지도서 각론1

PAGES = {
 'p014_02': dict(
   num='014', qbtn='Q1',
   title=dict(src='3_014_read_00', en='Small Moves, Big Changes', kr='해석x',
              cls='mainTitle', mark=''),
   blocks=[
     ('subtit', dict(src='3_014_read_01', en='Ken’s Story', kr='해석x',
                      cls='subTitle sTit01', mark='')),
     ('para', [
       ('02','Ken often got up late and felt tired in the morning.',
             '해석x'),
       ('03','He always rushed to school, but he was still late most of the time.',
             '해석x'),
       ('04','When the new school year began, he decided to get up early in the morning.',
             '해석x'),
       ('05','He set his [mark:1: alarm] for 7 a.m.',
             '해석x'),
       ('06','But as soon as the alarm rang, two voices started talking in his head.',
             '해석x'),
     ]),
     ('subtit', dict(src='3_014_read_07', en='Voice One', kr='해석x',
                      cls='subTitle sTit02', mark='')),
     ('subtit', dict(src='3_014_read_08', en='Voice Two', kr='해석x',
                      cls='subTitle sTit03', mark='')),
     ('para', [
       ('09','Wake up!',
             '해석x'),
       ('10','You [mark:2: promised] to get up early!',
             '해석x'),
       ('11','You’re so tired.',
             '해석x'),
       ('12','You want to stay in bed a little longer',
             '해석x'),
       ('13','Ken didn’t move at all and fell back asleep.',
             '해석x'),
       ('14','He not only got up late but also arrived late for school.',
             '해석x'),
       ('15','He told himself, “Tomorrow will be different.”',
             '해석x'),
       ('16','But that tomorrow never came, and his plan to get up early [mark:3: failed].',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q1',
     q='What did Ken decide to do when the new school year began?', qkr='해석x',
     a='He decided to get up early in the morning.', akr='해석x',
     qsrc='3_014_question_02', asrc='3_014_question_03'),
 ),

 'p015_01': dict(
   num='015', qbtn='Q2',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('subtit', dict(src='3_015_read_01', en='Somi’s Story', kr='해석x',
                      cls='subTitle sTit04', mark='')),
     ('para', [
       ('02','Somi had a bad day because she argued with her close friend.',
             '해석x'),
       ('03','She didn’t want to do anything and just stayed alone in her room.',
             '해석x'),
       ('04','Her mom told her to go for a walk, but she didn’t listen.',
             '해석x'),
       ('05','She said to herself,',
             '해석x'),
       ('06','No way!',
             '해석x'),
       ('07','That won’t help me at all.',
             '해석x'),
       ('08','I don’t feel like doing anything.”',
             '해석x'),
       ('09','Somi stared at her phone and just looked out the window, but she didn’t feel better.',
             '해석x'),
       ('10','[mark:3: In fact], she started to feel even more [mark:4: down].',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q2',
     q='What did Somi’s mom tell Somi to do?', qkr='해석x',
     a='She told Somi to go for a walk.', akr='해석x',
     qsrc='3_015_question_02', asrc='3_015_question_03'),
 ),

 'p016_01': dict(
   num='016', qbtn='Q3',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('subtit', dict(src='3_016_read_01', en='Andy’s Story', kr='해석x',
                      cls='subTitle sTit05', mark='')),
     ('para', [
       ('02','Andy thought playing soccer during lunch would be a [mark:1: waste] of time and make him tired.',
             '해석x'),
       ('03','So, he sat down to study for his math test.',
             '해석x'),
       ('04','But after a short while, he couldn’t [mark:2: concentrate] on his studies and started to feel sleepy.',
             '해석x'),
       ('05','He tried to solve some problems, but he didn’t understand anything.',
             '해석x'),
       ('06','He asked himself,',
             '해석x'),
       ('07','I even [mark:4: skipped] soccer to study more!”',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='tf', label=['Q3'],
     # ??? 정답(ans) 은 1=True, 2=False 입니다. 원고를 보고 확인하세요.
     items=[dict(q='Andy skipped soccer because he was so tired.', qkr='해석x', ans='1', src='3_016_question_02')]),
   think=dict(q='What do you usually do when you can’t concentrate?', qkr='해석x', src='3_016_think_about_this_01',
              ex=[('3_016_think_about_this_ex_01','I take short breaks every hour.','해석x'),
                  ('3_016_think_about_this_ex_02','I listen to classical music.','해석x')]),
 ),

 'p017_01': dict(
   num='017', qbtn='Q4~Q5',
   title=dict(src='3_017_read_01', en='Why Exercise Matters', kr='해석x',
              cls='subTitle sTit06', mark='[mark:1: ]'),
   blocks=[
     ('para', [
       ('02','Exercise, even for a short time, helps you in many ways.',
             '해석x'),
       ('03','It’s good not only for your body but also for your brain.',
             '해석x'),
       ('04','Starting your day with a little movement, such as stretching, is a good way to [mark:2: improve] brain performance.',
             '해석x'),
       ('05','Exercise helps your brain [mark:3: release] [mark:4: chemicals] that make you feel good and focus better.',
             '해석x'),
       ('06','Let’s look at the above stories again.',
             '해석x'),
       ('07','Ken should wake up his brain first.',
             '해석x'),
       ('08','A few simple stretches can help him wake up and make a fresh start.',
             '해석x'),
       ('09','What Somi needed was to go for a walk.',
             '해석x'),
       ('10','It could help her feel better.',
             '해석x'),
       ('11','When she moves her body, her brain becomes more active, and her [mark:5: stress] is [mark:6: reduced].',
             '해석x'),
       ('12','Andy didn’t know that he was missing something.',
             '해석x'),
       ('13','He can do better in his studies if he adds some [mark:7: physical] activity to his day.',
             '해석x'),
       ('14','Exercise helps you a lot!',
             '해석x'),
       ('15','If you exercise in the morning, afternoon, or before you study, your body and brain will wake up.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='tf', label=['Q4', 'Q5'],
     # ??? 정답(ans) 은 1=True, 2=False 입니다. 원고를 보고 확인하세요.
     items=[dict(q='Physical activity doesn’t improve brain performance.', qkr='해석x', ans='1', src='3_017_question_02'),
            dict(q='Going for a walk could help Somi feel better.', qkr='해석x', ans='1', src='3_017_question_04')]),
   mission=dict(kr='해석x',
                en='Did thinking of solutions to the problems the three students face help make the text more interesting?',
                src='3_017_mission_01'),
 ),

}

ORDER = ['p014_02','p015_01','p016_01','p017_01']

# 배경 이미지 원본 크기 (png 에서 읽음). 비어 있으면 크기 CSS 를 넣지 않는다.
IMG = {
 'p014_02': dict(),
 'p015_01': dict(bg=(2560, 2827)),
 'p016_01': dict(bg=(2560, 2187)),
 'p017_01': dict(bg=(2560, 4349), title=(1380, 294)),
}

# ============ 레이아웃 (사람이 눈으로 맞추는 값) ============

# 제목 이미지 위 단어 버튼 (left, top).
# read_measure.py 가 찍어 주는 "WORDBTN left 후보" 를 넣으세요.
WORDBTN = {
 'p014_02': [],
 'p015_01': [],
 'p016_01': [],
 'p017_01': [(0, 0)],   # ??? 측정값을 넣으세요
}

# 배경 그림 위 글자 자리. --layout 파일에서 온다.
CSS_LAYOUT = {
 'p014_02': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p015_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p016_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p017_01': '''
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

  <title>p014_01</title>
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
            <comp-translate kr="해결책을 생각하며 읽기" en="Reading with solutions in mind" src="media/mp3/3_014_read_smart_01.mp3" narrIdx="3" clickIdx="1"></comp-translate>
          </div>
        </div>

        <div class="headerInner Sub">
          <div class="headerText">
            <comp-translate kr="문제 상황에 적절한 해결책을 떠올리며 읽으면 글을 흥미롭게 읽을 수 있습니다." en="You can enjoy reading more if you think of appropriate solutions to the problem while reading." src="media/mp3/3_014_read_smart_02.mp3" narrIdx="3" clickIdx="2"></comp-translate>
          </div>
        </div>
      </header>

      <div class="mainContent">
        <div class="missionBox">
          <span class="missionTit">
            <b class="js-narrationBtn narrText" data-narr-idx="3" data-narr-src="include/media/common/missoin.mp3">Mission!</b>
          </span>

          <div class="missionTxt">
            <comp-translate kr="세 학생이 겪는 문제를 해결할 방안을 생각하며 글을 읽어 봅시다." en="Read the text while thinking of ways to solve the problems the three students face." src="media/mp3/3_014_read_smart_03.mp3" narrIdx="3" clickIdx="3"></comp-translate>
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