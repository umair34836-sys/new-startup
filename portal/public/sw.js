// Service worker: caches only static assets (CSS, JS, icons) and an offline page, to save requests on a
// 20-connection host. Pages, files and the API always go to the network, so clients never see stale order data.
const CACHE = 'portal-static-v7';
const ASSETS = ['assets/app.css?v=7', 'assets/app.js?v=7', 'assets/vendor/gsap-3.14.2.min.js', 'assets/icons/logo.png',
  'assets/icons/icon-192.png', 'assets/icons/logo-480.png', 'offline.html'];
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS.map((a) => new URL(a, self.registration.scope)))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  if (e.request.mode === 'navigate') {
    e.respondWith(fetch(e.request).catch(() => caches.match(new URL('offline.html', self.registration.scope))));
    return;
  }
  if (url.pathname.includes('/assets/')) {
    e.respondWith(caches.match(e.request).then((hit) => hit || fetch(e.request)));
  }
});
