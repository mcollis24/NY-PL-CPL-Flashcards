const CACHE='ny-law-cards-v1';const ASSETS=['/','/static/style.css','/static/app.js','/static/manifest.json'];
self.addEventListener('install',evt=>{evt.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)))});
self.addEventListener('activate',evt=>{evt.waitUntil(self.clients.claim())});
self.addEventListener('fetch',evt=>{evt.respondWith(caches.match(evt.request).then(r=>r||fetch(evt.request)))})