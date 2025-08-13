
(function(){
  const cards = window.FLASHCARDS || [];
  let i = 0;

  function shuffle(arr){
    for (let j = arr.length - 1; j > 0; j--) {
      const k = Math.floor(Math.random() * (j + 1));
      [arr[j], arr[k]] = [arr[k], arr[j]];
    }
    return arr;
  }
  shuffle(cards);

  const q = document.getElementById('question');
  const a = document.getElementById('answer');
  const law = document.getElementById('law');
  const pill = document.getElementById('lawPill');

  function show(idx){
    const c = cards[idx % cards.length];
    q.textContent = `What article covers: ${c.summary}?`;
    a.hidden = true;
    law.textContent = c.law;
    document.getElementById('article').textContent = c.article;
    document.getElementById('sections').textContent = c.sections;
    pill.textContent = c.law;
  }

  document.getElementById('revealBtn').addEventListener('click', ()=>{ a.hidden = false; });
  document.getElementById('nextBtn').addEventListener('click', ()=>{ i = (i+1)%cards.length; show(i); });

  if(cards.length){ show(i); }

  const list = document.getElementById('list');
  const search = document.getElementById('search');
  function renderList(items){
    list.innerHTML = '';
    items.forEach(item => {
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
    });
  }
  renderList(cards);

  search.addEventListener('input', (e)=>{
    const v = e.target.value.toLowerCase();
    const filtered = cards.filter(c =>
      c.summary.toLowerCase().includes(v) ||
      c.article.toLowerCase().includes(v) ||
      c.sections.toLowerCase().includes(v) ||
      c.law.toLowerCase().includes(v)
    );
    renderList(filtered);
  });

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
