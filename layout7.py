# -*- coding: utf-8 -*-
"""7단원 지면 구조 — 스토리보드에 박힌 교과서 지면(122~125쪽)을 보고 적었다.
   read_import.py 7 --layout layout7.py 로 쓴다."""

# 문단 나눔 : 쪽 -> [[그 문단에 드는 mp3 뒷번호들], ...]
PARAS = {
 '122': [['01', '02', '03', '04']],
 '123': [['02', '03', '04', '05'], ['06'], ['07', '08', '09', '10', '11']],
 '124': [['01', '02', '03'], ['04', '05', '06', '07', '08']],
 '125': [['01', '02'], ['03', '04', '05', '06'], ['07_1', '08', '09'],
         ['10', '11', '12'], ['13']],
}

# 그림 위에 따로 놓는 라벨 : (쪽, 뒷번호) -> css 클래스
LABELS = {}

# 아예 빼는 것 : 그림 안에 이미 그려져 있는 낱말들
DROP = {
 ('123', '01'),   # Earth
 ('124', '09'),   # Visible Light
 ('124', '10'),   # Infrared Light
}

# 문단 첫머리에 붙는 것 : (쪽, 뒷번호) -> 'mic' | 'speaker'
PREFIX = {
 ('122', '01'): 'mic',
 ('123', '02'): 'speaker', ('123', '06'): 'mic', ('123', '07'): 'speaker',
 ('124', '01'): 'mic',     ('124', '04'): 'speaker',
 ('125', '01'): 'mic',     ('125', '03'): 'speaker', ('125', '07_1'): 'mic',
 ('125', '10'): 'speaker', ('125', '13'): 'mic',
}
SPEAKER = 'Dr. Roman'

# 지면대로 고친 본문 (대본과 다른 곳)
TEXT = {
 ('122', '02'): '(JWST)',    # 대본에는 괄호가 없으나 지면은 (JWST)
}

# 배경 그림 위 글자 자리 (눈으로 맞춘 값)
_COMMON = '''
.readingCont { position: relative; }
/* 문단 첫머리 — 말하는 이와 마이크 아이콘 (본문 글자가 아니라 꾸밈이라 CSS 로 붙인다) */
.mainContent .ParagraphBox .Paragraph.spk .readText:first-of-type::before {
	content: 'Dr. Roman'; color: #2E6DB4; font-family: var(--gothic_EB); margin-right: 18px; }
.mainContent .ParagraphBox .Paragraph.mic .readText:first-of-type::before {
	content: ''; display: inline-block; width: 26px; height: 26px; margin-right: 10px;
	vertical-align: -5px; background: url(../images/PAGE/icon_mic.png) center/contain no-repeat; }
.readingCont .label { position: absolute; margin: 0; font-family: var(--gothic_EB); }
'''

CSS = {
 'p122_02': _COMMON.replace('PAGE','p122_02') + '''
.mainContent .ParagraphBox { margin-top: 250px; }
.mainContent .ParagraphBox .Paragraph { width: 880px; margin-left: 350px; }
''',
 'p123_01': _COMMON.replace('PAGE','p123_01') + '''
.mainContent .ParagraphBox { margin-top: 395px; }
.mainContent .ParagraphBox .Paragraph { width: 1000px; margin-left: 170px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(3) { margin-top: 26px; }
''',
 'p124_01': _COMMON.replace('PAGE','p124_01') + '''
.mainContent .ParagraphBox { margin-top: 430px; }
.mainContent .ParagraphBox .Paragraph { width: 1020px; margin-left: 140px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(1) { width: 600px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
''',
 'p125_01': _COMMON.replace('PAGE','p125_01') + '''
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

# 배경·제목 이미지 원본 크기 (브라우저로 읽은 값 — 컨테이너에서는 파일을 못 봐서 박아 둔다)
IMG = {
 'p122_02': dict(bg=(2560, 1918), title=(1422, 396)),
 'p123_01': dict(bg=(2560, 3388)),
 'p124_01': dict(bg=(2560, 3504)),
 'p125_01': dict(bg=(2560, 4369)),
}
