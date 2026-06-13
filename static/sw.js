// Khetika Service Worker — PWA Offline Support
const CACHE_NAME = 'khetika-v1';
const OFFLINE_URL = '/offline';

const PRECACHE_URLS = [
  '/',
  '/offline',
  '/static/manifest.json',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;800&family=Noto+Sans+Telugu&family=Noto+Sans+Devanagari&display=swap',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE_URLS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);

  // Network-first for API routes
  if (url.pathname.startsWith('/chat') || url.pathname.startsWith('/mandi') || 
      url.pathname.startsWith('/weather') || url.pathname.startsWith('/sms')) {
    event.respondWith(
      fetch(event.request).catch(() =>
        new Response(JSON.stringify({error: 'offline', reply: 'You appear to be offline. Please reconnect to send messages.'}),
          {headers: {'Content-Type': 'application/json'}})
      )
    );
    return;
  }

  // Cache-first for static assets
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => {
        if (event.request.headers.get('accept').includes('text/html')) {
          return caches.match(OFFLINE_URL);
        }
      });
    })
  );
});

// Background sync for queued messages
self.addEventListener('sync', event => {
  if (event.tag === 'khetika-sync') {
    event.waitUntil(syncQueuedMessages());
  }
});

async function syncQueuedMessages() {
  // Placeholder — real sync would read from IndexedDB and POST queued messages
  console.log('[SW] Background sync triggered');
}
