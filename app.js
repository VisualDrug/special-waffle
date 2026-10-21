var KEYS=Object.keys(CNT).map(Number);
var LN={'死亡率':'L','时间':'T','金钱':'M','自由':'F'}, LR={'死亡率':'Жизнь','时间':'Время','金钱':'Деньги','自由':'Свобода'};
var MN={'0':'Бесплатно','少':'Недорого','多':'Дорого'}, TN={'少':'Быстро','中':'Часы','多':'Каждый день'}, WN={'否':'Без усилий воли','些':'Немного воли','是':'Много воли'};
var BN={'大':'большая','中':'средняя','小':'малая'};
var st={lens:null,grade:null,top:0,free:0,dis:0,q:''}, loaded={}, filtering=false;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function inline(s){return esc(s).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/(https?:\/\/[^\s<>&]+?)(?=[\s<>]|&lt;|&gt;|$|[;,)]\s)/g,function(u){return '<a href="'+u+'" target="_blank" rel="noopener">'+u+'</a>'})}
function para(s){return String(s||'').split(/\n\s*\n|\n/).filter(Boolean).map(function(p){return '<p>'+inline(p)+'</p>'}).join('')}
function loadScript(src){return new Promise(function(ok,fail){var s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=fail;document.head.appendChild(s)})}
function loadCh(n){if(loaded[n])return loaded[n];var p=String(n).padStart(2,'0');return loaded[n]=loadScript('data/ch'+p+'.js').then(function(){var d=window.D[n];d.items.forEach(function(it){it.h=null});return d})}
function loadAll(){return Promise.all(KEYS.map(function(n){return loadCh(n)}))}
// map
var mapEl=document.getElementById('map');
CL.forEach(function(g){var tot=g[1].reduce(function(a,c){return a+CNT[c]},0);var d=document.createElement('div');d.className='grp';
  d.innerHTML='<h3>'+esc(g[0])+' <small>'+tot+' советов</small></h3><div class="chips">'+g[1].map(function(c){return '<button class="mchip" data-ch="'+c+'"><b>'+c+'</b>'+esc(CHN[c])+'</button>'}).join('')+'</div>';mapEl.appendChild(d)});
var chEl=document.getElementById('chapters'), secs={};
for(var c of KEYS){var d=document.createElement('details');d.className='ch';d.id='s'+c;d.dataset.ch=c;
  d.innerHTML='<summary><span class="cnum">'+c+'</span><span class="cname">'+esc(CHN[c])+'</span><span class="ccnt">'+CNT[c]+' сов.</span></summary><div class="body"><p class="note">Загрузка…</p></div>';chEl.appendChild(d);secs[c]=d}
function cardHTML(ch,it){
  var tg=['<span class="tag '+(LN[it[12]]||'')+'">'+(LR[it[12]]||'')+'</span>',(it[7]==='РФ'?'<span class="tag ru">Адаптировано для РФ</span>':'<span class="tag">Доказательность '+it[7]+'</span>')];
  if(it[13]==='极高')tg.push('<span class="tag top">Очень выгодно</span>');else if(it[13]==='高')tg.push('<span class="tag">Выгодно</span>');
  if(it[11])tg.push('<span class="tag">Польза: '+BN[it[11]]+'</span>');
  if(it[14])tg.push('<span class="tag warn">Спорное</span>');
  var lab=[MN[it[8]],TN[it[9]],WN[it[10]]].filter(Boolean).join(' · ');
  return '<article class="card" id="c'+ch+'-'+it[0]+'"><h4><span>'+ch+'.'+it[0]+'</span>'+esc(it[1])+'</h4><div class="plain">'+para(it[3])+'</div>'+
   '<p class="cost"><b>'+esc(lab)+'.</b> '+esc(it[2])+'</p><div class="tags">'+tg.join('')+'</div>'+
   '<details class="more"><summary>Подробнее: выгода, примечание, источники</summary><div class="mb"><h5>Выгода</h5>'+para(it[4])+(it[5]?'<h5>Примечание</h5>'+para(it[5]):'')+(it[6]?'<h5>Источники</h5>'+para(it[6]):'')+'</div></details></article>';
}
function match(it){
  if(st.lens&&it[12]!==st.lens)return false; if(st.grade&&it[7]!==st.grade)return false;
  if(st.top&&it[13]!=='极高')return false; if(st.free&&!(it[8]==='0'&&it[9]==='少'&&it[10]==='否'))return false; if(st.dis&&!it[14])return false;
  if(st.q){if(!it.h)it.h=(it[1]+' '+it[2]+' '+it[3]+' '+it[4]+' '+it[5]).toLowerCase(); if(it.h.indexOf(st.q)<0)return false}
  return true;
}
function fill(n){var d=secs[n];return loadCh(n).then(function(data){var arr=data.items.filter(match);
  d.querySelector('.ccnt').textContent=(filtering?arr.length+' из ':'')+data.items.length+' сов.';
  d.hidden=filtering&&!arr.length;
  d.querySelector('.body').innerHTML=(filtering?'':'<div class="intro">'+para(data.intro)+'</div>')+(arr.length?'<div class="list">'+arr.map(function(it){return cardHTML(n,it)}).join('')+'</div>':'<p class="note">Нет советов по фильтру.</p>');
  return arr.length})}
async function upd(){
  filtering=!!(st.lens||st.grade||st.top||st.free||st.dis||st.q);
  var cnt=document.getElementById('count');
  if(!filtering){cnt.textContent='Всего: 512 советов';for(var c of KEYS){secs[c].hidden=false;secs[c].open=false;secs[c].querySelector('.ccnt').textContent=CNT[c]+' сов.'}return}
  cnt.textContent='Ищу…';await loadAll();var tot=0;
  for(var c of KEYS){var k=await fill(c);tot+=k;if(k)secs[c].open=true}
  cnt.textContent='Найдено: '+tot+' из 512';
  var e=document.getElementById('emp');if(e)e.remove();if(!tot)chEl.insertAdjacentHTML('afterbegin','<div class="empty" id="emp">Ничего не найдено. Измените запрос или снимите фильтры.</div>');
}
chEl.addEventListener('toggle',function(e){var d=e.target;if(d.classList.contains('ch')&&d.open&&!d.dataset.f){d.dataset.f=1;fill(+d.dataset.ch)}},true);
document.addEventListener('click',function(e){
  var m=e.target.closest('.mchip');
  if(m){var n=+m.dataset.ch,d=secs[n];d.hidden=false;d.open=true;try{history.replaceState(null,'','#s'+n)}catch(x){}
    d.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});return}
  var c=e.target.closest('.chip[data-g]');
  if(c){var g=c.dataset.g,v=c.dataset.v,on=c.getAttribute('aria-pressed')==='true',flag=(g==='top'||g==='free'||g==='dis');
    document.querySelectorAll('.chip[data-g="'+g+'"]').forEach(function(o){o.setAttribute('aria-pressed','false')});
    if(!on)c.setAttribute('aria-pressed','true'); st[g]=on?(flag?0:null):(flag?1:v); resetF();upd();return}
  if(e.target.id==='reset'){st={lens:null,grade:null,top:0,free:0,dis:0,q:''};document.getElementById('q').value='';
    document.querySelectorAll('.chip[data-g]').forEach(function(o){o.setAttribute('aria-pressed','false')});resetF();upd()}
});
function resetF(){for(var c of KEYS)delete secs[c].dataset.f}
var qt;document.getElementById('q').addEventListener('input',function(e){clearTimeout(qt);var v=e.target.value.trim().toLowerCase();qt=setTimeout(function(){st.q=v;resetF();upd()},200)});
var h=location.hash.match(/^#s(\d+)$/);if(h&&secs[+h[1]])secs[+h[1]].open=true;
