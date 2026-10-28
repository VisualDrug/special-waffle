(function(){
  var root=document.documentElement;
  root.classList.add('js');
  // theme
  var btn=document.getElementById('theme');
  function cur(){var t=root.getAttribute('data-theme');if(t)return t;return matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}
  function icon(){if(btn)btn.innerHTML='<i class="ph '+(cur()==='dark'?'ph-sun':'ph-moon')+'" aria-hidden="true"></i>'}
  icon();
  if(btn)btn.addEventListener('click',function(){var n=cur()==='dark'?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}icon()});
  // mobile menu
  var b=document.getElementById('burger'),m=document.getElementById('mmenu');
  if(b&&m){
    var links=m.querySelectorAll('a');
    links.forEach(function(a,i){a.style.transitionDelay=(Math.min(i*60,400))+'ms'});
    function set(o){b.setAttribute('aria-expanded',o);m.classList.toggle('open',o);m.setAttribute('aria-hidden',!o);document.body.style.overflow=o?'hidden':'';
      links.forEach(function(a){a.tabIndex=o?0:-1});if(!o)links.forEach(function(a){a.style.transitionDelay='0ms'});else links.forEach(function(a,i){a.style.transitionDelay=(Math.min(i*60,400))+'ms'})}
    set(false);
    b.addEventListener('click',function(){set(b.getAttribute('aria-expanded')!=='true')});
    links.forEach(function(a){a.addEventListener('click',function(){set(false)})});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')set(false)});
  }
  // reveals (once)
  var rv=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:0.12});
    rv.forEach(function(el){io.observe(el)});
  }else rv.forEach(function(el){el.classList.add('in')});
  // tagline: words wake up one by one
  var tg=document.querySelector('[data-tagline]');
  if(tg){
    var words=tg.textContent.trim().split(/\s+/);tg.setAttribute('aria-label',tg.textContent.trim());
    tg.innerHTML=words.map(function(w){return '<span class="w" aria-hidden="true">'+w+'</span>'}).join(' ');
    var ws=tg.querySelectorAll('.w');
    if('IntersectionObserver' in window){
      var wo=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');wo.unobserve(e.target)}})},{rootMargin:'0px 0px -35% 0px',threshold:0});
      ws.forEach(function(w){wo.observe(w)});
    }else ws.forEach(function(w){w.classList.add('on')});
  }
})();
