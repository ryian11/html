# -*- coding: utf-8 -*-
# 8단원 Reading 본문 페이지 데이터
# read_import.py 가 만든 초안입니다. `# ???` 가 붙은 곳을 확인하세요.
# 출처: 녹음 대본 8과 / 스토리보드 Lesson 8 / 지도서 각론8

PAGES = {
 'p140_02': dict(
   num='140', qbtn='Q1',
   title=dict(src='3_140_read_01', en='The Red Bike', kr='빨간 자전거',
              cls='mainTitle', mark=''),
   blocks=[
     ('para', [
       ('02','Leo had always dreamed of having a bike.',
             'Leo는 늘 자전거를 갖는 것을 꿈꿔 왔었다.'),
       ('03','|1|To make his dream [mark:1: come true], he spent two years saving money.',
             '그의 꿈을 이루기 위해 그는 돈을 모으며 2년을 보냈다.'),
       ('04','He did small jobs for his neighbors, like cutting the grass and picking up leaves.',
             '그는 잔디를 깎거나 낙엽을 줍는 것 같은 이웃들을 위한 작은 일들을 했다.'),
       ('05','Finally, Leo was able to buy the perfect bike.',
             '마침내 Leo는 완벽한 자전거를 살 수 있었다.'),
       ('06','It was a bright red bike with 18 [mark:2: gears].',
             '그것은 18단 기어가 달린 밝은 빨간색 자전거였다.'),
       ('07','He named it Big Red.',
             '그는 그것에 Big Red라는 이름을 붙였다.'),
       ('08','He rode Big Red everywhere.',
             '그는 어디를 가든 Big Red를 타고 다녔다.'),
       ('09','|2|The more he rode it, the more memories he made.',
             '그가 그것을 많이 타면 탈수록 그는 더 많은 추억을 만들었다.'),
       ('10','As he grew taller, Big Red became too small for him.',
             '그가 키가 커지자 Big Red는 그에게 너무 작아졌다.'),
       ('11','Though it was still in great condition, Leo knew it was time for a new bike.',
             '그것은 여전히 좋은 상태였지만, Leo는 새 자전거를 탈 때가 되었다는 것을 알았다.'),
     ]),
     ('para', [
       ('12','|3|Leo decided to donate Big Red to an [mark:3: organization] whose [mark:4: mission] was to send bikes to people in need.',
             'Leo는 도움이 필요한 사람들에게 자전거를 보내는 것이 임무인 단체에 Big Red를 기부하기로 결심했다.'),
       ('13','But first, Leo wanted to make Big Red look its best.',
             '하지만 우선 Leo는 Big Red를 최고의 상태로 보이게 만들고 싶었다.'),
       ('14','He cleaned it, oiled the [mark:5: chain], and changed the [mark:6: handlebars].',
             '그는 그것을 깨끗이 닦고, 체인에 기름을 바르고, 손잡이를 교체했다.'),
       ('15','He [mark:7: whispered], “Thank you for all the [mark:8: adventures].”',
             '그는 “모든 모험에 대해 고마워.”라고 속삭였다.'),
       ('16','With a heavy heart, he rode Big Red to the shipping [mark:9: container].',
             '무거운 마음으로 그는 Big Red를 운송 컨테이너까지 타고 갔다.'),
       ('17','He said goodbye when the door closed.',
             '문이 닫힐 때 그는 작별 인사를 했다.'),
     ]),
   ],
   quiz=dict(kind='input', label='Q1',
     q='Why did Leo decide to donate Big Red?', qkr='해석x',
     a='Because it became too small for him.', akr='해석x',
     qsrc='3_140_question_02', asrc='3_140_question_03'),
 ),

 'p141_01': dict(
   num='141', qbtn='Q2~Q3',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','Big Red traveled to a new country.',
             'Big Red는 새로운 나라로 이동했다.'),
       ('02','|1|It found a new home with Emily, who lived with her grandmother and helped her in the fields.',
             '그것은 Emily와 함께 하는 새로운 집을 찾았는데, Emily는 할머니와 함께 살며 밭일을 도왔다.'),
       ('03','|2|Thanks to Big Red, Emily could ride to [mark:1: scare birds away] from the fields and go to the market to sell [mark:2: goods].',
             'Big Red 덕분에 Emily는 밭에서 새를 쫓기 위해 자전거를 타고 물건을 팔러 시장에 갈 수 있었다.'),
       ('04','She also rode Big Red to school every day.',
             '그녀는 또한 매일 Big Red를 타고 학교에 갔다.'),
       ('05','But more than anything, riding the bike gave her a quiet joy.',
             '그러나 무엇보다 자전거를 타는 것은 그녀에게 조용한 기쁨을 주었다.'),
       ('06','She felt the wind on her face and began to dream of a bigger world.',
             '그녀는 바람이 얼굴을 스치는 것을 느꼈고 더 넓은 세상을 꿈꾸기 시작했다.'),
     ]),
     ('para', [
       ('07','|3|Then one day, Emily was given a chance to continue her studies at a school in a big city.',
             '그러던 어느 날, Emily는 큰 도시의 학교에서 공부를 계속할 기회를 얻게 되었다.'),
       ('08','She knew her journey with Big Red had come to an end.',
             '그녀는 Big Red와의 여정이 끝났음을 알았다.'),
       ('09','|4|She hoped it would go to someone who [mark:3: truly] needed it.',
             '그녀는 그것이 정말로 그것을 필요로 하는 누군가에게 가기를 바랐다.'),
     ]),
   ],
   quiz=dict(kind='input2', label=['Q2', 'Q3'],
     items=[dict(label='Q2', q='What did riding Big Red give Emily?', qkr='해석x', a='It gave her a quiet joy.', akr='해석x', qsrc='3_141_question_02', asrc='3_141_question_03'),
            dict(label='Q3', q='Why did Emily have to stop using Big Red?', qkr='해석x', a='Because she was given a chance to continue her studies at a school in a big city.', akr='해석x', qsrc='3_141_question_05', asrc='3_141_question_06')]),
 ),

 'p142_01': dict(
   num='142', qbtn='Q4~Q5',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','One morning, Emily heard a news report on the radio.',
             '어느 날 아침, Emily는 라디오에서 뉴스 보도를 들었다.'),
       ('02','[mark:1: Healthcare] workers at a local [mark:2: clinic] needed bikes to visit sick people.',
             '한 지역 병원에서 보건 의료 종사자들이 아픈 사람들을 방문하기 위해 자전거가 필요했다.'),
       ('03','Emily looked at Big Red and smiled.',
             'Emily는 Big Red를 바라보며 미소 지었다.'),
       ('04','|1|She knew what to do.',
             '그녀는 무엇을 해야 할지 알았다.'),
       ('05','|2|That afternoon, she [mark:3: offered] Big Red to the clinic and felt proud that it would continue helping others.',
             '그날 오후, 그녀는 Big Red를 병원에 제공했고 그것이 다른 사람들을 계속 돕게 된 것이 자랑스러웠다.'),
       ('06','She [mark:4: patted] the seat and whispered, “Thanks for everything.”',
             '그녀는 자전거의 안장을 토닥거리며 “모든 것에 고마워.”라고 속삭였다.'),
     ]),
     ('para', [
       ('07','|3|At the clinic, the bike was turned into an [mark:5: ambulance] by adding a [mark:6: trailer].',
             '병원에서 자전거는 트레일러를 달아 구급차로 바뀌었다.'),
       ('08','The trailer had a [mark:7: stretcher] and a [mark:8: safety belt] in order to keep [mark:9: patients] safe during the ride.',
             '트레일러에는 환자들을 이동 중에 안전하게 지켜기 위해 들것과 안전벨트가 있었다.'),
       ('09','Big Red was ready to work.',
             'Big Red는 일할 준비가 되었다.'),
     ]),
   ],
   quiz=dict(kind='input2', label=['Q4', 'Q5'],
     items=[dict(label='Q4', q='How did Emily feel when she offered Big Red to the clinic?', qkr='해석x', a='She felt proud that it would continue helping others.', akr='해석x', qsrc='3_142_question_02', asrc='3_142_question_03'),
            dict(label='Q5', q='How was the bike turned into an ambulance?', qkr='해석x', a='It was turned into an ambulance by adding a trailer.', akr='해석x', qsrc='3_142_question_05', asrc='3_142_question_06')]),
   think=dict(q='Have you ever had something special that became too small for you?', qkr='해석x', src='3_142_think_about_this_01',
              ex=[('3_142_think_about_this_ex_01','Yes, I had my favorite sneakers that became too small for me.','해석x'),
                  ('3_142_think_about_this_ex_02','I gave them to a friend who wanted them.','해석x'),
                  ('3_142_think_about_this_ex_03','Yes, I had some clothes that became too small for me.','해석x'),
                  ('3_142_think_about_this_ex_04','I donated them to a children’s center.','해석x')]),
 ),

 'p143_01': dict(
   num='143', qbtn='Q6~Q7',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','|1|A healthcare worker whose name was Hannah began using the bike.',
             'Hannah라는 이름의 보건 의료 종사자가 그 자전거를 사용하기 시작했다.'),
       ('02','|2|She rode Big Red along small [mark:1: paths] where cars couldn’t go, [mark:2: delivering] medicines and bringing patients to the clinic.',
             '그녀는 약을 배달하고 환자들을 병원으로 데려오며 자동차가 갈 수 없는 좁은 길을 따라 Big Red를 달렸다.'),
       ('03','Soon it became famous for its good work, and the villagers loved it.',
             '곧 그것은 그것의 좋은 일로 유명해졌고, 마을 사람들은 그것을 매우 좋아했다.'),
     ]),
     ('para', [
       ('04','When Hannah [mark:3: took on] a new role in another town, she rode Big Red for the last time.',
             'Hannah가 다른 마을에서 새 역할을 맡게 되었을 때, 그녀는 마지막으로 Big Red를 탔다.'),
       ('05','|3|She whispered “Thank you,”',
             '그녀는 그것의 여정이 어디서 처음 시작되었는지 궁금해하며 “고마워.”라고 속삭였다.'),
       ('06','wondering where its journey had first begun.',
             '해석x'),
       ('07','|4|There was no [mark:4: hint] that a girl had once ridden it to the market or that a boy had ridden it around a small town.',
             '한 소녀가 한때 그것을 시장에 타고 갔다는 흔적 또는 한 소년이 작은 마을을 돌아다녔다는 흔적도 없었다.'),
       ('08','But they remembered Big Red, and Hannah would, too.',
             '그러나 그들은 Big Red를 기억했고, Hannah 역시 그럴 것이다.'),
     ]),
     ('para', [
       ('09','Adapted from The Red Bicycle',
             '해석x'),
       ('10','(Jude Isabella, 2015)',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input2', label=['Q6', 'Q7'],
     items=[dict(label='Q6', q='Where did Hannah ride Big Red?', qkr='해석x', a='She rode it along small paths where cars couldn’t go.', akr='해석x', qsrc='3_143_question_02', asrc='3_143_question_03'),
            dict(label='Q7', q='What did Hannah whisper when she rode Big Red for the last time?', qkr='해석x', a='She whispered “Thank you.”', akr='해석x', qsrc='3_143_question_05', asrc='3_143_question_06')]),
   mission=dict(kr='해석x',
                en='Did following the path Big Red took help you understand the story better?',
                src='3_143_mission_01'),
 ),

}

ORDER = ['p140_02','p141_01','p142_01','p143_01']

# 배경 이미지 원본 크기 (png 에서 읽음). 비어 있으면 크기 CSS 를 넣지 않는다.
IMG = {
 'p140_02': dict(bg=(2560, 3998), title=(1036, 362)),
 'p141_01': dict(bg=(2560, 3056)),
 'p142_01': dict(bg=(2560, 3214)),
 'p143_01': dict(bg=(2560, 3120)),
}

# ============ 레이아웃 (사람이 눈으로 맞추는 값) ============

# 제목 이미지 위 단어 버튼 (left, top).
# read_measure.py 가 찍어 주는 "WORDBTN left 후보" 를 넣으세요.
WORDBTN = {
 'p140_02': [],
 'p141_01': [],
 'p142_01': [],
 'p143_01': [],
}

# 배경 그림 위 글자 자리. --layout 파일에서 온다.
CSS_LAYOUT = {
 'p140_02': '''
.readingCont { position: relative; }

.mainContent .ParagraphBox { margin-top: 140px; }
.mainContent .ParagraphBox .Paragraph { width: 920px; margin-left: 330px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
''',
 'p141_01': '''
.readingCont { position: relative; }

.mainContent .ParagraphBox { margin-top: 30px; }
.mainContent .ParagraphBox .Paragraph { width: 1000px; margin-left: 170px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
''',
 'p142_01': '''
.readingCont { position: relative; }

.mainContent .ParagraphBox { margin-top: 330px; }
.mainContent .ParagraphBox .Paragraph { width: 1000px; margin-left: 200px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
''',
 'p143_01': '''
.readingCont { position: relative; }

.mainContent .ParagraphBox { margin-top: 300px; }
.mainContent .ParagraphBox .Paragraph { width: 1000px; margin-left: 170px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
/* 출처 표기 — 작게, 오른쪽 */
.mainContent .ParagraphBox .Paragraph:nth-of-type(3) { margin-top: 20px; text-align: right; text-indent: 0; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(3) .readText { font-size: 24px; }
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

  <title>p140_01</title>
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
            <comp-translate kr="글의 흐름을 파악하며 읽기" en="Reading for understanding the flow of the text" src="media/mp3/3_140_read_smart_01.mp3" narrIdx="3" clickIdx="1"></comp-translate>
          </div>
        </div>

        <div class="headerInner Sub">
          <div class="headerText">
            <comp-translate kr="등장인물과 사건의 흐름을 파악하며 읽으면 글을 더 잘 이해할 수 있습니다." en="You can understand the text better by paying attention to the characters and the order of events." src="media/mp3/3_140_read_smart_02.mp3" narrIdx="3" clickIdx="2"></comp-translate>
          </div>
        </div>
      </header>

      <div class="mainContent">
        <div class="missionBox">
          <span class="missionTit">
            <b class="js-narrationBtn narrText" data-narr-idx="3" data-narr-src="include/media/common/missoin.mp3">Mission!</b>
          </span>

          <div class="missionTxt">
            <comp-translate kr="본문에서 Big Red가 이동한 과정을 파악하며 글을 읽어 봅시다." en="Follow the path Big Red takes while reading the text." src="media/mp3/3_140_read_smart_04.mp3" narrIdx="3" clickIdx="3"></comp-translate>
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