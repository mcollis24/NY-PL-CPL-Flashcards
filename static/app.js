(function(){
  const QUIZ_SETS = window.QUIZ_SETS || {};
  const BROWSE = (window.BROWSE || []).slice();

  const q = document.getElementById('question');
  const a = document.getElementById('answer');
  const law = document.getElementById('law');
  const pill = document.getElementById('lawPill');
  const revealBtn = document.getElementById('revealBtn');
  const nextBtn = document.getElementById('nextBtn');
  const reshuffleBtn = document.getElementById('reshuffleBtn');
  const tPL = document.getElementById('tgl-pl');
  const tCPL = document.getElementById('tgl-cpl');
  const tECL = document.getElementById('tgl-ecl');

  let deck = [];
  let i = 0;

  function rebuildDeck(){
    deck = [];
    if (tPL.checked) deck = deck.concat(QUIZ_SETS['Penal Law'] || []);
    if (tCPL.checked) deck = deck.concat(QUIZ_SETS['Criminal Procedure Law'] || []);
    if (tECL.checked) deck = deck.concat(QUIZ_SETS['Environmental Conservation Law'] || []);
    for (let j = deck.length - 1; j > 0; j--) {
      const k = Math.floor(Math.random() * (j + 1));
      [deck[j], deck[k]] = [deck[k], deck[j]];
    }
  }

  function show(idx){
    if (!deck.length) {
      q.textContent = 'No sets selected — toggle some above, then press Apply.';
      a.hidden = true;
      return;
    }
    const c = deck[idx % deck.length];
    q.textContent = `What article covers: ${c.summary}?`;
    a.hidden = true;
    law.textContent = c.law;
    document.getElementById('article').textContent = c.article;
    document.getElementById('sections').textContent = c.sections;
    pill.textContent = c.law;
  }

  revealBtn.addEventListener('click', ()=>{ a.hidden = false; });
  nextBtn.addEventListener('click', ()=>{ i = (i+1)%deck.length; show(i); });
  reshuffleBtn.addEventListener('click', ()=>{ i = 0; rebuildDeck(); show(i); });

  rebuildDeck();
  show(i);

  // Browse (grouped headers)
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
      const enabled = (item.law === 'Penal Law' && tPL.checked) ||
                      (item.law === 'Criminal Procedure Law' && tCPL.checked) ||
                      (item.law === 'Environmental Conservation Law' && tECL.checked);
      if (!enabled) return;
      const idx = deck.findIndex(c => c.article === item.article && c.law === item.law);
      if (idx >= 0){ i = idx; show(i); window.scrollTo({top:0,behavior:'smooth'}); }
    });
    list.appendChild(el);
  }

  function renderList(items){
    list.innerHTML = '';
    const pl = items.filter(x => x.law === 'Penal Law');
    const cpl = items.filter(x => x.law === 'Criminal Procedure Law');
    const ecl = items.filter(x => x.law === 'Environmental Conservation Law');
    if (pl.length){ appendHeader('Penal Law'); pl.forEach(appendItem); }
    if (cpl.length){ appendHeader('Criminal Procedure Law'); cpl.forEach(appendItem); }
    if (ecl.length){ appendHeader('Environmental Conservation Law'); ecl.forEach(appendItem); }
  }

  renderList(BROWSE);

  search.addEventListener('input', (e)=>{
    const v = e.target.value.toLowerCase();
    const filtered = BROWSE.filter(c =>
      c.summary.toLowerCase().includes(v) ||
      c.article.toLowerCase().includes(v) ||
      c.sections.toLowerCase().includes(v) ||
      c.law.toLowerCase().includes(v)
    );
    renderList(filtered);
  });

  // Reset App
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