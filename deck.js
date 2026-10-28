var FAVON='<i class="ph-fill ph-heart" aria-hidden="true"></i> В избранном',FAVOFF='<i class="ph ph-heart" aria-hidden="true"></i> В избранное';

var LN={'死亡率':'L','时间':'T','金钱':'M','自由':'F'},LR={'死亡率':'Жизнь','时间':'Время','金钱':'Деньги','自由':'Свобода'};
var MN={'0':'Бесплатно','少':'Недорого','多':'Дорого'},TN={'少':'Быстро','中':'Часы','多':'Каждый день'},WN={'否':'Без усилий воли','些':'Немного воли','是':'Много воли'},BN={'大':'большая','中':'средняя','小':'малая'};
// card: 0ch 1n 2title 3plain 4cost 5grade 6money 7time 8will 9lvl 10lens 11ratio 12dis
var C=window.CARDS,byId={};C.forEach(function(c,i){c.i=i;byId[c[0]+'-'+c[1]]=c});
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(x){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[x]})}
function inline(s){return esc(s).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/(https?:\/\/[^\s<>&]+?)(?=[\s<>]|&lt;|&gt;|$|[;,)]\s)/g,function(u){return '<a href="'+u+'" target="_blank" rel="noopener">'+u+'</a>'})}
function para(s){return String(s||'').split(/\n+/).filter(Boolean).map(function(p){return '<p>'+inline(p)+'</p>'}).join('')}
// favorites
var KEY='vygodnee-fav',favs=[];
try{favs=JSON.parse(localStorage.getItem(KEY)||'[]').filter(function(k){return byId[k]})}catch(e){favs=[]}
function saveFavs(){try{localStorage.setItem(KEY,JSON.stringify(favs))}catch(e){}document.getElementById('favn').textContent=favs.length}
function isFav(k){return favs.indexOf(k)>=0}
function toast(t){var e=document.getElementById('toast');e.textContent=t;e.classList.add('on');clearTimeout(toast.t);toast.t=setTimeout(function(){e.classList.remove('on')},1600)}
// details lazy
function loadDetail(c){return new Promise(function(ok){var ch=c[0];function get(){var d=window.D&&window.D[ch];var it=d&&d.items.filter(function(x){return x[0]===c[1]})[0];ok(it)}
  if(window.D&&window.D[ch])return get();var s=document.createElement('script');s.src='data/ch'+String(ch).padStart(2,'0')+'.js';s.onload=get;s.onerror=function(){ok(null)};document.head.appendChild(s)})}
function cardEl(c){
  var k=c[0]+'-'+c[1],el=document.createElement('article');el.className='card deal';el.dataset.k=k;
  var tg=['<span class="tag '+(LN[c[10]]||'')+'">'+(LR[c[10]]||'')+'</span>',(c[5]==='РФ'?'<span class="tag ru">Адаптировано для РФ</span>':'<span class="tag">Доказательность '+c[5]+'</span>')];
  if(c[11]==='极高')tg.push('<span class="tag top">Очень выгодно</span>');else if(c[11]==='高')tg.push('<span class="tag">Выгодно</span>');
  if(c[9])tg.push('<span class="tag">Польза: '+BN[c[9]]+'</span>');if(c[12])tg.push('<span class="tag warn">Спорное</span>');
  var lab=[MN[c[6]],TN[c[7]],WN[c[8]]].filter(Boolean).join(' · ');
  el.innerHTML='<div class="chap">Раздел '+c[0]+' · '+esc(CHN[c[0]])+' · совет '+c[1]+'</div><h2>'+esc(c[2])+'</h2><div class="plain">'+para(c[3])+'</div>'+
   '<p class="cost"><b>'+esc(lab)+'.</b> '+esc(c[4])+'</p><div class="tags">'+tg.join('')+'</div>'+
   '<div class="acts"><button class="fav" aria-pressed="'+isFav(k)+'">'+(isFav(k)?FAVON:FAVOFF)+'</button><button class="fav share"><i class="ph ph-link" aria-hidden="true"></i> Ссылка</button></div>'+
   '<details class="more"><summary>Подробнее: выгода, примечание, источники</summary><div class="mb"><p>Загрузка…</p></div></details>';
  el.querySelector('.more').addEventListener('toggle',function(e){var d=e.target;if(!d.open||d.dataset.l)return;d.dataset.l=1;
    loadDetail(c).then(function(it){d.querySelector('.mb').innerHTML=it?'<h5>Выгода</h5>'+para(it[4])+(it[5]?'<h5>Примечание</h5>'+para(it[5]):'')+(it[6]?'<h5>Источники</h5>'+para(it[6]):''):'<p>Не удалось загрузить подробности.</p>'})});
  return el}
document.addEventListener('click',function(e){
  var f=e.target.closest('.fav:not(.share)');
  if(f){var k=f.closest('.card').dataset.k,i=favs.indexOf(k);if(i>=0)favs.splice(i,1);else favs.push(k);saveFavs();
    document.querySelectorAll('.card[data-k="'+k+'"] .fav:not(.share)').forEach(function(b){var on=isFav(k);b.setAttribute('aria-pressed',on);b.innerHTML=on?FAVON:FAVOFF});
    toast(isFav(k)?'Добавлено в избранное':'Убрано из избранного');if(!document.getElementById('favs').hidden)renderFavs();return}
  var s=e.target.closest('.share');
  if(s){var k2=s.closest('.card').dataset.k,u=location.href.split('#')[0]+'#c'+k2;
    (navigator.clipboard&&navigator.clipboard.writeText?navigator.clipboard.writeText(u):Promise.reject()).then(function(){toast('Ссылка скопирована')},function(){toast(u)})}
});
// deck
var res='all',freeOnly=false,queue=[],seen=[],hist=[],pos=-1;
function pool(){return C.filter(function(c){return (res==='all'||c[10]===res)&&(!freeOnly||(c[6]==='0'&&c[7]==='少'&&c[8]==='否'))})}
function shuffleDeck(){queue=pool().map(function(c){return c.i});for(var i=queue.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=queue[i];queue[i]=queue[j];queue[j]=t}hist=[];pos=-1;upd();document.getElementById('out').innerHTML='';document.getElementById('pile').hidden=false}
function upd(){document.getElementById('left').textContent='В колоде: '+queue.length+' из '+pool().length;document.getElementById('prev').disabled=pos<=0}
function show(arr){var out=document.getElementById('out');document.getElementById('pile').hidden=true;out.innerHTML='';arr.forEach(function(c){out.appendChild(cardEl(c))});
  var first=out.firstChild;if(first&&first.scrollIntoView)first.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'center'})}
function take(n){var r=[];for(var i=0;i<n;i++){if(!queue.length)break;r.push(C[queue.shift()])}return r}
function draw(n){if(!queue.length){var p=pool();if(!p.length){toast('Нет карт по фильтру');return}shuffleDeck();toast('Колода закончилась — перемешал заново')}
  var cards=take(n);hist.length=pos+1;hist.push(cards);pos=hist.length-1;upd();show(cards);try{history.replaceState(null,'',cards.length===1?'#c'+cards[0][0]+'-'+cards[0][1]:location.pathname)}catch(x){}}
document.getElementById('draw').onclick=function(){draw(1)};
document.getElementById('pile').onclick=function(){draw(1)};
document.getElementById('three').onclick=function(){draw(3)};
document.getElementById('prev').onclick=function(){if(pos>0){pos--;upd();show(hist[pos])}};
document.getElementById('shuffle').onclick=function(){shuffleDeck();toast('Колода перемешана')};
document.querySelectorAll('.chip[data-r]').forEach(function(b){b.onclick=function(){res=b.dataset.r;document.querySelectorAll('.chip[data-r]').forEach(function(o){o.setAttribute('aria-pressed',o===b)});shuffleDeck()}});
document.getElementById('free').onclick=function(){freeOnly=!freeOnly;this.setAttribute('aria-pressed',freeOnly);shuffleDeck()};
// favorites view
function renderFavs(){var box=document.getElementById('favlist');box.innerHTML='';
  if(!favs.length){box.innerHTML='<div class="empty">Пока пусто. Вытяните карту и нажмите «В избранное».</div>';return}
  favs.forEach(function(k){box.appendChild(cardEl(byId[k]))})}
document.getElementById('copy').onclick=function(){if(!favs.length){toast('Список пуст');return}
  var txt=favs.map(function(k){var c=byId[k];return c[0]+'.'+c[1]+' '+c[2]+'\n'+c[3]}).join('\n\n');
  (navigator.clipboard&&navigator.clipboard.writeText?navigator.clipboard.writeText(txt):Promise.reject()).then(function(){toast('Список скопирован')},function(){toast('Не удалось скопировать')})};
document.getElementById('clear').onclick=function(){var b=this;if(b.dataset.s){favs=[];saveFavs();renderFavs();b.textContent='Очистить';delete b.dataset.s;toast('Избранное очищено');return}b.dataset.s=1;b.textContent='Точно очистить?';setTimeout(function(){b.textContent='Очистить';delete b.dataset.s},3000)};
function tab(f){document.getElementById('deck').hidden=f;document.getElementById('favs').hidden=!f;
  document.getElementById('t-deck').setAttribute('aria-selected',!f);document.getElementById('t-fav').setAttribute('aria-selected',f);if(f)renderFavs()}
document.getElementById('t-deck').onclick=function(){tab(false)};document.getElementById('t-fav').onclick=function(){tab(true)};
saveFavs();shuffleDeck();
var m=location.hash.match(/^#c(\d+-\d+)$/);if(m&&byId[m[1]]){var c0=byId[m[1]];queue=queue.filter(function(i){return i!==c0.i});hist=[[c0]];pos=0;upd();show([c0])}
