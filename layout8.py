# -*- coding: utf-8 -*-
"""8단원 지면 구조 — 스토리보드에 박힌 교과서 지면(140~143쪽)을 보고 적었다."""

# 문단 나눔
PARAS = {
 '140': [['02','03','04','05','06','07','08','09','10','11'],
         ['12','13','14','15','16','17']],
 '141': [['01','02','03','04','05','06'], ['07','08','09']],
 '142': [['01','02','03','04','05','06'], ['07','08','09']],
 '143': [['01','02','03'], ['04','05','06','07','08'], ['09','10']],
}

LABELS = {}
DROP = set()
PREFIX = {}
SPEAKER = ''

# 지면대로 고친 본문
#  · 대본에 따옴표 안 대사가 빠져 있어 지면대로 넣는다
#  · 두 낱말 이상인 미니 단어장 항목은 손으로 감싼다
TEXT = {
 ('140', '15'): 'He [mark:7: whispered], “Thank you for all the [mark:8: adventures].”',
 ('141', '03'): 'Thanks to Big Red, Emily could ride to [mark:1: scare birds away] '
                'from the fields and go to the market to sell [mark:2: goods].',
 ('142', '06'): 'She [mark:4: patted] the seat and whispered, “Thanks for everything.”',
 ('143', '04'): 'When Hannah [mark:3: took on] a new role in another town, '
                'she rode Big Red for the last time.',
 # 구문 3 이 05+06 두 take 에 걸쳐 있어 |3| 을 손으로 넣는다
 ('143', '05'): '|3|She whispered “Thank you,”',
}

_COMMON = '''
.readingCont { position: relative; }
'''

CSS = {
 'p140_02': _COMMON + '''
.mainContent .ParagraphBox { margin-top: 140px; }
.mainContent .ParagraphBox .Paragraph { width: 920px; margin-left: 330px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
''',
 'p141_01': _COMMON + '''
.mainContent .ParagraphBox { margin-top: 30px; }
.mainContent .ParagraphBox .Paragraph { width: 1000px; margin-left: 170px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
''',
 'p142_01': _COMMON + '''
.mainContent .ParagraphBox { margin-top: 330px; }
.mainContent .ParagraphBox .Paragraph { width: 1000px; margin-left: 200px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
''',
 'p143_01': _COMMON + '''
.mainContent .ParagraphBox { margin-top: 300px; }
.mainContent .ParagraphBox .Paragraph { width: 1000px; margin-left: 170px; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(2) { margin-top: 26px; }
/* 출처 표기 — 작게, 오른쪽 */
.mainContent .ParagraphBox .Paragraph:nth-of-type(3) { margin-top: 20px; text-align: right; text-indent: 0; }
.mainContent .ParagraphBox .Paragraph:nth-of-type(3) .readText { font-size: 24px; }
''',
}

# 배경·제목 이미지 원본 크기 (브라우저로 읽은 값)
IMG = {
 'p140_02': dict(bg=(2560, 3998), title=(1036, 362)),
 'p141_01': dict(bg=(2560, 3056)),
 'p142_01': dict(bg=(2560, 3214)),
 'p143_01': dict(bg=(2560, 3120)),
}
