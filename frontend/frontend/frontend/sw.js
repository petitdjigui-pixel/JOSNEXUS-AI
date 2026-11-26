const CACHE_NAME = "josnexus-ai-v1";

const APP_FILES = [
    "/",
    "/static/style.css",
    "/static/app.js",
    "/static/manifest.webmanifest"
];


// Installation du service worker
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(APP_FILES))
            .then(() => self.skipWaiting())
    );
});


// Activation et nettoyage des anciennes versions
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys
                    .filter((key) => key !== CACHE_NAME)
                    .map((key) => caches.delete(key))
            );
        }).then(() => self.clients.claim())
    );
});


// Gestion des requêtes
self.addEventListener("fetch", (event) => {
    const request = event.request;
    const url = new URL(request.url);

    // Ne jamais mettre en cache les requêtes API
    if (
        request.method !== "GET" ||
        url.origin !== self.location.origin ||
        url.pathname.startsWith("/api/")
    ) {
        return;
    }

    event.respondWith(
        fetch(request)
            .then((response) => {
                if (response.ok) {
                    const copy = response.clone();

                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(request, copy);
                    });
                }

                return response;
            })
            .catch(async () => {
                const cached = await caches.match(request);

                if (cached) {
                    return cached;
                }

                return caches.match("/");
            })
    );
});
