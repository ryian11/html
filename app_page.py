# -*- coding: utf-8 -*-
"""화면. app.py 가 이 문자열 하나를 내보낸다."""

PAGE = r'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<title>HTML 생성기</title>
<style>
:root{--line:#dcdfe4;--bg:#f6f7f9;--ink:#1c1f23;--dim:#6b7280;--ok:#137a3d;--ng:#b3261e;--sel:#1a56c4}
*{box-sizing:border-box}
body{margin:0;font:14px/1.55 "맑은 고딕","Malgun Gothic",system-ui,sans-serif;color:var(--ink);background:var(--bg)}
header{display:flex;align-items:center;gap:14px;padding:10px 16px;background:#fff;border-bottom:1px solid var(--line)}
header b{font-size:15px}
select,input,button{font:inherit;padding:5px 9px;border:1px solid var(--line);border-radius:5px;background:#fff}
button{cursor:pointer}
button.go{background:var(--sel);color:#fff;border-color:var(--sel);font-weight:700;padding:6px 16px}
button:disabled{opacity:.5;cursor:default}
main{display:grid;grid-template-columns:330px 1fr;gap:0;height:calc(100vh - 47px)}
aside{border-right:1px solid var(--line);background:#fff;overflow:auto;padding:14px}
section{overflow:hidden;display:grid;grid-template-rows:auto 1fr auto}
h3{margin:18px 0 7px;font-size:12px;letter-spacing:.04em;color:var(--dim);text-transform:uppercase}
h3:first-child{margin-top:0}
.slot{margin-bottom:8px}
.slot label{display:block;font-size:12px;color:var(--dim);margin-bottom:2px}
.slot input{width:100%}
.slot .opt{color:#9aa0a6}
.units{display:flex;flex-wrap:wrap;gap:6px}
.units label{display:flex;align-items:center;gap:4px;border:1px solid var(--line);border-radius:5px;padding:3px 9px;background:#fff;cursor:pointer}
.units input{margin:0}
.steps{display:flex;flex-wrap:wrap;gap:8px;font-size:13px;color:var(--dim)}
.bar{display:flex;align-items:center;gap:10px;padding:8px 14px;background:#fff;border-bottom:1px solid var(--line);flex-wrap:wrap}
.files{display:flex;gap:6px;flex-wrap:wrap;max-height:74px;overflow:auto}
.files a{font-size:12px;padding:2px 8px;border:1px solid var(--line);border-radius:4px;background:#fff;text-decoration:none;color:var(--ink)}
.files a.on{background:var(--sel);color:#fff;border-color:var(--sel)}
iframe{width:100%;height:100%;border:0;background:#fff}
footer{border-top:1px solid var(--line);background:#fff;max-height:210px;overflow:auto}
pre{margin:0;padding:10px 14px;font:12px/1.5 Consolas,monospace;white-space:pre-wrap}
.ok{color:var(--ok);font-weight:700}.ng{color:var(--ng);font-weight:700}
.muted{color:var(--dim)}
.browse{margin-top:4px;font-size:12px;display:none;border:1px solid var(--line);border-radius:5px;max-height:170px;overflow:auto;background:#fafbfc}
.browse div{padding:3px 8px;cursor:pointer;border-bottom:1px solid #eef0f2}
.browse div:hover{background:#eaf0fb}
.browse .f{color:var(--dim);cursor:default}
.tabs{display:flex;gap:4px}
.tabs button{padding:4px 12px;font-size:13px}
.tabs button.on{background:var(--sel);color:#fff;border-color:var(--sel)}
#cfg{display:none;overflow:auto;background:#fff;padding:14px 18px}
#cfg h4{margin:0 0 6px;font-size:14px}
#cfg .pg{border:1px solid var(--line);border-radius:7px;padding:12px 14px;margin-bottom:14px}
#cfg .pg>b{font-size:14px}
#cfg .fld{margin:10px 0 0}
#cfg .fld>label{display:block;font-size:12px;color:var(--dim);margin-bottom:3px}
#cfg textarea{width:100%;font:12px/1.5 Consolas,monospace;border:1px solid var(--line);
  border-radius:5px;padding:6px 8px;resize:vertical}
#cfg table{width:100%;border-collapse:collapse;font-size:13px}
#cfg td{padding:2px 3px;vertical-align:top;border-bottom:1px solid #f0f1f3}
#cfg td.n{width:34px;color:var(--dim);font:12px Consolas,monospace;padding-top:8px}
#cfg td.lead{width:38px;color:#b06000;font:12px Consolas,monospace;padding-top:8px}
#cfg input.t{width:100%;border:1px solid transparent;border-radius:4px;padding:4px 6px;background:#fbfcfd}
#cfg input.t:focus{border-color:var(--sel);background:#fff}
#cfg input.t.over{background:#fff7e6;border-color:#e8c27a}
#cfg input.t.nokr{background:#fdeceb}
#cfg .sel{display:flex;gap:8px;flex-wrap:wrap;font-size:12px;color:var(--dim)}
#cfg .img{font:12px Consolas,monospace;color:var(--dim)}
#cfg .save{position:sticky;bottom:0;background:#fff;border-top:1px solid var(--line);
  padding:10px 0;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
</style></head><body>

<header>
  <b>HTML 생성기</b>
  <select id="recipe"></select>
  <span id="rname" class="muted"></span>
  <span style="flex:1"></span>
  <span id="state" class="muted"></span>
  <button onclick="quit()">끝내기</button>
</header>

<main>
<aside>
  <h3>① 자료</h3>
  <div id="slots"></div>
  <button onclick="saveSlots()">자료 경로 저장</button>

  <h3>② 프로토 (견본)</h3>
  <div id="pslots"></div>
  <div style="display:flex;gap:6px;margin:6px 0">
    <button style="font-size:12px;padding:3px 9px" onclick="loadProto()">견본 쪽 불러오기</button>
    <button style="font-size:12px;padding:3px 9px" onclick="allPages(1)">전체</button>
    <button style="font-size:12px;padding:3px 9px" onclick="allPages(0)">해제</button>
  </div>
  <div class="units" id="ppages"><span class="muted">프로토 단원을 적고 [견본 쪽 불러오기]</span></div>
  <div style="display:flex;gap:6px;margin-top:8px;flex-wrap:wrap">
    <button onclick="analyze()">프로토 분석</button>
    <button onclick="promote()">승격</button>
    <button onclick="compare()">코드와 대조</button>
  </div>
  <p class="muted" id="pinfo" style="font-size:12px;margin:7px 0 0"></p>
  <p class="muted" style="font-size:12px;margin:4px 0 0">
    분석 결과는 <code>rules/</code> 에만 쌓입니다. 생성 결과에는 아직 쓰이지 않습니다.</p>

  <h3>③ 단원</h3>
  <div class="units" id="units"></div>

  <h3>④ 쪽 <span style="text-transform:none;font-weight:400">(비우면 단원 전체)</span></h3>
  <div class="units" id="pages"><span class="muted">단원을 고르세요</span></div>
  <div style="display:flex;gap:6px;margin-top:6px">
    <button style="font-size:12px;padding:3px 9px" onclick="allUnitPages(1)">전체</button>
    <button style="font-size:12px;padding:3px 9px" onclick="allUnitPages(0)">해제</button>
  </div>

  <h3>⑤ 단계</h3>
  <div class="steps" id="steps"></div>
  <div style="margin-top:12px"><button class="go" id="run" onclick="run()">생성</button></div>
  <p class="muted" style="font-size:12px;margin:8px 0 0">
    산출 폴더에 바로 씁니다. 덮어쓰기 전에 <code>_backup/날짜시각</code> 으로 자동 저장됩니다.<br>
    쪽을 고르면 <b>그 쪽만</b> 씁니다. 고르지 않은 쪽 파일은 건드리지 않습니다.<br>
    들머리 쪽·전체듣기 팝업·예시답안은 단원 전체에서 나오므로 늘 함께 새로 씁니다.</p>

  <h3>되돌리기</h3>
  <select id="bk" style="width:100%"></select>
  <button style="margin-top:6px" onclick="restore()">이 백업으로 되돌리기</button>

  <h3>회귀 검사</h3>
  <div style="display:flex;gap:6px;flex-wrap:wrap">
    <button onclick="regress('check')">기준본과 견주기</button>
    <button onclick="regress('save')">지금 결과를 기준본으로</button>
  </div>
  <p class="muted" style="font-size:12px;margin:7px 0 0">
    임시 폴더에 다시 뽑아 바이트 단위로 견줍니다. 실기 폴더는 건드리지 않습니다.</p>
</aside>

<section>
  <div class="bar">
    <span class="tabs">
      <button id="tab_pv" class="on" onclick="tab('pv')">미리보기</button>
      <button id="tab_cfg" onclick="tab('cfg')">설정</button>
    </span>
    <span class="files" id="files"></span>
  </div>
  <iframe id="pv"></iframe>
  <div id="cfg"></div>
  <footer><pre id="log" class="muted">자료를 정하고 단원을 고른 뒤 [생성] 을 누르세요.</pre></footer>
</section>
</main>

<script>
let R=null, JOB=null, CUR={unit:null};
const $=s=>document.querySelector(s);

async function get(u){return (await fetch(u)).json()}
async function post(u,b){return (await fetch(u,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)})).json()}

async function boot(){
  const rs=await get('/api/recipes');
  $('#recipe').innerHTML=rs.map(r=>`<option value="${r.id}">${r.name}</option>`).join('');
  $('#recipe').onchange=()=>loadRecipe($('#recipe').value);
  if(rs.length) loadRecipe(rs[0].id);
  $('#steps').innerHTML=['extract','build','measure','verify']
    .map(s=>`<label><input type="checkbox" class="st" value="${s}" checked> ${
      ({extract:'추출',build:'생성',measure:'측정',verify:'검증'})[s]}</label>`).join('');
}

async function loadRecipe(id){
  R=await get('/api/recipe/'+id);
  $('#rname').textContent=R.name;
  const dat=R.slots.filter(s=>!s.key.startsWith('proto_'));
  const pro=R.slots.filter(s=>s.key.startsWith('proto_'));
  const slotHtml=s=>`
    <div class="slot">
      <label>${s.label}${s.optional?' <span class="opt">(선택)</span>':''}</label>
      <input id="sl_${s.key}" value="${s.value||''}" placeholder="${s.hint||(s.kind==='dir'?'폴더 경로':s.kind==='text'?'':'파일 경로')}"
             onfocus="this.nextElementSibling.style.display='none'">
      <div class="browse"></div>
      ${s.kind==='text'?'':`<button style="margin-top:3px;font-size:12px;padding:2px 8px"
              onclick="browse('${s.key}')">찾아보기</button>`}
    </div>`;
  $('#slots').innerHTML=dat.map(slotHtml).join('');
  $('#pslots').innerHTML=pro.map(slotHtml).join('');
  $('#units').innerHTML=R.units.map(u=>`<label><input type="checkbox" class="u" value="${u}" onchange="loadPages()"> ${u}단원</label>`).join('')
    || '<span class="muted">자료 경로를 먼저 정하세요</span>';
  $('#pinfo').textContent='';
  $('#pages').innerHTML='<span class="muted">단원을 고르세요</span>';
}

// ---------------------------------------------- 생성할 쪽
async function loadPages(){
  const us=[...document.querySelectorAll('.u:checked')].map(e=>e.value);
  if(us.length!==1){
    $('#pages').innerHTML='<span class="muted">'
      + (us.length?'단원을 하나만 골라야 쪽을 고를 수 있습니다':'단원을 고르세요')+'</span>';
    return;
  }
  const r=await get('/api/pages?recipe='+R.id+'&unit='+encodeURIComponent(us[0]));
  $('#pages').innerHTML=(r.pages||[]).map(p=>
      `<label><input type="checkbox" class="pg" value="${p}"> ${p}</label>`).join('')
    || '<span class="muted">먼저 한 번 생성해야 쪽이 보입니다</span>';
}
function allUnitPages(on){ document.querySelectorAll('.pg').forEach(e=>e.checked=!!on); }
function pickedPages(){ return [...document.querySelectorAll('.pg:checked')].map(e=>e.value); }

// ---------------------------------------------- 프로토
function pLesson(){ const e=$('#sl_proto_lesson'); return e?e.value.trim():''; }
function pOps(){ const e=$('#sl_proto_ops'); return e?e.value.trim():''; }

async function loadProto(){
  const n=pLesson();
  if(!n){ log('프로토 단원을 적어 주세요 (예: 6).'); return; }
  const r=await get('/api/proto?recipe='+R.id+'&lesson='+encodeURIComponent(n));
  if(r.error){ log('프로토: '+r.error); }
  const done=new Set(r.done||[]);
  $('#ppages').innerHTML=(r.pages||[]).map(p=>
      `<label><input type="checkbox" class="pp" value="${p}" ${
        done.size===0||done.has(p)?'checked':''}> ${p}</label>`).join('')
    || '<span class="muted">견본 쪽을 찾지 못했습니다</span>';
  const n2=Object.keys(r.items||{}).length;
  $('#pinfo').textContent = n2
    ? `이미 분석함 · 항목 ${n2}개 · ${r.made||''}` + (r.hasRules?' · rules.json 있음':'')
    : (r.ops? '아직 분석하지 않았습니다.' : '');
}
function allPages(on){ document.querySelectorAll('.pp').forEach(e=>e.checked=!!on); }

async function analyze(){
  const n=pLesson();
  if(!n){ log('프로토 단원을 적어 주세요.'); return; }
  const pages=[...document.querySelectorAll('.pp:checked')].map(e=>e.value);
  if(!pages.length){ log('견본으로 삼을 쪽을 고르세요. [견본 쪽 불러오기] 먼저.'); return; }
  $('#state').textContent='분석 중…';
  const r=await post('/api/analyze',{recipe:R.id,lesson:n,pages,ops:pOps()});
  JOB=r.job; pollTask(()=>loadProto());
}

async function promote(){
  const n=pLesson();
  if(!n){ log('프로토 단원을 적어 주세요.'); return; }
  if(!confirm(n+'단원 분석 결과를 rules.json 으로 옮깁니다.\n(생성 결과는 바뀌지 않습니다)')) return;
  $('#state').textContent='승격 중…';
  const r=await post('/api/promote',{recipe:R.id,lesson:n,fresh:true});
  JOB=r.job; pollTask(()=>loadProto());
}

async function compare(){
  const r=await get('/api/compare?recipe='+R.id);
  log(r.text||'');
}

async function regress(mode){
  const units=[...document.querySelectorAll('.u:checked')].map(e=>e.value);
  if(mode==='save' && !units.length){ log('기준본으로 삼을 단원을 고르세요.'); return; }
  $('#state').textContent='회귀 검사…';
  const r=await post('/api/regress',{recipe:R.id,units,mode});
  JOB=r.job; pollTask();
}

async function pollTask(after){
  const j=await get('/api/job?id='+JOB);
  log(j.log.join('\n'));
  if(j.state==='running'){ setTimeout(()=>pollTask(after),600); return; }
  $('#state').innerHTML = j.state==='done'
    ? '<span class="ok">끝</span>' : '<span class="ng">오류</span>';
  if(after) after();
}

async function browse(key){
  const inp=$('#sl_'+key), box=inp.nextElementSibling;
  const r=await get('/api/ls?path='+encodeURIComponent(inp.value||'.'));
  box.style.display='block';
  box.innerHTML=(r.up?`<div onclick="pick('${key}',${JSON.stringify(r.up).replace(/"/g,'&quot;')})">⬆ 상위</div>`:'')
    + r.dirs.map(d=>`<div onclick="pick('${key}',${JSON.stringify((r.path+'\\\\'+d)).replace(/"/g,'&quot;')})">📁 ${d}</div>`).join('')
    + r.files.map(f=>`<div class="f" onclick="setv('${key}',${JSON.stringify((r.path+'\\\\'+f)).replace(/"/g,'&quot;')})">📄 ${f}</div>`).join('');
}
function pick(k,p){ $('#sl_'+k).value=p; browse(k); }
function setv(k,p){ $('#sl_'+k).value=p; $('#sl_'+k).nextElementSibling.style.display='none'; }

async function saveSlots(){
  const slots={}; R.slots.forEach(s=>{const v=$('#sl_'+s.key).value.trim(); if(v) slots[s.key]=v;});
  await post('/api/settings',{recipe:R.id,slots});
  await loadRecipe(R.id);
  log('자료 경로를 저장했습니다.');
}

function log(s){ $('#log').textContent=s; }

async function run(){
  const units=[...document.querySelectorAll('.u:checked')].map(e=>e.value);
  if(!units.length){ log('단원을 고르세요.'); return; }
  const steps=[...document.querySelectorAll('.st:checked')].map(e=>e.value);
  const pages=pickedPages();
  if(pages.length && units.length>1){ log('쪽을 고를 때는 단원을 하나만 고르세요.'); return; }
  $('#run').disabled=true;
  $('#state').textContent = pages.length ? (pages.length+'쪽 생성…') : '도는 중…';
  const r=await post('/api/run',{recipe:R.id,units,steps,pages:pages.length?pages:null});
  JOB=r.job; poll();
}

async function poll(){
  const j=await get('/api/job?id='+JOB);
  log(j.log.join('\n'));
  if(j.state==='running'){ setTimeout(poll,600); return; }
  $('#run').disabled=false;
  $('#state').innerHTML = j.state==='done'
    ? (j.results.every(r=>r.ok)?'<span class="ok">끝</span>':'<span class="ng">확인 필요</span>')
    : '<span class="ng">오류</span>';
  const r=(j.results||[])[0];
  if(r){ CUR.unit=r.unit; showFiles(r); loadBackups(); loadPages(); CFG=null;
         if($('#cfg').style.display==='block') loadCfg(); }
}

function showFiles(r){
  const list=r.preview||[];
  const want=(r.pages&&r.pages.length)?(r.pages[0]+'.html'):null;
  const first=(want && list.indexOf(want)>=0) ? want : list[0];
  $('#files').innerHTML=list.map(p=>
    `<a href="#" class="${p===first?'on':''}" onclick="open_(this,'${p}');return false">${p}</a>`).join('');
  if(first) openPath(first);
}
function open_(a,p){ document.querySelectorAll('#files a').forEach(x=>x.classList.remove('on'));
  a.classList.add('on'); openPath(p); }
function openPath(p){ $('#pv').src='/files/'+R.id+'/'+CUR.unit+'/ops/'+p.split('/').map(encodeURIComponent).join('/'); }

async function loadBackups(){
  if(!CUR.unit) return;
  const r=await get('/api/backups?recipe='+R.id+'&unit='+CUR.unit);
  $('#bk').innerHTML=(r.list||[]).map(n=>`<option>${n}</option>`).join('')
    || '<option value="">(없음)</option>';
}
async function restore(){
  const stamp=$('#bk').value;
  if(!stamp || !CUR.unit){ log('되돌릴 백업이 없습니다.'); return; }
  const r=await post('/api/restore',{recipe:R.id,unit:CUR.unit,stamp});
  log('되돌림: '+CUR.unit+'단원 '+(r.n||0)+'개 — 미리보기를 새로고침하세요.');
}

// ---------------------------------------------- 설정 패널
let CFG=null;

function tab(which){
  const pv=which==='pv';
  $('#tab_pv').classList.toggle('on',pv); $('#tab_cfg').classList.toggle('on',!pv);
  $('#pv').style.display = pv?'block':'none';
  $('#cfg').style.display = pv?'none':'block';
  if(!pv && !CFG) loadCfg();
}

function cfgUnit(){
  if(CUR.unit) return CUR.unit;
  const u=document.querySelector('.u:checked');
  return u?u.value:'';
}

async function loadCfg(){
  const unit=cfgUnit();
  if(!unit){ $('#cfg').innerHTML='<p class="muted">단원을 고르세요.</p>'; return; }
  $('#cfg').innerHTML='<p class="muted">읽는 중…</p>';
  CFG=await get('/api/layout?recipe='+R.id+'&unit='+encodeURIComponent(unit));
  renderCfg();
}

function esc(v){ return (v==null?'':String(v)).replace(/&/g,'&amp;').replace(/</g,'&lt;')
  .replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

function renderCfg(){
  const d=CFG;
  if(d.error){ $('#cfg').innerHTML='<p class="ng">'+esc(d.error)+'</p>'; return; }
  const kinds=[['','(없음)'],['mic','마이크'],['speaker','말하는 이']];
  let h='<h4>'+esc(d.unit)+'단원 설정 <span class="muted" style="font-weight:400">'
      + esc(d.path.split(/[\\/]/).pop())+'</span></h4>';
  h+='<div class="fld"><label>말하는 이 이름 (단원 공통 · CSS 로 문단 앞에 붙습니다)</label>'
   + '<input class="t" id="c_speaker" style="max-width:280px" value="'+esc(d.speaker)+'"></div>';
  if((d.dropped||[]).length){
    h+='<div class="fld"><label>뺀 문장 — 지면에 그림으로 이미 있어 본문에서 지운 것</label><div class="sel">'
     + d.dropped.map(x=>`<label><input type="checkbox" class="undrop" value="${x.num}/${x.seq}"> ${x.num}/${x.seq} 되살리기</label>`).join('')
     + '</div></div>';
  }
  (d.pages||[]).forEach((pg,pi)=>{
    h+=`<div class="pg" data-i="${pi}"><b>${esc(pg.page)}</b> <span class="muted">${esc(pg.num)}쪽</span>`;
    h+=`<div class="fld"><label>문단 나눔 — 한 줄이 한 문단, 쉼표로 문장 번호</label>`
     + `<textarea rows="${Math.max(2,pg.paras.length)}" class="c_paras">${esc(pg.paras.join('\n'))}</textarea></div>`;
    h+='<div class="fld"><label>문단 첫머리</label><div class="sel">'
     + Object.keys(pg.prefix).map(sq=>`<label>${sq} <select class="c_prefix" data-seq="${sq}">`
        + kinds.map(k=>`<option value="${k[0]}" ${pg.prefix[sq]===k[0]?'selected':''}>${k[1]}</option>`).join('')
        + '</select></label>').join('') + '</div></div>';
    h+='<div class="fld"><label>문장 — 왼쪽은 지면 글자, 오른쪽은 해석. 고친 칸만 저장됩니다</label><table>'
     + pg.sents.map(sn=>`<tr data-seq="${sn.seq}">`
        + `<td class="n">${sn.seq}</td><td class="lead">${esc(sn.lead)}</td>`
        + `<td><input class="t c_en${sn.over?' over':''}" value="${esc(sn.en)}"></td>`
        + `<td><input class="t c_kr${sn.kr==='해석x'?' nokr':''}" value="${esc(sn.kr)}"></td></tr>`).join('')
     + '</table></div>';
    h+=`<div class="fld"><label>쪽 CSS — 문단 위치·너비·여백 (margin-top · width · margin-left)</label>`
     + `<textarea rows="${Math.min(16,Math.max(4,(pg.css||'').split('\n').length))}" class="c_css">${esc(pg.css)}</textarea></div>`;
    const im=Object.keys(pg.img||{}).map(k=>k+' '+pg.img[k].join('×')).join('   ');
    if(im) h+='<div class="fld"><label>이미지 크기 (잰 값 · 읽기 전용)</label><div class="img">'+esc(im)+'</div></div>';
    h+=`<div style="margin-top:10px"><button onclick="regen(['${pg.page}'])">이 쪽만 재생성</button></div>`;
    h+='</div>';
  });
  h+='<div class="save"><button class="go" onclick="saveCfg()">설정 저장</button>'
   + '<button onclick="loadCfg()">되읽기</button>'
   + '<button onclick="regen(null)">단원 전체 재생성</button>'
   + '<span class="muted" style="font-size:12px">저장은 layout 파일에만 씁니다. '
   + '재생성해야 HTML 에 반영됩니다.</span></div>';
  $('#cfg').innerHTML=h;
}

function cfgBody(){
  const d=CFG, pages=[];
  document.querySelectorAll('#cfg .pg').forEach(el=>{
    const pg=d.pages[+el.dataset.i], prefix={};
    el.querySelectorAll('.c_prefix').forEach(sl=>prefix[sl.dataset.seq]=sl.value);
    const sents=[];
    el.querySelectorAll('tr[data-seq]').forEach(tr=>{
      const seq=tr.dataset.seq, was=pg.sents.find(x=>x.seq===seq);
      const en=tr.querySelector('.c_en').value, kr=tr.querySelector('.c_kr').value;
      sents.push({seq, en, kr, over: was.over || en!==was.en});
    });
    pages.push({num:pg.num, page:pg.page, prefix, sents,
      paras: el.querySelector('.c_paras').value.split('\n').filter(x=>x.trim()),
      css: el.querySelector('.c_css').value});
  });
  return {unit:d.unit, speaker:$('#c_speaker').value, pages,
    undrop:[...document.querySelectorAll('.undrop:checked')].map(e=>e.value)};
}

async function saveCfg(){
  const r=await post('/api/layout', cfgBody());
  log(r.changed ? ('설정을 저장했습니다 — '+r.path+'\n백업: '+(r.backup||'없음')
                   +'\n\n[이 쪽만 재생성] 을 눌러야 HTML 에 반영됩니다.')
                : '바뀐 것이 없어 그대로 두었습니다.');
  CFG=null; loadCfg();
}

async function regen(pages){
  const unit=CFG?CFG.unit:cfgUnit();
  if(!unit){ log('단원을 고르세요.'); return; }
  const steps=[...document.querySelectorAll('.st:checked')].map(e=>e.value);
  $('#state').textContent='재생성…';
  const r=await post('/api/regen',{recipe:R.id,unit,pages,steps});
  JOB=r.job; CUR.unit=unit;
  pollTask(()=>{ if(pages&&pages.length) openPath(pages[0]+'.html'); loadBackups(); });
}

async function quit(){
  if(!confirm('생성기를 끝낼까요?')) return;
  try{ await post('/api/quit',{}); }catch(e){}
  document.body.innerHTML='<p style="padding:40px;font-size:15px">끝났습니다. 이 창을 닫으세요.</p>';
}

boot();
</script>
</body></html>
'''
