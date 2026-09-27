var staticCacheName = "hangarin-v2";

var filesToCache = [
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
    // Only cache GET requests that are not navigating HTML pages
    if (e.request.method === 'GET' && e.request.mode !== 'navigate') {
        e.respondWith(
            caches.match(e.request).then(function(response) {
                return response || fetch(e.request);
            })
        );
    } else {
        // Always go directly to network for HTML page navigations & POST forms
        e.respondWith(fetch(e.request));
    }
});