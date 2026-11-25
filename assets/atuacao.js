(function(){
  // Arcos: acendem só quando a pessoa passa o mouse (CSS :hover) ou toca no celular.
  [].slice.call(document.querySelectorAll('.arco')).forEach(function(a, k, todos){
    a.addEventListener('touchstart', function(){ todos.forEach(function(o){ o.classList.toggle('ativo', o === a); }); }, {passive:true});
  });

  // Áreas: o botão "Ver detalhes" (ou um toque no cartão) abre a lista completa.
  [].slice.call(document.querySelectorAll('.area-x')).forEach(function(card){
    var bt = card.querySelector('.mais');
    function abrir(sim){
      card.classList.toggle('aberta', sim);
      bt.setAttribute('aria-expanded', sim);
      bt.textContent = sim ? 'Fechar detalhes' : 'Ver detalhes';
    }
    bt.addEventListener('click', function(e){ e.stopPropagation(); abrir(bt.getAttribute('aria-expanded') !== 'true'); });
    card.addEventListener('click', function(e){
      if (e.target.closest('a') || card.classList.contains('aberta')) return;
      if (window.getSelection && String(window.getSelection())) return;
      abrir(true);
    });
  });
  if (location.hash) {
    var alvo = document.getElementById(location.hash.slice(1));
    if (alvo && alvo.classList.contains('area-x')) alvo.querySelector('.mais').click();
  }
})();
