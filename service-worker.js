var cacheName = '旧信箱里的拾信者';

/* Start the service worker and cache all of the app's content or use the existing one */
self.addEventListener('install', function (e) {
    console.log('Service worker installed.');
    self.skipWaiting();
});

self.addEventListener('activate', function (e) {
    e.waitUntil((async function () {
        // 换版本后丢掉缓存里旧的 game.zip，别让它盖住新包
        try {
            const cache = await caches.open(cacheName);
            const keys = await cache.keys();
            await Promise.all(keys.filter(function (r) {
                return r.url.indexOf('game.zip') !== -1;
            }).map(function (r) { return cache.delete(r); }));
        } catch (err) { }
        return self.clients.claim();
    })());
});


/**
 * True if the service worker should add the request to a persistent cache.
 */
let addToCache = false;

/**
 * Serves the cached version of the request if it exists, otherwise fetches the
 * request from the network and caches it. Fetch is used in the default mode,
 * which will use the cache for most network requests, freshening the cache
 * as required.
 */
async function fetchAndCache(request) {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);


    try {

        if (request.url.endsWith("?cached")) {
            request = new Request(request.url.replace("?cached", "?uncached"), request);
            let rv = await cache.match(request);

            if (rv == null) {
                rv = new Response("Not found in cache.", { status: 404, statusText: "Not found in cache." });
            }

            return rv;
        }

        // 带版本号的 game.zip 一律走网络：URL 变了就说明是新包，
        // 不能让旧缓存条目顶上来。
        if (request.url.indexOf('game.zip?v=') !== -1) {
            return await fetch(request);
        }

        // fetch 事件的 request.headers 不可写，直接 set 会抛 TypeError，
        // 一抛错就落到 catch 里返回旧缓存。用新 Request 包一层才安全。
        let fetchRequest = request;
        if (cachedResponse) {
            const h = new Headers(request.headers);
            const lm = cachedResponse.headers.get('Last-Modified');
            const et = cachedResponse.headers.get('ETag');
            if (lm) h.set('If-Modified-Since', lm);
            if (et) h.set('If-None-Match', et);
            fetchRequest = new Request(request, { headers: h });
        }

        const response = await fetch(fetchRequest);

        if (cachedResponse && response.status == 304) {
            return cachedResponse;
        }

        if (addToCache && response.status == 200) {
            await cache.put(request, response.clone());
        }

        return response;

    } catch (e) {

        if (cachedResponse) {
            console.log('Served from cache: ' + request.url);
            return cachedResponse;
        }

        console.log('Not found in cache: ' + request.url);

        throw e;
    }
}


/* Serve cached content when offline */
self.addEventListener('fetch', function (e) {
    e.respondWith(fetchAndCache(e.request));
});

self.addEventListener('message', function (e) {
    if (e.data[0] == "clearCache") {
        caches.delete(cacheName);
        console.log("Cache cleared in service worker.");

        addToCache = false;
    } else if (e.data[0] == "loadCache") {
        addToCache = true;
    }
});
