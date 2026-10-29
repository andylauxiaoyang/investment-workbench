/* 理财工作台 Service Worker（caifu 作用域） v40 */
/* ★v695 fw2_v695_sw_cache_bust：修复「线上已发布新版、浏览器长期停留在旧版」。
   病根两处——①CACHE 名写死 'caifu-v1'，install 时把**当时**的 index.html addAll 进缓存，
   该快照只在 fetch 失败（离线/断网）时被回退命中 ⇒ 用户一旦离线过一次，就可能被钉在旧快照上；
   ②本文件长期不在 push_gh_v39.py 的 FILES 清单里 ⇒ sw.js 自身从未更新（2026-09-11 → 2026-10-25）。
   修法：①CACHE 名版本化（改动须递增）；②install 不再预缓存 index.html；
        ③skipWaiting + clients.claim；④支持 SKIP_WAITING 消息；⑤fetch 网络优先、失败才回退缓存。
   配套：index.html 注册端 updatefound→activated 自动重载（标记 fw2_v695_sw_cache_bust）。 */
/* ★v774 fw2_v774_sw_bigbypass：修复「买入峰值/最大回撤（及依赖 fund-daily 净值序列的模块）线上恒为空」。
   实证（2026-10-29，Playwright 线上 A/B）：SW 开启时 fund-daily.json（8MB）响应 200 但响应体
   永不完成、r.json() 永不落地 ⇒ __NAV_SERIES__/__ALLOC_NAV__ 建不起来；SW 禁用即秒建 93 序列；
   本地 http 同 SW 不复现 ⇒ 线上 CDN/H2 × 大响应 × SW 拦截特有。
   修法：①fund-daily.json 一律不拦截（return 放行，走浏览器原生网络栈＝已验证可用路径）；
        ②其余响应 content-length > 2MB 不再写入缓存（防同族问题与缓存膨胀）；
        ③CACHE 名 v2→v3，激活时清掉旧缓存。前端 loader 同步加 json() 15s 超时兜底（fw2_v774_sw_bigbypass）。 */
const CACHE = 'caifu-v3';
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
  var url = req.url || '';
  /* v774：fund-daily.json（8MB 日频净值）不拦截——SW respondWith+caches.put 在线上会把
     响应体卡死（买入峰值/最大回撤恒「—」的根因），直接放行走原生栈。 */
  if (/fund-daily\.json/.test(url)) return;
  e.respondWith(
    fetch(req)
      .then(function (res) {
        try {
          var cl = +(res && res.headers && res.headers.get('content-length')) || 0;
          if (res && res.ok && cl <= 2097152 && (res.type === 'basic' || res.type === 'cors')) {
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
