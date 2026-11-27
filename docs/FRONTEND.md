# 前端口径（FRONTEND）— 改 index.html 之前必读

> 作用：把「取数逻辑已经台账化了，但计算逻辑还散在 3.7MB 单文件里」这块补上。
> 原则：**这里只写「谁是唯一真源 + 改动会踩什么」，不抄实现细节**；实现永远以 `edit_work/index.html` 为准，本文与代码不一致时以代码为准并回来改本文。
> 覆盖：`index.html` 3,750,957 字符（v897，2026-11-11；v881 时为 3,736,607）。函数位置会漂，故用 **tag** 定位，不用行号。

## 1. 前端读数的顺序（先搞清数据从哪来，再谈算法）

| 顺位 | 来源 | 何时读 | 覆盖内容 | 关键约束 |
|---|---|---|---|---|
| ① | `data/meta-bundle.json`（四合一静态包） | 首屏，经 `mbGet(key)` | 只有 4 个键：`holdings` / `watchlist` / `macro` / `gold` | **不是实时读取**；bundle 没重打＝页面旧，数据文件再新也没用（PITFALLS P1）。`fw2_v849_mb_timeout`：12s 未落地即显式失败，不许永久 pending |
| ② | 各独立 JSON（`data/fund-daily.json`、`data/pb-ratio.json`、`data/sec-daily.json`、`data/manager-pool.json` …） | 各模块按需 fetch | 序列类、画像类数据 | 每个都有 `cache:'no-store'` 或版本参数；新增 fetch 必须带，否则 SW 缓存会给你旧数据（PITFALLS P8） |
| ③ | `index.html` 内嵌快照（构建期注入） | 直接可用，无需 fetch | `SEC_DAILY`、`PB10Y`、`HOLDINGS_SEED`、`FUND_PROFILES_MIRROR`、`STRATEGY_SNAP` | 内嵌快照＝**构建时的静态副本**，与源文件同源但不会自动更新；改源文件后必须重打（`_make_bundle.py` / `_rebuild_macro_snap.py`） |

**判断「页面为什么是旧的」的固定顺序**：bundle 的 mtime → 对应源 JSON 的 mtime → 内嵌快照是否存在该字段 → 浏览器 SW/`?v=` 缓存。跳过前三步直接改代码，是历史上最常见的返工。

## 2. 五条硬口径（改前端时不许绕开）

**① 市值 = `shares × nav`，`holdRows()` 是唯一真源**

- `holdRows()`（导出为 `window.holdRows`，`fw2_v781b_hold_rows_export`）：合并「账户镜像 `pfMirMap()`」与 `DB.targets`，产出每只标的的份额/成本/净值/市值，是「我的持仓 / 资金平衡 / 资产配置」三处的共同数据源。
- 已被收编到 `holdRows` 的入口：`calcAlloc()`（资产分布，`v696`）、`calcSecurities()`（`fw2_v696_hold_core`）。原「流水份额 × `t.nav`」口径**已退役**——它就是三模块差 1114.09 的源头。
- 新增任何「合计市值 / 单只市值 / 占比」的地方，**必须走 `holdRows()`**，不许自己 `qty * nav` 再算一遍；绕过必被 `check_hold_consistency.py` 抓（`fw2_v696_hold_core` 已挂发布前硬卡）。
- 与天天基金账户总额的差额要**显式披露**（台账独占标的如手工建档股票），不许静默。

**② 价格取「昨收优先」**

- `priceOf(h)`：优先 `state.snapshot.quotes[code].preclose`，无则回落现价（`fw2_v260_px_unify`）。这样与资金平衡的收盘价口径一致；改成现价会与账户总额打架。

**③ 净值取序列，货币基金恒为 1**

- `navOnDate()` 从 `fund-daily.json` 序列取当日净值；**货币型（`funds[].isMoney`）在该文件里只有 `ret` 没有 `nav`**，必须补 `[d, 1.0]` 序列（`v650`），否则货基市值恒 0。这条踩过一次，改净值逻辑时先检查货基。

**④ 「数据截至」只能有一个出口**

- 所有卡片/图表的日期文案统一走 `asOf()`（`fw2_v878` 系列）：取序列末点或显式覆盖，不许各写各的。曾出现卡头 11-07、曲线末点 11-09 并存（PITFALLS P7）。

**⑤ 信号计算有缓存，改仓位后必须失效**

- `signalEvalAll(holdList, watchCodes, force)`（T/W/S 三段）：缓存 key 含持仓指纹（qty/cost/price/lastBuyNav/pePct）+ **5min TTL**（`fw2_v722_cache`）。
- `marketEvalAll(force)`（M 段宏观）：**600s 缓存**，`force=true` 绕过（`fw2_v429`，宏观数据就绪后主动重算让 M12 即时出现）。
- 教训：改了阈值或口径却只改函数体、没动缓存 key → 页面继续显示旧结论，看着像「没生效」。

## 3. 关键函数索引（改动落点）

| 函数 | 职责 | 改动前必须知道 |
|---|---|---|
| `holdRows()` | 三模块唯一持仓真源（份额/成本/净值/市值） | 只增不改；任何绕过它的市值计算都是 bug 源（`fw2_v781b`、`fw2_v696`） |
| `pfMirMap()` | 账户镜像（ttskill 同步结果） | 它是 `holdRows` 的上游；镜像缺标的时靠 `DB.targets` 补 |
| `priceOf(h)` | 单只价格 | 昨收优先（`fw2_v260_px_unify`） |
| `navOnDate(code, date)` | 单只某日净值 | 货基返回 1.0；序列未加载时返回 null 要显式处理 |
| `calcAlloc()` / `calcSecurities()` | 资产分布 / 证券合计 | 均走 `holdRows`；`status==='off'` 必须跳过（`v697d` 曾写反） |
| `poolHeldCodes()` | 三池「是否持仓」判定 | 账户权威优先，`manual_held` 只在未命中时生效（`fw2_v631_pool_held_live`；陈旧 off 曾抹掉真实持仓） |
| `signalEvalAll()` / `marketEvalAll()` | 信号 T/W/S 与 M 段 | 缓存 TTL 5min / 600s；改口径同时改指纹 |
| `mbGet(key)` | 读四合一包（仅 4 个键） | 必须处理超时失败态；新增键要先改 `_make_bundle.py` |
| `asOf()` | 统一数据截止 | 所有日期文案的唯一出口 |

## 4. 常见误改（每一条都真实发生过）

| 误改 | 症状 | 归属 |
|---|---|---|
| 新算一处市值（`qty*nav` 或 `qty*priceOf`） | 三模块数字不一致，差几十到上千 | P9 / `fw2_v696` |
| 改了阈值没改缓存 key | 刷新后仍显示旧结论，「像是没生效」 | PITFALLS P1 的变体 |
| 直接读源 JSON 而不读 bundle | 首屏空白/旧值，后台文件却是新的 | P1 |
| 内嵌快照里手改数值 | 下次重打被覆盖，或与源文件长期不一致 | P1 + 三条铁律第 3 条 |
| 给某个卡片单独写日期 | 卡头与曲线末点不同源 | P7 |
| 新增 fetch 不带 `no-store` | 换版本后线上仍是旧的 | P8 |

## 5. 改前改后各跑一遍（缺一项就别交付）

1. `& py check_js.py`（语法/未闭合/重复声明）
2. `& py check_html_comments.py`（注释隐患）
3. `& py check_hold_consistency.py`（三模块闭合、5 个入口必须经 holdRows、Σmv 与账户 total ±0.5）
4. **真实渲染截图**（本地 8791 → 点进对应页签 → 截图核对数值/日期/对齐）；只读代码不算
5. 改了页面必升 chip 版本并发布，发布后强刷验收（`sw.js` 必须同时发，P8）

## 6. 计划配置（5 万 / 11 只）不是数据文件，改标的或目标金额必须五处同源

`STRATEGY_SNAP` 是 v120 起**内联在 `index.html` 的手写主源**：无独立生成器、不在 `docs/data-ledger.json` 的 34 个数据集里、也不会被 `_make_bundle.py` 重打覆盖。L13 把它归进「内嵌快照」只表示「无需 fetch」，**与 `SEC_DAILY` / `FUND_PROFILES_MIRROR` 有源文件的那类不是一回事**——改它就改这里，别去数据链找生产者。

| 载体 | 定位 tag | 影响 |
|---|---|---|
| `STRATEGY_SNAP.assets` / `plan` / `first` | `window.STRATEGY_SNAP = {` 单行 JSON | 目标金额、定投档位、首次执行单；`assetOf()` / `liveMonthly()` / 执行卡全读它 |
| `firstInvest` / `monthlyNominal` | 同上，头部常量 | 首投合计 / **名义**月投额（后者＝11 只按 target÷12，不是 `plan.build` 数字和） |
| `ALLOC_DEF` | `var ALLOC_DEF = [` | 资产配置表计划内行；`planCodes` 据此把标的排除出「计划外存量」 |
| `roleCodes` / `roleNames` | `var roleCodes = {` | 逐标的执行卡角色归属与说明 |
| `SIGNALS_CFG.barbell.funds` | `barbell: {` → `funds: [` | 半杠铃四档目标权重 / 场内外对照 / 档位实际权重 |

- **现金标的实证（2026-11-10 CDP）**：`state.portfolio` 里 000912 是 `qty=5121.43 / cost=1 / nav=1 / marketValue=5121.43 / assetType=cash`，所以 `priceOf(cash)` 返回 1、`mvOf` 不会产出 `qty×cost` 的脏市值；把它纳入计划内后 `gap<=0 → liveMonthly=0 → 进度金额 0`，不会凭空多一笔定投。
- **改完必须同批**：`_audit_cross_module.py` 的 D 段只给 INFO 不 FAIL，别指望它替你发现 `barbell` 与 `ALLOC_DEF` 漂移（PITFALLS P19）。
- **验收**：`docs/PIPELINES.md` P8 全套；逐行按表头 x 断言列位（组头行 13 td / 普通行 11 td），改一行最容易复发 v872 的列错位事故。

## 7. 净值日期显示：分层时差，不按单一新鲜度阈值（v883 / `fw2_v883_nav_stale`）

| 落点 | 函数 / tag | 口径 |
|---|---|---|
| 交易状态列 | `tradeStatus(market, q, navDate, mlabel)` | 第 4 参数 `mlabel` 是**中文市场标签**（来自 `buildRows()` 的 `_mlabel = marketLabelOf(...)`），用于分层容忍窗口：海外 3 自然日 / 国内 1 自然日 |
| 时效判定唯一出口 | `navDateVerdict(navDate, overseas)` | 返回 `{label, kind, title, stale}`；`stale` 只在国内 `navDate < domNavMax`（**同账户国内基金最新净值日**，非 `state._pfAt`）时为真，`detailRow` 据此追加「·滞后」文字 |
| 现价列小字 | `detailRow` 第 6 个 `<td>` 的 `.sub-line` | `${r.navDate.slice(5)}` + `title` 解释「账户同步时点的最新已披露净值」与 QDII T+1~T+2 |
| 数据源 | `h.navDate`（`holdings-data.json` ← ttskill 双通道） | 页面显示的是**账户镜像的净值日期**，不是 `fund-daily.json` 序列末点；两者不同步时以序列末点为仲裁基准（见 `PIPELINES.md` P9） |

- ★**别把所有「净值11/06」都当异常**：QDII/海外基金跨市场结算，序列末点本身就可能只到 11-06，属正常时差；国内基金若早于账户同步日，才是「源站已有新净值、镜像未补齐」。按「距今几天」设统一阈值会同时误伤与漏报。
- ★**判据不依赖延后加载的序列**：v876 起 `fund-daily.json`（9 MB）在 6 s idle 或切视图才补齐，首屏 `__NAV_SERIES__` 可能为空。所以页面只用「市场标签 + `state._pfAt`」，把精确对拍交给离线硬卡 `_audit_nav_freshness_v883.py`，不要改回读序列。
- ★**改日期口径必同批**：`tradeStatus` 的 `overseas` 正则与 `navDateVerdict` 的 `pfDay` 判据、`detailRow` 的 `st.stale` 渲染是三处同源；只改一处会出现「标了但没解释」或「解释了但没标」。

- ★**v884 修正（2026-11-10 已发布）**：「滞后」参照**不能**用 `state._pfAt`（账户同步日）——今天盘中同步（`_pfAt=11-10`）而国内基金最新 NAV 日仍是 11-09 时，`11/09 < 11/10` 恒真会导致 8 只国内基金全误标「·滞后」。v884 改为取「**同账户国内基金 `navDate` 最大值**」（`domNavMax`）当参照（QDII 恒 ≤ 国内，取全体 max 等价取国内 max），今天盘中同步而 NAV 最新为 11-09 时不再误判；探针的 expected 也随之动态取 `domNavMax`（见 `PIPELINES.md` P9 发布记录）。
- **验收**：`docs/PIPELINES.md` P9 全套；`_probe_hold_dates.py` 的 `EXPECTED_STALE`（动态算，禁写死标的清单）必须等于 `FLAGGED`，海外行零误标、title 全非空、真渲染截图无溢出。

## 8. 资产配置表「共桶主题」限额制（v885 / `fw2_v885_us_broad`）

| 落点 | 函数 / tag | 口径 |
|---|---|---|
| 限额制主题白名单 | `var CAP_ONLY_THEMES = { '美股宽基': true }` | 标记哪些主题用「封顶预算桶」展示：子行**不显示各自目标金额/占比**（统一 `—`），只由组头与小计行展示桶合计 |
| 桶承载者 | `STRATEGY_SNAP.assets['016452'].target = 5000` | 共桶主题里**只有一只**在 SNAP 持 `target`，其余子行 `target=0`；`thGroups` 小计的 `tt` 对子行 `assetOf(code).target` 求和，自然 = 桶目标（5,000）|
| 主题归并 | `ALLOC_DEF` 016452 主题 `纳指100→美股宽基`；extra 块纳指/标普类 `xth = '美股宽基'` | 让 016452/019441/017641/096001 四只归入同一主题组，由同 theme 自动出小计行 |
| 子行目标列 | `renderStratAlloc()` 的 `it.m` 分支 `var capOnly = !!CAP_ONLY_THEMES[m[1]]; var tgtDisp = capOnly ? null : tgt;` | `capOnly` 时目标列渲染 `—`、目标占比同步 `—`；小计行不受影响（仍按真实 `tgt` 求和）|
| 档位归属 | `pileOf` 条件加 `|| xth === '美股宽基'` | 共桶主题归入「进攻/主题」档位，不依赖单只 code |

- ★**子行目标显 `—` 不等于「该主题无目标」**：桶目标 5,000 写在 `STRATEGY_SNAP.assets['016452']`，小计行照常展示 `5,000 / 10.00%`；`—` 只是说「这笔钱不拆给单只子行管」。改这块时别把小计的 `tt` 求和也屏蔽掉（小计 `tt` 用真实 `tgt`，与白名单无关）。
- ★**主题归并只在两处同批**：`ALLOC_DEF` 的主题字段 + extra 块 `xth` 判定；**禁动全局 `code→theme` 映射表**——那张表驱动持仓页/热力图家族聚合，动了会让别的模块跟着变。
- ★**列对齐陷阱（v872 同类）**：共桶主题的小计行若恰是「首组小计」（gi=0, first=true），它带 `grpTds`（合并「档位/档位目标」2 列）所以是 **13 列**（col 0–12）；被组头 rowspan 合并掉的子明细行是 **11 列**（col 2–12）。CDP 探针断言用「列集合 ∈ {[0..12],[2..12]}」判定，别用 `grp-start` class（首组小计行 cls 无 `grp-start`）。详见 `PIPELINES.md` P10 / `PITFALLS.md` P22。
- **验收**：`docs/PIPELINES.md` P10 全套；`_probe_alloc_us_v885.py` 的 `ALLOC_US_V885=PASS`（表头 13 列、子行目标列 `—`、小计 `5,000/10.00%`、无独立标普500/纳指100 小计、`errs=[]`）。

### 8b. v886 起：资产配置表按「指数家族」聚合，基金明细行整体隐藏（`fw2_v886_idx_alloc`）

用户拍板「明细只需要展示到指数合计，不需要标的明细（比如标普500、纳指100）」，且三决策＝**全表聚合 / 明细完全隐藏 / 目标按真实数据聚合**（推翻 §8 限额制「子行目标显 `—`」的展示层——聚合行直接承载真值）。

| 落点 | v886 后的口径 |
|---|---|
| 行结构 | 组内按 `idxFamily(code)`（v796 分类器，恒返回字符串）归并 `idxGroups`，每家族一行；`subtotal-row` 类、首行携带 `grpTds`、rowspan=家族数；**无主题小计层、无基金明细行** |
| 目标金额 | 组内 `it.m` 的 `assetOf(code).target` 求和（0 → `—`）——纳指100=5,000（016452 承载）、标普500=`—`（096001/017641 计划外 target 0） |
| 实际金额 | `it.m` 走 `mvMap`、`it.x` 走 `extra.mv`，逐只累加进家族 |
| 退役机制 | `CAP_ONLY_THEMES`/`tgtDisp` 不再被渲染引用（数据层归桶仍在：`ALLOC_DEF` 主题、extra `xth`、`pileOf`）；`allocThemeToggle`/thGroups/th-hide 折叠逻辑随明细行删除退役 |
| 审计锚点 | `_audit_alloc_cols.py` B 组重锚 `fw2_v886_idx_row`/`fw2_v886_planoutside_row`；A11/A12 断言旧明细行已删；`_audit_alloc_lag_color_v874.py` B02/B07/B09 重锚——**审计口径必须随合法行型变更同步重定目标，改锚点≠放水** |

- ★**rowspan 仍是 v872 回归点**：组头 rowspan=家族数、首行 13 列（grpTds 2 + 11）、续行 11 列；CDP 断言仍是「列集合 ∈ {[0..12],[2..12]}」，探针 `_probe_alloc_v886.py` 逐行按表头 x 归位。
- ★**探针解析陷阱**：单元格 textContent = 名称 + gsub「N 只同指数」直接拼接，`纳指100`+`11 只同指数` → `纳指10011 只同指数`，用 `\d+只同指数$` 剥离会把名字尾部数字一起吃掉——名称必须读 `<b>` 子元素，禁止解析拼接串。
- **验收**：`_probe_alloc_v886.py` `ALLOC_US_V886=PASS`；三审计 `_audit_alloc_cols`(21) / `_audit_alloc_color_v873`(20) / `_audit_alloc_lag_color_v874`(28) 全 PASS。
- **v887 增补（同日）**：`idxFamily` 末级兜底桶「主动权益」非真实指数（实证混主动基金/QDII/货基/国债ETF），按用户指令**展开为逐只标的行**（`fw2_v887_active_fund_row`/`fw2_v887_pl_fund_row`，rowspan 计入展开行数），指数家族聚合行不变。行型判定改二分：指数行=名称含「N 只同指数」、标的行=代码列 6 位码；`_audit_alloc_cols` 扩至 26 断言（B06–B10）；CDP `_probe_alloc_v887.py` `ALLOC_ACTIVE_V887=PASS`（线上 v887，4,332,491 B）。
- **v888 增补（同日）**：用户指令「保留一行主动权益小计＋下方明细」→ v887 纯展开升级两层：该家族先出**小计行**（`fw2_v888_active_subtotal_row`/`fw2_v888_pl_subtotal_row`，`subtotal-row` 类、`N 只标的·小计`、组内聚合目标/进度/实际、`offOf` 唯一实现）＋下方 v887 明细行；rowspan＝`1+明细数`。**家族横跨多档位组时各位置各自出小计**（CDP 实证 3 处）——组内聚合口径，跨档位不可加总。行型三分：指数行（N 只同指数）/ 小计行（N 只标的·小计）/ 标的行（6 位码）。`_audit_alloc_cols` 扩至 32 断言（B10 v888 公式＋B11–B15 小计模板）；CDP `_probe_alloc_v888.py` `ALLOC_SUBTOTAL_V888=PASS`（线上 v888，4,335,613 B，21:57 日频自动化代发、`git/blobs` 回读与本地一致）。整元显示下小计与明细和可差 ±1/行（舍入噪声，PITFALLS P24；严格配平须改口径另拍板）。
- **v889 增补（同日，最终口径）**：用户指令「直接展示标的，不用主动权益合计，主动权益不要显示在表格里」→ v888 小计行删除、明细行直出、**主题标签列空 td**——「主动权益」从表格 DOM 彻底消失（数据层 `idxFamily` 分组保留）。行型两分：指数行（N 只同指数）/ 标的行（6 位码）。rowspan＝`主动权益明细数 / 指数家族 1`（PITFALLS P25：计数按渲染行数非 items 数）。`_audit_alloc_cols` 32 断言（B06–B10 重锚＋B11–B15 负断言）；CDP `_probe_alloc_v889.py` `ALLOC_FLAT_V889=PASS`（14 可见行、「主动权益」表格零出现、明细 4 只标签列空、rowspan 闭合；线上 v889，4,332,564 B）。

### 8c. v890 起：配色 token「原蓝 ＋ 爱马仕橙」

- 用户三态预览后拍板①原蓝＋橙（**否决**方案 B 的克莱因蓝主色）。主色 `--brand #3F5DF8`、`--brand-ink #3a55d6`、15 处品牌蓝 rgba 派生、ECharts 线色与渐变、语义色四值（涨红 `#b91c1c` / 跌绿 `#047857` / 警示琥珀 `#9a4708`）**全部不动**。
- 新增 `--accent-warm #FC8416`（`:root` **单一真源**，只作非文字点缀）；`--ring` 原地改 `rgba(252,132,22,.42)`（焦点环）；`--accent` 仍是深蓝文字色——橙字白底仅 2.48:1，**禁用于文字**。
- 橙出现位置：主按钮底（配 `#101828` 深字 7.14:1，**含 hover 态**）、导航选中左条、聪明钱小色条、选中芯片 / 添加按钮边框、页签选中下划线。橙明定为「中性强调」，不承载涨跌 / 警示语义，面积压在 10% 以内。
- 规则放 `</body>` 前 `<style id="fw2_v890_orange_accent">`（PITFALLS P26：压过 body 后段同特异性规则、连伪类一起覆盖）；懒渲染元素用动态临时节点验证后置覆盖。
- 双层对比度复扫：静态 CSS 层 131 条规则 / 不达标 0 / 压线 0 / 四横线裸用 0；CDP 九视图合并不达标聚类 0；`_check_orange_v890.py` `ORANGE_V890=PASS`（20 项 computed）。
- **已知弱项（知情取舍）**：橙左条压原蓝底 2.05:1（图形元素建议 ≥3:1），比克莱因蓝底 4.71:1 弱；用户拍板的是预览所见，未擅自加粗 / 补描边。


### §8d 数据管理模块（v891，2026-11-11）

- **唯一真源**：`data/data-mgmt.json` 由 `_gen_data_mgmt.py` 生成，前端 `renderDataMgmt()` 正常态直读其 `datasets` 全字段；内嵌 `DMCONFIG` 只作状态文件加载失败时的骨架兜底（v845 起反漂移）。两份配置必须逐字段同源，`_audit_dm_v845.py` 卡 `driftKeys=0`。
- **展示粒度 ≠ 产物粒度**：一个 `macro-data.json` 在页面上拆成 macro / chain_extra / amt / us_fsi / wave 多行；`user_track` 合并 capital-balance + watchlist + ledger-import 三个文件取最新时间戳。故「发布清单 33 个 json」与「页面 39 行」不矛盾，禁止按文件数硬对齐。
- **时间戳口径**：`time` 取文件内字段（如 `meta.asOf`）、`time_text` 从 index.html 内嵌块抽、`time_files` 多文件取最大；`yellow/red=None` = 手动轨只显示天数不判滞后。`fund_jjcc` 用 `concDate`＝**披露期**（三季报 2026-09-30），不是刷新日；顶层无 meta 是结构决定，禁加 meta（会改前端 asOf 语义）。
- **新增/删除条目四步**：生成器 DMCONFIG → 前端 DMCONFIG → 页面写死条数文案 → 重跑状态文件；若产物进过 `push_gh_v39.py` FILES，发布硬卡会自动查漏登。
- **v891 实证补齐**：`sec_daily` 补登（此前发布清单有、页面无）；`fund_jjcc`/`macro_extra`/`user_track` 三项文案订正；`_audit_dm_v845.py` 挂成发布无条件硬卡。CDP `DM_V891=PASS`（39 行 10 列逐行归位）。
- **v892 三项口径拍板**：① 状态文件顶层删 `antiHalluc`（前端零消费、每天虚刷 `appliedAt`），防幻觉功能本体（页面展示列 + `_anti_halluc_p0_*` 注入字段）保留；② `fund_jjcc` 维持 `concDate` 季度披露期，数值与 time 路径不动，仅把口径写进 DMCONFIG 可见 `src` 列；③ `sources.json` 因 3 处真实消费（死规则① 数据日期 / `_audit_pe_chain_v846.py` 单源例外硬卡 / `verify_sync.py` 标记串）不删本体，只删 `_note` 失真宣称并如实化两端 DMCONFIG 的 `sources` 行。`DM_V892=PASS`。


## §8e 资产配置表「定投金额（月）」列（v893）

- **列位**：「目标占比」之后、「进度金额」之前，全表 14 列（colgroup 合计 100%，新列 9%）。组首行 14 td（含 2 个 rowspan 组头）、续行 12 td、合计行 14 td；合法归位集合为 `[0..13]` 与 `[2..13]`。
- **口径**：`_dcaMonthly(code)` = `liveMonthly(code)` = 目标金额 ÷ `totalMonths()`（固定分期），已达标（`gapOf().gap <= 0`）与日限额标的（020712）为 0 → 显示占位「—」。**计划口径，不是台账实际投入**，已在 `strat-note` 写明。
- **同源链**：指数家族行 = 组内各标的月定投额之和；主动权益标的行 = 单只月定投额；计划外两类行 = 「—」；合计行 = 按已渲染行累计的 `sumMonthly`。进度金额 = 月定投额 × 已过期数 `_ME`，进度金额合计 = `sumMonthly × _ME`。旧 `_dcaPlanTotal()`（独立遍历 ALLOC_DEF 全表）已退役，避免与表格逐行口径分叉。
- **改动配方（加/删列必做四步）**：① colgroup + thead + 四类行模板 + 合计行同时增减 td；② CSS `th:nth-child` 数字列居中规则按新索引重锚；③ `_audit_alloc_cols.py` 表头列数 / 行模板 td 数 / 列序索引同步；④ 历史 CDP 探针里的硬编码列索引（`_probe_alloc_color.py` 9/11/12）与其静态锚点（`_audit_alloc_lag_color_v874.py` B27）同步。漏任一处＝发布链红或历史配方悄悄测错列。
- **验证**：`_probe_alloc_v893.py` 逐行按表头 x 归位 + 新列/进度金额倍数同源 + 合计配平 + 表头 nowrap 不溢出 + 「主动权益」零出现 + 无 JS 错误。

## 8e 资产配置表列名口径（v894 / v896 回正）

- 表头 14 列，第 8 列「定投金额（月）」＝计划每月应投（`liveMonthly`，目标÷总月数·固定分期）；第 9 列「累计应投」＝它 × 已过定投期数 `_ME`；第 10 列「**实际市值**」＝持仓市值（`mvMap`＝份额 × 最新净值，含浮动盈亏，v896 由不准确的「实际已投」回正）；第 11 列「进度滞后」＝实际市值 − 累计应投。
- **「实际市值」不是台账累计净投入本金**。v894 曾把该列改名为「实际已投」，名字暗示本金但值是市值，且被两个公式引用，属 v697d 同类「宣称≠实现」；v896 按数值口径把名字改回来，并在可见说明追加「不用于计算投入产出」。`strat-note` 必须保留「含浮动盈亏；非台账累计净投入本金」字样，静态硬卡 `_audit_alloc_cols.py` E03 / E04 / E05 分层卡死。若将来真要换成台账本金口径，须同时改取数、口径说明与 E01–E07，不可只改列名。
- **改名连带清单**：`index.html` 表头 + `strat-note`；`_audit_alloc_cols.py` 的 `ths[]` 断言与 C01；所有用 `col('列名')` 定位的 CDP 探针。历史版本探针按版本冻结保留，不回溯改名。

## 8f 定投执行融合资产配置后的结构（v895）

- 策略执行页 3 个 tab：`alloc` / `bt` / `review`；`plan` 已退役。`stp-alloc` 是唯一承载容器，所有内容由 `renderStratAlloc()` 拼进**同一个 `html` 字符串**再 `el.innerHTML = html` 一次写入：`renderStratTodo()`（上方折叠条）→ 主表卡片 → `renderStratPlan()`（下方折叠存档卡）。任何新增内容必须拼进这条链，事后 `append` 会被重写抹掉。
- 两卡用原生 `<details>`，不用按钮 + 事件委托：切换由浏览器负责，**但折叠态本身会随 innerHTML 重写而丢**，故另存 `window.__ALLOC_OPEN__`，在 `el` 上挂 `toggle` 捕获监听（`toggle` 不冒泡、捕获阶段经过祖先；`el` 不被重写），写入后按状态恢复。静态硬卡 `_audit_plan_merge_v895.py` G01–G03 + CDP V11 卡死。
- **`.strat-note` 是历史探针的定位串**：`_probe_alloc_v88x` / `_probe_alloc_v894` 等都取 `#view-strategy` 内第一个 `.strat-note` 当主表口径说明。待办条位于主表之前，复用该 class 会令探针读到错误文本却不报错 → 新卡一律用 `.alloc-note` + 内联样式（C05 硬卡）。
- 回撤预警标记只加 `<span>` 到 `nm` 单元格内部，**不加列**：`_audit_alloc_cols.py` 的 14 列表头 / 四类行 12 td 断言、`_probe_alloc_color.py` 的列索引 10/12/13 全部无需重锚。这是「融合而不加列」的关键约束。
- 存档卡为历史经验参数（常态期 / 分位<30 加倍档 / 资金源，11 行），明确标注「2026-09-29 v4 · 5 万口径 · 非当前执行依据」与「策略配置截至」；当前每月应投以主表「定投金额（月）」为准。旧「建仓期（当月实投）」表头清零（CDP V10）。

## 8g 投资逻辑 ①–⑧ 表结构（v1029 建、v1050/v1054 加列）

- ①–⑦ 普通层 **10 列**：`代码 / 中文名 146 ｜ 信号含义 300 ｜ 作用·方向 92 ｜ 三态 136 ｜ 生效作用 300 ｜ 引擎 78 ｜ 实测 76 ｜ 口径 300 ｜ 动作 240 ｜ 备注 240`，`min-width:1890px`（实测 1908）。⑧ 层准入表 **5 列**：`150 ｜ 300 ｜ 380 ｜ 320 ｜ 250`，`min-width:1400px`，无三态与生效作用列。
- 三个文案常量同在一个 IIFE 内、互不挂 window：`LOGIC_EFF`（v1050，`[作用点, 组合影响, 现状]`）、`LOGIC_MEAN` / `LOGIC_WHERE`（v1054，id → 字符串）。渲染只有两个出口：`logicRowHtml`（行模板，BT 与非 BT 两分支）与 `logicEffTd(r, knob)`（生效作用单元格）。**改文案只改常量**，不要在两处模板里各写一份。
- 「生效信号显示位置」蓝字在 `logicEffTd` 末行（`#2563EB` / 10px / 1.5）；⑧ 层没有这一列，蓝字「落地位置」写在含义格内。映射缺失时渲染「（未登记含义）/（未登记显示位置）」——出现这两个占位就是数据漏了，不是设计。
- 列宽是硬约束：新增列必须重算 `min-width` 与 colgroup 总和（v505d 事故：项目列 auto 导致全表错位）。表容器为横向滚动，538px 视口下左 3 列可见，属预期。

## 9. 组合回测页口径（v897 / `fw2_v897_bt_panel` 起）

> 这一页曾经「数字都算得出来、但语义反着说」。改这里之前先把下面 6 条对齐，否则很容易把一条对的口径改成错的。

| # | 硬口径 | 唯一实现 | 踩了会怎样 |
|---|---|---|---|
| 1 | **收益率分母 = 本金 + 实际动用的预算外备用金**（`capBase = cfg.budget + P.gridUsed`） | `btRun()` 里 `stats` 段 | 分母钉死 5 万 ⇒ 48.74% 被显示成 66.59%（v896 实证，P32②） |
| 2 | **未动用的备用金既不进期末市值、也不进分母** | 同上；`endV = P.cash + Σqty·nav` | 算进分子＝「没进场的钱也在赚钱」的假高收益 |
| 3 | **「仅本金」口径另存 `retBase`，与主口径并列显示，不许合并/替换** | 统计卡「策略·总收益(仅本金)」 | 合并成一个数＝把「资金规模差异」藏起来，用户无法判断 |
| 4 | **差值一律「策略 − 对照」**；回撤是负数指标，策略更浅应为**负**差值（标红） | `card()` 第 3 参数 + 各卡传参 | 传 `hold.mdd - strat.mdd` ⇒ 策略更差时得正数、染绿（v896 实证，P32①） |
| 5 | **日期标签分三口径**：distinct 净值日期（含货基每日）/ 日历日 / 工作日；`annRet` 用日历天 | `calDays`、`curCalDays`、曲线 hint | 把净值日期数写成「交易日」（3281 vs 2390，P32③） |
| 6 | **截止日上限 = 数据 asOf，且要在数据到齐后回写** | `btMax` + `btLoad().then` 里 `eEnd.setAttribute('max', asOf)` | 只读首屏 `BT_CACHE` 会落占位值 `2026-12-31`；硬编码则选不到更晚日期（P32④）
| 7 | **回撤预算 = 用户亲口给的上限（当前 20%），不得由代码猜** | `btCfg().ddBudget`（默认 20）+ 一次性迁移 `fw2_v898_bt_ddbudget_migrate` | v897 默认写 35% 并在文案里括「可忍 25–35%」——那是**代码替用户编的风险偏好**，直接导致「只用了 35% 预算」这类错误结论（P32⑥） |
| 8 | **占用卡要带方向**：`h = ddBudget − |mdd|`（余量>0 绿 / 越界<0 红）；**Calmar 用严格口径** `(年化 − 无风险)/|回撤|`，达标线 `(目标年化 − 无风险)/回撤预算`；无风险利率走输入框 `btIn_rf`（默认 1.59%＝中国货币网 2026-11-10 10Y 国债 1.5880%） | `card()` 第 3/4 参；`ddCap`、`stats.rfUsed`、`calmarS` | 恒灰看不出越界；简版 Calmar（不扣无风险）会把「跑赢定存的部分」虚增，达标线也跟着虚高（v899 前：1.44 vs 0.50；v899 后：1.32 vs 0.42） |
| 9 | **备用金是「额外追加」，不占 5 万本金**；主口径分母＝本金＋实际动用追加，另列「仅本金」口径 | `capBase = cfg.budget + P.gridUsed`、`retBase` | 把追加当成「5 万内划出」会让两个口径混成一个，48.74% 与 66.59% 无法区分（P32②） |
| 10 | **结果区信息分层，不平铺**：固定四层——①结论条（✓/✗ 达标 + 差多少 + 一句诊断）②两行仪表（年化进度、回撤预算用量）③策略 vs 对照表（差＝策略−对照）④折叠 `<details>` 明细（档位/分年度/流水）。新增指标先决定放第几层，禁止再往平铺卡墙里塞 | `conclBar`、`gbar`、`cmpHtml`、`detailHtml`（tag `fw2_v900_bt_layout`） | 13 张同尺寸同权卡把结论/对照/明细压成一样重，读者要做减法，也看不出「差 3.61pct 是策略问题还是资金问题」（v900 前的用户原话：不够清晰明了、逻辑性不强） |

- **v901 起不再有「口径 / 收益口径」两行提示**（tag `fw2_v901_bt_hint_remove`）：规则文本（建仓 40/35/10/15、网格档距、止盈止损、再平衡带、分母含追加、年化按日历天、严格 Calmar 与无风险 1.59%）只在本文件 §9 与本页结论条体现，页面不再铺成文说明；改口径先改这里，别指望页面自己会解释。

配套不可逆的几处：
- **`tgtAt(d) = (1+目标年化/100)^((d - curve[0].d)/365.25天)`**，以 `curve[0]` 为 1.00 原点；图例/系列/颜色（`#9a4708` 琥珀虚线）三处必须同步，少一处图例就少一条。
- **`Calmar = ann / |mdd|`**、**回撤预算占用 = |mdd| / 回撤预算**：分母为 0 时返回 0，不许 return NaN。
- **分年度收益**：`yrMap[y] = {first, last}`，逐年首末净值求当年收益、**不复利**，超额 = 策略 − 对照。
- **档位表必须有「现金/未部署」行 + 「合计」行**，且合计值 = `stats.strat.end`（与期末市值同源），否则四档加总永远差一截（P32⑤）。
- **交易流水汇总**依赖逐笔 `trades[i].side ∈ {'buy','sell'}`；给 `Px.trades.push` 加新类型时，汇总三元组会漏，必须同时补分支。

### 9b. v902–v903 阈值分组、减配口径与 band 语义变更（2026-11-12）

- **阈值分组（v902b 起）**：`BT_PF` 11 只，宽基 base 4（001015 / 012761 / 023917 / 022438）、进攻 off 4（160422 / 012920 / 020712 / 016452）、黄金 hedge 1（000307）、国债 hedge 1（511260）、现金 bond 1（000912）。四组归属由各标的 **2017-05-07 起** 的实测 vol/mdd 决定（`pfBasis(code)` 实时算，页面同源）。
- **v903 止盈②退役**：`BT_PF` 的 `tp1/tp2` 全部清零，止盈分支代码保留但不触发（便于回滚）。「越涨越减配」改由 `btRebalance` 的**标的级只上带**实现：目标市值 = `T.per[code]` 归一化 × 当前总资产（现金＋全部持仓市值）；市值 > 目标 × (1+band) 就卖出至目标，跌破不补。
- **band 语义变更（最易踩）**：v903 前 `cfg.band`（默认 5）是「档位占比偏离提示」的带宽，只影响标红与提示；v903 起是「单标的减配带宽」（默认 25），直接驱动卖出。`btCfg()` 读到 `band ≤ 10` 一律重置为 25 并 `console.warn('BT_BAND_MIGRATED')`。**任何新增依赖 band 的逻辑，必须先确认拿到的是新语义。**
- **减配资金停在现金**（用户 2026-11-12 拍板）：只减不补、卖出的钱不自动转入其他标的。2017 起实测期末「现金/未部署」35.91%（目标 10%），底仓/进攻分别低于目标 13.65 / 15.74pct——这是设计选择不是漏算，页面动作口径已写明。
- **止损口径未变**：`pf.sl` 触发 `trySell` 清仓该标的、`sellLvl` 归零；之后网格可重新买入。
- **`000912` 特例**：`BT_PF['000912'].bd = 0`，不参与减配（现金等价物反复买卖无意义）。

### 9c. v904 五层信息结构 + 参数区降级（2026-11-12，本地草案）

用户拍板的三问：①参数区同意降为「运行条＋抽屉」②止损卡必须明写「清仓」③曲线把减配点、止损点一起标。

| 层 | 内容 | 实现 / id | 约束 |
|---|---|---|---|
| L1 结论 | `conclBar`：✓/✗ 达标 + 三个原子数（年化差多少 / Calmar 与达标线 / 回撤预算用 %）+ 一句诊断 | `fw2_v904_bt_concl_absorb` | 两行仪表（`gbar`/`gaugeBox`）与结论条重复算「回撤预算占用」，**已不再拼进 `out.innerHTML`**；变量与函数仍留（死代码，可后续清） |
| 运行条 | `#btRunBar`：起始日 / 截止日 / 可投资金 / 运行回测 / 全部参数 ⚙ / `#btRunSum`（一行「当前规则：减配 ±25% · 止损 8% · 网格 3%」） | `fw2_v904_bt_param_drawer` | 摘要独占一行（内联会挤成两行）；`_num()` 整数化，避免 `25.00%` / `¥500.00` |
| 抽屉 | `#btDrawer`（`display:none`）分「资金与区间 / 规则阈值 / 目标与口径」三组 | `fw2_v904_bt_drawer_btn` | **所有原 `btIn_*` id 必须原样保留**，否则 `go()` 收参与 `change` 监听（`btIn_` 前缀 + 250ms 防抖）会断 |
| L2 对照 | `cmpRows` 5 行（年化 / 最大回撤 / Calmar(严格) / 期末市值 / 交易笔数）+ `cmpSwap` 一句换算 | `fw2_v904_bt_cmp5` | 其余 4 行下沉 `cmpSub` 进 L5「对照口径细节」；换算句 = `|回撤差| / |年化差|`，分子为 0 时改文案不写「少亏 inf 块」 |
| L3 规则 | 三卡（减配 / 止损 / 网格），每卡「触发 · 动作 · 资金」三要素；止损动作 **红字加粗「清仓该标的全部持仓」** | `fw2_v904_bt_rules` | 数值由 `res.pfTable` 聚合（`_slBy`/`_gsBy` 按档位），不写死；阈值明细折进 `<details>▸ 按标的阈值（11 只）` |
| L4 证据 | 曲线 `markArea`＝最深回撤段（`_nearestX` 把峰谷日期映射到抽样类目索引）+ `markPoint`＝减配/止损触发点（最多 12 个）+ 分年度表**提到明面** | `fw2_v904_bt_chart_marks` | 类目轴标注必须用**索引**（`{xAxis: idx}`），用日期字符串会静默不显示；抽样 `step = ceil(len/500)` 故日期要经 `_nearestX` |
| L5 明细 | 期末档位占比 + 对照口径细节 + 交易流水（带类型筛选） | `fw2_v904_bt_trade_filter` | `btFilterTrades(k)` + 行 `data-t`；v903 已退役止盈档位，**止盈①② 按钮已删**（否则恒 0 行） |

- **总装顺序不可随意调**（`out.innerHTML =` 一行）：结论条 → 三条提示（asOf/备用金/网格）→ 对照表 + 换算句 → 规则三卡 + 阈值展开 → 曲线 → 分年度 → 明细 `<details>`。
- **`_num` 必须定义在 `conclBar` 之前**：`var` 会提升但赋值不会，放在 `ruleHtml` 之后会让整页弹「回测失败：_num is not a function」（本轮真踩，`fw2_v904d`）。
- **曲线必须跟随容器宽度**：`mountChart` 不自带 resize，挂 `ResizeObserver` 观察 `#btChart`（`fw2_v904f`），否则窄屏停在宽屏 canvas 宽度、整页横向溢出（实测 538px 视口溢出 433px）。
- **验收口径**：数字必须与 v903 逐项一致（2017-05-07→2026-09-28、5 万＋备用金 1 万：年化 6.08% / 回撤 −7.37%（对照 −15.42%）/ Calmar 0.61 / 预算占用 36.85% / 期末 ¥98,369.35 / 34 笔）；canvas 在页面滚动后**截图抓不到**（合成问题），取证改用 `canvas.toDataURL()` 导出。


### 9d. v905 对照表 7 行 + 总投资金额口径 + 「减配」改称「止盈减仓」（2026-11-12，本地已核验、未发布）

| 项 | 口径 | 实现 | 约束 |
|---|---|---|---|
| 对照表顺序 | 投入 → 时长 → 结果 → 风险 → 性价比 | `fw2_v905_bt_cmp7_tp_rename` | 7 行：总投资金额 / 投资年限 / 期末市值 / 总收益率 / 年化收益 / 最大回撤 / Calmar(严格)；**交易笔数下沉 `cmpSub`**（它是操作量，不是投资结果） |
| 总投资金额 | 本金 + **实际动用**的备用金 | `res.cfg.budget + S.gridUsed` | 不是设定额度（`gridFund` 10,000 只动了 6,500）、更不是累计买入流水；剩余备用金另起一行 `备用金未用尽` |
| 总收益率 | 与总投资金额**同分母**（`capBase`） | `S.strat.ret` | 必须与「总投资金额」自洽：`期末市值 / 总投资金额 − 1`。**不要用 `retBase`**（= `endV/budget`，分子含追加收益、分母只有本金，系统性高估；本机实测 96.74% vs 74.11%） |
| 投资年限 | 日历天 / 365.25 | `(new Date(S.end) − new Date(S.start))/86400000/365.25` | 不要依赖 `S.calDays`（渲染层未导出该字段）；`dateStr + 'T00:00:00'` 强制本地解析，避免 UTC 位移 |
| 止盈减仓 | 涨超目标 1+band 卖回目标 | `btRebalance`（未改逻辑） | **只改展示文案，`trades.type` 保持 `'再平衡'`**；筛选键 `data-k`/`data-t` 与 `actMark` 过滤依赖该值，改 type 会同时打断流水筛选与曲线标注 |
| 差列单位 | 收益率差 = pct，金额相对差 = % | `rN(nm, sv, hv, dv, u)` 第 5 参 | 期末市值这类行必须传 `'%'`，否则 `+5.30 pct` 单位错 |
| 标题防挤 | 长 hint 会把 `h3` 压成两行 | `h3 style="white-space:nowrap"` + 脚注 | 加长 hint 前先看窄屏；口径补充说明放表下 `font-size:11px` 脚注，不进 `card-h` |


## 8g v896 列名回正后的分区与重锚（2026-11-11）

- **旧列名不是全局清零**：`index.html` 全文「实际已投」允许且仅允许 2 处，都在表头 JS 注释块里——v894 改名史实 + v896 回正映射。现役表头与 `strat-note` 必须零残留。故 E04 硬卡用**精确形态**判定（`实际已投 = 当前持仓市值` / `目标 − 实际已投` / `实际已投 − 累计应投` / `<th>实际已投</th>` 四种），不能用 `'实际已投' not in s`，否则会误删护栏锚点。E06 反过来卡死史实注释必须保留。
- **改名的连带面比想象大**：`_audit_alloc_cols.py` A03b（`ths[9]`）/ C01 / E01 / E03 是发布硬卡，漏一处直接拒绝发布；`_probe_alloc_progress.py` 的 `col('实际已投')`、`_probe_alloc_v893.py` 的 `ths[9]['t']` 是复用探针，漏改会静默取到 `-1` 列。历史版本专用探针按版本冻结，不回溯改名。
- **分层硬卡防「改回名字又偷偷改数」**：E07 卡 `_dcaProg` / `_dcaMonthly` / `liveMonthly` 三处函数实现原文不动（注意 `_dcaMonthly` 真实形态带 `typeof` 守卫，别凭印象写锚点）；A02/A03/B03–B05/D01–D07 继续卡 14 列与同源。
- CDP 探针 V1 除列序外额外断言「表头零旧列名」，V1b 断言「口径说明零旧列名 + 投入产出禁用声明可见」；线上核验 A14 / C9 把同一判定延伸到 `git/blobs` 与 Pages 实况，避免本地对了、CDN 还是旧字节。

### 9e · v906 备用金不限额 / 投资口径三行 / 零头

| 指标 | 取值 | 必须自洽的点 |
|---|---|---|
| 总投资金额 | `预算 + 累计动用备用金`（`stats.gridUsed`） | 备用金不限额时＝实际累计花掉的总额，不再是固定 `+10,000` |
| 累计买入 | `Σ trades(side=buy).raw` | 含卖出回款再买，是**周转量**，不等于投入 |
| 净投入 | `累计买入 − 累计卖出` | 反映"还压在场内"的自有资金 |
| 总收益率 | `strat.ret`（分母 `capBase = 预算 + gridUsed`） | 与总投资金额同分母；**末期口径**，后投入资金未按期初计权，属保守读数 |

实现要点：

- **不限额哨兵**：`P.gridFund === null` 表示不限额，`0` 表示预算内（不开备用金）。判定必须写 `Px.gridFund !== 0` —— 写成 `!= null` 会把哨兵本身排除（`null != null === false`），表现为 `gridUsed` 恒 0、总投资金额倒退回本金。
- **不限额时的三处特殊处理**：`need` 用 `Infinity`（否则 `null < amt` 恒真、每笔都买不进）；`gridFund -= amt` 必须跳过（`null` 参与算术会被当 0）；`gridOk` 对 `null` 直接放行。
- **零头**：`gridAmt` 是单档金额，余额在 `(0, gridAmt)` 时改为按余额买，否则余额永远凑不够一档、`gridFundLeft` 永久为正且页面显示"未用尽"却再也不动。
- **金额精度**：流水 `t.amt` 是 `Math.round` 后的展示值，累计买卖必须用 `t.raw`，否则几十笔叠加会出现与总投资金额对不上的尾差。

### 9f · 持仓过程四图（v910）

容器：`#btPosChart`(320px) / `#btDDChart`(190px) / `#btMonChart`(250px) / `#btAttrChart`(290px)，插在净值曲线 `#btChart` 之后，标题「持仓过程」。挂在同一个 `setTimeout(..., 0)` 回调末尾，各自 `try/catch` + `console.warn`。

数据全部在 `renderBacktest()` 内由 `curve / trades / seriesBy` 现算，**不新增 `btRun` 返回字段**：

| 序列 | 构造 | 口径要点 |
|---|---|---|
| `_posSeries[code]` | 逐日推 `qty`（buy 加 `amt/nav`、sell 减 `min(amt/nav, pre)`），市值 = `qty × nav` | nav 取 `seriesBy[code].seq[d].nav`，停牌日沿用上一有效值；**月末覆盖**；`qty=0` 写 `null` 断线（写 0 会让所有线压在 0 轴） |
| `_posTot` | 同一时刻各标的市值之和 | **挂右轴** `yAxisIndex:1`——单只 5–8 千、合计 2–5 万，同轴会把单只压平 |
| `_ddSeries` | `v / 峰值 − 1` | 日频，面积倒挂 |
| `_monRet2` | 月末净值环比 | 柱状，正绿 `#047857` / 负红 `#B91C1C` |
| `_attrRows` | `mv + sell − buy` | 降序；**合计必须等于 `期末市值 − 累计买入`**（v910 实测 20,050.11 = 80,050.11 − 60,000） |

硬约束：本页 ECharts 只有 `line` / `bar` / `pie`，**heatmap / scatter / custom 会被静默丢弃**（见 PITFALLS P40）。

尺寸同步：`mountChart` 已在 v911 统一挂 `ResizeObserver`（`init` 后 `observe(el)` + 立即 `resize()`，`dispose` 前 `__ro.disconnect()`），窗口缩放 / 抽屉展开 / 面板显隐都会重绘。**判断布局宽度必须用 `canvas.getBoundingClientRect().width`，不能用 `canvas.width`**（后者是 DPR 绘图缓冲，会差 1.5–2 倍，见 PITFALLS P41）。

标题层（v912）：四图各有独立小标题 `① 分标的持仓市值` / `② 回撤水下` / `③ 月度收益` / `④ 收益归因`，各配一句 11px 灰字口径说明；大标题 `持仓过程` 的 hint 只留读法（四张图连看：谁在长 · 跌多深 · 哪个月难受 · 谁在撑）。标题是 HTML `<div>`，**不要**改成 ECharts `title` 配置——图内 title 会占 `grid` 顶部空间并与 legend 争位，窄屏更糟。说明行在 530px 内容宽下单行不折行，新增文案前先按此宽度估字数。

### 9g · 自选基金池与回测标的池（v913）

**子模块**：`#dcPoolWatchWrap`（tab `data-dc="pool-watch"`，排在 `overview` 之后），入口 `renderPoolWatch()`。数据三源合并：

| 来源 | 存储 | 写入方 |
|---|---|---|
| 自选表 | `watchlist-data.json` → `window.POOL_WATCHLIST` | 助手手工维护（生产链外，2026-10-22 后未更新） |
| 筛选池转入 | `localStorage.fw2_watch_added_v1`（无 `manual` 标记） | 「筛选基金」操作列 `data-pool-act="toWatch"` |
| 手动加入 | 同上，`{name, addedAt, manual:1}` | 本 tab 工具条 `#pwAddCode` / `#pwAddBtn`（支持「代码 名称」） |

剔除：`fw2_watch_removed_v1`（移除）、`poolHeldCodes()`（已持仓）。来源列按 `manual` 分「自选表 / 筛选池 / 手动」，note 三类计数分列。列集：**v914 起自选池改用精简 7 列**（`poolWatchCols()`，与资产配置/筛选池的 61 列全列集分开）：

| 列 | 取值 | 说明 |
|---|---|---|
| 名称 / 代码 · 来源 | `_meta.name` / `row.code` / `_meta.source` + `_meta.watchAt` 短日 | 三行小字，名称限宽 124px 折行（**必须** `inline-block + max-width + white-space:normal + word-break:break-word`，改 `nowrap` 会撑破列宽） |
| 档位 / 家族 | `_meta.e.role` / `_meta.e.family` | 双行，限宽 78px |
| 近1年 / 近3年 / 最大回撤 / 总分 | 直接复用 `poolColsAll()` 的 `iv_y1` / `iv_y3` / `mdd` / `score` 列对象 | 渲染与格式化仍在 `poolTableHtml` 内，别自己算 |
| 操作 | `opCell` 已买入 / 移除 | **竖排**（横排两按钮宽 ~110px 会把整表顶到 536px） |

实测 `scrollWidth=500 / clientWidth=501 / overflow=0`。资产配置池 61 列 / 4639px、筛选池 61 列，均未受影响；完整 64 列数据仍在两池可查。

**加载时序**：`loadPoolData()` 原只在 reload/首次进入基金数据时调用，`pool-watch` 分支漏调 → 自选表恒空。v913 在 `showTab` 的 `pool-watch` 分支先 `loadPoolData()`，并在 fetch 成功回调里检查当前 tab 是否仍是 `pool-watch` 再补渲一次。

**回测标的池**（`fw2_v913_bt_pool`）：

- 开关：`btCfg().pool`（`BT_KEY` 持久化），抽屉 `sel('pool', …)`，取值 `barbell`（默认，零回归）/ `barbell_watch` / `watch`。
- `btTargets(budget, cfg)`：`barbell` → `SIGNALS_CFG.barbell.funds` 原样（13 条，含 022676/007866 两只 w=0 候选）；其余两种模式把自选池里「不在原标的集」的代码追加（`barbell_watch`）或替换（`watch`）。
- 归堆：`btRolePile(role)` —— `底仓/缓冲→base`、`进攻/主题→off`、`海外独立→off`、`安全垫→bond`、`对冲→hedge`、其它→`off`。
- 权重：新增标的 `w = 该档非零 w 的中位数`（不能给 1，会被原标的 w≈10 压成 1%~2%），档内按 w 归一。
- `watch` 模式额外做一次档位归一：只在有标的的档位间按原 target 比例换算（缺档预算摊入其余档），否则全在进攻档时只用 35% 预算。
- 自选表要拉 `watchlist-data.json`，但回测闭包够不到 `loadPoolData` → 自带 `btEnsureWatchPool()`（相对路径 fetch，到位后 `__btGo()` 重跑一次）。
- `btRun` 返回新增 `poolInfo{ mode, planned, used, zeroW, skipped[] }`，摘要行据此回显「计划 / 实际建仓 / w=0 候选 / 缺日频代码」；`used` 必须排除 `w=0` 与无 `seriesBy` 的代码，才能与「按标的阈值」表只数（`res.pfTable.length`，v913 前硬编码 11）对齐。
- 阈值：新标的无 `BT_PF` 记录时 `btPF` 回退全局 `cfg`（sl/band/gridStep），不需要维护新表。

### 9g-b · 回测权重口径与「按基金类型」分档（v916）

- **权重口径＝每只固定占总预算 X%**（`btCfg().watchW` 默认 5，上限 45，抽屉 `#btIn_watchW`）。`btTargets` 里每只自选 `per = budget × watchW%`；同一档合计超该档目标 **85%** 时按比例压缩，压缩明细写进 `squeezed`（如 `off 99%→29.8%`）。
- **「杠铃 + 自选池」**：原杠铃标的只分「该档目标 − 自选占用」后的剩余预算，按原有 w 比例摊；自选 3 只各 5% 时不挤压原标的档位归属。
- **「仅自选池」**：**缺档预算不摊入其余档，直接留现金**（用户明确否决摊入方案）；空置比例写进 `idle`，摘要回显「缺档空置 85% 预算留现金」。
- **档位按基金类型判定 `btTypePile(code)`**（类型优先，`btRolePile` 仅兜底）：债/货币→`bond`；QDII/海外→`off`；黄金/商品（`type` 含其他/商品/另类 且 `family` 命中黄金/商品/原油/白银/REIT）→`hedge`；`family` 命中宽基白名单（A500/沪深300/中证500/中证800/上证50/红利/现金流/全指/MSCI/价值/成长/宽基）→`base`；其余 `type` 含 股票/偏股/指数 →`off`；都没有才回退 `role`。
- **画像加载是硬前提**：`poolProfileE()` 已加内嵌镜像懒加载（否则直接进策略页时 `FUND_PROFILES` 为 null、分档全落进攻）→ PITFALLS **P45**。
- `btRun` 返回的 `poolInfo` 透传 `watchW / idle / squeezed`，摘要行（`#btRunSum`）按模式回显，非 `barbell` 模式才出现自选权重段。

### 9g-c · 自选池列集回归三池统一（v917，用户 2026-11-12 要求）

- **口径**：自选池 `renderPoolWatch` 的 `cols` 从 `poolWatchCols()`（7 列精简）改回 `poolColsAll()`，与「资产配置」「筛选基金」**同一套 61 列、同一表头、同一列序**（实测三池 `thead th` 数量均为 61，前 12 列逐字相同：名称 / 代码 / 状态 / 档位 / 家族 / 收益36.27% / 风险27.47% / 经理27.47% / 产品8.79% / 总分 / 申赎 / 今年以来）。
- **操作列**：`opW` 108→170、竖排→横排（与筛选池 `opCell` 同款），末三列「申购限制 / 详情 / 操作」。
- **首列 sticky 恢复**：v915 关掉 `#dcPoolWatchWrap` 首列 left sticky 的三条覆盖整段删除（含表头 `top:0`），恢复与另两池一致的冻结首列。
  - **前提**：完整列集必然产生真实横向滚动（实测 `.table-wrap` `4566/509`），P44 的「`scrollWidth < clientWidth` 时 sticky 吞内容」不成立；`scrollLeft=1200` 与滚到最右（`4057/4057`）两种位姿下首列文字均可见（`firstTD.x=10`）。
  - **反向约束**：若日后又把自选池列集压到一屏之内，必须重新关掉 left sticky，否则首列内容会被裁（P44）。
- **名称列宽**：与筛选池完全一致（`td` 118px / 内层 `div` 105px / `overflow:hidden` / 全名进 `title` 悬浮 + 点击进基金透视），不是自选池单独收窄。
- `poolWatchCols()` 保留但不再被调用（v914 的 7 列定义仍在，便于回退）。

### 9g-d · 组合回测拆双入口 + 自选组合（v918，用户 2026-11-13）

**背景**：用户要求「组合回测里包含持仓组合回测、自选组合回测两项」，自选组合可选范围＝已持仓 / 自选池 / 筛选池三处。v913 曾有 `watch` / `barbell_watch` 两个遗留模式（只能取自选池），v918 保留它们但归到「自选组合」语义下，同时新增 `custom` 自由勾选模式。

**入口与路由**
- `renderBacktest()` 顶部 `btTab(v,t,sub)` 生成两个卡：`barbell`＝持仓组合回测（副标题「杠铃 11 只固定档位（原口径）」）、`custom`＝自选组合回测（副标题「自己勾基金：持仓 / 自选 / 筛选任选」）。
- 高亮：`on = (v==='barbell') ? cfg.pool==='barbell' : cfg.pool!=='barbell'`。**不要**写成 `cfg.pool===v`——旧的 `watch`/`barbell_watch` 会让「两个卡都不亮」或「亮错卡」。
- 点卡 → `cfg.pool = v` → `btSave(cfg)` → `window.__btGo()`。
- 面板显示条件 `cfg.pool !== 'barbell'`（不是 `=== 'custom'`）：旧模式也要能看到面板与「切换到自选组合」按钮。

**数据流**
- `btEnsureScreenPool()`：`fetch('./screen-pool.json')` → 失败走 `raw.githubusercontent.com/.../master/caifu/screen-pool.json` → 写 `window.SCREEN_POOL`；`window.__BT_SP_LOADING` 防重入。
- `btCustomUniverse()`：三池合并去重，`src` 优先级 **持仓 > 自选 > 筛选**；`pile` 用 `btTypePile(code)`（与 v916 分档同源，勿另建规则）；`hasSeq` 看 `BT_CACHE.rowsByCode[code]`，无序列的项标「无日频序列」并在跑回测时跳过（摘要行会列出来）。
- `btCuState() = { src:'all'|'held'|'watch'|'screen', kw:'' }`（`window.__BT_CU_STATE`）；`btCuSelected()` 读 `window.__BT_CUSTOM_CODES`，为空时回退 `cfg.customCodes`。

**权重口径（`btTargets` 内的分支顺序，顺序错会串模式）**
1. `mode==='custom' && wMode!=='fixed'` → 等权满仓：`pct=100/n`、`per=round(budget/n)`、`idle=0`；
2. `mode==='barbell'` → 原杠铃档位目标；
3. `else`（`barbell_watch` / `watch` / `custom+fixed`）→ v916 固定百分比（`watchW`%，缺档留现金，同档合计超 85% 压缩）。

**结果口径**
- custom 模式下 `tgtOut` 的四档目标＝勾选基金按 `pile` 汇总的真实占比，不再恒显杠杆档位 40/35/10/15。
- 透传 `customN / customWMode / eqPct` 到 `_poolInfo`，摘要行文案：「自选组合（等权满仓）（计划 N 只 / 实际建仓 M 只；N 只等权，每只 X%）」/「自选组合（每只固定 X%）（… 缺档空置 Y% 预算留现金）」。
- 空组合：`go()` 在 `btTargets` 前拦截，写「本次回测：自选组合未勾选任何基金」。

**事件绑定（IIFE 收尾处，改任一处都要把另外几处一起看）**
`[data-bt-tab]` 切 tab｜`[data-cu-code]` 勾选（change → 写 `__BT_CUSTOM_CODES` → `btSave` → 重跑）｜`#btCuSearch` 关键词｜`[data-cu-src]` 来源 chip｜`[data-cu-wm]` 等权/固定｜`[data-cu-act]` 预置（`barbell` 需 `filter(f => (+f.w||0) > 0)`，否则 13 只）｜`[data-cu-legacy]` 旧模式切 custom｜`window.__btCuRefresh` 供异步三池到位后重刷列表。

**验收基线（本地 8791，50,000 / 2021-01-04→2026-11-11 / sl=10 / band=25）**
- 持仓组合：年化 5.08%、计划 13 / 建仓 11、备用金 20 笔 ¥10,000、流水 41 行、面板隐藏。
- 自选组合等权 3 只（006373/270042/007817）：各 ¥16,667、年化 −1.83%、三只全止损清仓、期末 ¥48,005。
- 自选组合固定 5%：各 ¥2,500、空置 85%。
- 三池列表 66 项（持仓 23 / 自选 3 / 筛选 40），面板 509×418 无溢出。

### 9g-e · 删除「模式」下拉：回测口径固定为「固定预算」（v919，用户 2026-11-13 要求）

**背景**：v351 起参数抽屉有「模式」下拉，两项：
- `fixed` 固定预算（5 万从零建仓）：按 `btTargets` 的档位目标金额、在标的序列起点一笔建仓；
- `real` 真实持仓口径（台账买入驱动）：读 `localStorage.fw2_trade_ledger_v1` 的买入流水，用区间内首笔买入的**日期与金额**建仓。

2026-11-13 用户看过两者口径说明后要求删除 `real`。理由（实测）：`real` 是**混合口径**——只有台账在区间内买过的标的走真实分支，没买过的仍回退按档位目标建仓（判据 `ledgerBy[code] && ledgerBy[code].length`），名字与实现不符；且台账在本机常为空，一开就红字拒绝跑。

**删除清单（六处，缺一处就会留孤儿逻辑）**
1. `btCfg()`：`mode` 字段保留但合并 localStorage 后**强制** `d.mode = 'fixed'`（旧配置残留 `real` 就地压回）；
2. `btRun()` 开头：删 `ledgerBy` 整段（含 `LEDGER_KEY` 读取、按 code 分组、按日期排序）；
3. `btRun()` 建仓处：删 `realFirst` 分支，只留 `var amt = s.targetAmt;`；
4. `renderBacktest()` 抽屉：删 `sel('mode', …)`，替一行静态说明；
5. `go()`：删 `btIn_mode` 读取，写死 `c.mode = 'fixed'`；
6. `go()` 数据加载前：删「`mode==='real'` 且台账为空 → 红字拦截」。

**残留检查**（`_chk_v919.py`）：`ledgerBy` / `btIn_mode` / `realFirst` / `mode === 'real'` 必须全为 0；`LEDGER_KEY` 应仍有 7 处（「交易台账」页在用，不动）。

**验收基线**：徽标 v919、`btIn_mode` GONE、年化 5.08% / 41 笔流水（与 v918 固定预算一致）；把 `fw2_bt_cfg_v1.mode` 手动改成 `'real'` 再重载 → `savedMode` 必须是 `fixed`。

**代价（如实记录）**：删掉后无法在页面上对比「按真实买入时点/金额的复盘曲线」；要恢复只能从 v918 备份（`D:\Temp\index_v918_backup.html` 若有）或发布历史里取回这段实现。

### 9g-f · 「策略 vs 对照」改按标的明细宽表 + 合计行（v920，用户 2026-11-13 五点拍板）

**用户原话**：「组合回测完成后需要形成一个详细的表格，结合策略VS对照表的形式，把策略VS对照表融合成一个表，新表格的字段策略VS对照的所有字段，但是必须是以具体明细标的展示，最下面才是合计。」五点拍板：①同档位的标的放一起 ②按 20 列宽表 ③标的回撤和波动「都保留」（不并成一列） ④新表替代原「策略 vs 对照」表 ⑤「差异归因」列加。

**数据接入点（`btRun` 内，函数末尾）**
- 新增 `perFund` 数组并随 return 导出（`poolInfo` 之后）。字段：`code/name/pile/d0/dEnd/closed/yrs/buy/sell/mv/net/cnt/gridN/gridAmt/targetAmt/hEnd/retS/retH/annS/annH/mddS/mddH/volS/volH/calS/calH/why`。
- 策略侧全部由 `P.trades` 聚合：`buy=Σ buy.raw`（含 `src='备用金'` 的网格买入）、`sell=Σ sell.raw`、`d0`＝首笔 buy 日、`dEnd`＝`pp.qty<=0` 时的最后一笔 sell 日，否则 `days[n-1]`；`mv=pp.qty×s.lastNav`（`P.pos` 未随 return 导出，故必须在 `btRun` 内算）。
- 对照侧＝`s.targetAmt × navEnd/nav0`：`nav0` 取 `seq[d0].nav`、`navEnd` 取 `seq[S.end].nav`（S.end 当天若缺行则回退 `s.lastNav`）——**与内核 B 的市值口径完全同源**，合计恒等于 `stats.hold.end`（实测 11 只合计与组合级 44.57% 一致）。
- 回撤/波动：`_dd(vals)` 逐点峰谷、`_vol(vals)` 日收益总体标准差 ×√252（脚本内私有实现，未改全局 `annVol`/`maxDD`）。货基 `seq[d].nav` 恒为 1 → 回撤 0、波动 0、收益 0，与内核一致。
- 年化用 `Math.pow(1+ret, Math.min(365.25/hDays, 3))−1`，与组合级 `annRet` 同封顶规则。

**渲染层（`renderBacktest`）**
- 原 `cmpRows`（9 行主表）删除；`rN/rT` 保留给「明细·对照口径细节」副表 `cmpSub` 用。
- 排序：`_pord = {base:0, off:1, bond:2, hedge:3}`，同档内 `b.buy - a.buy`（投入降序）。
- 列（23）：标的（名称(代码)+清仓徽章）｜档位｜建仓日｜年数｜投入｜卖出｜期末在仓｜净收益｜总收益率 策略/对照/差｜年化 策略/对照/差｜回撤 策略/对照｜Calmar 策略/对照｜波动 策略/对照｜笔数｜备用金买入｜差异归因。
- 表宽 1850px（`min-width:1780px` + `width:100%`，auto 布局）、外层 `overflow-x:auto`；**整表 `white-space:nowrap`**（见 P48 ②）。
- 合计行：`_sb=S.buyAmt / _ss=S.sellAmt / _sm=S.sumPiles`，`net` 强制由三者相减；比率与风险列直接用 `S.strat.* / S.hold.*`（组合级），末格写「组合级」。
- 行内闭合：逐只先把 `buy/sell/mv` 四舍五入到分，再 `net = mv+sell−buy`，`retS = net/buy`，并让「差」列由两个已舍入值相减 —— 保证表内能被手算复核。
- 差异归因 `why`：`止损清仓 / 止盈减仓×N / 网格×N / 再平衡×N` 用「 · 」拼接；全无则「买入后未操作」。

**验收基线（本地 8791）**：11 行（底仓 4 / 进攻 4 / 安全垫 1 / 对冲 2）；合计 `¥60000.00 / ¥36717.91 / ¥43496.56 / +¥20214.47`（相减闭合）；`+33.69% / +44.57% / −10.88pct`；`+5.08% / +6.49% / −1.41pct`；`−7.02% / −21.66%`；Calmar `0.50 / 0.23`；波动 `4.59% / 8.09%`；41 笔；`¥10000.00 ×20`。逐行 `rect.height` 必须全为 30px（有折行即列宽不足）。

**已知边界**：①未清仓的 8 只「回撤/波动 策略」与「对照」必然相同（同一净值序列、同一区间），用户已明知并要求两列都留；②自选组合的 `fixed` 权重与「缺档留现金」两种路径未逐项验证 `perFund`；③逐只 Calmar 不扣无风险利率（合计行扣，脚注 ④ 已写明）。

**v921 补充（逐只 Calmar 口径统一）**：`perFund` 的 `calS / calH` 由 `年化/|回撤|` 改为 `(年化 − rfUsed)/|回撤|`，`rfUsed` 就是 `btRun` 里 v899 引入的那个（`cfg.rf`，抽屉 `btIn_rf`，默认 1.59%），与组合级 `stats.strat/hold.calmarS` 同一公式；`mdd === 0` 记 0。脚注 ④ 同步改写。**注意**：`rfUsed` 是 `btRun` 的局部变量，`renderBacktest` 里要用 `S.rfUsed`（见 P49）。逐只加权平均不等于合计（金额与持有期不同），脚注已写明，不要拿它做校验。

**v922 补充（配色口径）**：本表统一走 `_oC(v)`＝`v>0 ? CHART.up : (v<0 ? CHART.down : '#71717A')`（中式：盈利红 `#b91c1c`、亏损绿 `#047857`），回撤策略列同规则；「差」列因配色翻转，语义改写为「红＝策略更好 · 绿＝策略更差」。**注意**：`CHART.up/down` 在本工程就是「涨红跌绿」，别再单独写死颜色；结论条用的是另一套 `okCol`（状态语义），改配色时不要误伤。

**v923 补充（回测页配色口径）**：整页统一为「正数/盈利＝红 `CHART.up #b91c1c`、负数/亏损/回撤＝绿 `CHART.down #047857`、零＝灰 `#71717A`」。落点：明细表 `_oC`、摘要卡 `dcol`、副表 `rN`、按标的汇总与流水浮动 `_pColor`（三态）、风险 chips、月度柱 / 归因条 / 水下面积 / 净值图回撤区。**不在此口径内**：结论条达标状态色（`okCol` 绿 / `CHART.bad` 红）、流水动作类型色、报错红字、图表系列线色。新增着色时先问一句「这是盈亏还是状态/分类」，前者走 `_oC`/`_pColor`，后者别套红绿。


## v924 补充（自选组合回测：逐只参数口径）

- **逐只参数唯一来源**：`cfg.pf = {code:{w,bd,sl,gs,on}}`（`fw2_bt_cfg_v1` 内）。面板改动先写内存 `window.__BT_CU_PF`，再 `btSave`。
- **只在 custom 生效**：`btPF(code,cfg)` 里 `cfg2.pool === 'custom'` 才读 `cfg.pf`；`pool='barbell'` 仍走 `BT_PF_CONST`（内置预设），改自选组合里的同码标的不会影响持仓组合回测。
- **权重语义**：`w` 是该只占总预算的百分比。合计 >100 时 `btTargets` 按比例压到 100 并写入 `squeezed`；不足 100 的差额进 `idle`（留现金，摘要行回显）。
- **规则开关**：`on=false` 时 `btPF` 返回 `on:false`，该只只建仓、不执行止盈减仓/止损/网格；`sl=0` 是「设置止血损」（与 `on=false` 不同，止盈仍可触发）。
- **档位**：`btTypePile` 先查 `SIGNALS_CFG.barbell.funds` 的 `pile`，再按画像 `type/family` 判——杠铃标的的档位以杠铃配置为准（511260 曾被判「进攻」）。


## v925 补充（自选组合参数表 + 网格金额口径）

- **网格金额（ga，元/档）**：`cfg.pf[code].ga`。语义＝**每次网格触发买入多少钱**；与 `gs`（跌多少触发）相乘才是完整网格规则。默认取抽屉 `gridAmt`（¥500），逐只可改。
- **生效链路**：`btPF(code,cfg)` 返回 `ga`（custom 分支读 `cfg.pf[code].ga`，其余回落 `cfg.gridAmt`）→ `btRun` 网格段 `var _ga = (pfg.ga>0 ? pfg.ga : cfg.gridAmt)` → 用于 `gridOk` 余额判断与 `tryBuy(code,_ga,...)`。改 `cfg.gridAmt` 只影响没单填 ga 的标的。
- **仍为组合级、未逐只化**：备用金上限 `gridFund`、无风险利率 `rf`、本金 `budget`、起止日。
- **表格派生列**：`投入¥ = budget × w%`；`占投入% = ga / 投入¥`；`实测波动/最深回撤` 由 `btCuRef()` 从 `BT_CACHE` 现算（2017-05-07 起、日收益年化 252、峰谷回撤，货基 0，样本<30 给 —）。三者都**不落库**，随参数即时重算（`syncDerived`）。


## v926 补充（回测参数单一来源：组合级 ≠ 逐只级）

- **两层参数，各只有一个入口**：
  - **逐只级**（只对自选组合有意义）：`cfg.pf[code] = {w, bd, sl, gs, ga, on}` —— 权重% / 止盈带宽% / 止损% / 网格步长% / 网格金额¥/档 / 是否执行规则。编辑入口＝「标的与逐只参数」表的 12 列。
  - **组合级**（作用于整个组合）：`budget / start / end`（运行条）＋ `gridExt / gridFund / tgtAnn / ddBudget / rf / rebal / perFund`（表格上方「组合级参数」横条）。**这些不进逐只行**——它们对每只都一样，进表只会重复 N 遍。
- **id 复用约定**：组合级横条里的输入沿用 `btIn_gridFund / btIn_tgtAnn / ...` 这套 id。`go()` 用 `getElementById` 逐个读、document 级 `change` 委托按 `btIn_` 前缀触发 250ms 防抖 `__btGo`，所以**搬 DOM 位置不用改绑定**；代价是**同一 id 全页只能出现一次**，抽屉在 `pool=custom` 时必须不渲染这些 input（否则读到最后渲染的那个，值可能被空值带偏）。
- **抽屉条件渲染**：`pool=custom` → 只渲染建仓口径说明 + `btIn_pool` + 提示；被移走的全局兜底值（`gridStep/gridAmt/sl/band/watchW`）以 `type=hidden` 保留，因为 `btPF` 在逐只没填时会回落它们。`pool=barbell` → 完整抽屉（13 项）。
- **权重口径唯一化**：`customWMode` 在 `pool=custom` 下恒 `'manual'`。「等权」＝面板「等权重排」按钮把每只写成 1/N，不再有独立口径分支。


## v927 补充（自选组合参数表列序）

- **13 列（自上而下唯一口径）**：`基金名称 / 基金代码 / 档位 / 来源 / 权重% / 止盈带宽% / 止损% / 网格步长% / 网格金额¥/档 / 投入¥ / 实测波动·最深回撤 / 规则 / 操作`。
- **列身份**：名称格只放基金名（`esc(nm)`），代码格放 `sub`（6 位代码，非日频标的带「· 无日频」）；档位＝`pileTxt[x.pile]`（底仓/进攻/安全垫/对冲），来源＝`srcTxt[x.src]`（持仓/自选/杠铃）。这三格都是**只读派生**，不参与编辑。
- **联动三处必须同改**：`<thead>` 的 th 数量、`tbody tr` 的 td 数量、`tfoot td` 的 `colspan`（当前 13）。三者任一不同步，视觉上表现为表头错位或合计行留白。
- **编辑列定位**：仍靠 `data-pf="code" data-k="w|bd|sl|gs|ga|on"` 与 `data-cu-row="code"`，不靠 td 序号——所以重排列序不改任何事件绑定。

## v928–v932（2026-11-13，组合回测：滚动窗口 + 投入方式）

- **v928–v931 滚动窗口**：`btRoll(cfg, data)` 逐窗口 `cloneCfg` 后调 `btRun`；`btRollHtml(roll, S)` 渲染结论块 + B/C 矩阵 + 39 行明细（13 列，`min-width:980px`）。B 口径用 `_rollAvail` 白名单（只取进场时点已存在的杠铃标的，同档按 w 重归一）；C 口径固定 5 只长历史池。三处口径修正：货基按 `fund.isMoney` 放行（nav 恒 null）、相等判「平」（容差 0.05pct）、交易日历剔货基。
- **v932 投入方式**：
  - 入口：抽屉 `#btIn_investMode`（`lump|drip|base`）、`#btIn_baseRatio`、`#btIn_investPeriods`；`go()` 白名单校验后写入 `c.investMode/baseRatio/investPeriods` 并按 `fw2_bt_cfg_v1` 持久化。
  - 引擎：`_IV = {mode, periods, ratio}`（期数优先 `cfg.investPeriods`，否则 `(y1-y0)*12+(m1-m0)+1`）；`P.pos[code]` 增 `invested/dripDone/lastMo`、`P` 增 `invBase`；`tryBuy` 预算内买入累加 `invBase`；建仓段首期按模式、后续每月首投，对照侧（`B.pos`）同节奏。
  - **月首投点必须用 `_mfByCode[code][ym]`（逐标的当月第一个有净值的交易日）**，不能用全局日期并集的月首——货基元旦/节假日计提行会让权益标的整月跳过（实测 71 期只投 51 期）。
  - 分母＝`invested`（预算内 `invBase` ＋ 备用金 `gridUsed`）；`unused = budget - invBase` 只留在资产里、不进分子分母。收益率序列 `_vS = (pv - unused)/invested`，对照 `_vH = (Bv - bUnused)/bInv`，最大回撤从这两条序列上取。
  - 曲线：`(v - unused)/invested`（一次性仍 `v/budget`）。
  - 渲染回显：运行条 `#btRunSum` 显示投入方式与「已投＝预算内＋备用金／未投留现金」；明细说明 ⑤ 同步；② 说明在分批时改「对照同节奏」。
  - `cloneCfg(st, ed, avail, hold)` 的第 4 参用于按 `hold*12` 设期数，两处调用都要传 `h`，否则滚动窗口期数退回默认值。


### v933 补投与双口径回撤

- `_perOf(df)`：期数＝该标的可投月数（`max(start, dataFrom)` → `end`）；`_IV.explicit > 0` 时直接用 `_IV.periods`。首期 `amt/_perOf(...)`、后续 `perN = base ? max(1,pc-1) : pc`、循环条件 `dripDone < pc`。
- 全预算回撤：`stats.strat.mddFull = maxDD(curve.map(x=>x.v))`，与 `strat.mdd`（已投口径）并列；一次性两者相同。
- 结论条仅在 `S.dripMode !== 'lump'` 时显示括号内的全预算对照。


### v934 年线信号联动（C 组第一段：破 MA200 减半 / 破 MA20 清仓，T+1）

- **入口**：抽屉 `chk('sigYear')` → `go()` 写 `c.sigYear`（布尔）＋ `c.sigMa=200`；`btCfg()` 默认 `sigYear:false / sigMa:200`，并在合并存量配置后做**布尔归一化**（`d.sigYear === true || d.sigYear === 'true'`，防止手工改库把字符串 `'false'` 判成开）。
- **参数对象**：`btRun` 顶部 `_SG = { on, maL:200, maS:20, cut:0.5, warm:260 }`。`on=false` 时以下所有分支都不进入 → v933 口径逐位不变。
- **取数与预热**：`_rowsAll = rowsByCode[code].filter(r => r.d <= end)`；`rows = _rowsAll.filter(r => r.d >= start)`；建 `seq` 用 `_rowsAll.filter(r => r.d < start).slice(-260).concat(rows)`。**`allDays` 仍只吃 `rows`** —— 区间、曲线、分母不变；预热只服务均线（P54）。
- **均线预计算**：`seriesBy[c].ma = { [d]: {l, s} }`，用前缀和 `_sum[n]-_sum[n-200]` 求 MA200、`_sum[n]-_sum[n-20]` 求 MA20，`n < 窗口` 时置 `null`。O(n)，39 个滚动窗口 × 80 只也只多几毫秒。货基 `nav` 恒 1 → MA 恒 1，永不触发。
- **状态机**：`P.pos[code]` 增 `maSt`（1 正常 / 0 破 MA200 / −1 破 MA20）、`maPend`（待执行指令）、`sigOff`（已信号清仓）。**建仓当日按当天位置记 `maSt` 初值**，否则「入场即破线」会被当成刚跌破，买完次日就清仓。
- **T+1**：判定在每日循环末尾（网格/止盈之后、`btRebalance` 之前），只写 `pp.maPend`；执行在**下一交易日循环开头**（更新 `lastNav` 之后）按当日 `nav` 成交，流水 type 记 `年线减半` / `年线清仓`。跌破 MA20 直接 `'exit'`（不再先 `'half'`），回升不自动补回。
- **联动抑制**：网格买入加 `&& (!_SG.on || pp.maSt > 0)`；定投段 `_sigMute = _SG.on && (pp.sigOff || pp.maSt <= 0)` 只压策略侧，**对照片区照常**（保持「同节奏、不同规则」可比）。
- **渲染**：结论条追加一行「年线信号（C1）：MA200 … 触发 X 笔减半 / Y 笔清仓…」；`#btRunSum` 追加「· 年线信号 开（…）」；明细「差异归因」列补 `年线清仓×N` / `年线减半×N`（原先不认这两个 type，会显示「买入后未操作」）；滚动窗口卡追加「信号开时 39 窗同样带信号、不可与关闭时横比」。
- **stats**：`sigOn / sigMa / sigMaS / sigHalf / sigExit`。**注意 IIFE 必须写 `()`**——`sigExit: (function(){…})` 少一对调用括号，`check_js` 照样通过，但页面会把函数源码当数字打印（P56）。
- **实测口径**：一次性 关 0.55%/−0.11/47.89% → 开 0.29%/−0.24/27.47%；定投 71 期 开 0.76%/−0.08/49.73%（已投 ¥22,449.30、未投 ¥30,050.70、全预算最深回撤 −2.44%）。
- **已知缺陷**：`511260` 十年国债 2021-01-29 被 MA20 清仓且不回补，策略 +0.24% vs 对照 +22.97%（P55，待拍板豁免方式）。


---

> **文档恢复说明（2026-11-27 16:30）**：本文件在本轮编辑中曾被误覆盖为 4 KB 残片；已从 `D:\Temp\FRONTEND.md.bak_v1055pre`（73,139 B / 509 行）恢复 §1–§9 与 v1055 前内容。v1056–v1155 的 §10.x 明细暂缺（约 1,300 行），本节之后只补当前架构摘要与 v1156 新模块；历史章节需从备份或 README/INBOX 逐版补回，未补回前不要把本文件当作 v1056–v1155 的唯一真源。

## §10.46 v1056–v1155 变更索引（2026-11-27 从 README 重建，非原文）

> 说明：本节不是原 §10.16–§10.48 全文，而是按 README「当前进度」逐版条目提取的一行索引，供接手者定位版本与主题；详细实现仍以 README 对应条目和代码为准。索引按版本从新到旧排列。

- **v1155** · 2026-11-27 · v1155 第 3 项：标的池统一为「发现层」
- **v1154** · 2026-11-27 · v1154 第 2 项：策略工厂 v1（波动率目标 / 趋势跟踪，已发布）
- **v1153** · 2026-11-27 · v1153 012920 复盘改进第 1 项：T2b 条件化峰值回撤止盈 + T17 单只超配削峰
- **v1152** · 2026-11-27 · v1152 数据债第 1 项
- **v1151** · 2026-11-27 · v1151 P2-9 回撤账本补记 + JSON 导入
- **v1150** · 2026-11-27 · v1150 P2-9 实际回撤按 A+ 接执行层
- **v1149** · 2026-11-27 · v1149 P2-9 压力 20pp 接进买入冻结（历史；实际回撤已由 v1150 按 A+ 补接，见上条）
- **v1148** · 2026-11-27 · v1148 P2-11 三条边界收口
- **v1147** · 2026-11-27 · v1147 P2-11 从只读卡接成真正买入过滤
- **v1146** · 2026-11-27 · v1146 P2-11 终止风险闸门第一段只读卡
- **v1145** · 2026-11-27 · v1145 P2-9 单只 20% 接执行层
- **v1144** · 2026-11-26 · v1144 P2-9 组合风险闸门只读卡
- **v1143** · 2026-11-26 · v1143 012920 份额对账收口 + 活期宝按底层货基拆行
- **v1142** · 2026-11-26 · v1142 R2 定投保持关 + RB/BW/L1/TREND 只作手动参考
- **v1141** · 2026-11-26 · v1141 审计 P1：估值缺数据降级 + 证据分级 + 负边际移出生效叙事
- **v1140** · 2026-11-26 · v1140 ERP 固定 3% 口径
- **v1139** · 2026-11-26 · v1139 执行清单阶段2.4：今日待办 Top5
- **v1138** · 2026-11-26 · v1138 执行清单阶段2.3：按信号类型 SLA
- **v1137** · 2026-11-26 · v1137 执行清单阶段2.2：同日冲突优先级
- **v1136** · 2026-11-26 · v1136 执行清单阶段2.1：交易信号 act 四态
- **v1135** · 2026-11-26 · v1135 预算迁移一次性守卫
- **v1134** · 2026-11-26 · v1134 资产配置表标题预算 62,000→50,000
- **v1133** · 2026-11-26 · v1133 执行清单阶段1收口
- **v1129** · 2026-11-26 · v1129「我的持仓」新增账户口径对账卡
- **v1128** · 2026-11-26 · v1128 持仓信号隐藏活期宝等现金/货币基金兜底
- **v1127** · 2026-11-26 · v1127 持仓信号按持仓市值降序
- **v1126** · 2026-11-26 · v1126 宏观数据补丁
- **v1125** · 2026-11-26 · v1125 配置回测 V11 狙击筛选池加载时序
- **v1124** · 2026-11-26 · v1124 接手复核（文档轨，未改代码/数据、未重新发布）
- **v1123** · v1123 交接文件
- **v1122** · v1122：V11 赔率公式统一
- **v1121** · v1121：V11 狙击补运行回测 + KPI 压成 5 列 + 赔率门限统一 2.50
- **v1120** · v1120：交易信号页删除 V11 逐只执行行（2026-11-25，已发布 master `b3e2261f8c5c` / index 5,336,202 B / SHA256 `BC86EFD7A…
- **v1119** · v1119：V11 狙击从「交易信号」迁入「策略执行」（2026-11-25，已发布 master `2389e776e324` / index 5,338,041 B / SHA256 `7DAC3…
- **v1118** · v1118：5 万策略口径写进页面文案
- **v1117** · v1117：深跌买入出厂默认改为 10 万 / 每档 5,000
- **v1116** · v1116：801862 终止样本接入 2016+ 全池对照
- **v1115** · v1115：深跌买入接入「已终止指数 · 幸存者偏差校正」卡
- **v1114** · v1114：801862 补齐全历史日线与终止前 100 只最终名单；OMX 补最终 12 只（index-term v2，2026-11-25；页面/前端未动，徽标仍 v1112）
- **v1113** · v1113：新增「已终止指数 + 历史成分」数据集（index-term v1，2026-11-25；页面/前端未动，徽标仍 v1112）
- **v1112** · v1112：深跌买入补「区间曾深」+ 全池59（逐日机会）
- **v1111** · v1111：深跌买入焦点只看接近 70% + 买入区前移 + 组合默认最深 10
- **v1110** · v1110：核算块默认折叠 + 跨档「今日/对比日」日期对齐
- **v1109** · v1109：胜率后补「赔率」
- **v1108** · v1108：补「投入资金口径」——投入资金收益率 + 资金加权年化（XIRR）
- **v1107** · v1107：回测结果下方补每个指标的核算过程
- **v1106** · v1106：回测结果紧跟「档位回测」
- **v1105** · v1105：深跌买入显示顺序（方案 A，2026-11-24，index 5,283,743 B；数据未动）
- **v1104** · v1104：深跌买入六项全做
- **v1103** · v1103：子页签更名「深跌买入」
- **v1102** · v1102：分档股息率中位 + 便宜又深交集 + 距下档排序 + 窄屏紧凑列 + 预取骨架屏
- **v1101** · v1101：分档汇总加 PE 分位最低 + 组合池只选回撤最深 10 + 回撤表头点击排序
- **v1100** · v1100：分档汇总表 + 只选便宜一半 + 相对同类三态排序
- **v1099** · v1099：组合池按类别批量 + 估值「相对同类」列 + 跨档卡跟随类别
- **v1098** · v1098：快捷「距下档 ≤2pp」筛选 + 对照表 8 列 + 方案卡跟随排序
- **v1097** · v1097：监测卡「排序」开关 + 估值卡「同类别对照」
- **v1096** · v1096：先证伪三条补源路，再补两处可用性
- **v1089** · v1089：估值卡升 PE/PB 双分位 + 新增「今日跨档提醒」
- **v1088** · v1088：回撤档位新增「估值参考」卡
- **v1087** · v1087：回撤档位新增「多指数组合（共享资金池）」回测
- **v1086** · v1095：全指数 45 → 63 只（补境外 4 + 补齐 14 只 A 股）+ 估值卡全列
- **v1079** · v1080：资产配置「定投金额（月）／累计应投」改计划口径
- **v1078** · v1078：① 选品层 × 筛选规则口径统一（B 方案，2026-11-24，index 5,143,575 B，SHA256 `f799300eb1ae77b882f4e877fb25f70f45b…
- **v1077** · v1077：全量数据刷新 + 三处对比度与一处断言修正
- **v1076** · v1076：总纲五项冲突修复
- **v1069** · v1073：目标 4 行列序修正
- **v1068** · v1068：总纲「信号阈值（纲领）」入口挪到 ⑧ 准入规则之后
- **v1067** · v1067 · T10 开关：关 → 生效
- **v1066** · v1066：信号阈值（纲领）＝总纲内「独立入口 + 独立子视图」（方案 B，2026-11-23，index 5,102,781 B，SHA256 `6887474E79EE4B627225E3CB2…
- **v1059** · v1059：纲领与实验拆成两套——总纲三键独立存储、参数页恢复可编辑、页面去掉「母版」
- **v1058** · v1060：一次性迁移旧纲领值 + 清掉 tgGotoCard 死代码
- **v1057** · v1057：投资总纲改名后的可见文案一致性收尾
- **v1056** · v1056：投资逻辑升为独立一级模块「投资总纲」，回测参数迁回策略执行

## §10.49 v1156 网格计划独立化 + 核心-卫星边界（2026-11-27）

**位置与入口**：策略执行第 9 个页签 `data-st="gd">网格计划`，面板 `#stp-gd`，排在「策略工厂」之后、「月度复盘」之前。

**为什么独立**：网格是震荡市叠加工具，不是核心-卫星之外的第三套仓；四档杠铃 40/35/10/15 已承担核心-卫星，不再另建卫星仓。V11 狙击 / 深跌买入是卫星策略，各自独立预算。网格预算独立，但网格买入的份额市值仍计入所在桶的实际占比，不做份额级拆分——「预算独立」不等于「市值不计入」。

**配置存储**：`localStorage.fw2_grid_plan_v1`，结构 `{ver:'v1',updatedAt,funds:{code6:{on,step,amt,cap,src}}}`。`step` 1–20（默认3）、`amt` 0–100000（默认500）、`cap` 0–10000000（默认10000）、`src=1` 为可用备用金，否则预算内；`on` 缺省为开。只存配置，不写流水/持仓/交易状态；`gdReset` 恢复单只全局，`gdResetAll` 清空全部。v1157 起「已用金额」改读 `window.HOLDINGS_SEED.gridUsage`（ttskill `TRADE_QUERY` 买入成交流水聚合，窗口 2024-01-01 起），无数据才显示「已用 —（成交流水未载入）」。

**前端实现**：`gdGlobal / gdRead / gdWrite / gdHydrate / gdNum / gdCfgOf / gdSave / gdReset / gdResetAll / gdRole / gdMoney / gdCardsHtml / gdRender` 在 `var __stratPaneDone` 之前，不新增 window 键。`gdHydrate()` 进策略页时把 localStorage 配置写入 `C.grid.pf`；`gdRender()` 才重画。卡片按非现金持仓生成（当前 22 只），显示角色、步进/单笔/上限/资金来源、下次触发价、基准、距触发、可买档数；KPI 为已启用/合计上限/核心卫星叠加/计划外，全部现算。

**T13 接入**：`signalEvalAll` 内 `_gpf=(C.grid&&C.grid.pf&&C.grid.pf[code6])||{}`；`_gStep/_gOn/_gAmt/_gFund/_gExt` 逐只取值，未配置回落 `SIGNALS_CFG.grid`；v1157 起关闭仍 push 一行 `T13 网格跟踪`，`cur=已关闭`、`thr=梯度参考 → 已关闭`、`lvl=watch`，行动为「【不动】已关闭，不生成网格买入；恢复时在「网格计划」勾选启用」；开启才按逐只步进生成正常行。文案「（经验阈值未回测）」改为「（逐只计划）」。分母仍是 `lastBuyNav`，不是单位成本。

**顺带修复**：投资总纲「变更记录」不再渲染 `undefined undefined→`；`_logT` 对字符串直接返回，无 `x.id` 只显示 `x.t`，有 id 才拼 `x.t + ' ' + x.id + '→' + 状态`。

**窄屏**：`#stratTabs` 媒体查询必须 `repeat(9,minmax(0,1fr))`、gap 3px、字号 9.5px、padding 7px 1px；写成 `repeat(8,…)` 第 9 个页签会掉第二行。

**验收**：本地/线上 538 均 9 页签单行；22 张卡、`docW=529/cliW=529`、无横向溢出；012920 步进 3% 时「还需跌 12.40% / 触发价 ¥2.6465 / 基准 ¥2.7283 / 可买 20 档」。实测改 5% 后触发价 ¥2.5919、T13 变「距上次买入跌 5% / 还需跌 14.0%」并落观察组（默认折叠不是行丢失），恢复后回 3%。`check_js` ALL OK、`check_html_comments` 375 处 0 隐患、`check_globals` PASS（282 键/432 赋值点）、`check_hold_consistency` PASS=9 WARN=2 FAIL=0、`verify_manifest` PASS、`_audit_dm_v845` FAIL=False、`_audit_plan_merge_v895` 42/42 PASS（A01 扩 9 tab + A01g）。

**别碰**：不要猜已用金额（只认 `gridUsage` 成交流水）；不要把预算独立说成市值不计入；不要把网格当第三套仓；不要新增 window 顶层键；改 tab 列数必须同步媒体查询。

## §10.50 策略执行页与信号执行链（v1136–v1156 当前态）

**策略执行页签**：`#stratTabs` 现役 9 个，顺序为资产配置 / 配置回测 / 自选回测 / 回测参数（母版）/ 深跌买入 / V11 狙击 / 策略工厂 / 网格计划 / 月度复盘。`data-st` 分别为 `alloc / bt(pool=strategy) / bt(pool=custom) / param / dd / v11 / sf / gd / review`；`__stratActiveTab` 白名单、`__stratPaneRender` 分支、`switchStratTab` 重画名单三处必须同步，少一处就点进去空白或切回不重画。面板容器 `#stp-alloc / #stp-bt / #stp-param / #stp-dd / #stp-v11 / #stp-sf / #stp-gd / #stp-review`；`renderStrategyView()` 进入页时先 `gdHydrate()`（v1156），再按 active tab 渲染。

**信号表列**：持仓/自选/筛选/市场统一 9 列——信号 / 当前值 / 阈值 / 状态 / 执行 / 行动方案 / 数据日 / 来源 / 操作；表内 `min-width:1180px`，但 `.dc-card / .dc-body / .sig-wt-area` 必须 `min-width:0`、`.table-wrap` 必须 `max-width:100%`，否则 538 视口执行/行动/操作列不可达。

**act 四态**：`fw2_act_state_v1`，键 `pool:code:信号名`，值 `{st,at,upd,doingAt,doneAt}`；`pending → doing → done`，条件不再触发才 `expired`。已执行保留 45 天，过期记录保留 14 天；`actStateSync` 只对 `lvl==='act'` 建状态，不能在 `signalEvalAll` 里写状态。

**同日冲突**：`ACT_PRIO` 按 `sig.split(' ')[0]` 取规则码；T4 硬止损 / R6 硬止损 rank10 → T2 峰值回撤止盈20 → R7 再平衡30 → T1 阶梯止盈40 → T3 估值止盈45 → T16 卖出后破位减半50 → P2 单票暴露55 → TREND-DN/S-TREND 60 → T7/W2/S2 回撤补仓70 → T8 估值加仓75 → T13 网格跟踪/R3 网格买入80 → V11 狙击85；改信号代码首 token 必须同步改键，否则静默落 rank99。`actConflictMap` 按 `pool|code|name` 聚合，买入被更高 rank 且 `pending/doing` 的风控/拦截/卖出压制时，按钮 disabled 并显示「先 T4 硬止损」等中文名。

**按类型 SLA**：`ACT_SLA` 风控/卖出与拦截复核 T+1，网格/补仓/加仓 T+2，观察 T+5，季频/宏观 90 日，组合级不设；按周一至周五计，不含法定节假日。执行列只在 `pending/doing` 显示 SLA，`done/expired` 不显示也不计超时。

**今日待办 Top5**：`#todayTop5` 在 `#todayBand` 后、`#pfSrcNote` 前，`<details>` 默认收起，展开态 `fw2_tt5_open='1'`；`todayTop5Data()` 只收 6 位基金代码 + `lvl==='act'` + 非 `padRow`，排除 `done/expired`，按 `code|sig` 去重优先持仓，再用同日冲突；排序 `ACT_PRIO` → SLA（over > due > 正常）→ 日龄降序 → doing 优先 → 池优先级。卡片点击切 `showView('signal')`，筛选池切 `data-sigtab="screen"`、其余 `hold`；目标行 `data-sigkey` 加 `sig-row-hit` 1.8s，700ms 后要复查 DOM 是否被重写。

## §10.51 P2 组合风险闸门（v1144–v1151 当前态）

**位置**：`#hdP2Gate` 在 `#hdRecon` 后、`#hdTermGate` 前；`renderHoldP2Gate()` 由 `renderHoldings()` 在 `renderHoldRecon()` 后调用。四格＝单只 / 压力 / 实际回撤 / 回撤账本；≤980px 两列、≤520px 单列。`.hold-p2 .hr-grid` 必须自带 `display:grid`（只写 `.hold-recon .hr-grid` 不命中）。

**单只与压力**：`P2_GATE_CFG = {singleCap:20, stressPct:44.6, stressCap:20, ddFreeze:15, ddReview:20}`；`holdP2GateData()` 取最大非现金持仓（排除 `assetType='cash'`），集中度分母为确认份额×净值的决策权重。`p2BuyBlockOf(d,code)` 只在 `code === d.top.code` 且 `conc>20` 或 `stressPp>20` 时冻结该只买入，返回 `{conc,stressPp,flags}`；**只冻最大单只，不扩全组合**。函数必须挂 `window.SIGNALS_CFG.p2GateData / p2BuyBlockOf`，跨 IIFE 裸调用会被 try/catch 吞成静默 false。

**实际回撤 A+**：`P2_DD_CFG={minDays:20,key:'fw2_p2_dd_v1',flowKey:'fw2_p2_dd_flows_v1'}`；`_p2AsOfDate()` 取 `state._pfAt`（不是系统日期）；`_p2DdState` 按数据日去重、首日建基准；`_p2DdRecalc` 按日期升序算 `HWM=max(HWM_prev+净出入金, 总资产)`、`dd=总资产/HWM−1`；基准日不应用当日出入金。前 20 个数据日只读；满 20 后 −15% 全组合新增买入冻结、−20% 减仓评估。账本只存本机 localStorage，只记银行卡↔账户，基金内部申赎/转换不算外部现金流。补记只允许 `baseDate < date <= 今天`，同日覆盖；导入 `fw2_p2_portfolio_risk_v1`，基准日不后移、基准日前快照忽略、出入金按 id 去重。

**信号页表现**：`_p2Gate()` 整页缓存一次，`_p2blk` 命中时执行列 disabled「开始」+ `.sig-exe-wait`「买入冻结」+ `.sig-cap-freeze` 徽标；`_waitTxt` 用「；」拼 P2-9 与 P2-11，双命中显示「2 条闸门」；`actPlan` 统一「【不动】买入冻结 · 不买入（原因）；卖出/拦截不碰」。**只提示/冻结买入，不自动卖、不写交易状态、不改 `signalEvalAll` 判定/阈值/三态。**

## §10.52 v1157 网格已用接流水 + 发现层六源 + 策略工厂 v2（2026-11-27）

**网格已用金额**：`edit_work/gen_grid_usage.py` 复用 `refresh_holdings_ttskill.ttskill_trade`，窗口 `2024-01-01` 起、`busType=1`、`statu=2`、`pageSize=500`；`totalCount>=500` 视为可能截断，保留旧值并 `ok=false`。只保留持仓内非现金基金，写入 `holdings-data.json` 顶层 `gridUsage={asOf,windowStart,source,ok,error,queryCount,skippedNoAmount,funds:{code:{buyCount,buyAmt,lastBuyDate}}}`，再调 `_sync_holdings_inline.py` 带入 `window.HOLDINGS_SEED`。不存 tradeId、卡号、token，不写下单或交易状态。2026-11-27 实跑 23 只 / 169 笔；012920 17 笔 ¥8,700，最近 2026-03-06。

**前端网格**：`gdUsage(code)` 优先读 `window.HOLDINGS_SEED.gridUsage`；`gdCardsHtml()` 的 `used/left`、可买档数、脚注全部按流水现算；脚注格式「已用 ¥x / 上限 ¥y · 剩余/已超 · 累计 N 笔、至日期」。

**T13 关闭行**：关闭不再跳过，push `sig:'T13 网格跟踪'`、`cur:'已关闭'`、`curSub:'逐只计划「启用」未勾选'`、`thr:'梯度参考 → 已关闭'`、`lvl:'watch'`、`src:'网格'`；不生成网格买入，恢复需回「网格计划」勾选启用。

**T2b/T17 定稿**：分母统一单只决策权重；超配先 T17 削峰再 T2b；T2b −10% 卖半、−15% 清剩余、破 MA200 也清剩余（不再「再卖半留 1/4」）；`SIGNAL_REGISTRY` 同步。

**发现层六源**：`gen_discovery.py` 新增持仓（`hold`，过滤货币/活期宝/现金，当前 24 只，含黄金 000307）与策略工厂候选（`sf`，`v11-bt-data.series` 15 只）。持仓 note 写明「已持有不重复买入；网格/止盈在交易信号页处理，份额市值仍计入所在桶」；工厂 note 写明「只做研究，不生成买卖指令」。`counts` 增 `hold/sf`，`meta.asOf` 取六源最大；2026-11-27 输出 160 条 / 去重 137 / 跨源 23。前端 chips 与脚注同步六源。

**自动链**：`refresh_all.py` 的 `SERIAL_AFTER` 在 `holdings` 后加 `('grid-usage', ['gen_grid_usage.py'])`，在 `hold-xmod` 后加 `('discovery', ['gen_discovery.py'])`。

**策略工厂 v2**：新增 `mom` 动量轮动（全池 Top N，`topn/look`）与 `port` 等权组合（全池月度再平衡）；`sfPortBacktest(D,cfg)` 用全池日线并集日历、t−1 信号、t 收盘成交、现金 2.25%/年、单边费 0.05%，基准为起点可用标的等权买入持有、不再平衡；`sfRun` 分派 `sfBacktest / sfPortBacktest`；`sfResultHtml` 组合级 KPI 8 项 + 曲线 + 对比表 + 期末权重 + 结论；`sfSens()` 扫 vol 3×3 / trend 3×3（fast<slow 过滤后 8 组）/ mom 3×3，按 Calmar 排序；`sfSave/sfSaved/sfApplyCfg/sfClear` 用 `localStorage.fw2_sf_last_v1` 存 `{savedAt,cfg,R}`，重载只恢复不重跑；`sfExport()` 下载 `sf-result-<strategy>-<to>.json`（只含 cfg/result/stats/benchmark）。

**实测**：动量 Top3/60 期末 ¥37,709 / −24.58% / MDD −56.66% / 107 次；等权组合 ¥98,512 / +97.02% / MDD −26.52% / 9 次；基准 +185.69% / 10.12% / −21.54%。敏感性 mom 最高 Top5/20 +127.34% / Calmar 0.26；trend 最高 fast20/slow300 +94.28% / Calmar 0.33。导出文件 191,818 B，`strategy=port`、`eq=2646`、`total=0.970246`。

**别碰**：`v11-bt-data` 的 `day` 换算与 `t−1/t` 成交时点；组合基准不是再平衡组合；localStorage 只存上次结果，不当跨设备同步；不接实盘/下单；发现层不接预算。

## §10.53 v1158 网格逐只起算日 + 策略工厂去前视（2026-11-27）

**网格起算日**：`GD_PLAN_START='2026-11-27'`（计划上线日）；`gdCfgOf(code).since` 优先读 `localStorage.fw2_grid_plan_v1.funds[code].since`，缺省用计划上线日。`gdUsage(code, since)` 只统计 `window.HOLDINGS_SEED.gridUsage.funds[code].buys` 中日期 ≥ since 的成功买入；没有 `buys` 的旧数据回退 `buyAmt/buyCount` 全窗并标 `approx=true`。卡片脚注「已用 / 上限 / 剩余 / 累计 N 笔 / 自 YYYY-MM-DD」全部按起算日现算；`data-gd-rebase` 按钮把该只 since 改成 `gdToday()`，只写配置、不动持仓/流水；`gdSave` 规则：从关闭重新打开且从未记过 since 才用今天，已有 since 不重置。012920 在默认起算日下应显示「¥0 / ¥10,000 / 0 笔 / 自 2026-11-27」，把 since 设到 2025-01-01 才显示 17 笔 ¥8,700（2026-03-06 止）。

**策略工厂去前视**：`sfPortBacktest` 的动量打分固定 `ii-1` 为前一交易日收盘、`ii-1-look` 为回看起点，当日收盘调仓；`ym=year*12+month` 防跨年同月误判。v1158 引入 `poolmode`；v1159 起默认 `fixed`：`fixed` 用 `startAvail`（起点已有价格的标的）；`pit` 仍可手动切，用 `allCodes`、标的上市后满足 `look+1` 根才可入选。基准始终是 `startAvail` 等权买入持有、不再平衡。结果头显示「池 N 只 · 固定起点池/当时可用池」。`sfSens` 原样继承 `poolmode`。

**v1158 实测（本地与线上同口径）**：动量 Top3/60 期末 ¥40,072 / −19.86% / 年化 −2.01% / MDD −55.77% / Calmar −0.04 / 均仓 99.2% / 106 次；基准 +185.69% / 10.12% / −21.54%。固定起点池（7 只）Top3/60 +59.52% / 4.38% / MDD −32.02% / Calmar 0.14 / 101 次。敏感性 9 组最高为 Top5/回看120日 +160.70% / 9.20% / MDD −29.87% / Calmar 0.31；Top3/60 仍为 −19.86%。旧 v1157 的 −24.58% / 107 次含同日收盘前视，不得再用。

**两处真 bug（v1156 遗留）**：①`switchStratTab` 的懒渲染白名单漏了 `gd`，点「网格计划」只切 `display` 不调 `gdRender`，面板高度 0；已补 `name === 'gd'`。②`?view=strategy` 首屏在策略脚本尚未执行时调用 `renderStrategyView()`，控制台报 `ReferenceError`；已在分派处 guard `typeof window.renderStrategyView === 'function'`，否则挂 `load` 一次性补渲染。

**别碰**：起算日只影响「已用」统计，不改历史成本、份额、T13 判定；`buys` 是逐笔日期/金额，不要再退回只有聚合字段；`pit/fixed` 只改候选池，不改基准；改 `sf-note` 文案前先确认所在函数作用域（该段在 `sfShellHtml`，不是 `sfResultHtml`，不能引用 `cfg`）。

## §10.54 v1159 策略工厂默认固定起点池（2026-11-27）

**默认**：`sfCfg` 的 `poolmode` 缺省由 `pit` 改 `fixed`；`sfShellHtml` 的 `data-sf="poolmode"` 选项 fixed 在前并 `selected`，文案「固定起点池（起点已有，默认）」，pit 仍可选。结果头 `sfResultHtml` 的 `poolTxt` 输出「池 N只 · 固定起点池/当时可用池」。

**旧缓存迁移**：`sfSave` 的 payload 增 `ver:'v1159'`；`sfRender` 恢复时，若旧缓存 `saved.ver !== 'v1159'` 且 `poolmode` 为 pit/缺省，则把 cfg 的 poolmode 改 fixed，并按同一组参数 `sfRun()` 重算一次，避免「表单默认 fixed、结果仍是当时可用池」；已带 ver 的手选 pit 结果正常恢复，不再被迁移。迁移只针对旧缓存，不删本机结果。

**口径未动**：`sfPortBacktest` 的 t−1 信号、当日收盘成交、费率 0.05%、现金 2.25%、基准 startAvail 等权买入持有、`sfSens` 继承 poolmode 全部保持 v1158 口径。fixed 池 7 只 Top3/60：¥79,758 / +59.52% / 年化 4.38% / MDD −32.02% / Calmar 0.14 / 101 次；pit 池 15 只仍 −19.86% / MDD −55.77%。fixed 仍取自当前候选池，存在幸存者偏差，页脚已写明。

**验收**：本地与线上 538 真渲染，表单默认「固定起点池（起点已有，默认）」、结果「池 7只 · 固定起点池」；手选 pit 后重载仍保留，证明迁移只针对旧缓存。

**别碰**：不要删 `ver` 条件（否则手选 pit 每次重载会被改回 fixed）；不要把 fixed 的 +59.52% 当无偏全样本；不要改 `sfPortBacktest` 的成交时点。

## §10.55 v1160 网格预算 A 保守方案 + 卡片过滤修复（2026-11-27）

**默认预设**：`GD_PRESET_MARK='fw2_grid_budget_6000_v1'`、`GD_PRESET` 七只——`012920:1,500`、`001015 / 160422 / 000307:1,000`、`022438 / 012761 / 023917:500`；step 3、amt 500、src 0（预算内）。其余持仓默认 `on:false`，卡上显示「默认关闭」。合计上限 6,000，一次全触发 7×500＝3,500；`gdCashSum()` 从 `HOLDINGS_SEED.holdings` 的 `assetType='cash'` 汇总现金，当前 7,720.80。

**迁移**：`gdHydrate()` 先 `gdMigratePreset(gdRead())`；标记不存在时把七只写入 `fw2_grid_plan_v1.funds`（已有 `since` 保留，否则 `GD_PLAN_START=2026-11-27`），其余已有配置 `on:false` 且 `cap` 清 0，然后写标记。只改配置，不动持仓/流水/交易状态；「全部恢复默认」清空 `funds` 后，`gdCfgOf` 仍按预设返回，页面保持 7 只 / 6,000。

**读取**：`gdCfgOf(code)` 先读 `localStorage.funds[code]`，缺省按 `GD_PRESET`；未知标的 `on:false`、`cap:0`；返回 `preset/custom` 供脚注显示「= 默认配置 / = 默认关闭」。`window.SIGNALS_CFG.gridCfgOf = gdCfgOf` 不新增顶层键；T13 段 `_gCfgR` 优先读它，避免「网格页关闭、信号页仍按全局 10,000 生成」。

**卡片过滤（本轮修复）**：旧 `gdCardsHtml`/`gdRender` 用 `/货币|活期宝|现金/` 与 `status==='off'`，导致两个真持仓被吞——023917 名称「华夏国证自由现金流」被「现金」命中；012761/023917 台账 `status=off` 但账户镜像仍有份额，被整卡隐藏，页面只剩 5/22、5,000。新增 `gdIsCashRow(r)`：现金只认 `r.assetType`/`r._h.assetType==='cash'` 或 `cat==='现金'`，名称只认「活期宝 / 货币基金 / 现金宝」；`gdIsGridRow(r)`：`status==='off'` 仅当份额与市值都为 0 才排除。两个函数在 `gdCardsHtml` 与 `gdRender` 共用；页面 24 卡、7 启用。

**KPI/文案**：第 3 格「一次全触发」＝启用只 `Σ min(amt,cap)`；第 4 格「计划外标的」按角色统计；页头写「默认只开 7 只、合计上限 ¥6,000；其余默认关闭。当前启用 N 只，一次全触发 ¥X；现金 ¥Y。上限不是预算，执行前按现金复核。」「全部恢复默认」确认文案改为「默认预设（7 只 / 合计上限 ¥6,000，其余关闭）」。

**实测**：本地/线上 538 均「7 / 24」「¥6,000」「¥3,500」「计划外 14」，7 个勾选码与预设一致；012920 取消勾选→6 / ¥4,500，再勾→7 / ¥6,000；「全部恢复默认」后仍 7 / ¥6,000；T13 线上 7 只带「预算内（逐只计划）」，4 只「已关闭」，012761/023917 有行。`check_js` 22 块 ALL OK、`check_html_comments` 379 处 0 隐患、`check_globals` PASS（282 键 / 434 赋值点）、`verify_sync --gh-only` PASS（5,626,939 B）。

## §10.56 v1161 波动率只读监控 + 首屏预警（2026-11-27）

**位置与入口**：`#volCard`（约 L1974）保留 v699 的 20 日滚动组合 vs 沪深300，新增 `#volKpi`（60/120/250 日 KPI + 参考带）、`#volRisk`（120 日风险贡献 Top5）、`#volFoot`；`#hdSummary` 之后新增 `#volTopAlert`，仅当任一窗口 ≥`VOL_WARN=10` 显示，点击平滑滚到 `#volCard`。徽标 `v1161`，tags `fw2_v1161_vol_monitor` / `fw2_v1161_vol_top`。

**参数**：`WIN=20`、`WINS=[60,120,250]`、`VOL_WARN=10`、`VOL_HIGH=15`、`RC_WIN=120`；`annVolOf(rmap,win)` 取最后 N 个日收益样本 std × √252；`band(v)` 返回「正常/预警/高位」，`bandColor(v)` 只用于着色。10%/15% 是监控参考带，不是交易阈值。

**总资产口径（本版关键修正）**：`portWeights` 每行增 `isCash=h.assetType==='cash'`；`portReturns` 先收集所有净值日，现金行在每个净值日加 `w*0` 与 `w`，非现金仍按自身日历加收益/权重，最后按 `a.w` 归一。这样 37.6% 现金不再被漏掉，60/120/250 是「总资产」年化波动，不是「非现金部分」波动。`pr` 用于 KPI 与 20 日曲线；另有 `prNC=portReturns(非现金)` 只供风险贡献。

**风险贡献**：`riskContribs(wrows, serMap, prNC)` 用 120 日协方差近似，`贡献_i = w_i·cov(r_i,r_p)/(var_p·Σw)`，`wrows` 只传非现金、`Σw` 为非现金权重和，贡献合计 100%；按绝对值降序取 Top5。当前 012920 63.6%（权重 26.1%、单只波动 45.1%），160422 14.1%、001015 10.7%、022438 2.3%、022676 2.1%。

**覆盖率**：`CACHE.meta.cov = inc/ncTotal`，`inc` 为有 ≥2 点净值序列的非现金市值，`ncTotal` 为非现金总市值；`cashW` 为现金/总资产。**不要再用 `inc/W.total`**：现金有序列时会把覆盖率抬到 100%，没序列时又只剩 62.4%，且会把「非现金覆盖」误标成总覆盖。页脚固定写「非现金净值覆盖 X%；现金 Y% 按 0 波动计入」。

**实测（本地/线上 538）**：20 日组合 13.03% vs 沪深300 14.36%；60/120/250＝12.00% / 17.98% / 15.31%；非现金净值覆盖 100%；现金 37.6%；净值截至 2026-11-25、沪深300 截至 2026-11-25、权重快照 2026-11-26 22:05。首屏预警与页底三格一致；538 无横向溢出，参考带换行完整。

**闸门**：`check_js` 22 块 ALL OK、`check_html_comments` 382 处 0 隐患、`check_globals` PASS（282 键 / 434 赋值点、新增 0/消失 0）、`check_hold_consistency` PASS=9 WARN=2 FAIL=0、`verify_manifest` PASS（43 数据集 / 1 项 W2）、`_audit_plan_merge_v895` 42/42 PASS；`push_gh_v39.py`（`SKIP_GATE=1`）只 `[200] caifu/index.html`（5,635,501 B）。

**别碰**：`assetType==='cash'` 的 0 波动总资产口径；`riskContribs` 的非现金分母；10%/15% 只展示语义；不要接 P2-9/P2-11、网格或任何交易冻结；不要把非现金波动 0.624 倍后的数当总资产波动，也不要把总资产波动再乘 0.624。

## §10.57 v1162 012920 减仓 what-if（2026-11-27）

**位置**：`#volCard` 内 `#volRisk` 与 `#volFoot` 之间新增 `#volWhatIf`（约 L1982）；标题「012920 易方达全球成长精选混合(QDII)人民币A · 减仓 what-if（按总资产权重含现金；只算不改仓）」。徽标 `v1162`，tag `fw2_v1162_vol_whatif`（内部修正 `v1162b`）。

**函数**：`volWhatIf(W, ser)` 在 `riskContribs` 之后，复用 `portReturns` / `annVolOf`；目标 `[0.20,0.15,0]`，`delta=curW-t`，`sell=delta*W.total`，克隆 `W.rows` 后把 012920 权重设为 `t`、把卖出权重加到第一条现金行；不写死金额。`CACHE.wi` 在 `loadData` 的 `done` 内赋值；`draw()` 在 `#volRisk` 后渲染三行，每行 `display:flex;flex-wrap:wrap`，每个窗口一个 `white-space:nowrap` span，防 538 视口单字断行。

**口径**：卖出款全部转现金、不买入、不改其他仓位；目标是**总资产权重（含现金）**，不是决策权重。当前权重 26.1%：降到 20% 卖约 ¥1,252、15% 约 ¥2,279、清仓约 ¥5,361；对应 60/120/250 日年化 10.52/15.33/13.10、9.34/13.19/11.32、6.15/7.20/6.51；当前 KPI 仍 12.00/17.98/15.31。

**v1162b 修正**：`portReturns` 的 `allDs` 跳过 `isCash` 行，估值日只取非现金净值日；现金在这些日期按 0 波动计入。若把货币基金自身日历（000912 含周末 4,114 个日期）并入 `allDs`，清仓 what-if 会从 6.15/7.20/6.51 变成 5.69/5.09/5.80，线上与本地读数分叉；20%/15% 两档因 012920 仍有收益，差异被掩盖。

**实测（线上 538）**：`#volWhatIf` 483×129、`scrollWidth=483`；`body 529/529`、`vw=538`，无横向溢出；标题两行完整、无单字断行；页脚「假设卖出款全部转现金、不买入、不改其他仓位；只用于风险测算，不构成卖出建议」可见。

**闸门**：`check_js` 22 块 ALL OK、`check_html_comments` 383 处 0 隐患、`check_globals` PASS（282 键 / 434 赋值点、新增 0/消失 0）、`check_hold_consistency` PASS=9 WARN=2 FAIL=0、`verify_manifest` PASS（43 数据集 / 1 项 W2）、`_audit_plan_merge_v895` 42/42 PASS；`push_gh_v39.py`（`SKIP_GATE=1`）只 `[200] caifu/index.html`（5,639,329 B），master `5cbe34f51827`。

**别碰**：不要改回并入现金日历的 `allDs`；不要把 what-if 说成卖出建议或自动减仓；10%/15% 仍只展示；不要接 P2-9/P2-11、网格、回测或任何交易冻结；`riskContribs` 仍是非现金方差近似，不是严格风险分解。

## §10.58 v1163 波动率上限 20% + 收益目标 10%（2026-11-27）

**背景**：用户把风险口径说清——「年化收益率目标 10%，波动率 20% 以内」。v1161 的 10%/15% 原本只是展示参考带，不是收益目标；本版把卡内阈值改成 **20% 监控上限**，并把 10% 明确归到投资总纲收益目标，不再混作波动率线。徽标 `v1163`，tag `fw2_v1163_vol_cap20`。

**参数**：`WINS=[60,120,250]`、`VOL_CAP=20`、`RC_WIN=120`（约 L38757）；`VOL_WARN=10` / `VOL_HIGH=15` 删除。`band(v)` / `bandColor(v)` / `chip(v)` 改二元：`v>=VOL_CAP` → 「超上限」红色，否则「正常」绿色。

**首屏**：`#volTopAlert` 仅当 `Math.max(vol60,vol120,vol250)>=VOL_CAP` 时 `display:flex`，文案「组合波动率超 20% 上限」；当前最高 17.98%，因此隐藏。

**KPI / 页脚**：`#volKpi` 底部动态行由 `window.tgThesis()` 的 `tgtAnn`（默认 10）拼出「年化收益目标 10%（投资总纲，非本卡指标）」；前半句按最高窗口实时算「20% 上限内，最高 120日 17.98%（距上限 2.02pct）」。`#volFoot` 固定写「波动率上限 20%（用户 2026-11-27 设定，只读监控，不冻结买入）；年化收益目标 10%（投资总纲，非本卡指标）……20% 是监控上限，未接买入冻结/交易闸门」。

**未改**：`volWhatIf` 三档目标 `[0.20,0.15,0]` 与卖出额现算逻辑不变；`portReturns` 估值日仍只取非现金净值日、现金按 0 波动；`riskContribs` 仍以非现金方差为分母；what-if 三档只是颜色改按 20% 判断，数值仍 10.52/15.33/13.10、9.34/13.19/11.32、6.15/7.20/6.51。

**实测（线上 538）**：徽标 v1163；60/120/250＝12.00/17.98/15.31，三格全绿「正常」；20 日 13.03 vs 沪深300 14.36；Top5 012920 63.6% / 160422 14.1% / 001015 10.7%；首屏超限条 `display:none`；KPI 两行完整、页脚完整；`body 529/529`、无横向溢出。

**闸门**：`check_js` 22 块 ALL OK、`check_html_comments` 385 处 0 隐患、`check_globals` PASS（282 键 / 435 赋值点）、`check_hold_consistency` PASS=9 WARN=2 FAIL=0、`verify_manifest` PASS（43 数据集 / 1 项 W2）、`_audit_plan_merge_v895` 42/42 PASS；`push_gh_v39.py`（`SKIP_GATE=1`）只 `[200] caifu/index.html`（5,640,791 B），master `deb8fd924458`，raw 与本地 SHA256 逐字节一致 `6A21EF32DBC545D57F325EFEC684027B2E3E9E8A3FB81DA8185417AE39BEDF96`。

**别碰**：20% 只是监控上限，不要当买入冻结；10% 是投资总纲收益目标，不要写成波动率线；`tgThesis` 的 `ddBudget=20` 是回撤预算，不要和波动率上限合并；`VOL_CAP` 仍是前端常量，未进 `fw2_tg_thesis`。

## §10.59 v1164 20% 进总纲 + 波动率卡展示实际年化（2026-11-27）

**背景**：用户对 v1163 的三个待决项逐项选择「1、暂时只监控 2、放入总纲 3、展示组合实际年化收益」。本版不接买入冻结，只把 20% 变成投资总纲可编辑配置，并把卡首行从「只显示 10% 目标」改成「账户实际年化 + 目标对比」。

**上限配置化**：`VOL_CAP` 硬编码改为 `VOL_CAP_DEF=20`（约 L38777），实际值在 `draw()` 内直接读 `localStorage.fw2_tg_thesis.volCap`（默认 20），不依赖 `window.tgThesis`——总纲模块在持仓视图未渲染时不会挂全局；坏 JSON/缺字段回退 20。`#volTopAlert`、三格 `band/chip`、`#volKpi` 的 capTxt 与 `#volFoot` 全部改用这个 `volCap`，不再读常量。

**总纲四键**：`TG_THESIS_DEF` 由 `{tgtAnn:10, ddBudget:20, rf:1.59}` 改为 `{tgtAnn:10, ddBudget:20, volCap:20, rf:1.59}`；`tgThesis()` 白名单加 `volCap`；`tgMigrateOnce()` 对已有 `fw2_tg_thesis` 缺 `volCap` 幂等回填 20，旧 `fw2_bt_plan` 迁移也写入 `volCap:20`；`tgPlanEdit` 允许 `volCap`，范围 **1–80**，改动后 `setTimeout(window.__vol699Render,0)` 触发波动率卡重绘。总纲阈值表 `TGT.n` 4→5、`sub` 3→4，`_tgtRows` 在回撤预算与无风险利率之间新增「波动率上限 / volCap / 20 / 1–80」；表头「26 项可改 + 1 项已下线 · 28 行」、第 1 组「4 项」、数据管理「27 项 / 4 目标 / 四键」、总纲卡「波动率上限 ≤N%」chip、按钮「这四个数」、规则表脚注同步。

**实际年化口径**：新增 `actualRetOf(W, asOf)`（约 L38893），用账户权威 `holdProfit` / `cost`，`cum = ΣholdProfit / Σcost`，按首笔买入到最新净值的日历天 `365.25/days` 折算；`portWeights` 增 `cost/profit/firstBuyDate` 汇总；`CACHE.meta.act` 存实际，`CACHE.meta.ann` 保留 `annRetOf(pr)` 的当前权重回溯收益。当前 `holdProfit=1,398.45`、`cost=18,032.94`、首笔 2025-11-05、末 2026-11-25（385 天），累计 +7.75498%、年化 **+7.34%**，低于 10% 目标 **2.66pct**。卡首行显示「组合实际年化收益 +7.34%（账户持有收益/成本 …） · 目标 10% · 低于目标 2.66pct」；页脚写「含已实现盈亏与现金 0 收益；是成本口径简单年化，不是资金加权 IRR——外部现金流台账 0 笔，暂不可算」，并保留「当前配置回溯 +6.44%（2016-05-27→2026-11-25，历史权重按当时可用净值归一，不是账户实际持仓）」作参考。

**实测（本地 538 真渲染）**：`#volKpi` 首行 +7.34%、三格 12.00/17.98/15.31 全绿「正常」、第二行「20% 上限内，最高 120日 17.98%（距上限 2.02pct） · 年化收益目标 10%（投资总纲，非本卡指标） · 只监控，不冻结买入」；页脚实际/回溯两套口径完整，无重叠/溢出。真实 UI 总纲编辑：`#tgIn_volCap` 输入 22 + Tab → 输入框 22、`#tgGoalTxt` 变「10% 年化 / ≤20% 回撤 / ≤22% 波动」、`localStorage.fw2_tg_thesis` 变 `{"tgtAnn":10,"ddBudget":20,"volCap":22,"rf":1.59}`；切持仓页 `#volKpi` 显示「22% 上限内，最高 120日 17.98%（距上限 4.02pct）」、页脚「波动率上限 22%」；再改回 20 全部恢复。

**闸门与发布**：`check_js` 22 块 ALL OK、`check_html_comments` 387 处 0 隐患、`check_globals` PASS（282 键 / 基线 282，新增 0 / 消失 0 / 变化 17）、`check_hold_consistency` PASS=9 WARN=2 FAIL=0、`verify_manifest` PASS（43 数据集 / 1 项 W2）、`_audit_plan_merge_v895` 42/42；`push_gh_v39.py`（`SKIP_GATE=1`）`[200] caifu/index.html`（5,648,673 B），其余发布文件 `[SKIP] unchanged`，master `384c4e8cd640`；脚本随后 GitHub API 回读 `IncompleteRead` 崩，但 raw SHA256 `BECB316E…E15584` 与本地逐字节一致。**GitHub Pages 已恢复**：status 200，线上 v1164 持仓页 DOM 已见首行 +7.34%、三格 12.00/17.98/15.31、20% 上限说明；总纲页线上因 BU 视口 0×0 未触发懒渲染，总纲 UI 以本地真实 UI 验收为准；raw 已验收。

**别碰**：20% 仍只监控，不接 P2-9/P2-11/网格/回测/交易闸门；+7.34% 是成本口径简单年化，不是 IRR、不是已实现收益；`+6.44%` 是当前权重回溯、非账户实际持仓；`volCap` 与 `ddBudget=20` 不是同一个 20%；`portReturns` 只取非现金净值日、现金 0 波动、`riskContribs` 非现金分母均未改。
