# -*- coding: utf-8 -*-
# 2단원 Reading 본문 페이지 데이터
# read_import.py 가 만든 초안입니다. `# ???` 가 붙은 곳을 확인하세요.
# 출처: 녹음 대본 2과 / 스토리보드 Lesson 2 / 지도서 각론2

PAGES = {
 'p032_02': dict(
   num='032', qbtn='Q1',
   title=dict(src='3_032_read_00', en='Seeds of Hope: Preserving Our Future', kr='해석x',
              cls='mainTitle', mark='[mark:1: ]'),
   blocks=[
     ('para', [
       ('01','I\'m a little seed, and I\'m resing in a very special place.',
             '해석x'),
       ('02','It’s the Baekdudaegan Global Seed [mark:2: Vault].',
             '해석x'),
       ('03','Can you guess what this place is for?',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='tf', label=['Q1'],
     # ??? 정답(ans) 은 1=True, 2=False 입니다. 원고를 보고 확인하세요.
     items=[dict(q='The little seed is resting in the Baekdudaegan Global Seed Vault.', qkr='해석x', ans='1', src='3_032_question_02')]),
 ),

 'p033_01': dict(
   num='033', qbtn='Q2~Q3',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','What is a seed vault?',
             '해석x'),
       ('02','A seed vault is a safe place that [mark:1: stores] seeds.',
             '해석x'),
       ('03','There are many seed vaults around the world.',
             '해석x'),
       ('04','The most famous two are in Norway, and right here in Korea.',
             '해석x'),
       ('05','The seed vault in Norway [mark:2: mostly] stores the seeds of plants that people grow for food.',
             '해석x'),
       ('06','[mark:3: On the other hand], the BGSV stores the seeds of wild plants.',
             '해석x'),
       ('07','These plants grow naturally in mountains and fields.',
             '해석x'),
       ('08','The BGSV has been preserving its seeds under good conditions since 2018.',
             '해석x'),
       ('09','It’s [mark:4: located] [mark:5: underground] in the middle of a mountain.',
             '해석x'),
       ('10','So, the seeds in the seed vault can be protected from natural [mark:6: disasters], such as [mark:7: earthquakes].',
             '해석x'),
       ('11','The seeds are kept in a cold and dry place inside the vault.',
             '해석x'),
       ('12','Thanks to these conditions, seeds like me can stay safe for a long time.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input2', label=['Q2', 'Q3'],
     items=[dict(label='Q2', q='What kinds of seeds does the BGSV store?', qkr='해석x', a='It stores the seeds of wild plants.', akr='해석x', qsrc='3_033_question_02', asrc='3_033_question_03'),
            dict(label='Q3', q='Where is the BGSV located?', qkr='해석x', a='It\'s located underground in the middle of a mountain.', akr='해석x', qsrc='3_033_question_05', asrc='3_033_question_06')]),
   think=dict(q='What seed do you want to keep in the seed vault?', qkr='해석x', src='3_033_think_about_this_01',
              ex=[('3_033_think_about_this_ex_01','I want to keep rice seeds in the seed vault because rice is the main food for many people around the world.','해석x'),
                  ('3_033_think_about_this_ex_02','I want to keep four-leaf clover seeds because they bring hope and good luck.','해석x')]),
 ),

 'p034_01': dict(
   num='034', qbtn='Q4',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','Why is it important to keep seeds?',
             '해석x'),
       ('02','Do you know why saving seeds like me is important?',
             '해석x'),
       ('03','We grow into plants, and plants give people many things such as food, [mark:1: medicine], and clean air.',
             '해석x'),
       ('04','Plants also keep the environment healthy.',
             '해석x'),
       ('05','But today, many plants are in danger.',
             '해석x'),
       ('06','Because of the climate crisis, natural disasters, and other problems, many plant species are [mark:2: disappearing].',
             '해석x'),
       ('07','That’s why storing seeds is a smart way to protect plants.',
             '해석x'),
       ('08','If plants disappear, seeds can bring them back.',
             '해석x'),
       ('09','This way, we can preserve biodiversity.',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q4',
     q='What do plants give people?', qkr='해석x',
     a='They give many things such as food, medicine, and clean air.', akr='해석x',
     qsrc='3_034_question_02', asrc='3_034_question_03'),
 ),

 'p035_01': dict(
   num='035', qbtn='Q5',
   title=None,   # 제목·소제목 이미지가 없는 쪽
   blocks=[
     ('para', [
       ('01','What kinds of seeds are kept?',
             '해석x'),
       ('02','There are many seeds here in the BGSV.',
             '해석x'),
       ('03','Let me tell you my story.',
             '해석x'),
       ('04','I came from a special [mark:1: fir] tree at Haeinsa.',
             '해석x'),
       ('05','There is an old story about the fir tree.',
             '해석x'),
       ('06','Choi Chiwon, a [mark:2: scholar] from the Silla [mark:3: Dynasty], stuck his walking [mark:4: stick] in the ground, and it turned into a tree!',
             '해석x'),
       ('07','With this story and its long history, the tree became special to people.',
             '해석x'),
       ('08','But in 2019, the tree was [mark:6: damaged] by a [mark:7: typhoon].',
             '해석x'),
       ('09','People saved me and brought me here to the vault.',
             '해석x'),
       ('10','You can also find the seeds of the Ara Red [mark:8: Lotus] here.',
             '해석x'),
       ('11','They were found [mark:9: by accident] at a historical site.',
             '해석x'),
       ('12','Later, [mark:10: researchers] discovered that they were about 700 years old, from the Goryeo Dynasty.',
             '해석x'),
       ('13','Some of these seeds even grew into beautiful lotus flowers!',
             '해석x'),
       ('14','If there is a big crisis, people will need seeds like me.',
             '해석x'),
       ('15','Then, I will go out into the world again.',
             '해석x'),
       ('16','But for now, I’m happy to stay safe here.',
             '해석x'),
       ('17','Let’s hope the seeds never have to leave the seed vault!',
             '해석x'),
     ]),
   ],
   quiz=dict(kind='input', label='Q5',
     q='Where was the special fir tree?', qkr='해석x',
     a='It was at Haeinsa.', akr='해석x',
     qsrc='3_035_question_02', asrc='3_035_question_03'),
   mission=dict(kr='해석x',
                en='Did guessing the meaning of the unfamiliar words from context help you understand the text?',
                src='3_035_mission_01'),
 ),

}

ORDER = ['p032_02','p033_01','p034_01','p035_01']

# 배경 이미지 원본 크기 (png 에서 읽음). 비어 있으면 크기 CSS 를 넣지 않는다.
IMG = {
 'p032_02': dict(bg=(2560, 2380), title=(1280, 654)),
 'p033_01': dict(bg=(2560, 3186)),
 'p034_01': dict(bg=(2560, 3228)),
 'p035_01': dict(bg=(2560, 4588)),
}

# ============ 레이아웃 (사람이 눈으로 맞추는 값) ============

# 제목 이미지 위 단어 버튼 (left, top).
# read_measure.py 가 찍어 주는 "WORDBTN left 후보" 를 넣으세요.
WORDBTN = {
 'p032_02': [(0, 0)],   # ??? 측정값을 넣으세요
 'p033_01': [],
 'p034_01': [],
 'p035_01': [],
}

# 배경 그림 위 글자 자리. --layout 파일에서 온다.
CSS_LAYOUT = {
 'p032_02': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p033_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p034_01': '''
.mainContent .ParagraphBox { margin-top: 30px; }
''',
 'p035_01': '''
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

  <title>p032_01</title>
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
            <comp-translate kr="단어의 의미를 추측하며 읽기" en="Guessing the meaning of the word while reading" src="media/mp3/3_032_read_smart_01.mp3" narrIdx="3" clickIdx="1"></comp-translate>
          </div>
        </div>

        <div class="headerInner Sub">
          <div class="headerText">
            <comp-translate kr="문맥을 살펴보면서 모르는 단어의 뜻을 추측하며 읽으면 글을 더 잘 이해할 수 있습니다." en="You can understand better if you guess the meaning of the unfamiliar words from context while reading." src="media/mp3/3_032_read_smart_02.mp3" narrIdx="3" clickIdx="2"></comp-translate>
          </div>
        </div>
      </header>

      <div class="mainContent">
        <div class="missionBox">
          <span class="missionTit">
            <b class="js-narrationBtn narrText" data-narr-idx="3" data-narr-src="include/media/common/missoin.mp3">Mission!</b>
          </span>

          <div class="missionTxt">
            <comp-translate kr="모르는 단어가 나올 때 문맥을 살펴보면서 그 뜻을 추측하며 글을 읽어 봅시다." en="Read the text, guessing the meaning of the unfamiliar words from context." src="media/mp3/3_032_read_smart_03.mp3" narrIdx="3" clickIdx="3"></comp-translate>
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