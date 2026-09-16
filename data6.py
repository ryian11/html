# -*- coding: utf-8 -*-
# 6단원 Reading 본문 페이지 데이터
# read_import.py 가 만든 초안입니다. `# ???` 가 붙은 곳을 확인하세요.
# 출처: 녹음 대본 6과 / 스토리보드 Lesson 6 / 지도서 각론6

PAGES = {
 'p104_02': dict(
   num='104', qbtn='Q1',
   title=dict(src='3_104_read_00', en='Easy and Fast, but Be Careful!', kr='해석x',
              cls='mainTitle', mark=''),
   blocks=[
     ('para', [
       ('01','People can [mark:1: access] information quickly and easily in the digital age.',
             '해석x'),
       ('02','With just one click, you can read about topics such as sports, science, or world events.',
             '해석x'),
       ('03','|1|However, this [mark:2: convenience] can cause some problems.',
             '해석x'),
       ('04','|2|It often lets readers [mark:3: absorb] information quickly without much thought.',
             '해석x'),
       ('05','|3|For this reason, it is necessary to take your time and think carefully when you read articles online.',
             '해석x'),
       ('06','But do we really do that?',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q1',
     q='What should we do when we read articles online?', qkr='해석x',
     a='We should take our time and think carefully.', akr='해석x',
     qsrc='3_104_question_02', asrc='3_104_question_03'),
 ),

 'p105_01': dict(
   num='105', qbtn='Q2',
   title=dict(src='3_105_read_01', en='Why Are Headlines So Dramatic?', kr='해석x',
              cls='subTitle sTit01', mark='[mark:1: ]'),
   blocks=[
     ('para', [
       ('02','Online news often uses [mark:2: dramatic] headlines to get more clicks because more clicks mean more money.',
             '해석x'),
       ('03','|1|Some headlines are too [mark:3: shocking] to ignore.',
             '해석x'),
       ('04','|2|This style of writing is called yellow [mark:4: journalism], which uses [mark:5: sensational] words to [mark:6: attract] readers.',
             '해석x'),
       ('05','For example, imagine there’s an article with the title “[mark:7: Celebrity] [mark:8: Quits] Acting [mark:9: Forever]!”',
             '해석x'),
       ('06','|3|The title makes people think that something shocking has happened.',
             '해석x'),
       ('07','This title can also [mark:10: confuse] people or cause [mark:11: unnecessary] worry.',
             '해석x'),
       ('08','|4|But if you read the full story, you will find out that the celebrity is just taking a short break.',
             '해석x'),
       ('09','This shows that headlines do not always tell the whole truth.',
             '해석x'),
       ('10','So, read the full article before you trust a headline.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q2',
     q='What should we do before we trust a headline?', qkr='해석x',
     a='We should read the full article.', akr='해석x',
     qsrc='3_105_question_02', asrc='3_105_question_03'),
 ),

 'p106_01': dict(
   num='106', qbtn='Q3~Q4',
   title=dict(src='3_106_read_01', en='Different Opinions from Different Sources', kr='해석x',
              cls='subTitle sTit02', mark='[mark:1: ]'),
   blocks=[
     ('para', [
       ('02','When you see an [mark:2: issue] in the news, you should be careful.',
             '해석x'),
       ('03','Different news sources can [mark:3: present] the same topic in very different ways.',
             '해석x'),
       ('04','|1|For example, there is news A, which says, “Building more parks is necessary for our town.”',
             '해석x'),
       ('05','On the other hand, news B says, “Building more parks is not good for the environment.”',
             '해석x'),
       ('06','These two reports are talking about the same issue, but they have different opinions about it.',
             '해석x'),
       ('07','|2|That’s why it is important to read [mark:4: various] news sources and [mark:5: compare] their messages.',
             '해석x'),
       ('08','|3|By looking at various sources, you can think more clearly and have a more [mark:6: balanced] view.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='tf', label=['Q3', 'Q4'],
     # ??? 정답(ans) 은 1=True, 2=False 입니다. 원고를 보고 확인하세요.
     items=[dict(q='The same topic can be shown differently by different news sources.', qkr='해석x', ans='1', src='3_106_question_02'),
            dict(q='News A agrees with the idea of building more parks.', qkr='해석x', ans='1', src='3_106_question_06')]),
 ),

 'p107_01': dict(
   num='107', qbtn='Q5',
   title=dict(src='3_107_read_01', en='Real News vs. Fake News', kr='해석x',
              cls='subTitle sTit03', mark='[mark:1: ]'),
   blocks=[
     ('para', [
       ('02','|1|Online news is fast and easy to access, but not everything you read online is true.',
             '해석x'),
       ('03','Some news looks real, but it is fake.',
             '해석x'),
       ('04','|2|Fake news makes people believe things that aren’t true.',
             '해석x'),
       ('05','|3|So, we should find out if it is real.',
             '해석x'),
       ('06','It’s also important to check the writer and the source before we trust the news.',
             '해석x'),
       ('07','|4|Don’t [mark:2: judge] quickly if there is no [mark:3: official] report or clear result.',
             '해석x'),
     ]),
     ('subtit', dict(src='3_107_read_08', en='How to Be a Smart Reader', kr='해석x',
                      cls='subTitle sTit04', mark='')),
     ('para', [
       ('09','Don’t just read the headline.',
             '해석x'),
       ('10','Try not to be tricked by the title.',
             '해석x'),
       ('11','Read the whole article.',
             '해석x'),
       ('12','Read different opinions from various sources.',
             '해석x'),
       ('13','Don’t choose only one side.',
             '해석x'),
       ('14','Try to have a balanced view.',
             '해석x'),
       ('15','Be careful with fake news.',
             '해석x'),
       ('16','Check if the news is true and if you can trust the writer and the source.',
             '해석x'),
       ('17','Don’t make a quick judgement.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q5',
     q='What does fake news make people do?', qkr='해석x',
     a='It makes people believe things that aren’t true.', akr='해석x',
     qsrc='3_107_question_02', asrc='3_107_question_03'),
   mission=dict(kr='해석x',
                en='Did predicting the content from the title and subtitles help you understand the text?',
                src='3_107_mission_01'),
   think=dict(q='Have you ever read fake news?', qkr='해석x', src='3_107_think_about_this_01',
              ex=[('3_107_think_about_this_ex_01','Yes, I have.','해석x'),
                  ('3_107_think_about_this_ex_02','I read fake news about my favorite singer on the Internet, and it was very confusing.','해석x')]),
 ),

}

ORDER = ['p104_02','p105_01','p106_01','p107_01']

# 배경 이미지 원본 크기 (png 에서 읽음). 비어 있으면 크기 CSS 를 넣지 않는다.
IMG = {
 'p104_02': dict(bg=(2560, 3016), title=(1600, 596)),
 'p105_01': dict(bg=(2560, 3172), s1=(1764, 144)),
 'p106_01': dict(bg=(2560, 3272), s2=(1856, 152)),
 'p107_01': dict(bg=(2560, 3464), s3=(1856, 152), s4=(1724, 110)),
}

# ============ 레이아웃 (사람이 눈으로 맞추는 값) ============

# 제목 이미지 위 단어 버튼 (left, top).
# read_measure.py 가 찍어 주는 "WORDBTN left 후보" 를 넣으세요.
WORDBTN = {
 'p104_02': [],
 'p105_01': [(0, 0)],   # ??? 측정값을 넣으세요
 'p106_01': [(0, 0)],   # ??? 측정값을 넣으세요
 'p107_01': [(0, 0)],   # ??? 측정값을 넣으세요
}

# 배경 그림 위 글자 자리. --layout 파일에서 온다.
CSS_LAYOUT = {
 'p104_02': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p105_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p106_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p107_01': '''
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

  <title>p104_01</title>
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
            <comp-translate kr="글의 제목을 읽고 내용을 추측하기" en="Predicting the content by reading the title" src="media/mp3/3_104_read_smart_01.mp3" narrIdx="3" clickIdx="1"></comp-translate>
          </div>
        </div>

        <div class="headerInner Sub">
          <div class="headerText">
            <comp-translate kr="글의 제목과 소제목을 읽고 내용을 추측하면 글을 더 잘 이해할 수 있습니다." en="You can understand a text better by predicting the content from its titles and subtitles." src="media/mp3/3_104_read_smart_02.mp3" narrIdx="3" clickIdx="2"></comp-translate>
          </div>
        </div>
      </header>

      <div class="mainContent">
        <div class="missionBox">
          <span class="missionTit">
            <b class="js-narrationBtn narrText" data-narr-idx="3" data-narr-src="include/media/common/missoin.mp3">Mission!</b>
          </span>

          <div class="missionTxt">
            <comp-translate kr="본문의 제목과 소제목을 읽고 내용을 추측한 후 글을 읽어 봅시다." en="Read the text after predicting the content based on the title and subtitles." src="media/mp3/3_104_read_smart_04.mp3" narrIdx="3" clickIdx="3"></comp-translate>
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