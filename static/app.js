(function(){
  const original = (window.FLASHCARDS || []).slice(); // backend order
  const cards = original.slice(); // for quiz only

  // Shuffle quiz deck
  for (let j = cards.length - 1; j > 0; j--) {
    const k = Math.floor(Math.random() * (j + 1));
    [cards[j], cards[k]] = [cards[k], cards[j]];
  }

  const q = document.getElementById('question');
  const a = document.getElementById('answer');
  const law = document.getElementById('law');
  const pill = document.getElementById('lawPill');
  const revealBtn = document.getElementById('revealBtn');
  const nextBtn = document.getElementById('nextBtn');
  let i = 0;

  function show(idx){
    const c = cards[idx % cards.length];
    q.textContent = `What article covers: ${c.summary}?`;
    a.hidden = true;
    law.textContent = c.law;
    document.getElementById('article').textContent = c.article;
    document.getElementById('sections').textContent = c.sections;
    pill.textContent = c.law;
  }

  revealBtn.addEventListener('click', ()=>{ a.hidden = false; });
  nextBtn.addEventListener('click', ()=>{ i = (i+1)%cards.length; show(i); });
  if(cards.length){ show(i); }

  // Browse with grouped headers
  const list = document.getElementById('list');
  const search = document.getElementById('search');

  function appendHeader(text){
    const h = document.createElement('div');
    h.className = 'list-header';
    h.textContent = text;
    list.appendChild(h);
  }

  function appendItem(item){
    const el = document.createElement('div');
    el.className = 'list-item';
    el.innerHTML = `<div class="title">${item.law}: ${item.article}</div>
      <div class="muted">${item.sections}</div>
      <div>${item.summary}</div>`;
    el.addEventListener('click', ()=>{
      const idx = cards.findIndex(c => c.article === item.article && c.law === item.law);
      if(idx >= 0){ i = idx; show(i); window.scrollTo({top:0,behavior:'smooth'}); }
    });
    list.appendChild(el);
  }

  function renderList(items){
    list.innerHTML = '';
    const pl = items.filter(x => x.law === 'Penal Law');
    const cpl = items.filter(x => x.law === 'Criminal Procedure Law');

    if (pl.length){ appendHeader('Penal Law'); pl.forEach(appendItem); }
    if (cpl.length){ appendHeader('Criminal Procedure Law'); cpl.forEach(appendItem); }
  }

  renderList(original);

  search.addEventListener('input', (e)=>{
    const v = e.target.value.toLowerCase();
    const filtered = original.filter(c =>
      c.summary.toLowerCase().includes(v) ||
      c.article.toLowerCase().includes(v) ||
      c.sections.toLowerCase().includes(v) ||
      c.law.toLowerCase().includes(v)
    );
    renderList(filtered);
  });

  // Reset App: unregister SW + clear caches + reload
  async function resetApp(){
    try {
      if ('serviceWorker' in navigator) {
        const regs = await navigator.serviceWorker.getRegistrations();
        await Promise.all(regs.map(r => r.unregister()));
      }
      if (window.caches && caches.keys) {
        const keys = await caches.keys();
        await Promise.all(keys.map(k => caches.delete(k)));
      }
      setTimeout(() => location.reload(true), 250);
    } catch (e) {
      console.error('Reset failed', e);
      location.reload(true);
    }
  }
  document.getElementById('resetBtn')?.addEventListener('click', resetApp);

  // PWA install prompt
  let deferredPrompt = null;
  const installBtn = document.getElementById('installBtn');
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    installBtn.hidden = false;
  });
  installBtn?.addEventListener('click', async () => {
    installBtn.hidden = true;
    if (deferredPrompt) {
      deferredPrompt.prompt();
      await deferredPrompt.userChoice;
      deferredPrompt = null;
    }
  });
})();