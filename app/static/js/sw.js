const CACHE_NAME = 'ward42-cache-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css', // If you have custom css
    '/static/js/main.js',
    '/static/js/bootstrap.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js'
];

// Install Event: Cache the app shell
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(urlsToCache);
            })
    );
});

// Fetch Event: Serve cached content or fall back to offline page
self.addEventListener('fetch', event => {
    // Only handle GET requests
    if (event.request.method !== 'GET') return;

    event.respondWith(
        fetch(event.request)
            .catch(() => {
                // If network fails, try cache, then fallback to offline page
                return caches.match(event.request).then(response => {
                    return response || caches.match('/offline');
                });
            })
    );
});