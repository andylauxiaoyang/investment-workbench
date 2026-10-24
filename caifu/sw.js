/* 理财工作台 Service Worker（caifu 作用域） v39 */
/* ★v695 fw2_v695_sw_cache_bust：修复「线上已发布新版、浏览器长期停留在旧版」。
   病根两处——①CACHE 名写死 'caifu-v1'，install 时把**当时**的 index.html addAll 进缓存，
   该快照只在 fetch 失败（离线/断网）时被回退命中 ⇒ 用户一旦离线过一次，就可能被钉在旧快照上；
   ②本文件长期不在 push_gh_v39.py 的 FILES 清单里 ⇒ sw.js 自身从未更新（2026-09-11 → 2026-10-25），
   浏览器无从感知新版本。
   修法：①CACHE 名版本化到 v2（以后改动须递增），activate 清掉所有非当前 cache；
        ②install 不再预缓存 index.html（避免把安装时刻的快照钉死）；
        ③skipWaiting + clients.claim 让新 SW 立即接管；④支持 SKIP_WAITING 消息；
        ⑤fetch 仍网络优先、失败才回退缓存，并只缓存 basic/cors 的 ok 响应。
   配套：index.html 注册端加 updatefound→activated 自动重载（标记 fw2_v695_sw_cache_bust）。 */
const CACHE = 'caifu-v2';
const INDEX = './index.html';

self.addEventListener('install', (e) => {
  /* 不预缓存 index.html：只 skipWaiting，快照交给 fetch 的 network-first 写入 */
  e.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('message', (e) => {
  if (e.data && e.data.type === 'SKIP_WAITING') self.skipWaiting();
});

/* 网络优先：永远先取最新 HTML/数据，失败才回退缓存（离线兜底） */
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  var req = e.request;
  e.respondWith(
    fetch(req)
      .then(function (res) {
        try {
          if (res && res.ok && (res.type === 'basic' || res.type === 'cors')) {
            var copy = res.clone();
            caches.open(CACHE).then(function (c) { c.put(req, copy); });
          }
        } catch (err) {}
        return res;
      })
      .catch(function () {
        return caches.match(req).then(function (m) { return m || caches.match(INDEX); });
      })
  );
});
