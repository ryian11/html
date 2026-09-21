# -*- coding: utf-8 -*-
"""lesson08 dic1: 정답 실측폭 기반 input 폭 + 그룹 전체가 보이는 scrollTop"""
import re, os, json, asyncio
exec(open('/home/claude/cj/measure/opt.py').read().split('async def main')[0])

LADDER = [140, 200, 250, 300, 350, 400]
PAD    = 20     # input 좌우 padding
GAP    = 14     # 글자 오른쪽 최소 여백
BOXH   = 548
SAFE   = 20     # 위아래 안전 여백
LEAD   = 20     # 그룹 첫 문장 위 여유
# 실측 보정: 이 컨테이너(headless Chromium)가 실제 기기보다 본문 글자를 약 14px 넓게 잡는다.
# 그대로 재면 아슬아슬한 줄이 한 줄 더 접혀 scrollTop 이 한 줄(68px)씩 어긋난다.
# 측정할 때만 본문 칸을 14px 넓혀서 실제 기기와 같은 줄바꿈이 나오게 한다(산출물에는 안 들어감).
CALIB  = '.iframePopup[data-use="dictation"] .tabActBox{padding-right:1px !important;}'

STYLE_HEAD = """	<style>
		.scriptContainer .scriptBox:not(.subTitBox) .Script:first-of-type {
			margin-left: 20px;
		}

		.iframePopup[data-use="dictation"] .inputBox {
			width: 200px;
		}
"""
STYLE_TAIL = """
		.iframePopup[data-use="dictation"] .firstCapi .inputBox:first-of-type {
			text-transform: capitalize;
		}
	</style>"""

SPKW_JS = """() => {
  let mx = 0;
  document.querySelectorAll('.tabContent .Speaker strong').forEach(el => {
    mx = Math.max(mx, el.getBoundingClientRect().width);
  });
  return Math.ceil(mx);
}"""

MEASURE_TEXT = """() => {
  const c=document.createElement('canvas').getContext('2d');
  const o={};
  document.querySelectorAll('.tabContent .js-quizItem').forEach(inp=>{
    const a=inp.getAttribute('data-answer')||''; const cs=getComputedStyle(inp);
    c.font=cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;
    o[a]=Math.ceil(c.measureText(a).width);
  });
  return o;
}"""

GEO = open("/home/claude/cj/measure/geo.js").read()

def pick(need):
    for w in LADDER:
        if w >= need: return w
    return LADDER[-1]

def make_groups(geo, nsent):
    """묶음 나누기.
    - 글 덩어리(.Paragraph / Reading 은 scriptBox)가 바뀌면 무조건 새 묶음
    - 화면을 넘치면 새 묶음. 단 **한 화자 발화(scriptBox) 중간에서는 끊지 않는다** ->
      끊을 자리를 그 발화의 첫 문장까지 앞당긴다(그러면 묶음이 비어버릴 때만 예외)
    """
    it0 = geo[0]['items']
    hasSpk = geo[0].get('hasSpk')
    g = [0]
    origin = [0] * len(geo)
    first = True
    j = 1
    while j < nsent:
        slack = BOXH - SAFE - (0 if first else SAFE)
        # 강제 경계는 .Paragraph 만. 문단(scriptBox)은 넘칠 때 '앞당기기'로 처리한다
        # (짧은 목록 항목마다 박스가 나뉘는 페이지에서 매 줄 스크롤이 튀는 것을 막기 위함)
        newblock = it0[j]['para'] != it0[j - 1]['para']
        overflow = any(geo[t]['items'][j]['bot'] - origin[t] > slack for t in range(len(geo)))
        if newblock or overflow:
            k = j
            if not newblock:                       # 발화 중간이면 발화 첫 문장까지 되돌림
                while k > 0 and it0[k - 1]['box'] == it0[j]['box']:
                    k -= 1
                if k <= g[-1]:
                    k = j                          # 발화 하나가 한 화면보다 큰 경우
            if k <= g[-1]:
                j += 1
                continue
            g.append(k)
            origin = [geo[t]['items'][k]['top'] for t in range(len(geo))]
            first = False
            j = k + 1
            continue
        j += 1
    return g


def scroll_values(geo, g, nsent):
    """탭별·그룹별 scrollTop. 묶음 전체가 여백을 두고 보이도록"""
    vals=[]
    for t,tt in enumerate(geo):
        ms=tt['scrollH']-tt['boxH']; row=[]
        for k,s0 in enumerate(g):
            e = g[k+1] if k+1<len(g) else nsent
            ft = tt['items'][s0]['top']
            lb = max(tt['items'][i]['bot'] for i in range(s0,e))
            lo = lb + SAFE - BOXH          # 아래쪽 여백 확보
            hi = ft - SAFE                 # 위쪽 여백 확보
            v  = ft - LEAD
            if v < lo: v = lo
            if v > hi: v = hi
            v  = max(0, min(int(round(v)), ms))
            row.append(None if k==0 else v)
        vals.append(row)
    return vals

NAME_S = {1:'firstShort',2:'secondShort',3:'thirdShort',4:'fourthShort',5:'fifthShort'}
NAME_M = {1:'firstMid',2:'secondMid',3:'thirdMid',4:'fourthMid',5:'fifthMid'}
NAME_L = {1:'firstLarge',2:'secondLarge',3:'thirdLarge',4:'fourthLarge',5:'fifthLarge'}
ALL    = {140:'short',250:'mid',300:'wide',350:'toLong',400:'toLong2'}
POS    = {140:NAME_S,250:NAME_M,300:NAME_L,350:NAME_L,400:NAME_L}
LASTN  = {140:'lastShort',250:'lastMid',300:'lastLarge',350:'lastToLong',400:'lastToLong2'}

def classes_for(px_list):
    n=len(px_list); cls=[]; rules=[]
    for px in sorted(set(px_list)):
        if px==200: continue
        pos=[k+1 for k,v in enumerate(px_list) if v==px]
        if len(pos)==n:
            nm=ALL.get(px,'w%d'%px); cls.append(nm); rules.append((nm,'all',px)); continue
        for p in pos:
            if p==n: nm=LASTN.get(px,'last%d'%px); sel='last'
            else: nm=POS.get(px,{}).get(p,'p%dw%d'%(p,px)); sel=p
            if px in (350,400) and p!=n: nm={1:'firstToLong',2:'secondToLong',3:'thirdToLong',4:'fourthToLong'}.get(p,'p%dw%d'%(p,px))
            cls.append(nm); rules.append((nm,sel,px))
    return cls, rules

async def main():
    OUT='/home/claude/cj/measure/out'; os.makedirs(OUT,exist_ok=True)
    try:
        GRP=json.load(open('/home/claude/cj/measure/spkgroup.json'))
    except Exception:
        GRP={}
    rep={}
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1280,'height':720})
        # 사전 측정: 화자칸 폭(그룹은 최댓값 공유)
        SPKW={}
        for name in sorted(os.listdir(SRC)):
            h0=open(os.path.join(SRC,name),encoding='utf-8').read()
            if '__SPKW__' not in h0: continue
            t0=os.path.join(REF,'__pre.html'); open(t0,'w',encoding='utf-8').write(
                h0.replace('</head>','<style>.tabContent{display:grid !important;}'+CALIB+'</style></head>'))
            await pg.goto('file://'+t0); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
            SPKW[name]=await pg.evaluate(SPKW_JS); os.remove(t0)
        for g in set(GRP.values()):
            mem=[n for n in SPKW if GRP.get(n)==g]
            if mem:
                mx=max(SPKW[n] for n in mem)
                for n in mem: SPKW[n]=mx
        for name in sorted(os.listdir(SRC)):
            path=os.path.join(SRC,name); html,items=parse(path)
            idxs=[i for i,it in enumerate(items) if it['ans']]
            W={i:[200]*len(items[i]['ans']) for i in idxs}
            # 1) 정답 글자 실측폭
            tmp=os.path.join(REF,'__b2.html')
            open(tmp,'w',encoding='utf-8').write(inject(html,items,W))
            await pg.goto('file://'+tmp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            tw=await pg.evaluate(MEASURE_TEXT)
            spkw=SPKW.get(name, await pg.evaluate(SPKW_JS))
            W={i:[pick(tw.get(w,0)+PAD+GAP) for w in items[i]['ans']] for i in idxs}
            # 2) 확정된 화자칸/입력칸 폭으로 다시 렌더 -> 기하
            spk_css=CALIB
            if '__SPKW__' in html:
                spk_css+='.scriptContainer .scriptBox .Speaker{width:%dpx !important;}'%(int(spkw)+8)
            open(tmp,'w',encoding='utf-8').write(inject(html,items,W,spk_css))
            await pg.goto('file://'+tmp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            geo=await pg.evaluate(GEO); os.remove(tmp)
            nsent=len(geo[0]['items'])
            g=make_groups(geo,nsent)
            vals=scroll_values(geo,g,nsent)
            # 3) 문장별 scrollTop
            per=[[i for i,it in enumerate(items) if it['tab']==t] for t in range(len(geo))]
            st={}
            for t in range(len(geo)):
                for k,s in enumerate(g):
                    e=g[k+1] if k+1<len(g) else nsent
                    for pos_ in range(s,min(e,len(per[t]))):
                        st[per[t][pos_]]=vals[t][k]
            # 4) HTML 재작성
            allr={}; out=[]; last=0
            for i,it in enumerate(items):
                s0,e0=it['span']; out.append(html[last:s0]); last=e0
                a=re.sub(r'\s*scrollTop="\d+"','',it['attrs'])
                cur=re.search(r'\bclass="([^"]*)"',a)
                base=cur.group(1).split() if cur else []
                newc=[]
                if i in W:
                    newc,rules=classes_for(W[i])
                    for r_ in rules: allr[r_]=True
                cl=[c for c in base if c not in newc]+newc
                a=re.sub(r'\s*\bclass="[^"]*"','',a)
                pre=''
                if st.get(i): pre+=' scrollTop="%d"'%st[i]
                if cl: pre+=' class="%s"'%' '.join(cl)
                out.append('<script-cont%s%s></script-cont>'%(pre,a))
            out.append(html[last:])
            nh=''.join(out)
            body=''
            for px in sorted({r[2] for r in allr}):
                sels=[]
                for (nm,sel,p2) in allr:
                    if p2!=px: continue
                    base='.iframePopup[data-use="dictation"] .%s .inputBox'%nm
                    sels.append(base if sel=='all' else (base+':last-of-type' if sel=='last'
                                else (base+':first-of-type' if sel==1 else base+':nth-of-type(%d)'%sel)))
                body+='\n'+',\n'.join('\t\t'+s for s in sorted(set(sels)))+' {\n\t\t\twidth: %dpx;\n\t\t}\n'%px
            m0=re.search(r'<style>(.*?)</style>', html, re.S)
            pre=m0.group(1) if m0 else ''
            cut=pre.find('.iframePopup[data-use="dictation"] .inputBox')
            pre=pre[:cut].rstrip() if cut>0 else ''
            if '__SPKW__' in pre:
                pre=pre.replace('__SPKW__', str(int(spkw)+8))
            head='\t<style>\n'
            if pre.strip(): head+=pre.lstrip('\n')+'\n\n'
            head+='\t\t.iframePopup[data-use="dictation"] .inputBox {\n\t\t\twidth: 200px;\n\t\t}\n'
            nh=re.sub(r'\t*<style>.*?</style>', lambda m: head+body+STYLE_TAIL, nh, count=1, flags=re.S)
            # comp-script-box 의 numberScrollTop = 그 박스 첫 문장의 scrollTop
            def _fix_num(m):
                tag=m.group(0)
                nxt=re.search(r'<script-cont\b([^>]*)>', nh[m.end():])
                v='0'
                if nxt:
                    s2=re.search(r'scrollTop="(\d+)"', nxt.group(1))
                    if s2: v=s2.group(1)
                return re.sub(r'numberScrollTop="\d+"', 'numberScrollTop="%s"'%v, tag)
            nh=re.sub(r'<comp-script-box\b[^>]*numberScrollTop="\d+"[^>]*>', _fix_num, nh)
            nh=nh.replace('\r\n','\n').replace('\n','\r\n')
            if nh.endswith('\r\n'): nh=nh[:-2]
            open(os.path.join(OUT,name),'w',encoding='utf-8',newline='').write(nh)
            rep[name]={'groups':g,'vals':vals,'widths':{str(k):v for k,v in W.items()},
                       'ans':{str(k):items[k]['ans'] for k in idxs}}
            print('%s 그룹 %s  scrollTop(탭별) %s'%(name,g,[[x for x in r if x is not None] for r in vals]))
        await b.close()
    json.dump(rep,open('/home/claude/cj/measure/build2.json','w'),ensure_ascii=False,indent=1)
asyncio.run(main())
