const CACHE_NAME = "codex-ops-console-v2";
const ASSETS = [
  "./",
  "./index.html",
  "./styles.css",
  "./app.js",
  "./manifest.webmanifest",
  "./icon.svg",
  "./apple-touch-icon.svg",
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))),
    ),
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") {
    return;
  }

  const url = new URL(event.request.url);
  const sameOrigin = url.origin === self.location.origin;
  const isAppShellAsset =
    sameOrigin &&
    (url.pathname.endsWith("/ops/") ||
      url.pathname.endsWith("/ops/index.html") ||
      url.pathname.endsWith("/ops/app.js") ||
      url.pathname.endsWith("/ops/styles.css") ||
      url.pathname.endsWith("/ops/service-worker.js"));

  if (isAppShellAsset) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const responseClone = response.clone();
          event.waitUntil(
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, responseClone)),
          );
          return response;
        })
        .catch(() => caches.match(event.request)),
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request)),
  );
});
