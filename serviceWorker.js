const CACHE = 'marcos-lab-v1';
const ASSETS = [
  '/',                       // if you have an index
  '/assets/site.css',
  '/assets/site.js',
  '/manifest.json',
  '/car_loan_calculator.html',
  '/mortgage_calculator.html',
  '/round_robin.html'
];

// Install: cache core
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
});

// Activate: clean old caches
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.map(k => (k===CACHE?null:caches.delete(k)))))
  );
});

// Fetch: cache-first for assets/pages
self.addEventListener('fetch', (e) => {
  const req = e.request;
  e.respondWith(
    caches.match(req).then(cached => cached || fetch(req).then(res => {
      // Optionally cache new GET responses
      if (req.method === 'GET' && res.status === 200 && res.type === 'basic') {
        const resClone = res.clone();
        caches.open(CACHE).then(c => c.put(req, resClone));
      }
      return res;
    }).catch(() => cached))
  );
});
