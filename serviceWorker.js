// serviceWorker.js
const CACHE = 'marcos-lab-v3';

// Core shell (hub + shared assets)
const CORE = [
  '/', '/index.html',
  '/assets/site.css', '/assets/site.js',
  '/manifest.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(CORE))
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(k => (k === CACHE ? null : caches.delete(k))))
    )
  );
});

// Helper: same-origin check
const sameOrigin = (url) => {
  try { return new URL(url).origin === self.location.origin; }
  catch { return false; }
};

self.addEventListener('fetch', (e) => {
  const req = e.request;

  // 1) Navigations → network first, fallback to cached hub when offline
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).catch(() => caches.match('/index.html'))
    );
    return;
  }

  // Only handle GETs from our own origin
  if (req.method !== 'GET' || !sameOrigin(req.url)) return;

  const url = new URL(req.url);

  // 2) Any /apps/* file → cache-first, then network; cache new apps on first visit
  if (url.pathname.startsWith('/apps/')) {
    e.respondWith(
      caches.match(req).then(cached => cached ||
        fetch(req).then(res => {
          if (res && res.ok) {
            const clone = res.clone();
            caches.open(CACHE).then(c => c.put(req, clone));
          }
          return res;
        })
      )
    );
    return;
  }

  // 3) Static assets (css/js) → cache-first
  if (url.pathname.startsWith('/assets/') || url.pathname.endsWith('.css') || url.pathname.endsWith('.js')) {
    e.respondWith(
      caches.match(req).then(cached => cached ||
        fetch(req).then(res => {
          if (res && res.ok) {
            const clone = res.clone();
            caches.open(CACHE).then(c => c.put(req, clone));
          }
          return res;
        })
      )
    );
    return;
  }

  // 4) Everything else → network, fallback to cache if available
  e.respondWith(
    fetch(req).then(res => {
      // opportunistic cache of same-origin GETs
      if (res && res.ok) {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(req, clone));
      }
      return res;
    }).catch(() => caches.match(req))
  );
});
