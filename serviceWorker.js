const CACHE = 'marcos-lab-v2';
const CORE = [
  '/', '/index.html',
  '/assets/site.css', '/assets/site.js',
  '/manifest.json'
];
// Cache your app pages so they work offline from the hub
const APPS = [
  '/apps/car_loan_calculator.html',
  '/apps/mortgage_calculator.html',
  '/apps/round_robin.html'
];
const ASSETS = [...CORE, ...APPS];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.map(k => (k === CACHE ? null : caches.delete(k)))))
  );
});

// Navigation requests → serve cached hub (index.html) if offline
self.addEventListener('fetch', (e) => {
  const req = e.request;

  // If it's a navigation request, try network then fallback to cached index
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).catch(() => caches.match('/index.html'))
    );
    return;
  }

  // For other GETs, cache-first
  if (req.method === 'GET') {
    e.respondWith(
      caches.match(req).then(cached => cached ||
        fetch(req).then(res => {
          if (res && res.status === 200 && res.type === 'basic') {
            const clone = res.clone();
            caches.open(CACHE).then(c => c.put(req, clone));
          }
          return res;
        })
      )
    );
  }
});
