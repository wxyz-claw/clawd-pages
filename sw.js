/* Clawd Pages — service worker
 * Strategy:
 *  - App shell precached on install (offline-first).
 *  - Navigations: network-first, fall back to cached page, then the shell.
 *  - Same-origin assets: cache-first with background fill.
 *  - Google Fonts: stale-while-revalidate.
 * Bump VERSION when shell assets change.
 */
const VERSION = 'v9';
const SHELL_CACHE = `clawd-shell-${VERSION}`;
const RUNTIME_CACHE = `clawd-runtime-${VERSION}`;
const FONT_CACHE = `clawd-fonts-${VERSION}`;
const CURRENT_CACHES = new Set([SHELL_CACHE, RUNTIME_CACHE, FONT_CACHE]);

const SHELL_ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/apple-touch-icon.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/maskable-512.png',
  './reading/',
  './reading/index.html',
  './reading/reading.json',
  './reading/entries/cerebras-knowledge-base.md',
  './reading/entries/why-software-factories-fail.md',
  './reading/entries/practical-multi-agent-orchestration-in-codex.md',
  './reading/entries/agent-trading.md',
  './reading/entries/the-harness-is-all-you-need-mostly.md'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(SHELL_CACHE)
      .then((cache) => cache.addAll(SHELL_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.filter((key) => !CURRENT_CACHES.has(key)).map((key) => caches.delete(key)))
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  // Cross-origin: only handle Google Fonts (stale-while-revalidate).
  if (url.origin !== self.location.origin) {
    if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
      event.respondWith(staleWhileRevalidate(request, FONT_CACHE));
    }
    return;
  }

  // Page navigations: network first, fall back to cache, then the shell.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(RUNTIME_CACHE).then((cache) => cache.put(request, copy));
          }
          return response;
        })
        .catch(() =>
          caches.match(request).then((hit) => hit || caches.match('./index.html'))
        )
    );
    return;
  }

  // Other same-origin assets: cache first, then network (and store).
  event.respondWith(
    caches.match(request).then(
      (hit) =>
        hit ||
        fetch(request).then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(RUNTIME_CACHE).then((cache) => cache.put(request, copy));
          }
          return response;
        })
    )
  );
});

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(request);
  const network = fetch(request)
    .then((response) => {
      if (response && (response.ok || response.type === 'opaque')) {
        cache.put(request, response.clone());
      }
      return response;
    })
    .catch(() => hit || Response.error());
  return hit || network;
}
