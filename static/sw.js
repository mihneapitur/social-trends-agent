const CACHE_NAME = 'trendagent-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/style.css?v=4',
  '/script.js?v=4',
  '/assets/fb_profile.png',
  '/assets/ig_profile.png',
  '/assets/rd_profile.svg',
  '/assets/icon-192.png',
  '/assets/icon-512.png'
];

// Install Event - cache core files
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[Service Worker] Caching files');
      // Using map to prevent installation failure if some files aren't immediately found
      return Promise.allSettled(
        ASSETS.map(url => cache.add(url).catch(err => console.log('Failed to cache:', url, err)))
      );
    })
  );
  self.skipWaiting();
});

// Activate Event - clear old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            console.log('[Service Worker] Clearing old cache', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch Event - cache falling back to network or network falling back to cache
self.addEventListener('fetch', e => {
  // Only handle GET requests and skip API calls
  if (e.request.method !== 'GET' || e.request.url.includes('/api/')) {
    return;
  }

  e.respondWith(
    fetch(e.request)
      .then(res => {
        // Update cache with fresh version
        const resClone = res.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(e.request, resClone);
        });
        return res;
      })
      .catch(() => {
        // Fallback to cache if offline
        return caches.match(e.request);
      })
  );
});
