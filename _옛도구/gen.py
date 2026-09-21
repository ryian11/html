# -*- coding: utf-8 -*-
"""Dictation 팝업(dic1) 생성기 — lesson03 구조 기준"""
import re, sys
sys.path.insert(0, '/home/claude/cj')
import src

TAIL_PUNCT = '.,!?;:'

def sticker(sentence):
    out = []
    for tok in sentence.split():
        core = tok
        tail = ''
        while core and core[-1] in TAIL_PUNCT:
            tail = core[-1] + tail; core = core[:-1]
        if not core:                       # 문장부호만 있는 토큰
            if out: out[-1] += tok
            else: out.append(tok)
            continue
        out.append('|%s|%s' % (core, tail))
    s = ' '.join(out)
    return re.sub(r'\s+([%s]+)' % re.escape(TAIL_PUNCT), r'\1', s)

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')

HEAD = '''<!DOCTYPE html>
<html lang="ko">

<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0">
\t<link rel="stylesheet" href="../include/contentsUI/css/index.css">
\t<link rel="stylesheet" href="../include/css/common.css">
\t<link rel="stylesheet" href="../include/css/dictation.css">
\t<link rel="stylesheet" href="../include/css/font.css">

\t<title>{page}_dic1</title>
\t<style>
\t\t.scriptContainer .scriptBox:not(.subTitBox) .Script:first-of-type {{
\t\t\tmargin-left: 20px;
\t\t}}

\t\t.iframePopup[data-use="dictation"] .middleinput .inputBox:nth-of-type(3),
\t\t.iframePopup[data-use="dictation"] .inputBox {{
\t\t\twidth: 200px;
\t\t}}

\t\t.iframePopup[data-use="dictation"] .firstLong .inputBox:first-of-type,
\t\t.iframePopup[data-use="dictation"] .lastLong .inputBox:last-of-type,
\t\t.iframePopup[data-use="dictation"] .inputBox.long {{
\t\t\twidth: 250px;
\t\t}}

\t\t.iframePopup[data-use="dictation"] .short .inputBox,
\t\t.iframePopup[data-use="dictation"] .firstShort .inputBox:first-of-type,
\t\t.iframePopup[data-use="dictation"] .secondShort .inputBox:nth-of-type(2),
\t\t.iframePopup[data-use="dictation"] .middleShort .inputBox:nth-of-type(2),
\t\t.iframePopup[data-use="dictation"] .lastShort .inputBox:last-of-type {{
\t\t\twidth: 140px;
\t\t}}

\t\t.iframePopup[data-use="dictation"] .firstCapi .inputBox:first-of-type {{
\t\t\ttext-transform: capitalize;
\t\t}}
\t</style>
</head>

<body>
\t<div class="js-iframePopupContainer js-scale iframePopup" data-use="dictation" data-type="oneLine">
\t\t<div class="popContentContainer">
\t\t\t<!-- popHeader -->
\t\t\t<header class="popHeader">
\t\t\t\t<div class="popHeaderInner">
\t\t\t\t\t<h2 class="popHeaderTit">
\t\t\t\t\t\t<span>Dictation</span>
\t\t\t\t\t</h2>
\t\t\t\t</div>
\t\t\t\t<button class="js-closePopBtn closePopBtn"></button>
\t\t\t</header>

\t\t\t<!-- popContentBox -->
\t\t\t<div class="popContentBox tabBox">
\t\t\t\t<!-- tabBtnBox -->
\t\t\t\t<div class="tabBtnBox">
\t\t\t\t\t<button class="js-sliderBtn suppleBtn" data-sld-idx="1" data-sld-cont="1"></button>
\t\t\t\t\t<button class="js-sliderBtn basicBtn selected" data-sld-idx="1" data-sld-cont="2"></button>
\t\t\t\t\t<button class="js-sliderBtn deepBtn" data-sld-idx="1" data-sld-cont="3"></button>
\t\t\t\t\t<button class="js-sliderBtn newBtn" data-sld-idx="1" data-sld-cont="4"></button>
\t\t\t\t</div>

\t\t\t\t<!-- popContent -->
\t\t\t\t<div class="js-slider Tab popContent" data-sld-idx="1">
'''

QUIZ_TAB = '''\t\t\t\t\t<!-- 탭{n} -->
\t\t\t\t\t<div class="js-sliderContent js-quizContainer tabContent" data-sld-cont="{n}" data-quiz-type="input" data-quiz-opts="noAlert, noSound, noSolve, noRemoveSpace">
\t\t\t\t\t\t<div class="js-scrollContainer scrollContainer tabActBox" data-scroll-idx="{i}">
\t\t\t\t\t\t\t<div class="js-player Player js-scrollBox scrollBox" data-ply-type="language" data-ply-controls="play, pause, stop, progress" data-ply-opts="speed" data-speed-btn="0.8,1.0,1.2,1.5" data-ply-idx="{i}" data-scroll-idx="{i}">
\t\t\t\t\t\t\t\t<!-- scriptContainer -->
\t\t\t\t\t\t\t\t<div class="js-languageContainer scriptContainer" data-ply-idx="{i}">
\t\t\t\t\t\t\t\t\t<!-- Paragraph -->
\t\t\t\t\t\t\t\t\t<div class="Paragraph">
{boxes}
\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<!-- btnHandlerBox -->
\t\t\t\t\t\t<div class="btnHandlerBox selected" data-include="player">
\t\t\t\t\t\t\t<div class="btnBundle">
\t\t\t\t\t\t\t\t<div class="controlsBox" data-use="ui">
\t\t\t\t\t\t\t\t\t<div class="js-controlBoxContainer mediaControl" data-ply-type="language" data-ply-idx="{i}"></div>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<comp-btn-group hdlQuiz="{i}"></comp-btn-group>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

'''

TAB4 = '''\t\t\t\t\t<!-- 탭4 -->
\t\t\t\t\t<div class="js-sliderContent tabContent" data-sld-cont="4" data-act="attachSticker">
\t\t\t\t\t\t<!-- topEleBox -->
\t\t\t\t\t\t<div class="topEleBox">
\t\t\t\t\t\t\t<div class="btnBundle">
\t\t\t\t\t\t\t\t<button class="js-wordCoverBtn wordCoverBtn"></button>
\t\t\t\t\t\t\t</div>

\t\t\t\t\t\t\t<div class="btnBundle">
\t\t\t\t\t\t\t\t<button class="js-backBtn backBtn"></button>
\t\t\t\t\t\t\t\t<button class="js-firstBtn firstBtn"></button>
\t\t\t\t\t\t\t\t<!-- 사용 방법 -->
\t\t\t\t\t\t\t\t<div class="howToUseBtnBox">
\t\t\t\t\t\t\t\t\t<button class="js-openPopBtn openPopBtn howToUseBtn" data-pop-idx="10"></button>
\t\t\t\t\t\t\t\t\t<div class="js-popupContent miniPopup" data-pop-idx="10" data-use="howtouse">
\t\t\t\t\t\t\t\t\t\t<div class="miniContent arrayV">
\t\t\t\t\t\t\t\t\t\t\t<p><span class="wordCoverIcon"></span>를 클릭한 후, 화면에서 빈칸 처리할 단어를 클릭하면 스티커로 가릴 수 있습니다. 자유롭게
\t\t\t\t\t\t\t\t\t\t\t\tDictation을 만들어 수업에 활용해 보세요.</p>
\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t<button class="js-printBtn printBtn"></button>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="js-scrollContainer scrollContainer tabActBox" data-scroll-idx="3">
\t\t\t\t\t\t\t<div class="js-player Player js-scrollBox scrollBox" data-ply-type="language" data-ply-controls="play, pause, stop, progress" data-ply-opts="speed" data-speed-btn="0.8,1.0,1.2,1.5" data-ply-idx="3" data-scroll-idx="3">
\t\t\t\t\t\t\t\t<!-- scriptContainer -->
\t\t\t\t\t\t\t\t<div class="js-languageContainer scriptContainer js-printContainer" data-ply-idx="3">
\t\t\t\t\t\t\t\t\t<!-- Paragraph -->
\t\t\t\t\t\t\t\t\t<div class="Paragraph">
{boxes}
\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>

\t\t\t\t\t\t<div class="btnHandlerBox selected" data-include="player">
\t\t\t\t\t\t\t<div class="btnBundle">
\t\t\t\t\t\t\t\t<div class="controlsBox" data-use="ui">
\t\t\t\t\t\t\t\t\t<div class="js-controlBoxContainer mediaControl" data-ply-type="language" data-ply-idx="3"></div>
\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>

'''

FOOT = '''\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</div>
\t<script src="../include/js/config.js"></script>
\t<script src="../include/js/pageManager.js"></script>
\t<script src="../include/js/components.js"></script>
\t<script src="../include/js/common.js"></script>
\t<script src="../include/js/dom-to-image.min.js"></script>
\t<script src="../include/js/dictation.js"></script>
\t<script>
\t\tdocument.addEventListener("DOMContentLoaded", () => {
\t\t\twindow.CONFIG.AUDIO_SRC = '../include/media/'
\t\t});
\t</script>
</body>

</html>'''

IND = '\t' * 10          # script-cont 들여쓰기
BIND = '\t' * 9          # comp-script-box 들여쓰기

def quiz_boxes(groups, tab_i):
    """groups: [[(mp3, marked)], ...] 문단 단위"""
    out, n = [], 0
    for g in groups:
        lines = [BIND + '<!-- scriptBox -->', BIND + '<comp-script-box>']
        for mp3, marked in g:
            en, sizes = src.split_groups(marked)
            attrs = 'src="../media/mp3/%s" en="%s"' % (mp3, esc(en))
            if sizes:
                idx, n = src.item_idx(sizes, n)
                attrs += ' handler="%d" itemIdx="%s"' % (tab_i, idx)
            lines.append(IND + '<script-cont %s></script-cont>' % attrs)
        lines.append(BIND + '</comp-script-box>')
        out.append('\n'.join(lines))
    return '\n'.join(out)

def sticker_boxes(groups):
    out = []
    for g in groups:
        lines = [BIND + '<!-- scriptBox -->', BIND + '<comp-script-box>']
        for mp3, marked in g:
            plain = src.strip_marks(marked)
            lines.append(IND + '<script-cont src="../media/mp3/%s" sticker="%s"></script-cont>'
                         % (mp3, esc(sticker(plain))))
        lines.append(BIND + '</comp-script-box>')
        out.append('\n'.join(lines))
    return '\n'.join(out)

def build(page, tabs_groups):
    """tabs_groups: [보충groups, 기본groups, 심화groups]"""
    html = HEAD.format(page=page)
    for k, groups in enumerate(tabs_groups):
        html += QUIZ_TAB.format(n=k + 1, i=k, boxes=quiz_boxes(groups, k))
    html += TAB4.format(boxes=sticker_boxes(tabs_groups[0]))
    html += FOOT
    return html
