// serviceWorker.js
const CACHE = 'marcos-lab-v4';
const CORE = [
  '/', '/index.html',
  '/assets/site.css', '/assets/site.js',
  '/manifest.json',
  '/apps/apps.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    // Precache core + apps list
    await cache.addAll(CORE);
    // Precache each app href from apps.json (if available)
    try {
      const res = await fetch('/apps/apps.json', { cache: 'no-cache' });
      if (res.ok) {
        const apps = await res.json();
        const hrefs = apps.map(a => a.href).filter(Boolean);
        await cache.addAll(hrefs);
      }
    } catch (_) {
      // apps.json missing or offline during install — fine, apps will cache on first visit
    }
  })());
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(k => (k === CACHE ? null : caches.delete(k))))
    )
  );
});

// Helper: same-origin guard
const sameOrigin = (url) => {
  try { return new URL(url).origin === self.location.origin; }
  catch { return false; }
};

self.addEventListener('fetch', (e) => {
  const req = e.request;

  // Navigations → network first, fallback to cached hub if offline
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).catch(() => caches.match('/index.html'))
    );
    return;
  }

  if (req.method !== 'GET' || !sameOrigin(req.url)) return;

  const url = new URL(req.url);

  // Apps & assets → cache-first; fill cache on first visit
  if (
    url.pathname.startsWith('/apps/') ||
    url.pathname.startsWith('/assets/') ||
    url.pathname.endsWith('.css') ||
    url.pathname.endsWith('.js')
  ) {
    e.respondWith(
      caches.match(req).then(cached => cached ||
        fetch(req).then(res => {
          if (res && res.ok) caches.open(CACHE).then(c => c.put(req, res.clone()));
          return res;
        })
      )
    );
    return;
  }

  // Everything else → network with cache fallback
  e.respondWith(
    fetch(req).then(res => {
      if (res && res.ok) caches.open(CACHE).then(c => c.put(req, res.clone()));
      return res;
    }).catch(() => caches.match(req))
  );
});
