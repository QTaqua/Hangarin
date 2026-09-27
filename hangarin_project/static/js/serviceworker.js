var staticCacheName = "hangarin-v1";

// Files to cache when installing the service worker
var filesToCache = [
    '/',
    '/static/js/serviceworker.js',
    '/manifest.json'
];

self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open(staticCacheName).then(function(cache) {
            return cache.addAll(filesToCache);
        })
    );
});

self.addEventListener('activate', function(e) {
    e.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== staticCacheName) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', function(e) {
    e.respondWith(
        caches.match(e.request).then(function(response) {
            // Return cached asset if available, otherwise attempt network fetch
            return response || fetch(e.request).catch(function() {
                // Returns cached root page if network fails (offline fallback)
                return caches.match('/');
            });
        })
    );
});