const C='signspeak-v2',APP=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(APP)));self.skipWaiting()});
self.addEventListener('activate',e=>e.waitUntil(clients.claim()));
// cache-first; AI models + wasm are cached on first load so the app works offline later
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;
e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{
if(res&&(res.ok||res.type==='opaque')){const cp=res.clone();caches.open(C).then(c=>c.put(e.request,cp))}return res}).catch(()=>r)))});
