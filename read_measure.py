# -*- coding: utf-8 -*-
"""Reading 본문 페이지 측정기 — Playwright 로 실기 크롬에 띄워 재고 값 파일을 만든다.

  python read_measure.py 6

만드는 파일 (생성기 폴더):
  scrolls<N>.py    본문 페이지 scrollTop
  popscroll<N>.py  해석/전체듣기 팝업 scrollTop
  krlayout<N>.py   해석 줄 배치 (kr 안의 <span style='left:-N'>)

그리고 제목·소제목 이미지의 단어 상자 x 를 출력한다 (WORDBTN 에 손으로 넣는 값).

※ 반드시 read_gen.py 로 한 번 만든 뒤에 돌려야 한다. 영어 줄바꿈을 재기 때문이다.
※ 실기(Windows)에서 돌리면 컨테이너 headless 와의 오차 문제가 없다.

준비:  pip install playwright && playwright install chromium
"""
import os, sys, io, importlib
import read_paths as P
import read_gen

SAFE_BODY = 40      # 본문: 상단 고정 버튼(본문 전체 듣기)을 피하는 위아래 여유
SAFE_POP = 20       # 팝업: 위아래 여유
GAP_KR = 26         # 해석 조각 사이 여백


# ---------------------------------------------------------------- 브라우저 JS
JS_READY = """() => new Promise(r => {
  const ok = () => document.querySelectorAll('.js-languageTarget, .scriptTarget').length > 0;
  const t0 = Date.now();
  (function w(){ if (ok() || Date.now()-t0 > 8000) document.fonts.ready.then(()=>setTimeout(r,250));
                 else setTimeout(w,100); })();
})"""

JS_BODY_SCROLL = r"""(SAFE) => {
 const rc=document.querySelector('.readingCont'), sb=document.querySelector('.scrollBox');
 sb.scrollTop=0;
 const r0=rc.getBoundingClientRect();
 const k=rc.offsetWidth ? (r0.width/rc.offsetWidth) : 1;
 const T=[...rc.querySelectorAll('.js-readHide .js-languageTarget')].map(e=>{
   const r=e.getBoundingClientRect();
   return {m:(e.getAttribute('data-mp3')||'').split('/').pop().replace('.mp3',''),
           t:Math.round((r.top-r0.top)/k), b:Math.round((r.bottom-r0.top)/k)};});
 T.sort((a,b)=>a.t-b.t);
 const H=sb.clientHeight, MAX=sb.scrollHeight-H;
 const g=[]; let cur=[T[0]];
 for(let i=1;i<T.length;i++){
   const s=T[i], f=cur[0];
   // 첫 묶음은 scrollTop 을 안 넣으므로 화면이 0..H 다. 첫 문장 기준이 아니라 0 기준으로 잰다.
   const limit = (g.length===0) ? (H - SAFE) : (f.t + H - (SAFE+SAFE/2));
   if(s.b > limit){ g.push(cur); cur=[s]; } else cur.push(s);
 }
 g.push(cur);
 const out={};
 g.forEach((gr,i)=>{ if(i===0) return;
   const lo=gr[gr.length-1].b+SAFE-H, hi=gr[0].t-SAFE;
   let v=Math.max(lo, Math.min(hi, gr[0].t-SAFE));
   v=Math.max(0, Math.min(MAX, Math.round(v)));
   gr.forEach(s=>out[s.m]=v); });
 return {H, MAX, contH: rc.offsetHeight,
         groups: g.map(x=>x.map(y=>y.m).join('+')), v: out};
}"""

JS_POP_SCROLL = r"""(SAFE) => {
 const cont=document.querySelector('.scriptContainer'), sb=document.querySelector('.scrollBox');
 sb.scrollTop=0; const r0=cont.getBoundingClientRect();
 const T=[...document.querySelectorAll('.scriptTarget')].map(e=>{const r=e.getBoundingClientRect();
   return {m:(e.getAttribute('data-mp3')||'').split('/').pop().replace('.mp3',''),
           t:Math.round(r.top-r0.top), b:Math.round(r.bottom-r0.top)};});
 T.sort((a,b)=>a.t-b.t);
 const H=sb.clientHeight, MAX=sb.scrollHeight-H;
 const g=[]; let cur=[T[0]];
 for(let i=1;i<T.length;i++){const s=T[i], f=cur[0];const pad=g.length===0?SAFE:SAFE*2;
   if(s.b>f.t+H-pad){g.push(cur);cur=[s];}else cur.push(s);}
 g.push(cur);
 const out={};
 g.forEach((gr,i)=>{if(i===0)return;const lo=gr[gr.length-1].b+SAFE-H,hi=gr[0].t-SAFE;
   let v=Math.max(lo,Math.min(hi,gr[0].t-SAFE));v=Math.max(0,Math.min(MAX,Math.round(v)));
   gr.forEach(s=>out[s.m]=v);});
 return {H, MAX, v: out};
}"""

# 해석 줄 배치 — 문장별로 자기 영어 시작 x 아래에서 시작, 넘칠 때만 다음 줄 왼쪽으로
JS_KR = r"""([KOR, GAP]) => {
 const cont=document.querySelector('.scriptContainer');const r0=cont.getBoundingClientRect();
 const W=Math.round(r0.width);
 const boxes=[...document.querySelectorAll('.scriptBox')];
 const probe=document.createElement('div');const sample=document.querySelector('.kor');
 const cs=getComputedStyle(sample);
 probe.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;left:-9999px;top:0';
 ['font','fontFamily','fontSize','fontWeight','letterSpacing'].forEach(k=>probe.style[k]=cs[k]);
 document.body.appendChild(probe);
 const wOf=t=>{probe.textContent=t;return probe.getBoundingClientRect().width;};
 const out=[];let ks=0;const dbg=[];
 boxes.forEach((bx,bi)=>{
  const tgts=[...bx.querySelectorAll('.scriptTarget')];
  const frags=[];
  tgts.forEach((t,si)=>{
    const node=[...t.querySelectorAll('span')].map(s=>s.firstChild).filter(n=>n&&n.nodeType===3)[0]
       ||[...t.childNodes].filter(n=>n.nodeType===3)[0];
    if(!node)return;
    const rg=document.createRange();
    const push=(s,e,top,l)=>frags.push({si,top:Math.round(top-r0.top),L:Math.round(l-r0.left),txt:node.data.slice(s,e)});
    let ss=0,st=null,sl=null;
    for(let i=0;i<node.data.length;i++){rg.setStart(node,i);rg.setEnd(node,i+1);
      const rc=rg.getBoundingClientRect();if(rc.width===0&&rc.height===0)continue;
      const tp=Math.round(rc.top);
      if(st===null){st=tp;sl=rc.left;ss=i;}else if(tp!==st){push(ss,i,st,sl);st=tp;sl=rc.left;ss=i;}}
    if(st!==null)push(ss,node.data.length,st,sl);
  });
  const rows=[...new Set(frags.map(f=>f.top))].sort((a,b)=>a-b);
  const rowOf=t=>rows.indexOf(t);
  const startRow={},korX={},hasK={};
  tgts.forEach((t,si)=>{const f=frags.filter(x=>x.si===si)[0];if(f){startRow[si]=rowOf(f.top);korX[si]=f.L;}
    hasK[si]=!!(KOR[ks+si]||'').trim();});
  const fixed=rows.map(()=>[]);
  tgts.forEach((_,si)=>{if(hasK[si]&&startRow[si]!==undefined) fixed[startRow[si]].push(korX[si]);});
  fixed.forEach(a=>a.sort((x,y)=>x-y));
  const cursor=rows.map(()=>0);
  const leftLimit=rows.map((_,r)=>fixed[r].length?fixed[r][0]:W);
  const kr=new Array(tgts.length).fill('');
  const place=rows.map(()=>[]);
  tgts.forEach((_,si)=>{
    if(!hasK[si]) return;
    const ws=(KOR[ks+si]||'').trim().split(/\s+/);
    let i=0, lv=0; const chunks=[]; const xs=[]; let guard=0;
    while(i<ws.length && guard++<40){
      const r=startRow[si]+lv;
      if(r>=rows.length){ chunks[chunks.length-1]=(chunks[chunks.length-1]||'')+' '+ws.slice(i).join(' '); i=ws.length; break; }
      let x, avail;
      if(lv===0){ x=korX[si];
        const nxt=fixed[r].filter(v=>v>korX[si]);
        avail=(nxt.length?nxt[0]:W)-x-GAP;
      }else{ x=cursor[r]; avail=leftLimit[r]-x-GAP; }
      if(avail<60){ chunks.push(''); xs.push(x); lv++; continue; }
      let take=0,cand='';
      while(i+take<ws.length){
        const nx=(cand?cand+' ':'')+ws[i+take];
        if(wOf(nx)>avail){ if(take===0){cand=nx;take=1;} break; }
        cand=nx; take++;
      }
      chunks.push(cand); xs.push(x); i+=take;
      if(lv>0) cursor[r]=x+wOf(cand)+GAP;
      place[r].push({si,x,w:Math.round(wOf(cand)),t:cand});
      lv++;
    }
    let s='';
    for(let L=chunks.length-1;L>=1;L--){
      const left=(L===1? xs[L]-korX[si] : xs[L]-xs[L-1]);
      s="<span style='left:"+Math.round(left)+"px'>"+chunks[L]+s+"</span>";
    }
    kr[si]=chunks[0]+s;
  });
  kr.forEach(x=>out.push(x));
  const clash=[];
  place.forEach((ps,r)=>{const so=ps.slice().sort((a,b)=>a.x-b.x);
    for(let i=1;i<so.length;i++) if(so[i-1].x+so[i-1].w>so[i].x)
      clash.push('행'+r+' 문장'+so[i-1].si+'↔'+so[i].si+' '+Math.round(so[i-1].x+so[i-1].w-so[i].x)+'px 겹침');
    ps.forEach(p=>{if(p.x+p.w>W) clash.push('행'+r+' 문장'+p.si+' 오른쪽 '+Math.round(p.x+p.w-W)+'px 넘침');});});
  dbg.push({box:bi, clash,
    lines:rows.map((tp,r)=>'EN['+frags.filter(f=>f.top===tp).sort((a,b)=>a.L-b.L).map(f=>f.txt).join('')+']  KR: '
      +place[r].slice().sort((a,b)=>a.x-b.x).map(p=>'@'+p.x+'{'+p.t+'}').join(' '))});
  ks+=tgts.length;
 });
 probe.remove();
 return {W, out, dbg};
}"""

# 제목/소제목 이미지의 단어 상자 (열 잉크량으로 공백 구간 검출)
JS_TITLEWORDS = r"""([src, padLeft]) => new Promise(res=>{
 const im=new Image();
 im.onerror=()=>res(null);
 im.onload=()=>{
  const W=im.naturalWidth,H=im.naturalHeight;
  const c=document.createElement('canvas');c.width=W;c.height=H;
  const g=c.getContext('2d');g.drawImage(im,0,0);
  const d=g.getImageData(0,0,W,H).data;
  const ink=[];
  for(let x=0;x<W;x++){let n=0;
    for(let y=0;y<H;y++){const i=((y*W)+x)*4;
      const lum=d[i]*0.3+d[i+1]*0.59+d[i+2]*0.11;
      if(d[i+3]>60&&lum<140)n++;}
    ink.push(n);}
  const groups=[];let s=null,gap=0;
  for(let x=0;x<W;x++){ if(ink[x]>0){if(s===null)s=x;gap=0;}
    else if(s!==null){gap++;if(gap>14){groups.push([s,x-gap]);s=null;gap=0;}} }
  if(s!==null)groups.push([s,W-1]);
  res({w:W,h:H, groups:groups.map(([a,b])=>[Math.round(padLeft+a/2),Math.round(padLeft+b/2)])});
 };
 im.src=src;
})"""


# ---------------------------------------------------------------- 파일 쓰기
def _dump(path, header, body):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n' + header + '\n' + body)
    print('  쓰기:', os.path.basename(path))


def write_scrolls(n, data, gen_dir):
    lines = ['SCROLLS = {']
    for page in read_gen.ORDER:
        v = data.get(page, {})
        lines.append(" '%s': {" % page)
        items = sorted(v.items())
        for i in range(0, len(items), 3):
            lines.append('   ' + ' '.join("'%s': %d," % kv for kv in items[i:i + 3]))
        lines.append(' },')
    lines.append('}')
    _dump(os.path.join(gen_dir, 'scrolls%d.py' % n),
          '# read_measure.py 가 만든 값 — 직접 고치면 다음 측정 때 덮어쓴다.\n'
          '# 본문 scrollBox 기준, 위아래 여유 %dpx (상단 고정 버튼 회피).' % SAFE_BODY,
          '\n'.join(lines) + '\n')


def write_popscroll(n, kor1, allv, gen_dir):
    L = ['KOR1 = {']
    for page in read_gen.ORDER:
        v = kor1.get(page, {})
        L.append(" '%s': {" % page)
        items = sorted(v.items())
        for i in range(0, len(items), 3):
            L.append('   ' + ' '.join("'%s': %d," % kv for kv in items[i:i + 3]))
        L.append(' },')
    L.append('}')
    L.append('')
    L.append('ALL = {')
    items = sorted(allv.items())
    for i in range(0, len(items), 3):
        L.append(' ' + ' '.join("'%s': %d," % kv for kv in items[i:i + 3]))
    L.append('}')
    _dump(os.path.join(gen_dir, 'popscroll%d.py' % n),
          '# read_measure.py 가 만든 값 — 직접 고치면 다음 측정 때 덮어쓴다.\n'
          '# 팝업 scrollBox 기준, 위아래 여유 %dpx.' % SAFE_POP,
          '\n'.join(L) + '\n')


def write_krlayout(n, kr, gen_dir):
    L = ['KR = {']
    for page in read_gen.ORDER:
        L.append(" '%s': [" % page)
        for s in kr[page]:
            L.append('  %s,' % repr(s).replace('\\u', '\\u'))
        L.append(' ],')
    L.append('}')
    _dump(os.path.join(gen_dir, 'krlayout%d.py' % n),
          '# read_measure.py 가 만든 값 — 직접 고치면 다음 측정 때 덮어쓴다.\n'
          '# 문장별로 그 문장의 영어가 시작하는 x 아래에서 해석이 시작하고,\n'
          '# 그 줄에 다 안 들어갈 때만 <span style=\'left:-N\'> 로 다음 줄 왼쪽에 이어 붙인다.\n'
          '# (span 한 겹 = 100px 아래 줄)',
          '\n'.join(L) + '\n')


# ---------------------------------------------------------------- 본체
def measure(n, gen_dir=None, headless=True):
    gen_dir = gen_dir or os.path.dirname(os.path.abspath(__file__))
    read_gen.load_lesson(n)
    ops = P.ops(n)
    pages = read_gen.ORDER
    url = lambda rel: P.file_url(os.path.join(ops, rel))

    # 페이지별 해석 배열 (제목/소제목 포함, script-cont 순서)
    kor_of = {}
    for page in pages:
        p = read_gen.PAGES[page]
        arr = [p['title']['kr']]
        for kind, blk in p['blocks']:
            if kind == 'subtit':
                arr.append(blk['kr'])
            else:
                arr += [kr for _, _, kr in blk]
        kor_of[page] = arr

    from playwright.sync_api import sync_playwright
    warn = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=headless, args=['--allow-file-access-from-files'])
        pg = br.new_page(viewport={'width': 1280, 'height': 720})

        # 1) 본문 페이지 scrollTop + 제목 이미지 단어 상자
        print('[measure] 본문 페이지')
        scrolls = {}
        for page in pages:
            pg.goto(url(page + '.html'))
            pg.evaluate(JS_READY)
            r = pg.evaluate(JS_BODY_SCROLL, SAFE_BODY)
            scrolls[page] = r['v']
            print('  %s  쪽높이 %d  최대스크롤 %d  묶음 %s'
                  % (page, r['contH'], r['MAX'], ' / '.join(r['groups'])))
            # 제목·소제목 이미지 단어 상자
            for cls, img in _title_images(page):
                t = pg.evaluate(JS_TITLEWORDS, ['images/%s/%s' % (page, img), 40])
                if t:
                    g = t['groups']
                    print('    %-18s %dx%d  단어상자 x: %s' % (
                        img, t['w'], t['h'],
                        '  '.join('%d)%d~%d' % (i + 1, a, b) for i, (a, b) in enumerate(g))))
                    print('    %-18s → WORDBTN left 후보: %s' % (
                        '', '  '.join('%d)%d' % (i + 1, a - 15 - 40) for i, (a, _) in enumerate(g))))

        # 2) 해석 팝업 — 줄 배치 + scrollTop
        print('[measure] 해석 팝업')
        kr, popkor1 = {}, {}
        for page in pages:
            pg.goto(url('popup/%s_kor1.html' % page))
            pg.evaluate(JS_READY)
            r = pg.evaluate(JS_KR, [kor_of[page], GAP_KR])
            kr[page] = r['out']
            cl = [c for d in r['dbg'] for c in d['clash']]
            if cl:
                warn.append('%s_kor1: %s' % (page, '; '.join(cl)))
            s = pg.evaluate(JS_POP_SCROLL, SAFE_POP)
            popkor1[page] = s['v']
            print('  %s_kor1  폭 %d  묶음높이 %d  최대스크롤 %d  %s'
                  % (page, r['W'], s['H'], s['MAX'], '겹침/넘침 ' + str(len(cl)) if cl else 'OK'))

        # 3) 전체 듣기 팝업
        print('[measure] 전체 듣기 팝업')
        allpop = read_gen.all_popup()
        pg.goto(url('popup/%s.html' % allpop))
        pg.evaluate(JS_READY)
        korall = [x for page in pages for x in kor_of[page]]
        ra = pg.evaluate(JS_KR, [korall, GAP_KR])
        sa = pg.evaluate(JS_POP_SCROLL, SAFE_POP)
        cl = [c for d in ra['dbg'] for c in d['clash']]
        if cl:
            warn.append('%s: %s' % (allpop, '; '.join(cl)))
        flat = [x for page in pages for x in kr[page]]
        if ra['out'] != flat:
            diff = [i for i, (a, b) in enumerate(zip(ra['out'], flat)) if a != b]
            warn.append('%s 의 줄 배치가 _kor1 과 다름 (문장 %s) → 팝업 폭/줄바꿈 확인' % (allpop, diff))
        print('  %s  최대스크롤 %d  %s' % (allpop, sa['MAX'], '겹침/넘침 %d' % len(cl) if cl else 'OK'))

        br.close()

    write_scrolls(n, scrolls, gen_dir)
    write_popscroll(n, popkor1, sa['v'], gen_dir)
    write_krlayout(n, kr, gen_dir)

    for m in ('scrolls%d' % n, 'popscroll%d' % n, 'krlayout%d' % n):
        if m in sys.modules:
            importlib.reload(sys.modules[m])

    if warn:
        print('\n[!] 확인 필요')
        for w in warn:
            print('   -', w)
    else:
        print('\n[measure] 겹침·넘침 없음')
    return not warn


def _title_images(page):
    """그 쪽의 제목/소제목 클래스와 이미지 파일명"""
    p = read_gen.PAGES[page]
    fname = {'mainTitle': 'title', 'sTit01': 's_title01', 'sTit02': 's_title02',
             'sTit03': 's_title03', 'sTit04': 's_title04'}
    out = []
    cls = p['title']['cls'].split()[-1]
    out.append((cls, fname[cls] + '.png'))
    for kind, blk in p['blocks']:
        if kind == 'subtit':
            c = blk['cls'].split()[-1]
            out.append((c, fname[c] + '.png'))
    return out


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    sys.exit(0 if measure(n, headless='--show' not in sys.argv) else 1)
