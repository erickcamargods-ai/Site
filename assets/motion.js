(function(){
  var root=document.documentElement;
  var calmo=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

  // modo noturno: segue o aparelho até a pessoa escolher; a escolha fica guardada
  var nav=document.querySelector('.site-header .nav');
  if(nav){
    var bt=document.createElement('button');bt.type='button';bt.className='tema';
    var escuro=function(){var a=root.getAttribute('data-theme');return a?a==='dark':!!(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches);};
    var pinta=function(){var e=escuro();bt.textContent=e?'Modo claro':'Modo noturno';bt.setAttribute('aria-pressed',e?'true':'false');};
    bt.addEventListener('click',function(){var n=escuro()?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('tema',n);}catch(e){}pinta();});
    pinta();nav.appendChild(bt);
  }

  // toda página nova começa do alto (menos ao voltar, que retoma onde a pessoa estava)
  var tipo='';try{tipo=performance.getEntriesByType('navigation')[0].type;}catch(e){}
  if(!location.hash&&tipo!=='back_forward'){
    try{scrollTo(0,0);var topo=document.querySelector('.site-header');if(topo&&topo.scrollIntoView)topo.scrollIntoView({block:'start'});}catch(e){}
  }

  // véu e arco da portada
  var p=document.createElement('div');p.className='portada';p.setAttribute('aria-hidden','true');
  p.appendChild(document.createElement('b'));document.body.appendChild(p);

  // blocos que assentam ao rolar
  var grupos=['.cards>*','.areas>*','.method>*','.prose>h2','.juridica','.fontes','.stack>*'];
  grupos.forEach(function(sel){
    document.querySelectorAll(sel).forEach(function(el){
      var i=Array.prototype.indexOf.call(el.parentNode.children,el);
      el.classList.add('rola');el.style.setProperty('--i',Math.min(i,4));
    });
  });
  var alvos=document.querySelectorAll('.rola,.section-head,.papel');
  if(!('IntersectionObserver' in window)||calmo){alvos.forEach(function(el){el.classList.add('visto')});}
  else{
    var io=new IntersectionObserver(function(es){es.forEach(function(e){
      if(e.isIntersecting){e.target.classList.add('visto');io.unobserve(e.target);}
    });},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    alvos.forEach(function(el){
      // o que já está na primeira tela fica pronto de saída
      if(el.getBoundingClientRect().top<innerHeight*.92&&!el.classList.contains('papel'))el.classList.add('visto');
      else io.observe(el);
    });
    // quem pulou direto para o fim da página não deixa blocos apagados para trás
    var t;addEventListener('scroll',function(){clearTimeout(t);t=setTimeout(function(){
      document.querySelectorAll('.rola:not(.visto),.section-head:not(.visto),.papel:not(.visto)').forEach(function(el){
        if(el.getBoundingClientRect().bottom<0){el.classList.add('visto');io.unobserve(el);}
      });},120);},{passive:true});
  }

  // saída pela portada
  if(calmo)return;
  document.addEventListener('click',function(ev){
    if(ev.defaultPrevented||ev.button||ev.metaKey||ev.ctrlKey||ev.shiftKey||ev.altKey)return;
    var a=ev.target.closest&&ev.target.closest('a[href]');
    if(!a||a.target||a.hasAttribute('download'))return;
    var u;try{u=new URL(a.href,location.href);}catch(e){return;}
    if(u.origin!==location.origin)return;
    if(u.pathname===location.pathname&&u.search===location.search)return; // âncora na mesma página
    ev.preventDefault();
    root.classList.add('saindo');
    setTimeout(function(){location.href=a.href;},540);
  });
  // ao voltar (botão ou gesto de arrastar), a página anterior reaparece limpa, sem o arco por cima
  var limpa=function(){root.classList.remove('saindo');};
  addEventListener('pageshow',limpa);addEventListener('pagehide',limpa);
})();
