// 投资管理工作台 Service Worker
// 策略：仅缓存「应用壳」index.html，保证手机断网也能打开并打卡；
// 其余同源请求（version.json / 各类 -data.json / sw.js 自身）一律走网络，
// 避免脏缓存导致数据不实时、版本更新提示失效。
const CACHE = 'invest-wb-v20260810.8';
const APP_SHELL = ['./', './index.html'];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(APP_SHELL); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) { if (k !== CACHE) return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  if (new URL(req.url).origin !== self.location.origin) return; // 跨域（外部 API）走网络
  if (req.mode === 'navigate') {
    // SPA 导航：网络优先，失败回退缓存壳
    e.respondWith(fetch(req).catch(function () { return caches.match('./index.html'); }));
    return;
  }
  // 其余同源资源：直接走网络（不缓存）
  e.respondWith(fetch(req));
});
