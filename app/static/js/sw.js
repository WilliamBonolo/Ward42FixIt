const CACHE_NAME = 'ward42-cache-v2';

// We only cache local files to prevent the installation from failing if the internet drops
const urlsToCache = [
    '/',
    '/offline',
    '/static/js/main.js'
];

self.addEventListener('install', event => {
    // Skip waiting forces the new service worker to activate immediately
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
    if (event.request.method !== 'GET') return;

    event.respondWith(
        fetch(event.request)
            .catch(() => {
                // If network fails, try cache, then fallback to offline page
                return caches.match(event.request).then(response => {
                    if (response) return response;
                    if (event.request.mode === 'navigate') {
                        return caches.match('/offline');
                    }
                });
            })
    );
});