## 2026-11-27 · v1164 20% 进总纲 + 波动率卡展示实际年化（已发布）

- **改了什么**：`edit_work/index.html` 徽标 `v1164` + tag `fw2_v1164_tgt_volcap_return`，master `384c4e8cd640`（5,648,673 B / SHA256 `BECB316EE74F0661A409E3A27CD3B97F2270CB598D091F64AFEB090737E15584` / 纯 LF）。①`VOL_CAP` 改读 `fw2_tg_thesis.volCap`（默认 20，范围 1–80），`TG_THESIS_DEF` 四键化，旧存档幂等回填 `volCap:20`；总纲阈值表新增「波动率上限」行，表头 26 项可改 + 1 项已下线 · 28 行、第 1 组 4 项、数据管理 27 项 / 4 目标 / 四键。②新增 `actualRetOf(W,asOf)`，用账户 `holdProfit=1,398.45` / `cost=18,032.94`，首笔 2025-11-05→2026-11-25（385 天），累计 +7.75498%、年化 **+7.34%**；卡首行显示实际年化 + 目标 10% + 低于目标 2.66pct；页脚明写成本口径简单年化、不是资金加权 IRR，并保留当前权重回溯 +6.44% 作参考。③20% 仍未接买入冻结，未进 P2-9/P2-11/网格/回测/交易闸门。④真实 UI 把 22 写入总纲后卡联动「22% 上限内，最高 120日 17.98%（距上限 4.02pct）」、`tgGoalTxt` 变「≤22% 波动」，再恢复 20。⑤闸门 `check_js` 22 块 ALL OK、注释 387 处 0 隐患、`check_globals` PASS（282 键 / 基线 282，新增 0 / 消失 0 / 变化 17）、`check_hold_consistency` PASS=9 WARN=2 FAIL=0、`verify_manifest` PASS、`_audit_plan_merge_v895` 42/42；`push_gh` `[200] caifu/index.html`，其余 `[SKIP]`，脚本随后 API 回读 `IncompleteRead` 崩，raw SHA256 与本地一致。截图 `D:\Temp\v1164_act_kpi2_538.png` / `v1164_act_foot_538.png` / `v1164_act_top_538.png`。
- **未验证的假设**：①+7.34% 是账户持有收益/成本口径简单年化，不是资金加权 IRR；`capital-balance.json tx=0`、`ledger-import.json` 缺 11-06 至 11-25，IRR 暂不可算。②+6.44% 是当前权重回溯，历史权重按当时可用净值归一，不是账户实际持仓。③20% 仍只监控，未验证任何买入冻结路径。④GitHub Pages 已恢复（status 200）：线上 v1164 持仓页 DOM 已见 +7.34%、三格 12.00/17.98/15.31、20% 上限说明；总纲页因 BU 视口 0×0 未触发懒渲染，线上总纲 UI 未直接验收，以本地真实 UI 为准；raw 已验收。⑤全量 gate 未跑，发布走 `SKIP_GATE=1`，既有 WARN 未处理。⑥`tgSaveMsg` 真实输入 22 时只显示基础说明、未出现「已写入」绿字，但 localStorage/goal/重绘均生效，原因未细查。
- **下一步 + 别碰**：下一步＝①线上已恢复，强刷 `?view=holdings&t=v1164live1&final=1` 复核 +7.34%、三格 12.00/17.98/15.31、20% 上限说明、页脚两套口径（本轮 BU 已读到）；②`?view=tg&t=v1164live2&final=1` 验「这四个数」与第 1 组「波动率上限 20 / 1–80」，改 22 再改回 20（线上总纲懒渲染未触发，暂以本地真实 UI 为准）；③拍板是否接受成本口径实际年化、是否保留 6.44% 参考、20% 是否将来接买入冻结。别碰＝`portReturns` 只取非现金净值日、现金 0 波动、`riskContribs` 非现金分母；不要把 +7.34% 写成 IRR；不要把 6.44% 当账户实际；不要把 `volCap` 与 `ddBudget=20` 混为同一个 20；不要接 P2-9/P2-11/网格。

## 2026-11-27 · v1163 波动率上限改为 20%（已发布）

- **改了什么**：`edit_work/index.html` 徽标 `v1163` + tag `fw2_v1163_vol_cap20`，master `deb8fd924458`（5,640,791 B / SHA256 `6A21EF32DBC545D57F325EFEC684027B2E3E9E8A3FB81DA8185417AE39BEDF96` / 纯 LF）。①常量改 `WINS=[60,120,250], VOL_CAP=20`，旧 `VOL_WARN/VOL_HIGH` 删除；`#volTopAlert` 仅 ≥20% 显示，当前最高 17.98% → 隐藏；`band/chip` 改「正常 / 超上限」二元。②`#volKpi` 动态行「20% 上限内，最高 120日 17.98%（距上限 2.02pct） · 年化收益目标 10%（投资总纲，非本卡指标） · 只监控，不冻结买入」，10% 读 `tgThesis().tgtAnn`；`#volFoot` 明写 20% 只读监控、未接买入冻结。③what-if 三档数值未改（10.52/15.33/13.10、9.34/13.19/11.32、6.15/7.20/6.51），只改颜色判断。④线上 538 实测徽标 v1163、三格全绿、首屏无超限条、页脚完整、无横向溢出。⑤闸门 `check_js` / `check_html_comments` 385 / `check_globals` / `check_hold_consistency` / `verify_manifest` / `_audit_plan_merge_v895` 全过；`push_gh` 只 `[200] caifu/index.html`，raw 字节与本地一致。截图 `D:\Temp\v1163_online_vol_538.png` / `v1163_online_foot_538.png` / `v1163_vol_top_538.png`。
- **未验证的假设**：①20% 仍只是监控上限，未接买入冻结/交易闸门；②10% 只引用投资总纲目标，页面未计算组合实际年化收益；③`VOL_CAP=20` 是前端常量，未进 `fw2_tg_thesis`；④`riskContribs` 仍是 120 日协方差近似，不是严格风险分解；⑤what-if 仍假设卖出款全部转现金、不买入、不改其他仓位；⑥全量 gate 未跑，发布走 `SKIP_GATE=1`，既有 WARN 未处理。
- **下一步 + 别碰**：下一步＝①线上 `?view=holdings&t=v1163live1&final=1` 验 20% 上限口径与首屏隐藏；②拍板 20% 是否接买入冻结、是否把 `VOL_CAP` 放进投资总纲、是否展示组合实际年化收益。别碰＝`portReturns` 只取非现金净值日、`riskContribs` 非现金分母、what-if 三档数值；不要把 20% 与 `ddBudget=20` 混为同一个 20%；不要接 P2-9/P2-11/网格。

## 2026-11-27 · v1162 012920 减仓 what-if（已发布）

- **改了什么**：`edit_work/index.html` 徽标 `v1162` + tag `fw2_v1162_vol_whatif`（内部 `v1162b`），master `5cbe34f51827`（5,639,329 B / SHA256 `BF0E5CC9BADA00D6DD74478C0F501AE7B2BB863C79865AD9C16D2846A4CF7DAB` / 纯 LF）。①`#volCard` 内 `#volRisk` 与 `#volFoot` 间新增 `#volWhatIf`；`volWhatIf(W, ser)` 复用 `portReturns` / `annVolOf`，按总资产权重（含现金）算 012920 降到 20%/15%/清仓三档，卖出额现算；②`portReturns` 的 `allDs` 跳过 `isCash`，估值日只取非现金净值日，修掉线上清仓档 5.69/5.09/5.80 与本地 6.15/7.20/6.51 的分叉；③实测线上 538：10.52/15.33/13.10、9.34/13.19/11.32、6.15/7.20/6.51，KPI 仍 12.00/17.98/15.31；`#volWhatIf` 483×129、`body 529/529` 无横溢；④闸门 `check_js` / `check_html_comments` 383 / `check_globals` / `check_hold_consistency` / `verify_manifest` / `_audit_plan_merge_v895` 全过，`push_gh` 只 `[200] caifu/index.html`。截图 `D:\Temp\v1162_online_whatif_final_538.png` / `v1162_whatif_538b.png` / `v1162_foot_538.png`。
- **未验证的假设**：①what-if 假设卖出款全部转现金、不买入、不改其他仓位，不是实际调仓路径；②现金按 0 波动仍是假设；③`riskContribs` 是 120 日协方差近似，不是严格风险分解；④10%/15% 仍只是展示参考带，用户未拍板为硬阈值；⑤全量 gate 未跑，发布走 `SKIP_GATE=1`，既有 WARN 未处理。
- **下一步 + 别碰**：下一步＝①线上 `?view=holdings&t=v1162live2&final=1` 验三行 what-if 与页脚；②拍板 10% 是否硬目标、012920 是否接受降到 20%/15% 或清仓、是否把 ≥15% 接买入提示。别碰＝`portReturns` 估值日口径（只取非现金净值日）、`riskContribs` 非现金分母、10%/15% 展示语义；不要接 P2-9/P2-11、网格或任何交易冻结；不要把 what-if 说成卖出建议。

## 2026-11-27 · v1161 波动率只读监控 + 首屏预警（已发布）

- **改了什么**：`edit_work/index.html` 徽标 `v1161` + tags `fw2_v1161_vol_monitor` / `fw2_v1161_vol_top`，master `8105a92e8446`（5,635,501 B / SHA256 `C76FCEE8F8BC8A5F10870A0E8759CCFD9C3100962A89F50003FB9A75ED4D2479` / 纯 LF）。①`#hdSummary` 下新增首屏预警条，≥10% 才显示，点击滚到 `#volCard`；②页底卡扩为 60/120/250 日 KPI + 风险贡献 Top5，保留 20 日滚动 vs 沪深300；③`portReturns` 把 `assetType==='cash'` 按 0 收益计入全部净值日，`CACHE.vol` 为总资产口径；另算 `prNC` 供 `riskContribs`，贡献合计 100%；④覆盖率改 `inc/ncTotal`，现金单列；⑤实测 60/120/250＝12.00/17.98/15.31，20 日 13.03 vs 沪深300 14.36，012920 贡献 63.6%；⑥闸门 `check_js` / `check_html_comments` / `check_globals` / `check_hold_consistency` / `verify_manifest` / `_audit_plan_merge_v895` 全过，`push_gh` 只 `[200] caifu/index.html`。截图 `D:\Temp\v1161_vol_538c.png` / `v1161_topalert3_538.png` / `v1161_online_top_538b.png`。
- **未验证的假设**：①现金按 0 波动是监控假设，货币基金实际有极低波动；②`riskContribs` 是 120 日协方差近似，不是严格风险分解；③10%/15% 参考带是展示默认，用户未拍板为硬阈值；④数据仅到 2026-11-25（净值）/ 11-25（沪深300），跨 QDII T+1 断点按各自日历；⑤全量 gate 未跑，发布走 `SKIP_GATE=1`，既有 WARN 未处理。
- **下一步 + 别碰**：下一步＝①线上 `?view=holdings&t=v1161live2&final=1` 验首屏预警与页底卡；②拍板 10% 是否硬目标、是否做 012920 的 63.6% 减仓 what-if、是否把 ≥15% 接买入提示（本轮只读不冻结）。别碰＝`portReturns` 现金 0 波动、`riskContribs` 非现金分母、10%/15% 展示语义；不要接 P2-9/P2-11、网格或任何交易冻结；不要把非现金波动乘 0.624 当总资产波动，也不要把总资产波动再乘 0.624。

## 2026-11-27 · v1160 网格预算 A 保守方案（已发布）

- **改了什么**：`edit_work/index.html` 徽标 `v1160` + tag `fw2_v1160_grid_budget_6000`，master `1fec1b5f252d`（5,626,939 B / SHA256 `05FAC1E7FA6A1E2112E7C964695A69BB095883D0BC78FE917529DBD924B82F7C` / 纯 LF）。①网格默认预设七只：012920 1,500、001015/160422/000307 各 1,000、022438/012761/023917 各 500，合计上限 ¥6,000，其余关闭；一次全触发 ¥3,500，现金 ¥7,720.80。②`gdMigratePreset` 首次运行写入预设、其余旧配置 `on:false/cap:0`，只动 `localStorage.fw2_grid_plan_v1`，不动持仓/流水。③`gdCfgOf` 缺省按预设、未知 `on:false/cap:0`；`window.SIGNALS_CFG.gridCfgOf` 供 T13 优先读，避免网格页关闭后信号页仍按全局 10,000 生成。④修网格卡过滤：旧 `/货币|活期宝|现金/` 误伤 023917 自由现金流，旧 `status==='off'` 隐藏账户仍有份额的 012761/023917；新增 `gdIsCashRow/gdIsGridRow`，`gdCardsHtml` 与 `gdRender` 共用，页面 22→24 卡、7 只全可见。⑤KPI 第 3 格改「一次全触发」、页头文案与「全部恢复默认」确认文案同步；`gdSave` 的 `on` 兜底改回 `cur.on`，防编辑关闭卡字段时意外打开。⑥实测本地/线上 538：7 / 24、¥6,000、¥3,500、计划外 14；012920 关→6 / ¥4,500、再开→7 / ¥6,000；全部恢复默认仍 7 / ¥6,000；线上 T13 七只「预算内（逐只计划）」，012761/023917 有行，四只已关闭。⑦`check_js` 22 块 ALL OK、注释 379 处 0 隐患、`check_globals` PASS、`verify_sync --gh-only` 六文件字节一致（5,626,939 B）。截图 `D:\Temp\v1160_gd_538.png` / `v1160_gd_card_538.png` / `v1160_online_gd_538.png`。
- **未验证的假设**：①旧配置迁移只在「无 `fw2_grid_budget_6000_v1` 标记」的浏览器跑一次；已标记的浏览器若手动改过七只，不会被重新覆盖；跨设备/清缓存会按预设重写，但 localStorage 不跨设备。②迁移把其余旧配置 `cap` 清 0 不可逆（只保留 `on:false`），未做导出/备份；若要恢复旧 10,000 上限需手动逐只改。③6,000 是配置上限，不是预算/可用现金；实际同日可触发笔数仍受现金约束。④页面卡从 22 变 24 是修正非现金持仓口径（含 012761/023917），不是新增持仓；「计划外 14」包含关闭的 14 只。⑤网格「关闭」仍只表示默认不生成 T13 网格买入并保留一行「已关闭」，不是永久禁买/清空已用。⑥线上 Pages 首访可能仍读旧缓存，验收用 `?t=v1160live1` 强刷；全量 gate 未跑，本轮走 `SKIP_GATE=1`，既有 3 条 WARN 未处理。
- **下一步 + 别碰**：下一步＝①线上 `?view=strategy&t=v1160live1&final=1` 验「网格计划」7 / 24、¥6,000、¥3,500、计划外 14 与 7 个勾选；`?view=signal&t=v1160live2&final=1` 验 T13 七只逐只上限。②若要「关闭的 17 只不显示」或「关闭＝永久禁买/清空已用」，另定口径再改。③若要恢复某只旧上限，在网格卡手动改并保存，不要重跑迁移标记。别碰＝全局 `gridFund=10,000`、回测引擎、持仓/流水、信号阈值与三态；不要用宽泛 `/现金/` 过滤；不要用 `status==='off'` 一刀切隐藏账户仍有份额的基金；不要把 `assetType` 当成 `holdRows` 顶层字段。

## 2026-11-27 · v1159 策略工厂默认固定起点池（已发布）

- **改了什么**：`edit_work/index.html` 徽标 `v1159` + tag `fw2_v1159_sf_default_fixed`，master `ab411f887923`（5,622,268 B / SHA256 `39BADE21551CBD899D6E8ED1792FE43E319A80F751CB094417F0898E8B2D6E27` / 纯 LF）。①「组合池」默认由 `pit` 改 `fixed`（固定起点池），pit 仍可手动切；选项 fixed 在前并 selected，文案标「默认」。②旧缓存迁移：`sfSave` 增 `ver:'v1159'`；`sfRender` 只在旧缓存无 ver 且 poolmode 为 pit/缺省时，把 cfg 改 fixed 后同参数 `sfRun()` 重算一次；带 ver 的手选 pit 不再迁移。③页脚补「fixed 仍取自当前候选池、有幸存者偏差」。④实测 fixed 池 7只 Top3/60 ¥79,758 / +59.52% / 4.38% / MDD −32.02% / Calmar 0.14 / 101 次；pit 池 15只仍 −19.86%。⑤本地/线上 538 真渲染通过；`check_js` 22 块 ALL OK、注释 378 处 0 隐患、`check_globals` 新增0/消失0、台账 43 数据集 PASS、`_audit_plan_merge_v895` 42/42、`verify_sync --gh-only` 六文件字节一致。
- **未验证的假设**：①fixed 池 7 只仍取自当前 15 只候选，未包含已终止/未入池标的，不是无偏全样本；②旧缓存迁移只覆盖「无 ver 的 v1158 缓存」，更早缓存若已被手改成 fixed 只会正常恢复；③22 只 × ¥10,000 的网格上限未改，仍待用户拍板；④线上首访仍可能读旧 HTML 缓存，验收用 `?t=v1159live1` 强刷。
- **下一步 + 别碰**：下一步＝①线上 `?view=strategy&t=v1159live1&final=1` 验策略工厂默认 fixed 与 pit 切换；②拍板网格上限（A 保守 / B 总闸 / C 维持），清单建议 6–8 只有意义持仓 + 总闸 ¥5,000–7,000；③不改 `sfPortBacktest` 成交时点。别碰＝不要删 `ver` 条件（手选 pit 会被重置）；不要把 fixed 的 +59.52% 当无偏全样本；不要改 `sfPortBacktest` 的 t−1/当日收盘口径。

## 2026-11-27 · v1158 网格逐只起算日 + 策略工厂去前视 + 两个 v1156 渲染 bug（已发布）

- **改了什么**：`edit_work/index.html` 徽标 `v1158` + tag `fw2_v1158_grid_since_sf_lookahead`，已发布 master `e4c09694b753`（`caifu/index.html` 5,620,944 B / SHA256 `D9484E96B4C10C94750B27725BDD668C2E6A25B8CE2A3AF86F083330A0B450B5` / 纯 LF；`caifu/holdings-data.json` 同步逐笔 `buys`）。①网格「已用」改逐只 since：`GD_PLAN_START=2026-11-27`、`gdUsage(code,since)` 过滤 `gridUsage.funds[code].buys`，012920 由 ¥8,700/17 笔变 ¥0/0 笔、可买 20 档；新增「从今天重算」，暂停再开不重置。②策略工厂动量打分改 t−1（`ii-1`），Top3/60 由 −24.58% 变 −19.86%、MDD −55.77%、106 次；新增 `poolmode=pit/fixed`，固定起点池 7 只出 +59.52%；敏感性重跑最高 Top5/120 +160.70% / Calmar 0.31。③`switchStratTab` 懒渲染名单补 `gd`，修网格页签空白。④首屏 `view=strategy` 的 `renderStrategyView` 竞态加 guard + load 补渲染。⑤修我自己引入的 `sfShellHtml` 引用 `cfg` 报错，页脚改静态双口径。
- **未验证的假设**：①`buys` 窗口仍从 2024-01-01 取，早于它的买入不会被查回，所以「历史买入」不是全历史；②「暂停再开不重置」只对已有 `since` 的配置成立，旧配置没有 `since` 时会落到默认 2026-11-27；③固定起点池 = 起点日 2016-01-04 当天有价格的 7 只，换起点日池会变；④敏感性 9 组只说明参数不是孤点，不构成样本外证据；⑤线上 Pages 首访可能仍读旧缓存，验收加了 `t=v1158live1` 强刷。
- **下一步 + 别碰**：下一步＝①线上 `?view=strategy&t=v1158live1&final=1` 验收「网格计划」012920 与「策略工厂」Top3/60；②拍板网格 22 只默认每只 ¥10,000、合计 ¥220,000 上限是否要收，以及策略工厂默认是否从「当时可用池」改「固定起点池」；③补 `FRONTEND.md` v1056–v1155 缺失明细。别碰＝不要把 `buys` 退回聚合字段；不要把旧 −24.58% 当新结论；不要把 `since` 写进持仓/流水；不要在 `sfShellHtml` 引用 `cfg`。

## 2026-11-27 · v1157 六条回复落地：网格已用接流水 / 发现层六源 / 策略工厂 v2（已发布）

- **改了什么**：①`edit_work/gen_grid_usage.py`（新）从 ttskill `TRADE_QUERY` 买入流水生成 `holdings-data.json.gridUsage`，再调 `_sync_holdings_inline.py`；2026-11-27 实跑 23 只 / 169 笔，012920 17 笔 ¥8,700 / 至 2026-03-06。②`index.html` 徽标 v1157 + tag `fw2_v1157_grid_disc_sf`：`gdUsage` 读 `HOLDINGS_SEED.gridUsage`，网格卡显示已用/剩余/可买档/累计笔数；T13 关闭保留一行「已关闭」；`gen_discovery.py` 扩六源（持仓 24 / 工厂 15，160 条 / 去重 137 / 跨源 23）；`refresh_all.py` 挂 `grid-usage` 与 `discovery`；策略工厂 v2 增动量轮动、等权组合级、敏感性、localStorage 落盘/恢复、JSON 导出；T2b/T17 定稿。③`docs/DATA_LEDGER.md` / `data-ledger.json` / `FRONTEND.md` §10.49 修正 + §10.52 / `README.md` 四节同步。已发布 master `f0132ecf0586`，5,612,637 B / SHA256 `A02D41F2761EC827C1B7DCD55E5A2E21BAE914E994BF2FB0A7EDB5B4DBE71880` / 纯 LF；`verify_sync --gh-only` PASS；四项检查 + 两项审计全过。
- **未验证的假设**：①`gridUsage` 窗口是 2024-01-01 起累计，不是计划启用日起算；②`totalCount>=500` 截断分支未真实触发（本轮 169 笔）；③策略工厂动量池 / Top3 / 60 日 / 敏感性维度 / 组合基准均为本轮默认，用户未逐项拍板；④落盘只在本机 localStorage，不是跨设备同步；⑤「网格为什么要关闭」语义未澄清，当前只做「关闭保留行」；⑥线上 Pages 可能仍读旧缓存，需 `?t=v1157live1` 强刷；全量 gate 未跑，发布走 `SKIP_GATE=1`。
- **下一步 + 别碰**：下一步＝①线上 `?view=strategy&t=v1157live1&final=1` 验收网格已用/关闭行/策略工厂三项/发现层 chips；②拍板网格已用是否按计划启用日起算、网格是否要默认全开、策略工厂默认池与基准；③补 `FRONTEND.md` v1056–v1155 明细。别碰＝不要猜已用金额；不要把预算独立说成市值不计入；不要把 localStorage 上次结果当跨设备同步；不要接实盘/下单；不要改 `v11-bt-data` 的 `day` 换算与成交时点；不要对既有长文档用 `Write` 传单节。

## 2026-11-27 · v1156 网格计划独立化 + 核心-卫星边界（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1156 + tag `fw2_v1156_grid_indep`；新增第 9 个策略页签「网格计划」（`data-st="gd"` / `#stp-gd`），22 只非现金持仓逐只配置步进/单笔/上限/资金来源，配置存 `localStorage.fw2_grid_plan_v1`，不写流水/持仓/状态；T13 网格跟踪优先读 `C.grid.pf[code6]`，未配置回落全局，逐只关闭则不再生成该只 T13 行；新增核心-卫星边界卡（四档杠铃已是核心-卫星，不另建卫星仓；网格预算独立但份额市值仍计入桶）；顺带修总纲「变更记录」`undefined undefined→`。`_audit_plan_merge_v895` A01 扩 9 tab + 新增 A01g，42/42 PASS。已发布 master `4929a6bffdab`，5,592,623 B / SHA256 `1680C2136D5CEB7DA8B8400D88B2A47C6FB07FE1F9CA2DF9864165B31E46E28E` / 纯 LF；`verify_sync --gh-only` PASS，线上 538 9 页签单行、22 卡、012920 触发 ¥2.6465。同步 README 四节、`docs/FRONTEND.md` 恢复说明 + §10.49–§10.51、`docs/PITFALLS.md` P-v1156。
- **未验证的假设**：①改一只步进/单笔/上限后刷新保持、切信号页 T13 同步、关闭后行消失——本轮只实测「012920 3%→5% 触发价与 T13 文案变化、并落观察组」，未逐只全量验收；②网格配置只在本机 localStorage，换设备/清缓存不带走，未做导入导出；③「已用金额」未接流水，固定显示「—」，不是 0；④线上 Pages 可能仍读旧缓存，需 `?t=v1156live1` 强刷；⑤全量 gate 未跑，发布走 `SKIP_GATE=1`，既有 `verify_acc_nav.py` / `fund_daily` 阻塞仍在。
- **已知缺口（文档事故）**：本轮误用 `Write` 覆盖 `docs/FRONTEND.md` 为 4 KB；已从 `D:\Temp\FRONTEND.md.bak_v1055pre` 恢复主体，并补 §10.49–§10.51 当前摘要，但 **v1056–v1155 的 §10.x 明细约 1,300 行仍缺**，文件头已写恢复说明。接手者若要补，优先从 `D:\Temp\patch_docs_v1150.py` / `patch_docs_v1151.py` 与 README/INBOX 逐版恢复；未补回前不要把 FRONTEND 当 v1056–v1155 唯一真源。
- **下一步 + 别碰**：下一步＝①线上 `?view=strategy&t=v1156live1&final=1` 验收 9 页签/22 卡/KPI/012920；②改一只配置后切信号页验 T13 同步，关闭一只验行消失；③拍板「已用金额是否接流水」「关闭后保留一行还是直接消失」「预算独立但市值计入桶」；④补 FRONTEND 缺失章节。别碰＝不要猜已用金额；不要把预算独立说成市值不计入；不要把网格当第三套仓；不要新增 window 顶层键；改 `#stratTabs` 列数必须同步媒体查询；不要对既有长文档用 `Write` 传单节。

## 2026-11-27 · v1152 数据债第 1 项（已发布，含数据管理页源描述同步）

- **改了什么**：①`gen_fund_jjcc.py` 单线程 + 每只 2s + 514 重试，重跑 23/24，写 24 只、变动 0；②`gen_index_bench.py` 主源改腾讯 newfqkline、备源新浪日K / 中证官网，`curl` 3 次重试、15:10 前剔除当日，8/8 末点 2026-11-26；③`gen_macro_extra.py` 重写纯 urllib，6/6，`profit` 改官方工业利润 16.0/15.5/15.7、`real_estate` 改官方地产投资 −21.6/−20.6/−19.9；④`gen_pb_ratio.py` 改直连乐咕，512 周点；⑤`data-mgmt.json` 在 `DM_FROM_CHAIN=1` 下重生成，`refreshFailed=[]`；⑥新增 `docs/DATA_DEBT_2026-11-27.md`，同步 DATA_LEDGER / PITFALLS。⑦为过 `_audit_dm_v845` 的 `driftKeys=4`，`index.html` 只把数据管理页四行源描述同步成新文案并升徽标 v1152（无判定/布局改动）；已发布 5 个文件，`verify_sync --gh-only` PASS，线上 47 行、`refreshFailed=[]`、旧 akshare 文案 0 命中。
- **未验证的假设**：①`refreshFailed=[]` 是模拟链成功，不是完整 `refresh_all.py` 全链验证；②`sm_ashare` Q3（2026-09-30）仍未取，内嵌数据仍 `asOf=2026-09-22`；③`index_long` 000510/NDX/N225 仍 `push2his rc=56`，本轮拒绝写半套，文件仍 11-13；④`pe_hist`/`sources`/手工轨未重跑；⑤`pb_ratio` 11-29 是当前周锚的未完成周，11-22 的 12.17 对应 11-20 的 636/5224，跳升属实但未与另一源复核；⑥`index.html` 只同步数据管理页四行源描述 + 徽标 v1152，未改判定/布局；线上已发布但 `DM_FROM_CHAIN=1` 仍不是完整全链证据。
- **下一步 + 别碰**：下一步＝①线上 `?view=datamgmt&t=v1152live1&final=1` 展开 47 行验收四行源描述与刷新状态；②下一次 21:30 全链后复核 `data-mgmt.json`，不要用手改消红；③若要 `sm_ashare` Q3，改 `ashare_sm/fetch_ashare_smartmoney.py` 的 `QUARTERS` + aggregate + 注入 index.html 并升版渲染；④`index_long` 找 000510/NDX/N225 替代源。别碰＝不要把腾讯盘中线写进 index-daily；不要把 `profit` 再换回工业增加值；不要把 `real_estate` 换回国房景气；不要依赖 `_pydeps` 的 pandas；不要把 `DM_FROM_CHAIN` 的绿当全链通过。

## 2026-11-27 · v1151 P2-9 回撤账本补记 + JSON 导入

- **改了什么**：`edit_work/index.html` 徽标 v1151 + tag `fw2_v1151_p2_dd_backfill`，已发布 master `4152b3540a29`（5,534,973 B / SHA256 `6790C795A9C6C566BAA19F3EAB5FE3AD6A162FD2A6F04CA610CE8B7A0710EE7A` / 纯 LF）。新增 `_p2DdSave`；`_p2DdState` 增 `savedBase` 固定基准日并丢弃基准日前快照；`p2DrawdownData` 返回增 `baseDate/snaps`；`_p2SnapRowsHtml` / `_p2DdAddSnap` / `_p2DdDelSnap` / `_p2DdImport`；P2 卡 `<details>` 增「总资产快照补记」表单 + 快照列表 + 「导入账本 JSON」按钮/隐藏 file input；CSS 增 `.p2-flow-sub` / `.p2-flow-list` / `.p2-snap-list` / `.p2-snap-row`。未改 `signalEvalAll` 判定/阈值/三态、`data/*.json`、交易状态，未自动卖。
- **未验证的假设**：①A+ 基准日 2026-11-26 固定，补记只补之后，**基准日之前仍不可判**；②手工补记只能补「基准日之后、不晚于今天」的日期，不能替代每天打开工作台；③导入是文件级恢复/合并，不是跨设备自动同步；④导入按 id 去重，无 id 的旧流水会由 `_p2FlowLoad` 生成 `f日期_金额`，同日同额同备注可能合并；⑤Pages 首次强刷可能仍读旧缓存，需等 60–90 秒；⑥全量 gate 未跑，发布走 `SKIP_GATE=1`。
- **下一步 + 别碰**：下一步＝①线上 `?view=holdings&t=v1151live1&final=1` 强刷验收「总资产快照补记」+「导入账本 JSON」；②后续每天打开一次工作台，漏记日用补记补齐基准日之后；③P2-12 样本外 ≥1 年；④项目级数据债另案。别碰＝不要把补记扩到基准日之前；不要填假流水；不要把基金申赎算外部现金流；不要允许删基准日/当前数据日；不要先写后验导入；不要自动卖/写交易状态；不要新增 window 顶层测试钩子。

## 2026-11-27 · v1150 P2-9 实际回撤按 A+ 接执行

- **改了什么**：`edit_work/index.html` 徽标 v1150 + tag `fw2_v1150_p2_dd_exec`，已发布 master `bda24c3e7c34`（5,523,136 B / SHA256 `8ED4259A298ACD752E6244CEA8DF9410E2EE146D8622B583806680B88F40F27B` / 纯 LF）。新增 `P2_DD_CFG`（minDays 20 / 本机快照键 / 出入金键）、`_p2AsOfDate`、`_p2FlowLoad/Save/On`、`_p2DdState`、`_p2DdRecalc`、`p2DrawdownData`、`_p2DdExport`；`holdP2GateData` 增 `dd`；`p2BuyBlockOf` 在 `active && bad` 时对任意代码返回 `allBuys:true`；P2 卡四格 + 出入金 `<details>` + 导出；信号页 `_p2Dd` / `_p2Scope` / `_p2Bits` / `_hardRs` / `actPlan` 接全组合回撤冻结。前 20 个数据日只读。未改 `signalEvalAll` 判定/阈值/三态，未改 `data/*.json`，未自动卖/写状态。
- **未验证的假设**：①账本只在本机 localStorage，没打开工作台的数据日不会自动补，20 天样本可能积累很慢；②基准日当天出入金不参与 HWM 调整，是避免重复计入的暂定口径；③出入金日期必须与某个快照日期相同才影响该日 HWM，跨日补记不会自动分摊；④Pages 首次强刷可能仍读旧缓存，需等 60–90 秒；⑤全量 gate 未跑，发布走 `SKIP_GATE=1`。
- **下一步 + 别碰**：下一步＝①线上 `?view=holdings&t=v1150live1&final=1` 与 `?view=signal&t=v1150live2&final=1` 强刷验收四格卡、1/20、账本与导出；②确认前 20 日只读；③后续每天打开一次工作台积累数据日；④P2-12 样本外跟踪 ≥1 年。别碰＝`signalEvalAll`；`data/*.json`；不要填假历史 total/假流水；不要把基金申赎算外部现金流；不要用系统日期替代 `state._pfAt`；不要降低 `minDays=20`；不要冻结卖出/拦截/观察；不要自动卖；不要新增 window 顶层测试钩子。

## 2026-11-27 · v1149 P2-9 压力 20pp 接进买入冻结

- **改了什么**：`edit_work/index.html` 徽标 v1149 + tag `fw2_v1149_p2_stress_exec`，已发布 master `faf5cfe66090`（5,509,298 B / SHA256 `5C066703A41CCDFA96D4692D758B550353E76128FB6DB34C0BA2B0371A5083B8` / 纯 LF）。`holdP2GateData()` 新增 `stressBad`；`p2BuyBlockOf(d, code)` 改为「单只 >20% 或 压力 >20pp」且只冻最大非现金持仓，返回 `flags:['conc','stress']`；信号页 `_p2Flags/_p2Conc/_p2Stress` 可同屏两条原因；P2 卡改「组合风险闸门 · 单只 + 压力」、徽标「P2-9 已生效 · 实际回撤待建」。实际回撤仍不接，回撤格「待建立」。未改 `signalEvalAll` 判定/阈值/三态，未改 `data/*.json`，未自动卖/写状态。
- **未验证的假设**：①压力 >20pp 在当前阈值下需集中度 >44.8%，单只闸门通常先冻结，压力分支日常看不到，只有合成行能验收；②「只冻最大单只」是否足够，取决于你接受“其他标的仍可买、用来降集中度”；③实际回撤若改为「从今日起新建高水位」，历史段无法回填；④线上 Pages 可能有 CDN 传播延迟；⑤全量 gate 未跑，发布走 `SKIP_GATE=1`。
- **下一步 + 别碰**：下一步＝①线上 `?view=holdings&t=v1149live1&final=1` 与 `?view=signal&t=v1149live2&final=1` 强刷验收 P2 卡与冻结徽标；②拍板实际回撤口径（新建高水位 / 账户 P&L 近似 / 继续待建）；③P2-12 样本外跟踪 ≥1 年。别碰＝`signalEvalAll`；`data/*.json`；实际回撤无高水位时不要改灯；不要用当前权重倒推历史回撤；不要把压力超限扩成全组合冻结；不要拆掉 `window.SIGNALS_CFG` 挂载。

## 2026-11-26 · v1128 持仓信号隐藏活期宝等现金/货基兜底

- **改了什么**：`edit_work/index.html` 徽标 v1128 + tag `fw2_v1128_hide_cash_sig`，已发布提交 `42d3b0129757`（index 5,375,778 B / SHA256 `F72E2EC5A3B35122E583F5D8E79370AD4C2C64A8DD83F7235ABCF3591C202917` / 纯 LF）。`grp()` 在 `ddKeys` 前用 `_cashHold` 识别现金类（`state.portfolio` 的 `assetType==='cash'` 或名称含「货币/活期宝/现金宝」），并合并 `ddByCode[code].kind==='money'`；`ddKeys` 过滤后不再给 000912 生成空标卡/占位行。未改 `signalEvalAll` 判定、阈值、表内行序、自选/筛选/市场组、任何 `data/*.json`。
- **未验证的假设**：①活期宝只是从信号隐藏，仍在「我的持仓」、资产配置、现金口径中；②T10 若被投资总纲三态置「关」则不显示，属既有规则，不是本版删除；③线上 Pages 可能有 CDN 传播延迟；④全量 gate 未跑，`fund_daily` 既有 FAIL 与前端无关，发布走 `SKIP_GATE=1`。
- **下一步 + 别碰**：下一步＝①线上 `?t=v1128&final=1` 强刷验收徽标 v1128、持仓信号无「活期宝 / 000912 / 暂无信号·持仓兜底」，T10 汇总→012920→001015→160422→000307；②确认活期宝仍在我的持仓正常显示；③其余 4 项策略待拍板仍未动。别碰＝`signalEvalAll` 判定；`_mvByCode` 排序；`_cashHold` 不要用宽泛 `/现金/`（会误伤 023917 华夏国证自由现金流）；自选/筛选/市场组不套用本过滤。

## 2026-11-26 · v1127 持仓信号按持仓市值降序

- **改了什么**：`edit_work/index.html` 徽标 v1127 + tag `fw2_v1127_hold_sig_mv_sort`，已发布提交 `456d9b0cdb7d`（index 5,374,629 B / SHA256 `9EA42087D2E0DF8028125127FC91EB0E1C7DD91FA7B8F206D6BABC52812C22CA` / 纯 LF）。`renderSignalDash()` 的 `grp()` 内新增 `_mvByCode`（`state.portfolio` 的 `mvCny`/`mv`/`marketValue`，按 6 位代码汇总）；`targets.sort` 仅在 `main==='持仓信号'` 时、`T10 杠铃档位（四档）` 之后按市值降序，同额回退原等级/信号数/指数族/代码；`srcNote` 补「标的按持仓市值降序；T10 杠铃档位（四档）汇总置顶」。未改信号判定、同指数合并选择、表内行序、自选/筛选/市场组排序、任何 data/*.json。
- **未验证的假设**：①同指数合并组按**所显示代表基金自身市值**排，不按家族合计；若你要 12 只纳指100 合并组按合计市值排，需另改合并选择/组位，本轮未动；②活期宝是无信号持仓兜底（000912），按市值 2,843.63 排在第二位；若你要无信号兜底沉底，需另加规则；③线上 Pages 可能有 CDN 传播延迟，首次强刷若仍旧版，等约 3 分钟再试；④全量 gate 未跑，`verify_fund_daily` 既有 FAIL 与前端无关，发布走 `SKIP_GATE=1`。
- **下一步 + 别碰**：下一步＝①线上 `?t=v1127&final=1` 强刷验收表头顺序 `T10 杠铃档位（四档）`（汇总置顶）→012920→活期宝→001015→160422→000307…；②若要「无信号兜底沉底」或「同指数组合计市值排序」，明确后另开一版；③其余 4 项策略待拍板仍未动。别碰＝`T10` 汇总置顶；`_mvByCode` 只读 `state.portfolio`，不要改成读 data 或手填；同指数合并选择仍由 `fw2_v1042_sig_fam_merge` 决定；自选/筛选/市场组不套用本排序。


## 2026-11-26 · v1126 宏观数据补丁（nky 收盘刷新）

- **改了什么**：只刷宏观组 `python refresh_all.py --only macro --no-publish`（197.7s）；`macro-data.json` 451,732 B，nky 57,812.38→**57,498.94**（ts 2026-11-26 14:59:17、src=sina、chgPct 0.86、prevClose 57,011.4、histAsOf 2026-11-25），同时改 `amt/amtD/fsi/sentiment/wave`；`index.html` 由数据链改写 `MACRO_SNAP`，手工只换徽标 v1126 + tag `fw2_v1126_macro_nky_refresh`。`data-mgmt.json` 26,255 B / 47 项 / `refreshFailed=['fund_jjcc','index_daily','macro_extra']`（用 `DM_FROM_CHAIN=1 REFRESH_BAD_STEPS='gen_fund_jjcc.py;gen_index_bench.py;gen_macro_extra.py'` 重建，防把旧失败清成 ok）；`meta-bundle.json` 834,939 B；`nav-hold.json` 1,605,502 B（15:02 重建，24 只 / 33,797 行 / missing=[]）。已发布 master `592a65ec967e`（index 5,372,746 B / SHA256 `5D99FA1AF2E3EA60CF4B59E1F4D3B542AC4F8EF3CD2482987A1D4F413AA5BB75` / 纯 LF），`verify_sync --gh-only` PASS。
- **未验证的假设**：①`verify_nky` 是**降级 PASS**——`nky_live_cross` / `nky_last_3src` / `nky_ohlc_cross` 因实时独立源 `RemoteDisconnected` 按本地底线降级，备注「未获当日新浪×东财双源确认」，不等于双源确认；②`gen_macro_extra.py` rc=1（缺 `akshare`），macro_extra 数据未更新、仍标 fail；③`nav-hold` 的 15:02 重建由 `refresh_all --only macro` 触发，未逐字段与其旧版对比，只验 `missing=[]` / 24 只 / 33,797 行；④全量 gate 未跑，`fund_daily` 既有 FAIL 未处理；⑤Pages 首次检查仍为旧 v1125 缓存，约 3 分钟后才转为 v1126，属于 CDN 传播延迟，不是发布失败。
- **下一步 + 别碰**：下一步＝①线上 `?t=v1126&final=1` 强刷验收徽标 v1126 / 日经 57,498.94 / 成交额 246,541；②补 `akshare` 后重跑 `gen_macro_extra.py`，再以真实失败集重建 `data-mgmt`；③`fund_jjcc` / `index_daily` 上游恢复后重跑；④全量 gate 的 `fund_daily` 既有 FAIL 另案处理。别碰＝`MACRO_SNAP` 不手改；nky 降级 PASS 不冒充双源；`data-mgmt` 只由 `_gen_data_mgmt.py` 重建；`nav-hold` 是 fund-daily 子集，不手写；`index.html` 本轮只换数据与徽标，计算/信号零改。


## 2026-11-26 · v1125 配置回测 V11 筛选池加载时序

- **改了什么**：`edit_work/index.html` 徽标 v1125 + tag `fw2_v1125_sp_wait`，已发布 master `051bbbc43d28`（index 5,372,028 B / SHA256 `2825C3EF48B8320003642C76A4ECDD0F9473F0CB4ED749E7AF583152D8FF4E9C` / 纯 LF）。`btEnsureScreenPool(cb)` 增加 `._wait` 回调队列，就绪判据要求 `funds` 至少 1 只；配置回测 `_kick` 开头守卫：V11 开着且 `SCREEN_POOL` 为空/空对象 → 先提示「V11 狙击需要先加载筛选池」→ 加载成功自动续跑，失败明确拦截并 `return`；提示无条件覆盖旧快照，续跑用 `setTimeout` 不用 rAF。未改 `data/*.json`。
- **未验证的假设**：①全量 gate 未跑完：`verify_nky` 实时价 FAIL（macro.val 57812.38 vs 新浪/东财 57499，0.54%>盘中阈值，数据侧），`verify_fund_daily` 既有 FAIL；为不手改数据，发布走 `SKIP_GATE=1`，仅 index 一项 `[200]`，其余 41 项 `[SKIP] unchanged`。②自动化窗口被遮挡时 rAF 与 CSS 入场动画都会暂停，本地截图用 `setTimeout` + 强制 `animation:none/opacity:1`，属测试环境差异。③`screen-pool.json` 线上 404 兜底未单独断网实测（只拦请求复现失败路径）。
- **下一步 + 别碰**：下一步＝①你强刷线上 `?t=v1125&final=1`，在配置回测里清空筛选池/强刷后点「运行回测」，确认先出黄框、再自动续跑且 V11 非 0 笔；②断网/改坏 `screen-pool.json` URL 验红框拦截；③其余 4 项待拍板（V11 分段候选 / 5 万全投 / 历史快照门限 / 跨域 200 条）仍未动；④`verify_nky` 另跑 `refresh_nky_hist.py`/刷新 macro 修数据，不为过门禁手改。别碰＝`SCREEN_POOL` 结构与 40 只清单；`v11Gate` 1260 日赔率公式；`_SNP.list/base/maxN`；`btLoad()` 仍是唯一回测数据入口；不要给 `btEnsureScreenPool` 新增 `window.__BT_SP_*` 全局。



- **改了什么**：重跑 `_verify_online_v1124.py`（PASS）、`_audit_dm_v845.py`（47/47、`sameKeys=True`、`FAIL=False`）、`_audit_last_sell_link.py`（`FAIL=0 / WARN=4`）、`verify_manifest.py`（PASS，42 数据集 / 41 发布 JSON / 1 告警 W2）；补齐 README `prev` / `关键文件` / `下一步` 与 `docs/FRONTEND.md §10.22`、`docs/PITFALLS.md P-v1124`，只动文档，不动 `index.html` 与 `data/*.json`。
- **未验证的假设**：`gen_index_bench.py`（8 指数全 `JSONDecodeError`）与 `gen_fund_jjcc.py`（HTTP 514 限频、成功率 42%<60%）仍是上游环境问题，本轮重试仍 rc=1，`data/index-daily.json` 196,397 B 与 `data/fund-jjcc.json` 10,474 B 未变；未量化端点恢复时间。
- **下一步 + 别碰**：下一步＝①你刷新线上验 v1124 / 47 项 / 两处失败标记；②上游恢复后重跑两个生成器并以真实失败集重跑 `_gen_data_mgmt.py` 清标记；③从 V11 狙击分段候选 / 5 万全投 / 历史快照 2.0→2.5 / SCREEN_POOL 时序 / 跨域 200 条里选一项再动代码。别碰＝`#sigFootNote` / `#view-smartmoney` / 七标签 DOM 顺序；V11 狙击 1260 日公式；资产配置 14 列与「实际市值」列名；`ledger-import.json`（IRR 真源）；日频 rrule 21:30。

## v1124 · 全量刷新 + 数据管理补齐 + 两处假绿修复（2026-11-26，index 5,369,472 B / master `9483e81b947c`；已发布，线上 v1124）

- **改了什么**：①全刷 `refresh_all.py`（8 组并行 + 16 串行，6m47s），数据刷新到 11-26；②前端 DMCONFIG 补登 `logic_state` / `v11_bt_data`（45→47，与生成器同源）；③修 `_audit_dm_v845.py` 漏判 `sameKeys` 的假绿；④按既定口径修 `_audit_last_sell_link.py`（T16 卖出后破位减半冲突以账户确认为准，两源差异降为显式 WARN，份额守恒/锚完整/时效仍 FAIL），012920 申请日 vs 确认日差异如实披露；⑤补 `SCRIPT_TO_DM` 映射，refreshFailed 修正为真实失败集 `['fund_jjcc','index_daily']`；⑥`gen_v11_signal.py` 写盘补 `newline=`。
- **未验证的假设**：`gen_index_bench`（腾讯 WAF 501 + 东财空）与 `gen_fund_jjcc`（HTTP 514 限频）是上游环境问题，本轮按设计保留旧值（index-daily 停 11-23、fund-jjcc 停 09-30），**未量化端点何时恢复**；`_audit_pe_chain_v846` 的 idx/bl 数据日差是 index_bench 失败的连锁，随其恢复而解；012920 两源的 16 天日期差究竟是 QDII 确认时滞还是对账单申请日误录，无法从现有数据裁决（已按生成器既定口径取账户确认为 T16 卖出后破位减半基准）。
- **下一步 + 别碰**：下一步＝①上游恢复后重跑 `python gen_index_bench.py` / `python gen_fund_jjcc.py` 并 `DM_FROM_CHAIN=1 REFRESH_BAD_STEPS=<真实失败>` 重跑 `_gen_data_mgmt.py` 清标记（禁手改 data/*.json）；②强刷线上验 v1124 / 47 项 / 失败标记可见；③012920 口径若需改台账，须另拍板（资金平衡/IRR 真源，本轮未动）。别碰＝`#sigFootNote` / `#view-smartmoney` / 七标签 DOM 顺序；V11 狙击 1260 日公式；资产配置 14 列与「实际市值」列名；ledger-import.json（IRR 真源，生成器红线禁止写）；日频自动化 rrule（21:30，唯一调度真源）。

## v1121 · V11 狙击补运行回测 + KPI 压成 5 列 + 赔率门限统一 2.50（2026-11-25，index 5,366,219 B / master `6cbc60c112dd`；新增 v11-bt-data 1,005,256 B）

- **改了什么**：`index.html` 徽标 v1121——①`v11StrategyHtml()` 原 `.sh-grid` 被 `#view-strategy .sh-grid{flex:1 1 320px}` 撑成 320px 高（用户截图的大空白），改专用 `.v11-kpi`（5 列、`min-height:0`、窄屏 2 列），1430 宽实测 5×216.53px、KPI 行高 58.85px、策略卡总高约 229px；②新增 V11 运行回测（`v11RunCardHtml` / `v11Prep` / `v11Calc` / `v11DrawChart` / `v11BtResultHtml` / `v11LoadBtData` / `v11Run`），默认 2,500 / 625 / 4 仓 / 2.50 / 3×ATR / 吊灯 0.20→0.85 / 申购 0.15% / 赎回 0.5% / 现金 2.25%，只回测狙击仓；③`gen_v11_bt_data.py` 生成 `data/v11-bt-data.json`（15 只 ETF OHLC / 1,005,256 B / asOf 2026-11-25），已进 `push_gh_v39.py`，`_gen_data_mgmt.py` 补 `v11_bt_data`（`手工轨（未挂链）`）并重建 `data-mgmt.json`；④门限统一 2.50：`gen_v11_signal.py` 显式 `odds_thr=2.5`，`v11-signal.json` / 扫描表 `≥2.50`，今日 3 只就绪（159949 3.47 / 513050 30.30 / 513180 14.58）名单不变；⑤SVG 曲线替代 ECharts canvas（截图/CDP 下 canvas 不可见）；⑥修 `v11FmtMoney` 负数 `¥-1`→`-¥1`、运行卡长标签换行、策略卡误写 `2.00</div>` 导致 check_js 块 10 FAIL。`docs/FRONTEND.md` 补 §10.19；README 升 v1121。
- **未验证的假设**：①赔率公式仍两套——扫描/运行回测＝1260 日窗口最低收盘，配置回测 `v11Gate`＝p250/3×ATR，规则注册表＝3×ATR14；本轮只统一门限 2.50；②运行回测默认 2,500/625/4 仓＝5 万策略池 5%，不是 5 万全投；③`v11-signal-hist.json` 前 20 个快照仍是 2.00 旧口径，未重算，也未标注；④宽屏 1900 未实拍（1430 CDP 与 532 已核）；⑤样本外 249 pending / 0 完成，不能当已实现收益。
- **下一步 + 别碰**：下一步＝①刷新线上 `?t=v1121live&final=1` 点一次「运行回测」验收；②拍板赔率公式是否统一（见 README 待决首条）；③决定是否要 50,000 本金全投口径；④宽屏 1900 实拍；⑤全量 gate 的 fund_monthly `DUALSOURCE=FAIL` 单独修。别碰＝`#v11RunWrap` 放运行结果、`#v11BtWrap` 放样本外，不要混；`v11DrawChart` 原生 SVG 不要改回 ECharts；`.v11-kpi` 不要改回 `.sh-grid`；`v11-bt-data.json` 只由 `gen_v11_bt_data.py` 生成；`v11Prep` 的 1260 日窗口与 `v11Gate` 的 p250/3×ATR 未拍板前不要单边改。

## v1120 · 交易信号页删除 V11 逐只执行行（2026-11-25，index 5,336,202 B / master `b3e2261f8c5c`；数据未动）

- **改了什么**：`index.html` 徽标 v1120 + tag `fw2_v1120_v11_rows_removed`——①`signalEvalAll()` 内原 `/* ② V11 狙击 → rows.screen */` 整段删除（`window.__V11_SIG__` 读取、`loadV11Signal()` 兜底、`rows.screen.push` 的 V11 行与互斥标注全部删）；②`renderSignalDash()` 内 `loadV11Signal()` 调用删除，信号页不再请求 `v11-signal.json`；③信号页 `_v11MoveLine` 改「本页不再列 V11 逐只执行行，扫描与执行都在策略页」；④`v11StrategyHtml()` 卡内文案同步；⑤`LOGIC_WHERE.V11` 去掉「交易信号逐只执行行」。`docs/FRONTEND.md` 补 §10.18；README/frontmatter 升 v1120。
- **未验证的假设**：①线上 5.3MB 页面首次 `wait_for_load` 仍超时但内容可读（本轮已用 DOM 直读）；②扫描门限 `2.00`（`v11-signal.json` 自带）与策略/回测 `2.50`（`C.v11Odd`）仍未拍板，本轮未改生成器/参数；③宽屏 1900 未实拍（本地/线上均只验 538 视口）；④`v11-signal.json` 未重跑，仍是 `asOf=2026-11-23` / 15 只 / 3 就绪。**发布异常说明**：脚本对未改动的 `caifu/data/meta-bundle.json` 报 422（contents GET 瞬断被误判 NEW，PUT 缺 sha）；随后 GitHub API 查得远端 sha=`3adf781cf954`、834,572 B 仍存在，未改该文件，index 已按 expected 推送。
- **下一步 + 别碰**：下一步＝①你刷新线上页验收「交易信号无 V11 行、策略页仍有」；②拍板门限 2.00/2.50 以哪边为准，改生成器要重跑信号+样本外，改 `C.v11Odd` 要重跑回测；③宽屏 1900 实拍；④全量 gate 的 fund_monthly 既有 `DUALSOURCE=FAIL` 单独修。别碰＝V11 策略页 `v11StrategyHtml()` / `renderStratV11()` / `#stp-v11` 是唯一入口与唯一数据加载点；不要把 `loadV11Signal()` 接回信号页；不要删 `v11SignalHtml()` / `v11BtHtml()`；`data-st="v11"` 不改名。

## v1119 · V11 狙击迁入策略执行（2026-11-25，index 5,338,041 B / master `2389e776e324`；数据未动）

- **改了什么**：`index.html` 徽标 v1119 + 注释块 `fw2_v1119_v11_strategy_tab`——①`#stratTabs` 增 `data-st="v11"` 的「V11 狙击」第 6 个子页与 `#stp-v11`，新增 `v11StrategyHtml()` / `renderStratV11()`，策略卡输出 5 万预算 / 池 5%＝¥2,500 / 单注 ¥625 / 4 仓 / 2.50 门限 / 3×ATR / 吊灯 0.85，下方复用 `#v11Wrap` 与 `#v11BtWrap`；`__stratActiveTab` / `__stratPaneRender` / `switchStratTab` 接 v11。②交易信号 `_sigTabBtns` 删 V11 tab，`renderSignalDash()` 加 `_v11MoveLine` 指路条，`loadV11Backtest()` 不再无条件加载；v1119 当时逐只执行行仍由 `loadV11Signal()` 供给（**v1120 已删除**）。③赔率由百分比乘 100 改 `num2()` 两位小数倍数；扫描表加 `table-wrap` 横向滚动；`#stratTabs` 538 视口 7 tab 单行；`v11-signal.json` 的 2.00 与策略 2.50 不一致处加琥珀提示。`docs/FRONTEND.md` 补 §10.17；README/frontmatter 升 v1119。④**发布后自查**：`verify_sync --gh-only` 抓到 `index.html` 缺 v606 的 `隔离铁律` 标记（否则 rc=1），已在 `v11StrategyHtml()` 注释补回并重发 master `2389e776e324`；`_audit_plan_merge_v895.py` 的 A01 正则原 `[a-z]+` 认不出 `v11`，改为 `[a-z0-9]+` 并升「现役 7 tab」，新增 A01e 锁 `#stp-v11` + 两个函数，40/40 PASS。
- **未验证的假设**：①~~「策略页承载本体 + 信号页保留逐只执行行」尚未确认是否连筛选信号里的 V11 行也去掉~~ → **2026-11-25 用户选「删除」，v1120 已删除**；②扫描门限 `2.00` 与策略/回测 `2.50` 哪边为准未定，本轮只做页面提示，未改 `gen_v11_signal.py` 或 `C.v11Odd`；③宽屏 1900 未实拍（截图视口 538）；④策略卡 KPI 在窄屏为 3+2 两行，未做 5 列等高压缩；⑤V11 样本外仍 0 完成 / 236 积累中，不能当已实现收益。
- **下一步 + 别碰**：下一步＝①你验收归属与「信号页只留指路条」；②拍板门限 2.00/2.50 以哪边为准，改生成器则重跑信号+样本外，改 `C.v11Odd` 则重跑回测；③宽屏 1900 实拍；④全量 gate 的 fund_monthly 既有 `DUALSOURCE=FAIL` 单独修。别碰＝`data-st="v11"` / `#stp-v11` 不改名；`v11StrategyHtml()` / `renderStratV11()` 是唯一策略入口；`v11SignalHtml()` / `v11BtHtml()` 不复制第二套；`#v11Wrap` / `#v11BtWrap` 仅策略页使用；**v1120 起 `loadV11Signal()` 只在策略页调用，不要接回信号页**。

## v1118 · 5 万策略口径写进页面文案（2026-11-25，index 5,332,217 B / master `603513e366b0`；数据未动）

- **改了什么**：`index.html` 徽标 v1118 + 注释块 `fw2_v1118_capital_labels`——①V11 注册表 `def` 池 10%→5%（策略口径 5 万→¥2,500），`thr` 由 `C.v11Pct` 现算并加「回测按回测预算」；②`ruleCardHtml()` 标题加「口径：独立实验 · 不并入 5 万策略基准」chip，chips 下加黄框「资金口径」说明；③`termCardHtml()` 标题加「口径：独立实验 · 10 万 / 每档 2 万」chip，`termPoolHtml()` 副标题改「独立实验…」，`termBodyHtml()` 卡底加资金口径一条。`docs/FRONTEND.md` 补 §10.16；README/frontmatter 升 v1118。
- **未验证的假设**：①V11 `thr` 的「策略口径 5 万→¥2,500」是静态换算 5 万×`C.v11Pct`，未接 `STRATEGY_SNAP.totalTarget` 动态读取；若以后策略总额改离 5 万，这句话不会自动跟（但回测预算本来就是另一套，故未强行统一）；②深跌买入/终止样本参数仍 10 万与 2 万，未按 5 万重算，用户是否希望重算未确认；③宽屏 1900 未实拍（截图视口 538）；④线上页面 5.3MB，首次 `wait_for_load` 仍可能超时但内容已可读。
- **下一步 + 别碰**：下一步＝①拍板 T4 硬止损/R2 定投/全球成长 56.44% 再决定行为改动；②若要把「同日优先级 / act 执行状态」落地，另开一版，不在本版文案范围；③全量 gate 的 fund_monthly 既有 `DUALSOURCE=FAIL` 单独修。别碰＝`__DD_STATE` 仍 10 万/5,000；`index-term` 仍 10 万/2 万；V11 `thr` 的 2,500 必须随 `C.v11Pct` 算；`v971 池 10%` 历史注释保留。

## v1112 · 深跌买入补「区间曾深」+ 全池59（逐日机会）（2026-11-25，index 5,319,514 B / master `42e3a4261b8e`；数据未动）

- **改了什么**：`index.html` 徽标 v1112 + 注释块 `fw2_v1112_dd_hist_allpool`——A 监测卡加「区间曾深」切换（`ST.hist` / `histStatOf` / `histRows` / `histCardHtml`），按区间此前最高收盘列出 16 只曾≥70%、5 只已修复到 <60%；B 回测加第三档「全池59（逐日机会）」（`allPoolCodes`；`runPoolBT` 拆 `buyTiers/sellOne`，全池同日先卖后买、按当日回撤深→浅分配，跳档计数）。同轮修 `byTbl` 计数优先级 bug、参数三段 ternary 改为 `noteTxt`、scope 切换清旧结果、全池点行切单指数、历史窄屏 1px 横滑。`docs/FRONTEND.md` 补 §10.13；README/frontmatter 升 v1112。
- **未验证的假设**：①全池与历史表都只用**今天存续的 63 只**，未覆盖退市/改名指数，仍有幸存者偏差，不能当完整历史成分池；②全池 +74.82% 是「今天这 59 只、共享 10 万、每档 2 万」的规则结果，跳过 73 档，未做每档按本金比例自适应；③宽屏 1900 未实拍（截图视口固定 538）；④历史表阈值随 `start0()` 动（默认 70%），未固定 70%；⑤全池模式点表行改为切该指数单指数，是否合你操作习惯未确认。
- **下一步 + 别碰**：候选＝①历史表固定 70% 阈值；②补历史成分池（需新源）；③全池每档按本金比例；④历史表点行切单指数；⑤宽屏实拍。别碰＝`histStatOf` 必须先扫全序列再限定区间（峰值可早于起点）；`all` 的「同日深→浅、先卖后买」；默认 10 的 look-ahead 文案；4 只境外永不进组合池；`byTbl` 不要再用 `split('<tr>').length-1` 拼字符串。

## v1111 · 深跌买入焦点只看接近 70% + 买入区前移 + 组合默认最深 10（2026-11-25，index 5,309,303 B / master `b3c0abcdce81`；数据未动）

- **改了什么**：`index.html` 徽标 v1111 + 注释块 `fw2_v1111_dd_focus_reorder` / `fw2_v1111b_pool_focus`——新增 `focusMinDD()`＝起始−10pp（默认 70%→≥60%）、`focusOn/inFocusDD/effectivePick`；监测/分档/跨档/估值/单指数下拉/组合候选全部按焦点过滤，63→17 只；买入区卡前移到口径卡之后、参数卡之前并加红边；单指数下拉 17 只深→浅；组合默认 pick 改 `deepCodesOf(10)`，候选 chips 16 只境内焦点；焦外已选显式提示且本次回测不参与；默认最深 10 加 look-ahead 提示。`docs/FRONTEND.md` 补 §10.12。
- **未验证的假设**：①「接近 70%」取起始−10pp（默认 ≥60%）是按既有「60–70% 接近档」推的，**未获用户最终确认**；若用户意思是「严格 ≥70%」，只需把 `focusMinDD` 改成 `start0()`，代价是只剩 4 只、60–69% 会被隐藏；②默认最深 10 是**当前时点**事后选池，回测 +35.83% 含选择偏差（已在脚注标明），未做「区间起点时最深 10」；③宽屏 1900 未实拍（截图视口固定 538）；④起始 80% 时焦点只剩 4 只、组合默认 10 会有 6 只焦外不参与（已按 `effectivePick` 处理并提示），但未逐档实拍所有起始值。
- **下一步 + 别碰**：候选＝①焦点下界可选（10pp / 5pp / 仅 ≥70%）；②组合默认池增加「起点时最深 10（无 look-ahead）」；③买入区加「本笔拟买金额」列；④焦点切换记忆 localStorage；⑤宽屏 1900 实拍。别碰＝`focusMinDD` 必须跟 `start0()`；`ST.pick` 不因隐藏而删（只让 `effectivePick` 过滤回测入参）；`all` 是全池真相（估值同类中位仍用它）；4 只境外永不进组合池；look-ahead 文案不能删。

## v1110 · 核算块折叠 + 跨档日期标签对齐（2026-11-25，index 5,299,713 B / master `43894366a2ff`；数据未动）

- **改了什么**：`index.html` 徽标 v1110 + 注释块 `fw2_v1110_calc_fold_cross_date`——`calcHtml` 改原生 `details.dd-calc`（summary、默认收起、点击展开 15 项）；跨档表头「今日回撤/今日档位」→「最新回撤/最新档位」，末列「对比日」→「数据日 / 对比日」输出双日期，标题注明各行按自身最新交易日对比；`docs/FRONTEND.md` 补 §10.11。
- **未验证的假设**：①纳指/标普 11-20→11-23 的 +6.86% / +4.73% 与库内两根收盘自洽，但独立第二源未取到（腾讯 K 线 501、stooq JS 验证），是否源数据异常未下结论；②宽屏 1900 未实拍；③折叠态刷新即回默认（未做记忆）。
- **下一步 + 别碰**：候选＝①折叠状态记忆 ②境外行加「T-1」标签 ③数据日拆独立列 ④宽屏实拍。别碰＝跨档 p1/p0 与档位算法（不能为对齐 11-24 改口径）；`colspan=10` 与 10 列同步；核算 `<details>` 默认不要加 `open`。

## v1109 · 胜率后补「赔率」KPI（2026-11-25，index 5,298,312 B / master `5e58a3f7f5f1`；数据未动）

- **改了什么**：`index.html` 徽标 v1109 + 注释块 `fw2_v1109_payoff_ratio`——新增 `payoffOf(R)`；KPI 10→11 格，胜率后加「赔率」（平均盈利÷平均亏损）；核算块 14→15 项补一行（盈/亏笔数、合计、均值、算式）。`docs/FRONTEND.md` 补 §10.10。
- **未验证的假设**：①赔率口径按「平均盈利÷平均亏损」（金额、不加权），未与用户确认是否要「总盈利÷总亏损」的 profit factor；②样本仅 1 胜 1 负，14.05 波动极大，未做置信区间；③「0 胜」分支只做代码兜底，未造样本实拍；④宽屏 1900 未实拍。
- **下一步 + 别碰**：候选＝①胜率×赔率＝单笔期望值一行 ②赔率年化（与 XIRR 部分重复）③进投资总纲提示条 ④参数已变淡提示。别碰＝KPI 与核算必须共用 `payoffOf`（初版各算一套曾导致结果卡 0 格）；`odds` 不要用 `R.win` 反推笔数；赔率只读 trades、不参与买卖判定。
## v1108 · 回测补「投入资金口径」：投入资金收益率 + XIRR（2026-11-25，index 5,295,955 B / master `1b18abde1d4a`；数据未动）

- **改了什么**：`index.html` 徽标 v1108 + 注释块 `fw2_v1108_invested_basis`——新增 `effOf(R)`（现金流、累计投入、平均占用、利用率）与 `irrOf(fl,t0)`（扫描变号 + 二分，act/365）；KPI 8→10 格加「投入资金收益率 +6.41%」「资金加权年化 +9.96%」，账户口径改标「总资金」；核算块 11→14 项补投入口径三行。`docs/FRONTEND.md` 补 §10.9。
- **未验证的假设**：①平均占用用日历天数（710 天合计）与引擎年数「交易日÷244」不同源，两者都保留但未统一；②XIRR 的空值分支（现金流无变号）只做代码兜底，未造样本实拍；③「累计投入」为各笔买入之和，若卖出回款再买入会重复计，已写进文案但仍可能被当成「总投入本金」；④宽屏 1900 未实拍。
- **下一步 + 别碰**：候选＝①资金利用率进投资总纲提示条 ②「尚未回款」文案 ③参数已变淡提示 ④是否单列 TWR。别碰＝`effOf` 只读 R、XIRR 不反写引擎；平均占用必须用日历天数（`t.days` 是交易日）；账户口径「总资金口径」文案不能删。
## v1107 · 结果卡内逐项指标核算过程（2026-11-25，index 5,291,633 B / master `48d82fdb5b65`；数据未动）

- **改了什么**：`index.html` 徽标 v1107 + 注释块 `fw2_v1107_result_calc`——新增 `calcHtml(R)`，在 KPI 网格下、净值曲线前输出 11 项核算（本金/每档、总资产拆现金+市值、盈亏、收益率、年化含年数口径、最大回撤含峰谷日期、胜率、平均仓位、买卖、单笔实例、手续费；组合换参与/触发）。同时修自查发现的真 bug：MDD 峰值日期原取「最新峰值」导致与谷底日期倒挂，现记录该次回撤的前高日期 `pkWD`。`docs/FRONTEND.md` 补 §10.8。
- **未验证的假设**：①宽屏 1900 未实拍，长文本行宽/留白未检；②组合口径交易日数取曲线轴长度（各指数日期并集），未逐只核对停牌日差；③平均仓位/最高仓位直接采信引擎 R.avgPos/R.maxPos，未用 curve 独立重算一遍（仅抽 5.02% 等值目测合理）；④年化单指数用 244 天/年、组合用 365.25 天/年两套引擎既有口径，未与用户确认是否统一。
- **下一步 + 别碰**：候选＝①「参数已变，重新运行」提示 ②净值曲线横轴四位年份 ③分档「PB 分位最低」④最深 N 记忆 ⑤估值 PE/PB 双低排序 ⑥买入区「本笔拟买金额」。别碰＝`calcHtml` 只读 R；MDD 峰谷日期存前高；年数口径勿混；公式文字改动后必须与 KPI 逐项对拍（本轮对拍 103,845 / +3,845 / +0.38% / −11.64% / 50.0% / 3.80% / 3-2 / ¥0）。
## v1106 · 回测结果紧跟档位回测（2026-11-25，index 5,284,821 B / master `7957b87812f3`；数据未动）

- **改了什么**：`index.html` 徽标 v1106 + 注释块 `fw2_v1106_result_under_param`——`shellHtml()` 把 `resultHtml(window.__DD_RES)` 从页尾移到「档位回测」卡之后（顺序＝口径 / 档位回测 / 回测结果 / 跨档 / 买入区 / 监测 / 估值）；`doRun()` 替换 `#ddResultCard` 后 `scrollIntoView({block:'nearest',behavior:'smooth'})`，跑完结果直接进视野。`docs/FRONTEND.md` 补 §10.7。
- **未验证的假设**：①宽屏（1900）未实拍，只核对窄屏 538 的 KPI 四列换行与滚动落点；②`scrollIntoView` 在真机上 `behavior:'smooth'` 与底部固定导航的相对表现未逐机型验证（本机 bu 视口无固定导航）；③参数改动后旧结果卡保留旧参数自述，未加「参数已变」提示（用户可能误以为已更新，属候选改进）。
- **下一步 + 别碰**：候选＝①「参数已变，重新运行」淡提示 ②分档补「PB 分位最低的一只」③「最深 N」记忆 localStorage ④估值 PE/PB 双低排序 ⑤买入区「本笔拟买金额」列 ⑥参数一键复位。别碰＝`doRun()` 仍靠 `#ddResultCard` 就地替换（别改成整模块重画，会丢图表实例与滚动）；参数改动仍整块重画；结果卡必须紧跟 `paramHtml()`，别被顺手排回页尾。
## v1105 · 深跌买入显示顺序（方案 A）（2026-11-24，index 5,283,743 B / master `6fda767fca9a`；数据未动）

- **改了什么**：`index.html` 徽标 v1105 + 注释块 `fw2_v1105_dd_order_a`——`planCardHtml()` 拆为 `planParts()` / `ruleCardHtml()` / `buyCardHtml()`；口径卡压成一行 chips + 原生 details 折叠；`shellHtml()` 顺序改为 口径 → 参数区 → 跨档 → 买入区 → 监测+分档 → 估值 → 回测结果；参数改动（scope/gap/startDD/perBuy/capital/obs/back）整块重画并 `scrollTo` 回原位；修 `planParts()` 写死 `>=70` 的 bug（改起始回撤清单不动，实测 70→65 时 4→10 只）。`docs/FRONTEND.md` 补 §10.6 顺序与联动口径。
- **未验证的假设**：①宽屏只做列宽核算（截图视口固定 538，未实拍宽屏，`details` 展开后 940px 口径表在窄屏需横滑，宽屏未拍）；②`details` 展开态不持久（刷新收起，属有意，未与用户确认是否要记忆）；③买入区「接近 10pp」我按 `start-10 ~ start` 算，与监测表状态列同口径，但若起始回撤调到很低（如 30%），接近档会覆盖 20–30%，语义仍成立、未逐档实拍。
- **下一步 + 别碰**：候选＝①分档补「PB 分位最低的一只」②「最深 N」记忆 localStorage ③估值 PE/PB 双低排序 ④买入区加「本笔拟买金额」列 ⑤参数一键复位 ⑥已进档位/持有笔数进投资总纲。别碰＝参数改动必须整块重画（别再只刷 `ddXHost`）；买入区阈值走 `start0()`；`details` 里的四列口径表别改成窄屏自适应列宽（会重演 v505 列错位）。
## v1104 · 深跌买入六项全做（2026-11-24，index 5,280,195 B / master `9397c3453b72`；数据未动）

- **改了什么**：`index.html` 徽标 v1104 + 注释块 `fw2_v1104_dd_pb_tier_narrow2_deepn_progress`——①分档汇总加「PB 分位中位」（`pbs` 中位、有源只数；宽屏 9 列 / 窄屏 6 列）；②监测表「档位」表头可点排序，`ST.sort='tier'`＝档位深→浅 + 同档距下档少→多（`listCardHtml` / `planCardHtml` 两处 comparator 同源，排序行补第 5 颗按钮）；③`valCardHtml()` 窄屏 9→5 列（424px）；④`readJsonProgress()` 流式 reader 显示「已下载 x.xxMB / 约 4.13MB（n%）」，改用未压缩基准（GitHub Pages gzip 的 Content-Length 实测 1.44MB，会算成 3 倍）；⑤`ST.deepN` + `[data-dd-deepn]`（3–30，两个选池按钮共用；N=10 交集 1 只、N=20 交集 5 只）；⑥`docs/FRONTEND.md` §10 写入口径。另把审计 `_audit_plan_merge_v895.py` A01d 断言由「回撤档位」同步为「深跌买入」（v1103 改名后该闸门一直 FAIL，本轮才暴露）。
- **未验证的假设**：①宽屏布局只做静态列宽核算（分档 940 / 估值 1010），本机与线上截图视口固定 538，宽屏未实拍；②骨架屏进度在 <1s 的快网下几乎一闪而过，线上实测只能看到 5% / 80% 两个瞬间；③进度基准写死 4,330,804 B（`index-dd.json` 当前大小），若重生成数据文件需同步该常量，否则百分比会偏；④「档位」排序同档内再按距下档排，是我对「档位排序」的理解（否则与默认回撤排序完全同序、等于没效果），未与用户确认。
- **下一步 + 别碰**：候选＝①分档补「PB 分位最低的一只」②「最深 N」记忆到 localStorage ③估值卡 PE/PB 双低排序 ④方案卡「未进区最少还差」摘要条 ⑤参数一键复位 ⑥「已进档位 + 持有笔数」进投资总纲提示条。别碰＝三处排序（按钮 / `all.sort` / `hit.sort`）必须同步；`pePct`/`pbPct` 是 0–1 小数、`div` 已是百分数；窄屏阈值只走 `paneNarrow()`；`data-st="dd"` 与 `__DD_STATE` 不动。
## v1103 · 子页签更名「深跌买入」（2026-11-24，index 5,273,313 B / master `b00a9df4c6c5`；数据未动）

- **改了什么**：`index.html` 徽标 v1103 + 注释块 `fw2_v1103_dd_rename` / `fw2_v1103_dd_rename2`——`#stratTabs` 的 `data-st="dd"` 按钮「回撤档位」→「深跌买入」；`planCardHtml()` 卡头 →「深跌买入 · 指数回撤分档、越跌越买」；`mount()` 骨架屏、`ddLoading`、`load()` 失败卡头三处同步；`data-st="dd"`、`#stp-dd`、`__DD_STATE`、`__DD_DATA` 与全部取数/回测口径未动。
- **未验证的假设**：①只改了中文展示文案，`?tab=dd` 这类深链（若有）与 localStorage 里的 `__DD_STATE` 不受影响，未逐条实测深链；②窄屏下 tab 行 6 颗含「深跌买入」4 字，实测 538 视口换行正常，更窄（<380）未测；③文档与历史注释里仍保留「回撤档位」字样（版本史引用），属有意保留，不是漏改。
- **下一步 + 别碰**：下批候选＝分档「PB 分位中位」/ 监测表「档位」排序 / 估值表窄屏收列 / 骨架屏进度 / 交集阈值可调 / 把口径写进 `docs/FRONTEND.md`。别碰＝`data-st="dd"` 与 `__DD_STATE`（改名只动文本节点）；`pePct` 是 0–1 小数、`div` 已是百分数。

## v1102 · 分档股息率中位 + 便宜又深交集 + 距下档排序 + 窄屏紧凑列 + 预取骨架屏（2026-11-24，index 5,272,651 B / master `e13b5dfc57b7`；index-dd / index-val 未动）

- **改了什么**：`index.html` 徽标 v1102 + 注释块 `fw2_v1102_dd_div_mix_n2_narrow_prefetch`——`bkSum` 增「股息率中位」列（`div` 中位＋有源只数，窄屏 5 列 / 宽屏 8 列）；`cheapCodesOf()` / `deepCodesOf(n)` / `normPick()` 抽成单一实现，新按钮 `[data-dd-pickmix]`「只选便宜又深」取两者交集；`ST.sort` 加 `n2` 第四态（`[data-dd-sortn2]` 表头 + `data-dd-sort="n2"` 按钮 + 方案卡跟随）；`narrow`（面板宽 <700）分支把监测表收到 6 列、状态列改短词 + 「还差 x.xpp」副行，分档汇总 5 列，新 CSS `.dd-tbl--nar` / `.dd-skel`；`mount()` 未加载态先画骨架屏，IIFE 末尾 `prefetchDD()` 后台预拉两份 JSON；`ensureDefaults()` 池门槛 2→1（修「交集只有 1 只被重置回宽基」）。
- **未验证的假设**：①窄屏阈值口径是 `#stp-dd` 的 `clientWidth < 700`（不是 window.innerWidth），换侧栏折叠宽度时会跟着变，未穷举所有宽度；②「便宜又深」交集现算的是「同类别 PE 分位低于中位 ∩ 回撤最深 10」，两个集合各自独立、未做加权，交集只有 1 只属数据事实而非 bug；③骨架屏只在 `D` 未到时出现，若预取已完成则直接出表，骨架屏路径在快网下几乎看不到（弱网/强刷才可见）；④预取会多占一次 4.4MB 流量（首访即有），换来点入即用，未做「仅当日一次」的服务端缓存标记。
- **下一步 + 别碰**：第一步等你选子页签新名（候选：分档买入 / 回撤分批 / 深跌建仓 / 金字塔买入），改名只动展示层，别动 `data-st="dd"`、`__DD_STATE`、`__DD_DATA`。别碰＝`pePct` 是 0–1 小数（乘 100 才展示）、`div` 已是百分数（不要再乘 100）、窄屏分支靠 `narrow` 一处开关（不要散落写 media query）、`ddRefreshSoft` 的搜索聚焦跳过逻辑。

## v1101 · 分档汇总加 PE 分位最低 + 组合池只选回撤最深 10 + 回撤表头点击排序（2026-11-24，index 5,263,647 B；index-dd / index-val 未动）

- **改了什么**：`index.html` 徽标 v1101 + 注释块 `fw2_v1101_dd_pe_pickdeep_sortdd`——`listCardHtml()` 的 `bkSum` 增 PE 分位列（`(peMin*100).toFixed(1)`，`pePct` 是 0–1 小数）；`ddTbl` 监测表「回撤」th 带 `data-dd-sortdd` 与 CSS `th.dd-thsort`；`pickHtml()` 增 `[data-dd-pickdeep]` + `bindHost()` 分支；`ST.sort` 扩 `ddasc` 三态（`listCardHtml`/`planCardHtml`/脚注/按钮组）；新增 `ddRefreshSoft()` 供 `loadVal()` 两处 then 调用（修 v1100「估值到达后分档 PE 列与便宜一半计数不刷新」）；`__stratPaneRender` 的 dd 分支改为「脚本未就绪 → 400ms 重试、不置 done」（修线上首屏永久空白）。
- **未验证的假设**：①「PE 分位最低的一只」按同档内最低，样本随分档 4–16 只，极端档（≥70%）只有 4 只且 3 只无 PE 分位（房地产/基建/港股通互联网），实际只在传媒一只上有数，这条口径是否够用未与你确认；②「只选回撤最深 10」是固定 10 只（不做 N 可调），与「只选便宜一半」并列时两者交集未做；③线上首屏空白真因是脚本未解析完就点进来且 `__stratPaneDone` 被锁定，已改为 400ms 重试；重试后线上实测约 15s（4.3MB 数据下载）才出表，弱网下仍偏慢，未做预取/骨架屏；④`ddRefreshSoft` 在搜索框聚焦时跳过重画，因此「边输入边到达」的场景下分档 PE 列会保持「未加载」直到失焦；未做逐帧比对，仅代码路径判断。
- **下一步 + 别碰**：下一步候选＝分档汇总加「该档股息率中位」、组合池「便宜一半 ∩ 回撤最深」交集、监测表「距下档」表头排序、窄屏隐藏次要列。别碰＝`pePct` 是 0–1 小数（乘 100 才展示）、`ddRefreshSoft` 的聚焦跳过、最深 10 只算境内且按 indices 归一、汇总表不跟随搜索/快捷、`toNextOf`/`medOf` 单一实现。

## v1100 · 分档汇总表 + 只选便宜一半 + 相对同类三态排序（2026-11-24，index 5,258,900 B；index-dd / index-val 未动）

- **改了什么**：`index.html` 徽标 v1100 + 注释块 `fw2_v1100_dd_bksum_cheap_vsort`——`medOf()` 抽模块级；`listCardHtml()` 增 `bkSum` 分档汇总（minW 828）；`pickHtml()` 增 `cheapCodes`/`[data-dd-pickcheap]`；`valCardHtml()` 增 `relOf()`/`arrS`/`[data-dd-vsort]`；`ddTbl` 支持 `cols[i][3]` 作为 th 属性。
- **未验证的假设**：①「便宜一半」按同类别中位分界，样本只有 3–10 只（境外 3、主题 5），选中 10 只里宽基 5 / 行业 3 / 主题 2，分布不均属预期但未与「按全体 63 只统一分位」口径对比优劣；②分档汇总的「已进买入区」列在 60–70% 及以下必为 0（起始回撤 70%），属定义使然而非缺陷，未验证用户是否会误读；③`ddTbl` 新增的第 4 个可选元素只被估值主表用到，其余老调用回退兼容已跑过全页渲染，但未逐表断言行高/对齐未变。
- **下一步 + 别碰**：下一步＝汇总表加「该档 PE 分位最低的一只」、组合池「只选回撤最深 N 只」、主表回撤列排序。别碰＝`medOf` 单一实现、汇总表不跟随搜索、`vsort` 无分位行排末位。

## v1099 · 组合池类别批量 + 估值「相对同类」+ 跨档卡跟随类别（2026-11-24，index 5,252,979 B；index-dd / index-val 未动）

- **改了什么**：index.html 徽标 v1099 + 注释块 fw2_v1099_dd_pickcat_relcat——catBtns/[data-dd-pickcat]（按类别全选或取消、按 indices 顺序归一）；valCardHtml() 增 peMedCat 与「相对同类」列（9 列、minW 1010、|差|≤0.05pp 灰）；crossCardHtml() 改用 srcC 并加 catTag。
- **未验证的假设**：①类别批量取消到少于 2 只时会被 ensureDefaults 重置为宽基默认——只验证了「取消主题后仍 20 只」这一路，未验证「取消到 1 只」的边界（按代码应回落宽基）；②「相对同类」用同类别分位中位作基准，样本只有 3–10 只（境外 3、主题 5），中位对极端值不敏感但样本小，结论只宜做横向参照；③跨档卡跟随类别后，staleTxt 仍是全量 63 只的陈旧提示（有意保留），未验证「类别内无 stale、但全量有 stale」时读者是否觉得突兀。
- **下一步 + 别碰**：下一步＝分档汇总表、组合池按 PE 分位低半选、相对同类列可排序。别碰＝ensureDefaults 的 <2 只兜底、peMedCat 只统计有分位只数、跨档卡 stale 全量提示。

## v1098 · 快捷「距下档 ≤2pp」+ 对照表 8 列 + 方案卡跟随排序（2026-11-24，index 5,249,292 B；index-dd / index-val 未动）

- **改了什么**：`index.html` 徽标 v1098 + 注释块 `fw2_v1098_dd_n2_sort`——新增 `toNextOf()`、`ST.n2` 与 `[data-dd-n2]` 快捷行（四层过滤叠加）；`valCardHtml()` 的 `refRows` 增加 `dv` / `lowB`，对照表 6→8 列（minW 1036）；`planCardHtml()` 的 `hit` 改读 `ST.sort`。
- **未验证的假设**：①`toNextOf` 与跨档卡的 `nextPp` 是两处独立实现（公式同义），只对拍过「快捷 16 只」与跨档卡 15 只未跨档的差集（差的那只是当日跨档的纳指100），未做 63 只逐只公式对拍；②对照表 8 列在 538 视口需横向滑动（桌面宽屏应一屏显示，未在 ≥1280 实机目视）；③「股息率中位」只覆盖蛋卷有 `div` 的只数，与 PE 分位覆盖集不完全相同，未逐只核覆盖差集。
- **下一步 + 别碰**：下一步＝组合池按类别批量勾选、估值主表加「同类 PE 分位差」列、跨档卡跟随类别筛选。别碰＝`toNextOf` 单一口径、`ST.n2` 不进 `buckets`/`ST.pick`、对照表空组必须 `—`。

## v1097 · 监测卡排序开关 + 估值卡同类别对照（2026-11-24，index 5,246,710 B；index-dd / index-val 未动）

- **改了什么**：`index.html` 徽标 v1097 + 注释块 `fw2_v1097_dd_sort_valref`——`ST.sort` 两态 + `[data-dd-sort]` 按钮行（`listCardHtml()` 开头排序、只改显示顺序）；`valCardHtml()` 新增 `_med()`/`refRows` 与 6 列「同类别对照」小表（minW 822）。数据与生成器一行未改。
- **未验证的假设**：①`localeCompare(...,'zh-Hans-CN')` 在本机 Chrome / 内嵌浏览器与移动端排序一致（只实测了内置浏览器一种环境）；②对照表「PE 分位中位」只覆盖蛋卷 24 只（PE 分位仅这 24 只有），同名行显示「PE 分位 24」是口径差异而非漏算；③未做「排序 + 类别 + 分档 + 搜索」四者同时生效的组合穷举（只测了排序与搜索各自独立与排序切换）。
- **下一步 + 别碰**：下一步＝估值对照加 PB 最低 / 股息率中位，监测卡把「距下档 ≤2pp」做成一键筛选，方案卡跟随 `ST.sort`。别碰＝`ddArrOf`/`runBT`/`runPoolBT` 口径、`ST.sort` 不得进入 `buckets` 计数与 `ST.pick`、`_med` 空组必须回 `—`。

## v1096 · 三条补源路证伪 + 搜索/组合池全选 + 两处静默隐患（2026-11-24，index 5,243,006 B / index-dd 4,330,804 B）

- **改了什么**：`index.html` 徽标 v1096 + 注释块 `fw2_v1096_dd_search`（监测卡搜索 `ST.q`、组合池 `data-dd-pickall/pickd`、脚注境外名单现算）；`gen_index_dd.py` 去掉 `count.night`（并同步删掉 index-dd.json 的该键，4,330,804 B）；`gen_index_val.py` 新增 `dj_asof()` 替换写死的 `'2026-'`。
- **未验证的假设**：①中证估值 403 是限频还是长期封禁——只观察到「连 000300 也 403 且隔几分钟仍 403」，未排除长期封禁，也没有用代理绕；②搜索是前端过滤，63 行全在 DOM（首屏渲染耗时未重测，v1096 前后差异应可忽略）；③`全选境内 59` 后跑组合回测的极端情形（59 只争一个资金池、多数档位跳过）只确认能出结果，未核对逐笔明细。
- **下一步 + 别碰**：下一步＝中证估值恢复后重试 931637/000823；等可用汇率源再谈境外进池。别碰＝`.dd-pickall` 的境外过滤、搜索不得影响分档 `buckets`、`ensureDefaults` 的 `cat==='境外'` 过滤。

## v1095 · 全指数 45→63（补境外 4 + 14 只断尾 A 股）+ 估值卡全列（2026-11-24，index 5,240,314 B / index-dd 4,330,814 B / index-val 17,708 B）

- **改了什么**：`edit_work/gen_index_dd.py` 重写为 63 只（IDX 表加 `plan/sina_symbol/csi_code/xq_symbol`；新增 `xq_series()` 雪球取数、`csi_series()` 丢弃 2000-01-01 占位行、`merge()` 重叠校验）→ `data/index-dd.json` 4,330,814 B / 63 只；`edit_work/gen_index_val.py` 扩到 63 只（`hasPe/hasPb/total` 字段）→ `data/index-val.json` 17,708 B；`edit_work/index.html` 徽标 v1095 + 注释块 `fw2_v1095_dd_overseas`（类别加「境外」、副题口径、境外行补市场名、跨档展开 63、陈旧提示改现算、估值卡全列、境外不进组合池 + 参数卡币种提示）。交付前线上核对发现估值卡脚注仍写死「蛋卷 8 只 / 带※ 5 只」，与 63 只全列矛盾，已改为「蛋卷 24 只 / 带※ 32 只 A 股指数」并重推（index 5,240,328 B，master `b7f14f3b8862`，README head `19cc74862881`）。
- **未验证的假设**：①63 只的「宽基/行业/主题/境外」分类仍是人工归类（中证一级行业自有口径，这里是约定俗成）；②雪球与新时/中证的重叠同值率：000300 对新时 96.7%（差异多为末位小数）、932000/931775 对中证官网 100%，但**未对 63 只逐只做同值率统计**（合并只拦「差>0.01 的比例>10%」，通过即视为同一条序列）；③境外「历史最高」依赖雪球序列起点（恒指 2002-10、纳指/标普 2003-01），起点之前的极值（如恒指 2007 之前）不在窗口内；④4.33 MB 的 index-dd.json 在移动端首次加载耗时未实测。
- **下一步 + 别碰**：下一步＝补估值 7 只（需第三方源）/ 接汇率再让境外进组合池 / 试 日经225·DAX·KOSPI 的雪球前缀。别碰＝`ddArrOf` 回撤口径与 `runBT/runPoolBT` 买卖判定；`xq_series` 的时间戳换算（`ts/1000+8*3600`）与「先 GET xueqiu.com 拿 cookie」两步；`ensureDefaults` 里对 `cat==='境外'` 的过滤（删掉境外就会混进组合池）。

## v1094 · 回撤档位做成真·全指数（2026-11-24，index 5,237,061 B / index-dd 2,862,729 B）

- **改了什么**：`edit_work/gen_index_dd.py`（IDX 13→45 只 + `cat` 字段 + 新浪优先/中证→腾讯→carry 兜底）→ `edit_work/data/index-dd.json` 2,862,729 B；`edit_work/index.html`（徽标 v1094 + 注释块 `fw2_v1094_dd_allidx`）：标题回「全指数回撤监测」、类别/分档两组可点筛选、跨档卡默认紧凑（跨档 + ≤2pp）可展开 45、估值卡只列 13 只并注明 32 只无源、组合默认勾 18 宽基 + pick 迁移、「代码·市场」→「代码·类别」。
- **未验证的假设**：①45 只的「宽基/行业/主题」分类是我按名称人工归类，未逐只对照中证官方分类（中证 A 股行业指数有自己的 11 个一级行业口径，这里把「中证能源/金融/信息技术」等归为行业、把「白酒/新能源/传媒」等归为主题，属约定俗成）；②`stale` 判定沿用「末点距 updatedAt > 7 天」，未核对每只的官方交易日历（如北证50 与小盘指数偶有停牌日）；③2.86 MB 的 JSON 在移动端首次加载耗时未实测（只在本地桌面与 CDP 538 视口量过）。
- **下一步 + 别碰**：要加标的就改 `gen_index_dd.py` 的 IDX（`sina_symbol` 必填、`csi_code` 可空）后重跑；**别把新浪断尾序列（末点停在 2016/2019 的代码）放进池子**——前端会把 2016 年的回撤当「当前回撤」；中证官网现在整段 403、腾讯 fqkline 501，别把它们当主源。

## v1093 · 监测卡更名 + 档位列补全（2026-11-24，5,232,020 B）

- **改了什么**：`edit_work/index.html`（徽标 v1093 + 注释块 `fw2_v1093_dd_scope`）——「全指数回撤监测」→「跟踪指数回撤监测」，副题写明 13 只＝5 宽基 + 8 行业/主题、非全市场；档位 / 下一档改为对所有行计算（原先 <70% 显示「—」「未进区」），未进区灰色、已进区粗体；卡下注明口径。
- **未验证的假设**：①「不完全是全指数」我按「覆盖范围名不副实」理解并改名，若你本意是「要扩成全市场指数池」，需另做取数扩池；②13 只的 5+8 分类是按名称人工归类（沪深300/中证500/中证1000/创业板指/科创50 为宽基），未按中证官方分类逐只核。
- **下一步 + 别碰**：扩池需改 `edit_work/gen_index_dd.py` 的 IDX 表并重跑 `data/index-dd.json`（`gen_index_val.py` 依赖它）；**别把监测表的「全行档位」当成已进买入区**——方案卡的买入区只数仍只认 `ddAbs >= 起始回撤`；分档 chips 加指数后要核对合计＝行数。

## v1092 · 回撤档位表格全部左对齐（2026-11-24，5,231,271 B）

- **改了什么**：`edit_work/index.html`（徽标 v1092 + 注释块 `fw2_v1092_dd_leftalign`）——`#stp-dd .dd-tbl--tg th.r`、`td.r`、`.dd-tbl .num` 三处 `text-align` 由 right 改 left（数字保留等宽字体）；列宽/列数/取数/回测逻辑未动。
- **未验证的假设**：参数输入框（`#stp-dd .dd-dd`、`.dd-ti`）仍按原右对齐——我判断「表格的字段和内容」不含表单控件，用户若指全部则需再改。
- **下一步 + 别碰**：核对可用 `getComputedStyle(td.r).textAlign` 应等于 `left`；**别动** `table-layout:fixed` 与 `<col>` 宽度（左对齐不需要改列宽）；`min-width` 仍须≥列宽之和。

## v1091 · 回撤档位去掉宽度上限、加列铺满全屏（2026-11-24，5,230,958 B）

- **改了什么**：`edit_work/index.html`（徽标 v1091 + 注释块 `fw2_v1091_dd_full`）——`ddTbl()` 删 `max-width:1180px`（旧 `.dd-tbl` 同删），表随卡片铺满；五张表加列：策略口径 3→4（+在哪里改）、买入区 7→10（+距下档／历史最高收盘+日期／数据日）、回撤监测 7→10、跨档提醒 5→10（+现价／今日档位／昨日档位／距下档／对比日）、估值参考 5→8（PE/PB 现值、分位拆四列 + 口径·数据日）；新增 `hiOf(ix)`。
- **未验证的假设**：①宽屏只做 CDP emulation 量测（1770 下 6 表宽＝容器 1458、`uniq=1`、0 表头裁切），**没有真实宽屏截图**；②「列宽按比例拉伸」在超宽屏（>2000）时会让短文本列变松，未实测；③窄屏 10 列靠横滑，人眼可读性只看了 538 的截图。
- **下一步 + 别碰**：`min-width` 必须≥列宽之和（否则 fixed 布局压列、右对齐数字贴边）；`body.scrollWidth` 不许超过 `innerWidth`（横滑只能发生在 `.dd-tblwrap`）；加列要同步改 `ddTbl` 的 cols 与每行 `td`（手工拼串，漏格整表错位）；`runBT/runPoolBT` 共用买卖判定，改规则两边都要改并重跑「传媒三笔一致性」。

## v1090 · 回撤档位四块卡改「投资总纲」表格形态（2026-11-24，5,228,361 B）

- **改了什么**：`edit_work/index.html`（徽标 v1090 + 注释块 `fw2_v1090_dd_tbl`）——新增公共骨架 `ddTbl(cols,minW,rows,cls)`，把 `#stp-dd` 的方案卡（策略口径 5 行 3 列 / 买入区 7 列）、今日跨档提醒（5 列）、全指数回撤监测（7 列）、估值参考（5 列）四块改成总纲表形态（`table-layout:fixed` + `colgroup` 像素列宽 + 表头 `#F4F4F2` + 行线 `#F1EFE9` + `max-width:1180px`）；结果区旧 `.dd-tbl` 同步统一表头与内距。
- **未验证的假设**：①1770/1280 宽屏只做了 CDP emulation 量测（6 表宽 1180、13 行 `uniq=1`、0 裁切），**没有真实宽屏截图**（无头 Edge 158 的 `--headless=new` 立即退出且不产文件；`Page.captureScreenshot` 无视 emulation 恒回 538×643）——视觉上「宽屏留白多少」未经人眼确认；②`max-width:1180px` 是本轮自定（照总纲阈值表 1010 的量级放大），不是你给的数值。
- **下一步 + 别碰**：宽屏若要改宽度就改 `ddTbl` 里那一处 `max-width`（6 张表同源，改完要四块一起核列位置）；**别删 `max-width`**（删了跨档表又会被 `width:100%` 拉满整页，就是你截图看到的样子）；**别把 `<col>` 去掉**（`table-layout:fixed` 下无列宽会均分，看着像错位）；`runBT/runPoolBT` 买卖判定共用，改规则两边都要改并重跑「传媒三笔一致性」。

## v1089 · 估值双分位 + 今日跨档提醒（2026-11-24，index 5,226,029 B）

- **改了什么**：`edit_work/index.html`（tag `fw2_v1087_dd` 段内新增 `crossCardHtml()` + `#ddXHost`；估值卡改 5 列 PE/PB 双分位；CSS 加 `.dd-tbl--fit` 等）；`edit_work/gen_index_val.py` v2（蛋卷优先 + 中证兜底）→ `edit_work/data/index-val.json`（3,720 B）。
- **未验证的假设**：蛋卷 `pe_percentile` 的历史窗口口径（疑 10 年，与乐咕 10 年月频对拍差 <2pp 支持此判断，但**未取到蛋卷自身窗口声明**）；5 只缺源指数暂无可替代长序列（只验证了蛋咕/乐咕/中证三处）。
- **下一步 + 别碰**：重跑 `python gen_index_val.py` 后要连带确认 13 只代码与 `index-dd.json` 一致；`runBT`/`runPoolBT` 共用买卖判定，改规则两边都要改并重跑「传媒三笔一致性」；`#ddChart` 仍自绘 SVG。
- **旁注**：erify_sync.py GitHub 端全 PASS（iles 41 matched 41）；资料库端仍 FAIL（E_NOT_WORKBUDDY 未连接到 WorkBuddy 客户端宿主通道）——首次出现于 v1088，属宿主通道未连，**与本次改动无关**，别去改页面或 token 追这条。

## v1088 · 回撤档位新增「估值参考」卡（2026-11-24，5,221,282 B）

- **改了什么**：`edit_work/index.html` 徽标 v1088（tag `fw2_v1088_val`）——`#stp-dd` 在「全指数监测」与「档位回测」之间插入「估值参考」卡（`valCardHtml/valHostHtml/loadVal`，13 行 × 6 列：指数／当前 PE／近 20 日区间／股息率／价格 10 年分位／PE 10 年分位（月频）），懒加载 `data/index-val.json`。新建 `edit_work/gen_index_val.py` → `data/index-val.json`（3,387 B）；台账第 40 条 `index_val`、`DATA_LEDGER.md` 手工轨小节、`push_gh_v39.py` FILES 各补一条；`_globals_baseline.json` 277 键。
- **未验证的假设**：①中证官网估值 xls 是不是「每天滚动 20 行」而非固定 20 行——本次只看到 20 行、日期到 2026-11-23，未连续两天观察增量行为；②`pe2_lo/pe2_hi` 是这 20 个交易日内的极值（不是自然月/季度区间），页面按「近 20 日区间」表述，若日后再拉更长快照需要换文案；③`pricePct` 用「近 10 年窗口内 ≤ 当前收盘的比例」，与截图第三方的「时间/数值分位」定义未逐位对齐（本页已明标「不是 PE 分位」）；④乐咕月频 3 只的 `pePct` 与官网「当前 PE」口径不同源（月频 PE-TTM vs 官网市盈率2），两列并列时会有数值落差，未做统一。
- **下一步 + 别碰**：复跑 `python edit_work\gen_index_val.py`（依赖 `data/index-dd.json`、`data/pe-hist.json` 已生成；399006 必 404 属正常），再 `python edit_work\verify_manifest.py`（应 40 数据集 / 39 发布 JSON）；**别用官网 20 日快照去算 PE 分位**（样本不足，会得到假分位）；**别把 `pricePct` 与 `pePct` 混成同一列**（前者是价格分位）；**别删 `data/index-val.json` 的发布清单行**（否则线上 404、卡片永远空）。另：`verify_sync.py` 的 GitHub 端 41 文件字节全一致（PASS），但「资料库」回拉仍返回空（`.lib_tok_tmp` 存在、`download_page_artifacts.py` rc=0 却未落地任何 html）——与本次改动无关，属资料库节点/token 侧既有问题，需单独查。

## v1087 · 回撤档位新增「多指数组合（共享资金池）」回测（2026-11-24，5,217,654 B）

- **改了什么**：`edit_work/index.html` 徽标 v1087（tag `fw2_v1087_dd`）——`#stp-dd` 参数区加「回测方式」下拉（单指数/多指数组合），新增 `runPoolBT`（并集交易日轴、共享现金、逐笔独立卖出）、`pickHtml/togglePick`（13 只 chip 点选）、`resultHtml` 组合分支（参与/触发 KPI + 分指数表 + 逐笔「指数」列）；同轮修 `ymd()` 数字日期与 scope 切换不重画两处 bug。无新 tab、无新数据文件（复用 `data/index-dd.json`）。
- **未验证的假设**：①组合回测的「历史最高收盘」取各指数全序列（含回测起点之前的高点），所以 2016 年时可能一进场就已深于 70%——这是有意的（回撤是相对历史高点的事实），但没验证是否与你心里的「从区间起算」一致；②组合资金分配是「先触档先买」（时序优先），不是等权预算预留，小资金在早期被单一指数吃掉后会跳过后续档位（本次跳过 0 档，资金放大后行为会变）；③两只 93xxxx 已纳入可选 chips，但其数据止于 2025-12-31，参与组合只贡献到该日为止的行情。
- **下一步 + 别碰**：复跑 `python edit_work\check_js.py`（应 ALL OK 22 块）；本地 `http://127.0.0.1:8765/index.html` 进「策略执行 → 回撤档位」切组合应出 8 KPI；**别把 `runPoolBT` 的买卖判定改成与 `runBT` 不同**（两者必须同一套规则，交叉校验看「传媒三笔」是否仍为 −20.37/+68.28/+212.86）。

## v1086 · 策略执行新增「回撤档位」子页签（2026-11-24，已发布 master `061944270a1c`，5,205,810 B）

- **改了什么**：`edit_work/index.html` 徽标 v1086（tag `fw2_v1086_dd`）——策略执行第 5 个子页签「回撤档位」（`data-st=dd` / `#stp-dd`）：13 只指数高点回撤监测（分档 chips + 行点选）+ 单指数档位回测（8 KPI + 自绘 SVG 曲线 + 逐笔明细）；默认按用户口径「开始回撤 70%、间距 5pp、每档 ¥500、总资金 ¥10,000、反弹 2 档观察 / 回落 1 档卖出」。新建 `edit_work/gen_index_dd.py` → `data/index-dd.json`（926,441 B）；台账第 39 条 `index_dd`；`push_gh_v39.py` FILES 加该 JSON；`_globals_baseline.json` 276 键；`_audit_plan_merge_v895.py` A01 改 6 tab + 新增 A01d。
- **未验证的假设**：①「回撤 70% 起买」是照你一句话定的默认值，截图原页是 60%——没验证 60% 是否才是你更想要的长期口径（页面可改，改一次即生效）；②两只 93xxxx 的 2025-12-31 数据在页面上标了 stale，但没验证它们真实的 2026 年回撤（可能已不在 70% 区间）；③本模块 ECharts init 出空 canvas 的原因没查明（换 SVG 绕过），若后续有人把图表改回 ECharts 需先复现该问题；④窄屏断点 560px 是按 538 宽实测调的，420 宽时页面本身有横向滚动（非本模块引入）。
- **下一步 + 别碰**：数据重生成 `python gen_index_dd.py`（中证需 Referer、腾讯/新浪限流会空响应，重跑即可）；**别把 `#ddChart` 改回 `echarts.init`**（本模块 init 出空 canvas，v1086 已改自绘 SVG）；**别在 HTML 注释里写 `<script>` 字样**（`check_js.py` 会分块切错，块 12 报 `Invalid or unexpected token`）；回撤值只由 `gen_index_dd.py` 产，前端只做展示与回测。

## v1085 · 宏观环境新增「缠论结构 · 沪深300」（2026-11-24，已发布 master `e83b4a93f5b2` → `c2423cd4af60`，5,174,321 B）

- **改了什么**：`edit_work/index.html` 徽标 v1085（tag `fw2_v1085_chan`）——宏观环境第 5 个 tab「缠论结构 · 沪深300」；`renderMacro` 加 v-chan 分支；独立 IIFE 渲染头部（PE/PB 分位 + 估值窗口）/ 周期日周月 / 五类勾选 / 区间 / ECharts 蜡烛+笔+线段+中枢框+买卖点。新增 `edit_work/gen_chan_hs300.py` 与 `edit_work/data/chan-hs300.json`（416,688 B）；`push_gh_v39.py` 加发布行；台账 38 条；`_globals_baseline.json` 266 键。
- **未验证的假设**：①算法是「简化复刻」，笔/线段/中枢/买卖点数量与截图那套第三方实现不逐点一致（页面已声明，未与对方数对比）；②PE/PB 分位用本项目乐咕月频（12.64 / 61.2% / 1.32 / 20.7%），与截图 13.48 / 53.9% / 1.33 / 11.9% 不同源，非 bug；③周/月线与日线用同一套算法重算，未单独调参；④线上只核到「切走再切回图表重建」，未在线上改勾选写 localStorage（该模块不落盘，纯视图态）。
- **下一步 + 别碰**：重生成数据跑 `python gen_chan_hs300.py`（东财限流会空响应，重跑即可）；**别给模块卡片加 `mc-mod`**（`__mcApply` 会按 region 隐藏第 1/4 张，头部与图表一起消失——v1085 踩过）；**别把 `markArea` 标签打开**（窄中枢框里文字必被截断）；`dataZoom` 默认 `zoom:2` 是刻意选的观感值，别改回 3；分钟线没有数据源，别凭空造。

## v1084 · ⑧-A 子页签改名「⑧-A 回测参数」（2026-11-24，已发布 master `8900ae106cb4`，5,155,368 B）

- **改了什么**：`edit_work/index.html` 徽标 v1084（tag `fw2_v1084_bt_a_label`）——⑧-A 子页签去掉「（全量底稿）」，四处同名文案同步：`mk('plan', …)`、卡头 `sc === 'plan' ? …`、保存提示 `__btCfgScope === 'plan' ? …`、v1083 重置按钮 tooltip 里的母版名。纯可见文案，零逻辑。
- **未验证的假设**：无（改动为字符串替换，已在本地 :8765 与线上 Pages 双端读到三档文案与「全量底稿 0 次」；未逐字校验 `btParamSaveMsg` 的运行时输出，只静态确认了字符串已换）。
- **下一步 + 别碰**：改命名只动这四处可见字符串；**别顺手替换代码/HTML 注释里的旧名**（v1041/v1081 历史注释是留档，改了会让 PITFALLS 与版本史对不上）；回测引擎、`btSave`、`btApplyStd` 分支别动。重发 `python _push_rest_v1077.py`。

## v1083 · ⑧-B／⑧-C「重置」改「清空覆盖 · 继承母版」（2026-11-24，已发布 master `d7330b6756f6`，5,155,115 B）

- **改了什么**：`edit_work/index.html` 徽标 v1083——①`btParamsHtml` 新增 `var _bsc = window.__btCfgScope || 'plan';`，`btResetStd` 按钮文案/tooltip 按 scope 现算（`plan` 仍「重置为标准口径」，`hold`/`custom` 改「清空覆盖 · 继承母版」）；②`btApplyStd` 开头加非 `plan` 分支：读旧 diff 条数 → 写 `{}`（带 `win` 时只写 `{start,end}`）→ `renderBtCfgHost()` → `btToast` 报「清掉 N 条 + 母版现值」→ `renderBacktest()` + `setTimeout(__btGo,80)` → `renderLogicView()`；母版档原逻辑未动。
- **未验证的假设**：①线上只核到「清掉 0 条」（你线上 `fw2_bt_custom` 本就是 `{}`），非空覆盖的线上清空行为是靠本地造 `{budget:11111}` 验证的（本地与线上同一份代码，风险低但仍属推断）；②⑧-B（`fw2_bt_hold`）线上现值未查，只核了按钮文案；③清空后面板显示的是**母版现值**——若母版本身不是标准口径，清完看到的就是母版那一套（这是本次的语义选择，不是 bug）。
- **下一步 + 别碰**：改这颗按钮只动 `btParamsHtml` 里那段按钮拼接 + `btApplyStd` 的非 `plan` 分支；**别把 `if (_sc0 !== 'plan')` 的 `return` 删掉**（删了会继续往下跑「写标准值」那套，覆盖又被写回五条）；**别去掉 `win` 分支**（去掉则 3/5/10 年预设失效）；`btSave(c, scope)` 的显式 scope（v1082 修跨档）别回退；回测引擎、`BT_DEFAULTS`、`fw2_bt_plan` 结构别动。重发 `python _push_rest_v1077.py`。

## v1082 · 「重置为标准口径」修好（2026-11-24，已发布 blob `1466b9c71ac88fbbf1e129a382c1180ee602199f` / master `cc14fb077021`，5,152,820 B）

- **改了什么**：`edit_work/index.html` 徽标 v1082——①`btSave(c, scope)` 增显式 scope，`go()` 改 `btSave(c, window.__btScopeName || 'hold')`（原来是「按回测页 tab 取参数、按参数页 scope 落盘」，跨档会互相覆盖）；②`btApplyStd` 写盘后 `renderBtCfgHost()` 重画参数区；③新增 `btToast()` 页顶浮条（5 秒自隐）给出重置回执。`_globals_baseline.json` → 257 键。
- **未验证的假设**：①线上只读验过「现值已是标准口径、覆盖 `{}`」（所以此前点击确实无可改），未在线上点按（避免写你的存档）；行为验证全在本地 :8765 三档跑（⑧-A/B/C）。②浮条文案里「一次性（建仓底仓 30%）」等口径与 `BT_DEFAULTS` 一致是按代码读的，未逐键与出厂 diff 对拍。③本地测试把 :8765 的 `fw2_bt_plan` 与 `fw2_bt_hold/custom` 写成了标准口径（线上 origin 未动）。
- **下一步 + 别碰**：改重置只动 `btApplyStd` + `btToast`；**别把 `btSave(c)` 的显式 scope 去掉**（去掉就回到跨档覆盖的老 bug）；**别按 `__btCfgScope` 决定 go() 的落盘档**；回测引擎与 `BT_DEFAULTS` 别动。重发 `python _push_rest_v1077.py`。

## v1081 · 回测参数入口改名（2026-11-24，已发布 blob `6dee4cc060c79802d581b6790decd9842a7828c0` / master `47067636fc0a`，5,150,022 B）

- **改了什么**：`edit_work/index.html` 徽标 v1081 + 注释块 `fw2_v1081_bt_param_labels`——①「策略执行」页签 `data-st="param"` 文案「回测参数（全量底稿）」→「回测参数」；②`btSumHtml(cfg)` 新增 `_pname`/`_psub`，按 `sc`（hold/custom）现算按钮「修改参数 → 配置回测参数 / 自选回测参数」与副文案「参数在『策略执行 → 回测参数 → ⑧-B/⑧-C …』」；③其余 11 处「策略执行 → 回测参数（全量底稿）」指路文案统一成「策略执行 → 回测参数」；④⑧-A 子页签名保留「⑧-A 回测参数（全量底稿）」。
- **未验证的假设**：①⑧-A 是否也该去掉「（全量底稿）」（用户只圈了 nav 页签与两页按钮，⑧-A 保留母版底稿名，已在 README「下一步」里挂着待确认）；②副文案里补了「→ ⑧-B/⑧-C 子页签名」，比原来多一层信息，用户未明确要求，若嫌啰嗦可回退成只写「策略执行 → 回测参数」。
- **下一步 + 别碰**：改这两处只动 `btSumHtml` 的 `_pname`/`_psub` 与 nav 页签文案；**别碰** `btCfgGo`/`btCfg` 存取链（改文案不改跳转）、**别碰** ⑧-A/⑧-B/⑧-C 的 scope key（`plan`/`hold`/`custom` 是存储键，改了会丢覆盖项）。重发用 `python _push_rest_v1077.py`。

## v1080 · 资产配置「定投金额（月）／累计应投」改计划口径（2026-11-24，已发布 blob `395407182913e1c8d9881c9797d7275f46b103c4` / master `3a4215d44770`，5,149,001 B）

- **改了什么**：`edit_work/index.html` 徽标 v1080 + 注释块 `fw2_v1080_dca_plan_basis`——`_planCfg()` 新增 `d.plan = d.mode;`（记录 R2 折叠前的计划投入方式）、新增 `_planCfgPlan()`；`_rowMonthlyT(tgtS)` / `_rowProgT(tgtS)` 去掉市值参数、只按目标金额算（月投＝目标×(1−底仓%)÷12 / 目标÷12 / 0；累计＝首笔(目标×底仓%)＋月投×已过期数）；`_mColTxt(v,tgtS)` 有目标照实出数、无目标「—」；表尾改 `c.plan || c.mode` 并追加「R2 定投＝关，实盘暂不按月投（计划口径不受影响）」；口径说明折叠区两段重写。`_audit_alloc_cols.py` 扩到 60 条（D08–D17）。
- **未验证的假设**：①「累计应投」按纲领「底仓+定投 30%」含首笔，故单行 5,000 目标＝2,376（＝预算 47.5%），若你的口径是「纯按月投不含底仓」（417 / 1,250、合计 12,500），需把纲领投入方式切「每月定投」——本版未擅自改纲领；②合计「累计应投」23,760 与「调仓金额」31,932 不相等属计划 vs 净额的口径差，未与你确认是否要合计也按净额；③日限额 020712 仍不扣限额；④R2 仍「关」（`fw2_logic_v1` 覆盖 `R2='off'`），实盘暂不按月投。
- **下一步 + 别碰**：改这两列只动 `_rowMonthlyT / _rowProgT / _planCfgPlan`（`_audit_alloc_cols` D10–D17 会锁住「单一实现」与「计划口径」）；**别把两列再绑回持仓缺口**（v1079 被用户否掉的原因）、**别在 `_planCfg` 里删 `d.plan`**（删了 R2＝关时月投立刻归零）、**别碰** `mvMap` 取数（喂「实际市值」与「标的占比」）、`_dcaProg/_dcaFirst/liveMonthly` 本体（其它页面在用）。重发用 `python _push_rest_v1077.py`。

## v1079 · 资产配置表「累计应投 / 定投金额（月）」按行口径重算（2026-11-24，已发布 blob `8faf9b0b3774` / master `0efa8feb167f`，5,147,568 B）

- **改了什么**：`edit_work/index.html` 徽标 v1079 + 注释块 `fw2_v1079_dca_row_unify`——新增 `_rowMonthlyT(tgtS, mv)` / `_rowProgT(tgtS, mv)` / `_mColTxt(v, tgtS)` 三个块内助手，资产配置表「定投金额（月）」「累计应投」改为按「本行目标金额 + 本行实际市值（`mvMap` 份额×净值）」现算：家族行用整族 `tt`/`tm`，单只行用 `ft`/`fm`；lump＝max(0, 缺口)、base＝首笔(目标×底仓%，≤缺口)＋月投×已过期数、drip＝月投×已过期数；家族行不再 `Σ _dcaProg(成员)`。一次性口径下月投列显示灰「0」（不是缺数据）；口径说明整段重写。`_audit_alloc_cols.py` 新增 D08–D12 五条硬卡、D05 改判 `_mColTxt`（55:0）；`_audit_screen_consistency.py` 徽标断言由写死正则改「按 verBadge 现算数值 ≥1078」（原正则漏 1079）。
- **未验证的假设**：①「累计应投」合计按行 clamp 到 ≥0（只算欠配），所以与「调仓金额」净额不相等（本地差 5,410＝易方达 −5,198＋招商 −193＋标普 −19）——这是本轮保留的口径，未与你确认是否要改成净额；②日限额标的 020712（日经 225，10 元/日）本表按缺口出 4,826、不扣限额，与执行卡限速并存，未定谁优先；③线上你当前预算存的是 ¥62,000（本地 ¥50,000），故线上首笔合计 48,142 / 合计调仓 43,932，与 README 记录的 50,000 口径数字不同——两边都对，别当成 bug。
- **下一步 + 别碰**：改这两列只动 `_rowMonthlyT/_rowProgT/_mColTxt` 三个实现（`_audit_alloc_cols` D08–D12 会锁住「单一实现」）；**别碰** `mvMap` 取数（它同时喂「实际市值」与「标的占比」）、**别把家族行改回逐只累加**（漏同族持仓的根因）、**别用 `_dcaFirst` 的 `gapOf` 昨收价**（价源不同源）、`_dcaProg/_dcaFirst` 本体仍在别的页面用，不要删。重发 `python _push_rest_v1077.py`。

## v1078 · ① 选品层 × 筛选规则口径统一（B 方案，2026-11-24，已发布 blob `aba25a1349d2` / master `7a5d7e9918d8`，5,143,575 B）

- **改了什么**：`edit_work/index.html` 徽标 v1078 + 注释块 `fw2_v1078_sel_params`——①（① 层）S1/S5/S7 三行「信号含义」末尾挂 `selParamNote()`：琥珀「参数出处：…」**现算自 `screen-rules.json`**（2 亿 / 3 年 / 2 只）+ 蓝字「打开筛选规则 →」；筛选规则页（`poolRulesDocHtml`）头部加琥珀横幅「本页参数同时约束 ① 选品层 …」+「去投资总纲 ①」；`LOGIC_MEAN.S1/S5` 改写（S1 不再自称估值门槛、S5 不再自称用 5000 万淘汰）。新增门禁 `_audit_screen_consistency.py`（23 条），已登记 `refresh_all.py` `SERIAL_AFTER` 末位（组 `sel-scope-audit`）；`_globals_baseline.json` → 255 键（`selParamGo` / `selParamGoTotal`）。
- **未验证的假设**：①`screen-rules.json` 里 `hardGates.estabMinYears=3`、`batch.tribeMax=2` 是否为你想对 ① 层公示的口径（我按「文件里写的即真源」取，未改规则文件本身）；②线上筛选规则页首屏会出现「加载筛选规则…」再渲染（异步 fetch），首屏到内容有约 1–2 秒空窗，未做骨架屏；③窄窗（538×643）下 ① 层 10 列表仍靠横滑，参数出处小字在 146px 行高内不溢出，但更窄（<420px）未测；④`market_screen.py` 的估值只加分不淘汰是读代码得出（`bonus.valuation`），未跑一次真实筛选验证分数构成。
- **下一步 + 别碰**：改门槛只改 `edit_work/screen-rules.json`（数值唯一真源），改完跑 `python _audit_screen_consistency.py` + `python market_screen.py`（若重算池）；**别碰** ① 层的 `SEL_PARAM_SRC` 映射去写死数字（审计会 FAIL）、别把 S1 写回「估值门槛」、别在 S5 文案里写「≥2 亿淘汰」（淘汰属于硬门槛，不属于 S5）。重发仍用 `python _push_rest_v1077.py`（changed-only，安全）。

## v1077 · 全量数据刷新 + 三处对比度 FAIL（2026-11-23）

- **改了什么（前半轮：数据链 + 对比度）**：`refresh_all.py` 改用 `Python312\python.exe` 跑全链（裸 `python`＝沙箱 runtime 缺 pandas/akshare），主链全部刷到 2026-11-23；三处对比度 `fw2_v1077_a11y`——「观察」`#A9630B→#96560A`（4.37→5.39，分段控件选中态同步）、「关」`#71717A→#6B6B74`（4.47→4.88）、T9 CAP 禁用输入框 `#9A968C→#6B675E`（2.59→4.94），`_audit_contrast_css_v852` 由 3 FAIL → PASS 21/0；`_audit_pe_chain_v846` 的 peDate 断言改「跨市场只允许周末差」；发布走 `_push_rest_v1077.py` 续推（`push_gh_v39.py` 在 macro-data.json 上被 `IncompleteRead` 打断）。
- **改了什么（收官第二轮，已发布 blob `d902375c` / master `793280dfc474`，5,140,103 B）**：①`gen_sec_daily.py` 成功，`window.SEC_DAILY` 1,148 点至 2026-11-23 / 66.27%，`data/sec-daily.json` 同源，线上证券化率卡实测「自算·日频 66.27% · 日频段 2026-11-23 · 10年分位 P51」；②`index.html` 里 `window.MACRO_SNAP = ` 的重复链由 133 层折成 1 层（等价表达式，MACRO_SNAP 逐键比对一致，省 2,640 B），并把 `_merge_macro_v301.py` / `gen_industry.py` 的写入改为「注入前先折叠左侧连续前缀」，**否则每跑一次刷新就再多叠一层**；③`_push_rest_v1077.py` 续推 2 个文件（index.html + sec-daily.json）、0 失败，本地 blob sha vs 线上树全量比对 38/38 一致。
- **未验证的假设**：①`gen_index_long.py` 全 9 只 JSON 解析失败（东财 push2his / 同源限流），脚本「失败则其余仍写盘」路径下 `index-long.json` 未被覆盖、9 序列完好（逐只点数：000510/000300/000015 各 5309、000922 4440、399673 3017、NDX 5499、N225 5352、000985 3711、SPX 5507），但仍停 2026-11-13；②`_audit_sec_daily_v877.py` 首跑 OK 17 / FAIL 4，判定为「断言写死旧值」（`brokenPct=9.13`、`504/5521`、磁贴≈曲线末值、`verBadge` 停在 v879），只记录未改该审计；③`gen_fund_jjcc.py` 仍 42% 成功率（东财 `514 Frequency Capped`，IP 级限流），保留上季快照（Q3 2026-09-30，属最近可得季报），未换源；④`gen_index_bench.py` 重跑时东财 push2his 全部 8 只返回空（同日早前一次已成功、`index-daily.json` 8 序列末值均为 2026-11-23），本次未再双源对拍；⑤macOS / 手机端未测（本轮只核 538×643 窄窗）。
- **下一步 + 别碰**：要重发只跑 `python _push_rest_v1077.py`（`git/trees` 取 sha + contents PUT，避免 `push_gh_v39.py` 大响应 `IncompleteRead`）；别在 index.html 里手工拼 `window.MACRO_SNAP = ` 前缀（现在已是单层，脚本会自动折叠，手工拼会被下一次注入清掉但顺序可能错）。 另外：`index-daily.json` 若某天某只停在旧日期，先单跑 `gen_index_bench.py`（东财限流时等 10 分钟再试），**不要**为了让脚本 rc=0 关掉双源对拍；`peDate` 断言的周末规则写在 `_audit_pe_chain_v846.py`（工作日缺席仍判 FAIL，别改成「相差 ≤3 天」的宽判）。
- **发布路径变更（必看）**：`push_gh_v39.py` 会为每个文件先 `GET /contents/<path>` 取 sha，本机直连下 `caifu/macro-data.json`（451 KB）的大响应会被 `IncompleteRead` 截断，三次重试都落在同一个文件上 → 整包发布必崩（本轮崩两次，gate 本身仍 PASS）；改用 `edit_work/_push_rest_v1077.py`（`git/trees?recursive=1` 一次取 path→blob sha，再走 contents PUT，changed-only 语义不变，4 次退避重试）→ 首轮 13 文件、收官 2 文件，均 0 失败；核对时不要读大响应，改比「本地 blob sha vs 线上树 sha」全量对拍（本轮 38/38 一致）。

## v1076 · 总纲五项冲突修复（2026-11-23）

- **改了什么**：`edit_work/index.html` 徽标 v1076 + `fw2_v1076_conflicts`；R7 带宽与 T10 四档带拆开（band 25 / slotBand 5，老 5/5 存档一次性迁移回写）、R2 三态接 `_planCfg`（关→月投 0）、T4 与 R6 合并为同一 `slHard` 一条执行、CAP 输入框禁用并标「已下线」、T5 6→12 个月。已发布 blob `724044dab0b7`（5,140,641 B）。
- **未验证的假设**：①R2「观察」按 investMode 处理（与回测 `logicCfgOverlay` 的 obs=不下发口径对齐），未在真实「观察」态下实测金额；②`fw2_band_split_mig` 只在 `band=5 & slotBand=5` 时触发，若你此前手动把两值都设成别的同值（如 10/10）不会被迁移。
- **下一步 + 别碰**：接手者改阈值/回测先跑 `edit_work/handoff_check.py`；`cap` 键仍保留在 `SIG_THR_DEF/LIM/NAME`（T9 已下线，删键会影响 26 项计数与旧档升级，**暂不删**）；回测引擎与 `fw2_bt_*` 本版未动。

## v1074 · 2026-11-23 · 三态开关重绘（根因：根本没样式）

- **改了什么**：`edit_work/index.html`（tag `fw2_v1074_lgseg`，徽标 v1074）——新增 `#view-tg .lg-seg` 全套样式（轨道 + 白滑块 + 状态点 + hover/focus），删掉 `logicRowHtml` 里选中段的行内 `background/color`；三态列 136→148px（备注列 240→228）；八层表三态列改 `lg-cnt` 胶囊。`logicSet`、三态语义、`fw2_logic_v1` 存档格式一字未动。
- **未验证的假设**：①手机/窄屏未实测（表格本来就 `min-width:1890px` 横滑，控件宽度不受影响）；②`input[value="frozen"]` 这类未来新增的第四态没有配色，需另补规则；③旧浏览器（不支持相邻兄弟选择器的极端环境）会退化成无样式，未测。
- **下一步 + 别碰**：改三态观感只动 `#view-tg .lg-seg` / `#view-tg .lg-cnt` 两段 CSS，**不要**把颜色写回 `logicRowHtml` 的行内 style（那会盖掉 hover 与 focus 环）；三态列宽改动必须同步一条 `col`，否则会压到「生效作用」列。

## v1073 · 2026-11-23 · 目标 4 行列序修正（输入框回「当前值」列）

- **改了什么**：`edit_work/index.html`（tag `fw2_v1073_tgt_col_fix`，徽标 v1073）——`_tgtTd` 参数与 td 顺序改为 范围 → 出厂值 → 当前值，3 个目标行 + 1 个 Calmar 派生行调用同步；`fw2_tg_thesis` 写入链、23 行阈值、表头列宽、八层表零改动。
- **未验证的假设**：无（本地与线上均逐列打印第 1 组 4 行与 T1 对照，改 ddBudget 20→25→20 闭环已跑，`fw2_tg_thesis` 已复原 20）。
- **下一步 + 别碰**：跑 `cd edit_work; python verify_manifest.py` / `_audit_plan_merge_v895.py` / `_audit_alloc_cols.py` 应全 PASS；**别碰** `_tgtTd` 的 td 顺序与 `tgPlanEdit`（本版未动写入链），别给 TGT 组另设列宽（列宽随表头走）。

## v1072 · 2026-11-23 · 纲领三键搬进信号阈值表（第 1 组「纲领目标」）

- **改了什么**：`edit_work/index.html`（徽标 v1072，注释块 `fw2_v1072_tgt_in_table`）——`_grp` 加 `TGT{n:4}`；新增 `_tgv/_tgtRows/_tgtTd/_tgtInput/_tgtDef` 并把 4 行渲染在 23 项之前；总纲卡头部三个输入框撤掉、换只读 chip + 指路按钮；`sigThrReset` 提示改口径（只重置 23 项）。存储键未动：目标仍 `fw2_tg_thesis`、阈值仍 `fw2_sig_thr`。
- **未验证的假设**：①`tgPlanEdit` 只更新 `#tgIn_*`、`#tgGoalTxt`、`#tgCalmar`，其他地方（BT3 结论条、规则卡）靠下次渲染读取，页面若在 信号页/回测页 停留不会即时刷新（编辑入口只在总纲独立视图，暂无实际影响）；②`logicGo('sigthr')` 作为 onchange 二次调用会把焦点丢回页面顶部之外的视图，键盘连续输入体验未测；③派生 Calmar 只保留 2 位小数（与头部 chip 同口径）。
- **下一步 + 别碰**：目标三行 `id` 必须是 `tgIn_<键>`（`tgPlanEdit` 按 id 拆键）；不要在总纲卡再放同名输入框（会与表内重复、`getElementById` 只认第一个）；加/减目标项要同步 `_grp.TGT.n`、`_tgtRows`、`TG_THESIS_DEF` 与「26 项」类文案。

## v1071 · 2026-11-23 · 八层导航表格化（一行一层 · 7 列）

- **改了什么**：`edit_work/index.html`（徽标 v1071，注释块 `fw2_v1071_layer_table`）——`logicLayerHtml` 的 B 段由卡片网格（`repeat(auto-fill,minmax(104px,1fr))`）换成 7 列表格 9 行，`<tr onclick>` 跳层；`act` 加 `!_sigMode` 修「独立视图下 ① 与第 9 行同时高亮」。计数仍走 `logicLayerStat`。
- **未验证的假设**：①`<tr>` 上挂 onclick 在键盘导航/读屏下不可达（无 tabindex 与 role），只为点击服务；②第 9 行「23 项」写在文案里、未从 `fw2_sig_thr` 现算（阈值项数若变化要手改）；③窄屏（507px）需横滑 553px，未在手机真机测。
- **下一步 + 别碰**：改层名/职责只动 `LOGIC_LAYERS`（表自动跟随）；给表加列要同时改表头 `_lth(...)` 与行内 `<td>` 顺序，并重算 `min-width`；不要恢复卡片网格除非用户明确要求。

## v1070 · 2026-11-23 · 阈值表列序：当前值挪到出厂值之后

- **改了什么**：`edit_work/index.html`（徽标 v1070，注释块 `fw2_v1070_sigthr_colswap`）——表头与行内单元格顺序由「当前值｜范围｜出厂值」改为「范围｜出厂值｜当前值」，`stMsg` 文案同步；`_valCell/_defCell/_rngCell` 函数体未动，`st_*` id 与 `sigThrEdit` 未动。
- **未验证的假设**：①列宽沿用了原值（1018px 总宽），窄屏横滑量仍 544px，未在手机真机测；②列序改动属显示层，未重跑阈值引擎的联动回归（只核了单格写入与「已改」标记、23 行 8 列计数）。
- **下一步 + 别碰**：以后加列要同时改两处——表头 `_th(...)` 串与行内 `<td>` 顺序，错位不会被门禁抓到，只能靠渲染截图；改完照旧用 `_push_index_v1070.py` 类比脚本单推（整包 push 仍被 fund 数据门禁拦）。

## v1069 · 2026-11-23 · 信号阈值（纲领）改表格（23 行 × 8 列）

- **改了什么**：`edit_work/index.html`（徽标 v1069，注释块 `fw2_v1069_sigthr_table`）——`sigThrCardHtml` 里卡片网格 `grid(gSig)/grid(gMech)` 换成一张表：组（rowspan 10/13）｜代码｜中文名｜口径｜当前值｜范围｜出厂值｜生效点；新增 `ROWS` 元数据与 `_valCell/_defCell/_rngCell`。`st_*` id、`sigThrEdit/sigThrApply/SIG_THR_*` 一字未改。
- **未验证的假设**：①口径列与生效点列的文字是我按现行代码逐条归纳的，未逐条对页面文案做一致性断言（例如 T16 的「窗口」单位写「自然日」，代码只按天算未区分交易日/自然日）；②出厂值列对比的是 `SIG_THR_DEF`，若用户曾把某项改成与出厂相同值再改回，不会留「已改」痕迹（设计如此）；③窄屏 540px 时表格需横滑 544px，未在手机真机测。
- **下一步 + 别碰**：后续加阈值项＝往 `ROWS` 加一行 + `SIG_THR_DEF/LIM/UNIT/NAME` 同步，别在表里手写 HTML；`组` 列的 `_grp.n` 是写死的 10/13，加行要一起改；发布仍走 `_push_index_v1069.py` 类单文件推送（整包被 fund 数据门禁拦）。

## v1068 · 2026-11-23 · 总纲导航：信号阈值（纲领）挪到 ⑧ 准入规则之后

- **改了什么**：`edit_work/index.html`（徽标 v1068，注释块 `fw2_v1068_sigthr_after8`）——`logicLayerHtml` 里删掉八层网格下方的全宽「独立」入口条，把这颗按钮作为网格第 9 格排在 ⑧ 之后（`grid-column:span 2`、虚线琥珀底、首行「独立 · 不属于八层」/「23 项 · 点开 →」）。点击仍 `logicGo('sigthr')`，阈值卡本体、三态、回测全未动。
- **未验证的假设**：①只在 Chrome（本机 + 线上 Pages）看过 9 格布局；窄屏（< 520px）时 `minmax(104px,1fr)` 会退成 3 列，第 9 格 span 2 可能挤到第 4 行——未逐档核；②按用户截图理解为「放进网格、紧跟 ⑧」，若他本意是「整条移到 ⑧ 层正文之后仍保持全宽」，需要回退这一版（备份 `D:\Temp\index_v1067_before_v1068.html`）。
- **下一步 + 别碰**：强刷线上看 9 格与「点开 →／当前视图」；别动 `LOGIC_LAYERS`（8 条）与 `logicCur()` 的 `sigthr` 分支——第 9 格只是导航 DOM，不是第 ⑨ 层；整包 push 仍被 fund 数据门禁拦，发前端用 `_push_index_v1068.py`。

## v1067 · 2026-11-23 · T10 开关「关→生效」（纲领基线 L4）

- **改了什么**：`edit_work/logic-state.json` 的 `rules.T10` `off→on`、`ver` L3→L4、`counts 15/24/20`、`fingerprint 4441c63b`；本机与线上浏览器草稿 `fw2_logic_v1` 删除 `rules.T10` 覆盖键（让读取链回落到基线）；新增单文件发布器 `edit_work/_push_logic_state.py`。index.html 与徽标未改（仍 v1067）。
- **未验证的假设**：①只在 Chrome 本机与线上两个 origin 上验过「删草稿键→基线生效」，Firefox/Safari 或其它设备未试；②基线里 `T2` 仍为「关」，而本机草稿是「生效」——这是本次之前就存在的草稿差，本次没有替用户采纳，未验证两者并存时页面计数是否只差 1；③`verify_logic_state.py` 只校结构/计数/指纹，不校「T10 与 R7 共用 rebal 键」的语义冲突（R7 本来就是生效，引擎侧行为未逐位复算）。
- **发布**：`caifu/logic-state.json` 1,964 B / blob `f4a5edcf4c23` / `BYTE_MATCH True` / 远端 `ver=L4 T10=on`。整包 `push_gh_v39.py` 被 `fund_monthly`（verify_dual_source、verify_acc_nav）与 `fund_daily` 的存量数据门禁拦下（78 处发布文件与线上不一致），**与本次改动无关**，故改单文件推送；下次谁要整包发布，先修数据链，别 `SKIP_GATE` 蒙过去。
- **下一步 + 别碰**：要复验就强刷线上信号页看四行「偏离 ≥5pp → 再平衡」；别碰 `logic-state.json` 其余 58 条与 `rulesBT`（六条准入）；改 T10 参数（5pp）仍走总纲「信号阈值（纲领）」独立视图，别去改 `logic-state.json`。

## v1067 · 2026-11-23 · 5 项机制参数接实盘

- **改了什么**：`edit_work/index.html`（徽标 v1067，tag `fw2_v1067_live_params`）——①T10 一套口径（`sigThr()` 末尾 `o.band = o.slotBand`、`sigThrApply` 写 `C.barbell.band = o.slotBand`、`sigThrEdit` 双向同值）+ 导出 `window.sigThr`；②刹车接 `bkExitN/bkExitAct`（`brakeMA200()` 数连续破 MA200 天数、`_bkExitN/_bkExitAct`、`brakeStateOf` 先判破线、刹车卡「破线 x/N 日」副行与「破线冻结/清仓」下一档、分位卡「清仓 · 破线刹车」）；③建仓/定投接 `investMode/baseRatio`（`_planCfg/_planScale/_dcaFirst/_buildTxt`、`liveMonthly` 三态、`_dcaProg` 首笔+月投×期数、主表 `</tbody>` 前尾行「建仓口径」）；④修 T10 段市值取数（`h.qty·h.price` 已不存在 → `marketValue → mv → 份额×净值`）。
- **未验证的假设**：①~~T10 四档行不出~~ **已追查到底（不是 bug）**：行已产生（`rows.hold` 4 条 act、tot 18,112），被 `logicSigMark` 按投资总纲 T10「关」→ `_lgF` 过滤；内存放行后四行「偏离 ≥5pp → 再平衡」正常渲染，还原即消失。T10 阈值 DOM 实证补齐；要不要上线由用户把总纲 T10 改「生效」（同键 R7 一并开）；②`brakeMA200()` 用 200 日均线、不足 201 点返回 null（「待加载」），未对每只标的逐只核 200 个净值点是否齐；③建仓口径的「首笔合计/月投合计」是逐行累加，未与旧口径（`sumMonthly×_ME`）做 drip 态逐位对齐断言（只做了页面读数：3,335 vs 旧基线目测一致）。
- **发布**：master `089ec40136b3`；contents 5,113,283 B / blob `a1d455a749e8`；git blobs 原始字节 `BYTE_MATCH True`、锚点 16/16。发布前 `_audit_alloc_cols.py` 的 D02/D04/E07（写死 v896 `_dcaMonthly × _ME` 旧公式）拦下本次推送，已按 v1067 链路升级断言（PASS 47:3 → 50:0）；这是「口径变了、硬卡也要跟着定义清楚」，不是放宽。
- **下一步 + 别碰**：强刷 `?t=v1067live` 验收五条（band 5→7 同步 / 刹车 N=1+清仓 / 建仓口径三态 / 分位卡冲突 / 来源行文案，详单见 README「下一步」v1067 条）。别碰：`SIG_THR_ENG` 白名单（引擎仍只这 10 项）；`band` 与 `slotBand` 双写是有意的（合并成 22 项要另开一版改全站「23 项」文案）；建仓口径尾行必须在 `</tbody>` 之前（挪到 `</table>` 外会拆掉 `_audit_plan_merge_v895` B03 锚点）。

## v1066 · 2026-11-23 · 信号阈值＝总纲内「独立入口 ＋ 独立子视图」（方案 B）

- **改了什么**：`edit_work/index.html`（徽标 v1066，tag `fw2_v1066_sigthr_view`）——①`logicCur()` 放行 `sigthr`（不进 `LOGIC_LAYERS`、不是第 ⑨ 层）；②`renderLogicView()` 加 `_sigMode`，独立视图下 `L` 只占位；③八层按钮组之后加一条全宽入口「独立 · 信号阈值（纲领）｜23 项执行数值 · 不属于 ①–⑧ 任一层」（右「点开 →」/「当前视图」）；④拼装互斥：`host.innerHTML = a + b + (_sigMode ? sigThrCardHtml(true) : 普通层)`，普通层页尾不再挂卡；⑤`sigThrCardHtml(standalone)`——独立态去虚线、标签「独立视图」、右上「← 返回八层 ① 选品」；⑥信号页 `_stLine` 按钮跳总纲后 60ms 直落 `sigthr`；⑦徽标＋注释块。新增核验脚本 `_verify_online_v1066.py`。
- **未验证的假设**：①刷新页面后不保留独立视图（首入强制落 ① 选品，与八层一贯行为一致，属设计内，非 bug）；②线上 console 里 478 条 `ERR_FAILED` 为外部取数资源失败（本地/线上均同，v1059-v1065 一直有），本次**未**逐条归类，只确认 0 条 JS 异常；③仍未接实盘的 5 项（`slotBand` / `bkExitN` / `bkExitAct` / `baseRatio` / `investMode`）与 `v11Pct` 的实盘口径未动，仍见 README 待决。
- **下一步 + 别碰**：强刷 `?t=v1066live` 验收五条（入口条位置/独立视图结构/切层回退/改值联动/信号页直落，详单见 README「下一步」v1066 条）。别碰：`LOGIC_LAYERS` 数组本身（`sigthr` 是旁路，塞进去会变第 ⑨ 层、破坏八层计数与进度文案）；`sigThrCardHtml(false)` 分支（回退到普通层挂卡就与独立视图重复）；`SIG_THR_ENG` 白名单顺序。

## v1065 · 2026-11-23 · 来源行只留路径 ＋ 机制参数接实盘（8/13）＋ 阈值卡独立模块化

- **改了什么**：`edit_work/index.html`（徽标 v1065，tag `fw2_v1065_sig_src_path / sig_thr_exec / sig_thr_indep`）——①交易信号页来源行删掉全部当期数值，只留「阈值来源：投资纲领 →『信号阈值（纲领）』（共 23 项…）」＋跳转按钮；②`sigThrApply()` 新增映射：`gridStep→C.grid.step`、`gridAmt/fund/ext→C.grid.amt/fund/ext`、`postSellLo→C.postSellDD`、`postSellWin→C.t16WindowDays`、`addAmt→C.addAmt`、`v11Pct→C.v11Pct`；实盘 T13 网格行显示「网格买入 ¥500/档 · 上限 ¥10000 · 预算内／可用备用金」，T7 补仓行显示「每档补目标额 20%」；③阈值卡外包 `#sigThrModule`（顶虚线＋「独立模块」标签＋「不属于 ①–⑧ 任一层」），卡内机制组下加「已接实盘 / 仍只作纪律口径」说明。
- **未验证的假设**：①`postSellLo/postSellWin` 已映射进 `C.postSellDD/t16WindowDays`，但当前持仓没有卖出基准记录，**T16 行不出现**，无法做视觉验证（仅代码路径＋既有单测口径）；②`v11Pct` 只改注册表/文案，实盘 V11 池比例由后端 `v11-signal.json` 决定，改纲领不会改已算好的建议；③仍未接实盘：`slotBand`（T10 四档带宽，实盘 T10 用「偏离带」band）、`bkExitN` / `bkExitAct`（实盘刹车卡走 `BRAKE_T` 逐只 mdd，不读这两个）、`baseRatio` / `investMode`（建仓/定投计划走策略快照）。
- **下一步 + 别碰**：线上 `?t=v1065live` 验收来源行只有路径、网格/补仓建议带纲领数值、独立模块标签可见。别碰：`SIG_THR_ENG` 白名单顺序（引擎 10 项）；`C.grid.step` 同时被回测 `btCfg` 与实盘用，两套键名不同别混。

## v1064 · 2026-11-23 · 机制参数搬进纲领＋阈值卡独立成模块（页面末尾，⑧ 之后）

- **改了什么**：`edit_work/index.html`（徽标 v1064，tag `fw2_v1064_sig_thr_move`）——①阈值模块整块重写：`fw2_sig_thr` 由 10 项扩到 **23 项**（信号 10 ＋ 执行机制 13：`gridStep/gridAmt/gridFund/gridExt/addAmt/postSellLo/postSellWin/slotBand/v11Pct/bkExitN/baseRatio/investMode/bkExitAct`），新增 `SIG_THR_OPT`（三项 select），`sigThr()` 缺失键补默认、`sigThrEdit` 按 num/select 分型校验，卡内分「交易信号阈值（T1–T10）／执行机制口径」两组；②`thesisRuleCfg()` 去掉 `btCfg('plan')` 兜底，全量 `sigThr()`＋`tgThesis()`；`btRuleCardHtml` 删 `_btNumRows` 与「（⑧-A 数值）」行内标注，`_rFoot` 改「全部取自投资纲领…不含任何 ⑧-A 实验数值」；③`renderLogicView` 拼接改为 `a + b + c + _btRuleCard + … + sigThr`，阈值卡落在 `#tg-logic` 最末（`after=none`）；④数据管理 `fw2_sig_thr` 行改 23 项口径。`sigThrApply` 仍只覆盖引擎 10 项，回测引擎/`fw2_bt_plan` 零改动；`_globals_baseline.json` 仍 252 键。
- **未验证的假设**：①13 项机制参数只改规则卡/提示文案，尚未接进实盘执行链（设计如此，用户选「搬」时已确认）；②旧 10 键 `fw2_sig_thr` 自动补 13 项默认——只在本地「清空后新建」与「10 键旧档」两条路径验过，未在真实浏览器旧档上逐项比对。
- **下一步 + 别碰**：强刷 `?t=v1064live` 验收 23 项与页尾位置（详单见 README「下一步」v1064 条）。别碰：`sigThrApply` 的 10 项白名单（`SIG_THR_ENG`）——13 项写进去会改实盘信号；`btRuleCardHtml` 的 `opts.cn` 仍只允许总纲传；回测页 `btCfg` 口径不动。

## v1063 · 2026-11-23 · 规则卡改「纲领口径」＋信号页阈值出处

- **改了什么**：`edit_work/index.html`（徽标 v1063，tag `fw2_v1063_thesis_rules`）——①交易信号页 `body.innerHTML` 前插来源条（`_stLine`，七项中文名＋代码＋当期数值＋「去投资总纲改阈值 →」）；②`btRuleCardHtml(cfg, opts)` 新增 `opts.cn`：状态改读 `window.logicStateEff`（`fw2_logic_v1` 三态生效/观察/关），阈值来自 `window.thesisRuleCfg()`（`fw2_sig_thr`＋`fw2_tg_thesis`，`sl`/`addDD` 取绝对值），标题/副标题/表头「本次→纲领」随口径切换，卡下脚注写明三个键与「七个机制参数仍取 ⑧-A」，R1/R3/T7/R9/T10/T16/V11 行内标「（⑧-A 数值）」；③`tgThesis` 补 `window.tgThesis` 导出。`_globals_baseline.json` 250 → **252 键**。回测引擎、`fw2_bt_plan/hold/custom`、三态下发、注册表条目均零改动。
- **未验证的假设**：无（本地＋线上真渲染；状态与 `fw2_logic_v1` 逐条比对一致；纲领改 −10/−25 后 R6/T7 文案随动，测试值已清回 null）。过程中修掉两处自身回归：内联 `onclick` 的 `'…'` 打断 JS 单引号字符串（改 `&quot;` 实体）；直接传 `addDD1=-25` 出现「−-25%」（改 `Math.abs`）。
- **下一步 + 别碰**：按 README「下一步 v1063」六条验收；**别**把状态列改回从 cfg 布尔推导（那就回到「按 ⑧-A 实验参数算」的老问题）；**别**在 `thesisRuleCfg()` 里把 `sl/addDD` 传成负值（卡内文案自带「−」）；**别**把 `opts.cn` 传给回测页调用（回测页要的是本次实际 gridStep/结果）。七个机制参数是否进纲领待用户拍板（README 待决）。
- **发布**：5,089,066 B、SHA256 `55361DA86B911E6F346045188117AFE2766D984376AB868213C2B4E902F8D7A2`，git blobs API 逐字节 `MATCH=True`。
- **截图/备份**：`D:\Temp\v1063_local_rulecard.png`、`v1063_local_rulecard_foot.png`、`v1063_local_sigsrc.png`、`v1063_live_rulecard.png`、`v1063_live_sigsrc.png`；`index_v1062_before_v1063.html`。

## v1062 · 2026-11-23 · 实盘信号阈值进「投资纲领」（总纲新增「信号阈值（纲领）」卡）

- **改了什么**：`edit_work/index.html`（徽标 v1062，tag `fw2_v1062_sig_thr`）——新增 `SIG_THR_KEY='fw2_sig_thr'` / `SIG_THR_DEF`（10 项出厂） / `SIG_THR_LIM` / `SIG_THR_NAME` / `SIG_THR_UNIT` / `sigThr()`（读存储＋逐项范围校验＋补仓两档序校验） / `sigThrApply()`（覆盖 `window.SIGNALS_CFG` 的 9 标量＋`barbell.band`，**在 `SIGNAL_REGISTRY` 构建前执行**） / `sigThrCardHtml()`（挂 `window.sigThrCardHtml`，插在总纲 A 卡与八层导航之间） / `window.sigThrEdit(id,raw)` / `window.sigThrReset()`；`_sigCacheKey` 末位并入 `fw2_sig_thr`；数据管理本机存储卡新增该行。`_globals_baseline.json` 247 → **250 键**（`sigThrEdit`/`sigThrReset`/`sigThrCardHtml`）。回测侧零改动（`fw2_bt_plan` 与回测引擎未碰）。
- **未验证的假设**：无（本地＋线上都做了真渲染：改值→写盘→信号页 T1 阈值变「≥ +12%」、行动「+24% 再减1/4」；越界 500 与补仓逆序 -10 均红字回退；恢复出厂后键为 null、各框回厂；线上改 `-8→-9` 写盘后恢复出厂已把测试值清干净）。首版曾因 `sigThrCardHtml` 定义在 IIFE 内、调用点在外而 `ReferenceError`，已改 `window.sigThrCardHtml` + `typeof` 兜底。
- **下一步 + 别碰**：按 README「下一步 v1062」六条验收；**别**把 `sigThrApply()` 挪到 `SIGNAL_REGISTRY` 之后（会先按出厂值建好注册表，阈值文案与判定脱节）；**别**让 `sigThr()`/`sigThrEdit` 接受超出 `SIG_THR_LIM` 的值（越界须回退并提示）；**别**把 `fw2_sig_thr` 混进 `fw2_bt_plan` 或回测参数页（纲领只影响实盘信号，回测按自己的底稿）。
- **发布**：5,082,239 B、SHA256 `87A01DF215CFBD60465A06EDF85129FA098CDF3FD41933741D723759DBC15DDB`，git blobs API 逐字节 `MATCH=True`。
- **截图/备份**：`D:\Temp\v1062_local_sigcard.png`、`v1062_local_sigcard2.png`、`v1062_live_sigcard.png`；`index_v1061_before_v1062.html`。

## v1061 · 2026-11-23 · 参数 tab 改名「回测参数（全量底稿）」

- **改了什么**：`edit_work/index.html`（徽标 v1061，tag `fw2_v1061_base_label`）——可见文案「回测参数（实验）」11 处 → 「回测参数（全量底稿）」（tab、⑧-A 子页签与卡头、保存提示、总纲卡指路按钮 2 处、参数指路文案、未填可投资金报错）。**零逻辑**：无代码分支、无存储键、无默认值改动；注释里旧名 15 处保留作历史。
- **未验证的假设**：无（改动纯文案，本地与线上均已真渲染核对；47 控件、保存提示、旧名 0 命中）。
- **下一步 + 别碰**：按 README「下一步 v1061」五条验收；后续新增文案一律用「回测参数（全量底稿）」，别再出现「回测参数（实验）」或「母版」（`docs/FRONTEND.md` v1059/v1060/v1061 三节为准）。
- **发布**：head `0683f49b3614`，5,072,939 B、SHA256 `F1E80D00EAED4982E33EEC81A2D38B5A2266E46279A339DF89B90FEF25DB1111`，blob `MATCH=True`。
- **截图/备份**：`D:\Temp\v1061_local_param.png`、`v1061_live_param.png`；`index_v1060_before_v1061.html`。

## v1060 · 2026-11-23 · 一次性迁移旧纲领值 + 清掉 tgGotoCard 死代码

- **改了什么**：`edit_work/index.html`（徽标 v1060，tag `fw2_v1060_mig_goto`）——新增 `tgMigrateOnce()`（`tgThesis()` 之后、模块加载时跑一次）：标记 `fw2_tg_thesis_mig` 未置、且 `fw2_tg_thesis` 不存在时，把 `fw2_bt_plan` 里齐全的 `tgtAnn/ddBudget/rf` 搬入纲领键并置标记；总纲卡新增 `#tgMigNote` 绿字说明。删除 `window.tgGotoCard`（v1059 起零引用的「参数页跳总纲」死路径）。`_globals_baseline.json` 248 → **247 键**（note 追加删除说明）。
- **未验证的假设**：线上标签页未见迁移绿字，推断是该浏览器 `fw2_tg_thesis` 在此前某次加载已存在（`fw2_tg_thesis_mig`=1），迁移按设计不覆盖；迁移路径本身已在本地造场景（12/25/1.8）实证。
- **下一步 + 别碰**：`?t=v1060live` 按 README「下一步 v1060」五条验收；**别**把迁移写进回测写入路径（只在 `tgMigrateOnce` 里搬一次）、**别**让迁移覆盖已有纲领键、**别**恢复任何「参数页 → 总纲」跳转。控制台 `ERR_FAILED` /「[nky] 取数失败」经 v1059 备份页同环境对照为既有问题，不在本轮范围。
- **发布**：head `45ff84abe22f`，5,072,564 B、SHA256 `16C61B653BF87B89D7DBB6B584EF85034AC224191C56FF78BE722577BA65D990`，git blobs API 逐字节 `MATCH=True`。
- **截图/备份**：`D:\Temp\v1060_local_tg.png`、`v1060_local_param.png`、`v1060_live_param.png`；`index_v1059_before_v1060.html`、`v1060_ls_before.json`。

## v1059 · 2026-11-23 · 纲领 / 实验拆成两套（总纲三键独立存储、参数页恢复可编辑、页面去掉「母版」）

- **改了什么**：`edit_work/index.html`（徽标 v1059，tag `fw2_v1059_thesis_split`）——新增 `fw2_tg_thesis` 独立键（`TG_THESIS_KEY`/`TG_THESIS_DEF`/`tgThesis()`），`tgPlanEdit` 只写纲领键、删 `window.tgSetPlan`（撤销 v1058「纲领写回测母版 + 清 ⑧-B/⑧-C 覆盖」）；`btParamsHtml` / `btComboBarHtml` 三键恢复可编辑（47 控件）；`btCollectDom` 对 `tgtAnn/ddBudget/rf` 放行、新增 `btBindAuto()`（参数页也有 change 委托）＋ `#btParamSaveMsg`；全站可见「母版」改「实验 / ⑧-A」，注释保留并注明历史术语；三态条改「规则开关来源：投资总纲三态（只作用于本次运行，不写存档）」并在参数页加「不看纲领，按参数页值跑」开关；数据管理本机存储卡新增「投资纲领三键」行。`_globals_baseline.json` 249 → **248 键**（删 `tgSetPlan`）。
- **未验证的假设**：宽屏侧栏 9 项仍未真机截图（视口 538×643）；v1058 曾写入用户浏览器 `fw2_bt_plan` 的三键未迁移进 `fw2_tg_thesis`（默认 10/20/1.59），若用户此前改过纲领值不会继承——已列入 README「待决」等用户表态。
- **下一步 + 别碰**：`?t=v1059live2` 按 README「下一步 v1059」五条验收；**别**恢复 `window.tgSetPlan`、**别**把 `btIn_tgtAnn` 再改成只读（双写 / 静默不存都是这两处复发的），**别**清 `fw2_bt_plan` 里已有的三键（那是实验参数，与纲领无关）；**待清**：`window.tgGotoCard` 是 v1058 留下的「跳总纲」死代码（已无按钮引用），删它需同步 `_globals_baseline.json`（248 → 247）并重发版，建议并入 v1060。
- **发布**：head `86a371984e12`，5,070,884 B、SHA256 `F1CA9106…`，git blobs API 逐字节 `MATCH=True`（raw.githubusercontent 有缓存，别用它判）。
- **截图**：`D:\Temp\v1059_local_tg.png`、`v1059_local_param.png`、`v1059_live_param.png`、`v1059_live_bt8.png`；回滚备份 `D:\Temp\index_v1058_before_v1059.html`。

## v1058 · 2026-11-23 · 总纲卡三键就地可改（母版唯一写入口）

- **改了什么**：`edit_work/index.html`（徽标 v1058，tag `fw2_v1058_tg_write`）——总纲卡 `tgtAnn`/`ddBudget`/`rf` 改 number 输入（`tgIn_*`）；新增 `window.tgSetPlan`（范围校验 + `btSavePlan` 只 patch 三键 + 清 `fw2_bt_hold`/`fw2_bt_custom` 整组覆盖）与 `window.tgPlanEdit` / `window.tgGotoCard`；`btParamsHtml` 三行、`btComboBarHtml` 三行改只读指路。`edit_work/_globals_baseline.json` 249 键。
- **未验证的假设**：宽屏侧栏 9 项仍未真机截图（视口 538×643）；用户端 localStorage 若有更早的 `fw2_bt_plan` 缺这三键，仍走 `btCfg` 默认 10/20/1.59，未实测该分支（默认值来自 `BT_DEFAULTS` 同源）。
- **下一步 + 别碰**：`?t=v1058live` 验收三件事（改 12 → 0.52、改 99 → 回退、参数页只读 + 跳转）；不要恢复 ⑧-A 的 `btIn_tgtAnn`（双控件串值，v1002 教训）。
- **发布**：head `fe9bcd25127b`，raw 5,069,611 B、SHA256 `50988D78…`、逐字节 `MATCH=True`。
- **截图**：`D:\Temp\v1058_local_tg_final.png`、`v1058_local_param_ro.png`、`v1058_live_tg.png`、`v1058_live_param.png`。

## v1057 · 2026-11-23 · 投资总纲改名后的文案统一

- **改了什么**：`edit_work/index.html` 4 处可见文案「投资逻辑」→「投资总纲」（信号页筛选条 / 信号注册表空态 / 资产配置待办条统计 / 同条三态说明）+ 徽标 v1057 + 注释 `fw2_v1057_copy_unify`。零逻辑改动。
- **未验证的假设**：宽屏侧栏 9 项仍未真机截图（视口固定 538×643，按 36px×9≈332px 估不溢出）。
- **下一步 + 别碰**：`?t=v1057live` 只核三处文案；总纲 59+6 条、参数页 47 控件不要动。
- **发布**：head `384a4b177105`，raw 5,062,093 B、SHA256 `7243F417…`、逐字节 `MATCH=True`。
- **截图**：`D:\Temp\v1057_live_alloc.png`、`D:\Temp\v1057_live_signal.png`。

- **2026-11-23 · v1056 投资逻辑升为独立一级模块「投资总纲」，回测参数迁回策略执行**
  - **改了什么**：`edit_work/index.html` → v1056（徽标 `v1056` + 注释块 `fw2_v1056_invest_master`，L1553 长行内）。①导航第 9 项 `data-view="tg"`（我的持仓之后、策略执行之前）+ book-open 图标 CSS；②新增 `#view-tg` 独立 section（`#tg-logic`）+ `VIEW_META.tg` + `renderCurrentView` 的 tg 分派；③`renderLogicView` host 改 `#tg-logic || #stp-logic`，总纲卡 10%/≤20%/rf 1.59/Calmar 0.42 改为实时读母版 `tgtAnn`/`ddBudget`/`rf`；④`#stratTabs` 去 `logic`、`alloc` 默认 active、新增 `param` tab + `#stp-param`、`btParamTabsHtml`/`renderBtParamPane`/`btParamTab`（在 `renderBtCfgHost` 之后）；⑤`__stratActiveTab` 默认 alloc、`__stratPaneRender` 加 param、`switchStratTab('logic')` 转 `showView('tg')`；⑥`logicTraceTabsHtml` 收成单条「⑧ 准入规则 · 怎么证明一条规则算数（BT1–BT6 准入验证）」+ 指路按钮，`_btParamTab=false`，`renderLogicView` 不再渲染 `btCfgHost`；⑦`btCfgGo` 改跳策略执行 param tab；⑧`LOGIC_LAYERS` ⑧ 层 name 改「准入规则」；⑨窄屏 `#stratTabs .st-tab` padding 收紧、`.mobile-tabbar .tab` 改 `flex:1 1 0` 等分（9 项不挤出）；⑩`_globals_baseline.json` 243 → 246 键。
  - **未验证的假设**：⑴**桌面宽屏侧栏未真机截图**——浏览器视口固定在 538×643，只验了窄屏底栏 9 项（`clientWidth=scrollWidth=529`）；宽屏侧栏按 `.nav-item` 高约 36px×9 ≈ 332px < 643 估算不溢出，但没实拍。⑵**总纲目标函数三键只读**，写入口仍只在「回测参数（母版）→ ⑧-A」——这是为防 v1002 双控件串值做的取舍，用户可能希望「总纲里就地改」，未表态。⑶`?view=tg` 深链只在本机 8765 验过，线上未验。
  - **下一步 + 别碰**：发布后强刷 `?t=v1056live` 按 README「下一步」首条五点验收；再改这块先跑 `check_js.py`（21 块）/ `check_html_comments.py`（285 处）/ `check_globals.py`（246/246）/ `verify_manifest.py`。**别碰**：①母版 `fw2_bt_plan` 只能有一处控件（参数页 `#stp-param`），别在总纲再加输入框；②别把 ⑧ 层的参数三卡恢复到总纲（`_btParamTab` 恒 false 是有意的）；③`switchStratTab('logic')` 转 `showView('tg')` 是旧深链兼容，别删；④`.mobile-tabbar .tab` 的 `flex:1 1 0` 是 9 项铺满的关键，改回固定 60px 会把「数据管理」挤出屏幕。
  - **回滚点**：`D:\Temp\index_v1055_before_v1056.html`（5,053,294 B，改动前完整备份）；README 备份 `D:\Temp\README_v1055pre.md`。
  - **发布**：master `17ad1e2e9ecbf7f2122e4c594014cff28ced708d`（提交信息「数据更新（离线刷新 + 双轨发布）」）；`caifu/index.html` **5,061,774 B**、raw SHA256 `307FDEB903F6809D68CF8CBECC523CCD34E6A54272D832568E53E8E5E26EEFA5` 与本地逐字节一致（`match True`）。线上 `?t=v1056live` 真渲染：徽标 **v1056**、导航 9 项、「投资总纲」页 title/sub 正确、卡内 10% / ≤20% / 1.59% / Calmar 0.42、总纲 `btIn=0`/`btCfgHost=0`；策略执行 5 tab 一行、param 页 47 控件、参数来源「投资总纲」；底栏 9 项 `clientWidth=scrollWidth=529`。**发布插曲**：首次推送被 `_audit_plan_merge_v895.py` 的 A01 硬卡拦下（它写死「logic」在现役 tab 里）——已把断言改为 `['alloc','bt','bt','param','review']`、A04 改为四 pane 且断言 `stp-logic` 不存在，复跑 **PASS=38 FAIL=0** 后再推。
  - **截图**：`D:\Temp\v1056_a_master3.png`（总纲首屏：动态 10%/20%/1.59%/0.42 + 八层）、`v1056_b_admission2.png`（⑧ 层 5 列 6 行）、`v1056_c_params3.png`（策略执行 5 tab 一行 + 回测参数（母版）三卡）、`v1056_d_version.png`（版本与证据 / BT5 证据台账 / 池全量对照）。

- **2026-11-21 · v1053 月度待办事件接三态（P1 第一段）**
  - **改了什么**：`edit_work/index.html` → v1053（徽标 `v1053` + 注释块 `fw2_v1053_todo_logic`）；`STRATEGY_SNAP.events` 18 条各补 `rule`（16 条映射到八层、id16「001015 经理变更」无对应码不写）；`renderStratTodo` 事件循环接 `logicStateEff(e.rule)`（关→不提示 / 观察→标灰列出且不计触发 / 生效→计入）+ 摘要「◦ 观察 N（不计触发）」+ `badge.obs:'#6b7280'` + 折叠区口径说明；`edit_work/logic-state.json` `scopes.todo=true`；`edit_work/gate.py` 新增 `logic_state` 数据集（`verify_logic_state.py`、`stamp=None`，`MANIFEST` 告警 2→1）。
  - **未验证的假设**：⑴id14「组合回撤 -20%/-30% 两档逆向加仓」→`T7` 回撤补仓、id18「簇合计 >4 万停止补仓」→`T9` CAP 超限，是按 `ref` 章节 + 语义判的，未与你确认；⑵id16 无码是有意为之，未新增注册表条目；⑶「观察」事件「标灰列出但不计触发」是本轮取舍，未拿到你的页面确认。
  - **下一步 + 别碰**：线上强刷 `?t=v1053live` → 策略执行 → 资产配置按 README「下一步」首条四点验收；再改动这块先跑 `check_js.py`（21 块）/ `check_html_comments.py`（279 处）/ `check_globals.py`（243）/ `verify_logic_state.py` / `gate.py --datasets logic_state --check`。**别碰**：`events` 的 `rule` 是唯一真源（别再建映射表）；`obs` 事件必须「列出但标灰且不计触发」；`logic_state` 闸门组不要写戳记（文件被前端逐次 fetch 比指纹）；id16 别硬塞码。
  - **发布**：master `cc7d6125583709eedda793f95382b7dfe227f8ad`；contents `caifu/index.html` **5,030,969 B**、raw SHA256 `4E39DD8564EB12A7D58A9511A7224E11C0750880515D2209F75CC403D596D8FA` 与本地逐字节一致（`BYTE_MATCH True`）；`caifu/logic-state.json` 1,749 B（`scopes.todo=true` 已上线）。**注意**：`push_gh_v39.py` 两个 `[200]` 之后在收尾读回执时报 `IncompleteRead` 并以退出码 1 结束——写入已成功，别据此重推。线上 `?t=v1053live` 徽标 v1053、待办 2 项 / △ 临界 1 / 14·24·21；线上对照 `T1`→关 ⇒ 2→1 项且事件条消失，写回后复原（草稿 878 B 原文归还）。
  - **回滚点**：`D:\Temp\index_v1052_before_v1053.html`（5,029,130 B，改动前完整备份）。
  - **截图**：`D:\Temp\v1053_todo_T1off.png`（本地 T1=关：待办 1 项、事件条消失）、`v1053_todo_restored.png`（本地还原后 2 项 / 14·24·21）、`v1053_live_todo.png`（线上 v1053 同状态）。

- **2026-11-21 · v1052 投资逻辑三态接管交易信号页与待办（P0 · B 路线第一段）**
  - **改了什么**：`edit_work/index.html` → v1052（徽标 + 注释块 `fw2_v1052_logic_brain`）；新增 `edit_work/logic-state.json`（59 条可执行 + `rulesBT` 6 条，指纹 c7813842，counts 14/24/21）。信号页：`_holdSig` 与 chip 三档计数过三态、`_sigF` 过滤后对 obs 行浅拷贝降档（act/near→watch）、chip 条加「关 N 行 / 观察 M 行」；待办条摘要加「生效 14 · 观察 24 · 关 21」。`logicStateEff` 未知码返回 null（无意见），规则码来源 `sig + code`（市场行码在 `code`）。全局键 5 个已登记（基线 238→243）。
  - **未验证的假设**：⑴「观察降档」是否合你意（方案文档里两种呈现都写了，本轮选「显示但降为观察档」）；⑵`S.events` 无规则码 → 待办事件不受三态影响，这是数据缺口不是漏做；⑶线上未发布 `logic-state.json` 时 fetch 404 回退路径只在本机 8765 验过（发布后会变成 200，需再看一眼首屏）。
  - **下一步 + 别碰**：跑 `check_js.py` / `check_html_comments.py` / `check_globals.py`（应为 243/243 PASS）/ `verify_manifest.py`；线上强刷 `?t=v1052live` 按 README「下一步」首条三点看。**别碰**：`logicSigMark` 的「未知码＝无意见」、obs 行降档只改拷贝、`M\d+` 正则、`S.events` 在有规则码前别硬接。
  - **发布**：master `a08334eee647af5ca46421f257005d6fe96976b2`；contents 5,029,130 B；raw SHA256 `20CDFEFC…` 与本地一致；`caifu/logic-state.json` 已上线（1,716 B）；线上 `?t=v1052live` 徽标 v1052、chip「全部 411 / 动作 71 / 接近 59 / 关 71 行 · 观察 188 行」、待办条 14/24/21。首次推送被 v891 登记审计拦（`unregistered=logic-state.json`），已在 `_gen_data_mgmt.py` DMCONFIG 登记并重跑生成器。
  - **回滚点**：`D:\Temp\index_v1051_before_v1052.html`（5,021,607 B，改动前完整备份）。
  - **截图**：`D:\Temp\v1052_sig_bar2.png`（信号页 chip 三态说明）、`v1052_todo2.png`（待办条摘要 14/24/21）。

- **2026-11-20 · v1014 「策略回测」→「配置回测」+ 结果页运行条参数摘要整行退役**
  - **改了什么**：`edit_work/index.html` → v1014（4,909,496 B，master `b5207cedec6b`，线上 `?t=v1014live` 已验证徽标／tab／旧摘要清零）。两个 tag：①`fw2_v1014_a_cfg_rename`——39 处「策略回测」→「配置回测」（tab、面板标题、⑧-B 口径条、⑧ 层三卡、证据台账空态与提示、数据管理 hint、tooltip、保存提示、各处指路），池名仍 `strategy`（`data-pool`、`fw2_bt_ui_pool`、缓存键不动）；②`fw2_v1014_b_no_runsum`——`go()` 里 `runSum` 参数拼接（本金／区间／投入方式／刹车／年线／止盈止损／网格／备用金／标的池）整段删除，改 `_tips` 数组只留 ※实验口径 与 ⚠ 区间代表性两类提示，空时 `#btRunSum` 置 `display:none`。另同步 `_audit_plan_merge_v895.py` 的 A01／A01b 断言为「配置回测 / 自选回测」。
  - **未验证的假设**：⑴三类区间提示都不命中的区间（5 年窗 2021-07-01、10 年窗 2016-01-04 起）没有实跑，「`display:none` 不留空白」只有代码路径核对、无截图；⑵改名后按旧名检索的脚本（若有）会搜不到，本轮只改了 `_audit_plan_merge_v895.py` 一处断言，未全库扫 `docs/`；⑶「配置回测」与 ⑧ 层卡副标题、⑧-B 参数卡页签的措辞是否完全自洽，只核了页面文本，未逐卡审。
  - **下一步 + 别碰**：验收 `?t=v1014live` —— tab／标题／口径条／空态四处都写「配置回测」；跑一次后运行条只剩提示行（无「本次回测：本金…」）；结论条数字与 v1013 一致。**别碰**：`data-pool="strategy"` 与 `fw2_bt_ui_pool` 的值（改名只改显示名，池键一改历史缓存与旧存档全部失配）；`#btRunSum` 元素保留（删掉参数摘要后它是区间提示与实验口径警告的唯一出口）；`btRun` 引擎本轮零改动，别以「结果没变」为由去动它。
  - **回滚点**：`D:\Temp\index_v1013_before_v1014.html`（4,910,941 B，改动前完整备份）。
  - **截图**：`D:\Temp\v1014_local_result.png`（本地页头，tab/标题/口径条）、`v1014_local_result_b.png`（提示行 + 结论条，参数行已消失）、`v1014_online.png`（线上同页）。

- **2026-11-20 · v1013 回测页黄条退役 + 「持仓回测」改名「策略回测」（内建目标配置 11 只）**
  - **改了什么**：`edit_work/index.html` → v1013（4,910,941 B，master `f915cea0aef5`，线上 `?t=v1013live` 已验证徽标 / tab / 旧文案清零）。三个 tag：①`fw2_v1013_a_stale_off`——`go()` 的 `_stale` 分支不再拿旧 cfg 铺旧结果，改输出「口径已变，上次结果不再展示」+「按当前口径运行回测」并 return，`_staleBar` 置空；②`fw2_v1013_b_strategy_pool`——tab `data-pool="barbell">持仓回测` → `data-pool="strategy">策略回测`，新增 `BT_STRATEGY_PLAN`（11 只 / 22 字段）与 `btStrategyCodes()`／`btStrategyPf()`，`btRun` 入口把 strategy 归一为 custom + 逐只手动权重，`_btPoolKey` 三分支、`switchStratTab` 先写 `fw2_bt_ui_pool`、`go()` 加 `__BT_POOL_MODE` 兜底，⑧-B 标的池行对 strategy 只读；③`fw2_v1013_c_no_html_snap`——`__btHtmlByPool` 与 `lastHtml:` 写入退役，避免跨池铺错结果。另：`_audit_plan_merge_v895.py` 的 A01/A01b 断言同步改为「策略回测 / 自选回测」。
  - **未验证的假设**：⑴页面按可投资金 62,000 跑出 16.00%（node 同参数 100,000 为 14.34%），我把差异归因于「网格单档固定 500 元在更小预算下占比更低」——**没有做单变量归因实验**（固定 62,000、关网格再跑一次对比）来证实；⑵`BT_STRATEGY_PLAN` 里 000912 英大现金宝按 `gs=0 / on=false / sl=0` 处理，未验证货币基金在引擎里是否真走「无净值只有 ret」分支（本轮 40 笔成交里没有它的网格单，只在归因里拿到 +500）；⑶⑧-B 页面对 strategy 只读那行改写后，其余组合级 7 项仍对 strategy 无效却照常显示，未清理、未与用户确认；⑷`fw2_bt_hold` 旧杠铃参数与 `fw2_bt_ui_pool='strategy'` 在本机留痕，换设备行为未测。
  - **下一步 + 别碰**：验收 `?t=v1013live` 按 README「下一步」首条六点看（重点：tab 名、空态文案、全页无黄条、运行后标的池写「自选组合·逐只权重」、改参数后只出「口径已变」）。**别碰**：`btRun` 里 `pool==='strategy'` 的归一那一行不能删（删了 `btPF` 与 `btTargets` 都读不到 `cfg.pf`，会退回杠铃权重）；`go()` 的 `__BT_POOL_MODE` 兜底也不能删（没有它点 tab 仍跑 barbell，实测 13.67%）；`BT_STRATEGY_PLAN` 是「策略回测」唯一内容源，改权重改这里，不要改 ⑧-B 的控件。
  - **回滚点**：`D:\Temp\index_v1012_before_v1013.html`（4,905,260 B，v1013 改动前完整备份）；上一版 `D:\Temp\index_v1012.html`。
  - **截图**：`D:\Temp\v1013_live_d.png`（空态无黄条）、`v1013_live_e.png`（跑出策略结果）。

- **2026-11-20 · v1012 ⑧ 准入层五条校正（回撤进判定 / R4·R5 退役 / BT4 换 BH-FDR / BT3 门槛统一 / BT6 补采纳）**
  - **改了什么**：`edit_work/index.html` → v1012（4,905,260 B / 4,177,743 字符，master `9cef288135a3`，线上 `?t=v1012live` 已验证徽标 / 准入页 / 结论条）。五个 tag 可定向回滚：①`fw2_v1012_a_dd_gate`——结论条 `passAll` 加 `passDD = |mdd| ≤ ddBudget`（原只看年化 + Calmar，年化 25% / 回撤 45% 仍打「✓ 达标」），新增「年化达标、Calmar 也达标但回撤破预算」诊断分支，`ddUse > 100` 标红并追加「（超预算）」；②`fw2_v1012_b_r45_retired`——`SIGNAL_REGISTRY` R4/R5 `def` 改「off（引擎已退役）」，规则卡第 4 列改常量 `false`，说明列与卡尾脚注改写，`logicLoad` 加一次性迁移 `__r45Retired`（只把 R4/R5 从 on/obs 降 off 并记日志）；③`fw2_v1012_c_bt4_bh`——`btSigPersist` 判据 Bonferroni → BH-FDR（p 升序取最大 k 使 p(k) ≤ k/m·0.05，判据＝k ≥ 3 且主导档 ≤ 0.05 且 95% 区间不跨 0），存档加 `alphaBonf / passK / drop:'bh'`，`logicSigJudge` / chips / 横幅 / 卡头三处展示同步，旧记录保留旧口径并加一句「重跑即按 BH-FDR 重判」；④`fw2_v1012_d_bt3_line`——BT3 三项门槛改「年化 ≥ 目标 / 最深回撤 ≤ 预算 / Calmar ≥ 预算线（默认 0.42）」，删掉自相矛盾的「Calmar ≥ 0.5」；⑤`fw2_v1012_e_bt6_adopt`——新增 `logicNextVer` + `window.logicAdopt()` 与版本条「采纳草稿 → L(n)」按钮，`adopted` 字段首次真正被写。另把 BT5「20 个 cfg 全参」改为「全部 cfg + btParamHash 8 位指纹」。
  - **未验证的假设**：⑴R4/R5 退役是按 `_pfOf` 三处返回 `tp1:0/tp2:0`、触发条件 `pf.tp1 > 0` 恒假推的，**没有对全历史成交日志逐笔统计**「v903 后 tp1/tp2 从未成交」；⑵BH-FDR 的 k ≥ 3 门槛是建议值（旧 Bonferroni 在 3/5/10 年窗 15 档全灭，BH 放宽后当前记录仍是 0 档通过），宽严是否合适未与用户核对；⑶`logicAdopt` 只做版本 +1 与日志，**不存规则文本快照**——采纳后再改规则，旧 L2 的内容无从追溯（BT5 快照只管回测参数、不管规则文本），属未补的设计缺口；⑷旧 Bonferroni 记录不自动重算，只加说明句，用户是否接受未问。
  - **下一步 + 别碰**：验收 `?t=v1012live` 按 README「下一步」首条七点逐项看（重点：统计「生效 14 · 观察 24 · 关 21」、R4/R5「○ 关 · 引擎已退役」、BT3 无 0.5、BT4 写 BH-FDR、版本条「采纳草稿」按钮可用、回撤预算改 5% 能出「✗ 未达标 · 回撤预算用 117%」诊断）。**别碰**：回测引擎逐位未改——结论条数字应与 v1011 同口径完全一致；`btSigPersist` 的新旧口径分流靠 `drop === 'bh'` 字段，别给旧记录手填该字段；`__r45Retired` 迁移只跑一次，别在代码里改成「每次都强制降级」（用户若主观想开 R4/R5 会被反复改回）。
  - **回滚点**：`D:\Temp\index_v1012.html`（v1012 完整备份）、`D:\Temp\index_v1011.html`（上一版）。本轮未落新截图（核验走 bu 内联读 DOM）。

- **2026-11-20 · v1011 ⑧-C 自选回测参数与 ⑧-A/⑧-B 分组对齐**
  - **改了什么**：`edit_work/index.html` → v1011（4,895,406 B / 4,171,267 字符，master `97451f29a985`，线上 `?t=v1011live` 已验证徽标）。tag `fw2_v1011_c_align`：①`btParamsHtml` 里「资金与建仓」组去掉 `cfg.pool==='custom' ? ''` 条件 → ⑧-C 也渲染 3 行可改控件（`btIn_investMode / baseRatio / investPeriods`）；②「标的池与口径」在 ⑧-C 保留组标题、内容换成三条指路行（标的池固定＝自选组合 / 组合级 7 项见下方「组合级参数」/ 逐只 5 项见下方逐只表），不复制控件——`btComboBarHtml` 已占用 `btIn_gridExt|gridFund|tgtAnn|ddBudget|rf|rebal|perFund` 七个 id，重复渲染＝两份同 id、`getElementById` 只认第一个、改一处另一处不跟随（v1002 踩过）；③⑧-C 顶部说明框改写，点明上表承载哪些组、组合级与逐只在哪。
  - **未验证的假设**：⑴「资金与建仓」三行对 custom 生效是我按 `btCfg` 字段白名单 + 引擎读 `cfg.investMode` 推的，**没有实跑一次定投口径的自选回测**去比数字（用户当前自选组合为空，跑不出对照）；⑵⑧-C 与 ⑧-B/⑧-A 的 `investMode` 互不影响（各自存 diff）也未实测双向刷新；⑶三条指路行的措辞（「组合级 7 项」「逐只 5 项」）是否够清楚，只看过窄视口截图。
  - **下一步 + 别碰**：验收 `?t=v1011live` → ⑧-C 应 37 行 6 组、`投入方式` 可改、重复 id 0、下方组合级面板仍在；⑧-B 应 48 行零回归。**别碰**：`btComboBarHtml` 的 id 与「标的池与口径」组的 7 个同名控件**不要同屏并存**（否则串值）；若要真把 7 项搬进参数表，必须先拆 comboBar 并改 `btCuPanelHtml`。
  - **截图**：`D:\Temp\v1011_c_top.png`（本地 ⑧-C 上部资金组）、`v1011_c_pool.png`（本地指路组 + 下方组合级面板）、`v1011_online_c1.png`、`v1011_online_c2.png`（线上同两处）。

- **2026-11-20 · v1010 回测页「修改参数 →」直达 ⑧ 参数页 + 参数表不再折叠改三列表格**
  - **改了什么**：`edit_work/index.html` → v1010（4,893,649 B / 4,170,436 字符，线上 `?t=v1010live` 待验）。三个 tag：①`fw2_v1010_bt_cfg_jump` + `fw2_v1010b_jump_layer`——`btCfgGo(scope)` 一次做全：设 `__btCfgScope` / `__logicBtTab` → dispatch click 切 `[data-st="logic"]` 主 tab → **`logicGo('trace')` 把 ⑧ 层设为当前层**（首版只调 `renderLogicView()`，实测跳过去仍停在层卡列表、`btCfgHost` 不存在，本轮回补）→ 120ms 后 `#btCfgHost.scrollIntoView`；②`fw2_v1010_bt_param_table`——删 `#btParamBtn` 与 `#btDrawer` 的 `display:none`，抽屉改三列表（参数 / 当前取值（可直接改）/ 可选值 · 说明），`table-layout:fixed` + `colgroup` 196/200px + auto + `min-width:780px` + 外层 `overflow-x:auto`，6 分组共 42 行参数，每行「中文名 + 代码」，⑧-C 只隐藏「资金与建仓」「标的池与口径」两组（25 行 / 4 组）；③`fw2_v1010b_sw_text`——勾选类参数 `_c` 改为「勾选框 + 开 / 关」，显隐由 `#btDrawer` 内联 CSS 按 `:checked` 驱动。控件 id 仍是 `btIn_*`，`btCollectDom` / change 监听 / 存取一字未改。
  - **未验证的假设**：⑴⑧ 层原先默认落 ⑧-A（plan），`btCfgGo` 强制写 `__logicBtTab` 为 hold/custom 后是否与用户「上次在这页改到哪」的记忆冲突——未问；⑵42 行参数的分组归类（尤其「季度再平衡 / 按标的分设阈值 / 目标年化 / 回撤预算」放进「标的池与口径」组、⑧-C 会随之隐藏）是我按 v1002 划分推的，用户只说了「以表格展示供选择」，没逐项确认组名单；⑶`min-width:780px` 在 <800px 视口要横向滚动才能读到说明列（截图已确认无重叠，但需滑一下）；⑷跨设备打开的旧 localStorage 参数值（当前这台：V11 狙击 / T7 回撤补仓 / 季度再平衡 / 按标的分设阈值 为开）未与用户核对是否符合他的策略口径。
  - **下一步 + 别碰**：验收 `?t=v1010live` → 持仓回测点「修改参数」应落 ⑧-B（48 行）、自选回测应落 ⑧-C（29 行），两页都**没有「收起参数」**，开关右侧有「开 / 关」文字；改一项后离开再回来值应保留。**别碰**：`btCfgGo` 里必须保留 `logicGo('trace')`——只调 `renderLogicView()` 会退回「停在层卡列表」的老 bug；`btIn_*` 控件 id 与 `btCollectDom` 不要动（⑧-B/⑧-C 的覆盖存档 `fw2_bt_plan_hold|custom` 依赖它）。
  - **截图**：`D:\Temp\v1010_p1.png`（⑧-B 表格左侧）、`v1010_n1.png`（分组与开关文字）、`v1010_n2.png`（横向滚到说明列）、`v1010_n3.png`（V11 狙击 / T7 回撤补仓 开态）、`v1010_c.png`（⑧-C 4 组 29 行）、`v1010_tabs.png`（⑧-C 页签深绿高亮）。

- **2026-11-20 · v1009 数据日更新不再误判「口径不一致」**
  - **改了什么**：`edit_work/index.html` → v1009（4,169,562 B，master `b4ae275bfdd6`，线上 `?t=v1009live` 已验证徽标）。两个 tag：①`fw2_v1009_stale_asof`——`_hit` 后新增 `_asOfOnly`：四段缓存 key「参数指纹｜池｜数据日｜观察窗」里只有数据日不同、且 `cfg.end <= 旧数据日` 时视为命中，直接用旧结果渲染、不弹黄条，并把 key 修正为当前数据日回写 IndexedDB；②`fw2_v1009_stale_brief`——黄条原先把 `btEntWin()`（当前观察窗）硬拼在旧口径行尾，导致两行看起来只差一个数字；现在两行都带「观察窗 X 日 · 数据日 YYYY-MM-DD」（旧值取自旧 key），顶部新增「差在：」逐项清单。
  - **未验证的假设**：⑴`_asOfOnly` 的前提是「新数据只是多出区间之后的日子」；若上游对**历史**净值做过重算（回补/修正），旧 asOf 之前的数值变了而 end 仍 ≤ 旧 asOf，这条会错误复用旧结果——本轮未验证 fund-daily 是否存在历史回补（它的 `meta.asOf` 只是最新日期，没有 revision 标记）。⑵观察窗仍计在 key 里是有意保留：v996 注释写明它只改 `btEntryStats` 统计卡口径、不进 cfg；若从 key 去掉，入场分档卡会沿用旧窗口数字，与池卡现算结果打架。⑶线上只是用这台浏览器现有的旧缓存（asOf 11-16）验证「不弹条」，没有在全新设备上验证冷启动路径（冷启动走空态，与本次改动无关）。
  - **下一步 + 别碰**：验收 `?t=v1009live` → 自选回测应直接出结论条、无黄条；把截止日改到 2026-11-19 再跑应重新计算；改任一参数应重新弹条且写「差在：回测参数不同」。**别碰**：`btOutKey` 的四段结构（去掉任何一段都会让另一处口径失配）；`_asOfOnly` 里的 `String(c.end) <= String(_op[2])` 是字符串日期比较，别改成数值比较。
  - **截图**：`D:\Temp\v1009_no_bar.png`（本地构造旧数据日不弹）、`v1009_stale_bar.png`（构造参数差异后弹条且列差异）、`v1009_online_nobar.png`（线上用户原场景无黄条）。

- **2026-11-18 · v988h 修 tab 行跳动 + ⑧ 层改「回测验证·逻辑准入」**
  - **改了什么**：`edit_work/index.html` → v988h（4,748,831 B，commit `eb83b7aa`，blob `e259dbbc`）。`logicGo()` 删除 `scrollIntoView({block:'start'})`（这是 tab 行跳动的唯一根因）；`LOGIC_LAYERS` 第 8 项改为 `k:'trace'` / `回测验证 · 逻辑准入`；`LOGIC_IDEAS`（I1–I6 投资思想）整体替换为 `LOGIC_BT`（BT1–BT6 准入规则）；引擎位「准入规则」、实测位「方法论」；`logicLoad()` 清理已删条目存档键。
  - **未验证的假设**：⑴BT1–BT6 六条准入口径由我按本项目既有回测实践（三尺度、起点错位、三项门槛、单规则 A/B、证据绑定快照、草稿≠采纳）整理，用户尚未逐条确认；⑵只测了「点层卡不滚动」，未测「用户已在页面底部时点卡片是否需要滚回表头」——目前完全不滚，若层表在下屏之外需手动滑；用户如觉不便可改为「仅当表不可见时滚到表头」（需再确认，别再默认加滚动）。
  - **下一步 + 别碰**：验收 `?t=v988h1`（断言 8 卡、点三张卡 tabsTop 恒定、⑧ 层 BT1–BT6、65/22/24/19）。**别碰**：`logicGo` 里**禁止**再加 `scrollIntoView`（用户明确嫌跳）；⑧ 层若再加条目，只需改 `LOGIC_BT` + `LOGIC_LAYERS[7].ids`，并同步清除不再使用的旧 id 存档键逻辑。

- **2026-11-18 · v988g 投资逻辑加第⑧层（思想总纲）+ 八层单击展示**
  - **改了什么**：`edit_work/index.html` → v988g（4,748,176 B，commit `addcd3ca`，blob `fc75bc99`）。`LOGIC_LAYERS` 增 `idea`（⑧ 投资思想·总纲，`manual:true`）；新增 `LOGIC_IDEAS` 6 条（I1–I6，`人工维护`、不回测、默认生效）；`logicLayerRows/logicAllRows` 统一全集（65 条）；`renderLogicView` 的 B 区改为 8 张层卡导航、C 区只渲染当前层（`fw2_logic_view` 持久化选中层）+ `←/→` 切换。
  - **未验证的假设**：⑴I1–I6 是我按你已表态的立场提炼的**初稿**（不预测只应对 / 杠铃而非中庸 / 目标函数锁定 / 证据先行再升级 / 唯一写入口 / 回撤优先于收益），文案与取舍未经你逐条确认；⑵⑧ 层不参与 `logicToCfg()`（P2 只映射 ①–⑦），它只作「准入约束」，尚未有自动校验（即违规不会被拦）；⑶一次性观察到首屏 ⑧ 卡显示「生效 0」——清空 `fw2_logic_v1`/`fw2_logic_view` 冷启动后**未复现**（显示 6/6），推测与旧档残留/首屏渲染时序有关，未定位到根因。
  - **下一步 + 别碰**：验收 `?t=v988g1`（断言 8 卡、tables=1、⑧ 卡 6/6、A 区 65/22/24/19、刷新停原层）；P2 写 `logicToCfg()` 时**不要**把 ⑧ 层映射成 cfg 键（它没有引擎分支）。**别碰**：`LOGIC_IDEAS` 是 ⑧ 层唯一内容源，改文案改这里、别改注册表；`fw2_logic_view` 只存「当前看哪层」，与三态存档 `fw2_logic_v1` 是两件事，别合并。

- **2026-11-18 · v988f 策略执行新增「投资逻辑」子模块（页面 · 大脑控制面）**
  - **改了什么**：`edit_work/index.html` → v988f（4,743,005 B，commit `68a0e242`，blob `7831a8c4`）。`#stratTabs` 首位新增 `data-st="logic"`（默认 active）+ `#stp-logic` 面板；插入 LOGIC 模块（七层 59 条映射、三态存档 `fw2_logic_v1`、四区渲染：核心思想条 / 决策流水线 / 七层矩阵 / 版本证据）；`renderStrategyView()` 调 `renderLogicView()`。表格为主行 5 列 + 明细行（口径 / 动作）。
  - **未验证的假设**：⑴三态基线是「按注册表 def + modeled 文本推断」的现状镜像（16/24/19），不是引擎运行时真值——例如 T1 阶梯止盈显示「生效」但引擎标注「未接线」，已加橙色警示，仍未逐条与引擎分支对齐（P2 一致性闸门才做）；⑵七层归类里 `T8/T15/W3/S4` 归④买入节奏、`S3/S6` 归⑥观察，是我按「动作方向」定的，用户尚未逐条过目；⑶「投资逻辑」设为默认 landing 未经用户明确同意（他只要了 tab 名与副标题）。
  - **下一步 + 别碰**：验收 `?t=v988f1`（断言 tables=7 / tbody=118 / summary=16/24/19 / 徽标 v988f）；P2 先写 `logicToCfg()` 再改抽屉（顺序反了会出现两处真相源）。**别碰**：`fw2_logic_v1` 只存三态、**不要**在 P2 之前让其它模块读它（现在读它＝假的「已生效」）；`SIGNAL_REGISTRY` 原字段（`def/modeled/thr/act`）是唯一内容源，投资逻辑页只读不改写。

- **2026-11-18 · v988e 持仓表新增「卖后涨跌」列（页面）**
  - **改了什么**：`edit_work/index.html` → v988e（4,726,933 B，commit `8d8ef37a`，blob `ef7c7349`）。列位在「最大回撤」后；新增 `window.__LASTSELL_ALL__`（`last-sell.json` 的 sells+history 合并，swap 时不改 `__LASTSELL__`）；表头 16→17，组头行/合计行/空态 colspan 同步。
  - **未验证的假设**：⑴`history` 里的卖出是「该标的上一轮清仓」，若期间又买入，本列仍按卖出后至今的净值比——口径已写进 title，但未与用户确认这是否他想要的「卖早/卖对」口径；⑵卖出确认净值 `nav` 与页面 `price` 都取单位净值，分红再投型基金存在口径差（未用累计净值序列）。
  - **下一步 + 别碰**：要看某只明细 → 直接对 `data/last-sell.json` 的 `sells/history`；要把「卖后涨跌」并进信号页/复盘 → 需另开一版。**别碰**：`__LASTSELL__`（T16 的 90 天窗口口径，改了会误触发「卖出后破位减半」）；`last-sell.json` 只在 `gen_last_sell.py` 生成。另：曾记「用户截图 012920 最大回撤 −6.51% 与全序列 −42.4% 不一致」——**2026-11-18 21:5x 复查推翻此记录**：把原截图（3786×1947）该格裁切放大后读到的是 **−42.37%（谷底 2026-11-06）**、买入峰值 **+115.13%（2026-06-22）**，与线上 v988e 实测逐位相同，−6.51% 系读错。核验链：线上主世界探针 `__NAV_SERIES__['012920']`＝1134 点（2022-01-11→2026-11-13，max 5.3763/2026-06-22）；本地 `nav-hold.json`（meta.genAt 2026-11-17T21:39:53，23 只/33,237 点）同为完整序列；两者都含 6-22 高点，故首屏迷你序列与全量两条 loader 路径口径一致、无截断。数值：3.0986/5.3763−1＝−42.37%（线上序列末点 11-13）；本地序列到 11-16（nav 3.0941）→−42.45%，差的 0.08pp 仅来自净值日差 1 天。**无需再追，既有列无 bug。**

- **2026-11-18 · v988d T13 口径收敛（备用金摘出）+ 锚点窗（页面+文档）**
  - **改了什么**：`edit_work/index.html` → v988d（4,724,030 B，commit `5395c345`，blob `986e6c94`）；T13 行只留纯网格口径 + 短/长窗限定；脚注加锚点复核与池深度说明；`docs/SIGNAL_INVENTORY.md` 加 14.21.5。
  - **未验证的假设**：⑴两个锚点窗各只有 1 窗，只作方向性复核，未作显著性；⑵「池内最晚标的 160422 起 2018-11-16」取自 fund-daily.json 首个净值日，未与基金成立日交叉核对；⑶早期窗口里无数据标的的权重如何处理（转现金还是重分配）未从引擎源码确认。
  - **下一步 + 别碰**：复算锚点 → 起 8765、`?t=xxx`、设 `btIn_gridExt/gridFund/gridOn` 后改起止日；数据在 `D:\Temp\_t13_anchor.json`。**别碰**：`gridOn` 默认值、`gridExt` 默认值；14.21.4 的 12+8 窗数字（已发布，勿回改）。

- **2026-11-18 · v988c T13 三尺度验证 + 档位升开 + 备用金降级（页面与数据）**
  - **改了什么**：`edit_work/index.html` → v988c（4,723,627 B，commit `b2c18a13`，blob `a20082ad`），含 v988b（4,722,971 B，`1e01bc9a`/`76603ab4`）。①总表 T13 网格跟踪 行档位 `可选`→`开`（#B45309→#0F766E）、实测列改三尺度三段；②抽屉 `gridExt` 选项与上限 label 标「降级」、R3 备注标「降级·实测 −0.20，上限 0＝不限」；③补跑 60 窗（5Y 12 + 10Y 8 × 基线/B/A），页面 T13 行/脚注/R3 滚动格改三尺度；④`docs/SIGNAL_INVENTORY.md` 新增 14.21.4（窗口集、三组结果表、四条结论、落盘路径）。
  - **未验证的假设**：⑴5 年 12 窗 / 10 年 8 窗的窗口高度重叠，只作方向性证据，未做显著性检验；⑵10 年窗起点只到 2016-06（再往后容纳不下 10 年），未来若补 2010–2014 起点需确认标的池在该期是否齐全；⑶B 组「纯现金缓冲」在 5/10 年是预算外 ¥6,200，与 3 年同额，未验证「不限额」口径的效果。
  - **下一步 + 别碰**：要复算 → 起 `python -m http.server 8765 --bind 127.0.0.1`（工作目录 `edit_work`），打开 `?t=xxx`，进「策略执行 → 持仓回测」，改 `btIn_start/end` 自动重跑；结果读 `#btOut` 内首列为「合计」的 tr 的 td[11]/[14]/[16]/[20]。统计用 `D:\Temp\_t13_5y10y_split.py`（读 `_t13_5y10y_ab.json`）。**别碰**：`gridOn` 默认值（用户明确保持开）；`gridExt` 默认值（保持不启用）；历史条目旧写法。

- **2026-11-18 · v988a 规则代码全站带中文名（页面文案补 20 处）**
  - **改了什么**：`edit_work/index.html` → v988a（4,722,670 B，commit `9de00cb2`，blob `2ed05195`）。用户指出规则卡虽已是「代码+中文名」，但页面其它文案仍写裸代码（尤其 T13）。逐处补齐：`T7 补仓→T7 回撤补仓`（抽屉 V1 勾选标签 / S-TREND 与 V1 说明列 / 页脚注共 6 处）、`T10 四档 5pp 再平衡→T10 杠铃再平衡·四档 5pp`、`T10 杠铃失衡→T10 杠铃再平衡（失衡）`（6 处）、`R9 互斥/R9 优先→R9 峰值刹车`、`R8→R8 年线信号`、`R4/R5→R4 止盈①/R5 止盈②`、`R2→R2 定投`、`T13 已用…→T13 网格跟踪 已用…`、`T5 为标的层→T5 时间止损 为标的层`；「明细见 14.18/14.20」补成 /14.21。另在 `AGENTS.md` 加「强制规则 8」，把这个约定写成规则而不是一次性修补。
  - **未验证的假设**：⑴ 逐行扫描只覆盖「策略执行 → 持仓回测」页（含抽屉），其它 tab（我的持仓/资金平衡/交易信号/基金数据/宏观/数据管理）未逐页扫，可能有同类裸代码残留；⑵ 两行配对（代码一行、中文名下一行）判定为合规，是按视觉合理性判断，非用户明确口径。
  - **下一步 + 别碰**：要复扫其它 tab 就照本轮办法——展开面板后用 `innerText` 逐行跑「代码同行是否带中文名」，命中且下一行不是中文名的才改。**别碰**：历史版本条目里的旧写法（属当时记录，不回溯改写）；`_idCn` 映射键名与规则卡两行结构。

- **2026-11-18 · v988 网格总开关 + T13 网格跟踪 三成分分离 + 规则卡中文名**
  - **改了什么**：`edit_work/index.html` → v988（4,722,355 B，commit `5c41226e`，blob `19067c2d`，线上 `caifu/index.html`）。①新增 `gridOn` 网格买入总开关（4 处：`btCfg` 默认 `gridOn:true`、收参 `c.gridOn`、引擎 `cfg.gridOn !== false &&`、运行条 `#btIn_gridOn` 勾选行「网格买入（T13 网格跟踪 · 总开关）」）；②规则卡 `_idCn` 中文名映射，左列改成「代码 + 中文名」两行、列宽 60→76px、表头「代码／中文名」；③R3 红字滚动格 / 总表 T13 网格跟踪 行（默认列 `—`→`随R3`）/ 总表脚注三处改为「三组已分离」；④`docs/SIGNAL_INVENTORY.md` 新增 14.21（14.20 混杂段补指向）；README ver v988 + `next`/三节/待决/下一步同步。
  - **未验证的假设**：⑴ 两成分「近可加」（−0.20+0.18≈−0.02、+0.25+0.52≈+0.77pp）只是 24 窗均值上的验算，没有逐窗做分解校验；⑵ 年化 Δ ±0.18 的显著性判断（t≈1.4）是按区间粗估，未做正式检验；⑶ 24 窗高度重叠，不是独立样本；⑷ 网格「摊低成本→年化微升」的机制解释属推测，未实证；⑸ 只测了 `BT_PF` 内置步长（宽基 3%/进攻 5%/债 1.5%），其他步长未测。
  - **下一步 + 别碰**：强刷 `?t=v988live1` 走「策略执行 → 持仓回测」核五点（徽标 v988、运行条网格开关已勾选、表头「代码／中文名」两行、R3 滚动格三段数、基线 13.67/−5.91/2.04/103）。要复跑三组：基线＝重置为标准口径直接跑；B＝备用金勾「预算外」+ 上限 6200 + 取消「网格买入」；A＝B 再勾回网格——改起止日会自动重跑，不必 reload。数据在 `D:\Temp\_t13_on.json`（A）与 `_t13_b.json`（B），统计脚本 `_t13_split.py`。**别碰**：`btRun` 主体、`_navToday()`、`BT_PF` 内置逐只 gs/sl/band；`gridOn` 不要放进抽屉 `comboBar`（只在 `pool='custom'` 分支渲染，杠铃池看不见）；`BT_DEFAULTS` 捕获位置不能挪到 localStorage 合并之后。

- **2026-11-18 · v987a 纪律实测总表 + T13/T5 体检**
  - **改了什么**：`edit_work/index.html` → v987a（4,720,045 B，commit `717f6261`，线上 `caifu/index.html`）。①规则卡容器内新增「纪律实测总表」11 行 × 4 列（信号/默认/实测/档位，五档配色：开绿·实验橙·可选橙·关红·只复核灰）；②`滚动` 从 `seg` 内挪成独立格（`grid-column:2/3` 红字），支持顶层 `g.roll` 与 `R3→T13` 映射——R3 网格行因此显示 T13 的 24 窗结论；③`docs/SIGNAL_INVENTORY.md` 新增 14.19（总表 + 五条判断原则）/ 14.20（T13 逐窗 Δ 与混杂说明、T5 样本统计）；④README frontmatter 与三节、待决同步。
  - **未验证的假设**：⑴ T13 的 24 窗边际（Δ年化 −0.02 / Δ回撤 +0.77pp）同时含「备用金现金缓冲」与「网格买入」两成分，未分离——对照组 C 与 B 组逐位相同已证明 `cfg.pf` 在杠铃池无效，但纯网格效应本轮拿不到；⑵ T5 样本按每 20 交易日取样、样本高度重叠，只作方向性证据，未做显著性检验；⑶ 总表档位（T13 归「可选」、W3/S4 归「实验」）是按数值自行归纳，未经用户逐条拍板。
  - **下一步 + 别碰**：先强刷 `?t=v987live` 走「策略执行 → 持仓回测 → 运行」，核徽标 `v987a`、R3 滚动格、总表 11 行四列与脚注；再点「重置为标准口径」确认回到 13.67/−5.91/2.04/103。若要做 T13 纯效应，需新增网格总开关或 `pool='custom'` 复刻杠铃权重——会动引擎口径，先拍板再动手。**别碰**：`btRun` 主体、`_navToday()`、`BT_PF` 内置逐只 gs/sl/band（改它会同时改三个口径）。

- **2026-11-18 · v986 S-TREND 24 窗滚动定论**
  - **改了什么**：`edit_work/index.html`（v986）规则卡 seg 增通用 `roll` 渲染位 + S-TREND 补 24 窗结论；`docs/SIGNAL_INVENTORY.md` 14.18（24 窗完整表 + 五条结论）；README ver v986 与三节同步。
  - **未验证的假设**：无。ST 关 24 窗与 14.12 表1 C0 逐位一致（24/24），口径可核。
  - **下一步 + 别碰**：别把 S-TREND 改默认开——24 窗均值 −0.18、胜 5/24，连熊段（熊B −1.19、熊转牛 −1.73）都是负的。要复跑：先点「重置为标准口径」，再切 1/6/9 月各 8 窗，两组只差 `stGate`。原始结果在 `D:\Temp\_st_off_jan.json` / `_st_on.json`。

- **2026-11-18 · v985 口径预设 3/5/10 年发布**
  - **改了什么**：`edit_work/index.html`（v985）新增 `BT_WIN` + `btWinBtn` + `#btWinRow` 三颗胶囊；`rsBtn` 处理器抽成 `applyStd(win)`，切窗与重置同一入口；`docs/SIGNAL_INVENTORY.md` 14.17（三档起止日 + 双环境验收表 + 已知局限）、`docs/PITFALLS.md` 追加 v985 一句、README 三节与 ver 同步。
  - **未验证的假设**：无。三档在本地与线上都跑过，与表2 基线逐位一致。
  - **下一步 + 别碰**：别把 5 年起点「顺手对齐」成 2021-07-03、10 年起点改成 2016-07-03——历史基线是 2021-07-05 / 2016-01-04，改了数字就对不上表2。10 年窗页面自带「滚动拼接样本」提示，引用 5.33% 时必须一起引。

- **2026-11-18 · v984 一键「重置为标准口径」发布**
  - **改了什么**：`edit_work/index.html`（v984）新增 `BT_DEFAULTS` 出厂默认快照 + 运行条 `#btResetStd` 按钮（还原默认→叠加标准覆盖→存盘→重渲染→自动重跑）；`docs/SIGNAL_INVENTORY.md` 14.16、`docs/PITFALLS.md` 口径漂移条目的机制层修法、README 三节与 ver 同步。
  - **未验证的假设**：无。按钮行为在本地与线上各做过一轮「污染→点重置」实测，结果回 13.67/−5.91/2.04/103。
  - **下一步 + 别碰**：引用任何回测绝对值前先点「重置为标准口径」再跑；别把 `BT_DEFAULTS` 的捕获位置移到 localStorage 合并之后（那样快照就带残留了）。`pool`/`customCodes` 是刻意保留的，不要顺手一起清掉。

- **2026-11-18 · C0 口径漂移结案（无页面改动）**
  - **改了什么**：`docs/SIGNAL_INVENTORY.md` 新增 14.15（三条证据 + 8 组候选参数复现失败）；`docs/PITFALLS.md` 新增「跨会话数字对不上」症状→证伪→根因→修法；README `next`/当前进度同步（ver 仍 v983，页面未改）。
  - **未验证的假设**：v976 那次记录究竟残留了哪个参数仍未确定（8 组候选都不匹配 10.35/−4.82）；不影响结论方向，但若有人要考古需继续试 止盈/止损/网格常数 与旧数据快照。
  - **下一步 + 别碰**：后续任何跑批必须显式写全 20 个 cfg 字段；跨会话引用绝对值前先同会话重测。别碰 `_v976_probe.html` 这类临时文件（已删）；本地复跑用 `python -m http.server 8765`（用完停进程）。

- **2026-11-18 · v983 五年尺度起点错位：保险线定稿收口**
  - **改了什么**：`docs/SIGNAL_INVENTORY.md` 新增 14.14（5 年 6/9 月起点各 6 窗全表 + 18 窗合并）；`edit_work/index.html` 规则卡 W3 行补 5 年结论、徽标 v983；README `next`/当前进度/ver 同步。
  - **未验证的假设**：①5 年 9 月末窗 2021-09→2026-07 仅 4.8 年；②仍未测分批（定投）与网格口径下的滚动；③回测引擎对 2019 上半年池内仅 5 只标的给出「滚动拼接样本」提示，跨段可比性未逐段核。
  - **下一步 + 别碰**：保险线定稿，后续若要再验只能换口径（分批/网格，或加入止盈参数交互）；否则优先处理 v978 遗留的 C0 口径漂移（今日与 v976 差 0.1–0.8pct）。别碰 `_bearNow()`、`_slowBuild()`、`btIn_bearBuildGate` 默认值（都是 false，勿改）。跑法：抽屉设 start/end → 点运行，5 年窗约 30 秒，单次调用别超过 6 窗否则 COMMAND_TIMEOUT。

- **2026-11-18 · v982 起点错位复核：期望 0.00 不是起点挑出来的**
  - **改了什么**：`docs/SIGNAL_INVENTORY.md` 新增 14.13（6 月/9 月起点各 8 窗全表 + 24 窗合并统计）；`edit_work/index.html` 规则卡 W3 行补起点错位结论、徽标 v982（commit `9f5a09f5`，4,708,726 B）；README `next`/当前进度/ver 同步。
  - **未验证的假设**：①9 月末窗 2023-09→2026-07 只有 2.8 年（截断），与整 3 年窗不同质，已单独标注但未排除；②未测 5 年尺度下的 6/9 月起点（本轮只做 3 年滚动）；③未做分批/网格口径。
  - **下一步 + 别碰**：保险线到此收口，若还要继续只能换口径（5 年 6/9 月起点、或分批与网格）；否则转 v978 遗留的 C0 口径漂移（今日与 v976 记录差 0.1–0.8pct）。别碰 `_bearNow()` 与 `btIn_bearBuildGate` 的默认值；跑法：抽屉设 start/end → 点运行，免 reload，单窗约 5 秒；结果可写 `fw2_roll_off`。

- **2026-11-18 · v981（文档层）滚动窗口复核：熊市保险期望为零/五年全负**
  - **改了什么**：`docs/SIGNAL_INVENTORY.md` 新增 14.12（3 年 8 窗、5 年 6 窗三组全表 + 统计）；README `next`/当前进度/下一步同步；页面无需改代码（本轮结论为「不开」）。
  - **未验证的假设**：①窗口起点固定为每年 1 月 3 日，未做起点错位（如 7 月）的稳健性；②只用 62,000 预算 + 一次性口径，未测分批/网格口径下滚动结果；③数据起点 2016-01，早于此的周期不可见。
  - **下一步 + 别碰**：下一步＝若还要动保险，只能换「起点错位 + 分批口径」再验一轮；否则转回 v978 遗留的 C0 口径漂移（与 v976 记录差 0.1–0.8pct）。别碰 `btRun` 与 `_navToday()`；滚动跑法：抽屉里设 start/end 后直接点运行，无需 reload（单窗约 4 秒）。

- **2026-11-18 · v980（建仓侧熊市保险：bearSlowB / bearBuildGate）——软减速仍无效，硬拦 10 年反噬**
  - **改了什么**：`edit_work/index.html` → v980（4,708,053 B，commit `c49e5bce`）。新增 `_bearNow()` 公共熊市判定、`_slowBuild()`（建仓侧按 50% 投）、`bearBuildGate`（熊市首笔挂起、转牛再建，复用 `buildPend`）；抽屉新增两行开关；`docs/SIGNAL_INVENTORY.md` 加 14.11；README 三节同步。
  - **未验证的假设**：①熊A 的 +0.42/+0.81 只来自单段单次首笔建仓，样本不足；②5 年 +1.37 与 10 年 −1.32 对冲，方向未定；③`bearSlowPct` 25/75 未测（按结论预期无效）。
  - **下一步 + 别碰**：下一步＝不再给熊市保险单开开关，改做滚动窗口验证；或回到 v978 遗留的口径漂移（C0 与 v976 记录差 0.1–0.8pct）。别碰 `btRun` 主体与 `_navToday()`；跑分段先把 cfg 写进 `fw2_bt_cfg_v1` 再 reload。

# 交接收件箱（INBOX）

> 目的：**换 AI 不丢线索**。任何一个 AI（豆包 / Cursor / Claude Code / 其他）在本目录收尾时，
> 在下面「待接手」区追加一条 5 行记录；下一个接手的 AI 开工时先读这里，再读 README。
> 规则：只写「下一步要做什么 + 怎么验证」，不写过程流水账；超过 30 天的条目可以删（历史在 README 的版本段里）。

## 模板（复制这段，替换方括号）

```
### [日期] · [一句话主题] · [状态：待接手 / 进行中 / 已交接]
- 改了什么：[1–2 句，带上文件与 tag]
- 新增资产：[新脚本 / 新数据源 / 新字段；没有写「无」]
- 未验证的假设：[我推断但没实证的东西，明确标「待核实」；没有写「无」]
- 下一步：[具体命令或动作 + 期望结果]
- 别碰：[正在被人改 / 有已知问题但暂不修的地方]
```

- **2026-11-18 · v977（W3/S4 条件化纪律）**
  - **改了什么**：`edit_work/index.html` → v977（4,701,622 B，commit `d2f9ca48`）。新增 cfg `trendBearOnly`（默认关）/`trendBearMode`(ma200|ma60|own|dead)/`trendBearScope`(all|addon)；`_regBear` 熊市判定表在 MA 表之后生成；`_gateOK(_s,_d,_nav,_isAddon)` 增加第 4 参；抽屉 W3/S4 下方加「仅熊市生效」勾选＋判据/范围下拉；规则卡 W3/S4 行写入 v977 实测结论；`docs/SIGNAL_INVENTORY.md` 新增 14.9；README 三节与 ver 更新。
  - **未验证的假设**：①「四判据数字相同」解释为「补仓发生在跌破均线日 ⇒ 判据在决策日恒真」，这是从结果反推的机制解释，未逐笔核对每笔被拦的买入当天 MA 状态；②`own` 档（逐标的破年线）只做过零星运行、未跑满六段；③熊A/熊B/牛B/熊转牛在 scope=addon 下的四格未补测，矩阵只做了牛A 与熊尾 + 一个牛市小窗。
  - **下一步 + 别碰**：下一步可跑「熊市减速」（跌破年线期间网格/T7 补仓金额 ×50%，不是停手）做 A/B，命令＝线上页抽屉改参数跑六段；别碰 `btRun` 引擎主体与 `_navToday()`；跑分段前先把 cfg 写进 `fw2_bt_cfg_v1` 再 **reload**，否则抽屉重渲染会把下拉值冲回 cfg 默认（本轮因此先得到「换判据数字不变」的假结论）。

## v1075 · T1 阶梯止盈接回引擎

- **改了什么**：`edit_work/index.html`（tag v1075 / 注释块 `fw2_v1075_t1_tp`）：`btPF` 四分支改走 `_tpPair(cfg)`；`cfg.tpOn` 由 T1 三态驱动；第二档加「隔 ≥2 个交易日」（`dIdx`）；`LOGIC_CFG_MAP` 增 T1→tpOn；T1/R4/R5 文案与组合层计数同步。
- **未验证的假设**：①「隔 2 个交易日」是我为修 v903 连砍缺陷加的护栏，强度未经分段实测（原缺陷是 +25%/+40% 档位下相邻两日，10/20 档位是否仍会连触发未单独统计）；②实测只跑了一个 3 年窗（纯牛市段），熊市段 T1 是否真的降回撤未测；③本地 `配置回测` 在本机浏览器只出快照、点「运行回测」不重算（线上正常），本地数值验证改在线上做。
- **下一步 + 别碰**：要复核就强刷线上 → 策略执行 → 配置回测 → 运行回测，看「差异归因」是否出现「止盈减仓×2」；别碰 `_tpPair` 之外的 `btPF` 分支语义（自选池逐只参数 `u0` 与 `perFund=false` 两条是别用途）。

## 待接手

### 2026-11-26 · 「逐个做」交接第七节 5 项取证（只读，未改工程/未发布）

- **改了什么**：无工程改动（index.html 仍 v1123 / 5,369,050 B）。用户「逐个做」后逐项取证，保留配方 `edit_work/_calc_v11_seg_v1124.py`，临时探查脚本已清。
- **①V11 seg 重算（候选取到，未替换）**：旧数字在 `index.html` L4384 注册表 `V11.seg` / L22544 `LOGIC_WHERE.V11` / L22612 投资逻辑清单三处，已标「旧口径失效」。用现役 1260 统一公式 + node 直跑 `btRun`（★v1018 起是 `function*`，须 `it.next()` 驱动到 done；★须注入 `screen-pool.json` 作 `window.SCREEN_POOL`，否则 `_SNP.list` 空→零交易）重跑六段开vs关边际，候选 Δ年化：牛A +1.74 / 熊A −0.80 / 熊B −0.39 / 牛B +2.13 / 熊转牛 −0.27 / 熊尾 +0.51 pct。**两处未决故未替换**：a) 注入 SCREEN_POOL 才出交易＝第④项症结，页面实际零交易，此值是「筛选池就绪」口径；b) 基线区间 2023-07-03→26-07-03 关侧复现 10.69%/−4.35%/CalmarS 2.09 vs v1122 README 记 13.04%/−5.65%/2.03 未精确对齐（差异或来自当时 localStorage 参数污染/数据版本）。
- **②5万全投**：运行回测默认 `capital:2500/perBet:625/maxN:4`（L17430），「狙击池本金」本就可手填 50000＝全投。所谓「另开口径」＝改默认值或加预设，属口径选择。
- **③历史快照门限**：`data/v11-signal-hist.json` hist=21，前 20 条（10-19→11-23）`odds_thr=2.0`、仅第 21 条（11-25）=2.5。重算需逐日重放 K 线或长期标旧。
- **④SCREEN_POOL 时序**：`_SNP.list` 仅从 `window.SCREEN_POOL.funds` 填（L25178），未就绪即空→配置回测 V11 零交易（v1122「V11 未产生交易」根因）。注入后 40 只筛池、28 只有 >1260 点净值，每段 36–72 笔成交。修复需单独设计。
- **⑤跨域 200 条**：沿用 v1123 验收分类，全为 `web.ifzq.gtimg.cn` / `api.fund.eastmoney.com` CORS/资源失败，JS 异常 0、业务 console.error 0，属数据源网络策略非代码 bug。
- **未验证的假设**：候选 seg 未做「旧口径 vs 新口径」同数据基线对拍；注入 SCREEN_POOL 的口径是否被认可为注册表现役口径待用户定。
- **下一步 + 别碰**：5 项全部待拍板后才动（①是否用候选替换 seg + 如何处理基线差异；②是否改默认/加 5 万预设；③重算或标旧；④加载时序修复设计；⑤是否换代理/同源转发）。别碰 V11 统一 1260 日口径、`#sigFootNote` / `#view-smartmoney` 锚点、btRun 引擎主体。

### 2026-11-26 · v1123 交接验收（只读，未改工程/未发布）

- **改了什么**：无工程改动。按 `docs/HANDOFF_v1123.md` 开场要求走开工三步（README 顶部 / DATA_LEDGER 相关条 / `handoff_check.py`），新增只读探针 `edit_work/_probe_handoff_v1123.py`，连**线上页**真渲染验收四项。结果 `HANDOFF_V1123_VERIFY=PASS`：①徽标 v1123；②`#sigBody` 12 子节点、`#view-smartmoney` idx=10、`prev=sigThroughPane` / `next=sigFootNote`；③两张表 17 行（9+8）；④JS 异常 0 / 业务 console.error 0。切「趋势策略」sm display=none、切回 block 也对。交接自称与实测一致，v1123 可结案。
- **未验证的假设**：①日志里 200 条 CORS / `Failed to load resource`（`web.ifzq.gtimg.cn`、`api.fund.eastmoney.com` 等跨域 K 线/净值请求）是数据源跨域策略，与 v1123 锚点改动无关，按「非 JS 报错」排除；若把这些也算「控制台报错」则数字为 200。②宽屏 CDP 截图文字不落墨未用第二浏览器复核（交接已注明，本轮按交接指示用 DOM 断言未截图）。
- **下一步 + 别碰**：交接第七节 7 项待拍板，优先 3（V11 旧 3×ATR14 收益结论按 1260 日统一公式重算，另开一版）/ 4（是否另开 5 万全投口径）/ 5（前 20 快照旧门限 2.00 是否重算）；用户确认前不动代码、不重跑数据链。别碰 `#sigFootNote` / `#view-smartmoney` 唯一锚点、`v-tabs` 与 `sigLvlBar` 在内容前的位置、V11 统一 1260 日口径。

### 2026-11-23 · 卡玛/回撤长窗口重算（只读分析，未改工程/未发布）

- **改了什么**：无工程改动。新增配方 `edit_work/_calc_barbell_long.py`、`_calc_barbell_short_fixed.py`、`_out_long_curve.json`。**发现并修正上一轮 `_calc_barbell_dd.py` 的权重公式 bug**：`scale_other` 非进攻档多除 `100/65`，权重和 0.7725，归一化后「标称 35%」实跑 45.3% → 上一轮全部短窗口数字作废。新脚本加权重守恒硬断言。
- **关键结论**：长窗口 2014-06→2026-11（12.41y，指数代理）进攻35% → 年化 **8.88%** / MDD **−26.74%** / 卡玛 **0.33**，MDD 定型于 2015 股灾；进攻↑卡玛单调升(0.20→0.49)。修正后短窗口 2.77y 进攻35% → 13.37% / −14.44% / 0.93，进攻↑卡玛单调降(1.06→0.78)。**两窗口结论系统性相反**，根因是进攻端 3/4 为海外资产，2015 股灾 A 股腰斩而海外小跌，提高进攻端实为降 A 股敞口。
- **未验证的假设**：代理偏差未量化（价格指数不含股息、汇率未计、012920 用 SPX 粗代、511010 久期≠10年）；静态日再平衡无申赎费/定投现金流；未做显著性检验；跨市场年化必须用日历天数（用 N/252 高估 12.1%）。
- **下一步 + 别碰**：若要把长窗口口径固化进工作台，须先拍板代理映射与现金假设——属数据口径变更。别碰：`index.html` 的 `SIGNALS_CFG.barbell`（现役 11 只 40/35/10/15），用户记忆仍是「8 只 34.5/18/47.5」，分叉未拍板。

### 2026-11-23 卡玛问答 + 进攻端占比回撤曲线（只读分析，未改工程/未发布）
- **改了什么**：无工程改动。新增只读配方 `edit_work/_calc_barbell_dd.py` / `_calc_barbell_dd2.py`，写当日记忆 `.workbuddy/memory/2026-11-23.md`。
- **未验证的假设**：静态日再平衡、无现金流/申赎费，不等同实盘；QDII 净值滞后未量化；卡玛差异未做显著性检验。
- **下一步 + 别碰**：★口径分叉未拍板——用户记忆「8 只 34.5/18/47.5」vs 现役 `SIGNALS_CFG.barbell`「11 只 40/35/10/15」、纲领回撤 ≤20% vs 记忆 25–35%；动配置前先问以哪套为准。★四口径 MDD 全落在 2026-03/06→11（正在发生的下跌），右端截断低估真实回撤，别拿「MDD 只有 10–12%」当最坏情况。曲线结论随窗口反转（2.63y 卡玛峰值在进攻 20%，4.81y 单调下降），不要单口径定论。别碰 index.html / 数据文件。

- **改了什么**：`edit_work/index.html` v1055 / tag `fw2_v1055_bt_meaning_parity` —— 只改 `LOGIC_MEAN` 的 `BT1`–`BT6` 六条「信号含义」，改成与 ①–⑦ 同构的四段式（管什么 → 阈值事实 → 通过/不通过怎么做 → 边界）；徽标 v1054→v1055。另因发布硬卡，跑 `gen_last_sell.py` 刷新了 `data/last-sell.json`（`updatedAt` 11-19→11-22，sells 仍 1 只 `012920`）。
- **未验证的假设**：①BT1「反向窗超过 1/3 就退回观察」、BT2「6 月 / 9 月起点各 12 窗」等数字照 `LOGIC_BT.act/thr` 原文，未重跑一遍准入流程验证这些分支真的按此执行；②BT4「k≥3 档通过」写的是判据，实际买点类规则当前有没有一条达标未核对；③「本身不出任何回测数字」依据是 `LOGIC_BT` 的 `modeled='准入规则（无引擎分支）'` 与渲染代码，不是跑出来的。
- **下一步 + 别碰**：强刷 `?t=v1055live` → 策略执行 → 投资逻辑 → ⑧ → 准入规则与证据，看六条第 2 列是否是同构叙述。跑 `python check_js.py`（21 块 ALL OK）、`check_html_comments.py`（281 处 0 隐患）、`check_globals.py`（243 键 PASS）、`python _audit_last_sell_link.py`（WARN=0 FAIL=0）。**别碰**：`LOGIC_MEAN` 的其余 59 条（用户只要求 ⑧ 层同层）、`LOGIC_WHERE` 65 条、5 列结构；BT3 的 Calmar 线是 0.42（不是 0.5），BT4 是 BH-FDR α=0.05（Bonferroni 已停用）；`data/last-sell.json` 只由 `gen_last_sell.py` 生成，别手改 `updatedAt`。

- **改了什么**：`edit_work/index.html` v1054 / tag `fw2_v1054_logic_meaning` —— 投资逻辑 ①–⑧ 表在「代码 / 中文名」后新增「信号含义」列（`LOGIC_MEAN` 65 条），「生效作用」列末行加蓝色小字「生效信号显示位置」（`LOGIC_WHERE` 65 条）；普通层 9→10 列（min-width 1890、实测 1908px），⑧ 层 4→5 列（1400px），⑧ 层蓝字写在含义格内。README 三节 + frontmatter（ver v1054）同步，`docs/FRONTEND.md` 新增 §8g。
- **未验证的假设**：①每条含义的实测数字（如 T13 的 Δ年化 +0.18、W3 的 −5.05/−6.97/+17.31）抄自 `SIGNAL_REGISTRY` 的 `act`/`seg` 字段，**没有逐条重跑回测复核**；②`M1`–`M6` 的显示位置写「市场信号表（快照/日K 就绪时才出）」——本轮线上与本地实测该 6 行**都未出现**，判断依据是代码条件（`px('000300')` / `ks`），并非观察到它们渲染；③`R1`–`R11` 的「规则卡」位置按 v1012 记录与 `btRuleRows` 数组推断，未逐个点开核对卡内文案；④「W 系不逐行」是当前渲染事实（`watchRows` 仅进计数与自选雷达），若未来把自选信号并入表格，`LOGIC_WHERE` 的 W 条目需同步改。
- **下一步 + 别碰**：强刷 `?t=v1054live` → 策略执行 → 投资逻辑：①–⑦ 每层第 2 列应为「信号含义」、生效作用格末行应为蓝字；⑧ 层展开「准入规则与证据」应为 5 列。跑 `python check_js.py`（21 块 ALL OK）、`check_html_comments.py`（280 处 0 隐患）、`check_globals.py`（243 键 PASS）、`verify_manifest.py`（37/36 PASS + `sec_daily` 1 告警）。**别碰**：`LOGIC_MEAN`/`LOGIC_WHERE` 别接成 cfg 或判定；阈值文案唯一真源仍是 `SIGNAL_REGISTRY`（S1/W1/T8 是 30%，20/50 三档只属 S7/T15/W9）；别把 `watchRows` 塞进持仓信号表；别为对齐给 ⑧ 层硬加第 6 列。

- **改了什么**：`edit_work/index.html` v1051 / tag `fw2_v1051_logic_cfg` —— 投资逻辑 ①–⑦ 三态接入回测参数（`LOGIC_CFG_MAP` 16 条→13 个 cfg 键、`logicCfgOverlay` 只改运算副本不写存档、总开关 `fw2_logic_cfg_on` 默认开、回测页参数来源条 + ⑧ 参数页只读条 + ④ 层表下开关行与接线清单）。README 三节 + frontmatter（ver v1051）同步。
- **未验证的假设**：①共用键（gridOn / trendGate）「任一条生效即开」的口径是按 v1050 映射表推断，未逐条跑回测验证；②只实测 S4 趋势确认→trendGate 一条路径（其余 14 条共用同一 overlay 代码，但各自 cfg 键在引擎里的消费点未逐个复核）；③自选回测（custom 池）不读这 13 个键，本轮刻意未接；④「默认开」属口径选择，待用户确认（见 README 待决）。
- **下一步 + 别碰**：强刷 `?t=v1051live` → ④ 买入节奏点 S4 关→生效 → 配置回测应见「本次下发 1 项（与抽屉不同）」+ 指纹 2d5da788→0473e993 → 点运行回测数字应变（实测年化 16.00%→18.58%、回撤 6.53%→8.60%、Calmar 2.21→1.98）→ 回投资逻辑确认三态仍是「生效」且抽屉值未被改写。**别碰**：`btCfg()` 仍是唯一存档真相源；`go()` 里覆盖必须在 `btSave(c)` 之后；共用键别拆；`__lcOv` 必须非枚举。

- **改了什么**：`edit_work/index.html` v1050 / tag `fw2_v1050_logic_eff` —— 投资逻辑 ①–⑦ 规则表在「三态」后新增「生效作用」列（59 条三件套：作用点 + 现状标签 + 组合影响），并加表下诚实边界句；列宽 8→9 列、min-width 1560。纯展示层，判定/存档/回测参数零改动。
- **未验证的假设**：①各条「组合影响」取自注册表 `act`/`seg` 的实测结论与引擎 cfg 语义，属设计意图描述，**未逐条重跑回测复核**；②窄视口（538px）下新列需横向滚动才看全（表 1608px），未在 1440px 桌面实测整表一屏。
- **下一步 + 别碰**：跑 `python check_js.py` / `check_html_comments.py` / `check_globals.py`（期望 ALL OK / 277 处 0 隐患 / 235 键 PASS）；`verify_fund_daily.py` 校验1 仍 FAIL（`000041` 2019 早期缓存缺，属既存，见 README 待决），发布继续用 `SKIP_GATE=1`。**别碰**：`LOGIC_EFF` 别接成 cfg 下发；别把「开关在回测参数」写成「已生效」；既有 8 列列宽别压。

### 2026-11-21 · v1049 列组 chip 条与 tab 行压字修复 · **已发布 `2e712462`（仓库 raw 字节一致 SHA256 `e2f0c94f…`，index 5,000,576 B）**
- **改了什么**：`edit_work/index.html` 徽标 v1049 + 注释 `fw2_v1049_cgbar_gap`。两处内联 margin `0 2px 10px` → `14px 2px 10px`：①`dcCgBarHtml()` 返回的 bar div（资产配置/自选/经理池共用）；②筛选基金 v1040 的 `#dcScreenColBar` 字符串。**零逻辑、零列结构**：chip 计数、`data-col-grp` 绑定、`dcColsFiltered` 全部未动。README 三节 + frontmatter（ver v1049）同步。
  根因实测：`#dcTabs` 800px 级视口折两行（tab 44px + gap 8 → 96px），chip 条 `margin-top:0`，`tabs.bottom = bar.top = 16.64px`，间距 0 → 文案行贴住第二行 tab 下边框。六 pane 扫描：ov 131px / watch 109px / screen 0→14 / mgr 0→14；rules、chart 无 chip 条未动；四条 bar 内部 `innerOverlap=false`。门禁：`check_js` 21 块 OK / `check_html_comments` 277 处 0 隐患 / `check_globals` PASS（235 键，无新增）。
- **新增资产**：无。
- **未验证的假设**：①用户截图是 2x DPR 的约 800 CSS px 窗口（按 7 个 tab 折两行 + 每 tab 视觉宽约 110 CSS px 反推），本机只复现到 538px 视口下的同一形态（同样 0 间距、同样折两行），**没有在 800px 精确视口下实测**；②14px 是否「够松」是按 chip 内部 gap 6 与 tab 行距 8 估的，未与用户确认视觉偏好；③本轮仍未跑 `verify_sync.py`，双端只做 index 单文件 SHA256 比对。
- **下一步 + 别碰**：强刷 `?t=v1049live` 看筛选基金/基金经理两页的 14px 空档即可。**别碰**：①`--ui-tap` 44px（整站按钮最小高度）；②别用负 margin / 收缩 `#dcTabs` 高度省空间（那正是成因）；③筛选规则、收益曲线没有 chip 条，别为统一硬加。
- **回滚**：`Copy-Item D:\Temp\index_v1048_before_v1049.html edit_work\index.html`。

### 2026-11-21 · v1048 资产配置/自选/基金经理 接入列组 chip · **已发布 `3839045f`（仓库 raw 字节一致 SHA256 `198074ab…`，index 5,000,059 B）**
- **改了什么**：`edit_work/index.html` 徽标 v1048 + 注释 `fw2_v1048_colgrp_all`。①机制外扩：`dcColGrpOn(k, scope)` 加 scope；新增 `dcGrpStore` / `dcColsFiltered` / `dcCgBarHtml` / `dcBindCgBar`；`poolScreenCols()` 改为 `dcColsFiltered(poolColsAll(),'screen')`（行为等价）。②资产配置（`data-dc="overview"` 的 `renderDcOverview`）：`OVC` 按 scope=ov 过滤 + chip 条；CSV 导出仍全量。③自选基金：`cols` 按 scope=watch 过滤 + chip 条（重渲 `renderPoolWatch`）。④基金经理：31 列逐列打 `g`（3 基础 / 8 收益 / 4 风险 / 6 经理 / 6 产品 / 4 详情）+ 按 scope=mgr 过滤 + chip 条（重渲 `renderPool('all')`）。⑤README 三节 + frontmatter（ver v1048）。
  实测（本地 `?t=v1048probe`，真渲染 + DOM 几何）：ov 61→48→12；watch 61→46；mgr 31→25→3；三表状态互不影响（自选关收益后 ov 仍 48/61）；筛选基金 61→60（旧桶，未受影响）。th 与每行 td 数一致（mgr 唯一例外为「▼ 债券池 Top 10」colspan 分隔行）；表头左边界单调递增、无重叠。门禁：`check_js` 21 块 OK / `check_html_comments` 277 处 0 隐患 / `check_globals` PASS（235 键，无新增）/ `verify_manifest` PASS（36 数据集，1 项 W2 旧告警）/ `check_hold_consistency` PASS（9 过 2 警）/ `_audit_alloc_cols` PASS 50 / `_audit_capbal_kpi` PASS 49。
- **新增资产**：无（无新 window 键、无新数据文件、无 localStorage 键）。
- **未验证的假设**：①经理池的 5 组划分（8/4/6/6/4）是按列语义自拟的，用户只给了「按图的模式」、未逐列确认；尤其「分位打折」归收益、「星级」归经理、「代表规模季增 / 限购」归产品，若用户想换组只改 `MGR_CG` 映射表一处；②资产配置「当前 N/M 列」把操作列计入（opN=1），与筛选基金文案同口径，未与用户确认是否需要单列；③本轮仍未跑 `verify_sync.py`，双端一致性只做了 index 单文件 SHA256 比对（本地 / raw 均 `198074ab…`、5,000,059 B）。
- **下一步 + 别碰**：强刷 `?t=v1048live` 按 README「下一步」首条验收。**别碰**：①三个新桶（`state.dcColGrpX.ov/.watch/.mgr`）别合并回 `state.dcColGrp`（用户要独立记忆）；②过滤必须按 `g` 键，不要按列索引（v505d/v778）；③策略执行页 `renderStratAlloc` 与「精简 7 列 / 完整 14 列」、`_audit_alloc_cols.py` 的 12 列硬卡本轮未动；④列组状态别写 localStorage。
- **回滚**：`Copy-Item D:\Temp\index_v1047_before_v1048.html edit_work\index.html`。

### 2026-11-21 · v1047 信号效率移到内层 tab 最左 · **已发布 `f27980be`（仓库 raw 字节一致 SHA256 `41b7480c…`，index 4,994,519 B）**
- **改了什么**：`edit_work/index.html` 徽标 v1047 + 注释 `fw2_v1047_eff_first`。`_sigTabBtns` 数组把 `{k:'eff', label:'信号效率'}` 提到首位，顺序变为 **信号效率 / 持仓信号 / 筛选信号 / 市场信号 / V11狙击 / 趋势策略 / 聪明的钱 / 持仓穿透**（8 个）。**纯位置调整**：`_sigTab = 'hold'` 默认选中未动，pane 结构、tab 切换委托、`fw2_sig_tab_v1` 写入逻辑一字未改。README 三节 + frontmatter（ver v1047）同步。
  实测（本地 `?t=v1047probe`）：徽标 v1047；首个 tab 左偏移 23 = 容器左边缘；默认高亮仍为「持仓信号」；点「信号效率」→ 主表 31 行 × 13 列照常。门禁 `check_js` 21 块 OK / `check_html_comments` 277 处 0 隐患 / `check_globals` PASS（235 键）。
- **新增资产**：无（单文件内两行调整）。
- **未验证的假设**：①用户是否希望**默认也直接停在「信号效率」**——本轮按「只改点名范围」处理，`_sigTab` 仍是 `hold`；若要改，一处 `_sigTab = 'eff'` 即可（会改变交易信号首屏内容）；②窄视口（538px）下 8 个 tab 会折两行，信号效率在第一行首格，位置正确，未做额外排版；③本轮仍未跑 `verify_sync.py`，双端只做 index 字节哈希比对（本地/raw 均 `41b7480c…`）。
- **下一步 + 别碰**：强刷 `?t=v1047live` 看 tab 顺序即可。**别碰**：①`_sigTab` 默认值（改了会改首屏）；②pane 的 DOM 顺序（显隐由 `data-sigpane` 控制）；③tab 切换委托与 localStorage 写入。
- **回滚**：`Copy-Item D:\Temp\index_v1046_before_v1047.html edit_work\index.html`。

### 2026-11-21 · v1046 信号效率「独立观测」列 + 胜率分口径 · **已发布 `42e42202`（仓库 raw 字节一致 SHA256 `42d52b66…`，index 4,994,259 B；`caifu/data/signals-backtest.json` 同批上线 1,440,458 B）**
- **改了什么**：①`edit_work/gen_backtest.py` → `stat_block()` 加 `uniqN`（`len({(code,date)})`），`pools`/`lvls`/`poolLvls` 自动带出；终端打印加 `uniq=`；**逐笔口径零改动**。②`edit_work/index.html` 徽标 v1046 + 注释块 `fw2_v1046_bt_uniq`——主表 12→**13 列**（样本后加「独立观测」，min-width 900→980）、档位卡 10→**11 列**（760→860）；「胜率」→「正收益胜率」、「跑赢基准」→「超额胜率」；口径行补两句定义；判定句「样本 N 笔」补「只对应 M 个独立观测」。`uniqN < n` 的格子标 `#b45309` 加粗。③README 三节 + frontmatter（ver v1046）。
  起因：用户发现表里没有一个正的。查证结论：230 笔完成的入场日只有 2026-10-19（151 笔）与 10-21（79 笔），47 只标的；去重后 **72 个独立观测**。012920 一只基金在 10-19 被九条信号（T1 阶梯止盈/T2 峰值回撤止盈/T3 估值止盈/T4 硬止损/T5 时间止损/T7 回撤补仓/T12 距历史低点/T13 网格跟踪/V1 波动赶底）同时命中、10-21 再九次，同一窗口收益 −5.58% / −8.72% 被记 18 笔——这是 T 系七族均值/中位完全相同的根因。
  重跑：ALL 230/72、act 62/51、near 64/56、**watch 104/19**；统计量（−10.06% / 正收益胜率 7.4% / 超额胜率 15.7%）一个数未变。同期指数（本地 `index-daily.json`，10-19→11-16）：沪深300 −4.66% / 中证500 −7.40% / 创业板指 −15.52% / 中证红利 −0.61%，筛选池 −14.69% 与创业板跌幅相当，性质是「选的就是这类资产 + 这类资产在跌」，不是选错标的。
  门禁：`check_js` 21 块 OK / `check_html_comments` 277 处 0 隐患 / `check_globals` PASS（235 键）/ `verify_manifest` PASS（36 数据集，1 项 W2 旧告警）/ `check_hold_consistency` PASS（9 过 2 警）/ `_audit_capbal_kpi` PASS 49。实测本地 `?t=v1046probe` 与线上 `?t=v1046live`：13 列 31 行、每行 13 格、左偏移 `40/100/240/287/333/407/485/563/651/725/786/864/942` 逐位一致、容器 980=内容 980；档位卡 11 列 4 行；ALL 行 `230 / 72（橙）`；筛选池 6 行 + 档位 3 行、ALL `94 / 53`。
- **新增资产**：`signals-backtest.json` 每个统计行新增 `uniqN` 字段（`groups`/`pools`/`lvls`/`poolLvls` 全部覆盖）；无新 window 键（基线仍 235）。
- **未验证的假设**：①「筛选池 −14.69% ≈ 创业板 −15.52%」只做了跌幅比对，**没有逐只核对筛选池标的的跟踪指数**（表里 `name` 字段多数只有代码，基金名缺失，无法从数据侧判断成分）；②`uniqN` 用 `(code, date)` 去重，同一基金不同快照日本就是两个观测——这个口径未与用户确认是否是想要的「独立」定义；③本轮仍未跑 `verify_sync.py`，双端一致性只做了 index.html 单文件字节哈希比对（本地/raw 均 `42d52b66…`、4,994,259 B）。
- **下一步 + 别碰**：强刷 `?t=v1046live` 按 README「下一步」首条验收（13 列 / 11 列 / 230-72 橙色 / 数值与 v1045 完全相同）。**别碰**：①别用 `uniqN` 当分母重算均值或胜率——那是把口径从「信号笔数」改成「标的数」，与 V11 表和历史版本不可比；②去重键别改成只按 `code`；③橙色只用于「样本 > 独立观测」提示，别与收益红绿混用；④两个胜率标签必须并存。
- **回滚**：`Copy-Item D:\Temp\index_v1045_before_v1046.html edit_work\index.html`；后端 `Copy-Item D:\Temp\gen_backtest_v1045.py.bak edit_work\gen_backtest.py`；数据 `Copy-Item D:\Temp\signals-backtest_v1045.json.bak edit_work\data\signals-backtest.json`（v1045 前端不读 `uniqN`，只回前端也能跑）。

### 2026-11-21 · v1045 信号效率独立子模块（P0 前端 + P1 数据链）· **已发布 `ad3dae7e25e0`（仓库 raw 字节一致 SHA256 `329f51d9…`，index 4,992,311 B；`caifu/data/signals-backtest.json` 同批上线 1,438,599 B）**
- **改了什么**：①`edit_work/index.html` 徽标 `v1045` + 注释块 `fw2_v1045_sig_eff`——交易信号内层 tab 7→**8**，在「持仓信号」后插入「信号效率」；`#btStatWrap` 从持仓 pane 整体迁到新 pane（`#btPoolBar` 池 chip → `#btStatWrap` 主表 → `#btLvlWrap` 档位卡）；主表 10→**12 列**（加 最好／最差 = maxRetPct/minRetPct），`min-width` 760→900，标题「信号效率 · 族 × 档位（样本外）」；新增 `btLvlHtml()`（档位 4 行 × 10 列 + 动态判定句）、`btPoolChipHtml()`、`window.__btEffRender__()`；池状态 `window.__SIG_BT_POOL__`（内存，默认 all）；点击委托加 `data-btpool` 分支（只换数据源，不重拉文件）。②`edit_work/gen_backtest.py` 新增 `build_groups(rows)` / `pools`（all·hold·watch·screen 各一套族×档位表，ALL 总行置顶）/ `lvls` / `poolLvls`（每池 4 行档位汇总）/ `meta.poolCounts`；raw 四分支补 `pool` 字段；旧 `groups` 保留。**逐笔口径（买入日 / 持有 20 净值日 / 基准同窗 / pending 排除）零改动**。③`edit_work/_globals_baseline.json` 233→**235** 键（新增 `__SIG_BT_POOL__` / `__btEffRender__`）。④README 三节 + frontmatter（ver v1045 / updated 2026-11-21）与本文同步。
  重跑结果：`raw 4655 / done 230 / pending 4367 / noNav 58`；`pools` 行数 all 31 · hold 18 · watch 11 · screen 6；`poolLvls` hold 16/4/65/85、watch 5/7/39/51、screen 41/53/0/94；`lvls` act 62（−13.866%）/ near 64（−14.609%）/ watch 104（−4.992%）/ all 230（−10.06%）。ALL 的 beat 16.5%→15.7%、超额 −6.46%→−6.528%，**原因：`index-daily.json` 基准序列多了新点，属数据变化，不是口径改动**。
  实测（本地 :8765 + 线上 `?t=v1045live`，真渲染）：tab 8 个；主表 31 行 / 每行 12 格 / 左偏移 `40/102/246/294/342/422/503/560/637/699/779/860` 逐位一致 / `thOver=false`；档位表 10 列 4 行、溢出版本 0 格；四池切换逐池核对（持仓 18 行 + 16/4/65/85、自选 11 + 5/7/39/51、筛选池 6 + 41/53/0/94 → 观察档 0 时档位卡 3 行），卡头数字与 `meta.poolCounts` 一致；筛选池 ALL 行 −16.101% 与 json 同值。门禁：`check_js` 21 块 ALL OK / `check_html_comments` 277 处 0 隐患 / `check_globals` PASS（235 键）/ `verify_manifest` PASS（36 数据集，1 项 W2 sec_daily 校验器未入闸门的旧告警）/ `check_hold_consistency` PASS（9 过 2 警）/ `_audit_capbal_kpi` PASS 49。
- **新增资产**：`signals-backtest.json` 新增顶层键 `pools` / `lvls` / `poolLvls`，`meta` 新增 `poolCounts`；raw 每笔新增 `pool`；页面新增两个 window 键（基线 233→235，`docs/GLOBALS.md` 已补登记理由）。
- **未验证的假设**：①「T10 红铃失衡」计入 `noNav` 并在口径行写「组合级信号只计入『全部』口径」——这是按 `no-nav codes` 里出现 `T10` 推的，**未逐笔确认它是否真的只出现在 all 池**；②判定句「观察档比行动档高 8.9pp ⇒ 档位不能当预测用」是**单一 19 快照日样本的事实陈述**，未做滚动/分段复算，不代表信号无效；③本轮仍未跑 `verify_sync.py`（前次 `--gh-only` 13 分钟无返回、已中止），双端一致性只做了 **index.html 单文件字节哈希比对**（本地/raw 均 `329f51d9…`、4,992,311 B），README 与资料库语义等价**未验**；④`docs/data-ledger.json` 未改（`signals_backtest ← gen_backtest.py ← G fund-daily` 已登记，本轮只增字段）；`verify_manifest` PASS 但那是**结构对齐**，不代表台账文字描述了新字段。
- **下一步 + 别碰**：强刷 `?t=v1045live` 按 README「下一步」首条逐项验收（8 tab / 12 列 / 四池切换 / 判定句）。剩一件小事：想验双端就跑 `cd edit_work; python verify_sync.py`（预留 15 分钟以上，失败先看是否网络卡住，别当代码问题）。
  **别碰**：①池 chip 点击别改成重新 `loadBacktest()`（会再拉 1.4 MB 并重渲染整页信号表）；②`btStatHtml` / `btLvlHtml` 别在页面里自算分组（唯一口径在 `pools` / `poolLvls`）；③`poolLvls` 必须每池都出，只出 `lvls` 会让「主表在筛选池、档位卡在全部三池」；④「最好 / 最差」只展示、不参与判定句排序；⑤`v11BtHtml()` 那张 V11 表仍未动（家族是 V11-R/V11-W 对照组）。
- **回滚**：前端 `Copy-Item D:\Temp\index_v1044_before_v1045.html edit_work\index.html`；后端 `Copy-Item D:\Temp\gen_backtest_v1044.py.bak edit_work\gen_backtest.py` + `Copy-Item D:\Temp\signals-backtest_v1044.json.bak edit_work\data\signals-backtest.json`，再 `cd edit_work; python check_globals.py --update` 把基线从 235 键退回 233（回滚前端后旧表读 `groups`，旧 json 里就带着，所以只回前端也能跑）。

### 2026-11-20 · v1044 信号回测统计表拆列：代码｜含义｜档位 · **已发布 `1332f1bd5be9`（仓库 raw 字节一致 SHA256 `1d4c383d…`）**
- **改了什么**：`edit_work/index.html` 徽标 `v1044` + 注释块 `fw2_v1044_bt_stat_cols`。`btStatHtml()`（L16426 起）的表由 8 列改 10 列：原首列一格写「S2 行动」（信号族代码与档位压在一起），现拆成 **信号族（代码）｜含义｜档位** 三格，其后仍为 样本／平均收益／中位／胜率／跑赢基准／盈亏比／平均超额；表 `min-width` 600→760px。含义不硬编码：`_famName(f)` 读 `window.SIGNAL_REGISTRY[f].name`（与信号页、投资逻辑页同一份注册表；`code:` 字段是源码行号不是名字，别取错），`ALL` 行写「全部信号（不分族）」，取不到写「—」。卡底口径行前补两句：统计范围＝hold/watch/screen **三池全部基金信号**（三档都算，按族×档分组；M 系宏观非基金、P1/P2 穿透个股无日频净值，都不计入）＋「N 笔完成 · M 笔积累中」是逐快照日累计**笔数**、≠ 信号页 chip 的**当前快照行数**。`v11BtHtml()` 那张 V11 表**未动**。文件 4,981,703 → 4,983,226 B（+1,523）。
  实测（本地 :8765 `?t=v1044probe`，真渲染）：表头 10 项逐字对；**31 行**、每行 `children.length` 集合 `[10]`；抽前 4 行逐格左偏移完全一致（40/131/341/411/481/599/716/800/912/1003）；表宽 1,080 = 容器宽、`scrollWidth−clientWidth=0`；18 个族名全部命中、无一行落「—」；口径行 h=77px、`overflowX=false`。
- **未验证的假设**：①用户第 1 问的答案取自 `gen_backtest.py` 头注 L12 与 L102 `for grp in ("hold","watch","screen")`，**没有逐条比对 `signals-hist.json` 里 hold/watch/screen 的实际笔数分布**（即「三池合计 4655 笔」是按 meta.rawCount 读的，未拆池核对）；②V11 表是否也该拆列，用户未表态，我按「只改点名那张」处理；③含义列 `white-space:nowrap` 让「峰值回撤止盈」独占 210px，宽屏无横向滚动，但 **538px 窄视口下整表要横滚 2 屏**（属既有行为，未优化）；④T3 现实是「估值止盈 / 估值加仓」两行共用一个代码，含义列只显示注册表里的「估值止盈」，未做双名标注。
- **下一步 + 别碰**：强刷 `?t=v1044live` → 交易信号 → 「信号回测统计（样本外）」：表头 10 列、无「信号族 × 档位」；首行 ALL／全部信号（不分族）／全部；其后每行「S2｜回撤买入｜行动」；卡底首句「统计范围：持仓 / 自选 / 筛选池三池的全部基金信号」。别碰：①含义列必须走 `SIGNAL_REGISTRY`（改注册表时这里自动跟着变，抄一份就漂移）；②V11 表（首列「信号族 × 状态」）别照拆——家族是 V11-R/V11-W 对照组，会全列「—」；③统计数值与 `groups` 过滤一个字符没动，数字若变要查 `gen_backtest.py`。回滚：`Copy-Item D:\Temp\index_v1043_before_v1044.html edit_work\index.html`。

### 2026-11-20 · v1043 个股移出持仓信号表 · **已发布 `5f138f034d33`（仓库 raw 字节一致）**
- **改了什么**：`edit_work/index.html` 徽标 `v1043` + 注释块 `fw2_v1043_sig_pen_off`。①`renderSignalDash()` 内新增 `_holdSig = rows.hold.filter(code !== 'P1' && code !== 'P2')`，chip 计数（`actTot/nearTot/watchTot`）与「持仓信号」组入参都改用它——`P1 穿透拥挤` / `P2 单票暴露` 是穿透个股级信号（code 固定 P1/P2、一只股票一行、各最多 6 行），原来把台积电 / 英伟达顶在表顶各成一组；②持仓信号卡下加一行「P1 穿透拥挤 / P2 单票暴露（个股级）不在本表展示 · 明细见「持仓穿透」页」；③`renderSignalSummary()` 的 `all` 同口径过滤（该函数当前无容器、属保留代码）。`P3 穿透 Top5 集中度` / `P4 穿透覆盖率` 是组合级指标，保留。文件 4,980,439 → 4,981,703 B（+1,264）。
  实测（v1042 vs v1043）：组头 50→**35**；chip 全部 452→**443**、只看有动作 87→**85**、只看接近 113→**106**（观察 184 不变）；持仓卡头 行动 50→**48**、接近 78→**71**；页高 7,066→**6,398px**；「N 条数据日过期」12→**3 条**（原过期源主要是穿透个股季频日期）；act 档组头 16→15、near 档 31→29，全表 `/穿透个股/` 命中 0。
- **未验证的假设**：①首版说明行 90 字在 540px 视口外被截，改 44 字后截图可完整读（未在更窄视口复核）；②`renderSignalSummary()` 无容器（`#ovSignal` 在 DOM 里已不存在），我在死代码上做了同口径过滤，只对「将来恢复时」有意义，**未验证它真能跑通**；③「数据日过期 12→3 条」是把 P1/P2 的季频日期一起摘掉的连带效果，是否掩盖了原本要提醒个股数据过期这件事未与用户确认（若要提醒，可移到「持仓穿透」页）。
- **下一步 + 别碰**：强刷 `?t=v1043live` → 持仓信号：不再有「台积电（穿透个股）」「英伟达（穿透个股）」，首组是「杠铃档位（四档）」；卡头 行动 48 · 接近 71 · 观察 184；chip 443 / 85 / 106；「持仓穿透」tab 个股表照常。别碰：①`P1/P2` 判定与 L3961/L3962 投资逻辑注册表（本版只摘展示）；②`P3/P4` 别一起摘；③chip 与表格必须共用 `_holdSig`（单改一处即「数字 ≠ 行数」）；④`ddWarnRows` 照旧并入。回滚：`Copy-Item D:\Temp\index_v1042_before_v1043.html edit_work\index.html`。

### 2026-11-20 · v1042 交易信号页同指数只出一只 · **已发布 `eace481ad3d1`（仓库 raw 字节一致）**
- **改了什么**：`edit_work/index.html` 徽标 `v1042` + 注释块 `fw2_v1042_sig_fam`。①`renderSignalDash()` 的 `byTarget` 分支里，`targets` 排序之后、生成 `seq` 之前按 `idxFamily(code)` + `MERGE_IDX_FAM`（纳指100／标普500／A500指数）分家族归并，每家族只留 1 只代表（行动数降序 → 接近数降序 → 代码升序），其余 target 的行不进 `seq`；②代表那一组的组头加一行短提示「同指数 12 只 · 此表仅列 019441 万家纳斯达克100指数发 · ⚠ 另有 11 只带行动」+「展开全部 12 只 / 收起为 1 只」按钮（`sigFamBtn`，`state.sigFamShow` 内存态不落盘），完整清单放 `title` 悬停；③观察档（`opts.watchRow`）跳过 famNote，否则每行重复一次；④展开态同家族每组都带「第 k 只（已展开）」+ 收起按钮。文件 4,974,101 → 4,980,439 B（+6,338）。
  实测（v1041 vs v1042 同口径同数据）：`#sigBody` 行 598→428、组头 50→37；持仓信号组卡 342→172 行 / 26→13 组；纳指100 组头 12→1（代表 019441）、标普500 2→1（代表 017641）、A500 2→1（代表 022438）；信号页页高 10,501→7,066px（−32.7%）；chip 三档 452／87／113 不变（判定层零改动）。展开→37/48 组、428/572 行，收起回 37/428。
- **未验证的假设**：①代表选择用「行动数 → 接近数 → 代码」，会把「行动数同为 3 的 12 只纳指」按代码取最小那只（全档 019441、act 档 016452、near 档 023422）——用户是否认可「代表随档位变化」未问过；②`自选信号` 分支保留了但没有实测样本（当前页面 tab 已无该组），将来恢复才生效；③只量了 538px 窄屏视口，宽屏下组头提示是否显得太空未测；④东财 `api.fund.eastmoney.com/f10/lsjz` 仍 118 例 `net::ERR_FAILED`（历史既有、走内置快照兜底），未逐条证明与本次改动无关。
- **下一步 + 别碰**：强刷 `?t=v1042live` → 交易信号（持仓信号 / 全部 452）→ 纳指100 只有一组（代表 019441，行动 3 · 接近 3）且组头有「展开全部 12 只」；标普500、A500 各一组；持仓信号卡 172 行 / 13 组头；点展开→12 组，点收起→1 组；「只看接近」档提示应写「余 11 只收起（展开可见）」而非「只见我的持仓」。别碰：①`MERGE_IDX_FAM` 别加「主动权益」（10 只跟踪不同指数）；②`sigTableHtml` 仍按「连续相同 code」分组，别改成按家族分组；③代表别按市值选（会把有动作的小额碎片折叠成没动作的代表）；④`state.sigFamShow` 别落盘；⑤筛选信号组别去重。回滚：`Copy-Item D:\Temp\index_v1041_before_v1042.html edit_work\index.html`。

### 2026-11-20 · v1041 数据管理页三处折叠 · **已发布 `b9fec74fffac`（仓库 raw 字节一致）**
- **改了什么**：`edit_work/index.html` 徽标 `v1041` + 注释块 `fw2_v1041_dm_fold`。①`renderDataMgmt()` 的 `paint()` 加 `isNeed(r)`，默认只显示「需要注意」8 行，其余 33 行留在 DOM 但 `display:none`，chip「当前显示 8 / 41 行」+「只看需要注意 / 展开全部」两按钮（只切 display，不重渲染）；②更新操作区顶部说明 / 6 个轨卡的命令与 note / 底部注意事项折进 `<details>`；③首页新鲜度卡长说明折进 `<details>`；④顺带修轨卡「需求」chip 溢出（`max-width:100%;white-space:normal`）。文件 4,969,476 → 4,974,101 B。整页 6,799px → **3,017px**。
- **未验证的假设**：①只量了 538px 窄屏；更宽视口下两个按钮不换行、chip 行更舒展，未实测；②「需要注意」的语义边界（手动轨算需要注意）是我的判断，用户可能认为「手动轨 = 常态」不该占位置——若要改成仅「滞后/失败」，改 `isNeed` 一行即可；③线上只验了默认态与 `vis=8`，线上「展开全部」按钮未点（本地已验 41 行 / 5,514px）；④骨架阶段仍全列 41 行（5,476px），首次进入最坏 8 秒内会先长后短，未做进一步优化。
- **下一步 + 别碰**：强刷 `?t=v1041live` → 数据管理 → chip 应「当前显示 8 / 41 行」、表格 8 行、整页 3,017px；点「展开全部 41」→ 41 行。别碰：①`isNeed` 判据；②别把折叠改成重调 `renderDataMgmt()`（会再 fetch、页面二次变空）；③`data-dmcmd` 复制逻辑；④骨架阶段别折叠。回滚：`Copy-Item D:\Temp\index_v1040_before_v1041.html edit_work\index.html`。

### 2026-11-20 · v1040 筛选基金表列组 · **已发布 `4717b5962c82`（仓库 raw 字节一致）**
- **改了什么**：`edit_work/index.html` 徽标 `v1040` + 注释块 `fw2_v1040_colgroup` / `fw2_v1040b_quick`。①`poolColsAll()` 尾部给每列打 `g` 组键（base／rank／risk／mgr／prod／entry），新增 `dcColGrpOn` / `poolScreenCols`；②`renderPoolScreen` 的 `cols` 改 `poolScreenCols()`，`poolTableHtml` 未改；③chip 行 5 个组开关 +「全部」「只留基础」；④`state.dcColGrp` 不落盘。文件 4,964,120 → 4,969,476 B（+5,356）。实测 61/4,728px → 12/987px，关收益 46/3,962px；资产配置 61/4,660、自选 61/4,573 零回归。
- **未验证的假设**：①只量了 538px 窄屏（用户实际是手机竖屏），更宽的桌面视口未测 chip 换行表现；②组内列数按「组键命中列数」实测（rank 16 / risk 5 / mgr 11 / prod 14 / entry 1），若后续在 `poolColsAll()` 里加列要记得补 `__CG` 映射，否则新列会落 base 且无法隐藏——**没有断言保护**，下一个加列的人容易漏；③排序：点被隐藏列的表头仍能排序（`_cellVal` 找得到 key），但用户看不到该列，未做「隐藏列不可排序」的限制；④线上只验了 61→12 与 61 全开两态，46 列态只在本地验过。
- **下一步 + 别碰**：强刷 `?t=v1040live` → 基金数据 → 筛选基金 → chip 行应见 5 组 + 全部/只留基础；点「只留基础」=12 列/987px；点「收益」=46 列/3,962px；资产配置与自选仍 61 列且无 chip。别碰：①不要改成按索引隐藏（三池共用列定义）；②`poolTableHtml` 别动；③`state.dcColGrp` 别落盘；④`poolColsAll()` 别改共享单例；⑤其它 pane 的 `cols` 别换 `poolScreenCols()`。回滚：`Copy-Item D:\Temp\index_v1039_before_v1040.html edit_work\index.html`。

### 2026-11-20 · v1039 信号页行级筛选 · **已发布 `a909e875f9db067a17ec934d6ba9263fca324753`（仓库 raw 字节一致）**
- **改了什么**：`edit_work/index.html` 徽标 `v1039` + 注释块 `fw2_v1039_sig_lvl`。①信号页 tab 行下加 chip「全部 452 / 只看有动作 87 / 只看接近 113」，`state.sigLvl` 驱动、不落盘；②过滤只在 `grp()` 的三个 list 入参（`_sigF()`），不碰判定层；③`grp()` 空组早退 + 按标的模式兜底行改 `else if (_sigLvl === 'all')`（首版实测漏改，混进 2 行兜底）；④`body.onclick` 加 `[data-sig-lvl]` 分支。文件 4,961,292 → 4,964,120 B（+2,828）。
- **未验证的假设**：①「只看接近」档在**筛选信号 / 市场信号 / V11 狙击**等其它内层 tab 下的行数覆盖率未逐 tab 量（只量了持仓信号 tab 的三档 341/63/102 与市场 tab 的 818px）；②筛选态下「组头计数＝筛选后数量」依赖用户读那句说明，未做可用性测试；③`_sigF` 对 `lvl` 缺失的行（理论上不存在，`sigTableHtml` 三档全渲染）会直接丢弃——未造缺字段样本验证；④线上只验了持仓信号 tab 的 341/63 两档，其它 tab 未逐一点。
- **下一步 + 别碰**：强刷 `?t=v1039live` → chip 三档数字应为 452/87/113，点「只看有动作」后 63 行 / 13 组 / 无兜底行 / 无空卡。别碰：①筛选别下沉到 `signalEvalAll` 或阈值层（会让「全部」态数字变）；②chip 右侧「组头计数为筛选后数量」说明别删；③「观察」档别加 chip（与 `fw2_sig_wt_v1` 折叠打架）；④`state.sigLvl` 别写 localStorage；⑤兜底行只在 `all` 态补。另：体检第 4 条 ticker「文字被裁」经 `zoom:2` 复核为**误判**，先写的 CSS 已整段撤回（P62）。回滚：`Copy-Item D:\Temp\index_v1038_before_v1039.html edit_work\index.html`。

### 2026-11-20 · v1038 热力图碎块聚合 · **已发布 `350481851118`（仓库 raw 字节一致）**
- **改了什么**：`edit_work/index.html` 徽标 `v1038` + 注释块 `fw2_v1038_other_pool`。`drawHoldingsTreemap` 内：权重 <5% 的家族块聚合为「其他 N 块」（总面积不变、面积＝权重仍成立，碎块合计 >30% 时不聚合）；`rawShare`/`data` 改吃 `mapRows`；tooltip 对聚合块列名单；标签去后缀 + 截 9 字；卡底 note 条件改为 `capped || pooledNote`。文件 4,958,087 → 4,961,292 B（+3,205）。20+ 块 → 4 块。
- **未验证的假设**：①阈值 5% 是看 483×180 卡片定的（4.6% 的 A500 块在 483px 宽下只能显示 3–4 字，故并入）；**若换到宽屏/大卡片，5% 可能偏粗**——未在大视口复核，后续若发现大屏上「其他」过大，可按容器宽度分档；②「碎块合计 >30% 不聚合」的保护阈值 30% 是拍的，未用历史组合回测过；③标签截 9 字对超长名（如「易方达全球成长精选混合(QDII)人民币A」）显示为「易方达全球成长精选…」，是否够辨识未征求用户意见。
- **下一步 + 别碰**：强刷 `?t=v1038live` → 热力图应只剩 4 块且出现「其他 9 块」；卡底有合并口径说明；悬停「其他 9 块」能看到名单。别碰：①聚合别改成面积封顶（会破坏面积＝权重）；②`POOL_PCT` 改值后 note 文案自动跟（`POOL_PCT * 100` 硬拼），别改成写死「<5%」；③tooltip 名单只拼前 6 个，12 只纳指全串会爆宽；④v47 的 75% 封顶是窄屏兜底，别删也别扩阈值。回滚：`Copy-Item D:\Temp\index_v1037_before_v1038.html edit_work\index.html`。

### 2026-11-20 · v1037 持仓体检第 5/6/7/8/11 条 · **已发布 `28b270c0fe6a`（仓库 raw 字节一致）**
- **改了什么**：`edit_work/index.html` 徽标 `v1037` + 注释块 `fw2_v1037_hold_audit2`。①`HD_SLIM_HIDE` + `applyHdColMode()`（按列索引隐藏 10 列，默认关，opt-in，`fw2_hd_slim_v1` 记忆）；②`_isAlert()` + 「⚠ 只看异常」chip + 零值 chip 不再常驻 + 筛选时组强制展开；③`#hdFoot` 按 `state._pfAt` 条件化去掉「示例持仓为模拟数据」；④`detailRow` 加「⚠首笔待同步」行内徽标；⑤`renderDiscipline` gap 文案加「约需补／减 ¥X」。文件 4,951,242 → 4,958,087 B（+6,833）。18 列结构、取数、KPI 零改动。
- **发布后补**：KPI 行「1 只待同步（三列与 T5 不可用）」的裸 `T5` 补成「T5 时间止损」，发布闸门 `_audit_capbal_kpi.py` 的 F02 期望串同步改（非绕过）。
- **未验证的假设**：①精简列后表宽 754px 仍超视口 483px（横滚 1.5 屏），未进一步压缩列宽——压列宽会触发 auto 布局重排，风险大于收益；②「约需补／减」金额用 `denom`（Σ有市值取市值、缺行情取成本 ＝ 18,505.8）而非 KPI 市值 18,520.72，差 14.9 元来自缺行情那只按成本计，未与用户确认是否该统一到 KPI 口径；③「只看异常」未做多选分类（回撤类 / 数据缺口类），目前是一枚混合 chip。
- **下一步 + 别碰**：强刷 `?t=v1037live` → 默认 18 列不变；勾「精简列」→ 8 列 + 自动回最左；点「⚠ 只看异常」→ 3 只（012920／160422／023422）且组已展开；页脚应写账户同步文案；纪律卡应有「约需补 ¥2,405.76」「约需减 ¥5,944.33」。别碰：①「精简列」默认别改成开；②别把列隐藏改成逐格挂 class / CSS 固定列；③异常阈值别新增常量；④`HD_SLIM_HIDE` 索引表要跟着列顺序改（现在 0 基索引，列 3/6/7/8/9/10/12/15/16/17 是保留列）。回滚：`Copy-Item D:\Temp\index_v1036_before_v1037.html edit_work\index.html`。

### 2026-11-20 · v1036 持仓模块体检三条 · **已发布 `7a33510bc39a`（线上字节一致）**
- **改了什么**：`edit_work/index.html` 徽标 `v1036` + 注释块 `fw2_v1036_hold_audit`。①`DISCIPLINE_CFG.ai` 正则去掉「成长／标普500／中证A500」（保留 AI／人工智能／半导体／芯片／科创50／创业板／纳指100／科技），`renderDiscipline` 超线时追加「主因 X 占 Y pct」；AI 科技 67.0% → 5.2%。②新增 `HEALTH_CFG`（mddDeep −20 / lossDeep −20 / volHigh 30）与 `healthOf` 第二段（回撤深／浮亏深／波动高，插在「高集中」之前），健康度 td 补 title 写全两段口径。③`#discCard` 整块从 KPI 与表格之间下移到持仓表之后，`renderDiscipline` 把 `g==='ok'` 的磁贴折叠成一行「达标 N 项」。文件 4,946,283 → 4,951,242 B（+4,959）。
- **未验证的假设**：①「成长」移出 AI 口径后，若某基金实际是纯科技主题（名称只写「成长」、sector 写「主动权益」），现在不会被计入——属**口径取舍**（宁可漏算也不造假红线），但未用重仓股穿透核实过任何一只的真实科技暴露；②`HEALTH_CFG` 的 20%／30% 取自用户风险预算与「近 250 日年化」档，未做过「多少只因此变标签」的敏感性分析；③线上验收时数据未就绪阶段 `r.mdd` 为 null，012920 会先显示「高集中」、数据到位后变「回撤深」，未在慢网上计时该切换的耗时。
- **下一步 + 别碰**：强刷 `?t=v1036live`，按 README「下一步」首条逐项看；复跑 `python verify_sync.py` 期望全量 PASS。**别碰**：①AI 正则别把宽基与「成长」加回；②`HEALTH_CFG` 别并进 `RISK_CFG`（后者三处共用）；③纪律卡别搬回表格上方；④18 列与列宽别动。回滚：`Copy-Item D:\Temp\index_v1035_before_v1036.html edit_work\index.html`。

### 2026-11-20 · v1035 持仓表新增「波动率」列 · **已发布 `53ee475fe190`（线上字节一致）**
- **改了什么**：`edit_work/index.html` 徽标 `v1035` + 注释块 `fw2_v1035_hold_vol_col`；持仓表 `#hdTable` 由 17 列改 18 列，在「权重」左侧插入「波动率」——表头约 L1650、计算段 `fw2_v1035_hold_vol`（`renderHoldings` 内 `fw2_v641_peak_dd` 之后，取序列末 251 点→250 日收益，≥60 点才出值）、明细行 `r.vol` 单元格在 `${r.weight.toFixed(2)}%` 之前、组头/合计各补「—」、空态 colspan 17→18。口径＝近 250 净值日年化波动（日收益总体标准差×√252×100），分红型用累计净值 `__NAV_ACC__`，其余 `__NAV_SERIES__`；现金/货基/无序列/样本不足 →「—」。文件 4,943,162 → 4,946,283 B。
- **未验证的假设**：①`__NAV_ACC__` 是 fund-daily 原始 `acc` 字段序列（v936 建，供刹车卡用），我按「累计净值环比＝含分红总收益」直接用它算波动；未与「按 div_t 公式链乘」版本做过数值对拍（两者在分红日附近可能有细微差）。②023422 在 `fund-daily.json` 无序列（0 点）是数据缺口，不是代码问题——未去核该基金是否新成立/停更。③视口仅 538px 宽，18 列必然横向滚动；未在平板/手机宽度（>800px）下验证「波动率」与邻列是否仍不挤压（auto 布局理论可自适应）。
- **下一步 + 别碰**：强刷 `?t=v1035live` 看首行 012920 是否 38.4%、权重 57.10%，现金/组头/合计为「—」；复跑 `python verify_sync.py` 期望全量 PASS，`python check_globals.py` 期望 PASS（233 键 / 488 点）。**别碰**：①口径窗口（250 净值日 / ≥60 点）与「分红型用累计净值」这两条——改任一都会让 23 只数值集体变；②别给现金/货基填 0.0% 或按类别推断；③别给该列加固定宽度或 colgroup（列错位事故史见 PITFALLS）；④组头/合计的「—」不要改成加权平均。回滚：`Copy-Item D:\Temp\index_v1034_before_v1035.html edit_work\index.html`。

### 2026-11-20 · v1034 补齐 verify_sync（双端校验首次全绿） · **已发布 `021c12d679ea`（线上字节一致）**
- **改了什么**：①`edit_work/verify_sync.py` 19 条陈旧 marker 清账（16 改现役原文、3 删并留 `# ★v1034 清账` 注释）+ `lib_check` 报错补 rc/两端字节/stderr；②`edit_work/cmp_lib.py` **重建**（此前文件丢失，导致「cmp 未 PASS: 」后面空白）——归一化：剥平台 `inject.js`、`pnid` 注释、节点号属性，属性按名排序，空白归一，逐块比；③`edit_work/index.html` 徽标 v1034 + 注释块 `fw2_v1034_orphan_span`，删 hero 区两处孤立 span 闭合标签；④`edit_work/_lib_import_v152.py` 兼容 skill-library 5.11.x 的 `_file_meta` 拆分；⑤资料库节点用 `import_html.py --node-block-id I5QXvst27sR4FsxFbQi2ai` 覆盖到当前版（旧 `op_` token 停在 2026-11-17、报 10034）。⑥顺带清账：`策略执行优化清单` 里 v1029 单文件评估段遗留的 6 处 `%%`（旧脚本 % 格式化漏出）还原为 `%`。README 三节 + frontmatter、清单追加、PITFALLS P58、本文件三行同步；README 已单推 GitHub（1,369,910 B，`BYTE_MATCH True`）。
- **未验证的假设**：①资料库节点覆盖成功但 `publish_url` 为空——我按「协作页」理解、未再核对外部访问口径，若该页需公开发布请另行确认；②cmp_lib 归一化容忍了「平台挪注释/删空容器/重排属性」三类回写，若将来平台开始改写实质内容（如压缩 JS）会判 FAIL，届时按差异块调整口径而不是放宽到忽略内容；③本地仍余 1 处未闭合 span（v7xx 起既有、库端同形态），未动。
- **下一步 + 别碰**：`cd edit_work; python verify_sync.py` → 期望 `PASS —— 双端同步正常（GitHub 六文件字节一致 + 资料库语义等价）`；`--gh-only` 免 token 亦可。**别碰**：①cmp_lib 归一化别放宽到忽略内容差异（判别力基线：对 `D:\Temp\index_v1031_before_v1032.html` 必须仍判 FAIL）；②hero 区孤立 span 已删别加回；③3 条清账 marker 对象已不存在，不要恢复。

### 2026-11-20 · v1033 修复回测页图表全部不绘制 · **已发布 `93657016ef8b`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1033（4,942,462 B，SHA256 `3a4a273d04e5c3a73f5d11c4e7b48d8d411d81f784f37ba6a397c0540e12396d`）。注释块 `fw2_v1033_bt_chart_mount` + 徽标 v1033；把 `_after` 里包着挂图的 `setTimeout(...,0)` 改为命名函数 `_mountBtCharts`，并在 `out.innerHTML` 之后调用。五图（净值 / 分标的市值 / 回撤水下 / 月度收益 / 收益归因）恢复绘制，主图 markArea「区间最大回撤 -6.53%」可取证。ECharts 配置与 `btRoll` 零改动。README 三节 + frontmatter、清单追加、本文件三行同步。
- **未验证的假设**：①修复只保证「数据就绪 + 容器在 DOM」两条前提，若将来 `btRoll` 改成同步、或结果区被改成不插 DOM，仍会退回空图，未加断言保护；②五个容器宽度 511px 下测得 canvas 各 1，更窄屏未测；③`verify_sync.py` 仍 FAIL（≥10 条既存缺标记，v1022 起），与本轮无关未处理。
- **下一步 + 别碰**：接手可验 —— 强刷 `?t=v1033live`，配置回测跑完滚过五图，逐个看是否出线；同时看控制台应无 `reading 'map'`、无 `bt*Chart` 告警。**别碰**：①图表 ECharts 参数与 `btRoll` 口径；②挂图时机别前移；③懒加载四图必须滚进视口才 init，直接 read DOM 判空会误判。

### 2026-11-20 · v1032 回撤诊断区三处旧词改「区间最大回撤」 · **已发布 `dfdc4ceeebfb`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1032（4,940,790 B，SHA256 `1e912d7ecacd7d141b8bcf9c3c9f2eb5b760587b20d86550b224105467151472`）。注释块 `fw2_v1032_diag_mdd_label` + 徽标 v1032；3 处文案：回本所需涨幅卡副行、卡标题「区间最大回撤回本用时」、滚动表标题「口径 B · 年化 / 区间最大回撤」。数值取 `v3.deepDD` / `v3.rec.days` / `roll.b`，零改动。README 三节 + frontmatter、清单追加、本文件三行同步。
- **未验证的假设**：①副行文字 +2 字后在 130px 卡内由 2 行变 3 行（内容完整、无截断、卡高自适应），更窄视口或字号放大会不会 4 行未测；②「回撤预算（已用 / 上限）」与分档表列头「该档回撤（均 / 最深）」有意保留，未与用户确认是否也要改；③净值图 markArea 标注（v1031 改）本轮仍未取得图内渲染证据，本机图表 canvas 不生成属既存缺陷。
- **下一步 + 别碰**：接手可验 —— 强刷 `?t=v1032live`，配置回测滚到「波动与耐受力」：卡标题「区间最大回撤回本用时」77 天、副行「谷底 2025-04-07 → 峰值 2025-02-19；区间最大回撤 −6.53%」、下方「口径 B · 年化 / 区间最大回撤」。**别碰**：①`v3.deepDD` / `v3.rec.days` / `roll.b`；②「回撤预算」口径别混；③分档表列头不在本轮范围。

### 2026-11-20 · v1031 研究页/回测页「区间最大回撤」标签 · **已发布 `46779fab1e69`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1031（4,939,908 B，SHA256 `af18490f830781f6f1f02d1cead0b688f67b629cbb1dea7500d26a829d04a6db`）。注释块 `fw2_v1031_range_mdd_label` + 徽标 v1031；6 处文案：研究页风险速览、回测页吸顶小结、未达标诊断句、过程风险 chip、净值图 formatter、图注「红区＝…」；另给图注 hint 加 `white-space:normal` 防省略号截断。**计算链 `S.strat.mdd` / `st.mdd` 零改动**。README 三节 + frontmatter、清单追加、本文件三行同步。
- **未验证的假设**：①**净值图内 markArea 标注未取到渲染证据**——本机 548px 下主图与四张分图 canvas 都未生成（12 条 `Cannot read properties of undefined (reading 'map')`；用 `D:\Temp\index_v1030_before_v1031.html` 做对照，同样 12 条、canvas=0，属既存缺陷），故该处只有代码层核对，未截图；②吸顶条/图注/chip 的换行只在 548px 视口实测，更窄或浏览器字号放大未测；③「回撤预算（已用/上限）」、诊断卡「最深回撤回本用时」与「口径 B · 年化 / 最深回撤」保留旧词是有意为之，未与用户确认是否也要统一；④`pfHtml` 按标的阈值表自 v1008 起不渲染，本轮未为它调 colgroup。
- **下一步 + 别碰**：接手可验 —— 强刷 `?t=v1031live`：研究页（基金透视 → 012920）「风险速览」第二格「区间最大回撤（近500净值日）」−42.90%；配置回测吸顶条「区间最大回撤 6.53%（预算 20.00%，用 32.63%）」、chip「区间最大回撤 -6.53%（最长水下 204 天）」、图注两行完整。**别碰**：①`S.strat.mdd` / `st.mdd` 算法；②诊断区旧词别顺手改（未获授权）；③图注 hint 的 `white-space:normal` 别删。

### 2026-11-20 · v1030 持仓表列头「最大回撤」→「买入最大回撤」 · **已发布 `ff511dd8ebb8`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1030（4,938,354 B，SHA256 `ed3ac230897534e72356c53264adc3f3261d8a372519d6397a325fd9cd379adf`）。注释块 `fw2_v1030_buy_mdd_label`（L1532 长行内）+ 徽标 v1030；落点仅一处——持仓表 `#hdTable` 表头第 11 列（约 L1648）文案 `最大回撤` → `买入最大回撤`，title 原样。**计算链 `fw2_v641_peak_dd` 与 `r.mdd` 渲染零改动**。README 三节 + frontmatter、清单末尾追加留痕、本文件三行同步。
- **未验证的假设**：①**只有持仓表这一处改名**——研究页（`最大回撤（近500净值日）`）与回测页（`回撤 区间最深`）的「区间最大回撤」是另一口径，**本轮刻意没动、也未与用户确认是否也要改**；②列宽 87px 是 548px 视口下的实测，更窄或浏览器字号放大时未测（auto 布局 + nowrap 不会截断文字，但可能挤压相邻列的内联内容）；③未测移动端底栏遮挡/表格横向滚动条的交互变化（加宽约 26px）。
- **下一步 + 别碰**：接手可验 —— 强刷 `?t=v1030live`，持仓表第 11 列应为「买入最大回撤」，数值与 v1029 逐位一致（012920 −42.90% / 2026-11-17、000746 −6.47%、001015 −18.81%）。**别碰**：①`fw2_v641_peak_dd`（跳过买入前的 `_sd < firstBuyDate`、峰值 `_runPk` 从 `firstBuyNav` 起、`_dd = _sn/_runPk - 1`）——改它会动所有历史数值；②研究页/回测页的「区间最大回撤」别顺手改；③别给该列加固定宽度（548px 下 87px 刚好）。

### 2026-11-20 · 单文件 4.9 MB 拆分评估 · **结案：方案 A「不拆」（用户拍板）** · 未改 index.html
- **改了什么**：清单 P3 最后一条「单文件 4.9 MB」结案——用户 2026-11-20 拍板方案 A 不拆；评估主文档 `docs/SINGLE_FILE_SPLIT.md`，清单 P3 行与批注、README 三节 + frontmatter + 待决、本文件三行同步。`edit_work/index.html` **零改动**（4,937,477 B、徽标 v1029），因此本轮不升版本号、未发布。
- **未验证的假设**：结案本身是决策记录，无新增假设；沿用两条仍是估算——①线上「8,096 ms → 约 6.5 s」是按本地拆出版比例线性外推，**没有线上同构实验**；②「发布去注释压缩省约 0.5 s」是估算，未做构建实验（该方案已否决，不必再验）。
- **下一步 + 别碰**：清单 P3 清零，等新需求；要重开按触发条件（首屏 ≤2 s / 文件 ≥6 MB / 弱网移动端）走方案 C，顺序与验收标准在 `docs/SINGLE_FILE_SPLIT.md` §5。**别碰**：①别把结案理解成「以后禁止拆」——条件到了就拆；②`index.html` 本轮零改动，别因文档提到「评估轨」而误升徽标；③别把 `D:\Temp\_probe_v1029\c_split.html`（故意挖空四个块的测量样本）当可用版本发布。

### 2026-11-20 · 单文件 4.9 MB 拆分评估（评估轨，未改 index.html） · **仅出评估、未发布**
- **改了什么**：新增 `docs/SINGLE_FILE_SPLIT.md`（体积构成表、七个大块清单、三组 DCL 实测、四方案对比、推荐与触发条件、复测方法）。`edit_work/index.html` **零改动**（徽标仍 v1029、4,937,477 B），因此本轮不升版本号、未发布。实测脚本 `D:\Temp\_v1029_split_scan.py` 与 `D:\Temp\_v1029_probe_gen.py`；探针文件在 `D:\Temp\_probe_v1029\`（已移出 `edit_work`）。清单 P3 该条已就地批注（建议不拆）、README 三节 + frontmatter + 待决、本文件三行均已同步。
- **未验证的假设**：①**结论「拆 25% 省 0.78–1.02 s」来自本机 Edge 内核 + 本地 http.server 的 DCL 对照**，没在线上做同构实验（线上拆出版需要真发布才能测，成本高）；线上 8.1 s → 6.5 s 是按 download 比例线性外推，**未实测**。②骨架版 202 ms 只证明「HTML+CSS 布局成本极低」，**没证明**去掉那四个块后页面功能可用（C 版是故意让它报错来测 DCL，所以不能拿它当「拆分已验证」。③「660 处 `index.html` 引用」是 `Select-String` 计数，含注释与文档字符串，**真正必须改的脚本数未逐个清点**（要拆就得先点清）。④未测移动端/弱网（触发条件里列了，但没数据支撑具体阈值）。⑤「发布去注释压缩省 0.5 s」是估算，没做构建实验。
- **下一步 + 别碰**：接手可复测 —— 跑 `D:\Temp\_v1029_split_scan.py` 看体积构成；跑 `D:\Temp\_v1029_probe_gen.py` 生成骨架版/拆出版，开 `http://localhost:8765/_probe/...` 读 `performance.timing`（期望全量 3.4–3.8 s / 骨架 0.2 s / 拆出版 2.6–2.8 s）。**别碰**：①`index.html` 本轮零改动，别因看到「v1029」就以为要再升版；②若决定拆，先做方案 C 的第一块并保留 `?v=` 逐文件指纹，别用 `defer`/动态 import；③`_audit_plan_merge_v895.py` 等按单文件函数顺序定位的锚点，拆文件后要重锚，不许删断言凑绿；④别把 `D:\Temp\_probe_v1029\c_split.html` 当可用版本发布（它是故意挖空四个块的测量样本）。

### 2026-11-20 · v1029 策略执行四面板结构索引（注释密度） · **已发布 `d05aeef6f65f`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1029（4,937,477 B，SHA256 `18801024f9e7775942cd110428f794e7bca908a932dc207a8fceea68404ccde8`）。注释块 `fw2_v1029_pane_index`（L1532 长行内，`fw2_v1028_fd_singleflight_vol` 之前）说明「只加不删」与注释体积实测；四个 6 行结构索引分别落在 `renderLogicView`（投资逻辑 · 约 L20954）、`renderStratAlloc`（资产配置 · 约 L21112 前）、`renderBacktest`（配置·持仓·自选回测 · 约 L25407，函数定义在行首无缩进）、`renderStratReview`（月度复盘 · 约 L21114 前）。内容统一六项：入口 / 写入口 / 存储键 / 数据口径 / 缓存键 / 已知坑。README 三节 + frontmatter、清单 P3 行与批注均已同步。
- **未验证的假设**：①**「6 行索引够用」是设计判断，没做实测**——没有找第二个人（或隔几天后的自己）按索引去定位函数并计时；若实际仍要翻沿革注释，说明索引粒度不够细或位置不对。②索引里写的函数名与存储键**是 2026-11-20 的静态真相**，靠 grep 核对，之后任何改名都会让它过时（无自动化校验，只能靠人守纪律）。③「注释不占体积」的结论按字节字符数统计，**未做 gzip 后对比**（注释在压缩后占比更低，结论只会更极端，不影响判断方向）。④四段注释插在函数定义之前，**未验证对 IDE 折叠 / 代码大纲的影响**（不影响运行）。
- **下一步 + 别碰**：接手可验 —— 强刷 `?t=v1029live` 应只见徽标变化；`view-source` 搜「结构索引（v1029）」应 4 命中、「fw2_v1029_pane_index」1 命中；门禁 `cd edit_work; python check_js.py; python check_html_comments.py; python check_globals.py` 应全绿。**别碰**：①索引里的键名 / 函数名改代码时必须同步改（假路标比没有更坏）；②别删历史 `fw2_v*` 注释；③注释里别写 `window.xxx` 字面与 HTML 标签字面（会让 check_globals 读取计数漂移 / check_html_comments 报 TAGLIT）。清单 P3 只剩「单文件 4.9 MB」，未拆。

### 2026-11-20 · v1028 fund-daily 本地副本 + HEAD 指纹 + 加载路径合并 · **已发布 `284fb1c87b348a92a19601ef7d7af546bc9a4213`（线上字节一致；中间版 v1027 `cbaa8471c13c`）**
- **改了什么**：`edit_work/index.html` → v1028（4,932,481 B）。tag `fw2_v1027_fd_idb_cache`：`__FD_ONCE__` 单飞加 HEAD 指纹（ETag | Last-Modified | Content-Length）+ IndexedDB 副本（库 `fw2_fd_cache_v1` / store `kv` / 键 `raw`，存 `{json, fp, savedAt}`），指纹一致直接用本地副本、不一致走原 GET 链并在空闲写回；拿到的 json 挂 `window.__FD_JSON__`，回测 `btLoad` 入口直接分组复用。tag `fw2_v1028_fd_singleflight_vol`：波动率卡的 `loadData` needFund 分支并入 `__FD_ONCE__` 并立即 `__FD_FLUSH__`（此前它在首屏 300ms 自己 `fetchJson` 一份全量，与单飞重复）。`docs/GLOBALS.md` 更新基线（233 键 / 488 赋值点）并新增「新增键登记」表。清单 P3 条已就地批注（含对「12MB / 按月切片」前提的修正与「为什么不做切片」）。
- **未验证的假设**：①**HEAD 指纹只在 github.io 同源路径验证过**（线上 ETag 形如 `W/"6b0003fe-8b9246"` + Last-Modified + Content-Length 三项齐备）；`raw.githubusercontent.com` 回退源未测——跨域下 ETag 不在 CORS 安全头列表，很可能读不到，但那只在第一源 404 时才走。②**IndexedDB 不可用（隐私模式 / 配额不足 / 企业策略）时的降级路径没实测**：代码全是 try/catch 静默回退到原 GET，逻辑上等价，但没有真机样本。③**「数据更新日指纹会变」用篡改 IDB 指纹模拟**（改成 `STALE-*` → 重下并回写），没有等真实数据刷新日验证；若 GitHub Pages 的 ETag 在内容未变时也变动，会导致每次都重下（收益归零但不会出错）——这点建议在下次数据刷新后看一眼 HEAD 是否仍命中。④**其它设备/浏览器首次打开仍下一次 9MB**（缓存 per-device，未做共享）。⑤**多标签同时打开**未测：两个页面同时冷启动可能各下一次（IDB 写入后才有共享）。⑥`index.html` 自身 4.9 MB 未动。
- **下一步 + 别碰**：接手可验 —— 强刷线上 `?t=v1028live` **两次**：第一次约 6 秒下载一次 `fund-daily.json`（decoded 8,933KB / 传输 1,125KB）并写 IDB；**第二次应只剩一发 HEAD、零下载**。控制台核验：`performance.getEntriesByType('resource').filter(e=>/fund-daily/.test(e.name)).map(e=>[Math.round(e.startTime), e.decodedBodySize])` → 第二次只有一条 `decodedBodySize=0`。页面应与 v1026 逐项一致（持仓 18,520.72 / 17,397.79、行动信号 41、波动率卡 22.62% vs 16.90% / 覆盖度 86%、配置回测 16.00% / −6.53% / 2.21 / 指纹 `2d5da788`）。**别碰**：①`cache:'no-cache'` 与 `__FD_FLUSH__` 时序；②HEAD 指纹「三件套取并集」（只留 ETag 会让本地 http.server 永不命中）；③IDB 键 `raw` 与 `fw2_bt_cache_v1` 是两个库，别合并；④`__FD_JSON__`（已在 GLOBALS.md 登记，删了回测会再下一次 9MB）。清单只剩「注释密度」一条；`verify_sync.py` 全量仍 FAIL（≥10 条既存缺标记，v1022 起就缺）。

### 2026-11-20 · v1026 window 全局键孤儿清理 + 基线门禁 · **已发布 `9be24147a139`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1026（4,925,171 B，**已发布**：master `9be24147a139`，本地/线上 SHA256 `10a2a396…`，`BYTE_MATCH True`）。tag `fw2_v1026_globals_gc`：删 4 个除赋值外全文 0 读取的 `window` 键（`__SEC_AS` / `__SIGCNT__` / `__pxKline` / `__pxPre`）；`__vol699Render` 因是调试 / 外部触发入口保留。**新增门禁** `edit_work/check_globals.py` + 基线 `edit_work/_globals_baseline.json`（**232 键 / 486 赋值点**）：默认「新增未登记键 FAIL / 键消失 WARN / 读取次数变化 INFO」，`--update` 重写基线，`--file` 指副本做构造测试，跳过 HTML 注释区间。**新增台账** `docs/GLOBALS.md`（五类计数 18 内联依赖 / 36 数据挂载 / 150 导出 / 27 同块自用 / 5 孤儿→删 4、不做单一命名空间的三条理由、分批迁移路径）。清单 P3 条与「P3 剩余」行、README 三节 + frontmatter 均已同步。
- **未验证的假设**：①**「那 4 个键真没人读」是静态扫描结论**——判据为 `window.X` 词边界读取 = 0 且裸标识符引用 = 0；**没做运行时监控**（未 hook `window` 属性读写观察 30–60 秒真实交互），也没排除「其它脚本 / 外部页面通过 window 访问」的可能。②**孤儿判定依赖注释跳过**：注释里写的 `window.X =` 示例不算赋值（首版没跳，基线多出假键 `X`，已修）；但若有人在**字符串字面量**里写 `window.X =` 仍会被计为赋值点——目前无此写法，未加字符串剥离。③**`__vol699Render` 保留是凭源码注释判断**（「调试 / 外部触发入口」），没实测控制台里是否真会用到。④线上只做首屏 + 宏观 + 信号 + 配置回测口径条冒烟，**未逐页点 8 个模块的每个子页**；`check_globals` 只对当前 `index.html` 生效，不覆盖 `edit_work` 之外其它 html。
- **下一步 + 别碰**：接手可验 —— `cd edit_work; python check_globals.py` 应打 `PASS（232 键 / 486 赋值点，新增 0 / 消失 0）`；想看门禁真挡得住，跑 `python check_globals.py --file D:\Temp\_globals_probe1.html`（该副本里插了 1 行 `window.__probe_undeclared = 1;`，应 `FAIL 新增 1`）。**别碰**：①18 个内联属性调用的全局函数（`logicSet` / `__btGo` / `allocColMode` / `logicGateToggle` / `__mcGo`）——删了按钮当场失灵；②36 个数据挂载键（`SIGNALS_CFG` / `SM13F` / `SEC_DAILY` / `HOLDINGS_SEED` / `BRAKE_T` / `MACRO_SNAP`）；③`__vol699Render`；④别用前缀 / 正则批量删 window 键；⑤`check_globals.py` 的注释区间跳过别删。清单剩余：单文件 4.9 MB / 每次回测拉 12 MB `fund-daily.json`、注释密度；`verify_sync.py` 全量仍 FAIL（≥10 条既存缺标记，v1022 起就缺，本轮未处理）。

### 2026-11-20 · v1025 localStorage 遗留键一次性清理 · **已发布 `483a03147f45`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1025（4,923,459 B，**已发布**：master `483a03147f45`，本地/线上 SHA256 `0bd2e460…`，`BYTE_MATCH True`）。tag `fw2_v1025_ls_gc`：文件末尾（PWA 注册注释之前）新增一段独立 IIFE，一次性删除 **11 个源码已无独立引用的遗留键**（`fw2_roll3` / `fw2_roll5` / `fw2_roll_cur` / `fw2_roll_off` / `fw2_roll_off5` / `fw2_slow_probe` / `tmp_v977r` / `fw2_bt_ovr` / `fw2_v957_t2_on` / `fw2_v970_v11_on` / `fw2_v971_v11_p10`），白名单硬编码、跑完写 `fw2_ls_gc_v1025` 不再遍历。判据＝键名在 index.html 按词边界（前后非字母数字下划线）独立匹配为 0、同仓其它 js/py/json 亦为 0。清单 P3「全局命名空间」条已就地批注（含对本条原口径「26 键 / 8 个迁移键」的修正：实测 45 键 / 10 个标记类、其中 3 个是死标记）。
- **未验证的假设**：①**「那 7 个迁移标记仍然需要」是读代码推的**——它们的迁移段在 `btCfg()` 里、位于「合并存档之后」，即首次会覆盖存档里的显式值；删标记会让旧设备上的实验残留（`postSellHalf:true`、`tpPeak:true` 之类）复活一次。本机存档（`fw2_bt_plan` 1,021 B、`fw2_bt_hold`/`fw2_bt_custom` 各 2 B）看不出残留，但**没在「带残留的老存档」上做删标记的对照实验**，所以保守保留。②**其它设备未验**：手机/另一台机器上的 11 个死键要等各自下次打开页面才会清，本轮只在当前这台机器（本地域 + 线上域）实测。③**`__onT` 未删**：0 引用但不是本项目命名（非 `fw2_` 前缀）、来路不明，按「不删来路不明的键」保留；若确认是某个早退 SDK 的残留，可加进白名单。④清理脚本是同步执行的，实测不影响首屏（它在页面末尾、且只读 11 次 `getItem`），但**没在低端机/冷启动上量过耗时**。
- **下一步 + 别碰**：接手可验 —— 线上 `?t=v1025live` 控制台列 `localStorage` 键：应为 **35 个**，不再有上述 11 个，且多一条 `fw2_ls_gc_v1025`；`capital_balance_v1` 仍 25,424 B、`fw2_trade_ledger_v1` 仍 10,201 B、`fw2_bt_plan` 仍 1,021 B、`fw2_logic_v1` 仍 878 B（数值不变即证明只删了该删的）。**别碰**：①7 个仍在起作用的迁移标记（见上）；②别把白名单改成前缀批量删；③`fw2_ls_gc_v1025` 标记别删（删了只是多跑一次，但没必要）；④`__onT` 别删。清单剩余：`window.xxx =` 230 键 / 单文件 4.9 MB 与每次回测拉 12 MB 日频数据 / 注释密度。

### 2026-11-20 · v1024 清单 P3 第 2 条「重复 id」清理 · **已发布 `42f48eaf875d`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1024（4,920,955 B，**已发布**：master `42f48eaf875d`，本地/线上 SHA256 `aa6a5ca4…`，`BYTE_MATCH True`）。tag `fw2_v1024_dup_id`：①研究页两套页头按钮差异化——股票页头 `rsCollect`/`rsAddHold` → `rsCollectS`/`rsAddHoldS`，场外基金页头 → `rsCollectF`/`rsAddHoldF`（`renderResearchHead` / `renderFundHead` 各自的绑定同步）；②两套「综合诊断」环 `rsRing` → `rsRingFund`（后端 market_screen 口径）/ `rsRingStock`（固定规则打分），各自 `chartOf` 同步；③另修第三组运行时重复 id：移动底栏 `labelOf(b)` 原本用一条「span class="dot」开头的正则去红点，但源码 span 的属性顺序是 data-page-node-id 在前、class 不在首位，正则匹配不到，整段 span 连同 `id="navNewsDot"` 被复制进底栏 → 运行时两个同名 id；改为 cloneNode 后按 class 删 `.dot`。DOM 结构、class、样式、点击处理、图表配置零改动。清单 P3「重复 id」条已就地批注落地；README 三节 + frontmatter（`ver: v1024` / `next` / `updated`）同步。
- **未验证的假设**：①**两套模板真正同屏共存从未构造**——当前股票/场外基金页头互斥渲染，改名后「同屏各绑各的」只是代码上成立，没有造同屏样本点过。②**底栏红点「本来就该没有」是读 CSS 推的**：`.nav-item .dot` 才有 display:none/`.on` 亮起规则，底栏 tab 是 `.tab` 不带该样式、也收不到 `add('on')`，所以修复前也没有可见故障；若当初设计本意是「底栏也要红点」，那正确修法是给底栏加样式与同步，而不是删 dot——本轮按「注释里写的是去红点」理解。③线上首屏只渲染持仓（144 个 id），研究页那几组 id 的唯一性是在本地逐页点过后测的，线上未逐页遍历（字节一致，逻辑等价）。④`rsRingFund` / `rsRingStock` 只验了「存在 + 118×118 + 1 个 canvas + 圆环成像」，未逐项核对环内数字与 v1023 是否逐位相同（模板与取数未动，推断相同，未做数值比对）。
- **下一步 + 别碰**：接手可验 —— 线上 `?t=v1024live` 进「基金数据 → 基金透视」分别分析 `510300` 与 `f012920`，两套页头的「★ 收藏」「＋ 持仓」都应在、点了有反应，「综合诊断」环分别 80 分（维度加权）/ 56 分（推断·规则打分）；`document.querySelectorAll('#rsCollect,#rsAddHold,#rsRing').length` 应为 0。**别碰**：①`chartOf('rsRingFund')` / `chartOf('rsRingStock')` 与容器 id 必须同名（只改 id 不改 chartOf 会静默不挂图）；②底栏 `labelOf` 别再回到正则写法（属性顺序不保证）；③`navNewsDot` 现在全页唯一，别再给它加副本（`$('#navNewsDot').classList.add('on')` 只作用桌面那份）。清单剩余：P3 全局命名空间（window 230 键 / localStorage 26 键含 7 个一次性迁移键）/ 单文件体积与 12 MB 日频数据 / 注释密度。

### 2026-11-20 · v1023 清单 P3 第 1 条「死代码」整段清理 · **已发布 `10e437ef9244`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1023（4,918,773 B，**已发布**：master `10e437ef9244`，本地/线上 SHA256 `6ec3c1ab…`，`BYTE_MATCH True`）。tag `fw2_v1023_dead_code`：按「函数名在全文件作为标识符只出现 1 次」判据删除 28 个无引用函数（341 行），并删 2 行孤立分节注释；同时修 `edit_work/_audit_plan_merge_v895.py` 的 B01 锚点（`recForm()` → `renderRecList()`）与 `edit_work/verify_sync.py` 期望清单里指向被删函数的 5 条断言（带「★v1023 清账」注）。另在根目录清单里就地作废 P2「⑧-B 参数页 7 项对配置回测无效」一条（逐项核对后 7 项全部参与计算）。
- **未验证的假设**：①**「只出现 1 次」判据只覆盖 `function name(` 声明形式**——`var f = function`、箭头函数、以及 `window['draw' + kind]` 这类动态拼接调用不在覆盖范围，本轮 28 个逐个确认无这类引用（静态 grep + 运行时页面无报错双证），但不能保证全文件没有第二个死函数藏在别的写法里。②**运行时覆盖是抽样而非穷举**——八个模块首屏 + 策略 5 子页 + 信号 7 子页 + 数据 12 子页 + 研究页两种页头都点过，但没点遍所有按钮与弹层（例如「负债设置」「批量净值」这两个表单的原入口按钮若还在会立刻暴露，实测没有按钮引用）。③**`verify_sync.py` 仍 FAIL，属既存**：报 ≥10 条缺标记，逐串与 `D:\Temp\index_v1022_before_v1023.html` 对照在 v1022 就已缺失，与本次删除无关；本轮只摘除指向被删函数的 5 条，其余留给下一轮清账。④行高差异（本地同表 61/60 vs v1021 基线 38–39px）源于名称格多了一行「△ 接近预警（N 只）」小字，属数据侧标记，未经数据侧确认其触发口径。
- **下一步 + 别碰**：接手可验 —— 线上 `?t=v1023live` 抽查资产配置（应仍是 7 列 / 14 行 / 角标 ×2·×12·×2、合计 62,000 / 100.00% / 18,521 / +43,479）；`rg 'function recForm|function btScopePanelHtml|function renderConA' edit_work/index.html` 应 0 命中。**别碰**：①`_audit_plan_merge_v895.py` 的 B01 锚点是「策略渲染链结束分界」，只能挂到其后仍存活的函数（现为 `renderRecList()`），挂错会连带跳过 B02–B06；②`verify_sync.py` 里 5 条「★v1023 清账」注释是台账留痕，删了会让后来人以为标记丢了；③不要再按「出现 1 次」无脑删，必须先人工确认无 `var` 形式/动态拼接引用。清单剩余：P3 的重复 id / 全局命名空间与一次性迁移键 / 单文件体积 / 注释密度。

### 2026-11-20 · v1022 投资逻辑页 h3/h4 + 三态单选 · **已发布 `7b6f8c1ceb5f`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1022（4,939,697 B，**已发布**：master `7b6f8c1ceb5f`，本地/线上 SHA256 `5aa9fa3c…`，`BYTE_MATCH True`）。tag `fw2_v1022_logic_h3_radio`：①页头「投资逻辑」、当前层标题（`logicLayerHtml` 的 head）由 `b` 改 h3，「版本与证据」由 `div` 改 h4（h4 显式写 margin，全局只重置了 h1–h3）；②`logicRowHtml` 的三态由 3 个 button 改为一组单选：`.lg-seg` 外壳 + 三段 label + 3 个视觉隐藏 radio（`aria-label` + 外壳 `role=radiogroup`），点击仍 `onchange="logicSet(id,st)"`。三态判定、买点闸拦截、存档键 `fw2_logic_v1`、重渲染路径均未改。
- **未验证的假设**：①**买点闸拦截分支未构造实测**——升「生效」被拦那条路径（`logicSet` 里 `logicGateIds()` 命中且 `logicSigJudge` 未 pass）本轮只读代码，radio 走的是同一个函数入口，理论上等价，但没有造一个必然被拦的样本点一遍。②分段宽度随文字自适应（生效 37 / 观察 37 / 关 25px），窄屏（<380px）下 8 列表格本就横向滚动，三态列未单独再压。③键盘可达性：radio 是隐藏的（`opacity:0;width:0;height:0;pointer-events:none`），Tab 会聚焦到一个不可见控件，**未做 focus-visible 处理**——若后续要做无障碍，给 `.lg-seg:focus-within` 加描边即可。④测试中动过 P6 状态，已把 `dirty=false`、`updatedAt='2026-11-20 10:47'`、删两条 log 写回，页面复显「L3 · 基准（未改动）」；若用户此前另有未采纳草稿，这份写回会把它一并抹掉（本轮实测存档本就是基准态，脚本按实测值恢复）。
- **下一步 + 别碰**：接手可验 —— 线上 `?t=v1022live` 进「策略执行 → 投资逻辑」，三态列应是一段式分段控件、按钮总数 11、`#stp-logic h3` = 2。**别碰**：radio 的 `onchange`（改成 click 会与 label 的默认行为重复触发两次 `logicSet`）；隐藏 radio 别改 `display:none`（部分浏览器 label-for 点击不触发 change）；`.lg-seg label:last-child{border-right:0}` 别删（否则右边缘多一条竖线）。清单剩余：P2「⑧-B 参数页 7 项对配置回测无效」（v1016 已代码核对否掉，清单待就地更正）、P3 死代码 / 重复 id / 一次性迁移键 / 8 个数据集新鲜度告警 / 注释密度。

### 2026-11-20 · v1021 资产配置指数家族角标 · **已发布 `628a1badddd4`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1021（4,937,962 B，**已发布**：master `628a1badddd4`，本地/线上 SHA256 `1265baaf…`，`BYTE_MATCH True`）。tag `fw2_v1021_alloc_idx_badge`：资产配置表两处指数家族聚合行（主动权益明细聚合 + 计划外指数聚合，同一模板）把名称下的 `div.gsub`「N 只同指数」改成贴名称右上方的 inline 角标 `×N`（11px 灰底圆角，title 写「同指数 N 只基金合并为这一行」），**只在 >1 只时渲染**；CSS 追加 `.idx-n`。取数、7/14 两套列结构、数值、rowspan、排序、颜色、折叠逻辑零改动。
- **未验证的假设**：①「同指数 =1 只的家族行不需要 ×1」是按「行首列已标『指数』、数量 1 无信息量」判断的，用户未表态；若他想要每行都标数量，把条件 `> 1` 去掉即可（一处两行）。②行高下降量（55–56 → 38–39px）是在 548×546 探针视口、内容区 490px 下测的；宽屏下名称格更宽、`gsub` 本来也可能不折行，**节省可能更小，未验**。③整表 833 → 682px 的对比取自线上 v1020（预算 62,000）与本地 v1021（预算 50,000）同页不同预算——行数同为 14、行高由内容决定，推断差值主要来自 9 个家族行各降 17px，但**不是严格同参对比**；要严格可把两版挂同预算再测。④完整 14 列态在 490px 下角标折行（名称格极窄），属 v1019 起既有挤压，未修。
- **下一步 + 别碰**：接手可验 —— 线上 `?t=v1021live` 进「策略执行 → 资产配置」，家族行应为单行「A500指数 ×2」「纳指100 ×12」「标普500 ×2」，单只家族无 ×1，列仍 7 列、表高明显变矮。**别碰**：`.idx-n` 的 `white-space:nowrap`（去掉会让「×12」自身折行）；`> 1` 条件（见上方未验证假设 ①）。清单剩余：P2「⑧-B 参数页 7 项对配置回测无效」、P2「投资逻辑页 h3/h4 与三态单选」、P3 死代码 / 重复 id / 一次性迁移键 / 8 个数据集新鲜度告警。

### 2026-11-20 · v1020 回测结论吸顶小结 · **已发布 `d46f995cd7e7`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1020（4,936,511 B，**已发布**：master `d46f995cd7e7`，本地/线上 SHA256 `71766ef2…`，`BYTE_MATCH True`）。①`fw2_v1020_bt_kpi_sticky`：结果区最前拼一条 `bt-kpi-bar`（左「✓ 达标 / ✗ 未达标」徽标 + 年化·最深回撤·Calmar(严格) 三组判定），变量全部复用 `conclBar` 那组（`S.strat.ann` / `S.strat.mdd` / `S.strat.calmarS` / `ddUse` / `tgt` / `ddCap` / `calmarLine`），空态/运行中/失败分支不插入。②`fw2_v1020b_bt_kpi_fixed`：`position:sticky` 实测失效后改 fixed 浮条 `.bt-kpi-ghost` + `window.__btKpiBind/__btKpiUpd`，判据「自然条 `rect.bottom<=0` 且结果区 host `rect.bottom>=90`」，宽度 `min(host.width, innerWidth-16)`、`left=max(8, host.left)`、左边框色随自然条；监听 window scroll/resize 与 `.scroll-area` scroll（passive），渲染后 60ms 补一次定位。③徽标 v1020 + 两个注释块。引擎、结论条三判定、⑧ 层参数、资产配置列结构零改动。
- **未验证的假设**：①**`.scroll-area{overflow:auto}` 夺走 sticky 上下文**这一根因是实测链条（滚动发生在 window、`.scroll-area` 自身不滚、条 `top` 随内容走）推出来的，未做「去掉 overflow 后 sticky 恢复」的反向实验——若要做，需先确认 `.scroll-area` 的 overflow 是否为别的模块依赖。②同一原因下回测页 `.tb thead th` 的表头吸顶**一直失效**（实测滚过表头后 `th.top=-120`），本轮未修、未回归测试别的 view 的 sticky 表头（`#view-data .dc-tbl thead th` 同样是 `top:0`，推测同病，未验）。③浮条显示判据里的 `90` 是「底部 tab bar 高度 + 余量」的经验值，换设备/换 DPI 未复测。④浮条宽 519 = 本机内容区宽（视口 548 下 host.width），宽屏未实测；窄到 380px 时浮条内三组文字可能折行增高，未验。⑤曾加的 `body.bt-kpi-on` + `--bt-kpi-h` 表头下推补丁**已整段撤回**（实测零效果），别照旧笔记再找它。
- **下一步 + 别碰**：接手可验 —— 线上 `?t=v1020live` 进「配置回测」跑一次，滚到净值曲线时顶部应有小结条、滚回顶部消失；`#stp-bt` 结论仍是 16.00% / 6.53% / 2.21 / 32.63%。**别碰**：`upd()` 的两个判据（只判滚动量会在结果区上方误显）；宽度公式（写死像素就不再对齐内容区）；`__btKpiBind` 的 `passive` 监听（去掉会让滚动掉帧）。清单剩余：P1 第 3 条「2 只同指数」角标、P2「⑧-B 参数页 7 项对配置回测无效」、P2「投资逻辑页 h3/h4 与三态单选」、P3 死代码 / 重复 id / 一次性迁移键 / 8 个数据集新鲜度告警。

### 2026-11-20 · v1019 品牌英文名 + 资产配置表列收敛（7 列 ⇄ 14 列）· **已发布 `efeec76919a6`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1019（4,930,841 B / 4,193,227 字符，**已发布**：master `efeec76919a6`，本地/线上 SHA256 `6e0da295…`，`BYTE_MATCH True`）。①`fw2_v1019_brand_en`：title / apple-mobile-web-app-title / 侧栏 `.b1` 统一 `Personal Finance Desk`，`.b2` 改 `display:none`（同名英文行）；logo「理」实测本就 `display:none`，模块中文名未动。②`fw2_v1019_alloc_slim`：资产配置表默认 **7 列**（档位 / 代码 / 资产名称 / 目标金额 / 目标占比 / 实际市值 / 调仓金额），表头右侧按钮切回完整 14 列（整表重绘，选择存 `localStorage.fw2_alloc_colmode_v1`）；五类行模板 + 两个 rowspan 组头 + 合计行逐处配条件 td，取数/数值/rowspan/颜色零改动。③静态卡 `_audit_alloc_cols.py` 改为 A02（精简 7 列）/A02b（完整 14 列）/A03/A03b（只卡完整态）/A03c（两套 colgroup 与表头配对），50 项 PASS。
- **未验证的假设**：①**CSS 隐列方案已被实测否掉**——`col{visibility:collapse}` 在 Chromium 不折叠列宽，5 个次级列仍占位，实测「实际市值 / 调仓金额」被压成 0 宽、表宽 314px、表头叠字；同思路别再用（v778 是折 `tr`，对 `tr` 有效、对 `col` 无效）。②精简列数是在**本机内容区 490px**（bu 探针视口 548）下调出来的；更窄（手机 380–420px）未实测，届时 7 列仍会挤，可考虑档位与名称再收。③切换按钮走整表重绘，**未测**在「正在跑回测/净值异步回来触发重绘」期间连点两次的表现（重绘会覆盖，理论上状态以 localStorage 为准、不会错乱）。④「2 只同指数」角标（清单 P1 第 3 条）**未做**，仍占名称格一行。
- **下一步 + 别碰**：接手可验 —— 线上 `?t=v1019live` 进「策略执行 → 资产配置」应为 7 列、数字完整（`10,575` 不被截、合计 `62,000 100.00% 18,521 +43,479`），点「列：精简 7 列（显示全部 14 列）」切 14 列再切回，刷新保持；宽屏侧栏品牌应只有 `Personal Finance Desk` 一行。**在 548px 探针视口下侧栏是响应式隐藏的**（`aside.sidebar{display:none}`），想核验品牌文案需临时 `display:flex` 或换宽视口。**别碰**：`renderStratAlloc()` 里 `_colSlim` 必须在函数开头赋值（放 html 拼接之后会因 var 提升拿到 undefined、表格永远不带精简态——本轮踩过）。

### 2026-11-20 · v1018 回测引擎分片（冻结消失 · 有进度）· **已发布 `e51f568d4488`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1018（4,925,750 B / 4,189,802 字符，**已发布**：master `e51f568d4488`，本地/线上 SHA256 `c0d063f4…` 逐字节一致）。tag `fw2_v1018_bt_chunk`：①`btRun` 改 generator，主循环按 `performance.now()` 每约 40ms `yield` 一次进度、进循环前先 `yield 0`；同步调用走 `btDrain`（返回值与原函数逐位相同），异步走 `btPump`（让出用 `MessageChannel`，`setTimeout(0)` 会被钳到 4ms）。②`btRoll`（滚动窗口矩阵，2016–2023 × 持有 1/2/3 年 × B/C 两池，最坏 48 次 btRun＝耗时主因）改 `async`，逐窗口 `await btPump` 回报「已完成/总窗口」。③`go()` 取数段拆成「算」与「渲染」，原 894 行渲染收进 `async _after`；命中缓存仍同步调 `_after`（旧路径不变），要算时先 `btPump` 再写 `__btCacheByPool`/`_idbPut` 再调 `_after`。④结果区新增真实进度行（主回测百分比 → 滚动矩阵 d/t 窗口，文本节流 250ms）。⑤滚动矩阵结果加内存缓存 `__btRollCacheByPool`（键＝口径指纹 + `|roll`），`__btRunTok` 令牌丢弃跑动中换口径的旧结果。
- **未验证的假设**：①「60–90 秒」是清单写的历史估计，本机实测同步版只要 **5.1 秒**（同参数 3 年期 11 只），已在清单就地更正；**重场景（自选池几十只 / 十年区间 / 冷数据）未实测**，那里分片的价值应更大，但总墙钟翻倍的代价也可能更大。②本地总墙钟 5.1 → 10.2 秒、线上同口径 3.5 秒，差异来源推断为「让出期间别的页面任务插进来跑」（本地同源多标签、探针 interval 等），未逐项拆账。③最大单次停顿 649–943ms 落在跑完后的整页渲染（`_after` 一次性 innerHTML + 四图挂载），这一段未分片；低端机可能更长，未测。④`btRoll` 内存缓存在刷新页面后清空，未落 IDB/localStorage（体积大，未评估）。
- **下一步 + 别碰**：接手可验 —— 线上 `?t=v1018live` 进「配置回测」点运行，应看到进度行从「主回测 x%」走到「滚动矩阵 d/t」，期间可点别的 tab；跑完 `#stp-bt` 24,569 字符、结论 16.00% / 2.21 / 32.63%。**别碰**：`btPump` 的 `MessageChannel`（改回 `setTimeout(0)` 会把总耗时再拉长）；`btDrain` 的两个同步调用点（`btRoll` 里的准入评估 `fac`）改 `btPump` 会拿到 Promise 而不是结果；`_paint` 的 250ms 节流别删。清单剩余项：P1 资产配置 14 列收敛（列错位历史事故多，未拍板）、P2 回测结果 sticky 小结、P2 投资逻辑 h3/h4 与三态单选、P3 死代码/重复 id/一次性迁移键；Web Worker 方案仍挂账未做。

### 2026-11-20 · v1017 策略执行四面板懒渲染 · **已发布 `e23bf5f27961`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1017（4,918,991 B / 4,184,945 字符，**已发布**：master `e23bf5f27961`，本地/线上 SHA256 `d0cc9b73…` 逐字节一致；README 推 `BYTE_MATCH True`）。tag `fw2_v1017_lazy_panes`：①`renderStrategyView()` 只画当前激活的 `st-tab`（新增 `__stratActiveTab` / `__stratPaneRender` / `__stratPaneDone`）；②`switchStratTab()` 切到「资产配置」「月度复盘」时重画目标面板（回测仍走 v997 骨架重建、投资逻辑仍走 v1004 逻辑分支）；③**切过去每次都重画，不做「画过就沿用」**——沿用会把面板钉在「数据：加载中…」（首次切回测时净值未到齐，之后只重绘当前 tab，再切回来因标记已置不再重画）；④两处隐式依赖补丁：`go()` 的 `_kick` 里先回填 `btDataHint`（空态 / 口径已变两条 return 也覆盖），`renderStrategyView()` 里提前 `ensurePeHist()`、分位到齐后若回测面板画过就补画一次。
- **未验证的假设**：①线上「配置回测」本机无该口径缓存 → 只能看到空态（506 字符、hint 已正确为 `asOf 2026-11-19`），**「买点闸 · 估值分档从 0 个恢复到 31 个」这条修复只有本地有结果的页面验过**（v1017 与 v1016 的 bt `textContent` 24,569 字逐字一致），线上要出结果需真跑一次 20–90 秒。②切 tab 每次重画实测 5–17ms 是在 548×546 视口、本机、4.9MB 页面上测的，低端机/移动端未测。③`__stratPaneDone` 现在只用于「分位到齐要不要补画回测」，若日后有人把它当成「跳过重绘」的开关用，会重现「加载中钉死」。
- **下一步 + 别碰**：接手可验 —— 线上 `?t=v1017live` 点「策略执行」（应只画投资逻辑，另外三块空）、逐个切 tab 看内容齐全（资产配置 3,620 / 复盘 3,647 / 回测 312 为空态）。**别碰**：`ensurePeHist()` 的提前调用（删了回测分档缺分位）；`__stratPaneDone` 的用途（只做补画判断）；四个渲染函数本体本轮零改动。清单剩余项：P1 回测同步阻塞（`btRun` 在 `go()` 里同步跑 60–90 秒，建议分片让出或 Worker，动调用时序，需先定「同参数结论条逐字一致」的验证口径）、P1 资产配置 14 列收敛（列错位历史事故多，未拍板）、P2 回测结果 sticky 小结、P2 投资逻辑 h3/h4 与三态单选、P3 死代码/重复 id/一次性迁移键。

### 2026-11-20 · v1016 资产配置口径折叠 + 回测空态按钮收敛 · **已发布 `d65be85af165`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1016（4,915,016 B / 4,182,592 字符，**已发布**：master `d65be85af165`，本地/线上 SHA256 `1f3d7a62…` 逐字节一致；README 同步推 `BYTE_MATCH True`）。两个 tag：①`fw2_v1016_note_fold`——`renderStratAlloc()` 的 `.strat-note` 只留 5 句核心口径，其余（定投金额·月 / 累计应投 / 进度滞后 / 目标偏移 / 颜色口径）收进同卡内 `details`，summary 为「展开：定投 / 累计应投 / 进度滞后 / 目标偏移 / 颜色口径」，**文字一字未删**；②`fw2_v1016_one_run_btn`——删掉空态块与「口径已变」分支里两颗重复的「运行回测」，改为「点上方『运行回测』开始（约 20–90 秒）…」文字指路，顶部运行条成唯一入口。
- **未验证的假设**：①线上「自选回测」池因浏览器缓存命中直接走了结果分支、进不到空态，该池的空态改法只有**本地实测**（`#stp-bt` 454 字符、按钮 2 个）＋线上字节一致作为间接证据；线上空态只在**配置回测**池实拍（无缓存、`#stp-bt` 523 字符、按钮 = 运行回测｜修改参数 →、含「点上方」指路）。②线上自选回测结果区出现「合计 0 只 · 组合级」而合计行仍有 ¥23,711.28 投入——未查，可能是空标的池渲染旧结果，属**既存**疑点，与本轮改动无关，未下结论。③清单里「⑧-B 7 项参数对配置回测无效」经代码核对**不成立**（`perFund` 关掉会回退全局阈值 L23005、`rebal`/`gridExt`/`gridFund` 参与计算、`tgtAnn`/`ddBudget`/`rf` 即达标线），已就地更正清单，未折叠。
- **下一步 + 别碰**：接手可验 —— 强刷 `?t=v1016live` 看资产配置首屏（口径 5 句 + 一行折叠 summary，展开后多 483 字；表头 29 个 th / 14 列数值不变）；或清掉 localStorage 的 `lastResult:*` 再进自选回测验证空态只剩一颗按钮。**别碰**：`details` 里那段口径文字（刹车卡/分位卡共用依据）；`btRun` 引擎与结论条本轮零改动，回测结论应逐字不变（16.00% / 2.21 / 32.63%）。清单剩余项：回测同步阻塞（分片/Worker，动 `btRun` 调用时序，需先定"结论逐字一致"的验证口径）、`renderStrategyView` 懒渲染、资产配置 14 列收敛（列错位历史事故多，未拍板）、回测结果 sticky 小结、投资逻辑 h3/h4 与三态单选、P3 死代码/重复 id/一次性迁移键。

### 2026-11-20 · v1015 月度复盘月报口径自愈 + 回测第三池预热/归池补全 · **已发布 `ad4f2dfba4a7`（线上字节一致）**
- **改了什么**：`edit_work/index.html` → v1015（4,914,046 B / 4,182,338 字符，**已发布**：master `ad4f2dfba4a7`，线上 SHA256 `297d425a…` 与本地逐字节一致）。两个 tag：①`fw2_v1015_review_dc`——`renderStratReview()` 首次渲染时若 `window.__NAV_MONTH__._dcReady` 为假则 `ensure()` 月末净值索引，就绪后置 `_dcReady`、调 `window.__rptSync`（＝资金平衡 IIFE 内 `autoGenReports` 的跨块出口，紧跟在 `var _autoRpt = autoGenReports();` 之后挂出）重放存量月报并重渲染，`_revEnsure` 防重入；`revKpis()` 返回对象增 `navBasis`，`revConclusion()` 在 `navBasis !== 'month-end-v2'` 且差额 > 0.5 时改出「月报口径待重放：…不是账实差异 / 不必手工修数据」，`revReportHtml()` 的判语同步把「校验差」改「口径待重放」。②`fw2_v1015_pool_warm` + `fw2_v1015_pool_key`——启动预热列表 `['barbell','custom']` 补 `'strategy'`；`_poolOfKey` 由「custom 否则 barbell」改三分支。
- **线上首开实测（自愈链已跑通，不再是假设）**：线上域名首开时 localStorage 存着上一版的 9,322 字符 latest-fallback 旧月报、`_dcReady` 未就绪；只点「策略执行 → 月度复盘」（未进资金平衡页），页面即出 18,827.95 / 21,057.12 / −2,969.17 / 净投入 740 / 自洽 ✓，全页「先修数据」「口径待重放」均 0 命中；回读该条月报已为 `navBasis=month-end-v2`、`generatedAt 2026-11-20T04:51:35Z`，存储 9,322→8,854 字符；三表复核 18,827.95 − 21,057.12 − 740 = −2,969.17 闭环。**仍未验证**：⑴「口径待重放」这个分支本身没有实跑（自愈完成后没有可停留的未就绪窗口，仅代码路径核对）；⑵线上配置回测仍空态「这个口径还没有算过」——该域名 localStorage 从无此口径缓存，不是预热失效（预热命中已在本地 origin 实测）；⑶本轮**推翻了优化清单里 P0 的原始定性**：清单引用的「上月净资产 17,641.93 / 本月收益 −11,606.09 / 净利润 6,035.83 / 自洽差 −17,641.93」是旧会话 latest-fallback 读数，重载两次后复盘与资金平衡一致（21,057.12 → 18,827.95、净投入 740、净利润 −2,969.17），说明问题在口径时序而非账实不符；⑷`lastHtml:` 读取路径（`__btHtmlByPool`）仍未拆，v1013 只停了写入。
- **下一步 + 别碰**：验收 `?t=v1015live` → ①徽标 `v1015`；②**不进资金平衡页**直接看「策略执行 → 月度复盘」，2026-10 应为 18,827.95 / 21,057.12 / −2,969.17 / 净投入 740，判语「自洽 ✓」，全页无「先修数据」；③到资金平衡三表核同一组数（18,827.95 − 21,057.12 − 740 = −2,969.17）；④重开浏览器直接进配置回测，应「正在复用上次结果…」并在数秒内出结论条（16.00% / 2.21 / 32.63%），不再空态、不重跑。**别碰**：`__rptSync` 是复盘拿 `autoGenReports` 的唯一入口（跨 IIFE 不能直引）；月报重放必须保持幂等，别加「只跑一次」标记，否则台账补录后不再刷新；`_poolOfKey` 三分支别退回两分支（旧 strategy 单键会被归进杠铃池）。
- **回滚点**：`D:\Temp\index_v1014_before_v1015.html`（4,909,496 B，改动前完整备份）。
- **截图**：`D:\Temp\v1015_bt_warm.png`（配置回测命中缓存后出结论条）、`v1015_review.png`（月度复盘 2026-10 自洽）。


- **2026-11-19 · v993 滚动矩阵跳过重抽（结掉 blocks=19 的悬案）**
- **改了什么**：`edit_work/index.html` 的 `btRun` 加第三参 `opt`，`btRoll` 两处调用传 `{skipFac:true}` 跳过 `btEntryStats`/`btEntrySig`；`btSigPersist` 记录补 `src:'main'`；徽标 v993。已发布 commit `964b3c29` / blob `3531beac` / 4,831,590 B。
- **未验证的假设**：⑴矩阵跳过后耗时下降多少没有前后对比测（旧版没记时），只能确认结果数值与滚动窗口段未变；⑵跳过 `ent` 不会影响矩阵任何展示列（矩阵只用 `strat`/`hold` 汇总，按代码推断，未逐列核对）；⑶仍没排除「别的视图也渲染显著性卡」的可能，`src` 字段只是让这种情形可被看见。
- **下一步 + 别碰**：若要量耗时，在 `btRoll` 首尾打 `performance.now()` 存 `window.__rollMs`；观察窗 60/120/250 要动 cfg 键与指纹，先拍板。**别碰**：`btRun` 的主运行调用（24404）不能传 `skipFac`，否则⑧ 层买点闸永远拿到空证据；规则计数 65 条；指纹 `deef15c1`。

- **2026-11-19 · v992 买点闸接线（从文案到拦截）**
- **改了什么**：`edit_work/index.html` 新增 `LOGIC_SIG_KEY`/`LOGIC_ENTRYBAND_IDS`/`logicSigLatest`/`logicSigJudge`/`logicGateLine`/`btSigPersist`；`logicSet` 加硬闸；`btSigCardHtml` 渲染时落盘；徽标 v992。已发布 commit `e636103b` / blob `481f0162` / 4,831,120 B。
- **未验证的假设**：⑴`LOGIC_ENTRYBAND_IDS` 只有 T8/T15，是人工判定「靠估值分位挑买点」，没有机器判据；⑵存档曾出现 blocks=19/minP=0.012 的一路写入，来源未定位（疑为对照口径或自选 scope 的 btRun），若那两个视图也渲染显著性卡，会覆盖「最近一次」；⑶闸门只拦「升生效」这一个动作，不改引擎、不影响回测数字。
- **下一步 + 别碰**：要查 `blocks=19` 那一路，在 `btRun` 各调用点加 `console.count` 或给 `btSigPersist` 加 `scope` 字段区分；把纳入清单做成 ⑧ 层可勾选需动 LOGIC_BT 结构。**别碰**：规则总数 65 条、回测引擎与指纹 `deef15c1`、`fw2_bt_sig_latest` 的键名（⑧ 层读它）。

- **2026-11-19 · v991 BT4 买点闸（规则层收口）**
- **改了什么**：`edit_work/index.html` 的 `LOGIC_BT` 里 BT4 口径前置「【买点闸】」并把「分档显著性（块重抽 2,000 次 ＋ Bonferroni α=0.0033）」写成硬门槛，动作行补「判证据不足 · 暂不启用」；徽标 v991。已发布 commit `0c6ce2ca` / blob `347727ba` / 4,824,610 B。
- **未验证的假设**：⑴「买点类规则」只列了四个因子，若将来新增第五因子（如 PE 分位），需同步扩这句话，否则新因子会绕开闸门；⑵闸门只写在规则文案里，**没有代码拦截**——用户仍可手工把某条改成「生效」，页面不会阻止。
- **下一步 + 别碰**：若要真拦截，应在 `logicSet` 或采纳流程加校验（当前 P1 只读＋三态存档，尚未接线）；观察窗 60/120/250 可配置需变量化卡面「120 日」文案。**别碰**：规则总数 65 条（新增条目会改 ①–⑦ 计数与页面文案）、回测引擎与 `deef15c1`。

- **2026-11-19 · v990 入场分档显著性检验（块重抽 + Bonferroni）**
- **改了什么**：`edit_work/index.html` 新增 `btEntrySig`（按买入月份分块、B=2000、固定种子 LCG）+ `btSigCardHtml`（显著性卡，插在入场质量卡之后），`stats.sig` 由 `btEntrySig(stats.ent, 2000)` 计算；徽标 v990。已发布 commit `58b5f73a` / blob `291617b6` / 4,823,797 B。
- **结果**：3 年窗 16 块 15 档全不显著（最小 p=0.18）；5 年窗 35 块，净值中间档 p=0.03（校正阈值 0.0033，不算显著）；10 年窗 50 块 15 档全不显著（最小 p=0.10）。卡面结论=分档只能当描述，不能进准入规则。
- **未验证的假设**：⑴块内买入仍可能来自同一只标的，实际独立信息量低于笔数；⑵Bonferroni 是最保守校正，换成 BH-FDR 可能出现 1 档「边缘显著」，未做对照；⑶固定种子保证同机同数据可复现，但换种子后 p 值会小幅波动，未做多种子稳健性检查。
- **下一步 + 别碰**：若要观察窗可配置（60/120/250），必须同时变量化卡面「120 日」文案并接受 `btParamHash` 指纹变更（`deef15c1` 会变）。**别碰**：回测引擎与 3 年窗硬基线 13.67/−5.91/2.04/103。

- **2026-11-19 · 分档敏感性：5 年窗重算 + 60/250 日观察窗**
- **改了什么**：无代码净变更（临时把 `btEntryStats` 第三参改 60、250 各跑一遍，已还原 120，文件 4,814,547 B 与线上一致、`deef15c1`、13.67 复现）。结论写进 README ⑦⑧⑨ 三段。
- **数据**：5 年窗（当前代码口径）94 笔 +11.64% 基准 65.82%/+9.60% → 超额 +2.04 pct；10 年窗 117 笔 → +3.07 pct；3 年窗 60/120/250 日 → +3.54 / +9.70 / +23.84 pct。深回撤档三窗最差（3 年 60日 42.11%、120日 52.63%、250日 68.42%；5 年 68.75%；10 年 62.50%）。高波动档 60日 61.11% → 250日 94.44%，翻转不可用。
- **未验证的假设**：⑴超额随窗长放大可能只是基准分母效应，未做同窗随机对照分层；⑵样本 54 笔且同波段多次买入高度自相关，任何百分比都不可当独立样本；⑶未做 block bootstrap 显著性检验。
- **下一步 + 别碰**：若要做观察窗可配置（60/120/250），必须同时把卡片表头/说明里的硬编码「120 日」换成变量（实测改 60/250 后仍显示「平均 120 日」），且新增 cfg 键会改动 `btParamHash` 指纹（`deef15c1` 会变），需同步更新证据台账口径。**别碰**：回测引擎与 3 年窗硬基线 13.67/−5.91/2.04/103。

- **2026-11-19 · v989 版本号改整数递增（原 v988l）+ 10 年窗分档验证**
- **改了什么**：`edit_work/index.html` 15 处 `v988l`→`v989`，徽标后新增 `fw2_v989_renumber` 注释（记录新规则 v989→v990→… 禁字母后缀，并列历史 v988a–v988l 对应关系）；已发布 commit `e825f387` / blob `adcd5b7f` / 4,814,547 B。README 加版本号规则行、`ver: v989`、当前进度补「⑦ 10 年窗验证」，INBOX 本条。
- **10 年窗（2016-01-04→2026-07-03）实测**：回合 11 / 8胜3负 / 72.73% / 均盈 +73.65% / 均亏 −11.23% / 赔率 6.56 / 期望 +50.50% / PF 19.39；仅已平仓 2 笔全亏（0%/−16.85%）。入场 117 笔、基准 41,075 个（66.29%/+10.18%）、实际 +13.24% → **超额 +3.07 pct**（3 年 +9.70 / 5 年 +2.04）。距 250 日高点「深回撤」档三窗都是最差（52.63%/68.75%/62.50%）；双高 83.33%/63.33%/76.47% 不稳。
- **未验证的假设**：⑴「深回撤最差」只是三窗描述性一致，未做显著性检验，同波段多次买入高度自相关；⑵波动「高」档两窗最好，未排除高波动区间后续普遍反弹的 beta 效应；⑶线上 CDN 首次核验常仍旧版，本次以 `?t=v989live` 强刷确认 v989。
- **下一步 + 别碰**：跑 60/250 日窗口敏感性（改 `btEntryStats(data,trades,cfg,N)` 第三参，无需改 UI）；PE 历史轨要等台账补序列，别用当前快照 `pePct` 回溯。**别碰**：回测引擎与 3 年窗硬基线 13.67/−5.91/2.04/103、指纹 `deef15c1`。

- **2026-11-19 · v989 ③ 胜率赔率 + 入场质量因子分档（原记 v988l）**
  - **改了什么**：`edit_work/index.html` → v989（4,813,771 B，commit `4e83f601`，blob `4dbee9d3`，已发布；版本号由 v988l 顺延为 v989，用户 2026-11-19 要求 988 后按 989 递增、禁用字母后缀）。新增 `btWinRateStats(list)`（回合口径胜率/赔率/期望/金额 PF，挂 `stats.wr`）＋`btWrCardHtml(S,cfg)`；新增 `btFacAt(rows,idx)`（只用 0..idx 算因子）＋`btEntryStats(data,trades,cfg,120)`（买入笔→120 交易日收益→四因子分档＋两维交叉＋基准，挂 `stats.ent`）＋`btEntCardHtml(S,cfg)`；`perFund` 每条加 `f`（建仓日因子）；两张卡插在 `btVolCardHtml` 之后。口径＝用户「按照你建议继续」的 A 口径。
  - **未验证的假设**：⑴120 交易日是拍定值，**未测 60/250 日敏感性**（同一批买入换窗口，档位排序可能翻转）；⑵分档阈值取样本自身 33%/67% 分位，**跨区间不可比**（3 年与 5 年窗的档界不同，如 2.8% vs 17.6%）；⑶同一波段内的多次买入高度自相关（网格连续加仓），**样本名义 N 笔但有效样本远小于 N**，未做显著性检验，结论只能当描述性统计；⑷赔率失真阈值 2% 是经验设定（1% 时仍出现 13.33，故抬到 2%），非统计推导；⑸「买点超额」基准是「同区间任一天买入」的算术平均，**未按资金量加权**，也未剔除区间末不足 120 日的截断样本（基准含截断样本，实际笔含 4 笔截断）。
  - **下一步 + 别碰**：验收 `?t=v988l*`（断言徽标 v988l、基线 13.67/2.04/103、指纹 `deef15c1`、两张卡出现、回合卡黄标「样本不足」、入场卡基准行有数）。下一段建议先跑 **10 年窗**看分档是否与 3/5 年同向（3 年超额 +9.70 / 5 年 +2.04，差异过大，需第三窗判是否区间巧合）；PE 历史轨接上后再补第 5 因子。**别碰**：`btRun` 内核与 `perFund.retS` 口径（指纹 `deef15c1` 与 13.67/−5.91/2.04/103 是硬基线）；`btEntryStats` 里 `rows` 必须过滤 `r.d <= cfg.end`（曾漏过滤，把区间外净值算进 120 日收益，导致 5 年窗数字错一版）；卡片置灰**不要**用外层 `opacity`（合成层导致内容不绘制、整卡只画背景）。
- **2026-11-19 · v988k ② 波动率三项客观量 + 波动三分位分档**
  - **改了什么**：`edit_work/index.html` → v988k（4,785,660 B，commit `22c8b650`，blob `53100b14`，已发布）。新增 `btVolMetrics(curve,cfg)`（结果挂 `stats.vol3`）与 `btVolCardHtml(S,cfg)`（插在结论区 `cmpHtml` 之后）：回本所需涨幅（最深回撤谷底→峰值所需涨幅）、最长水下天数（连续低于历史峰值的最长日历天数，期末未回本标 open）、最深回撤回本用时（峰值日→首次回本日）；波动分档＝20 日滚动年化波动 33%/67% 分位切低/中/高，各档给占比·复合年化·回撤均/最深·波动区间。**不设「拿不住」阈值**（用户明确表态）。另修回归：`applyStd` 提为模块级 `btApplyStd`，`renderBtCfgHost` 补绑「3/5/10 年」「重置为标准口径」按钮。
  - **未验证的假设**：①「该档复合年化」是把各档不连续日收益连乘后折年，等效于「该状态下日收益的平均水平」，不是某段连续持有收益——文案已注明，但若要做「高波动时段之后 N 日收益」需另算；②分档阈值用区间自身的三分位，跨区间不可比（同一策略在 3 年/5 年窗阈值不同，属预期）；③「每 1% 年化对应 X% 波动」为线性外推，只作量级参照。
  - **下一步 + 别碰**：跑 ③ 胜率赔率 + 五因子分档（PE 分位 / 自身净值分位 / 距 250 日高点回撤 / 相对 MA200 / 波动档；样本 <20 笔置灰；交叉只做「双低 / 一高一低 / 双高」三档）。复现：本地 `python -m http.server 8765`（cwd `edit_work`）→ 持仓回测运行 → 应得 13.67/−5.91/2.04/103 且卡片显示 +6.28% / 206 天 / 90 天。**别碰**：回测引擎逐位不变；测试后把母版区间清回 `2023-07-03~2026-07-03`（本轮已还原），并删 `fw2_bt_evidence` 测试记录。
- **2026-11-19 · v988j 补实回测四条边界（选品消费端 / 证据指纹 / scope 显隐 / 恢复继承）**
  - **改了什么**：`edit_work/index.html` → v988j（4,773,964 B，commit `398e1e15`，blob `ffaeead7`，已发布）。①⑧-A 新增「母版口径 → 选品（消费端）」：`btPickRun/btPickHtml/renderBtPickHost`＋`PICK_KEY='fw2_pick_snapshot'`＋`btPickCap(cfg)`，真读 `btCfg('plan')` 的 pool/watchW/budget，按筛选池既有顺序取前 N=⌊100/watchW⌋ 只、单只额度=预算×占比。②BT5：`BT_EVID_KEY='fw2_bt_evidence'`／`btParamHash(cfg)`（FNV-1a 8 位 hex）／`btEvidenceWrite(cfg,res)`（`go()` 内 btRun 后自动写）／`btEvidenceHtml()`＋`btEvidCount()`（⑧ 层准入规则视图下方台账，卡头「已挂 N 条」）；回测页口径条出「· 指纹 <hash>」。③显隐：`btParamsHtml` 用 `<span id="btBlockPoolW">` 包住自选权重/每只占比，`renderBtCfgHost()` 按 scope 隐藏/禁用/收敛池选项；`btCfg(scope)` 末尾按 scope 强制 `d.pool`。④`btScopeExtraHtml()`＋`window.btScopeReset(scope)`（confirm → removeItem → 重绘）。**同轮修 4 个真 bug**：btSavePlan/btSave 丢弃 pool（⑧-A 改池无效）；renderBtCfgHost 未写回 `window.__btCfgScope`（改动存不进）；btCfg 池类型未按 scope 强制（母版改池带偏 ⑧-B）；`c.pool` 笔误（ReferenceError 被 catch 吞 → 面板 0 控件）。另修：证据卡静态占位改按条数；`btResetStd` title 裸代码补中文名（T16 卖出后破位减半 / T7 回撤补仓 / V11 狙击 / W3·S4 趋势闸门）。
  - **未验证的假设**：①选品容量口径 N=⌊100/watchW⌋（5%→20 只）是否就是用户心里的「容量」——若想按档位目标（进攻 35%）再乘一次则要改；②选品排序用筛选池 `Object.keys(funds)` 的既有顺序（未按 3 年年化/夏普重排，用户未表态）；③「恢复继承」用系统 confirm，未做自定义弹层；④⑧ 层改池后回测页是否要提示「参数已变请重跑」未做。
  - **下一步 + 别碰**：跑 ② 波动率三项客观量（回本所需涨幅 = 1/(1+mdd)−1、最长水下天数、回撤持续期，按波动分档，**不设「拿不住」阈值**），再跑 ③ 胜率赔率 + 五因子分档（PE 分位 / 自身净值分位 / 距 250 日高点回撤 / 相对 MA200 / 波动档；样本 <20 笔置灰）。复现基线：本地 `python -m http.server 8765`（cwd `edit_work`）→ 持仓回测点「运行回测」应得 13.67/−5.91/2.04/103、指纹 `deef15c1`。**别碰**：回测引擎逐位不变；`fw2_bt_plan` 现在会存 pool，测试后请清回 `{budget:62000,start:'2023-07-03',end:'2026-07-03',pool:'barbell'}`，并删 `fw2_bt_hold/fw2_bt_custom/fw2_bt_evidence/fw2_pick_snapshot`，否则本地台账会带测试记录。
- **改了什么**：`edit_work/index.html` v988i（`fw2_v988i_bt_param_single_source`）——回测参数单点化：`btParamsHtml(cfg)` 唯一渲染入口 + 三层存储（`fw2_bt_plan` 母版／`fw2_bt_hold`、`fw2_bt_custom` 覆盖 diff）+ `go()` 改存储驱动 + 回测页参数控件归零 + ⑧ 层二级「准入规则／回测口径」三卡 + `btCollectDom` 类型还原修复。已发布 commit `2b1f2cda` / blob `5b0cdcfa` / 4,755,556 B。
- **未验证的假设**：①自动化选标的链路目前**没有任何代码**读 `fw2_bt_plan`，⑧-A 卡上「自动化选标的按它跑」只是文案承诺，尚未接消费端；②「允许覆盖」只在纯前端存储层生效，尚未接入 BT5「证据绑定快照」——回测结果还没记下"这次用的是哪个 scope 的哪份参数"；③47 个控件里 `customCodes/customW/customWMode` 只对 ⑧-C 有意义，在 ⑧-A/⑧-B 下仍会渲染，未做按 scope 显隐。
- **下一步 + 别碰**：跑 `edit_work/check_js.py`（末行 `结论: ALL OK`）与 `check_html_comments.py`（233 处注释 0 隐患）；本地 `python -m http.server 8765` 后进「策略执行 → 持仓回测」点运行，期望 3.26%/0.23/36.49%（默认母版 ¥62,000）。**别碰**：回测引擎 `btRun`、`LOGIC_BT` 六条准入文案、①–⑦ 三态存储 `fw2_logic_v1`。
- **2026-11-18 · v978（熊市减速 bearSlow）——实测零差异，实现未落地**
  - **改了什么**：`edit_work/index.html` → v978（4,705,514 B，commit `aac8f998`）。cfg 加 `bearSlow`/`bearSlowPct`；`_slowMul(_d,_s,_nav)` 作用定投/网格/T7；v978e 加逐标的破年线兜底（首版 `_regBear` 空表 → 静默失效）。规则卡 W3 行、注册表 W3、`docs/SIGNAL_INVENTORY.md` 14.10、README 三节已同步（结论按实测改写为「零差异」）。
  - **未验证的假设**：①减速零差异的原因未定位（探针 1468/2708 返回 0.5 但成交无标签，疑被 `_gateOK`/`_v1OK`/cash 先截断）；②窗口层（3/5/10 年）出现的 +0.27/+1.26/+0.11 差异与六段零差异不自洽；③今日 C0 与 v976 基线漂移 0.1–0.8pct 未查明。
  - **下一步 + 别碰**：下一步＝在 `tryBuy` 入口打日志逐笔核 40–96 笔（区间用六段常量），再把减速改到建仓侧 `bearSlowBuild`。别碰 `btRun` 主体与 `_navToday()`；跑前写 cfg + reload。

### 2026-11-18 · 回测区间代表性三层矩阵（层1 分段 / 层2 长寿极端 / 层3 滚动）· **已交接（只跑实验 + 文档，产品代码零改动，页面仍 v971c）**
- 改了什么：`docs/SIGNAL_INVENTORY.md` 新增第 14 节（三层全部数字与结论）；README「当前进度 / 下一步」各加一条。**未动** `edit_work/index.html` 一字、未发布。
- 新增资产：无新脚本（全程用线上页面 `?t=reg1..reg4` 驱动 `btRun`，自选回测走 `localStorage` `pool/customCodes` 预设后重载生效）。
- 未验证的假设：①2015-02→2016-01 段的 4 只权重（35/25/25/15）是人为设定、非档位目标，方向性参考；②层3 只跑池0/池10，未跑「纪律全关」，故 T7/T16 的 3 年分布仍缺；③5/10 年滚动只在市场代理层面算过、未进引擎；④口径为 20bps（默认 fee0 下年化约高 0.1–0.2pct）。
- 下一步：等用户拍板三件事（见 README「下一步」首条）。若要做「三列报告口径」，改 `SIGNAL_REGISTRY` 加 `bullAnn/bearAnn/bearDD` 三字段 + 规则卡加列，属产品改动，须先升版。若要下调 V11 池比例，改 `btCfg()` 默认 + 迁移键即可（回滚点 `6bd6a69f`）。
- 别碰：`btRun` 引擎与 `fw2_v971_nav_today` 的 `_navToday()`（买入/卖出日估值唯一真源）；`localStorage['fw2_bt_cfg_v1']` 里 `pool='custom'` 是实验残留，重载后已恢复 `pool='barbell' / start 2019-01-01 / end 2026-09-28 / feeBps 0 / v11Pct 10`（若发现不是，别急着改代码，先看缓存）。
### 2026-11-18 · v971 V11 参数重定「池 10%·赔率 2.5」+ 修买入日估值假回撤 · **已发布 `0549cb46fb81566378b37cc420bc81b8fe6502aa`（4,688,045 B，线上核验 PASS 15/15 + 反向 7/7、BYTE_MATCH True）**
- 改了什么：`edit_work/index.html` ①**修 bug**（tag `fw2_v971_nav_today`）：权益估值原用 `s.lastNav`，而它只在日循环开头对「当天之前已有持仓」刷新，当天新买仓位按前一日净值/0 计价 → 买入日权益少一注、制造等于 4×单注＝池比例的假回撤（池 10%/15% 长区间 −10.00%/−15.00%，恰在 2019-01-02 首日建仓）。新增 `_navToday(code)`（优先 `s.seq[d].nav`、缺值回落 `lastNav`），`pv`/`bv` 与 `P.snp` 同法。②`btCfg()` 默认 `v11Pct: 10, v11Odd: 2.5`（单注 25 / cap4 不变），一次性迁移 `fw2_v970_v11_on` → `fw2_v971_v11_p10b`（同时对齐 `v11Bet=25 / v11Max=4`，清掉补测期 20/30 残留）；抽屉两处默认、注册表 `fw2_v971_v11`、规则卡 V11 行、抽屉表头、徽标同步。**默认口径变为短 19.71/2.27/39.84、长 8.62/1.14/30.93**（fee0；fee20 为 19.63/2.24/40.18 与 8.52/1.11/31.21）。
- 新增资产：`_navToday`；localStorage `fw2_v971_v11_p10b`；脚本 `D:\Temp\_api_push_page_v971.py`、`D:\Temp\_verify_v971_api.py`；诊断链 `D:\Temp\_v971_diag_analyze.py`、`_v971_diag_artifact.py`、`v971_diag_*.json`；截图 `D:\Temp\v971_local_drawer.png`、`v971_local_rule_v11b.png`、`v971_online_drawer.png`、`v971_online_rule_v11.png`。
- **2026-11-18 拍板**：用户回「A」→ V11 默认 池 10%·赔 2.5·单注 25%·cap4 确定，B/池 15% 作废。代码 v971c 即 A 口径，无需再改；若后续想试 B，只需改 `btCfg()` 的 `v11Pct: 10` + 迁移块 `fw2_v971_v11_p10b` 内 `v11Pct`（两处），其余不动。测试用的线上 `fw2_bt_cfg_v1` 已恢复默认，接手者不必再清理。
- **A/B 最终对照（20bps，同会话复测，含绝对回撤）**：基线 16.48/2.14/34.84（−6.97%）· 7.59/1.06/28.39（−5.68%）；B 池5·赔2.5 18.07/2.20/37.53（−7.51%）· 8.06/1.09/29.68（−5.94%）；A 池10·赔2.5 19.63/2.24/40.18（−8.04%）· 8.52/1.11/31.21（−6.24%）。A 比 B 多赚 1.56／0.46pct、多承受 0.53／0.30pp 回撤。**纠错**：旧记录 fee20 长「8.75/1.11/32.35」为跨会话残留，同会话复跑两次均 8.52/1.11/31.21，已在 index.html / README / SIGNAL_INVENTORY 三处改正，线上 commit `6bd6a69f26b6b4327023387f8a162a59361beff4`、BYTE_MATCH True。
- 未验证的假设：①fee0 下「池 10%·注 20%」长区间未跑（缺数字，只有注 25/30 等价结论）；②「注 25 与注 30 长区间逐位相同」解释为「cap4×30%>100% 池、现金先耗尽」，**未逐笔核流水验证该解释**；③fee20 长区间年化（8.75）略高于 fee0（8.62）属路径依赖，**未做归因**；④跨设备/多浏览器各自残留的 `v11Bet` 差异只在本机验证过。
- 下一步：用户强刷 `?t=v971live` 核五项（徽标 v971 / 抽屉池 10 赔率 2.5 且默认勾选 / 规则卡 20 条开 10 关 10 + V11「● 开·证据 A」含假回撤说明 / 默认短 19.71-2.27-39.84 与长 8.62-1.14-30.93 / 旧缓存自动纠回 10-2.5-25-4）。若用户要回保守方案（池 5%·赔率 2.5），只改 `btCfg()` 两个默认 + 迁移块两个值。
- 别碰：`_navToday`（改回 `lastNav` 会重现假回撤，且会影响所有历史数字）；`v11Pct` 收参的 `isFinite` 分支（允许 0 做不变式自检）；`fw2_v971_v11_p10b` 键名；`fw2_bt_ovr` 默认必须是 `{}`。

### 2026-11-18 · v970 V11 狙击升默认开 · **已发布 `cd0219cae18898532e63b8a9377ce6a3bb4be576`（4,686,319 B，线上核验 PASS 14/14 + 反向 5/5、BYTE_MATCH True）**
- 改了什么：`edit_work/index.html` 把 `btCfg()` 默认改 `v11Gate:true / v11Pct:5`（其余 `v11Odd 2 / v11Bet 25 / v11Max 4` 不变），新增一次性迁移 `fw2_v970_v11_on`（纠回 v968/v969 补测残留的 `false/10`，打标后不再覆盖）；注册表 V11 `def`=on、`act` 写新数字、`code`→`fw2_v970_v11`；规则卡 V11 行改「v970 起默认开」并写锁 5% 的理由；抽屉池输入默认 5、标签含「单注＝池 25%、最多 4 仓」、表头说明改写；徽标 v970。**默认口径变为短 18.26/2.19/38.05、长 8.19/1.08/30.59**（相对 v969 基线 +1.63/+0.56pct、Calmar +0.03/+0.01、回撤预算 +3.31/+2.36pp），规则卡「共 20 条，开 10 / 关 10」。
- 新增资产：localStorage 标记 `fw2_v970_v11_on`；脚本 `D:\Temp\_api_push_page_v970.py`、`D:\Temp\_verify_v970_api.py`；截图 `D:\Temp\v970_local_drawer.png`、`v970_local_rule_v11b.png`、`v970_online_drawer.png`、`v970_online_rule_v11.png`。
- 未验证的假设：①「两区间 Calmar 都不低于基线」是相对**fee 0** 口径，20bps 成本下 V11 的边际（狙击往返多、成本更高）**未重测**；②池 5% 之外的参数仍用 v969 单次扫描值，未做「池 5% × 赔率 1.5/2.5/3 × 单注 20/30」的二维确认；③`fw2_v970_v11_on` 迁移只在本机浏览器验证过，未验证多设备/多浏览器各自残留的差异。
- 下一步：用户强刷 `?t=v970live` 核五项（徽标 v970 / 抽屉默认勾选且池 5 / 规则卡 20 条开 10 关 10 + V11「● 开·证据 A」/ 默认短 18.26-2.19-38.05 与长 8.19-1.08-30.59 / 旧缓存自动纠回）。**下一步建议**：把 fee 20bps 下的 V11 重测补上（费用对狙击这类高频往返策略影响应比 T7 大得多），结论再决定是否保留默认开。
- 别碰：`fw2_v970_v11_on` 键名；`v11Pct` 收参的 `isFinite` 分支（允许填 0 做不变式自检，别改成 `|| 5`）；`fw2_bt_ovr` 覆盖口（实验用，默认 `{}`；跑完记得 `removeItem`）。

### 2026-11-17 · v969 V11 补测 + 修正「最多 4 仓」上限 · **已发布 `842f17bc35866e755c7fc5c5f4492c6bd360686a`（4,685,452 B，线上核验 PASS 16/16 + 反向 5/5、BYTE_MATCH True）**
- 改了什么：`edit_work/index.html` 给狙击段补两条守门——`Object.keys(P.snp).length >= _SNP.max` 仓数上限（**v968 文档写了 4 仓但代码没有**）与 `P.snpDone[c7]` 一次性入场；新增 cfg 键 `v11Max/v11Den/v11Once`（`v11Bet` 原已存在）与 `localStorage['fw2_bt_ovr']` 覆盖口；ATR 预计算顺带算 `_s.lo20/_s.lo60`，赔率分母三选一（`atr` 默认 / `leg20` / `leg60`）；注册表 V11 `code→fw2_v969_v11` 与 def/modeled/thr/act 全换新、规则卡 V11 行换新数字并注明旧记录作废、抽屉勾选框标签补「最多 4 仓」、徽标 v969。
- 新增资产：`_SNP.max/den/once`、`P.snpDone`、`_s.lo20/_s.lo60`、`fw2_bt_ovr` 覆盖口（`{v11Bet,v11Max,v11Den,v11Once}`）；脚本 `D:\Temp\_api_push_page_v969.py`、`D:\Temp\_verify_v969_api.py`。
- 未验证的假设：①v968 记录 20.74 与本次 cap10 复跑 21.04 差 +0.30pct/−13pp，理论上应等价，**未做残差归因**（按作废处理）；②「一生一次」与「可再入场」逐位相同 → 推断区间内无二次入场样本，**未逐笔核狙击流水**；③池 10%/15% 长区间回撤 50%/75% 的成因（仓数 vs 品种）未拆解。
- 下一步：用户强刷 `?t=v969live` 核四项（徽标 v969 / 抽屉 V11 标签含「最多 4 仓」/ 规则卡 V11 行新数字且「○ 关·证据 A」/ 默认 16.63/2.16/34.74、20 条开 9 关 11；勾 V11 池10% 应得 19.72/2.20/41.29）。然后**待拍板：V11 是否启用「池 5%·赔率 2·单注 25%·最多 4 仓」**（唯一两区间 Calmar ≥ 基线、回撤 +3.3/+2.4pp）。
- 别碰：`fw2_bt_ovr` 默认必须是 `{}`（跑完实验记得 `localStorage.removeItem('fw2_bt_ovr')`）；`_SNP.max` 上限 10；`v11Bet` 保留 5–50 校验；`P.snpDone` 只在买入成功后写（写在判定前会把整只标永久封死）。

### 2026-11-17 · v968 V11 狙击（筛选池独立仓位池）· **已发布 `d4dc3fb3a8f91daceeab30763ca581972f013946`（4,680,113 B，线上核验 PASS 22/22 + 反向 3/3）**
- 改了什么：`edit_work/index.html` 新增 `cfg.v11Gate/v11Pct/v11Odd/v11Bet`；V11 开时筛选池 40 只入 `seriesBy`（只入序列、`targetAmt=0`），按 `v11Pct` 从预算切出 `P.snpCash`、杠铃目标按 `1−pct` 缩放；独立账本 `P.snp` 做狙击仓（止损入场净价 −3×ATR、浮盈 ≥20% 后吊灯＝峰值×0.85），入场条件赔率＝(P250−nav)/(3×ATR14) ≥ `v11Odd`，单注＝池 25%；`p250` 守卫放到 `cfg.addDD || cfg.v11Gate`，新增 `_s.atr`；权益曲线并入 `P.snpCash` 与 `P.snp` 市值；流水档位列对狙击成交显示「狙击池」；规则卡第 20 行、抽屉两个输入、注册表 V11 `ev` C→A。
- 新增资产：`_SNP`、`P.snp`、`P.snpCash`、`_s.atr`、drawer `btIn_v11Gate/btIn_v11Pct/btIn_v11Odd`。
- 未验证的假设：①ATR14 是「近 14 日平均绝对日收益 × 当日净值」的近似，**不是真实波幅（无 OHLC）**；②赔率分母固定 3×ATR，与用户原话「回撤腿」未逐字对齐；③「卖出后可再入场」未与「一生一次」做过对照；④单注 25% / 最多 4 仓 / 池 10% 未做参数扫描（只测了 10%·赔率2 与 5%·赔率3 两组）。**（②③④ 已于 v969 补测钉死，见上一条；另发现「最多 4 仓」当时代码未实现，v968 的 20.74/67.92 已作废。）**
- 下一步：发布 → 线上核验（徽标 v968 / 抽屉 V11 勾选框与两个输入 / 规则卡 20 行 V11「○ 关·证据 A」/ 默认 16.63/2.16/34.74；勾 V11 短区间应得 20.74/1.41/67.92）→ 用户强刷。**批 2 到此全部结案**，下一批进批 3。
- 别碰：`P.snp` 必须与 `P.pos` 隔离（塞进 `P.pos` 会被 T7/T16/止盈/刹车误伤）；`P.snpCash` 必须计入权益（漏掉短区间年化掉到 3.08）；筛选池序列进 `allDays` 必须按 `[start,end]` 过滤（否则区间被拉回 2007）。

### 2026-11-17 · v966 V1/V2 + v967 表头 · **已发布 `5223f8709ec0` / `5326808561a9`**
- 改了什么：`edit_work/index.html` 加 20 日年化波动率与近 250 样本分位（`_s.vol/_s.vrk`）、`_v1OK` 恐慌过滤挂在 T7 补仓、`cfg.v1Gate`、抽屉勾选框、规则卡第 18/19 行、注册表 V1 `ev` C→A / V2 标观察型；表头补 V1 说明。
- 未验证的假设：①波动率分位用「20 日年化波动率在自身 250 个样本里的位置」，与信号层「≥80 分位」的具体口径（未见实现，筛选页无 V1 行）尚未逐字对齐；②V2 判不成交只靠代码检索（注册表 + 无成交分支），未跑「假装成交」的对照。
- 下一步：批 2 只剩 V11（狙击，单列最后）。V11 要 ATR/赔率/吊灯止损，得先定门限与样本口径。跑完批 2 再进批 3。
- 别碰：`_v1OK` 缺样本时返回 false（设计如此，宁缺勿滥）；`_s.vrk` 只在建表条件下才有值，别在未开 `v1Gate/stGate/trendGate` 的路径里直接读。

### 2026-11-17 · v964 S-TREND + v965 等级修复 · **已发布 `ee8246e439f3` / `00856e7065c0`**
- 改了什么：`edit_work/index.html` 加 MACD 与 `_gateOK`（trendGate+stGate 可叠加）、`cfg.stGate`、抽屉勾选框、gate 覆盖建仓/T7 补仓/定投/网格；注册表 S-TREND `ev` C→A、`modeled`=已建模；规则卡第 17 行；等级查表回落 A/B 组 ID。
- 未验证的假设：①MACD 以首日净值起算 EMA（上市初期的前 26 日柱值偏粗糙，未与行情软件逐点对齐）；②gate 拦截后 T7 档位标记 `pp.t7Lvl` 不推进，等于「破位期不再补、解除后只补一档」，这是我有意取的保守口径，未做替代方案对照。
- 下一步：V1（波动赶底，250 日回撤 ≤−25% 且波动率 ≥80 分位，只 near 不成交）→ V2（强势延续/波动赶顶）。两区间 × fee 0/20 照旧；新开关必须让两区间数字变化（v953 验收条件）。
- 别碰：`_gateOK` 的两开关判断顺序（trendGate 先、stGate 后）不要合并成一条 AND 条件，否则两开关同时开会互相污染口径；`s.macd` 只在建表条件成立时才存在，读取必须先判空。

### 2026-11-17 · v963 W3/S4 趋势确认 · **已发布 `ef8a9c66c935`**
- 改了什么：`edit_work/index.html`：MA 表加 `m60`、建表条件加 `cfg.trendGate`；每日循环加 `pp.buildPend` 延后建仓分支；建仓处加 gate 判定；cfg/收参/抽屉勾选框/规则卡第 16 行；注册表 W3/S4 ev C→A、def 标注两区间均负。
- 未验证的假设：延后建仓期间该标的的现金是否被计入「已投」分母未逐项核对（`pp.invested=0` 的处理会影响策略年化分母）；MA20/MA60 用等权净值均值（与信号层同口径），未做复权差异核对。
- 下一步：做 S-TREND（趋势破位 + MACD 绿柱）→ V1（波动赶底）→ V2；两个区间 × fee 0/20 的 A/B 照旧。
- 别碰：`pp.buildPend` 只允许建一次；`_SG.maS` 固定 20（年线用 `l`=MA200），勿把 MA60 写成 `s`。

### 2026-11-17 · v962 T7 升默认开 + W2/S2 结案 · **已发布 `2ad11a9e99e8`**
- 改了什么：`edit_work/index.html`：`btCfg()` `addDD: true` + 迁移 `fw2_v962_t7_on`；注册表 T7 def/act、W2/S2 ev/def/modeled 改写；规则卡 T7 第四列默认开、脚注与抽屉表头同步；徽标 v962。
- 未验证的假设：W2/S2 的「等价 T7」判断基于阈值逐项相同（wDD1=−20/wDD2=−30 与 addDD1=20/addDD2=30），未逐只核对信号页触发口径（同标的池不同）。
- 下一步：强刷 `?t=v962live`；然后建 W3/S4 趋势分支（多头排列 gate）——需在引擎买入路径上加「未满足 MA20/MA60 则延后建仓」的开关。
- 别碰：`fw2_v962_t7_on` 标记（缺了会重新覆盖用户手动取消）；T7 规则卡第四列 `!!_cv.addDD`。

### 2026-11-17 · v961 规则卡 T7 行口径统一 · **已发布 `9369cb3057f8`**
- 改了什么：`edit_work/index.html` T7（回撤补仓）规则卡 hint 整句改为含成本重测口径；删残句「年化 」与旧括注「长区间 Calmar 持平（弱正）」。
- 未验证的假设：无（仅文案，数字取自 v960 实测）。
- 下一步：强刷 `?t=v961live` 看规则卡 T7 行文案；随后拍板 T7 是否升默认开。
- 别碰：T7 hint 里已写明「v960 重测」，勿再引批 1 的 16.20/7.83（那是 T16 关口径）。

### 2026-11-17 · v960 T9 取消封顶 + 单边成本模型 + T7 重测 · **已发布 `fffe36e164a0`，线上核验 PASS**
- 改了什么：`edit_work/index.html`：T9（组合投入封顶）六处下线（引擎守卫/抽屉勾选框/cfg 键/规则卡行/注册表/信号页 lvl）；新增 `cfg.feeBps` 单边成本（`tryBuy`/`trySell`/对照侧三处注入，默认 0）；抽屉「纪律开关」块加成本输入框；徽标 v960。
- 新增资产：`D:\Temp\_api_push_page_v960.py`、`_verify_v960_api.py`、截图 `v960_online_drawer.png` / `v960_online_concl.png`。
- 未验证的假设：①成本模型只作用于回测引擎，实盘执行与「策略 vs 对照」逐只表已同源，但未做逐只重算核对；②feeBps 上限 200bps 为人为区间，超限静默回落 0。
- 下一步：强刷 `?t=v960live` 核徽标 v960、抽屉四开关 + 成本框、规则卡「共 15 条」、默认 15.78、成本 20bps 时 15.65；然后拍板 **T7 是否升默认开**（数据见 README v960 条目）。
- 别碰：`btIn_feeBps` 元素 id（go() 直接读它）；「纪律开关」块的拼接顺序（成本行紧跟 T2 行）。

### 2026-11-17 · v958 T2 回退默认关（撤销 v957）· **已发布 `16c3174429a9`，线上核验 PASS**
- 改了什么：`edit_work/index.html`：`btCfg` 恢复 `tpPeak: false`；删 `fw2_v957_t2_on` 迁移块，加反向迁移 `fw2_v958_t2_off`；注册表 T2 `def`=off、规则卡 hint/脚注/抽屉表头同步；徽标 v958。
- 新增资产：`D:\Temp\_api_push_page_v958.py`、`D:\Temp\_verify_v958_api.py`、截图 `v958_online_drawer.png` / `v958_online_concl.png`。
- 未验证的假设：①老用户若在 v957 期间手动取消过 T2，v958 的迁移同样把 false 写成 false，行为无差；②若某账号 v957→v958 之间从未加载页面，则缓存里仍是旧 false，迁移只是打标。
- 下一步：强刷 `?t=v958live` 核徽标 v958、抽屉 T2 未勾 + T16 勾、规则卡 T2「○ 关」、默认短 **15.78/2.02/35.17**、长 **7.32/0.97/29.55**。
- 别碰：`fw2_v958_t2_off` 键名；`tpPeakArm/tpPeakDD` 白名单；T2 在「一天一笔」链中的位置（止损之后、止盈档之前）。

### 2026-11-17 · v957 T2 峰值回撤止盈默认打开 · **已发布 `29c71bd94044`，线上核验 PASS**
- 改了什么：`edit_work/index.html`：`btCfg` 默认 `tpPeak: true`；新增一次性迁移 `fw2_v957_t2_on`；注册表 T2 `def` = on；规则卡 T2 行 hint 改「v957 起默认开；实测仍劣于不用」；脚注与抽屉表头同步；徽标 v957。
- 新增资产：`D:\Temp\_api_push_page_v957.py`、`D:\Temp\_verify_v957_api.py`、截图 `v957_online_drawer.png` / `v957_online_concl.png`。
- 未验证的假设：①“默认开”只在未改过本地缓存的新环境/已迁移环境成立；②T2 与 T7 回撤补仓的互斥仍沿用 v671 的「买类降档」逻辑，未针对 T2 单独复核。
- 下一步：强刷 `?t=v957live` 核徽标 v957、抽屉 T2+T16 两勾、规则卡 T2 行「● 开」、默认短区间 **11.55/1.74/28.69**、长 **5.97/0.85/25.91**。
- 别碰：①迁移键名；②`tpPeakArm/tpPeakDD` 白名单；③想回更优口径就回滚到 `1ef1c13c0ac4`（v956）。

### 2026-11-17 · v956 同标的一天最多一笔卖单（显式化）· **已发布 `1ef1c13c0ac4`，线上核验 PASS**
- 改了什么：`edit_work/index.html`（tag `fw2_v956_one_sell_a_day`）：卖出链加 `daySoldD` 记账；T2 分支加「今日已卖则让位」守卫并在成交后记 `daySoldD`；T16 分支加 `daySoldD !== d`；注册表 T16 `act` 与规则卡脚注写死优先级链；徽标 v956。
- 新增资产：`D:\Temp\_api_push_page_v956.py`、`D:\Temp\_verify_v956_api.py`、截图 `v956_online_default.png`。
- 未验证的假设：①「一天一笔」在 T2 关闭时对默认口径无影响（已由逐位相同的数字旁证）；②T16 卖出后破位减半基准在 T2 卖出后仍被重置（新基准=当日净值），这条行为沿用未改；③跨标的同日多笔卖出不受限制（本来就该各卖各的）。
- 下一步：强刷 `?t=v956live` 核徽标 v956、默认 15.78/2.02/35.17、脚注优先级链；如需复算同日重复，看 `btTradeBody` 里同日期同标的只应有一行卖出。
- 别碰：①`daySoldD` 记在止盈链之后；②T2 成交要记 `daySoldD`；③T16 不回写 `lastSellNav`；④T2 默认仍关。

### 2026-11-17 · v955 同日多卖出优先级＝D（T2 优先）· **已发布 `076f69984d2f`，线上核验 PASS**
- 改了什么：`edit_work/index.html`（tag `fw2_v955_same_day_d`）：日循环先算 `_t2today`（T2 判据同源，顺手推进 `peakGain`），两条止盈分支加 `!t2today` 守卫；止损分支未动；注册表 T1/T2 `act` 补同日口径；规则卡脚注补优先级链「止损＞T2＞止盈档＞T16」；徽标 v955。
- 新增资产：`D:\Temp\_api_push_page_v955.py`、`D:\Temp\_verify_v955_api.py`、截图 `v955_online_default.png` / `v955_online_t2on.png`。
- 未验证的假设：①D 只在「T2 开」时有意义，T2 仍默认关，所以默认口径零变化；②T2 触发当日止盈让位后，**次日若 T2 已卖半、止盈档仍满足才会补卖**，这条路径未逐笔核对流水；③止损与 T2 同日同标的时止损先清仓，属实现既定行为（非本次新增）。
- 下一步：强刷 `?t=v955live` 核徽标 v955、默认 15.78/2.02/35.17、勾 T2 后 11.55/1.74/28.69、脚注出现优先级链。
- 别碰：①`_t2today` 必须在止盈链前算；②止损分支别加 `!t2today`；③T2 默认仍关。

### 2026-11-17 · v954 T16 卖出后破位减半升为默认开 · **已发布 `6a0d5dc01ed6`，线上核验 PASS**
- 改了什么：`edit_work/index.html`（tag `fw2_v954_t16_on`）：①`btCfg()` 默认 `postSellHalf: true`；②合并 localStorage 后加一次性迁移（旧缓存里的 false 是批 1 实验残留，首次加载回 true 并打标，用户主动取消后不再覆盖）；③注册表 T16 `def=on`、`modeled` 注明 v954；④规则卡脚注同步。
- 新增资产：迁移键 `localStorage['fw2_v954_t16_on']`；核验脚本 `D:\Temp\_verify_v954_api.py`；截图 `D:\Temp\v954_online_t16_default.png` / `v954_rule_t16_on3.png`。
- 未验证的假设：①T16 与 T2/止盈/止损**同日多笔卖出的优先级仍未定义**（本次未改）；②T16 用「最近一次卖出成交净值」作基准，卖出后又买入的情形需人工复核（信号层已有提示，回测里不回写）；③无手续费/滑点，T16 增加的卖出笔数真实成本未计入。
- 下一步：线上强刷 `?t=v954live` 核：徽标 v954、抽屉五勾选仅 T16 选中、规则卡「共 16 条，开 8 条 / 关 8 条」且 T16 行 `● 开 · 证据 A`；**新基线＝短 15.78/2.02/35.17、长 7.32/0.97/29.55**。
- 别碰：①迁移键名不要改；②`postSellLo/postSellWin` 仍在收参白名单；③T16 卖出那笔不回写 `lastSellNav`（否则一路追着卖）；④`check_html_comments` 期望 **230 处**。

### 2026-11-17 · v953 批 1 五条纪律进引擎 + 两区间实测 · **已发布 `e1d0645989f3`，线上核验 PASS**
- 改了什么：`edit_work/index.html`（tag `fw2_v953_batch1` / `fw2_v953_discipline` / `_t7` / `_t2_t16` / `_t9` / `_t10`）：cfg 新增 14 键（5 开关 + 9 阈值，默认全关）+ 归一化、pos 记账位、`s.p250` 预计算、`trySell` 记卖出基准、`_capHit`（建仓/定投/网格三处守卫）、T2/T16 与 T7 两个逐日循环、新函数 `btSlotRebal`（季末调用）、抽屉「纪律开关」5 勾选框 + 收参 5 布尔 **与 9 阈值**、规则卡 R1–R11 → **16 行**、R8 三小步（默认关 + 注册表注明四档均负 + T14「仅提示，不触发成交」）。文档：`docs/SIGNAL_INVENTORY.md` 新增 **11.7 节**（五条实测表 + 四条结论 + 踩坑）。
- 新增资产：无新数据源；`docs/SIGNAL_INVENTORY.md` 11.7 与 README v953 条目为新增文字。探针脚本 `edit_work/_mk_probe.py` / `_mk_probe2.py` 与副本 `_v953_probe.html` 用完即删（可再生的做法写在 11.7「踩坑」段）。
- 未验证的假设：①截图通道 **GAC 本轮全程超时**（`bu.screenshot` / 元素裁剪 / `cu` 桌面都失败），**未取真渲染截图**，只用 DOM 尺寸核对（5 个勾选框宽 483、无溢出；规则卡 16 行、列宽 40/281/92/46 与模板一致）——**待下一位补一张**；②T7「一档＝目标额 20%」是本轮自定假设（清单原文只说「补仓」未给量）；③T2/T16 与 T4 止损、止盈链同一天可能各卖一笔，**同日多笔卖出的优先级未定义**；④T9 只用「Σ成本」口径测过，「Σ市值」口径未测。
- 下一步：①已发布 —— **已推线上**（commit `e1d0645989f3`，blob `742148a8`，4,659,874 B），`D:\Temp\_verify_v953_api.py` 报 `ONLINE_V953=PASS`：BYTE_MATCH True、must 12/12、gone 3/3、Pages CDN 已出 v953；②真渲染截图**已补**（通道后来恢复）：`D:\Temp\v953_discipline.png` / `D:\Temp\v953_rule16.png` / `D:\Temp\v953_rule16c.png`——抽屉 5 勾选框全不勾、规则卡头「共 16 条，开 9 条 / 关 7 条」、T16/T9/T10 三行带「证据 A + 实测数字」、阈值单源脚注完整；③③等用户拍板 T16 是否开默认。
- 别碰：①`c.tpPeakArm/tpPeakDD/addDD1/addDD2/addAmt/postSellLo/postSellWin/capAmt/slotBand` 这 9 个阈值必须留在收参段——删掉就会退回「勾了开关但数字不变」的坑；②`btSlotRebal` 与 `btRebalance` 是两套（档位 vs 单只），别合并；③T16 卖出那笔**不能**回写 `lastSellNav`（否则一路追着卖）；④`check_html_comments` 期望已到 **230 处**。

### 2026-11-17 · R8 破线动作四档实测（只跑实验，生产未改）· **三档全负，三小步已随 v953 落地**
- 改了什么：**`edit_work/index.html` 一字未改**（仍 v952 / 4,643,506 B / `cc0fbcb9ae91`）。产出写进 `docs/SIGNAL_INVENTORY.md` **第 11.6 节**（四档 × 两区间表 + 四条结论 + 口径提醒）。两个实验副本 `edit_work/_t14_r8_half.html` / `_t14_r8_rebuy.html` **已删除**。
- 新增资产：`D:\Temp\_make_t14_r8.py`（生成两档副本：H＝`maPend` 恒 `'half'`；R＝清仓后重站 MA200 连 3 日解锁并重置建仓游标）。**没有**新增数据源或字段。
- 未验证的假设：①「回补」只试了「重站 MA200 连 3 日」一种节奏，未试「即日回补」或「连 1 日」，**回补节奏未做敏感性**；②四档都是「刹车关」口径，**不能**与 14.07%/1.81/34.40%（刹车开）混比；③回测**无手续费与滑点**模型，39/85 次来回的真实成本未计入（方向上只会更差）；④「9 笔清仓来自 MA20」仍是推断，未逐笔核。
- 下一步 + 别碰：等用户拍板三小步——①确认 R8 默认不被参数恢复逻辑自动勾上；②`SIGNAL_REGISTRY` 的 `R8.act` 加注「四档均负，仅供研究」；③T14 文案补「仅提示，不触发成交」。**别碰**：①`_SG.on = !!cfg.sigYear && !cfg.sigBrake`（年线与刹车互斥）与 `pp.sigOff` 一旦置 true 就永不回补，这是现口径，别在没有实验依据前改生产；②`cut: 0.5` 与 `maS: 20` 硬写死，要可调得先加输入框；③跑实验务必用副本、跑完即删，别把实验开关留在生产文件里。

### 2026-11-17 · T14 年线 MA200 vs MA250 首测（只跑实验，生产代码未动）· **等是否转 R8 动作分解**
- 改了什么：**`edit_work/index.html` 一字未改**（仍 v952 / 4,643,506 B / commit `cc0fbcb9ae91`）。产出写进 `docs/SIGNAL_INVENTORY.md` **第 11.5 节**（六组数字 + 三条结论 + 未核实项），11.4 批 1 表把 T14 划掉、改成「R8 破线动作分解」。实验副本 `edit_work/_t14_ma250.html` **已删除**（生成器留在 `D:\Temp\_make_t14_ma250.py`，改完即弃）。
- 新增资产：`D:\Temp\_make_t14_ma250.py`（把 `sigMa: 200`→250、`c.sigMa = 200;`→250、徽标加 `·MA250`，命中数不符即 abort）。**没有**新增数据源或字段。
- 未验证的假设：①「9 笔清仓全部来自 MA20 破线」是按规则文本推断（`maS: 20` 与 `sigMa` 一样在 `_SG` 里硬写死、无 UI 开关），**未逐笔核对交易明细**；②年线关的基准 15.38%/1.74/39.66%（短）与 7.53%/0.87/34.30%（长）是「刹车关」口径，与本日之前 14.07%/1.81/34.40%（刹车开）不是同一组参数，**不可混用比较**；③`btIn_*` 参数会跨会话恢复（localStorage），所以复跑前必须显式确认 `sigYear`/`sigBrake` 两个勾选态，否则会串味。
- 下一步 + 别碰：下一步建议跑 **R8 破线动作分解**（提示 / 减半 / 只冻不卖 / 清仓可回补，四档同区间），复用 `bkExitAct` 的 `freeze|exit` + `bkHalfOff`/`bkStopOff`，新分支最少；期望回答「清仓不回补值不值」。**别碰**：①`_SG.on = !!cfg.sigYear && !cfg.sigBrake` —— 年线与刹车**互斥**，同时勾时刹车优先、年线根本不生效（这是判读结果的前提）；②`c.sigMa = 200` 与 `maS: 20` 都是硬写死，想让用户可选得先加输入框，别在收参处改默认值绕过去（会把 v933 口径悄悄改掉）；③`BRAKE_T` 仍单源；④复跑记得两区间同向才算证据，单区间好就落默认＝违规。

### 2026-11-17 · v952 交易逻辑单源 SIGNAL_REGISTRY（B1）+ 止盈定乙 + 回测规则卡 11 条 · **已发布并核验**
- 改了什么：`edit_work/index.html`（徽标 **v952**，4,643,506 B，commit `cc0fbcb9ae91`）——①新增 `window.SIGNAL_REGISTRY`（59 条，紧随 `SIGNALS_CFG`，字段 `name/layer/obj/dir/ev/def/modeled/thr/act/code`，**阈值一律从 `SIGNALS_CFG` 拼串引用、不复制字面数字**）+ `signalRegOf(sig)`；②T1 止盈文案「卖1/3」→「减1/4，+20% 再减1/4」（定乙），证据等级 C→A；③回测页「当前生效的规则」3 条 → **R1–R11 全量清单**（含默认关），每行「本次开/关（按 `res.cfg||cfg` 实时算）」+「证据 A/B/C」徽标，标题改「本次回测执行的规则」；④`rows.meta` 三条占位（T6/T11/W4）清空，信号页「未启用…」提示消失；⑤`ruleCard` 保留未删（无引用）。
- 新增资产：`D:\Temp\_api_push_page_v952.py`（发布）、`D:\Temp\_verify_v952_api.py`（线上核验，锚点 7 条 + 反向 5 条）、截图 `D:\Temp\v952_rule_list.png`。文档 `docs/SIGNAL_INVENTORY.md` 仍 v2（第 8 节止盈拆解、第 11 节四类划分、第 12 节架构决定）。
- 未验证的假设：①注册表 59 条的 `thr` 文案是**逐条手写拼串**，只有 `SIGNALS_CFG` 值变时才自动跟随，**字段名/层级关系在改 cfg 时不会自动校验**——一致性断言脚本尚未写（第 12 节 B1 后续项）；②`gate.py --check` 本轮跑 >5 分钟未出结果（疑似卡网络刷新，已 TaskStop），**闸门未拿到绿**，本轮只用 `check_js` + `check_html_comments` + 真渲染 + 线上字节一致兜底；③R3 网格行显示的「宽基3%/进攻5%/对冲1.5%/3%」是分组阈值文本，未在窄视口逐组核；④`dripAmt/dripDays` 是否死参数**仍未核实**。
- 下一步 + 别碰：接手跑 `check_js.py`（20 块 ALL OK）、`check_html_comments.py`（期望 **229** 处 0 隐患）；线上强刷 `?t=v952live` 核徽标 / T1 文案 / T6·T11 提示消失 / 规则卡 11 行。**别碰**：①注册表是唯一准绳，新增信号必须同时补注册表与 `_rList`，**不得抄字面阈值**；②`BRAKE_T` 仍单源、`SIGNALS_CFG` 值本轮未改；③`_SG.on`/`_SG.bk` 互斥不改；④批 1 回测（T14 + T2/T7/T16/T9/T10）**尚未开跑，等用户点头**；⑤逻辑库独立模块未开工。

### 2026-11-17 · v951 回测页「按标的明细」提到刹车卡上面 · **已发布**
- 改了什么：`edit_work/index.html`（徽标 **v951**，4,620,759 B，tag `fw2_v951_bt_brake_below_cmp`）——纯显示顺序调整、零计算改动。①面板层（运行条之后）删除 `brakeCardHtml({ctx:'bt'})`，原位留说明注释；②结果区 `out.innerHTML` 改成 `… + cmpHtml + brakeCardHtml({ctx:'bt'}) + gridListHtml + ruleHtml + …`，即 结论条 → **策略 vs 对照明细表 → 单只刹车卡** → 备用金明细 → 当前生效的规则 → 四图 → 明细；③`if (!res)` 无有效数据分支同样追加该卡（静态阈值表不因回测失败消失）；④卡内副标题「勾选下面的刹车开关」改为「勾选上方参数抽屉里的刹车开关」；⑤徽标 v951 + 长注释。
- 新增资产：补丁脚本 `D:\Temp\_apply_v951.py`（5 处精确替换，命中数不符即 abort）；备份 `D:\Temp\index_v950_pre_v951.html`（回滚首选）；截图 `D:\Temp\v951_bt_order_local.png`。
- 未验证的假设：①刹车卡改为「结果渲染时才出现」——**首屏在「正在跑组合模拟…」那一瞬没有这张卡**，本轮只在跑完后断言过，未为「未运行/跑挂了」另加占位（`if (!res)` 分支已兜住）；②自选回测是用临时勾入 012920 + 016452 两只验的（`top=1208/1724`），未验「自选池为空以外的极端组合」（0 只时无结果区，属既有行为）；③窄视口（538×643）下刹车卡 6 列仍会折行（与改前同一窄视口一致，属既有行为）。
- 下一步 + 别碰：接手跑 `check_js.py`（期望 20 块 ALL OK）与 `check_html_comments.py`（期望 228 处 0 隐患）；线上强刷 `?t=v951live` 进「策略执行 → 持仓回测 / 自选回测」核 明细表在刹车卡之上、副标题写「上方参数抽屉」。**别碰**：①`brakeCardHtml` 只接受 `ctx`，阈值只在 `BRAKE_T` 一处，别把数字抄进卡里；②别在面板层再插第二份（会双份）；③资产配置页的 `brakeCardHtml() + peCardHtml()` 卡序是另一套，改回测页不要顺手动它。

### 2026-11-16 · v950 修正 016452 / 020712 成本记错（69.8 归因）· **已发布 commit `2646371fdbf8`**
- 改了什么：`edit_work/index.html`（徽标 **v950**，4,619,397 B，tag `fw2_v950_cost_2fix`）+ `edit_work/holdings-data.json`——用户「继续」。016452 `cost` 140.00→**60.96**（`unitCost` 5.2711→2.2943）、020712 `cost` 190.03→**200.99**（`unitCost` 1.3127→1.3884），两份文件同改并写 `costSrc`；说明行硬编码「约 69.8 / 约 1.2」改为语义化「舍入差，已逐只核对到 ±0.x 级」。**零公式改动**。
- 新增资产：归因脚本 `D:\Temp\_attribute_6979.py`（逐只偏差排序）、`_pre_fix_cap.py`（CAP 阈值与修后 Σ 预演）、`_fix_cost_v950.py`（json + seed 对象级精确替换）、`_apply_v950.py`（徽标/注释/文案）、`_verify_v950_api2.py`（API 分块回读核验，绕过 raw CDN）、`_diff_online_local.py`；备份 `D:\Temp\index_v949_pre_v950.html`、`holdings_v949_pre_v950.json`；截图 `D:\Temp\v950_kpi.png`、`v950_hold.png`。
- 未验证的假设：**「016452 / 020712 的账户隐含成本（mv − cp）就是真实已确认成本」**——依据是生成脚本 L397-398 的口径注释与 012920 流水法闭合（该只差 0.00），但这两只本身没有逐笔流水重放核对，属「按账户口径反推」而非「流水独立证实」；若要 100% 证死，需拉 016452（2026-03 卖出 13,426.72）与 020712 的全部 `trade_detail` 重放。
- 下一步：①线上强刷 `https://andylauxiaoyang.github.io/investment-workbench/caifu/index.html?t=v950live` 确认徽标 v950、未实现 **+¥1,344.80**、在盘成本 **¥19,117.39**、累计 **+¥2,224.76**；②若要根治复发，改 `edit_work/refresh_holdings_ttskill.py`：对有 `pendingBuy` 的标的加「|cost −(marketValue−constantProfit)| > 5 元 时按账户值校准并写 `costSrc`」，改完必须跑 `refresh_holdings_ttskill.py --dry-run` 比对 24 只 cost 不误伤。
- 别碰：其余 21 只 0.68 的舍入（不要再逐只凑）；`constantProfit` 的收益率分母含在途（平台口径，别自作主张去掉）；`holdProfitRate` 优先取账户值的逻辑（T1/T4/T5 依赖它）。

### 2026-11-16 · v949 累计总盈亏改走账户权威累计（实盘流水闭合）· **已发布 commit `164b581f20e8`**
- 改了什么：`edit_work/index.html`（徽标 **v949**，4,646,563 B，tag `fw2_v949_pnl_acct`）——用户「按照你建议改」。①新增 `calcAcctHoldCount()`；②`pnlSum` 改 `acctHpN > 0 ? acctHp : (realizedNet + unreal)`，累计卡从此等于账户 Σ`holdProfit`（含已实现）；③累计卡副标按口径切「账户累计收益 · 含已实现」/「已实现 + 未实现 · 估算」；④说明行把 68.63 拆成「成本口径差约 69.8 − 已实现口径差约 1.2」。其余五卡与全部 `calc*` 未动。
- 新增资产：**实盘核实脚本** `D:\Temp\_audit_012920.py`（拉 `ACCOUNT_HOLDING` 字段 + `TRADE_QUERY` 全量流水并逐笔 `trade_detail`）、`_audit_012920_calc.py`（流水法闭合计算）、`_audit_realized_all.py`（全账户卖出核实）、`_probe_trades.py`（确认 `trade_list` 是否自带金额）；明细落盘 `D:\Temp\_audit_012920_trades.json`、`_all_trades_v948.json`；备份 `D:\Temp\index_v948_pre_v949.html`；截图 `D:\Temp\v949_kpi.png`。
- 未验证的假设：①**已实证（本地 8792 真渲染 532×641）**——6 卡无折行，累计 +¥2,224.76、副标「账户累计收益 · 含已实现」、说明行 2,224.76/2,156.13/68.63 齐全。②**已实证（线上 raw）**——4,646,563 B、sha256 `e4a0d112557d8e54` 与本地一致、正向锚点 6/6、反向锚点 2/2 消失。③**未验证**——线上 DOM 仍取不到（本机访问 Pages 时 `data/*.json` 全 `net::ERR_FAILED`，`window.DB/state` 未初始化），故线上仍是「字节一致 + 本地同源真渲染」证据链，不是 DOM 级。④**本轮推断（待核实）**——本地文件体积 4,617,423 → 4,646,563 的变化来自并行刷新链重写（代码锚点未被覆盖）；若那条链仍在跑，下次发布前应重新 `Get-FileHash` 确认推送的就是当前磁盘内容。
- 下一步：①若要继续修 69.8 成本口径差：**先重建流水成本链**（逐笔 buy/sell 重放算出每只每轮的加权成本），不要直接改 `cost` 字段——016452 的 `unitCost` 已被记成 5.2711（市值 196 元），证明「清仓重建」会覆盖旧成本，用当前成本反推历史卖出会得到 −22,968 这类荒谬值（本轮已实测）。②线上补 DOM 核验：`?t=v949live` 打开后点 `[data-view=capbal]`，读 `#cbKpiRow` 应为 6 卡、累计 +¥2,224.76。③回滚 `Copy-Item -LiteralPath "D:\Temp\index_v948_pre_v949.html" -Destination "edit_work\index.html" -Force`（再往上是 `index_v947_pre_v948.html`）。
- 别碰：①**不要再用 `realizedNet + unreal` 当累计**——那是台账成本与镜像成本两套基准相加，天然少 68.63；②**不要把 69.8 摊进任何一张卡的显示值**去凑自洽（那是造假），要么修成本链、要么保留说明行；③`calcAcctHoldProfit` 与 `calcAcctHoldCount` 必须保持「只读 holdRows、不写状态」，否则会污染信号层；④并行自动链仍在写 `index.html` 时，不要跑 `gate.py --check` 全量（会被实时改写的文件打断），只推页面。

### 2026-11-16 · v948 盈亏口径标签修正：两处「盈亏」同名不同义 · **已发布 commit `6740d601ee59`**
- 改了什么：`edit_work/index.html`（徽标 **v948**，4,614,421 B，tag `fw2_v948_pnl_caliber`）——用户贴「资金平衡」截图、红框圈住「未实现盈亏 +¥1,276.69」「累计总盈亏 +¥2,156.13」，说「这个数据错了吧，我目前持仓盈利都2200多，已经实现的800多」。逐只核算 `edit_work/holdings-data.json`（syncedAt 11-16 21:36、24 只、total 21,226.69）：`ΣholdProfit`＝**2,224.76**（含已实现的累计收益，「我的持仓」表「总盈亏」列一直走它，即用户口中的「2200多」）、`ΣconstantProfit`＝**1,346.52**（持有收益·不含已实现）、`Σ(市值−成本)`＝2,041.21、`ΣpendingBuy`＝764.48、已实现＝879.44 ⇒ 资金平衡「未实现」1,276.69 与「我的持仓」2,224.76 差 **948.07 ≈ 已实现 879.44 + 68.63**。**数字没算错，是同名不同义**。仅改标签与说明、计算一律未动：①「我的持仓」表头 `总盈亏`→**`累计收益`**（title 补「含已实现盈亏与份额确认/费用」）；②「未实现盈亏」副标 `市值 − 成本`→`市值 − 成本 · 不含已实现`；③`#cbKpiAsof` 增动态口径桥（账户持有收益 Σ¥2,224.76 含已实现·勿当浮盈、与本页累计差 ¥68.63 系摊薄成本 vs 镜像成本）；④新增 `calcAcctHoldProfit()`（仅说明行取数、不进 KPI）、`holdRowOf` 两处 return 透传 `hp`。
- 新增资产：`calcAcctHoldProfit()` 函数（说明行专用汇总器，故意不接入任何 KPI，避免与已实现重复相加）；备份 `D:\Temp\index_v947_pre_v948.html`（4,612,192 B）；截图 `D:\Temp\v948_kpi7.png`（6 卡 + 新副标题 + 口径桥）、`v948_hold.png`（持仓表头「累计收益」+ 012920 +2,703.50）。
- 未验证的假设：①**已实证（本地 8792 真渲染 399×481，与线上同一份文件）**——6 卡两列无折行、副标题不溢出；未实现副标「市值 − 成本 · 不含已实现」；说明行动态输出 Σ¥2,224.76 / 差 ¥68.63；表头第 4 列「累计收益」。②**未验证（重要）**——**线上 `caifu/` 的 DOM 级核验没做成**：本机浏览器打开 Pages 后 `data/*.json` 全部 `net::ERR_FAILED`（`performance.getEntriesByType('resource')` 里这些条目是 200，但 `window.DB / state / HOLDINGS_SEED` 全未初始化），重载一次仍如此；判断为本机网络/代理受限，非页面问题。已用 raw 字节一致（4,614,421 B、sha256 前缀 `7c105ee89e9a5455`）+ 本地同源文件真渲染替代。若网络恢复，请补一次线上真渲染。③**未修的口径差（明写不掩盖）**——`Σ(市值−成本)` 1,276.69 与账户 `ΣconstantProfit` 1,346.52 差 **69.79**，来自 13 只在途买入标的的 cost 反推误差（020712 差 11、016452 差 60、其余小额）。
- 下一步：①若要修那 69.79：根因是 `holdRowOf` 的 `cost` 走对账单/加权 unitCost，而账户 `constantProfit` 以账户市值（含在途）反推，两条口径在「有 pendingBuy 的标的」上分叉；建议先写一个只读核对脚本，逐只输出 `marketValue − constantProfit` 与 `cost` 的差，确认是成本漏记还是份额四舍五入，再决定改 `refresh_holdings_ttskill.py` 还是前端。**动 cost 会牵动刹车/信号/收益率三处，必须单开版本并跑一遍回测对照。** ②线上补核 `D:\Temp\_verify_v948_online.py`（raw 已 PASS）；如需 DOM 核验，用 `?t=v948live` 打开后点 `[data-view="capbal"]` 读 `#cbKpiRow` 与 `#cbKpiAsof`。③回滚 `Copy-Item -LiteralPath "D:\Temp\index_v947_pre_v948.html" -Destination "edit_work\index.html" -Force`（再往上是 `index_v947_pre.html` 4,612,192 B）。
- 别碰：①**不要把「未实现盈亏」直接改成 ΣholdProfit（2,224.76）**——holdProfit 已含已实现（012920 实证 2,703.50 = 1,825.27 + 878.23），抬高它会与「已实现 879.44」重复计量、累计变 3,104，属造假；②`calcAcctHoldProfit()` 只给说明行用，禁止接进 KPI 或「累计总盈亏」；③`holdRowOf` 的 `mv` 是「份额×净值」（不含在途），`marketValue`（数据文件字段）才含在途 764.48——两者不可混用，混用就是本轮 948.07 这类「看起来对不上」的源头；④并行自动链 `refresh_all.py --allow-partial-publish` 可能仍在跑，若要在它活着时发布，只推页面（contents API），别去碰 `gate.py` 全量。

### 2026-11-16 · v947 红利行换中证红利 + 自由现金流补数 · **已发布 commit `e2f4595b852a`**
- 改了什么：`edit_work/index.html`（徽标 **v947**，tag `fw2_v947_mid_div_fcf`）——v946 交付后用户回「更想看中证红利」「自由现金流数据不全，补齐」。①红利行：`PX_ASSETS` 的 `hsdiv` 由「红利指数 / `sh000015` / heldBy 012761」改为「**中证红利** / `sh000922` / **无 heldBy**」——012761 是华泰柏瑞上证红利ETF联接、跟踪 000015，与中证红利非同一标的，标错持仓比不标更糟（该行持仓列现在 `—`，上证红利 PE 9.25/分位 98.4% 仍可在「分位卡」看）；`PX_PE_IDX`/`PX_DY_IDX` 的 `hsdiv` 键同步 `'000922'`。②自由现金流：`PX_PE_IDX` 增 `fcf:'980092'`、`PX_DY_IDX` 增 `fcf:'980092'`、`PX_PE_NA` 删 `fcf:'暂无源'`、`PX_PE_NA_NOTE.fcf` 与 `PX_DY_NOTE.fcf` 改为「已接东财人工快照 + 分位仅 3 年」。③分位窗口标注：`pxPeInfo()` 回传 `win`（缺省 10），`pxRowHtml()` 在 `win≠10` 时于分位格加小字「3年分位」+ tooltip；表头「10年分位」title 补「历史不足按可得样本标注」。④说明行加 amber 口径提示。⑤数据层 `refresh_mkt_snap.py`：`DJ_IDX` 增 `'000922': ('SH000922','中证红利')`（保留 `'000015'` 便于切回）；新增模块级 `STATIC_IDX`（980092 的 `pe 12.36 / pos 0.227 / win 3 / dy 0.03989 / date 2026-11-13 / manual True`，`src` 与 `dysrc` 分写）并在 `main()` 里合并进 `MKT_SNAP.idx`、遇同键活源则跳过；`pxDyInfo()` 改读 `dysrc`。
- 新增资产：`MKT_SNAP.idx` 新增 `000922`（蛋卷活源）与 `980092`（人工快照，含 `win`/`manual` 两个新字段，闸门脚本不校验这些，已确认不触发 FAIL）；脚本侧新增 `STATIC_IDX` 常量，是「蛋卷覆盖不到、但东财妙想能查」这类指数的统一入口；截图 `D:\Temp\v947_left.png`（左半：PE 9.28/88.6%、12.36/22.7%·3年分位）、`v947_right.png`（右半：4.40%/+2.75pp、3.99%/+2.34pp）；备份 `D:\Temp\index_v947_pre.html`。
- 未验证的假设：①**已实证（本地 8792 真渲染 1280×960）**——17 列 19 行；中证红利 5,589.29 / 9.28 / 88.6% / 4.40% / +2.75pp / 「股息>2×国债·股息占优」/ 持仓 `—`；自由现金流 4,890.04 / 12.36 / 「22.7% 3年分位」/ 3.99% / +2.34pp / 「持 · 现金流」；tooltip 文案（PE 单元格 src、分位小字、股息率 src、利差算式）逐条读出核对过。②**未验证**——宽屏（≥1600px）一屏是否列宽拥挤未看；本机 tab 恒 1280×960，窄视口下仍走横滚（表 1640px / 容器 961px）。③**待用户确认**——「中证红利行不挂持仓」是否接受：若希望这行也标「● 持仓」，需要换一只跟踪中证红利的基金的代码，或改成「上证红利 + 中证红利」两行并存（那就变 20 项、文案与表宽要再调）。④**口径提示**——980092 的股息率在东财有两套 `indId`（`23495` → 3.989%、`55881` → 3.836%），本轮取与 PE 同批的 `23495`；若别的平台显示 3.8% 级属口径差异。⑤**闸门插曲与最终发布路径（已解决）**——首发 `gate.py --check` 被 `DUALSOURCE` / `ACCNAV` 拦（P3 共享缓存竞态：`_hist_cache` 到 11-16、月度产物停 11-15）；备份 `D:\Temp\fund-monthly_v947pre.json` → 全量 `gen_fund_monthly.py`（81 只 / 7382 行 / 1,330,924 B）→ 两项转 PASS → `gate.py --check` GATE=PASS（11 数据集）。随后 `push_gh_v39.py` 两次仍被拦（`发布文件不一致=13` 后 `=1`），排查确认**本机有并行自动链** `refresh_all.py --allow-partial-publish`（21:32 起两个进程）在持续刷新 `data/_hist_cache` 与 `data/fund-monthly.json`、并每 6 秒推一个「数据更新（离线刷新 + 双轨发布）」commit，闸门对拍被实时改写的数据打断——与 v947 改动无关。页面侧校验全绿且已完整 `GATE=PASS` 过一次，故本轮**只推页面**：GitHub contents API 直传 `caifu/index.html` → commit **`e2f4595b852a`**（22:13），数据文件交由并行链续推。线上 raw 回读 **BYTE_MATCH True**（4,612,192 B、sha256 前缀 `30cd0a0e25e1f3ea`）、锚点 **10/10**、反向锚点 **3/3 全消失**（`D:\Temp\_verify_v947_online.py` = `ONLINE_V947=PASS`）。
- 下一步：①若怀疑数据过期：东财妙想 `mx_index_block_finance_data` 重查「自由现金流指数 980092 市盈率TTM / 股息率TTM / 3年市盈率历史百分位」，改 `refresh_mkt_snap.py` 的 `STATIC_IDX`（连同 `date`/`src`）后跑 `python -u refresh_mkt_snap.py`，期望输出多一行 `MANUAL 980092`。②**线上核验已完成**——`D:\Temp\_verify_v947_online.py` = `ONLINE_V947=PASS`：raw 与本地逐字节一致（4,612,192 B、sha256 前缀 `30cd0a0e25e1f3ea`）、锚点 10/10、反向锚点 3/3 消失（注意 raw.githubusercontent 有 CDN 缓存，核验 URL 需带 `?t=` 参数，否则会读到上一版）。③回滚 `Copy-Item -LiteralPath "D:\Temp\index_v947_pre.html" -Destination "edit_work\index.html" -Force`（再往上是 `index_v946_pre_pub.html`）。
- 别碰：①`PE_IDX_MAP`（信号层，`012761→000015`、`023917→000985`）与全景表的 `PX_PE_IDX` 是两套口径，换中证红利时**只改全景表三处**，不要顺手改信号层映射；②`STATIC_IDX` 的 `manual:True` 不要删——它是「这是人工快照、不会自动更新」的唯一标记，删了后人会把它当活源；③不要为了让 980092 的 1-20 年收益列好看而伪造月线：腾讯月线只回 1 根、东财 `push2his` 月线最早 2024-08-30（28 根），指数 2023-11 才发布，3 年收益目前无免费源；④分位 `win` 只在「历史确实不足」时传，别给正常 10 年窗口的指数也传 `win`——否则每行都会多出「N年分位」小字。

### 2026-11-16 · v946 资产监控补红利/自由现金流两项 + 股息率两列 · **已发布 commit `b3da67b0443f`**
- 改了什么：`edit_work/index.html`（徽标 **v946**，4,607,624 B，tag `fw2_v946_dy_div_fcf`）——用户贴「大类资产监控 · 全景表」截图：「这个资产监控没有红利指数和自由现金流指数监控，能否加上。且在周期指向前面加入一列股息率，再加入一列股息率与无风险利差」。①`PX_ASSETS` 在「中证1000」之后插两行：`hsdiv` 红利指数（`sh000015` 上证红利，heldBy 012761）、`fcf` 自由现金流指数（`sz980092` 国证自由现金流，heldBy 023917）；只进 `PX_ASSETS`，**不进** `PX_DAILY` / `PX_CORR_ASSET_IDS`（相关性矩阵口径不变）。②`pxTableHeadHtml()` + `pxRowHtml()` 各加两列，位置严格在「52周区间」之后、「周期指向」之前：股息率（`MKT_SNAP.idx[key].dy`，蛋卷 `yeild`×100，与 PE/分位同批同日，单元内小字标日期）、股息率与无风险利差（股息率−无风险，pp；A股用中债10Y `erp.cur.y10`、美股/港股用 10 年美债 `fx` 末点第 4 位；正红负绿，tooltip 带完整算式）。③新增 `PX_DY_IDX` / `PX_DY_NOTE` / `pxDyInfo()`；`PX_PE_IDX` 增 `hsdiv:'000015'`；`PX_PE_NA` 增 `fcf:'暂无源'` + NOTE 说明已探测三条路径。④`pxCycleAndSigs()` 增 `hsdiv` / `fcf` 分支（股息率 vs 中债10Y：≥2× 占优 / ≥1× 偏股息 / <1× 偏债券；无源写「股息率暂无源」）。⑤文案「17 项→19 项」两处 + 说明行补口径，表宽 1360→1520。⑥数据层 `refresh_mkt_snap.py`：`DJ_IDX` 增 `'000015': ('SH000015','上证红利')`，`danjuan_all()` 解析 `yeild → dy`（非 0 才写），`MKT_SNAP.idx` 每项多 `dy`；重跑活源 10/10、`updatedAt` 仍 2026-11-13。
- 新增资产：`edit_work/index.html` 内嵌 `MKT_SNAP.idx` 增 `000015` 键与全表 `dy` 字段（无新数据文件，故未动 `push_gh_v39.py` FILES / `data-ledger.json` / `_gen_data_mgmt.py` / 页面 DMCONFIG）；截图 `D:\Temp\v946_local_dy.png`（股息率+利差两列与日期小字、正红负绿）、`D:\Temp\v946_local_rows.png`（红利 3,321.96 / PE 9.25 / 分位 98.4%，自由现金流 4,890.04 / PE 与分位暂无源）；备份 `D:\Temp\index_v946_pre.html`（4,599,181 B）。
- 未验证的假设：①**已实证（本地 8792 真渲染 538×643）**——17 列 19 行、列序 …52周区间→股息率→股息率与无风险利差→周期指向…；逐行核算与算式一致（沪深300 +1.36pp / 中证500 −0.01 / 创业板 −0.38 / 科创50 −1.37 / 中证1000 −0.36 / 红利 4.42%−1.65=+2.77pp / 纳指 −4.48 / 标普 −3.89 / 恒生 −1.49）；债券商品汇率「不适用」、上证综指/日经/自由现金流「暂无源」；两行均挂「● 持仓」。②**未验证**——宽视口（2048）本机仍取不到（tab 恒 538×643），窄视口下 17 列走横滚（容器 483px、scrollWidth 1642），无挤压错位；建议宽屏再看一眼。③**口径判断（待用户确认）**——「红利指数」取的是**上证红利 000015**（与持仓 012761 同标的、项目 pe-hist 也用它），若用户想改**中证红利 000922**（蛋卷股息率 4.48%、PE 9.13），只改 `PX_ASSETS` 里 `hsdiv.qt`（`sh000922`）、`PX_PE_IDX.hsdiv`/`PX_DY_IDX.hsdiv`（`'000922'`）与 `refresh_mkt_snap.py` 的 `DJ_IDX` 三处即可。④**已知缺源**——自由现金流 980092 无合规免费估值/股息率源（蛋卷 63 指数未收录、国证官网 4 条路径全 404、中证 `indicator` 404），故该行 PE/分位/股息率/利差显「暂无源」，不臆造。
- 下一步：①线上核验已完成——raw 回读 `BYTE_MATCH True`（4,607,624 B、sha256 前缀 `a9b4a3a5713adc46`）、锚点 **10/10**、反向锚点 2/2 消失，脚本 `D:\Temp\_verify_v946_online.py`；线上 `caifu/?t=v946live` 真渲染复核 17 列 19 行、两列位置与取值全部对上（截图 `D:\Temp\v946_online_left.png` / `v946_online_dy.png`）。②若用户要改中证红利，按上一条三处替换后重跑 `refresh_mkt_snap.py`。③回滚 `Copy-Item -LiteralPath "D:\Temp\index_v946_pre_pub.html" -Destination "edit_work\index.html" -Force`（再往上是 `index_v945_pre_pub.html`；**注意**本轮另重算了 `data/fund-monthly.json`，回滚页面不会回滚数据）。
- 别碰：①`PX_CORR_ASSET_IDS`（= `PX_DAILY.concat(PX_MONTHLY)`）不要顺手把新两行加进去——矩阵项数、表头文案、月度序列装配都要跟着改，超出本次范围；②`MKT_SNAP` 是**内嵌在 index.html** 的一整行 JSON，只能由 `refresh_mkt_snap.py` 用 `raw_decode` 定位改写，不要用正则/文本替换去改它；③`danjuan_all()` 里 `yeild` 字段拼写就是蛋卷原文（不是 `yield`），改错会静默取不到值；④股息率口径是「小数×100 显示」，`dy` 存 0.0442 这样的原始小数，别在数据层先 ×100；⑤无风险利率必须按市场分组（A股中债10Y / 美股港股美债10Y），不要统一成一条——恒生/纳指用中债算出来的利差是错的。

### 2026-11-16 · v945 持仓回测 / 自选回测升为一级子模块 · **已发布 commit `725ecb4fa031`**
- 改了什么：`edit_work/index.html`（徽标 **v945**，4,599,181 B，tag `fw2_v945_bt_submodules`）——用户贴「组合回测」首屏截图、红框圈住面板内两张模式卡（「持仓组合回测 · 杠铃 11 只固定档位（原口径）」/「自选组合回测 · 自己勾基金」）并要求「这两个子模块放到策略执行下面作为一级子模块展示。名字分别改成持仓回测，自选回测」。①`#stratTabs` 的 `<button data-st="bt">组合回测</button>` 拆成两个同级 tab：`data-st="bt" data-pool="barbell">持仓回测` + `data-st="bt" data-pool="custom">自选回测`，面板仍是同一个 `stp-bt`；②`renderBacktest()` 的 `h3` 改按 `cfg.pool` 显示「持仓回测 / 自选回测」；③面板内两张 `btTab` 模式卡删除（`btTab` 函数与 `[data-bt-tab]` 绑定块保留为空转死代码）；④`switchStratTab(name, pool)` 接管切换：写 `fw2_bt_cfg_v1` 的 `pool` → 清空 `stp-bt` 触发兜底 `renderBacktest()` 重建 → 160ms 后 `__btGo()` 自动重跑；高亮改为「st 相同且 pool 匹配当前 pool」，否则两个 bt 按钮会同时点亮；⑤`bindStratTabs()` 传 `b.dataset.pool`。
- 新增资产：截图 `D:\Temp\v945_tabs.png`（4 个 tab 一行：资产配置 / 持仓回测[选中] / 自选回测 / 月度复盘 + h3「持仓回测」）、`D:\Temp\v945_tabs_custom.png`（自选回测高亮 + 勾选面板「自选组合 · 基金与逐只参数 已选 0 只」）；备份 `D:\Temp\index_v945_pre_pub.html`（4,599,181 B，回滚首选）；闸门日志 `D:\Temp\gate_v945.out`。
- 未验证的假设：①**已实证（本地 + 线上）**——本地 8792：点「自选回测」→ `active`=自选回测、`h3`=自选回测、旧模式卡 0、`btCuPanel` 出现、`pool=custom`、运行条「自选组合未勾选任何基金」；点「持仓回测」→ `active`=持仓回测、`h3`=持仓回测、`btCuPanel` 消失、`pool=barbell`、结果区 14,667 字符（自动重跑成功）；`#view-strategy` 可见文本「组合回测」出现 0 次。线上 `caifu/?t=v945live`（1280×960 宽视口）：badge=v945、tab 行 4 个、两个 tab 切换与本地逐项一致（截图 `D:\Temp\v945_online_tabs.png` / `v945_online_custom.png`）——宽视口证据本轮拿到了，v943/v944 的宽屏缺口顺带补上。②**未验证**——自选模式下真的勾几只基金跑一次完整回测（只验了空态，引擎侧未动故风险低）。③**新发现（数据侧）**——出版首发被 fund_monthly 的 `verify_dual_source` / `verify_acc_nav` 阻断：三只 QDII（012920 / 013328 / 017436）发布值停在 11-12、源重建已到 11-13（`发布文件不一致=1~3`），根因是 `PITFALLS.md#P3` 共享缓存竞态；重跑 `gen_fund_monthly.py`（**必须全量**，`--only` 只抓数不落盘）后 asOf 推到 11-15、两项转 PASS。⇒ **月度产物会随缓存漂移，发布前若 gate 报 fund_monthly 红，先重跑月度再查**。
- 下一步：①**线上核验已完成**——raw 回读 **BYTE_MATCH True**（4,599,181 B、sha256 前缀 `3ff5dc0dcfd227d0`）、锚点 **8/8**、反向锚点 **4/4 全消失**，脚本 `D:\Temp\_verify_v945_online.py`；②文档已单推（README `895dbfd84812` / INBOX `c48f68cf382e`）；③回滚：`Copy-Item -LiteralPath "D:\Temp\index_v945_pre_pub.html" -Destination "edit_work\index.html" -Force`（再往上是 `index_v944_pre_pub.html`；**注意**本轮另改了 `data/fund-monthly.json`，回滚页面不会回滚数据，asOf 仍是 11-15）。
- 别碰：①`switchStratTab` 的高亮条件不能退回 `b.dataset.st === name`——两个 bt 按钮会同时点亮；②`renderBacktest()` 里 `cfg.pool !== 'barbell'` 的 `btCuPanelHtml(cfg)` 分支不能删（自选回测面板靠它）；③`btTab` 函数与 `[data-bt-tab]` 绑定块现在是死代码（页面已无该属性元素），清理前先确认没有别处按这个属性取元素；④`_audit_plan_merge_v895.py` 的 A01/A01b/A01c 已改成「4 个 tab + 两个 bt 的 pool」，别按 v944 前的「3 个 tab」改回去；⑤回测引擎 `btRun`、参数抽屉、`fw2_bt_cfg_v1` 结构本轮一行未改。

### 2026-11-16 · v944 可投资金入口并入资产配置表标题 · **已发布 commit `c5f7a6bbb7a0`**
- 改了什么：`edit_work/index.html`（徽标 **v944**，4,596,355 B，tag `fw2_v944_budget_inline`）——用户贴图圈出「可投资金 62000」问「这个为什么会放在这里？我感觉不太合理」，随即拍板「我觉得可以删除，因为资产配置标题有括号里写了」。①删 `#view-strategy` 顶部那条 flex 输入条（连 `#stratBudgetHint`），`#stratTabs` 直接跟在 section 开头；②主表标题改为「资产配置（计划 ¥[input] · 目标 11 只）」，`input#stratBudgetIn`（84px、右对齐、placeholder＝基准金额、title 写明作用范围）内嵌其中；③`renderStratAlloc()` 开头那版「回填 + 绑定」IIFE 删除，改为 `el.innerHTML = html` → `.na` 打标 → 折叠态恢复**之后**的 `bindBudget()`；④输入**停顿 600ms 才重绘**（内嵌 input 每次重绘都会重建，逐字符重绘会丢光标），重绘后靠 **1500ms 时间窗** `__ALLOC_BUD_UNTIL__` 把焦点放回输入框、`__ALLOC_BUD_POS__` 记光标（number 类型 `selectionStart` 恒 null，实际光标落末尾＝追加输入正合适），回车 `preventDefault` + blur 并关窗；⑤清空＝存 0＝回退 `S.totalTarget` 基准（口径同 v935）；⑥文案两处：`rulesBannerHtml` 脚注「预算在「资产配置」表标题处修改」、回测预算空态「在表格标题「资产配置（计划 ¥…）」里填写」。
- 新增资产：截图 `D:\Temp\v944_top.png`（538×643 顶部：指数条 → tab → 待办 → 表标题内嵌「计划 ¥ 50000」）；备份 `D:\Temp\index_v944_pre_pub.html`（4,596,355 B，回滚首选）；闸门日志 `D:\Temp\gate_v944.out`。
- 未验证的假设：①**已实证**——改 62000 → 合计行 `62,000 / 100.00% / 4,135 / 8,270`（与用户截图口径逐位一致）；清空 → 回退 `50,000 / 100.00% / 3,335 / 6,670`；改值重绘后 `activeElement` 仍是 `stratBudgetIn`；顶部条 `gone`、徽标 `v944`。②**待核实**——宽视口（用户 2048 屏）没有截图证据：本机所有 bu tab 恒为 538×643，`bu.cdp("Emulation.setDeviceMetricsOverride")` 报 `Session with given id not found`，只能 `documentElement.style.zoom=0.55` 等效 978px 宽验证 h4 **单行**；**建议在宽窗口真机上再看一眼标题是否挤压**。③**未验证**——连续快速输入（每秒 >2 字符）跨过一次重绘的中间态没有机械化验证，只测了单次赋值 + 重绘后焦点保持。
- 下一步：①**线上核验已完成** —— raw 回读 `caifu/index.html` **BYTE_MATCH True**（4,596,355 B、sha256 前缀 `a310227bcd289bd2`）、锚点 **8/8**、反向锚点 **3/3 全消失**（`id="stratBudgetHint"` / `<span>预算在「策略执行」顶部修改</span>` / 「请先到「策略执行」页面 <b>顶部</b> 填写」），脚本 `D:\Temp\_verify_v944_online.py`；线上 `caifu/?t=v944live2` 真渲染 badge=v944、顶部预算条 gone、标题内 input `value=62000`（宽 84），改 62000 → 合计 `62,000 / 100.00% / 4,135 / 8,270`（14 列）且焦点保持（截图 `D:\Temp\v944_online_top.png`）；②文档单推 `edit_work/_push_docs_v943.py`（改 message 复用）；③回滚：`Copy-Item -LiteralPath "D:\Temp\index_v944_pre_pub.html" -Destination "edit_work\index.html" -Force`（再往上是 `index_v943_pre_pub.html`）。
- 别碰：①`btCfg()` 的 `if (!(+d.budget > 0) && typeof rulesBudget === 'function') d.budget = rulesBudget();` **要保留**——回测预算为空时仍回退读「可投资金」，删了会让老配置跑不出数；②`el.innerHTML` 之后 `.na` 打标 → 折叠态恢复的顺序不能插新代码（`_audit_alloc_color_v873` A13 卡「距 `el.innerHTML` < 900 字符」），`bindBudget()` 只能放在折叠态恢复**之后**；③HTML 注释里别写 `input` 元素的尖括号字面（`check_html_comments.py` 的 TAGLIT 规则会判隐患，本轮踩过一次，写成 `input（id=stratBudgetIn）` 才过）；④金额口径（目标＝可投资金×各档占比、合计行、占比列）本轮一行未改，别顺手动。

### 2026-11-16 · v943 资产配置主表置顶 · **已发布 commit `56ec72415949`**
- 改了什么：`edit_work/index.html`（徽标 **v943**，4,593,441 B，tag `fw2_v943_alloc_first`）——**只调拼装顺序，卡内逻辑零改动**。`renderStratAlloc()` 里 `var html = renderStratTodo() + brakeCardHtml() + peCardHtml();` 改为 `var html = renderStratTodo();`，主表 `st-card` 提到最前；末尾 `html += renderStratPlan();` 之后再补 `html += brakeCardHtml() + peCardHtml();`（两张诊断卡下移）。新顺序：**待办条（一行，仍置顶）→ 资产配置主表（口径行 + 11 行明细 + 合计）→ 策略参数存档卡 → 单只刹车卡 → 分位卡**。**闸门脚本同步**：`edit_work/_audit_plan_merge_v895.py` 的 B02 断言原本写死 `'var html = renderStratTodo() + '`，本次合法重排被它判 FAIL 并**阻断首发**（`!!! v895 定投执行融合结构审计 FAIL，拒绝发布 !!!`）；改为正则 `var html = renderStratTodo\(\)`（语义不变：待办条仍拼进同一 html 串）+ 新增 B02b（要求 `renderStratPlan()` 之后确实接 `brakeCardHtml() + peCardHtml()`），审计由 35→36 项、`PASS=36 FAIL=0`，`gate.py --check` 复跑 **GATE=PASS**。
- 新增资产：截图 `D:\Temp\v943_top2.png`（顶部：待办条 → 资产配置表 + 口径行）、`v943_after_table.png`（表尾：合计行 → 存档条 → 刹车卡 11 行）、`v943_alloc_zoom.png`（zoom 0.55 全表）；备份 `D:\Temp\index_v943_pre_pub.html`（4,593,441 B，回滚首选）。
- 未验证的假设：①**已实证**——合计行改前（线上 v942）与改后（本地 v943）逐位一致：`合计 | 100.00% | 50,000 | 100.00% | 3,335 | 6,670 | 20,724 | +14,054 | 41.45% | +29,276 | +58.6%`；主表 14 列 14 可见行几何断言 `misaligned=0`；块顺序实测 y/h＝待办 308/64、主表 380/1795、存档 2185/64、刹车卡 2248/691、分位卡 2952/711。②**待核实**——只在本机 538×643 视口与 zoom 0.55 下核过；用户 2048 宽屏的列宽表现未直接截屏（窄视口下 colgroup 百分比会挤压折行，属 v942 既有行为）。③**未做**——「月度复盘」tab 的卡片顺序未动（本轮只动资产配置页）。
- 下一步：①**线上核验已完成**——raw 回读 `caifu/index.html` **BYTE_MATCH True**（4,593,441 B、sha256 前缀 `788d2ab4c0712241`）、锚点 **7/7**（`verBadge v943` / `fw2_v943_alloc_first` / `var html = renderStratTodo();` / `html += brakeCardHtml() + peCardHtml();` / `fw2_v942_bk_freeze_log` / `bkFreezeDays`），核验脚本 `D:\Temp\_verify_v943_online.py`；线上 `caifu/?t=v943live` 真渲染 badge=v943，块顺序 y/h＝待办 308/64、主表 380/1795、存档 2185/64、刹车卡 2248/691、分位卡 2952/711，合计行与本地逐位一致（截图 `D:\Temp\v943_online_top5.png`）；②**文档已推**——README blob `6e3a141f13ae`、INBOX `43cb56e59122`（`edit_work/_push_docs_v943.py`）；③若要回滚：`Copy-Item -LiteralPath "D:\Temp\index_v943_pre_pub.html" -Destination "edit_work\index.html" -Force`。
- 观察留痕（**非缺陷，勿重复排查**）：线上页面在 bu 的 538×643 窄视口 tab 里「滚动之后再截图」会出现主体空白，同视口下**旧版 v942 页面同样空白**（`D:\Temp\v942_cmp_scrolled.png`），本地 127.0.0.1 同视口滚动截图正常 ⇒ 属截图环境的窄视口合成问题，与本次改动无关；用户 2048 宽屏幕正常。
- 别碰：①`brakeCardHtml()` 与 `peCardHtml()` 的**定义**与会话状态不要动（本轮只动调用位置）；②`el.innerHTML` 之后那段 `.na` 打标 → 折叠态恢复的**顺序不能插新代码**（`_audit_alloc_color_v873.py` A13 卡「`classList.add('na')` 距 `el.innerHTML` < 900 字符」）；③主表 14 列 colgroup 与 `.strat-note` 口径行文案别顺手改（本轮只搬位置）；④若有人想把待办条也挪到表后——先问用户，v895「待办条置顶」是先前拍板。

### 2026-11-16 · v942 破线冻结留痕 · **已发布 commit `32262da7c1bb`**
- 改了什么：`edit_work/index.html`（徽标 **v942**，4,591,013 B，tag `fw2_v942_bk_freeze_log`）——只加计量与展示、**不改交易行为**。①引擎判定期 freeze 分支：`if (!pp.bkFrozen) { P.bkFreezeN = (P.bkFreezeN||0)+1; pp.bkFzFrom = d; pp.bkFzDays = 0; }` → `pp.bkFrozen = true`；②解冻块（重站连 3 日）命中时 push `{code,name,from,to,days,open:false}` 到 `P.bkFreezeLog` 并清 `bkFzFrom/bkFzDays`，**未命中时**在 `else` 分支 `pp.bkFzDays++` 与 `P.bkFreezeDays++`（＝「每个处于冻结的交易日」计 1）；③`curve` 构建完成后，对区间末仍冻结的标的补一段（`to`＝区间最后一日、`open:true`）；④`res.stats` 新增 `bkFreezeN` / `bkFreezeDays` / `bkFreezeFund` / `bkFreezeLog`；⑤结论条 freeze 分支「（破线冻结 N 次 · K 只标的 · 合计 M 只·日，不产生清仓成交）」、运行条「减半 X 笔 / 冻结 N 次（M 只·日）」、触发明细表头「· 冻结 N 次 / M 只·日」；⑥明细下新增可折叠「破线冻结记录（N 次 · K 只 · 合计 M 只·日）」表（标的 / 冻结起 / 解冻日 / 天数 / 结束方式）+ 脚注；⑦exit 口径的共用句从「停加与破线冻结期间…」改为「停加与清仓锁定期…」。
- 新增资产：截图 `D:\Temp\v942_concl2.png`（结论条 36 次/10 只/1003 只·日）、`v942_fzlog2.png`（冻结记录表终版）、`v942_fzlog.png`（改版前对照）；备份 `D:\Temp\index_v942_pre_pub.html`（4,591,013 B）；脚本 `D:\Temp\upd_readme_v942.py`。
- 未验证的假设：①**已实证**——freeze 短区间 14.07/1.81/预算 34.40 + 4 笔减半与 v941 逐位一致；冻结 **36 次 / 10 只 / 1003 只·日**，逐段 Σ＝1003 且结论条·运行条·表头三处一致；`exit` 短 13.85/1.55/39.63（10/32）逐位同 v940 且**不渲染**冻结块。②**待核实**——「只·日」算法＝每个（标的×冻结交易日）记 1，同一标的多段各自累加；未用独立脚本从 `fund-daily.json` 重算 36 段的 from/to 做交叉校验。③**未做**——长区间（2017-05-07→2026-09-28）的冻结留痕未跑（结构同源，仅短区间已核）。
- 下一步：①**线上核验已完成**——raw BYTE_MATCH True（4,591,013 B、sha256 `0b23c40c70dd0014`）、锚点 13/13；`caifu/` 真渲染 freeze 得 14.07/1.81/34.40 + 4 笔减半，结论条「冻结 36 次 · 10 只标的 · 合计 1003 只·日」、表头同数字、记录表 36 行，与本地逐位一致（`D:\Temp\v942_online_fzlog.png`）；②②文档单推（README + INBOX），复用 `edit_work/_push_docs_v941.py` 改 message；③若要看长区间：`btIn_start` 改 2017-05-07 重跑，核对冻结次数与「长区间 5 笔减半」是否相容。
- 别碰：①判定期 freeze 分支仍**不能 return**（一 return 减半档就停）；②**天数计数只能放解冻块的 `else` 分支**——放到达标分支会漏掉「已破线但在等重站」的日子（本轮已踩：012761 一段 2024-05-24→05-29 曾只记 1 天，改后 3 天）；③明细里读的是 **`S`（＝`res.stats`）不是 `res`**（`res` 顶层没有这些字段，误读会显示「冻结 0 次」，本轮已踩一次）；④运行条仍只能写纯文本。

### 2026-11-16 · v941 破线动作改「冻结买入」（退役清仓，用户拍板 A）· **已发布 commit `80fa8b77d9b7`**
- 改了什么：`edit_work/index.html`（徽标 v941，4,584,530 B，tag `fw2_v941c_bk_freeze`）——①`btCfg()` 默认对象尾部 `bkExitAct: 'freeze'` + 归一化（非 `'exit'` 一律 `'freeze'`）；②`_SG` 透传 `bkExitAct`；③`P.pos` 加 `bkFrozen: false`；④判定期分叉：破线达标后 `if (_SG.bkExitAct === 'exit') { pp.bkPend = 'exit'; return; }` 走旧清仓路径，否则 `pp.bkFrozen = true`（**不卖、不清 `sigOff`**）；⑤紧随的解冻块 `if (_below) pp.bkRst = 0; else pp.bkRst++; if (pp.bkRst >= 3) { pp.bkFrozen = false; pp.bkRst = 0; }`，**不 return**（保证减半档继续工作）；⑥定投 `_sigMute` 加 `pp.bkFrozen`、网格买入条件加 `!pp.bkFrozen`；⑦`go()` 收参 `c.bkExitAct`；⑧抽屉加 `sel('bkExitAct','破线动作',[freeze / exit])`，「清仓判据」→「破线阈值」、「本次回测不清仓」→「本次回测关闭破线动作」、勾选标题改「连 2 日破 MA200 冻结买入 · 重站连 3 日解冻」；⑨结论条 / 运行条 / 刹车触发明细表头与脚注 / 明细表 hint / 刹车卡页脚 / 长说明② / 灰字全部按 act 分叉（freeze 不再显示「N 笔清仓」「买回间隔」）。
- 发布与线上核验（**已完成**）：commit `80fa8b77d9b7`（只含 `caifu/index.html`）；raw 回读 **BYTE_MATCH True**（4,584,530 B、sha256 `9c748b16e853565e`）；12/12 锚点命中；线上 `caifu/` 真渲染 freeze 口径 **14.07/1.81/34.40 + 4 笔减半 / 0 清仓**，与本地逐位一致。
- 新增资产：`D:\Temp\v941c_ab.json`（freeze vs exit × 两区间）、`v941c_drip.json`（定投口径 4 组）；截图 `D:\Temp\v941c_drawer2.png`、`v941c_conclbar.png`；备份 `D:\Temp\index_v941_pre_pub.html`（4,584,530 B）；策略文档 `策略大脑_v2.0_刹车与分位规则_待确认.md` §2 / §3 表头 / §4 整节 / §6 步 6 / §8 已同步为「冻结买入」口径。
- 未验证的假设：①**已实证**——`bkExitAct='exit'` 短 13.85/1.55/39.63（10 减半/32 清仓）、长 5.39/0.52/36.44（9/74）**逐位等于 v940 线上基准**（零回归）；`freeze` 短 **14.07%/1.81/预算 34.40%（maxDD −6.88、水下 97、4 减半/0 清仓）**、长 **5.18%/0.56/31.85%（maxDD −6.37、水下 830、5 减半）**。②**推断（待核实）**——一次性口径下 `freeze` 与 v941「清仓整档关」组逐位等价（已建满仓 + gridExt 关无网格可拦，冻结没有可拦的买入），故 A 的实盘价值只在定投/网格场景；drip 对照仅作方向（短 10.19%/1.00/−8.60 vs 3.88%/0.26/−8.86；长 4.24%/0.20/−13.22 vs **−3.45%/−0.13/−39.17**），未逐笔核对。③**未做 → 已由 v942 补上**（`fw2_v942_bk_freeze_log`：结论条 / 运行条 / 触发明细表头显示「冻结 36 次 · 10 只标的 · 合计 1003 只·日」，并新增可折叠「破线冻结记录」表）。
- 下一步：①线上核验：仿 `edit_work/_verify_online_v940.py` 建 v941 版（锚点需含 `bkExitAct` / `bkFrozen` / `bkCoolN` / `bkCoolLeft` / `_bkStAdj` / `bkStopOff` / `bkHalfOff`），并到 `caifu/` 真渲染核 freeze 结论条 14.07/1.81/34.40；②文档单推：`edit_work/_push_docs_v940.py` 改 commit message 后复用（README / INBOX）；③若要补「冻结留痕」：引擎加 `S.bkFreezeN` / `S.bkFrozenDays` 并在触发明细表头显示，**不要动 trades 结构**。
- 别碰：①判定期 `freeze` 分支**不能 return**（一 return 减半档就停）；②解冻与清仓复位共用 `bkRst`，改任一侧都要看 `bkCoolLeft` 的递减顺序（冷却只在 `exit` 口径有意义）；③运行条仍只能写纯文本（`textContent` 赋 HTML 会字面显示，v941 已踩过一次）；④不要把 freeze 的 14.07 说成「策略升级的收益」——它主要来自「少卖」而非「多赚」，与 v941「清仓关」是同一条数据。

### 2026-11-16 · v941b 清仓冷却期实验 · **本地已改、门禁绿、实验跑完、未发布**
- 改了什么：`edit_work/index.html`（徽标**仍 v940**，tag `fw2_v941b_bk_cool`，4,579,336 B）。①`btCfg()` 默认对象尾部加 `bkCoolN: 0` + 归一化（1..250 取整、非法/缺省回 0）；②`_SG` 透传 `bkCoolN`；③`P.pos` 初始化加 `bkCoolLeft: 0`；④清仓执行处（`pp.sigOff/ bkHalf/ bkRst/ bkSt` 归零之后）加 `pp.bkCoolLeft = _SG.bkCoolN || 0`；⑤复位段先 `if (pp.bkCoolLeft > 0) pp.bkCoolLeft--;`，**解禁条件由 `pp.bkRst >= 3` 改为 `pp.bkRst >= 3 && pp.bkCoolLeft <= 0`**，解禁块内 `bkCoolLeft = 0`（冷却期 `sigOff` 保持 true，建仓/网格/定投自然全被拦，单点改动）；⑥`go()` 收参 `c.bkCoolN`；⑦抽屉在「不『减半』」后加 `清仓冷却` 下拉（0/20/40/60/120 个交易日内不买回）+ 灰字；⑧结论条 / 运行条加实验口径提示；⑨**自纠 v941 遗留 bug**：运行条是 `textContent = runSum`，v941 写进去的 `<b>` 标签会字面显示（当时只核了结论条），本轮四处改纯文本 `※实验口径：…`。
- 新增资产：`docs/v941b_清仓冷却期实验.md`（设计 + 表 A 冷却梯度 × 两区间 + 表 B 清仓单档 + 结论 6 条 + 口径警示 + 复现 + 待拍板三选一）；原始数据 `D:\Temp\v941_cool_short.json`（短 5 组）、`v941_cool_long.json`（长 5 组）、`v941_cool_onlyexit.json`（清仓单档 6 组）；截图 `D:\Temp\v941b_drawer_cool.png`、`v941b_concl_cool.png`、`v941b_conclbar_cool.png`。
- 未验证的假设：①**已实证**——`bkCoolN=0` 零回归：短 13.85/1.55/39.63（10/32）、长 5.39/0.52/36.44（9/74）逐位等于 v940 线上基准。②**已实证**——冷却梯度两区间共 10 组 + 清仓单档 6 组：**全部单调变差**（短年化 13.85→13.73/13.28/12.41/10.16，长 5.39→5.06/5.00/5.01/4.12；maxDD 短 7.93→8.04/8.52/8.08/8.04，长 7.29→7.47/7.87/7.47/7.64）；清仓笔数短 32→25/21/18/15、长 74→59/46/40/32。③**推断（未逐笔核对）**——「冷却切断的循环是正贡献」是从「笔数腰斩 + 年化/Calmar/maxDD 同步变差」反推，未逐笔列出被冷却取消的买回笔与其后续净值变化；若策略层要求更硬证据，可加跑「清仓后仅按原节奏买回、不设冷却」的逐笔明细对照。④**未跑**——定投（drip）口径的冷却梯度（与 lump 不可互比，v941 已记录 drip 有 1.25%/maxDD −12.73% 病态组）。⑤**假改善已标注**——冷却 120 日档 maxDD 回到 8.04/7.64 是「仓位长期空置」换来的，不是风控起作用。
- 下一步：①复核直接跑 `http://127.0.0.1:8792/index.html?t=v941b`（工作目录 `edit_work`）→ 组合回测 → 勾刹车 → `btIn_bkCoolN` 选 0/20/40/60/120 → 运行；②**等策略层拍板后再发布**（用户 2026-11-16 明确「等策略层定了再一起发」）：备份 `D:\Temp\index_v941b_pre_pub.html` → `check_js` / `check_html_comments` / `verify_strategy_sync` / `verify_manifest` / `_audit_dm_v845` → `push_gh_v39.py`（`$env:PUSH_MSG`）→ 仿 `_verify_online_v940.py` 建 v941b 版（锚点需含 `bkCoolN` / `bkCoolLeft` / `_bkStAdj` / `bkStopOff` / `bkHalfOff`）；③待用户三选一：**A（推荐）退役清仓**（破 MA200 只冻结买入不卖出，敞口交减半档）／B 按 v941 只留减半（短 14.07/1.81/−6.88、长 5.32/0.59/−6.34）／C 维持 v940。
- 别碰：①复位段的递减顺序（必须在 `bkRst` 累加之前、解禁判定之前，否则冷却少算一天）；②运行条只能写纯文本（`textContent` 赋值，写 HTML 标签会字面显示）；③冷却期的 120 日档数字不得当作「风控改善」引用（那是空仓换来的）；④drip 口径未跑，禁止用本轮数字推断定投场景。

### 2026-11-16 · v941 刹车三档分解实验（2×2×2）· **本地已改、门禁绿、实验跑完、未发布**
- 改了什么：`edit_work/index.html`（徽标**仍 v940**，tag `fw2_v941_bk_factorial`）。①`btCfg()` 默认对象加 `bkStopOff: false` / `bkHalfOff: false` + 归一化；②`_SG` 透传两键，紧随新增 `_bkStAdj(st)` 档位压平（**顺序固定：先压 2→1 再压 1→0**，否则「两个都关」会残留 1 仍冻结定投）；③判定期 `var st4 = _bkStAdj(_brakeStOf(code, d))`、复位段 `pp.bkSt = _bkStAdj(...)`；④`go()` 收参并入两键，并把 v940 遗留的 `bkExitN` 非法回退 **1→2**（与 `btCfg` 归一化对齐）；⑤抽屉加两勾选「本次回测不『停加』」「本次回测不『减半』」+ 灰字改「三个开关可组合」；⑥结论条 / 运行条红字覆盖两键。
- 新增资产：`docs/v941_刹车三档分解实验.md`（完整 8 组 × 2 区间 + 主效应 + 只留一档对照 + 口径警示）；原始数据 `D:\Temp\v941_short.json`、`v941_long.json`、`v941_drip_short.json`（定投口径，**不纳入结论**）；计算 `D:\Temp\v941_calc.py`；截图 `D:\Temp\v941_drawer_switch.png`、`v941_drawer_switch2.png`、`v941_concl_red.png`。
- 未验证的假设：①**已实证**——三开关默认关＝零回归（短 13.85/1.55/39.63/10/32、长 5.39/0.52/36.44/9/74，逐位等于 v940）；16 组 Calmar 反算 `(ann−1.59)/|mdd|` 与页面值差 ≤0.005，无口径错位；「回撤预算用 %」＝`|maxDD|/20%×100`（与过程风险条 maxDD 同源）。②**主结论**——减半两区间改善 maxDD（+0.89／+0.77pct）与最差单月（+0.73／+0.62），代价年化 −0.90／−0.44；清仓两区间**双负**（年化 −0.73／−0.24 且 maxDD 反而深 0.89／1.18、水下多 29.5／13 天）；停加主效应落在 ±0.06pct 噪声内。③**未验证**：停加档在**一次性口径**下几无定投可冻结，属「测不到」而非「无价值」；定投（drip）口径已跑 8 组但指标不可比（结论条同屏给出「已投口径 76.74%」与「全预算口径 44.98%（最深回撤 −9.00%）」，过程条走已投口径），且出现 1.25%/maxDD −12.73% 的病态组，**禁止引用**——要判停加须另做「定投 + 绝对金额」实验。④**已纠错**：上一轮「实测回撤 31.8%–41.1% 全在预算外」是把「预算占用率」误读成「回撤幅度」；实际 maxDD 6.34–8.68%、占用 31.7–43.4%，回撤远在 20% 预算内。
- 下一步：①复核直接跑 `http://127.0.0.1:8792/index.html?t=v941a`（工作目录 `edit_work`）→ 组合回测 → 勾刹车 → 三开关组合 → 运行；②若需发布 v941：先备份 `D:\Temp\index_v941_pre_pub.html` → `check_js` / `check_html_comments` / `verify_strategy_sync` / `verify_manifest` / `_audit_dm_v845` → `push_gh_v39.py`（`$env:PUSH_MSG`）→ 仿 `_verify_online_v940.py` 建 v941 版（锚点需含 `bkStopOff`/`bkHalfOff`/`_bkStAdj`）；③三件待用户拍板：清仓档整档退役 or 改「清仓后冷却期（如 60 交易日不买回）」再测、停加是否单做定投口径实验、减半是否接受 0.44–0.90pct 年化成本保留。
- 别碰：`bkStopOff`/`bkHalfOff` 的压平顺序（先 2→1 再 1→0）不可调换；`go()` 里 `bkExitN` 回退值必须与 `btCfg` 归一化一致（都是 2）；定投口径的 8 组数字不得用于策略结论。

### 2026-11-16 · v940「清仓判据改连续 2 日破 MA200 + 国债豁免清仓」· **已发布 `919a99860c02` / 4,574,084 B / 线上核验 PASS 17/17 + 2/2**
- 改了什么：`edit_work/index.html`（徽标 **v940**，tag `fw2_v940_bk_exit_n`，**4,574,084 B**）。①`btCfg()` 默认对象 `bkExitN: 2` / `bkExitOff: false` + 归一化（`bkExitN` 取 1–5 整数、非法回 **2**；存量配置无此键自然落 2，显式存过 1 的老用户保 1）；②`_SG` 透传 `bkExitN` / `bkExitOff`；③清仓判定改 `pp.bkBelow` 连续破线计数（**站上 MA200 当日清零**），`bkBelow >= _SG.bkExitN` 才挂 exit，`bkExitOff` 可整档跳过；④`BRAKE_T['511260']` 加 **`noExit: true`**（单源自阈值表、不另建白名单）→ 国债豁免清仓；⑤`go()` 收参加 `bkExitN` / `bkExitOff`（**漏这步会只改 UI 不落库**，本轮踩过一次：跑了 N=2 结果与 N=1 完全一致）；⑥抽屉保留「清仓判据」下拉（1/2/3/5，默认 2）＋「本次回测不清仓」勾选（灰字标「实验口径（非策略）」），勾选框文案、长说明②、结论条、运行条全部同步为「连续 2 日」；⑦策略文档 `策略大脑_v2.0_刹车与分位规则_待确认.md` §2/§4/§8 同步为「已确认」。
- 新增资产：`edit_work/_verify_online_v940.py`（17 锚点 + 2 数据文件 + raw 字节比对）；截图 `D:\Temp\v940_online_concl.png`、`v940_online_drawer.png`、`v940_online_trace.png`（线上）、`v940_concl2.png`、`v940_drawer2.png`（本地）；备份 `D:\Temp\index_v940_pre_pub.html`（4,574,084 B）。未新增数据文件（四处同改规则本轮不触发）。
- 未验证的假设：①**已实证**——两区间 × 5 口径（杠铃 11 只 / 一次性 / ¥50,000 / 目标 10% / 回撤预算 20% / 无风险 1.59%）：短区间（2024-02-07→2026-09-28）全关 15.38/1.74/39.66、单日 13.14/1.40/41.13（46 清）、连2日 13.85/1.55/39.64（36 清）、连3日 13.68/1.44/42.00（34 清）、清仓关 14.07/1.81/34.40；长区间（2017-05-07→2026-09-28）全关 6.12/0.66/34.50、单日 5.03/0.45/38.56（107 清）、连2日 5.39/0.52/36.44（81 清）、连3日 5.25/0.47/38.66（75 清）、清仓关 5.18/0.56/31.85。②**已实证（v940 落地口径，含国债豁免）**——短 13.85/1.55/39.63 / 10 减半 / 32 清仓（15 笔 47%、卖飞 14 笔 +3.2%）、长 5.39/0.52/36.44 / 9 减半 / 74 清仓（38 笔 51%、卖飞 34 笔 +2.5%）；线上 `caifu/` 真渲染**逐位复现**短区间基准。③**零回归已实证**：`bkExitN=1` 仍 13.14/1.40/41.13/8/46。④**新发现（非 bug）**：线上初始跑出 13.27/1.50/38.79，根因是 localStorage `fw2_bt_cfg_v1` 里 `gridExt:true`（网格扩展开）——不是 v940 引入的差异，把网格扩展关掉即回到基准；此结论已写入 README「下一步」。⑤**未验证**：清仓关时「减半 8→4」是仓位路径变化（不清仓就没有复位后第二次减半机会），未逐笔核对，仅据笔数差异推断。
- 下一步：①若要复核，直接强刷 `https://andylauxiaoyang.github.io/investment-workbench/caifu/index.html?t=v940live`（**必须带 `caifu/`**），按 README「下一步」五处逐项核对；②若要再改清仓逻辑，**先跑 `bkExitN=1` 零回归**（13.14/1.40/41.13/8/46）再动；③剩余两件策略层待决（清仓整档是否退役 / 停加+减半整档是否重估）在 README「待决」，需用户拍板，不擅自动。
- 别碰：`bkExitN=1` 的零回归是唯一安全线；`go()` 收参必须同步两个新 key；`pp.bkBelow` 必须在站上 MA200 当日清零（只在破线分支累加会永远累计到 N、等于退化成单日）；`BRAKE_T` 只有一份（`noExit` 写在表里，不要另建白名单）；`check_html_comments` 期望已到 **215 处**（新增 1 条 HTML 注释）；回滚基准 `D:\Temp\index_v940_pre_pub.html`，上一版线上 v939 `6fd98f50a640`（4,567,817 B）。

### 2026-11-16 · v939 刹车卡进「组合回测」+ 刹车触发明细 · **已发布 `6fd98f50a640` / 4,567,817 B / 线上核验 PASS 17/17**
- 改了什么：`edit_work/index.html`（徽标 v939，tag `fw2_v939_brake_in_bt`，**4,567,817 B**）。①`brakeCardHtml(opts)` 加 `ctx`（`'alloc'` 默认 / `'bt'`），回测页在 `btRunBar` 之后、结果区之前复用同一张 11 行 6 列卡（副标题「本页只读…与资产配置页同一张表」，脚注「清仓不走这张表，见刹车触发明细」），阈值仍单源 `BRAKE_T`；②`renderBacktest` 渲染层新增「刹车触发明细」块（`bkTraceHtml`，仅 `cfg.sigBrake` 开时渲染，5 列 54 行＝清仓 46 + 减半 8，列＝日期/标的/动作/金额/下次买回（间隔·净值）+ 判定副行 卖飞·低吸·有效离场·真离场·减半·未清）。
- 新增资产：截图 `D:\Temp\v939_bt_card4.png`（本地回测页刹车卡）、`D:\Temp\v939_trace4.png`（本地明细 5 列 54 行、509px 无溢出）、`D:\Temp\v939_online_card.png`（线上刹车卡）、`D:\Temp\v939_online_trace.png`（线上明细 99 行）；`_verify_online_v939.py`（raw 字节 + 17 锚点 + 2 数据文件）、`_push_docs_v939.py`（README/INBOX 单推）；备份 `D:\Temp\index_v939_pre_pub.html`（4,567,817 B）；日志 `D:\Temp\push_v939.log`（`GATE=PASS` / `[200] caifu/index.html 4567817` / `AUDIT=PASS 36/36` / 各段 `FAIL=0`）。
- 未验证的假设：①「清仓判据改『连续 3 日破 MA200』能减少反复砍仓」——**未实测**，属推断，需加 `sigBrakeExitN` 跑对照才能证实；②「国债清仓是纯摩擦」——仅据 4 笔样本（232 日后买回 −0.3%、9 日后 +0.2%、31 日后 +0.3%），样本小，不宜外推；③已交叉核对：页面「卖飞 22 笔 平均 +2.7%」与离线 Python 逐笔统计一致；离线另算出价差成本 Σ(清仓金额 × 买回净值变化)＝**+¥5,764**（占清仓额 ¥173,212 的 +3.33%，33 笔损失 vs 7 笔保护），这是「卖→买回」价差和、**不等于**组合总收益差（全关 15.38% vs 刹车 13.14%），不能相加减；④`res.trades` 超 200 笔时流水表截断、「刹车触发明细」取全量（线上默认口径 90 清仓可完整显示），二者行数不等属预期。
- 下一步：①发布：`edit_work\push_gh_v39.py`（token `.gh_tok_tmp`，20–25 分钟，成功标志 `GATE=PASS` + `[200] caifu/index.html` + `VERIFY master head sha=…` + `AUDIT=PASS 36/36` + 各段 `FAIL=0`）；②线上强刷 `?t=v939live` 复核：回测页运行条下方出现刹车卡 11 行 + 勾刹车跑一次出现「刹车触发明细 54 行」+ 徽标 v939；③**待用户拍板**：国债是否豁免清仓（文档 §4 L120「建议豁免…待确认」，v938 未豁免）；清仓判据对照**已跑完**（见上一条 v940：连 3 日不成立、连 2 日两区间改善、清仓整档关掉更优），等三选一。**（2026-11-16 已全部闭环：v939 已发布 `6fd98f50a640`；两件待拍板见顶部 v940 条目——清仓改连续 2 日、国债豁免清仓均已落地。）**
- 别碰：`brakeCardHtml` 只接受 `ctx` 参数，别把阈值写进卡里（两页必须同源 `BRAKE_T`）；「刹车触发明细」只读 `res.trades`、不改引擎；`check_js` 期望 **20 块 ALL OK**、`check_html_comments` 期望 **214 处 0 隐患**（v938 是 213，本轮 +1）；`_SG.on` 与 `_SG.bk` 互斥仍是有意；新增数据文件仍须四处同改。

### 2026-11-15 · v938 回测接入策略 v2.0 刹车 + 清仓复位（A→C→B 的 B 段）· **已发布 `d6b8ac9966de` / 4,560,930 B / 线上核验 PASS**
- 改了什么：`edit_work/index.html`（徽标 v938，tag `fw2_v938_sig_brake`，**4,560,930 B**）。`btCfg` 新增 `sigBrake`（默认关）+ 归一化；`_SG` 加 `bk` 并与 `sigYear` 互斥（bk 优先）、预热 260→**2600**；新增逐日 10 年滑窗回撤预计算 `seriesBy[c].dd`（单调队列 O(n)）、`_brakeTh()/_brakeStOf()`、`P.pos[c].bkSt/bkHalf/bkPend/bkRst`、T+1 执行段、「收盘后刹车判定」段；`window.BRAKE_T` 导出以复用同一张阈值表；结论条/运行条各加一条刹车口径回显；`stats.bkOn/bkHalf/bkExit`。另为过发布门禁补了四处登记：`push_gh_v39.py` `FILES`（+pe-hist/+index-long）、`docs/data-ledger.json`（34→36）、`_gen_data_mgmt.py` `DMCONFIG`、页面内嵌 `const DMCONFIG`（frontN/genN 39→41）。
- 新增资产：`_upload_data_files.py`（contents API 单文件补传）、`_ledger_add_v938.py`（台账补两条，幂等）、`_verify_online_v938.py`（raw 字节比对 + 13 锚点 + 数据文件可达）；截图 `D:\Temp\v938_panel.png`、`v938_drawer.png`、`v938_online_brake.png`、`v938_online_pe.png`、`v938_online_bt.png`；日志 `D:\Temp\push_v938{,b,c}.log`；备份 `D:\Temp\index_v938_pre_pub.html`。
- 未验证的假设（**已实证四条，剩一条待核实**）：①「复位只置 sigOff 无效」已实证——11 只清仓后 0 只回到场内、年化 4.29%；修后 8 减半 / 46 清仓、年化 13.14% ✓；②`¥0.00` 假成交已实证（020712 两笔）并修 ✓；③线上刹车卡/分位卡/回测三处真渲染已实证（截图+DOM）✓；④线上同池对照已实证（关 6.36%/0.48/49.40% → 开 5.39%/0.45/41.93%，回撤预算降 7.5pct、年化让 0.97pct）✓；⑤**待核实**：`index-long.json` 已上线 200 且进清单，但页面当前**并未引用**（刹车与 MA 都用 `fund-daily` 自身净值序列），若后续要用指数口径需另行接入。
- 下一步：①线上强刷 `?t=v938live` 复核三处（刹车卡 11 行 / 分位卡 11 行且「暂缓 · 刹车优先」生效 / 回测勾刹车跑一次出现「触发 N 笔减半 / M 笔清仓」）；②若要回归门禁，跑 `_verify_online_v938.py` 期望 `ONLINE_V938=PASS 13/13 2/2`；③**待用户拍板**：46 笔清仓＝平均每只 4 次进出，是否加「复位后 N 日冷却」或「复位需回撤 < X%」缓冲；刹车卡是否也进「组合回测」tab。
- 别碰：`_SG.on` 与 `_SG.bk` 的互斥是**有意**的（同一根年线两套规则同时开会重复砍仓）；`BRAKE_T` 只有一份（页面卡片与回测共用 `window.BRAKE_T`），别在回测里再抄一份数字；`check_js` 期望 **20 块 ALL OK**、`check_html_comments` 期望 **213 处 0 隐患**；**新增数据文件＝四处同改**（FILES / `docs/data-ledger.json` / `_gen_data_mgmt.py` DMCONFIG / 页面 `const DMCONFIG`），漏一处会被 `verify_manifest` H4 或 `_audit_dm_v845` 在发布末段拦下、整段回退。

### 2026-11-14 · v935 策略执行「可投资金」改用户自填、取消 5 万硬编码 · **已发布 `14639f07c84e`**
- 改了什么：`edit_work/index.html`（徽标 v935，tag `fw2_v935_nobudget`）。`rulesBudget()` 默认 `50000`→**0** + 新增 `rulesSaveBudget`；`btCfg` 默认 `budget:50000`→**0** 且读库后 ≤0 回退 `rulesBudget()`；`#view-strategy` 顶部恢复「可投资金」输入条（`#stratBudgetIn`/`#stratBudgetHint`，写 `fw2_capital_budget_v1`）；`renderStratAlloc` 加 `_sc = total/baseTotal` 缩放（单只 `ft`、小计 `tt` 同乘），卡标题改「¥<填写金额>/基准 ¥50,000 计划」动态；`liveMonthly()` 月定投额同口径缩放；纳指补 `n100Cap<=0?'na'` 防零预算误报。
- 新增资产：`rulesSaveBudget(v)`、`fw2_capital_budget_v1` 恢复写入、`D:\Temp\v935_budget_30000.png`、`D:\Temp\v935_budget_empty.png`、`_upd_readme_v935.py`。
- 未验证的假设：①**回测抽屉 `btCfg.budget` 与可投资金是否该强制联动未定**——用户 localStorage 仍有 `budget=50000`，本轮未清，故回测行为不变；②`STRATEGY_SNAP.totalTarget` 仍为 50000，只当比例分母，未改成百分比字段（等价但少一层改造）；③滚动窗口/定投多期口径**未随新缩放重跑**（缩放只影响金额列与月定投额，收益率口径不应变，但未实测确认）。
- 发布结果（2026-11-14）：`GATE=PASS`、`[200] caifu/index.html 4535190 B`、**`master head sha = 14639f07c84e`**、`AUDIT=PASS 36/36`；线上 `?t=v935live` 徽标 v935、入口在；**旧 5 万已清**（线上 `fw2_capital_budget_v1` 删、`fw2_bt_cfg_v1.budget` 删，本地同样处理）。回测 0 预算已拦（提示「未填写可投资金，无法回测」），抽屉「5 万从零建仓」文案改「可投资金从零建仓」。验收图 `D:\Temp\v935_online_clean.png`。
- 下一步：①填可投资金后重跑回测与滚动窗口，核对缩放后收益口径是否与 v934 一致（预期收益率不变，仅金额变化）；②策略 v2.0 单只刹车卡（峰值回撤/距停加/减半差额）+ 回测接刹车 + 10 年 mdd 与 `pe-hist.json` 接入；③确认后发布：`push_gh_v39.py` 期望 `GATE=PASS` + `[200] caifu/index.html`。
- 别碰：文件里另外 47 处 `50000` 是内嵌宏观/持仓数据的数值巧合，不是硬编码；`liveMonthly` 的 `_DAILY_LIMIT`（020712 日限额）在缩放下仍返回 0，别改成非 0；清空输入框会 `removeItem` 该键（不是写 0），否则下次会被当成「填了 0」。

### 2026-11-13 · v934 C1 年线破位减半接进回测（C 组第一段）· **已发布 `234c90ad55c2`**
- 改了什么：`edit_work/index.html`（徽标 v934，3,898,247 字符 / 4,530,659 B）。`btRun` 内新增 `_SG` + 逐标的 MA200/MA20 预计算（前缀和）、T+1 待执行队列、收盘后状态机（`maSt` 1/0/-1）、破线期间暂停网格与定投、清仓后 `sigOff` 不回补；抽屉加勾选 + 口径说明；`go()` 读 `sigYear`；结论条/摘要/差异归因列同步。脚本 `_apply_v934_sigyear.py`(18) / `_apply_v934b_why.py`(2)。
- 新增资产：`cfg.sigYear` / `cfg.sigMa`、`_SG`、`seriesBy[c].ma`（逐日 `{l,s}`）、`P.pos[c].maSt/maPend/sigOff`、`stats.sigOn/sigMa/sigMaS/sigHalf/sigExit`、两条新流水 type「年线减半 / 年线清仓」、`D:\Temp\v934_page.png`、`_stitch_v934.py`。
- 未验证的假设：①**底仓+定投模式未重跑**（定投 71 期已补测：0.76% / −0.08 / 49.73%，已投 ¥22,449.30、未投 ¥30,050.70、全预算最深回撤 −2.44%）；②`MA200` 用简单净值均值、未做指数对齐（净值本身已复权，与页面「年线信号」同源），**口径一致但未与 v625 年线信号做过逐日比对**；③滚动窗口的数字是「同一 cfg 全量复制」跑出来的，未与单独手算某个窗口做过对拍。
- 发布结果（2026-11-13）：`GATE=PASS` + 10 道子审计 `FAIL=0`（`AUDIT=PASS 36/36`）；`[200] caifu/index.html 4530659 bytes`；**`master head sha = 234c90ad55c2`**；`_verify_online_v934.py` → **`ONLINE_V934=PASS`**（BYTE_MATCH True、12 锚点全中、反向 `v933`/`v931` 徽标 0 次、Pages 200 同字节 + 同尺寸）。线上真渲染：徽标 v934、运行条「年线信号 关/开」、C1 行与 6 减半 / 9 清仓均正常；**默认杠铃池 关 5.08%/0.50/35.10% → 开 0.45%/−0.42/13.54%**（伤害比 5 只自选更大）。验收图 `D:\Temp\v934_pub_online.png`（538×1286）。
- 下一步：①拍板低波动档豁免方式（P55 三选项：只留 MA200 减半 / 整档豁免 / 重回年线再接回）；②C2 峰值止盈（25% 带宽）、C3 组合回撤档加仓，随后「三档同屏」；③PE 分位仍不做、界面标注「不可回放」。线上若见异常：`Copy-Item -LiteralPath "D:\Temp\index_v934_pre.html" -Destination ...\edit_work\index.html -Force` 回 v933 后重推。
- 别碰：`_SG` 只在 `cfg.sigYear` 真时进入；预热段只进 `seq` 不进 `allDays`（P54）；`maSt` 建仓日初值；`511260`/国债/黄金被砍是口径缺陷不是 bug（P55）；线上核验别按「运行时拼接后的文案」写锚点（P57）。

### 2026-11-13 · v933 补投 + 全预算回撤对照（v932 收尾）· 已发布
- 改了什么：`edit_work/index.html`（徽标 v933）。`_perOf(dataFrom)` 让晚成立标的按成立后剩余月数分摊目标（022438 ¥3,394→¥11,000）；`stats.strat.mddFull` 另报全预算口径回撤，结论条双口径并列。脚本 `_apply_v933.py`(11) / `_apply_v933_badge.py`(1)。
- 新增资产：`stats.strat.mddFull`、`stats.hold.mddFull`、`stats.dripPeriodsFixed`、`_perOf()`、`_vSFull/_vHFull`。
- 未验证的假设：①底仓+定投模式未在补投后重跑（同一 `_perOf` 路径，按逻辑应同样投满）；②滚动窗口在补投后的胜率未重测（期数按 `hold*12` 显式传入，`_perOf` 走 explicit 分支，理论上与 v932 一致，**待核实**）。
- 下一步：C 组信号联动（年线 MA200 破位减半 / 峰值止盈 25% 带宽 / 组合回撤档加仓，T+1 成交 + 旧口径对照 + 三档同屏 + 流水标注触发源；PE 分位不做并界面标注；宏观开关仅 2018 后窗口）。
- 别碰：`btRun` 里 `_IV.explicit > 0` 的分支是滚动窗口的命门（改了会连带 39 个窗口口径）。
- 发布：`master bb75b52de6e3`；`caifu/index.html` 4,524,219 B；`_verify_online_v933.py` → `ONLINE_V933=PASS`（BYTE_MATCH True / 21 锚点 / Pages 200）。
- 数据侧（本轮顺带）：`fund-daily.json` 182,109 行 / 9,128,671 B、`fund-monthly.json` 1,330,901 B（按 P34 先日频后月频重建）；`holdings-data.json` 由主链 `refresh_holdings_ttskill.py` 刷到 2026-11-13（000746 双通道按 navDate 仲裁取东财 5.893），**持仓总市值 17,987.95 → 21,476.17**（账户金额 vs 份额×净值 差额，脚本 WARN「份额可能已变动，发新对账单核对」，属既有口径差异）。
- 发布脚本内硬卡实测：`refresh_holdings_nav.py`（旁路）不做日期仲裁，`000746` 会保留旧值导致 `C07` FAIL；必须走主链 `refresh_holdings_ttskill.py`。

### 2026-11-13 · v932 组合回测「投入方式」三选一（B 组）· 已落地本地、**未发布**
- 改了什么：`edit_work/index.html`（徽标 v932，3,892,029 字符）。抽屉「资金与区间」加投入方式（一次性/每月定投/底仓+定投，缺省一次性）+底仓比例+分摊期数；`btRun` 支持分批建仓，分母＝期末累计投入（用户拍的方案 B）；对照「买入持有」改同节奏分批；滚动窗口 39 窗口同步按已投分母。四支补丁：`_apply_v932_drip.py`(18) / `_apply_v932b_ui.py`(2) / `_apply_v932c_dotmap.py`(2) / `_apply_v932d_render.py`(5) / `_apply_v932e_copy.py`(3) / `_apply_v932f_hint.py`(3) / `_apply_v932g_rollnote.py`(1) / `_apply_v932h_rollsig.py`(2)。
- 新增资产：`stats.invested/unused/dripMode/dripPeriods/baseRatio`；`curve[].invBase/gridUsed/bInv`；`_mfByCode`（逐标的月首投点）；`btRollHtml(roll, S)` 新签名；`#btDataHint`。
- 未验证的假设：①定投下「未投到目标金额」不补投（022438 晚 2024-11 成立，只投 24/71 期、仓位 6.8%，属分批机制固有，非 bug，待用户确认是否接受）；②定投早期分母小导致回撤百分比被放大（最大回撤 −19.15% → 预算用 95.75%），是否需要另报一条「全预算口径回撤」待用户定；③`localStorage` 会记住上次 investMode（现已存成 drip），新装用户缺省仍是 lump。
- 下一步：用户确认后发布——`python gate.py --datasets fund_monthly --check`（期望 `GATE=PASS`，FAIL 走 P34 处置链）→ `python push_gh_v39.py`（期望 `[200] caifu/index.html` + `VERIFY master head sha`）→ 仿 `_verify_online_v931.py` 写 `_verify_online_v932.py`（断言 `fw2_v932_bt_invest` / `btIn_investMode` / `btIn_baseRatio` / `btIn_investPeriods` / 「投入方式」/ `_mfByCode` / `期末累计投入` / 旧徽标 v931 ×0）。
- 别碰：`btCfg` 里 `drip/dripAmt/dripDays` 三个旧死字段（保留不影响，别删以免旧配置读挂）；`D:\Temp\index_v932_pre.html` 是 v931 发布版回滚基准。

### 2026-11-13 · v931 滚动窗口测试（A 组）· 已发布 `b3384e0ab047`
- 改了什么：`index.html` 新增 `btRoll(cfg,data)` + `btRollHtml(roll)`（tag `fw2_v928_bt_roll`），`go()` 在分年度表后插入卡片；`btTargets` 加「传了 `_rollAvail` 才生效」的标的白名单；徽标 v931。每年 1 月首个交易日进场、持有 1/2/3 年，B 口径（窗口起点可得标的同档重归一，24 窗口）/ C 口径（代表池 5 只，15 窗口）。三段式渲染：结论条 + 双矩阵 + 39 行明细（13 列，横滑）。
- 未验证的假设：止损清仓后引擎不自动重建（只有季度再平衡补回）——已写进页面读法，但未单独做实验证明每个窗口都是这个原因；货基 000912 按恒 1 净值处理属引擎既有口径，未改。
- 下一步：①用户强刷 `?v=931a` 核卡片与数字（B 50.0% / C 40.0%、覆盖 50%/65%/100%）；②按 D1 进 B 组「投入方式」（一次性/定投/底仓+定投，`btCfg` 的 `drip/dripAmt/dripDays` 是死字段，需改 `btRun` 建仓段）；③再进 C 组「信号联动」。
- 别碰：滚动窗口的 `gridExt=false`（预算内口径）、`_rollAvail` 的条件生效、日历「只取非货基日期」、跑赢三态判定。回滚基准 `D:\Temp\index_v928_pre.html`（= v927 发布版 4,496,286 B）。


### 2026-11-13 · v923 回测页整页中式配色 · 已改待发布
- 改了什么：9 处翻转（摘要卡差值 / 副表差值 / 净值图回撤区 / 水下面积 / 月度柱 / 归因条 / `_pColor` / 风险 chips / 月度图文案），规则＝正红负绿零灰；tag `fw2_v923_bt_page_cn_color`，徽标 v923。另修 `_pColor` 0 值染色→中性灰。
- 未验证的假设：结论条状态色、流水动作类型色未动（判断为「状态/分类」语义，不是盈亏）；若用户要求全改，属另一轮改动。
- 下一步：发布后线上强刷 `?v=923a` 核色；回滚基准 `D:\Temp\index_v922_backup.html`（发布前需先落地该备份）。
- 别碰：图表系列线色（品牌蓝/灰/琥珀）、报错红字、`CHART.up/down` 常量定义。

### 2026-11-13 · v922 明细表配色改中式（盈利红 / 亏损绿）· 已发布
- 改了什么：`_oC` 由「正绿负红」翻转为「正红 `CHART.up` 负绿 `CHART.down`」；回撤策略列（逐只 + 合计）由红改绿；表头 hint 改写（红＝策略更好 · 绿＝策略更差）；tag `fw2_v922_bt_cn_color`，徽标 v922。仅动「策略 vs 对照 · 按标的明细」一张表。
- 新增资产：`_apply_v922_cn_color.py` / `_stitch_v922.py`；交付图 `D:\Temp\v922_table.png`。
- 未验证的假设：其它表（分年度 / 档位阈值 / 流水 / 按标的汇总）仍是国际惯例（正绿负红），与明细表不一致 —— 用户只点了这张表，故未扩改；是否需要全页统一待拍板。
- 下一步：线上强刷 `?v=922a` 核色值（正则/取色即可：正数 `rgb(185,28,28)`、负数 `rgb(4,120,87)`）；若要全页统一，搜 `CHART.bad` / `okCol` 在 renderBacktest 内的其余用法逐处翻转。
- 别碰：结论条状态色（达标绿/未达标红，属状态语义）；备用金的 `#b45309` 琥珀；对照列与波动列的中性灰（刻意弱化）。

### 2026-11-13 · v921 逐只 Calmar 统一扣无风险利率 · 已发布
- 改了什么：`perFund` 的 `calS/calH` 从 `年化/|回撤|` 改为 `(年化−rfUsed)/|回撤|`（rfUsed＝cfg.rf，抽屉「无风险利率」1.59%），脚注 ④ 改写；tag `fw2_v921_bt_calmar_rf`，徽标 v921。
- 新增资产：`_apply_v921_calmar_rf.py` / `_stitch_v921.py`（拼接几何 LEFT=10 TOP=6 H=423 CW=506）；交付图 `D:\Temp\v921_table.png`。
- 未验证的假设：改抽屉无风险利率后逐只与合计是否同步变——代码上同取 `cfg.rf`，但未实测换值（只验了默认 1.59%）。
- 下一步：线上强刷 `?v=921a` 核 Calmar 两列与脚注 ④；若要看换 rf 的效果，把抽屉无风险利率改成 3.0 重跑，逐只与合计应同时下移。
- 别碰：组合级 `stats.strat/hold.calmarS`（本就是严格口径，未改）；其余 22 列与合计行金额。

### 2026-11-13 · v920 组合回测「策略 vs 对照」改按标的明细 23 列宽表 · 已发布
- 改了什么：`btRun` 返回新增 `perFund`（逐只资金流 + 策略/对照两套收益·年化·回撤·Calmar·波动 + 差异归因）；`renderBacktest` 把原 9 行主表换成 23 列宽表 + 合计行 + 7 条脚注（tag `fw2_v920_bt_detail`，徽标 v920）；顺带把 `stats.buyAmt/sellAmt` 从取整 `t.amt` 改为精确 `t.raw`（消除 0.09 累计误差）。
- 新增资产：`_apply_v920_bt_detail.py` / `_fix_v920.py` / `_fix_v920b.py` / `_fix_v920c.py` / `_chk_v920_post.py` / `_stitch_v920.py`；交付图 `D:\Temp\v920_table.png`（1850×412 四段拼接）；备份 `D:\Temp\index_v919_backup.html`。
- 未验证的假设：①自选组合（`pool=custom`）下 `perFund` 的对照侧仍按各只 `targetAmt` 算——等权满仓时 `targetAmt=budget/n`，与 `stats.hold` 一致，但「固定百分比」「缺档留现金」两种权重下未逐项验证；②差异归因只描述触发过的操作类型，不解释金额差来源（如备用金加仓时点造成的差）。
- 下一步：线上强刷 `?v=920a` 核徽标与合计行四个金额（应可手算闭合：`43496.56 + 36717.91 − 60000 = 20214.47`）；再切「自选组合回测」勾 3 只跑一遍，确认 `perFund` 行数与摘要「建仓 N 只」一致。
- 别碰：「对照口径细节」副表（`cmpSub`，仍用 `rN/rT`）；净值曲线 / 持仓过程四图 / 流水 / 按标的汇总；`#btOut` 第 7 张表首列两金额粘连属 v909 既有缺陷，本轮未修。

### 2026-11-13 · v919 删除「真实持仓口径」回测模式 · 已发布（head `a695d45338e9` / 4,446,350 B）
- 改了什么：抽屉 `sel('mode')` 下拉整项移除、改静态口径说明；`btRun` 删 `ledgerBy`/`realFirst` 分支与台账为空拦截；`go()` 删 `btIn_mode` 读取；`btCfg` 合并后强制 `mode='fixed'`（tag `fw2_v919_drop_real`，徽标 v919）。
- 新增资产：无（纯删除 + 一行说明；`_chk_v919.py` 为临时残留检查脚本）。
- 未验证的假设：删掉「真实持仓口径」后，历史上基于该口径得出的对比结论（如早期「真实口径 4.36% vs 固定 5.08%」之类记录）都失去复现入口 —— 若以后要追溯，只能去 git 历史或 v918 备份里找实现。
- 下一步：线上已复核（徽标 v919、抽屉无「模式」下拉、持仓组合 5.08% 零回归）。若要恢复该模式，从 `D:\Temp\index_v918_backup.html` 取回 v351 实现。
- 别碰：`LEDGER_KEY` / 「交易台账」页（回测不再读台账，但台账本身仍要维护）；`btIn_pool` 四个选项与 v918 自选组合面板。

### 2026-11-13 · v918 组合回测拆「持仓组合 / 自选组合」双入口 · 已发布（head `0eb3e0c1af38` / 4,446,323 B）
- 改了什么：`renderBacktest` 顶部两个 `[data-bt-tab]` 入口卡；`btCuPanelHtml` 三池勾选面板（`btCustomUniverse` 把 持仓 23 / 自选 3 / 筛选 40 合成 66 项）；`btTargets` 新增 `custom` 分支（等权满仓 / 固定百分比两口径）；预置三键（杠铃 11 只 / 自选池 / 清空）；tag `fw2_v918_bt_custom`。
- 新增资产：`_apply_v918_bt_custom.py`（15 处精确替换）、`_patch_docs_v918.py`；六个函数 `btEnsureScreenPool / btCustomUniverse / btCuState / btCuSelected / btCuListHtml / btCuPanelHtml`。
- 未验证的假设：「等权满仓」「默认空选」是我替用户定的（他两个确认问题 120s 未回）；`btEnsureScreenPool` 只在面板首次渲染时拉 `screen-pool.json`，若该文件 404 会退到 raw.githubusercontent，两步都失败则「筛选」池为空（页面不报错，列表少 40 项）—— 这一支未实测断网态。
- 下一步：线上已复核（`?v=918a` 徽标 v918、两个入口卡、三池 66 项、持仓组合 5.08% 零回归）。若要动权重默认值，改 `btCfg()` 的 `customWMode`；若要改默认预选，给 `btCustomUniverse()` 加初始选中逻辑。
- 别碰：`btTypePile` 的类型白名单（v916 刚定）；`#btOut` 第 7 张表首列两金额粘连是 v909 既有格式，本轮未修；`#view-data .dc-tbl td:first-child{position:sticky;left:0}` 三池共用，别动。

### 2026-11-12 · v917 自选池列集回归三池统一 · 已发布（head `6b42d1662b27`）
- 改了什么：`renderPoolWatch` 的 `cols` 由 `poolWatchCols()` 改回 `poolColsAll()`（61 列，与资产配置/筛选同表头同列序）+ `opW` 170 + 操作按钮横排 + 删掉 v915 三条首列 static 覆盖、恢复冻结首列（tag `fw2_v917_watch_cols_aligned`）。
- 新增资产：工具 `_apply_v917_watch_cols_aligned.py` / `_patch_docs_v917_pre.py`；`poolWatchCols()` 保留但不再调用（回退用）。
- 未验证的假设：完整列集下 501px 容器要横滑约 9 屏才到操作列，我按"用户要一致性优先"处理，未回头征求是否再收一版折中列集（如 30 列）。
- 下一步：线上 `?v=917a` 核徽标 v917 与自选池 61 列；若要回退 7 列版，把 `cols:poolColsAll()` 改回 `cols:poolWatchCols()` 并重新加回 `#dcPoolWatchWrap` 首列 static 覆盖（P44 判据：先量 `.table-wrap scrollWidth vs clientWidth`）。
- 别碰：`#view-data .dc-tbl td:first-child{position:sticky;left:0}` 这条全局规则别动（三池共用，资产配置/筛选池依赖它冻结首列）。

### 2026-11-12 · v916 自选池回测权重改固定百分比 + 档位按基金类型 · 已发布（head `a7eb7c2d4b3a`）
- 改了什么：`btCfg().watchW`（自选每只固定占总预算 %，默认 5/上限 45）+ `btTypePile()`（类型优先分档）+ `btTargets` 权重重写（同档 85% 压缩、`watch` 缺档留现金）+ 抽屉 `#btIn_watchW` 与 5 行口径说明 + 摘要回显 `watchW/idle/squeezed`；附带修 `poolProfileE` 懒加载（P45）。
- 新增资产：tag `fw2_v916_bt_watchw`；工具 `_apply_v916_bt_watchw.py` / `_apply_v916b_ui.py` / `_apply_v916c_prof_lazy.py` / `_apply_v916_badge.py` / `_patch_docs_v916_pre.py`。
- 未验证的假设：`watchW` 上限 45 与 85% 压缩阈值是我按"单只别压过整档"定的经验值，未与用户确认；`btTypePile` 的宽基白名单是按现有 family 词表写的，新家族名（如 中证A100/科创50）会落到「进攻」。
- 下一步：用户要看「仅自选池 85% 留现金 → 年化 2.26%」是否可接受；若要满仓需改口径（池内按类型归一）而不是改代码即可。复测命令：本地 8791 → 策略执行 → 组合回测 → `#btIn_pool` 设 `barbell/barbell_watch/watch` → 读 `#btRunSum`。
- 别碰：`caifu/` 下 3 个数据文件夜间自动化与本轮 push 并行出现 409（内容已一致），别再手动重推；`btRolePile` 保留为兜底，不要删。

### 2026-11-12 · v915 修自选池首列空白（v914 线上缺陷）· 已发布（head `d2a580f115db`）

- **改了什么**：`edit_work/index.html`（徽标 **v915**，tag `fw2_v914_watch_cols` + `fw2_v915_watch_nostick`）——新增 `poolWatchCols()`，自选基金池由 64 列全列集改为 7 列（名称/代码·来源、档位/家族、近1年、近3年、最大回撤、总分、操作），操作列两按钮改竖排；实测 `scrollWidth=500 / clientWidth=501 / overflow=0`。资产配置与筛选池仍是 61 列（未动）。
- **v914 发布后线上缺陷（v915 已修）**：1280 宽视口自选池首列全空白——`td:first-child{position:sticky;left:0}` 在「表格不横向滚动」时会裁掉内容层（背景照画、纯红测试文字也不显示，DOM/`elementFromPoint` 全正常）。v915 对 `#dcPoolWatchWrap` 关掉首列 left sticky（连表头 `top:0` 一起 static），宽屏恢复。详见 PITFALLS **P44**。
- **发布记录**：2026-11-12 21:03 head **d2a580f115db**（index.html 4,422,658 B，prev_sha=30aa3629），`AUDIT=PASS 36/36`，commit「数据更新（离线刷新 + 双轨发布）」。两轮被打回都是数据新鲜度：①`fund_monthly` 双源/ACCNAV（`--only fund-monthly,fund-daily` 补齐）；②`v883 净值新鲜度硬卡` 9 只持仓 `navDate=2026-11-11 < fund-daily 末点 2026-11-12`（`--only` 不刷持仓）→ 跑**完整** `refresh_all.py`（不带 `--only`）后转 PASS。**晚间盘发布时 `--only fund-monthly,fund-daily` 不够用**。
- **数据缺口（发布当日实况，不阻断页面）**：`fund-daily` 103 只里 66 只末点 2026-11-12、37 只仍 2026-11-11（当日披露未齐）；`holdings` 全部 24 只 navDate 已随完整日频链刷到 2026-11-12。`refresh_all` 全刷后 4 个检查步骤 FAIL：`_audit_pe_chain_v846`（peDate 出现 11-11/11-12 两日）、`_audit_chart_tokens_v851`（var 兜底漂移 334 > 基线 332）、`_audit_contrast_css_v852`、`_audit_sig_type_v856`（`:root --fs-sm` 实测 12px ≠ 脚本期望 11px）——这 4 项**不进发布闸门**，属历史基线待校准，接手时别误当本次改动引入。
- **未验证的假设**：极窄视口（501px 视口 → 内容宽 469px）下模拟测得 `scrollWidth 478`（溢出 9px，操作列仍完整）；线上本次视口恰好 499px 内容宽（`499/499` overflow 0）。真 529px/375px 视口未直测（CDP 改视口报 session not found，用注入窄屏规则近似）。
- **下一步 + 别碰**：发布走 `cd edit_work; & py push_gh_v39.py`（先确认无并发 gate；gate 常因当日新披露净值卡在 `fund_monthly`，跑 `refresh_all.py --only fund-monthly,fund-daily --no-publish` 再发）。**别碰** 名称列的 `inline-block + max-width + word-break` 三件套——改成 `nowrap` 会让列宽按内容撑开、回到 700px+ 横滑。若要恢复全列，把 `cols:poolWatchCols()` 换回 `poolColsAll().concat([…])` 即可（其余逻辑不依赖列集）。

### 2026-11-12 · v913 新增自选基金子模块 + 回测标的池 · 已发布（head 172b74b94a43）

- **改了什么**：`edit_work/index.html`（徽标 v913，tag `fw2_v913_watch_pool` / `fw2_v913_watch_add` / `fw2_v913_bt_pool`）——①基金数据 tab 在「资产配置」后新增「自选基金」（恢复 v563 下线、v644 回退的死代码 `renderPoolWatch`）；②补「手动加入」工具条（代码 + 可选名称，写入 `fw2_watch_added_v1` 并带 `manual:1`）；③修 `loadPoolData()` 无调用点导致自选表恒空；④参数抽屉新增「标的池」下拉（杠铃档位 / 杠铃+自选池 / 仅自选池），`btTargets(budget,cfg)` 按 `cfg.pool` 组标的集，新增标的按该档 w 中位数、仅自选池时档位目标在有标的的档位间归一。
- **新增资产**：`edit_work/_apply_v913_pool*.py`（补丁脚本 9 个，可留档）；`window.__poolHeldCodes` 导出（v913）。
- **未验证的假设**：①`holdnums`/画像 `role` 中「海外独立」归进攻档属我的判断，没有用户确认；②自选池 64 列宽表未做窄屏裁剪，是否要裁待用户拍板。
- **发布记录**：首轮 gate FAIL 于 `fund_monthly`（`DUALSOURCE` + `ACCNAV`，发布文件不一致=2）——当日新披露净值、本地数据落后一天，非本次改动引起；`refresh_all.py --only fund-monthly,fund-daily --no-publish` 后 GATE=PASS，head **172b74b94a43**（4,417,103 B）。
- **下一步 + 别碰**：线上已验（徽标 v913 / tab 顺序 / 自选池 3 行 / 标的池三档 / 摘要三数闭合）。若要改自选池纳入回测的权重口径，先跑三模式对照（杠铃 13/11、杠铃+自选池 16/14、仅自选池 3 只），摘要行的「计划/建仓/w=0」三数必须与「按标的阈值」表只数对得上。发布仍走 `cd edit_work; & py push_gh_v39.py`（先确认无并发 gate；日志 0 字节 15–22 分钟属正常）。改 `btTargets` 的权重口径前先跑三模式对照（杠铃 13/11、杠铃+自选池 16/14、仅自选池 3 只），摘要行的「计划/建仓/跳过」三数必须与「按标的阈值」表只数对得上。**别碰** `SIGNALS_CFG.barbell.target`（40/35/10/15）——回测的档位归一是在计算层临时换算，不改配置。

### 2026-11-12 · v912 四图加小标题 · 已发布（head 3d94545384c8）

- **改了什么**：`edit_work/index.html`（tag `fw2_v912_bt_chart_titles`，徽标 v912，4,403,449 B）——四图前各插 13px 加粗小标题 + 11px 灰字口径说明（① 分标的持仓市值 ② 回撤水下 ③ 月度收益 ④ 收益归因），大标题 hint 压成「四张图连看：谁在长 · 跌多深 · 哪个月难受 · 谁在撑」。纯 HTML，未动任何图配置/数据。
- **未验证的假设**：无。说明行在 530px 内容宽下单行不折行，已截图确认。
- **发布踩坑**：首轮 gate FAIL，原因是 `data/fund-daily.json` 停在 11-10 而在线源已放出 11-11（017436 华宝纳斯达克精选），与本次改动无关；`refresh_all.py --only fund-monthly,fund-daily --no-publish` 补齐后通过。详见 PITFALLS **P42**。
- **下一步 + 别碰**：四图标题是 HTML `<div>`，不要改成 ECharts `title`（会占 grid 顶部并与 legend 争位）。改说明文案前先按 530px 估字数。

### 2026-11-12 · v911 修四图尺寸不同步 · 已发布（head 25b3dadc5a29）

- **改了什么**：`edit_work/index.html`（tag `fw2_v911_chart_resize`，徽标 v911，4,402,124 B）——`mountChart` 统一挂 `ResizeObserver`（`init` 后 `observe(el)` + 立即 `resize()`，`dispose` 前 `__ro.disconnect()`）。
- **症状与根因**：v910 四图在窗口缩放 / 抽屉展开 / 面板显隐后不重绘 → 内容挤在左侧、x 轴只剩一两个标签。ECharts 只在 init 读一次容器尺寸；`#btChart` 有独立 RO，新四图漏挂。
- **发布证据**：`[200] caifu/index.html (prev_sha=3546f4c8, 4402124 bytes)` → `VERIFY master head sha = 25b3dadc5a29`，audit 36/36。
- **未验证的假设**：无（用户的具体触发路径未逐条复刻，但 RO 覆盖了"容器尺寸后变"这一类全部成因）。
- **下一步 + 别碰**：判断图表布局宽度必须用 `canvas.getBoundingClientRect().width`，**不要用 `canvas.width`**（DPR 缓冲，会差 1.5–2 倍，P41）。别用 heatmap/scatter/custom（P40）。
- **文档已同步**：README 三节 + ver v911、`docs/PITFALLS.md` P41、`docs/FRONTEND.md` §9f 补尺寸同步约束。

### 2026-11-12 · v910 持仓过程四图 · 已发布（head 5ec87333df96）

- **改了什么**：`edit_work/index.html`（tag `fw2_v910_bt_process_charts`，徽标 v910，4,401,256 B）
  - 「持仓过程」卡四图：①分标的月频市值（11 条 + 合计黑粗线挂右轴，清仓后断线）②日频回撤水下面积 ③月度收益正负双色柱 ④收益归因横条
  - 数据全在 `renderBacktest()` 内由 `curve / trades / seriesBy` 现算，`btRun` / `tryBuy` / 阈值表**零改动**
- **发布证据**：`GATE=PASS` → `AUDIT=PASS 36/36` → `[200] caifu/index.html (prev_sha=19254b26, 4401256 bytes)` → `VERIFY master head sha = 5ec87333df96`
- **两条自洽校验**：合计线末值 43,332.20 = 汇总表期末在仓；归因合计 20,050.11 = 80,050.11 − 60,000
- **未验证的假设**：「已实现盈亏」按均价摊减成本结转，与券商实际成本核销口径可能不同（回测内部自洽）。
- **下一步 + 别碰**：别碰 `P.gridFund` 三态哨兵（P39）；**别用 heatmap/scatter/custom**——本页 ECharts 精简构建未注册（P40），会静默出空白图。
- **文档已同步**：README 三节 + frontmatter（ver v910）、`docs/PITFALLS.md` P40、`docs/FRONTEND.md` §9f。

### 2026-11-12 · v909 持仓过程视图 · 已发布（head dcf83f5ddb08）

- **改了什么**：`edit_work/index.html`（tag `fw2_v909_bt_pos_timeline`，徽标 v909，4,392,085 B）
  - 流水表 9→7 列（标的/代码、动作/档位双行），新增「在仓(该标的)」= 该笔成交后市值 + 浮动%
  - 新增「按标的汇总」表（5 列双行：买入/卖出 · 在仓/成本 · 浮动 · 已实现 + 合计行）
  - 新增「过程风险」条（年化波动 / 最大回撤与最长水下天数 / 最差单日 + 日期 / 最差单月 / 正收益月）
  - 全部在渲染层由 `trades / curve / seriesBy` 现算，未改回测核心
- **发布证据**：`GATE=PASS` → `AUDIT=PASS 36/36` → `[200] caifu/index.html (prev_sha=6e741855, 4392085 bytes)` → `VERIFY master head sha = dcf83f5ddb08`
- **合规性校验**：期末在仓 ¥43,332.20 + 期末现金 ¥36,717.91 = 策略期末市值 ¥80,050.11（恒等式成立，已写进页面脚注）
- **未验证的假设**：「已实现盈亏」按均价摊减成本结转，与券商实际成本核销口径可能不同（回测内部一致，不代表真实账户账务口径）。
- **下一步 + 别碰**：若要加「分标的持仓曲线」或「回撤水下图」，在 `renderBacktest` 内新增 ECharts 实例即可，勿动 `tryBuy/trySell/BT_PF`。别碰 `P.gridFund` 三态哨兵（v906 P39）。

### 2026-11-12 · v908 回测参数回显 · 已发布（head a536aa4e8e13）

- **改了什么**：`edit_work/index.html`（tag `fw2_v908_bt_param_echo`，徽标 v908，4,382,380 B）
  - `runSum` 由「当前规则：止盈减仓 ±A · 止损 B · 网格 C」改为「**本次回测：本金 ¥X · 起→止 · 止盈减仓 ±A · 止损 B · 网格 C · 备用金不限额/上限 · 动用备用金 N 笔 ¥Y**」
  - 目的：用户改金额或年份时这一行必变，避免「参数改了页面毫无反应」被误判为「每次都一样」
- **矩阵实测（证伪「固定 20 笔」）**：16 笔 ¥8,000（2021-2023）/ 7 笔 ¥3,500（2024-2026）/ 17 笔 ¥8,500（本金 20 万）/ 20 笔 ¥10,000（2021-2026 本金 5 万）
- **发布证据**：`GATE=PASS` → `AUDIT=PASS 36/36` → `[200] caifu/index.html (prev_sha=1e374a10, 4382380 bytes)` → `VERIFY master head sha = a536aa4e8e13`
- **未验证的假设**：用户端看到「每次 20 笔」的具体操作路径未复现（推测为改参数后未重算/未触碰 change 事件所致，本次以回显兜住，若仍复现需抓他当时的输入框值）。
- **下一步 + 别碰**：若仍出现「参数变了笔数不变」，直接抓 `btIn_start/btIn_end/btIn_budget` 的 `value` 与 `btRunSum` 文案比对。别碰 `tryBuy`、`BT_PF`、止损判定块。

### 2026-11-12 · v907 备用金动用笔数 + 逐笔明细 · 已发布（head b8e3ce237907）

- **改了什么**：`edit_work/index.html`（tag `fw2_v907_bt_grid_evidence`，徽标 v907，4,381,513 B）
  - 明细行「其中动用备用金」加笔数：`¥10,000.00（20 笔，不限额）`
  - 流水 hint 加「其中备用金来源 20 笔 ¥10,000.00（逐笔看「资金」列）」
  - 新增折叠块「备用金动用明细（20 笔 · 合计 ¥10,000.00 · 不限额，按实际累计）」，逐行 日期 · 标的 · 金额
- **发布证据**：`GATE=PASS` → `AUDIT=PASS 36/36` → `[200] caifu/index.html (prev_sha=c72474b3, 4381513 bytes)` → `VERIFY master head sha = b8e3ce237907`
- **未验证的假设**：无。
- **下一步 + 别碰**：若要验证「不限额确实会多买」，换配置即可（90,000 / 2021-01-01→2026-06-30 / `perFund=false` → 26 笔 ¥13,000）。别碰 `btRebalance`、`BT_PF`、止损判定块。

### 2026-11-12 · v906 备用金取消上限 + 主表累计买入/净投入 + 零头修复 · 已发布（head 3c5ef89baf2d）

- **改了什么**：`edit_work/index.html`（tag `fw2_v906_bt_fund_unlimited`，徽标 v906，3,776,641 B）
  - 备用金上限 `gridFund=0` 即不限额（默认；旧默认 10000 自动迁移）；`P.gridFund=null` 哨兵，`need=Infinity`、`gridOk` 放行、扣减跳过
  - 主表 7 → 9 行：加「累计买入 / 净投入」（`stats.buyAmt / sellAmt` 用 `t.raw` 精确求和）
  - 零头修复：余额在 (0, gridAmt) 时直接用余额买，不再永久卡池
- **未验证的假设**：无。（不限额后「累计买入恰好等于总投资金额」是当前策略卖出后钱停现金、不再买回所致，非计算耦合；若日后恢复下带补仓，两者会分离。）
- **发布证据**：`GATE=PASS` → `AUDIT=PASS 36/36` → `[200] caifu/index.html (prev_sha=d1c778ab, 4380253 bytes)` → `VERIFY master head sha = 3c5ef89baf2d`（日志 `edit_work/push_v906_fg.log` 17,658 B，err 0 B）。线上实测与本地逐项一致：徽标 v906、默认 `gridFund=0`、摘要「备用金不限额」、主表 9 行、`overflow=0`；同配置 总投 ¥103,000 / 累计买入 ¥103,000 / 净投入 ¥61,344 / 期末 ¥121,380.65 / 17.85% / 3.03% / −5.90% / 0.24。
- **别碰**：`btRebalance`（只上带）、`BT_PF` 阈值表、止损判定块；README 条目顺序重排是独立高风险项。

### 2026-11-12 · v905 对照表 7 行 + 总投资金额口径 + 「减配」改称「止盈减仓」 · 已发布（head 3004e877e2ad）

- **改了什么**：`edit_work/index.html` v904→**v905**（徽标已升，纯 LF，3,774,988 chars / 4,378,035 B）。①`cmpRows` 5→7 行（总投资金额/投资年限/期末市值/总收益率/年化收益/最大回撤/Calmar），交易笔数下沉 `cmpSub`；②总投资金额 = `res.cfg.budget + S.gridUsed`（实测 ¥56,500），总收益率同分母（74.11%）；③**删掉「总收益率（仅本金分母）」错配行**（`endV/budget` 分子含追加、分母只有本金，实测虚高到 96.74%），换成 `其中动用备用金 ¥6,500` + `备用金未用尽 ¥3,500`；④「减配」10 处可见文案改「止盈减仓」，`trades.type` 仍为 `'再平衡'`；⑤`rN` 加单位参数（期末市值 `+5.30 %`）、两个 `h3` 加 nowrap。补丁 `_apply_bt_v905.py`/`v905b`/`v905c`/`v905d`/`v905e`/`v905f`，tag `fw2_v905_bt_cmp7_tp_rename`。
- **未验证的假设**：无。7 行数字逐项从 `#btOut` 读出并与 `期末/总投资−1` 手工对账；宽屏与 500px 容器模拟均 `overflow=0`、表行高 32/33px 一致；曲线 `toDataURL` 导出三条线 + 红区 + ▲ 标记齐全。
- **发布证据**：`push_gh_v39.py` → `GATE=PASS` → `AUDIT=PASS 36/36` → `[200] caifu/index.html (prev_sha=3a45121c, 4378035 bytes)` → `VERIFY master head sha = 3004e877e2ad`（日志 `edit_work/push_v905_fg.log` 17,658 B）。线上实测徽标 v905、主表 7 行、三卡「止盈减仓 / 止损 / 网格」、筛「全部/建仓/止盈减仓/止损/网格」、零「减配」残留、`overflow=0`；线上实跑 6.19% / −7.91% / Calmar 0.58 / 占用 39.54%，与 v903·v904 同配置逐项一致。注意：`prev_sha` 不是 v904 的 `7f3e273a2d1e`，中间插了一次数据自动刷新提交，属正常。
- **别碰**：`trades.type` 的 `'再平衡'` 值（改显示层即可）；`retBase` 不要再拿回主表（分母错配）；`BT_PF` 与 `btRebalance` 本轮零改动，阈值仍是 v903 那套（宽基 −12% / 进攻 −15% / 对冲 −8%·−12% / 现金不设，止盈减仓 ±25%）。
### 2026-11-12 · README 头部结构修复（治理轨，前端零改动） · 已完成

- **改了什么**：`README.md` 结构归位 —— ①孤立 `---` 补成成对 frontmatter（第 1–5 行：`---` / `next:` / `ver: v904` / `updated:` / `---`）；②原被塞在标题前的 689 行历史条目（v901 详细 → v687 简短）+ v900/v899 两条，整块搬到 `## 当前进度` 末尾并加 `### 历史条目（v901 → v687，写入序，非严格倒序）` 小标题；③清 2 行真重复（v902b 标题重复第二行、v902 缩写残片，后者信息并入完整条目标题）。
- **新增资产**：无（备份 `D:\Temp\README_v904_backup.md` 892,044 B）。
- **未验证的假设**：无实质假设。搬迁用行切片 + 多重集校验（丢/增均逐条断言），`## ` 标题数与字符量均核对。
- **下一步**：如需再读断点，跑 `cd edit_work; & py handoff_check.py`，期望 `README updated : 2026-11-12` 且 `next:` 首 300 字能正常打印。**若要推送 README**：`cd edit_work; & py _push_readme.py`（末行须 `BYTE_MATCH True`）——本轮**未推送**，线上 README 仍是上一版。
- **别碰**：`## 当前进度` 与 `### 历史条目` 两段的条目顺序**仍未按版本号重排**（两段并列、段内各自写入序），重排是独立项、风险高，改动前先备份并逐条比对版本号；`handoff_check.py` 依赖行首 `updated:`/`next:`，动 frontmatter 后必须重跑它。

### 2026-11-12 · v904 组合回测页五层结构 + 参数区抽屉 · 已发布（head 7f3e273a2d1e）

- **改了什么**：`edit_work/index.html` v903→**v904**（徽标已升，纯 LF）。七处：参数区拆 `#btRunBar`（区间/本金/运行/全部参数⚙/`#btRunSum` 摘要）+ `#btDrawer`（默认 `display:none`，三组，原 `btIn_*` id 全保留）；结论条吸收重复的两行仪表；对照表 9→5 行 + 一句换算句（其余 4 行下沉「对照口径细节」）；L3 三规则卡（减配 ±25% / **止损触发即清仓·红字** / 网格）；阈值表折进 `▸ 按标的阈值（11 只）`；曲线 `markArea` 最深回撤 + `markPoint` 减配/止损点；分年度表提到明面；流水按类型筛选（`btFilterTrades`）。补丁 `_apply_bt_v904a.py` / `v904b` / `v904c` / `v904d` / `v904e` / `v904f`。
- **新增资产**：`docs/v904_bt_panel_wireframe.html`（纸面稿，已拍板）；无新数据源。
- **未验证的假设**：①「用 0.80pct 年化换 8.05pct 回撤＝少亏约 10 块」只是比值换算，未按复利/时间折算；②最深回撤区间落在曲线尾部（2025-10→2026-08，抽样索引 465–479），是 v903 把前面回撤压小后的真实结果，未与逐年回撤逐段对拍；③窄屏 538 的「策略 vs 对照」标题折行属**模拟假象**（只改容器宽度不触发媒体查询；真机 <560px 由 `.card-h` 的 column + ellipsis 规则兜底），未在真实窄窗口复验。
- **发布证据（2026-11-12 09:34→09:53 实测）**：`GATE=PASS`（gate 段日志 0 字节约 18 分钟，属正常）→ `[200] caifu/index.html (prev_sha=7919b385, 4376198 bytes)` → `VERIFY master head sha = 7f3e273a2d1e`，audit `PASS=35 FAIL=0`。线上核验：徽标 **v904**、页面零「v903」可见字样、信息块 13 个顺序正确、`#btRunSum` 摘要正确、抽屉默认 `none`（点开后文案「收起参数 ⚙」/ 10 个输入）、流水 5 个筛选按钮、29 行点「减配」筛出 10 行（建仓 11 / 再平衡 10 / 网格 7 / 止损 1）、曲线 `series=3 / pts=480 / markArea=true / markPoints=11`；**同配置数字与 v903 线上逐项一致**（6.19% / 0.58 / 39.54%）。
- **下一步**：无阻塞。待拍板的口径项：band 按标的分设 / 止损再调 / 网格清仓后是否暂停 / 费率扣减 / 无风险利率取值 / 「同期对齐」长窗口。若要重跑验证：`python -m http.server 8791`（cwd=`edit_work`）→ 点侧栏「策略执行」→ 点 `#stratTabs .st-tab[data-st="bt"]` → `#btRunBtn.click()` → 等 8~9s；**曲线取证必须等动画结束（≥3s）再 `toDataURL`，否则只导到坐标轴**。
- **别碰**：`BT_PF` / `btPF` / `btRun` / `btRebalance`（v903 已定稿，回测数字是基线，任何改动都会重算全史）；`gbar`/`gaugeBox` 是死代码但保留着（回滚用）；`README.md` 头部 frontmatter 已结构性损坏（孤立的 `---` + 条目被塞进 frontmatter 区 + v902b 条目重复），**本轮未重排，改动前先备份**；`D:\Temp\index_v904_backup.html`（4,376,198 B）是发布前本地副本，回滚基准。

### 2026-11-12 · v903 止盈档位退役 + 标的级带宽减配 · 已发布（head 01c5fe06b06c）

- **改了什么**：`edit_work/index.html` v902d→**v903**（4,365,122 B / 3,764,193 chars / 纯 LF / `ver-badge">v903`）。五处改动：`btRebalance` 重写为标的级只上带（tag `fw2_v903_bt_asset_band`）、`BT_PF` 的 tp1/tp2 清零且 000912 加 `bd:0`、`btCfg` 默认 band 5→25 并加 `band ≤ 10 → 25` 迁移（tag `fw2_v903_bt_band_migrate`）、参数区撤掉止盈①②输入并改「减配带宽(%)」、阈值表 8 列改 7 列（「减配 / 权重上带」列）。补丁 `_apply_bt_v903.py` / `_apply_bt_v903b.py` / `_apply_bt_v903c.py`。
- **未验证的假设**：①35.91% 的期末现金堆积是否可接受（只减不补的必然结果，年化因此低于对照 6.88%）；②band=25 是统一值，未按标的分设——若要做「进攻档放宽、国债收窄」，BT_PF 的 `bd` 字段已就位可直接填数；③减配成交未计申赎费（与全项目同口径，`btRun` 主循环无费率逻辑）。
- **发布证据（2026-11-12 实测）**：`[200] caifu/index.html (prev_sha=55e21a30, 4365363 bytes)` → `VERIFY master head sha = 01c5fe06b06c`；线上 `https://andylauxiaoyang.github.io/investment-workbench/caifu/index.html` 徽标 **v903**、页面无「止盈①」字样；线上真跑 2017-05-07→2026-09-28：gridAmt=500 时 **6.19% / −7.91% / Calmar 0.58**（与 Node 实验 V17 逐项一致），用户旧配置 gridAmt=1000 时 6.31% / −7.92% / 0.60（差异仅来自网格额）。README 已推（BYTE_MATCH True / 885,007 B）。
- **首推被拦（真阻塞，已排除）**：push 内 gate 报 `verify_acc_nav ACCNAV=FAIL` / 019155「意外跳过」，实为手动 gate 与 push 内 gate 并行读写 `data/_hist_cache/019155.json` 的竞态；`verify_acc_nav.py --only 019155` 复验 `ACCNAV=PASS`（39 月全对）后重推成功。见 P37。
- **下一步 + 别碰**：先让用户看线上 v903（`python -m http.server 8791`，cwd=`edit_work`）并决定「减配资金去哪」（停现金 / 转国债档 / 开下带补仓），再连同 v902b/c/d 一起发布；发布前必须补 `docs/FRONTEND.md` §9（减配口径 + band 迁移）与 `docs/PITFALLS.md` 两条（①带下补仓在下跌中逆势接刀；②band 语义变更后旧值必须迁移，否则 5% 带宽驱动减配会把换手抬高 3–4 倍）。别回滚 `BT_PF` 的 `tp1/tp2` 清零——止盈分支代码仍在，填回数值会与减配叠加成双重机制。

### 2026-11-11 · v901 删掉回测页「口径 / 收益口径」提示 · 已发布（head 6c94d625c86e）

- **改了什么**：`edit_work/index.html` v900→**v901**（3,756,834 chars / `ver-badge">v901`）。删除 `renderBacktest()` 参数区下方两行 `rv-line`（`口径` 与 `收益口径`）共 875 字符，tag `fw2_v901_bt_hint_remove`（原位留注释）。`ddLine` 计算保留未删（无人消费，回滚可直接复用）。
- **未验证的假设**：这两行原本承载「无风险利率来源（中国货币网 2026-11-10 10Y 1.5880%）」与「备用金＝额外追加」的成文依据，删除后页面文字层面不再声明；若日后被问口径来源，答案在 `docs/FRONTEND.md` §9 第 7–9 条与本 INBOX。
- **下一步 + 别碰**：`& py push_gh_v39.py` 发布（先 gate，落 `push_v901_fg.log` 读证据）；线上强刷确认「收益口径」「建仓=」已消失且四层结构仍在。别把结论条里的「Calmar(严格) / 达标线」也删掉——那是判断核心。
- **已发布证据（2026-11-11 实测）**：`[200] caifu/index.html (prev_sha=e39c6f98, 4355440 bytes)` → `VERIFY master head sha = 6c94d625c86e`；index.html / data/fund-monthly.json / data/fund-daily.json 三件 raw 回读与本地 **逐字节一致**（4,355,440 / 1,330,683 / 9,114,036 B），index sha12 `addb8a96dbba`；线上徽标 v901，回测页 `hasHint=false`（无「收益口径」「建仓=」），结论条/仪表/对照表不变。
- **途中闸门拦截（真问题）**：首推 `GATE=FAIL`（`fund_monthly` 的 `verify_acc_nav`/`verify_dual_source`）——163813、501226 两只 QDII 的 2026-11-10 净值今晚才补发，本地数据停在 11-09。修法＝重跑 `gen_fund_daily.py`（181,812 行）+ `gen_fund_monthly.py`（81 只 7,382 行），单组闸门回到 PASS 后再推。详见 PITFALLS P34。

### 2026-11-11 · v900 组合回测改四层信息结构 + 参数联动修复 · 已发布（head b24b2f291a6b）

- **改了什么**：`edit_work/index.html` v899→**v900**（3,757,634 chars / `ver-badge">v900`）。回测结果区从 13 张平铺卡改为四层：结论条 `conclBar`（达标药丸 + 三个不拆行短语 + 一句诊断，诊断按「两项达标 / 年化不足且预算未满 / 年化不足且预算已满 / 年化超但 Calmar 不足」四分支）、两行仪表 `gbar`（年化进度、回撤预算用量，越界转红）、「策略 vs 对照」表 `rN`/`rT`（指标/策略/对照/差，差＝策略−对照）、折叠明细 `detailHtml`（档位+分年度+流水进 `<details>`），tag `fw2_v900_bt_layout`。同时修 `fw2_v900b_bt_cfg_refresh`（`btSave(c)` 后 `cfg = btCfg()`，解决「改目标年化后结论条不跟」）与 `fw2_v900c_no_silent_catch`（`renderStrategyView` 空 catch 改 `console.error('BT_RENDER_ERR',…)`）。
- **新增资产**：无新脚本；截图证据 `D:\Temp\bt900_top.png` / `bt900_detail_collapsed.png` / `bt900_detail_open.png`。
- **未验证的假设**：①「差」列里的年化波动是「策略−对照」的反号写法（波动越低越好，所以取 `hold.vol − strat.vol`），未在文案里额外解释；②诊断四分支的 85% 阈值是我按经验定的分界，用户没拍过。
- **下一步 + 别碰**：`& py push_gh_v39.py` 发布（先 gate，落 `push_v900_fg.log` 读 `GATE=PASS` 与 `[200] caifu/index.html`，**勿只看 exit code**），raw 逐字节回读 + 线上强刷核对四层是否都在；再在线上把目标年化改 25→10 验证面板跟随。别碰 `btRun()` 的 `stats` 段（分母/Calmar 口径 v899 刚定），别把净值曲线折进 `<details>`（用户要看趋势）。
- **已发布证据（2026-11-11 实测）**：`GATE=PASS` → `[200] caifu/index.html (prev_sha=051d0db3, 4356794 bytes)` → `VERIFY master head sha = b24b2f291a6b`；raw 逐字节回读 online/local 均 4,356,794 B、**BYTE_MATCH True**、sha256 前 12 位 `f594442e4a1d`；标记命中 `ver-badge">v900` 1、`fw2_v900_bt_layout` 1、`fw2_v900b_bt_cfg_refresh` 1、`fw2_v900c_no_silent_catch` 1、`btIn_rf` 1、`额外追加` 2。线上实测徽标 v900、默认区间结论条「✗ 未达标｜6.39%（缺 3.61pct）｜Calmar 0.41（差 0.01）｜占用 59.00%」、仪表与对照表齐全、目标年化 10→25→10 面板跟随。截图 `D:\Temp\bt900_live.png`。

### 2026-11-11 · v899 严格 Calmar（扣无风险）+ 备用金定为「额外追加」· 已发布（head a9b7c33989ee）

- **改了什么**：`edit_work/index.html` v898→**v899**（3,753,028 chars）。`btCfg()` 增 `rf: 1.59`；参数区增输入框 `btIn_rf`「无风险(%)」；`btRun` 增 `stats.rfUsed` / `calmarS = (ann−rf)/|mdd|`、`hold.calmarS`；Calmar 卡改名为「策略 · Calmar(严格)」、达标线 `(tgt−rf)/ddCap`；口径行加严格定义与 rf 来源（中国货币网 2026-11-10 10Y 国债 1.5880%）＋「备用金＝额外追加（不占 5 万本金）」；备用金灰条补「不占用 ¥50000.00 本金」。tag `fw2_v899_bt_calmar_strict`。
- **未验证的假设**：①rf 默认值是「取数当日」的 10Y 国债，国债收益率变了页面不会自动更新（要人改输入框）；②严格 Calmar 用 CAGR 减算术无风险利率，属常规近似（未做逐日无风险贴现）。
- **下一步 + 别碰**：`& py push_gh_v39.py` 发布（先 gate，落 `push_v899_fg.log` 读证据，**勿只看 exit code**）；线上核对「Calmar(严格) 1.32 / 达标线 0.42」「口径行含 额外追加」「灰条含 不占用 ¥50000.00」。**已发布**：head a9b7c33989ee / 4,351,560 B / raw sha 38d606b2f9f4 / BYTE_MATCH True / 提交 2026-11-11T06:11:07Z；线上实跑读到「Calmar(严格) 0.41、达标线 0.42、−0.01」与占用 59.00%（默认区间 2020-05-07→2026-09-28）。**别碰** `btRun` 的 `capBase/retBase` 双口径与 `card()` 符号规则（v897/v898 已定案）；`switchStratTab` 里 `try{renderBacktest()}catch(e){}` 的空 catch 是已知隐患（本轮踩过，未修，另立条目）。

### 2026-11-11 · v898 回测页风险预算改回用户真实容忍度（目标年化 10% / 回撤 20%）· 待发布

- **改了什么**：`edit_work/index.html` v897→**v898**（3,751,972 chars）。`btCfg().ddBudget` 默认 35→**20**；口径行删掉「可忍 25–35%」这句替用户假设，改「回撤预算＝你可忍上限（>100% 越界）」；`回撤预算占用` 卡改为有符号差 `ddBudget − |mdd|`（余量绿/越界红）；`策略·Calmar` 卡第二行改「策略 − 达标线（目标年化/回撤预算＝0.50）」，副标保留对照 Calmar；`card()` 加第 5 参 `hideH` 修「距目标年化」差值重复两遍；localStorage 里恰好 35 的存量配置一次性迁移并在页面明示。tag `fw2_v898_bt_risk_budget` / `fw2_v898_bt_ddbudget_migrate` / `fw2_v898_bt_card_hideh`。
- **未验证的假设**：①迁移只对「恰好等于旧默认 35」生效，若某台机器上用户曾手动填过 35 会被一并迁走（页面已明示、可改回，未做二次确认）；②「达标 Calmar＝目标年化/回撤预算」是近似判据（严格口径应按超额收益/无风险利率算），本页只作够不够用的粗筛。
- **下一步 + 别碰**：`& py push_gh_v39.py` 发布（先跑 gate，约 20 分钟，**必须落日志读**，不可只看 exit code）；线上强刷核对「占用 66%± / 上限 20.00% / 余 +x pct 绿」「Calmar 副标含 达标线 0.50」。**别碰** `btRun()` 的 `stats` 段与 `capBase/retBase` 双口径——v897 已定案；也别把 20% 再写死进任何结论文案。

### 2026-11-11 · v897 组合回测页升级为决策面板（**已发布 head d586638f**，待用户强刷验收）· 已交接

- **改了什么**：`index.html` 组合回测段（tag `fw2_v897_bt_panel` 等）——4 条 P0 修复（回撤差值改 `strat-hold` 并标红 / 收益率分母 `capBase = budget + gridUsed` 且并列「仅本金」口径 / 「交易日」改「净值日期 + 日历日」/ 截止日 `max` 读 asOf 并在数据到齐后回写 + 落后天数提示）+ 4 个判断入口（10% 目标年化线入图 / 回撤预算占用 / Calmar / 分年度收益对比表）+ 档位表现金行与合计行 + 流水「买入/卖出/净投入」汇总 + 参数单位与非法值提示。`verBadge v897`，3,750,957 字符。补丁 `_apply_backtest_v897.py`（31 处唯一性断言）+ 2 处内联。
- **新增资产**：无新数据文件；`D:\Temp\index_v896_backup.html`（回滚基准）、`D:\Temp\bt897_*.png`（真渲染取证 4 张）。
- **未验证的假设**：①`_bt_verify.html`（把 fund-daily 指向本地）验证通过，**交付文件的数据源未改**，线上仍走 GitHub raw；②`btRun` 主循环是否扣申赎费/管理费**未核实**（本轮未动费率逻辑）；③那 6,000 备用金是「5 万内划出」还是「额外追加」未拍板——所以主口径取「含实动追加」、并列「仅本金」，等用户确认哪个当默认。
- **下一步 + 别碰**：线上强刷确认三处：回撤卡差值变红负数、总收益出现两行（含追加 / 仅本金）、净值图有琥珀色目标年化虚线；核对数值 48.74% / 5.85% / −12.25%。**别碰**：`btMax` 的「渲染读 asOf + 数据到齐回写」两处必须同时在（少一处就落占位值）；`capBase` 里别把未动用备用金加进分子；`stats.strat.ret` 与 `retBase` 是两个口径不要合并。

### 2026-11-11 · v896 资产配置表第 10 列回正「实际市值」（已发布，线上 v896）· 已交接

- **改了什么**：`index.html` 表头 `<th>实际已投</th> → <th>实际市值</th>`；`strat-note` 三处口径说明同步（首句定义 / 调仓金额 / 进度滞后）并新增「不用于计算投入产出」；`verBadge v896`；表头 JS 注释追加 `fw2_v896_col_rename_back` 回正映射。`_audit_alloc_cols.py` A03b/C01/E01/E03 重锚 + E02 补旧名清零 + 新增 E04–E07；`_probe_alloc_progress.py`、`_probe_alloc_v893.py` 定位串同步；新增配方 `_apply_col_rename_v896.py`、探针 `_probe_alloc_v896.py`、核验 `_verify_online_v896.py`。
- **没改什么**：`_dcaMonthly` / `_dcaProg` / `liveMonthly` / `mvMap` / `sumMonthly` 取数链，14 列结构、colgroup、四类行模板 td 数、合计行、全部数值；v894 改名史实注释（旧列名仅存于注释区 2 处：史实 + 回正映射）；历史版本配方资产与历史 changelog 全部冻结。
- **怎么验证**：`& py _audit_alloc_cols.py`（`PASS=47 FAIL=0`）；`& py check_js.py`（`ALL OK`）；`& py _probe_alloc_v896.py`（`ALLOC_PLAN_MERGE_V896=PASS`）；`& py _verify_online_v896.py`（`ONLINE_V896=PASS`）。
- **下一步 + 别碰**：别把「实际市值」当台账累计净投入本金去与资金平衡/净资产趋势对拍；真·本金列须新建四段数据链，属数据口径变更，先拍板。凡再改列名，必须同步 `_audit_alloc_cols.py` 的 `ths[]`、C01、E01–E07 以及所有 `col('列名')` 定位的探针（P29 第二次实证）。全局替换旧列名前先分区：表头注释区与 docs/changelog 的历史引文是护栏锚点，禁改。
### 2026-11-11 · v895 定投执行去重融合进资产配置（已发布，线上 v895）· 已交接

- **改了什么**：`index.html` 删 `data-st="plan"` tab / `stp-plan` 容器（4→3 tab）；`renderStratTodo()` 改返回主表上方 `<details>` 折叠条；`renderStratPlan()` 改返回主表下方「策略参数存档」折叠卡（只留常态期/加倍档/资金源，删重复列与 `planNote`）；新增唯一实现 `ddwOf(codes)` 把回撤预警挂进四类行 `nm` 单元格；折叠态 `window.__ALLOC_OPEN__` + `el` 捕获监听跨 innerHTML 重写保持；`verify_sync.py` v142 标记串重锚；`verBadge v895`。新增 `_audit_plan_merge_v895.py` 并挂 `push_gh_v39.py` 硬卡。tag `fw2_v895_plan_merge`。
- **没改什么**：`_dcaMonthly` / `_dcaProg` / `mvMap` / `sumMonthly` 取数链、14 列结构、colgroup、四类行模板 td 数、合计行、全部数值、`STRATEGY_SNAP` 内嵌数据。`__mcGoAlloc()` 跨页跳转指向 alloc，不受影响。
- **怎么验证**：`& py _audit_plan_merge_v895.py`（`PASS=33 FAIL=0`）；`& py check_js.py`（`ALL OK`）；`& py _probe_alloc_v895.py`（`ALLOC_PLAN_MERGE_V895=PASS`，含 V11 重渲染后折叠态保持）。
- **下一步 + 别碰**：别把待办条/存档卡里的说明再用 `.strat-note` class（历史 CDP 探针取第一个 `.strat-note` 会静默读到错误说明，已用 `.alloc-note` 隔离）；别把折叠态只挂在 DOM 上而不做重写恢复（异步净值回来会把用户展开的卡收起）。存档卡是**历史存档非执行依据**，别拿它跟主表数值对拍。`S.plan` 的 5 万口径静态参数若要退役属删功能，需另拍板。

### 2026-11-11 · v894 资产配置表两列改名（已发布，线上 v894）· 已交接

- **改了什么**：`index.html` 表头 `进度金额→累计应投` / `实际金额→实际已投`，`strat-note` 口径说明同步并如实标注「实际已投＝持仓市值（含浮盈亏，非台账累计净投入本金）」，`verBadge v894`；`_audit_alloc_cols.py` A03b/C01 重锚 + E01–E03 新硬卡；`_probe_alloc_v893.py`、`_probe_alloc_progress.py` 列名定位串同步；新增配方 `_apply_col_rename_v894.py` / `_probe_alloc_v894.py`。tag `fw2_v894_col_rename`。
- **没改什么**：`_dcaMonthly` / `_dcaProg` / `mvMap` / `sumMonthly` 取数链、14 列结构、colgroup、四类行模板、合计行、所有数值。历史版本配方资产中的旧列名保留作版本史实。
- **怎么验证**：`& py _audit_alloc_cols.py`（期望 `PASS=43 FAIL=0`，含 E01–E03）；`& py _probe_alloc_v894.py`（期望 `ALLOC_RENAME_V894=PASS`）。
- **下一步 + 别碰**：接手先确认列名是否被后续版本再次改动——**凡改列名必须同步所有用列名做定位串的审计/探针**，否则发布链静默红或探针空跑。别把「实际已投」当成台账本金去与资金平衡对拍（口径不同，已写进口径说明）。真·本金列需另建数据链，属待拍板。


### 2026-11-11 · v893 资产配置表新增定投金额（月）（已发布，线上 v893）· 已交接

- **改了什么**：`index.html` 13→14 列 + 同源重构 `_dcaMonthly` / `sumMonthly`；`_audit_alloc_cols.py` 重锚并新增 A03b/D01–D07；`_probe_alloc_color.py` 列索引 9/11/12→10/12/13；`_audit_alloc_lag_color_v874.py` B27 同步。补丁 `_apply_dca_monthly_v893.py`，探针 `_probe_alloc_v893.py`。tag `fw2_v893_dca_monthly_col`。
- **口径**：新列 = `liveMonthly(code)`（计划每月定投额＝目标÷总月数·固定分期），与「进度金额」同源；**不是台账实际每月投入**。零新数据源、零数值口径变更。
- **已验证**：三条静态硬卡 PASS=40/20/28 FAIL=0；`node --check` 通过；CDP `ALLOC_DCA_MONTHLY_V893=PASS`（14 列逐行归位 / 合计 3,752＝逐行和 / 表头无溢出 / errs=[]）；CRLF=0。
- **未验证的假设**：真实浏览器（非 headless）观感待用户验收；「用户想要的是计划口径」属推断，若其实要台账实际投入需另建数据链（待表态）。
- **下一步 + 别碰**：下一步＝用户强刷验收 + 对「计划口径 vs 台账实际投入」表态。别单独改新列口径而不补数据链；别把 `_dcaMonthly` 拆回多处重复实现；**加/删列时必须同步重锚** `_audit_alloc_cols.py`、`_probe_alloc_color.py` 列索引、`_audit_alloc_lag_color_v874.py` B27（P29）。

### 2026-11-11 · v892 三项口径拍板落地（已发布，线上 v892）· 已交接

- **用户答复**：① 删除；② 基金持仓是季度披露的；③ 如果没有实际用途可删除。
- **改了什么**：`_gen_data_mgmt.py`（删 antiHalluc 写入段 + fund_jjcc/sources 两处 src 文案）、`index.html`（双份 DMCONFIG 同源文案 + `verBadge v892`）、`data/data-mgmt.json`（重跑生成，顶层 5 键 / 39 项 / 21,742 B）、`sources.json`（`_note` 失真宣称删除、如实描述、updated=2026-11-11）。补丁 `_apply_dm_v892.py`，探针 `_probe_dm_v892.py`。tag `fw2_v892_dm_caliber`。
- **已验证**：`_gen_data_mgmt.py` rc=0；`_audit_dm_v845.py` FAIL=False；`node --check` 通过；CDP `DM_V892=PASS`（39 行 10 列归位 / 两处口径可见 / errs=[]）。
- **未验证的假设**：① 真实浏览器（非 headless）观感待用户验收；② `sources.json` 未覆盖的数据集真实渠道数仍未逐项核实（本轮只收窄宣称、未补登）；③ `peDate` 两个数据日未统一，属既有挂账。
- **下一步 + 别碰**：三项口径已全部落地，原「待拍板/别碰」限制解除。别把 `sources.json` 从发布清单或 DMCONFIG 里删掉（3 处硬卡依赖它，P28）；别给 `fund_jjcc` 顶层加 `meta` 或改 `time` 路径（季度披露期口径）；别把 `antiHalluc` 写回生成器（前端零消费）。别回滚 DMCONFIG 双份同步（审计立刻红）。

### 2026-11-11 · v891 数据管理模块全量对账补齐（已发布，线上 v891）· 已交接

- **改了什么**：`index.html`（两端 DMCONFIG +1 `sec_daily` / 3 项文案订正 / 5 处「38→39」文案 / 周轨指令 / verBadge v891）、`_gen_data_mgmt.py`（同源 DMCONFIG）、`data/data-mgmt.json`（重跑生成，39 项）、`push_gh_v39.py`（挂 `_audit_dm_v845.py` 无条件硬卡）、`_probe_dm_v891.py`（新增 CDP 探针）。tag `fw2_v891_dm_sync` / `fw2_v891_dm_audit_gate`。
- **已验证**：`_gen_data_mgmt.py` rc=0；`_audit_dm_v845.py` FAIL=False（driftKeys=0 / unregistered=[]）；`node --check` SYNTAX_OK；CDP `DM_V891=PASS`（39 行逐行按表头 x 归位、三处订正、文案、指令、errs=[]）；发布链全审计绿。
- **未验证的假设**：①真实浏览器（非 headless）观感待用户验收；②`gen_sec_daily.py` 无参直跑能否成功刷新**未实测**（只在周轨指令里登记，脚本存在性已卡）；③`sources.json` 未覆盖数据集的真实渠道数未逐项核实，故未擅自补登。
- **下一步 + 别碰**：接手先 `& py _audit_dm_v845.py`（期望 FAIL=False）；三项口径已于 v892 拍板落地（见上方交接段），原「别碰」限制解除； `data-mgmt.json` 的 `antiHalluc`、`fund_jjcc` 的 time 路径、`sources.json` 的 `_note` 宣称。别回滚 DMCONFIG 双份同步（审计会立刻红）。
- **原待拍板三项**：已于 v892 全部落地，不再待拍板。

### 2026-11-10 · v890「原蓝＋爱马仕橙」正式落地·**已发布，线上 v890，待用户验收**
- 改了什么：用户拍板①原蓝＋橙 → `edit_work/index.html` 升 `verBadge v889→v890`（4,333,503 B，+939，CRLF=0）。`:root` 新增 `--accent-warm #FC8416` **单一真源**；`--ring` 原地 `rgba(63,93,248,.24)` → `rgba(252,132,22,.42)`（不制造双份定义）；`</body>` 前插 `<style id="fw2_v890_orange_accent">`。主色 `--brand #3F5DF8`、`--brand-ink #3a55d6`、15 处品牌蓝 rgba 派生、ECharts `CHART.brand #3a55d6`、语义色四值**全部不动**。写盘脚本 `_apply_orange_v890.py`。
- 新增资产：`_check_orange_v890.py`（CDP 20 项 computed 探针，含 hover 态与动态节点后置覆盖实证）；两份预览副本＋四个生成/检查脚本（配色预览配方资产，均不在发布清单）。
- 验证：静态 CSS 层 131 条配色规则 / 不达标 0 / 压线 0 / 四横线裸用 0（`_audit_contrast_css_v852.py` PASS 21）；CDP 渲染态九视图 `_audit_contrast.py` 合并聚类 **0**；`ORANGE_V890=PASS`；另 HTML 注释 0 隐患、var_paren 42、sig_unify 26、alloc 32/20/28 全 PASS。
- 未验证的假设：①真实浏览器（非 headless）观感待用户验收；②橙左条压原蓝底仅 2.05:1（图形建议 ≥3:1）已知偏弱——用户拍板的是预览所见，**未擅自加粗/描边**，若要补对比属一句话改动。
- 已完成发布：`push_gh_v39.py`（SKIP_GATE=1）全链绿 → `[200]` 4,333,503 B、head `2211bc38318b`；README 已同步推送；`git/blobs` sha `e1caba6ec456` ＋ Pages CDN 双路 **ONLINE_OK=True**（blob/page/local 三份字节完全相同、ver=890）。回读首次遇 `IncompleteRead` 网络中断 → 给回读加重试后通过（推送本体 `[200]` 早已成功，勿盲重跑发布）。
- 下一步：用户强刷验收（主按钮橙底深字含 hover、导航左条橙、语义色不变、数据密集页是否晃眼）；验收后清理两份预览副本 `preview_theme_b*.html`。
- 别碰：语义色 token、`--brand` 与 15 处 rgba 派生（v853 配方：改主色必须连派生一起换，是另一个量级的活）；勿把预览副本加进 `push_gh_v39.py` FILES。

### 2026-11-10 · 第二份配色预览「原蓝＋橙」三态对照·**已拍板①原蓝＋橙，落地见上方 v890 条**
- 背景：用户看完方案 B 预览后要求「在原蓝色的基础上配上橙色效果渲染下看」→ 新增 `edit_work/preview_theme_b2.html`（4,340,471 B），本地 `http://127.0.0.1:8918/preview_theme_b2.html`（会话内有效）。**默认「原蓝＋橙」**：`--brand #3F5DF8`、`--brand-ink #3a55d6`、17 处 rgba 派生、ECharts 线色/渐变全部保持真源原值，只新增 `--accent-warm #FC8416`（橙点缀规则与 B 完全一致）。工具条四按钮可切「方案 B 深蓝＋橙」/「原配色」/「说明」，一页横向比完三态。
- 生成/验证资产：`_make_theme_b2_preview.py`（占位符 replace 而非 `.format`，避开 CSS/JS 大括号转义）、`_check_theme_b2.py`（CDP **29 项三态全 PASS**：`THEME_B2_PREVIEW=PASS`；三态 `errs=[]`、资产配置表均 14 行、verBadge 仍 v889、`--accent` 未被橙污染）。注意真源 `--brand-ink` 是 `#3a55d6` 不是 `#3F5DF8`，探针首版断言写错产生 1 次假红已修。
- ★**本轮核心发现（影响拍板）**：橙点缀压在**原蓝底**上只有 **2.05:1**（图形元素建议 ≥3:1，会「发闷/发飘」），压在**克莱因蓝底**上有 **4.71:1**。同一份橙，深蓝才托得住撞色张力。若最终选「原蓝＋橙」，落地时建议把橙左条加粗或补深色描边补对比；其余橙场景（白底小色条/边框/焦点环）为装饰性，2.48:1 可接受但需静态层复扫确认。
- 真源 `index.html` 仍 v889 / 4,332,564 B **一字未动**，线上未发布；两份预览副本均不在 `push_gh_v39.py` FILES 白名单。
- 下一步：**等用户在三态间拍板**（原蓝＋橙 / 方案 B 深蓝＋橙 / 都不要）。任一通过 → 落 token 层（改 1 处定义＋派生同步）＋**双层对比度复扫（静态＋CDP 九视图）**＋升 verBadge＋README changelog＋发版；否决 → 清理 `preview_theme_b*.html` 与四个预览脚本即可，真源无需回滚。
- 别碰：真源 `index.html`；勿把任何预览副本加进发布清单。

### 2026-11-10 · 方案 B 配色（克莱因蓝＋爱马仕橙）预览·**用户已否决（拍板①原蓝＋橙），未落地未发布**
- 背景：用户问撞色能否用于工作台，三档 trade-off 后倾向 B；本轮要求「渲染一个页面我看完再决定」→ 已出**可切换预览副本** `edit_work/preview_theme_b.html`（4,338,844 B），本地服务 `http://127.0.0.1:8918/preview_theme_b.html`（会话内有效）。真源 `index.html` 仍线上 v889 / 4,332,564 B **一字未动**；副本不在 `push_gh_v39.py` FILES 白名单，不会被发布。
- 预览内容：默认进 B 态（克莱因蓝 `--brand #022A99`＋新增 `--accent-warm #FC8416`），右下角工具条可切「原配色」逐视图对比、点「说明」看改动点与实测对比度；切换走 localStorage＋reload，ECharts 线色/渐变同步。生成脚本 `_make_theme_b_preview.py`、CDP 验证 `_check_theme_b.py`（16 项全 PASS，两态均 `errs=[]`、资产配置表 14 行正常）。
- ★**落地前必读约束**：`--accent` 承担多处**文字色**，橙绝不能写进它（橙字白底仅 2.48:1）→ 新增独立 token 只用于非文字点缀（焦点环/导航左条/小色条/选中态边框/主按钮底配深字）；语义色涨红 `#b91c1c`、跌绿 `#047857`、警示琥珀 `#9a4708` 原封不动，橙只作「中性强调」不承载涨跌/警示。
- WCAG 实测：克莱因蓝白字 11.71:1（原 5.08）、橙白字 2.48:1（淘汰）、橙配 #101828 深字 7.14:1、橙配克莱因蓝字 4.71:1。
- 下一步：**等用户看完页面拍板**。若通过 → 按 v853 配方改 token＋rgba 派生，但**必须双层对比度复扫（静态＋CDP 九视图）**、升 verBadge＋README changelog＋发版（v852 教训：颜色从不生效变生效会带来新不达标）；若否决 → 只需清理预览副本与两个预览脚本，真源无需回滚。
- 别碰：真源 `index.html`（v889 已发布，勿在预览阶段改动）；日频自动化 21:30 仍按 rrule 运行，勿把预览副本误加进发布清单。

### 2026-11-10 · 资产配置表「主动权益」取消小计、逐只明细直出、家族名不入表（已发布，线上 v889）· 已交接
- 改了什么：用户指令「直接展示标的就可以，不用主动权益合计，主动权益不要显示在表格里」→ v888 小计行删除（`fw2_v888_*` 模板全清），该家族逐只明细直接渲染，明细行主题标签列改**空 td**——「主动权益」连同标签从表格 DOM 彻底消失；数据层 `IDX_FAMILY`/`idxFamily` 分组保留（仅展示层压制）。写盘脚本 `edit_work/_apply_active_flat_v889.py`。`verBadge v888→v889`，4,332,564 B。
- 验证：`node --check` SYNTAX_OK；`_audit_alloc_cols` 32 断言全 PASS（B06–B10 重锚 v889、B11–B15 负断言小计块/`esc(ftag)`/`offOf(att,atm,…)` 清零）；v873 20 / v874 28 全 PASS；CDP `_probe_alloc_v889.py` `ALLOC_FLAT_V889=PASS`（14 可见行、**「主动权益」表格零出现**、明细 4 只直出标签列空、组 rowspan 闭合、纳指100 5,000/标普500 `—` 不变、`errs=[]`）。线上 blob+Pages 双路 4,332,564 B 与本地字节一致。
- 新增资产：`_apply_active_flat_v889.py` + `_probe_alloc_v889.py`（PIPELINES P11 配方资产）。
- 未验证的假设：①真实浏览器（非 headless）观感待用户验收；②本次 push 后回读 GET 遇 `IncompleteRead` 网络中断（Traceback 在推送成功之后，发布本体 `[200]` 已确认）——属瞬时网络问题非脚本缺陷，复现再查。
- 下一步：用户线上强刷核 `v889`（CDN 约 1–2 分钟）：进攻/主题组见 000746/012920 明细行直接顶上（无小计行、无「主动权益」字样）、安全垫组 000912、对冲组 511260 同口径；指数行不变、列不右移。
- 别碰：`idxFamily`/`IDX_FAMILY` 与持仓页/热力图共用（禁改语义）；rowspan 公式 `(fam==='主动权益') ? rows.length : 1` 是审计 B10 锚点。
- 挂账（既往未变）：整元显示小计/明细 ±1 舍入配平待拍板（v888 引入，v889 小计已删、此挂账随小计行**自然消解**，仅合计行整元显示维持现状）；21:30 日频自动化双实例竞态未修。

### 2026-11-10 · 资产配置表「主动权益」＝小计行＋逐只明细（已发布，线上 v888）· 已交接（展示口径已被 v889 取代）
- 改了什么：用户指令「保留一行主动权益小计＋下方明细」→ v887 纯展开升级两层：`renderStratAlloc` 内该家族先出小计行（`subtotal-row`、`N 只标的·小计`、组内聚合目标/进度/实际，`offOf` 唯一实现）＋下方 v887 逐只明细；家族横跨多档位组各位置**各自出小计**（CDP 实证 3 处），rowspan＝1+明细数；计划外组同口径。写盘脚本 `edit_work/_apply_active_subtotal_v888.py`。`verBadge v887→v888`，4,335,613 B（含日频链 21:32 重嵌 +288 B）。
- 验证：`node --check` SYNTAX_OK；`_audit_alloc_cols` 扩至 **32 断言**（B10 重锚 v888 公式、B11–B15 小计模板）；v873 20 / v874 28 全 PASS；CDP `_probe_alloc_v888.py` `ALLOC_SUBTOTAL_V888=PASS`（17 可见行、行型三分、小计×3 与明细块对拍一致、无孤儿明细、`errs=[]`）。
- 新增资产：`_apply_active_subtotal_v888.py` + `_probe_alloc_v888.py`（PIPELINES P11 配方资产）。
- 未验证的假设：①真实浏览器（非 headless）观感与列宽待用户验收；②整元显示下小计与明细和可差 ±1/行（舍入噪声，探针容差放行）——若用户要求账面严格配平需改显示层（挂账未拍板）；③21:30 日频自动化**再次双实例启动**（两个 refresh_all 并行、各带一个 push_gh_v39）——本次产物字节无损坏，但双实例竞态属既有挂账（11-09 runner 失败标记矛盾同源），未修。
- 下一步：用户强刷核 `v888`；若要求小计严格等于明细显示值之和，拍板是否改「小计=明细显示值求和」口径。别碰：`refresh_all` 正在收尾（data-mgmt 回写/健康检查），等它退出后再动数据链。
- 别碰：`fw2_v888_*` 锚点注释是审计引用禁清；`_audit_alloc_cols.py` B10/B11–B15 与 v888 公式绑定。

### 2026-11-10 · 资产配置表「主动权益」展开为具体标的行（已发布，线上 v887，被 v888 小计＋明细取代）· 已交接
- 改了什么：用户截图圈「主动权益」行指令「需要展示具体标的」→ v886 的 `idxFamily` 末级兜底桶「主动权益」不是真实指数（CDP 实证混着 000746 招商行业精选 / 012920 易方达全球成长 / 000912 活期宝现金 / 511260 国债ETF），改为该家族**展开为逐只标的行**（代码/基金名/主题标签 + 各自真实目标/进度/实际/滞后/调仓/偏移），组头 rowspan 同步计入展开行数；其余指数家族聚合行不变；计划外组同口径。写盘脚本 `edit_work/_apply_active_alloc_v887.py`。`verBadge v886→v887`，4,332,491 B。
- 验证：`node --check` SYNTAX_OK；`_audit_alloc_cols` 扩至 **26 断言**（B06–B10 锁 v887 锚点）；v873 20 / v874 28 全 PASS；CDP `_probe_alloc_v887.py` `ALLOC_ACTIVE_V887=PASS`（14 可见行、6 位码仅在代码列、rowspan=6 闭合、4 只标的行数据真实、`errs=[]`）。
- 发布收口：`push_gh_v39.py`（SKIP_GATE=1）全审计链绿 → `[200] caifu/index.html` 4,332,491 B、head `b93e07ab71a1`；`_push_readme.py` BYTE_MATCH True（808,320 B）；线上核验 **ONLINE_OK=True**（git/blobs 权威口径 + Pages CDN 双路 4,332,491 B ver=887 与本地字节一致；raw 当日 404 传播异常，soft 证据不作数）。
- 新坑（已记 PITFALLS P23 ④⑤）：①审计锚点注释带尾注时查找串不能含 ` */`（find=-1 假红）；②GitHub contents API 对 >1MB 文件返回 `content=""`，权威回读必须走 `git/blobs/{sha}`（P 系流水线早有此口径，本次临时核验脚本踩同一坑）。
- 下一步：线上强刷核 `v887`：主动权益 4 只标的行（012920 目标 5,000/实际 10,608 等）、指数行不变、列不右移。
- 别碰：同 v886 条（idxFamily/锚点注释）；`fw2_v887_active_fund_row`/`fw2_v887_pl_fund_row` 锚点是审计引用。
- tag：`fw2_v887_active_expand`

### 2026-11-10 · 资产配置表按指数家族聚合、隐藏基金明细行（已发布，线上 v886）· 已交接
- 改了什么：`edit_work/index.html` 升 `verBadge v885→v886`，用户指令「明细只需要展示到指数合计（比如标普500、纳指100）」→ `renderStratAlloc()` 组内改按 `idxFamily(code)` 归并，每指数家族一行（`subtotal-row` + 首行 grpTds + rowspan=家族数），基金明细行彻底不渲染；纳指100 行目标=5,000（016452 承载）、标普500 行=`—`（计划外 target 0）；计划外组同口径聚合。写盘脚本 `edit_work/_apply_idx_alloc_v886.py`（行范围替换 + `newline=''` 保 LF）。**v885 限额制展示层（capOnly/tgtDisp）退役，数据层归桶不变。**
- 新增资产：`_probe_alloc_v886.py`（CDP 五断言）、审计重锚 `_audit_alloc_cols.py`（A05/A11/A12/B01–B05）、`_audit_alloc_lag_color_v874.py`（B02/B07/B09）。
- 未验证的假设：①真实浏览器（非 headless）观感与列宽**待用户验收**；②`idxFamily` 名称启发式对新入池基金自动归并未实测新样本——待核实；③511360/511260 交易入口 `purchase_check_failed` 仍挂账（既往）。
- 下一步：线上强刷核 `v886`：进攻/主题组只见指数行（纳指100 目标 5,000、标普500 `—`）、无逐只基金行、列不右移。发布已收口：`push_gh_v39.py`（SKIP_GATE=1）`[200] caifu/index.html` 4,329,101 B、head `05d0c32c9049`；`_push_readme.py` BYTE_MATCH True；三路核验 `_verify_online_v886.py` `ONLINE_OK=True`（API/raw/Pages 三路 4,329,101 B ver=886 与本地字节相同，核验脚本已删、正则口径见 PITFALLS P23 同款）。
- 别碰：`idxFamily`/`IDX_FAMILY`（持仓页/热力图共用）；`docs/data-ledger.json`；`index.html` 内 `fw2_v886_idx_row`/`fw2_v886_planoutside_row` 锚点注释（审计引用）。
- 验证记录：`node --check` SYNTAX_OK；三审计 21/20/28 全 PASS FAIL=0；CDP `ALLOC_US_V886=PASS`（13 可见行全对齐：5 组首行 13 列 + 8 续行 11 列、无 6 位基金码、rowspan=5 闭合、`errs=[]`）。
- tag：`fw2_v886_idx_alloc`

### 2026-11-10 · 资产配置表 标普500+纳指100 并入「美股宽基」共桶 5,000（已发布，线上 v885）· 已交接
- 改了什么：`edit_work/index.html` 升 `verBadge v884→v885`（4,333,706 B，LF），按用户截图「标普500 和纳指100 共用目标金额 5,000，进度/实际/滞后合计」做**限额制**合并：5,000 是「美股宽基」组的封顶预算，不拆给子行；子行只展示各自进度/实际/滞后，目标金额与目标占比对子行显 `—`，组头与小计显合计 5,000 / 10.00%。新增 `var CAP_ONLY_THEMES = { '美股宽基': true }`；`ALLOC_DEF` 016452 主题 `纳指100→美股宽基`（桶承载者，`STRATEGY_SNAP.assets['016452'].target=5000` 仍由 SNAP 持有，017641/096001/019441 计划外、target=0）；extra 块纳指/标普类 `xth` 归并「美股宽基」；`pileOf` 加 `|| xth==='美股宽基'`；`it.m` 目标列用 `tgtDisp`（capOnly 时 `null`→`—`）。写盘脚本 `edit_work/_apply_alloc_us_v885.py`。**未改全局 `code→theme` 映射表（避免影响持仓页/热力图家族聚合）；未改 `data/*.json`、`docs/data-ledger.json`、未推远端（线上仍 v884）。**
- 新增资产：`_apply_alloc_us_v885.py`（9 处精确替换 + 备份 `index_bak_v884_pre_us.html` + 自证）、`_probe_alloc_us_v885.py`（CDP 真渲染 + 列对齐 + 共桶断言）、`_probe_snap.py`（括号平衡解析定位 STRATEGY_SNAP 真值，实证 016452.target=5000、其余三只不在 SNAP）。
- 未验证的假设：①共桶后「进攻/主题」档位占比是否因四只并入「美股宽基」而需重新校准（页面仍按 SNAP target 求和，未实证数值漂移）——**待核实**；②真实浏览器（非 headless）字体/滚动**待核实**；③511360/511260 交易入口 `purchase_check_failed` 仍挂账（既往）。
- 下一步：发布 `& py push_gh_v39.py`（`SKIP_GATE=1`）→ `& py _push_readme.py` → 线上强刷核 v885，确认美股宽基小计=5,000、四只子行目标列=—、无独立标普500/纳指100 小计；随后验收 `& py _probe_alloc_us_v885.py` 期望 `ALLOC_US_V885=PASS`。
- 别碰：全局 `code→theme` 映射表（持仓页/热力图依赖）；`docs/data-ledger.json`；`index_bak_v884_pre_us.html` 回滚备份；`data/_hist_cache`。
- 验证记录：静态 15 项 `rc=0`（check_js 20 块 ALL OK / HTML 注释 0 隐患 / `HOLDCONSISTENCY=PASS` / `MANIFEST=PASS 34` / cross_module FAIL=0 / v873–v876 各硬卡全 PASS / trade_entry 34/34）；CDP `VER=v885` / 表头 13 列 / 美股宽基小计 `目标=5,000 占比=10.00% 进度=834 实际=258 滞后=-576`（四只合计）/ 016452/019441/017641/096001 目标列=— / 无独立标普500/纳指100 小计 / `errs=[]` / 真渲染截图无错位溢出（`ALLOC_US_V885=PASS`，探针列对齐断言首版误判首组小计行 13 列、已改为「列集合 ∈ {[0..12],[2..12]}」放行）。
- tag：`fw2_v885_us_broad`
- **发布记录（2026-11-10）**：随 `push_gh_v39.py`（SKIP_GATE=1，其无条件静态链含 `_audit_alloc_cols`/`_audit_alloc_color_v873`/`_audit_alloc_lag_color_v874`/`_audit_nav_freshness_v883` 全过）+ `_push_readme.py` 发布，线上 v885。GitHub API + Pages CDN 双路核验 `verBadge=v885`。

### 2026-11-10 · 日频自动化 rrule 第二次漂回 20:30（已复位 21:30 并 view 回读） · 已交接
- 改了什么：收尾实证时 `automation_update view` 查唯一日频自动化 id `b1109994-5d76-4e8a-b728-8ab3c0b97f6e`，status ACTIVE 但 `rrule=FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=20;BYMINUTE=30`（**实际 20:30**），与 prompt 首句、页面 `verify_sync` 标记串「每晚 21:30 自动」全不一致。这是 11-07 已修过的**同型第二次漂移**（`.workbuddy/memory/2026-11-07.md` L102-109 曾把 `BYHOUR=20` 改回 21 并回读确认 `nextRunAt=11-09 21:30`）。按既定规则只改 rrule（`automation_update update` 仅传 id+rrule → `BYHOUR=21;BYMINUTE=30`），`view` 回读确认持久化、`nextRunAt=1794317400000`＝**2026-11-10 21:30 +08:00**（UTC 13:30）；prompt／页面／硬卡一字未动，避免制造第三处漂移。零本地文件改动、零远端推送。
- 新增资产：无（仅服务端调度配置复位）。
- 未验证的假设：①11-09 `holdings-data.json syncedAt=20:36:17`、`gold-data.json` 20:35 落在 20:30 档，时间吻合这一跑，但**究竟是自动化那一跑还是手工触发，未取证**——待核实；②「20:30 偏早 ⇒ pingzhongdata 尚未追平 ⇒ 双通道不一致窗口变宽」只是时间吻合的**推测**，v883 主因仍是旧 `x = None; src = x or y` 下沉旧源（日志铁证），不可倒置因果——待核实；③rrule 为何会二次漂移（时区换算／编辑器默认值／同步覆盖）根因未查——待核实。
- 下一步：每个 AI 接手／收尾都用 `automation_update view`（id 见上）实证 `rrule` 并把 `nextRunAt` 换算成北京时间，**别拿 prompt／页面文案当证据**；今晚 21:30 跑完后 `& py _audit_nav_freshness_v883.py` 期望 `AUDIT=PASS 36/36`，并看 4 只国内 `navDate` 是否补齐到 11-09。可考虑把这条列进开工门禁第 5 步（需用户拍板）。
- 别碰：prompt 的「21:30」文案、页面 `verify_sync` 标记串「每晚 21:30 自动」（改文案会踩硬卡并制造第三处漂移）；`docs/data-ledger.json`；`index.html` 版本号；未授权不推远端。
- tag：`fw2_v883_rrule_drift2_20261110`

### 2026-11-10 · 持仓净值日期 6号/9号分叉：双通道下沉旧源已修（已发布，线上 v884）· 已交接
- 改了什么：用户指出「有些 6 号有些 9 号，QDII 要理解时间差，但国内 A500 竟只到 6 号」。实证 `holdings-data.json` `syncedAt=2026-11-09T20:36:17+0800`、24 只 `navDate` 分布 11-05(4)/11-06(14)/11-09(6)；`data/fund-daily.json` 末点 4 只国内=**11-09**、QDII=**11-06**；`_refresh_logs/refresh_holdings_group.log` L7-18 记录 8 只「净值双通道不一致 east=新值 ping=旧值，保留旧净值」。根因＝`edit_work/refresh_holdings_ttskill.py` 旧 `x = None; src = x or y` **静默下沉到较旧通道**，把东财已披露的新净值丢掉，日志「保留旧净值」还与行为不符（实际写入 ping 值）。修法：新增 `choose_nav(x,y,fd)`（取 navDate 较新者 + `fd_latest_map()` 日期仲裁，仲裁不了返回 None 由 `if src:` 真正保留原值）与 `fd_latest_map()`；★仲裁是**同口径**（fund-daily 的 navSource 同为东财 lsjz），只判「谁更新」、不冒充独立第二源，已在代码里写明。页面 `index.html` 升 `verBadge v882→v883`（4,332,668 B，LF）：新增 `navDateVerdict()` 分层（QDII/海外不告警 + title 解释 T+1~T+2；国内 `navDate < state._pfAt` 标「·滞后」），现价列小字补 title。`_audit_nav_freshness_v883.py` 已挂 `push_gh_v39.py` 发布闸门。**未重跑数据链、未手改 `data/*.json`、未推远端**（线上仍 v881）。
- 新增资产：`refresh_holdings_ttskill.py`（改，含 `choose_nav`/`fd_latest_map`）、`_audit_nav_freshness_v883.py`（32/36，含 8 组实证 + 2 负向 + 1 一致动态自测、源码防回归、国内 FAIL/海外 WARN 分层、空 PASS 防护）、`_apply_nav_date_v883.py`、`_probe_hold_dates.py`（CDP 真渲染 + 分层标注断言 + 截图）、`_probe_hold_dates_raw.json`、回滚备份 `index_bak_v882_pre_navdate.html`、`push_gh_v39.py`（挂硬卡）、`docs/` 四件套 + README + 当日 memory。
- 未验证的假设：①**今晚 21:30 日频自动化是否真跑、跑完 4 只是否补齐，未实证**（rrule 是唯一调度真源，页面宣称不算）——**待核实**；②修好后 nav 由 11-06→11-09 会让 `shares×nav` 与账户 `marketValue` 出现小额差（022438 约 0.4 元），预期由 `pendingBuy` 吸收并触发份额 WARN，但**未实跑** `check_hold_consistency.py` 验证不 FAIL——**待核实**；③`pingzhongdata` 追平后自动恢复双源对拍的时点**待核实**；④`_refresh_logs/runner_2026-11-09.log` 显示 3 个失败步骤且「data-mgmt 生成失败」，但 `handoff_check.py` 报 `refreshFailed=[]`，疑似失败标记丢失，**本轮未查证、未修**；⑤真机（非 headless）浏览器字体/滚动**待核实**。
- 下一步：①`& py handoff_check.py` 看 4 只 `navDate` 是否变 11-09；`& py _audit_nav_freshness_v883.py` 期望 `AUDIT=PASS 36/36`；②若仍滞后，按死规则①跑**完整** `& py refresh_all.py`（全刷所有数据集），**禁止手改 `data/*.json` 冒充更新**；③数据补齐后才可发布：`& py push_gh_v39.py`（新鲜度硬卡此时才放行）→ `& py _push_readme.py` → 线上强刷核 `v883`；④`& py _probe_hold_dates.py` 期望 `V883_LABEL_CHECK=PASS`；断言已**动态化**（`expected` 由「国内行 navDate < 账户同步日」实时算出，不写死 4 只清单），数据补齐后 `EXPECTED_STALE` 与 `FLAGGED` 自动双双归零，仍由「国内≥5 / 海外≥10 行 + title 全非空」防空 PASS。
- 别碰：`_trade_entry_v1.py` 的 PLAN 与 `_audit_trade_entry_v1.py`（授权锁定、口径已失效）；`docs/data-ledger.json`（本轮**未改数据链路**，`verify_manifest.py` 已 `MANIFEST=PASS 34/34` 证实，改它反而制造无意义分叉）；`index_bak_v882_pre_navdate.html` 回滚备份；`data/_hist_cache`；README 版本史（并行 AI 在编辑，行号会漂）；当前 `AUDIT=FAIL` 的 4 条数据滞后**不要手改文件消红**，它是发布闸门在如实挡住历史脏数据。
- 验证记录：静态 15 项 `rc=0`（check_js 20 块 ALL OK / HTML 注释 189 处 0 隐患 / `HOLDCONSISTENCY=PASS` / `MANIFEST=PASS 34` / cross_module FAIL=0 / v873–v876 各硬卡全 PASS / trade_entry 34/34）；新硬卡 `AUDIT=FAIL 32/36`，4 条 FAIL 全是 11-09 历史数据滞后（预期，会阻断发布至日频链补齐）；`choose_nav` 单测 8 组日志实证 + 2 负向 + 1 一致全 PASS（旧逻辑对照会写入 11-06/11-05）；CDP `VER=v883` / `DOMESTIC_STALE_FLAGGED=4/4` / `OVERSEAS_CHECKED=15`（海外零误标）/ `errs=[]` / 真渲染截图「净值11/06·滞后」只出现在 A 股行、无错位溢出；`COLOR_CHECK=PASS`（超前蓝 8 / 滞后红 12 / 绿色 0）。
- tag：`fw2_v883_nav_stale_20261110`
- **发布记录（2026-11-10）**：随 v884 发布（线上 v884 = v882+v883+v884 三版合一）。完整 `refresh_all.py` 后 4 只国内基金 `navDate` 由 11-06→11-09（022438/022676/023917/012761），`_audit_nav_freshness_v883.py` 转 `AUDIT=PASS 36/36`；发布前探针抓到 v883 参照回归并已用 v884 `domNavMax` 修正（见 `PITFALLS.md` P20），最终 `V883_LABEL_CHECK=PASS`/`EXPECTED_STALE=[]`/`FLAGGED=[]`；GitHub API + Pages CDN 双路核验 `verBadge=v884`。

### 2026-11-10 · 安全垫改活期宝 5,000 / 删 511360（已发布，线上 v884）· 已交接
- 改了什么：`edit_work/index.html` 升 `verBadge v881→v882`（4,330,723 B，LF），按**五处同源**收口计划配置——`STRATEGY_SNAP.assets/plan/first` 三处 511360→000912（target 5,000）、`firstInvest 4500→3938`、`ALLOC_DEF`、`roleCodes/roleNames`、`SIGNALS_CFG.barbell.funds` bond 档 `w:10`，另同步 `heldBadge` 弹药池徽标与再平衡建仓提示；`monthlyNominal 4169` **刻意不动**（名义月投额，等量替换总额不变）。写盘脚本 `edit_work/_apply_alloc_cash_v882.py`。**未改数据链路 / `data/*.json` / `docs/data-ledger.json`；未推远端，线上仍 v881。**
- 新增资产：`_apply_alloc_cash_v882.py`、`_probe_cash_000912.py`（实证 cash 行 `cost=1 / nav=1 / qty=5121.43`，故 `priceOf(cash)` 不会产出 `qty×cost` 脏市值）、`_probe_v882_visual.py`（逐行按表头 x 断言列位 + 真渲染截图）、`_probe_progress_before_v881.json` / `_v882_visual_raw.json` / `_probe_cash_raw.json`、回滚备份 `index_bak_v881_pre_cash.html`。
- 未验证的假设：①`monthlyNominal 4169` 判为「11 只按 target÷12 的名义月投额」而非 `plan` 数值项之和（原 3752），因无消费点仅元数据，等量替换故不动——**待核实**；②511260 仍是场内 ETF，上一轮 `purchase_check_failed` 未解决，**待核实**；③活期宝作申购支付通道、安全垫现金能否直接动用，**待核实**；④本地 v882 未在真机（非 headless）浏览器核对字体/滚动，**待核实**。
- 下一步：①用户拍板新补齐口径 **3,250 元**（016452 779 / 012761 632 / 023917 631 / 000307 430 / 511260 416 / 022438 362）与**钱从哪来**——活期宝 5,121 已锁定 5,000 作安全垫目标，仅余 **121** 可用；②`_trade_entry_v1.py` 的 PLAN 仍是旧 7 只 / 4,084（含已删 511360），授权范围已失效，**须重新授权才可再执行**；③发布：`& py push_gh_v39.py`（`SKIP_GATE=1`）→ `& py _push_readme.py` → 线上强刷核 v882；④验收命令 `& py _probe_v882_visual.py` 期望 `VISUAL_CHECK=PASS`、`HAS511360=False`。
- 别碰：`_trade_entry_v1.py` 的 PLAN 与 `_audit_trade_entry_v1.py` 的 34/34 断言（授权锁定）；`FUND_PROFILES_MIRROR` / `FUND_LX_RAW` / URL 映射 / `data/*.json` 里剩余的 15 处 511360（数据层与历史注释，删了破坏历史序列）；README 版本史（并行 AI 在编辑，行号会漂）。
- 验证记录：静态 15 项 `rc=0`（`check_js` 20 块 ALL OK / HTML 注释 189 处 0 隐患 / `check_hold_consistency` FAIL=0 / `MANIFEST=PASS` 34 项 / `cross_module` FAIL=0 / v873–v876 各硬卡全 PASS / trade_entry 34/34）；CDP `VER=v882`、`ASSETS=11` 合计 50,000、表 13 列 29 可见行无重复列、`HAS511360=False`、`CASH_ROW 5,000 / 5,121 / -121 / -2.4%`、`COLOR_CHECK=PASS`（超前蓝 8 / 滞后红 12 / 绿色 0）、两张真渲染截图无错位溢出；补齐缺口 4,084→**3,250**。
- tag：`fw2_alloc_cash_v882_20261110`
- **发布记录（2026-11-10）**：随 v884 发布（线上 v884 = v882+v883+v884 三版合一）。活期宝目标 5,000 / 删 511360 已上线；补齐口径 3,250 元仍待你定资金来源与重新授权（`_trade_entry_v1.py` 旧 4,084 清单已失效）。GitHub API + Pages CDN 双路核验 `verBadge=v884`。

### 2026-11-10 · 跨 AI 交接体系落地（第一版） · 已交接
- 改了什么：新增 `docs/DATA_LEDGER.md`、`docs/data-ledger.json`（34 个数据集）、`docs/PIPELINES.md`、`docs/PITFALLS.md`、`docs/INBOX.md`；新增 `edit_work/handoff_check.py`（7 段状态出口）与 `edit_work/verify_manifest.py`（已挂 `gate.py` 的 `manifest` 数据集，`MANIFEST=PASS` 34/34、2 项真实告警）；AGENTS.md 增「开工三步 / 收尾三行」；README 加「关键入口」表并修三处过时值（月度 81 只·7,382 行·1,330,695 B / 日频 103 只·181,694 行 / 交接入口 → docs/INBOX.md）。**未改 `index.html`，chip 仍 v881。**
- 新增资产：`verify_manifest.py`（离线秒级校验「台账 ↔ 生产者 ↔ 发布清单 ↔ 闸门 ↔ 链组名」）；`handoff_check.py`（断点/新鲜度/闸门/待办一条命令）。
- 未验证的假设：①README「关键文件」节里的历史条目未逐条重核（只修了被实证过时的三处）；②台账「手工轨」判定基于全仓 grep 调用点，未逐个实跑验证这些脚本当前还能跑通；③`docs/` 四件套**尚未在 `push_gh_v39.py` 的 FILES 里**，所以 GitHub 仓库上还没有它们——本地接手的 AI 读得到，只读远端的 AI 读不到（待定是否入库）。
- 下一步：新 AI 首次接手按 AGENTS.md 跑 `handoff_check.py`；如继续治理，把台账「已知盲区」四条排成任务（fund_jjcc 生产者重建 / gold 加校验器 / amtD 第二源 / macro_extra 挂链或下线）。
- 别碰：`refresh_all.py` 的组顺序（并行/串行约束见 PIPELINES P0）；`data/_hist_cache`（删了要重抓全部历史）。
- **后续（同日定案）**：`docs/` 与两个脚本确定**只存本地**、不进 `push_gh_v39.py`；新增 `CLAUDE.md`、`.cursorrules` 两个指路垫片（正文仍只在 `AGENTS.md`）。本机三工具各自是否自动加载规则文件未验证，接手的第一个 AI 若能自己念出「开工三步」即说明加载成功。
- **验证记录（2026-11-10）**：上述「未验证」已闭环——豆包工作 / Trae / 千问办公 用同一问句「按本目录的规则，开工第一步做什么？」自检，三家均准确复述「开工三步」+ 门禁条件，无幻觉。**仍未验证**：它们会不会真的去跑 `handoff_check.py`、能不能只读 `docs/` 答对三条口径（`DATA_LEDGER.md` 第 6 节已给出答案，可用于对照）。

### 2026-11-10 · v881d 前端口径 + 四处数据盲区收口 · 待接手（含 2 项残留）
- 改了什么：新建 `docs/FRONTEND.md`（五条前端硬口径 + 9 个函数落点 + 6 条误改 + 5 步验证）；重建 `edit_work/gen_fund_jjcc.py`（`fw2_v881d_jjcc_chain`）并挂进 `SERIAL_AFTER` 的 `jjcc` 组；`gen_macro_extra.py` 挂进 `G macro`（`fw2_v881d_macro_extra_chain`）；新增校验器 `_verify_gold.py` / `_verify_amt_consistency.py` / `_verify_macro_extra.py` 并挂进 `gate.py` 三个新数据集；`refresh_all.py` / `gate.py` / `docs/data-ledger.json` / `docs/DATA_LEDGER.md` / README 同步。**未改 `index.html`，chip 仍 v881。**
- 新增资产：上述三个校验器 + `gen_fund_jjcc.py`；`docs/FRONTEND.md`；`docs/` 六文件云端备份 URL：DATA_LEDGER `https://aka.doubaocdn.com/s/VP8ndJ4Z5D` ／ data-ledger.json `https://aka.doubaocdn.com/s/n7JUHIm63j` ／ PIPELINES `https://aka.doubaocdn.com/s/McPnJf3NHe` ／ PITFALLS `https://aka.doubaocdn.com/s/iekJaFZyMJ` ／ INBOX `https://aka.doubaocdn.com/s/8greD4j4Ox` ／ FRONTEND `https://aka.doubaocdn.com/s/qOozlskLmv`（**只是备份/给别的 AI 传，不是真源**）
- 未验证的假设：①`gen_fund_jjcc.py` 解析正确性只对 4 只做过逐字段对拍（000746/000834/012752/000307，与旧文件完全一致），其余 20 只靠结构同构推断；②`real_estate` 同比≈92、`exports` 末点 2025-08 的真实成因**未定源**（只确认「不合理」，没确认「该取哪一列」）；③`jjcc` 挂进日轨后，夜刷耗时增加未实测（24 只并发 6，单只约 1–2s）；④云端 URL 的有效期未确认。
- 下一步：`& py gate.py --datasets gold --check`（期望 `GOLD=PASS`）／`--datasets amt_consistency`（`AMTCONS=PASS`）／`--datasets macro_extra`（`MACROEXTRA=PASS` 5 告警）／`& py verify_manifest.py`（`MANIFEST=PASS` 34/34、1 告警）。要修 `macro_extra` 的两处可疑值，先查 akshare 该函数返回列的实际含义，**不要照现有 91.45 反推口径**。
- 别碰：`jjcc` 组位置（必须在 `holdings` 之后，它刷的是 holdings 里那批代码）；`docs/data-ledger.json` 的 `fund_jjcc.asof` 必须保持 `null`（结构决定，加 meta 会改变前端语义）。
- **反向继承（仍待用户实操）**：需另一家 AI 做一件小事后按模板写回本文件；模板给了，但还没有第三方真实写过一条——这是「传承」最后一块未验证的拼图。

### 2026-11-10 · P1-2 台账补录（阻塞中） · 进行中
- 改了什么：`edit_work/_repair_trades_v880.py` 已就绪（默认 dry-run）。
- 新增资产：无。
- 未验证的假设：`ledger-import.json` 68 笔 / 10 代码与 ttskill 账户流水是否已完全对齐（待跑 `--apply` 后由 `_audit_holdings_linkage.py` 反证）。
- 下一步：ttskill 每日配额恢复后 `& py _repair_trades_v880.py --apply`，再跑 `_audit_holdings_linkage.py`（期望 WARN 3→0）、`_audit_cross_module.py`（WARN 16→收敛）。
- 别碰：14 只缺口代码（000307 等）在补齐前不要改 `holdings-data.json` 的份额。

### 2026-11-10 · 冷启动接手自证 + 反向继承写回（零工程改动） · 已交接
- 改了什么：`docs/INBOX.md` 追加本条（按模板真实写回，闭环 v881d 条目 L35 标记的「反向继承仍待用户实操」）；`docs/PITFALLS.md` 追加 P11 / P12 两条路由与环境坑。**未改** `index.html`、`data/*.json`、`docs/data-ledger.json`、`gate.py`、`refresh_all.py`、README；chip 仍 v881。tag `fw2_handoff_selfcheck_20261110`。
- 新增资产：无。
- 未验证的假设：①README「关键入口」节本次实测在 L678，但本会话内已从 L672 漂到 L678（并行 AI 正在编辑），行号只代表 10:38 快照，下次接手须重新 Grep 定位（待核实）；②PowerShell 中文 stdin 乱码的根因推断为 PowerShell 5.1 管道走系统 ANSI 编码，未做字节级取证（待核实）；③`docs/AGENT_PROMPT.md` 只做了措辞定位 Grep、未通读全文（按「只读关键入口表」约束），与 `AGENTS.md` 是否有其它分叉未逐条对拍（待核实）。
- 下一步：`& py handoff_check.py`（期望 README `updated=2026-11-10`、滞后 >7 天 10 条且全为 `[manual]`、自动链无 >7 天；数字随刷新变化，以当次输出为准）→ `& py verify_manifest.py`（期望 `MANIFEST=PASS`）。若要根治 P11，统一 `AGENTS.md` L17 / `docs/AGENT_PROMPT.md` L23 / README「下一步」三处「顶部」措辞为「按标题 Grep 定位」，**需先确认没有并行 AI 正在改这三份文件**。
- 别碰：`refresh_all.py` 组顺序、`data/_hist_cache`、`jjcc` 组位置（必须在 `holdings` 之后）、14 只缺口代码在 P1-2 补齐前不要改 `holdings-data.json` 份额、`docs/data-ledger.json` 的 `fund_jjcc.asof` 保持 `null`。
- **验证记录（2026-11-10 10:38）**：按四步顺序真跑 `handoff_check.py`（rc=0）；README 836 行 / 438,767 字符 / updated 2026-11-10；`next` 首条＝「v881d 前端口径 + 四处数据盲区已收口」；最近闸门 2026-11-10 10:29（1 组 `manifest PASS`）、最近全量 2026-11-10 00:51（7 组全 PASS）；滞后 >7 天 **10 条全为 `[manual]`**，与 `DATA_LEDGER.md` §4 手工轨判定一致 → **门禁通过**。本轮无改动任务，未动任何数据/前端。

### 2026-11-10 · 策略执行「补齐投资进度」只读测算 · 已交接
- 改了什么：新增只读 CDP 探针 `edit_work/_probe_alloc_progress.py`（取 `#view-strategy .alloc-tbl` 13 列真渲染值，展开折叠行后按表头 x 对齐取列）＋产物 `edit_work/_probe_progress_raw.json`；本文件追加一条。**未改** `index.html`、`data/*.json`、`docs/data-ledger.json`、README；chip 仍 v881。tag `fw2_alloc_progress_probe_20261110`。
- 新增资产：`_probe_alloc_progress.py`（PORT 8913 / DPORT 9413，复用 `_probe_alloc_color.py` 的连接骨架）。
- 未验证的假设：①`012920` 实际 10,608 > 目标 5,000，代码注释称「已达标→`liveMonthly=0`→进度金额=0」，但页面进度金额实测 **834**（417×2）；推断为 `gapOf/heldOf` 未命中该标的（`holdings-data.json` 里 012920 的 `qty=null`、只有 `marketValue=10608.4` / `nav=3.0986`），**未逐行读 `heldOf` 取证**（待核实）；②页面「5 万计划 / 11 只 / 12 期」与项目长期约定「CAP 10 万 / 8 只半杠铃」是否属同一套参数未与用户确认（待核实）。
- 下一步：`& py _probe_alloc_progress.py`（期望 `VER=v881`、`ME` 随「当月 20 日界」变化、`SUM need_now` 与本条记录对得上）；查 012920 异常先读 `index.html` L19962 `heldOf` / L19975 `mvOf` / L20013 `gapOf`，再对拍 `state.portfolio` 与 `holdings-data.json` 的 qty 来源。
- 别碰：`liveMonthly` / `_monthsElapsed` 口径（用户 2026-10-09 拍板「9 月起 12 个月、固定分期、不考虑剩余资金」）；「当前月 ≥20 日才计入」的期数规则；`data/_hist_cache`；14 只缺口代码在 P1-2 补齐前不要改 `holdings-data.json` 份额。
- **测算结果（2026-11-10 10:47，页面 `_ME=2`）**：补齐到当前进度＝**7 只 / 4,084 元**（511360 834、016452 779、012761 632、023917 631、000307 430、511260 416、022438 362）；连 11 月这期一起投＝**6,794 元**。001015 / 160422 / 012920 已超前，020712 为日限额 10/日，均不补。

### 2026-11-10 · 天天基金交易入口能力边界裁定（红线未授权，零工程改动） · 待接手
- 改了什么：`docs/INBOX.md` 追加本条、`docs/PITFALLS.md` 追加 P15。**未改** `index.html`、`data/*.json`、`docs/data-ledger.json`、`AGENTS.md`、README；未调用任何交易入口、未推远端。tag `fw2_trade_entry_boundary_20261110`。
- 新增资产：无（只读调研，未落脚本）。
- 未验证的假设：①用户「只需确认密码/支付指纹」是否等于同意修改 `AGENTS.md` L10 红线（待用户拍板，本轮未替其判定）；②`FUND_TRADE_ENTRY` 的 `open_h5` 在本机 prod 能否真打开、7 只标的里哪几只会被 `purchase_unavailable` 拦下（**未实跑，待核实**）；③`items` 多基金入口对场内 ETF（511360 / 511260）的实际返回未测，`SKILL.md` L34 只接受 `SpecialFundType===-1`、L88 禁止自动把 ETF 换成联接，推断大概率被拦（待核实）；④`RATION_PLAN` 只查询不新建系由 `files` 仅 `plan_list`/`plan_result` 推断，未通读其 `SKILL.md`（待核实）。
- 下一步：先由用户明确授权范围（是否允许接生产交易入口）与补齐口径（4,084 补 2 期 / 6,794 含 11 月）；授权后先只读取证 `ttskill skill info FUND_TRADE_ENTRY --json`（期望 `env=prod`）与 `ttskill status --json`（本轮已实测 `has_token=true` / `is_expired=false`），**不要直接跑 `run-script open_h5`**；若要落地执行链，须同步改 `AGENTS.md` L10 与 `docs/PIPELINES.md`，并把「逐项 `results[].opened` 才算打开」写成验收硬卡。
- 别碰：`AGENTS.md` L10 红线（未经用户明确授权不得改）；`ttskill` 登录态与任何凭证字段（`status --json` 的 `auth` 只取布尔值，禁止打印 token/Cookie）；`refresh_all.py` 组顺序；14 只缺口代码在 P1-2 补齐前不要改 `holdings-data.json` 份额。
- **实证记录（2026-11-10 10:58）**：本机 ttskill 0.1.2 / `env=prod` / 已装 39 个 enabled skill，含 `FUND_TRADE_ENTRY` 1.0.1、`CONDITION_ORDER` 1.0.0、`RATION_PLAN` 1.0.0。`FUND_TRADE_ENTRY/SKILL.md` L9「Agent 仅负责…登录和打开页面…不代替用户提交交易」、L51「银行卡、协议、密码和最终确认均在页面完成」、L53 `amount` 只作 H5 预填、L104 `status=batch` 只表示汇总须逐项看 `results[].opened`、L142「CLI 退出码为 0 不等于页面打开成功」、L152 `commit_order` 等 action 保留给已鉴权 H5 且 Agent 不直接调用、L154「不自动提交买入、卖出、撤单」。`CONDITION_ORDER/SKILL.md` L5/L22 明确「仅提供条件单查询能力，不提供新建、修改…或其他交易操作」。工程侧 grep：`edit_work/*.py` 只有 `ACCOUNT_HOLDING` / `TRADE_QUERY` 只读调用，`index.html` 唯一含「下单」处是注释「非自动下单」→ **工作台本体纯只读，交易入口未接入**。

### 2026-11-10 · 补齐口径定稿：4,084 元（补 2 期） · 已交接
- 改了什么：`docs/INBOX.md` 追加本条；按用户 11:04 拍板把补齐口径锁定为「补当前 2 期＝**4,084 元**」（非连 11 月的 6,794）。**未改** `index.html`、`data/*.json`、`docs/data-ledger.json`、`AGENTS.md`、README；未调用交易入口、未推远端。tag `fw2_alloc_4084_final_20261110`。
- 新增资产：无（清单由既有 `edit_work/_probe_progress_raw.json` 重算得出，未落新脚本）。
- 未验证的假设：①511360 / 511260 场内 ETF 能否在天天基金账户买入（`FUND_TRADE_ENTRY/SKILL.md` L34 只接受 `SpecialFundType===-1`、L88 禁自动换联接，推断会被拦，未实跑 `open_h5` 取证，待核实）；②活期宝 000912 的 5,121 元能否直接作申购支付方式（工程侧无对应接口，`cashbag_available_share` 保留给已鉴权 H5 且 Agent 不直调，待核实）；③`012920` 进度金额 834 与「已达标应为 0」注释矛盾的根因仍未取证（承接上一条，待核实）。
- 下一步：`& py handoff_check.py`（本轮已跑 `rc=0`：README 836 行 / 438,767 字符 / updated 2026-11-10，滞后 >7 天 10 条全 `[manual]`）→ 若要执行，先由用户明确授权范围并改 `AGENTS.md` L10；授权后按本文件「交易入口能力边界裁定」条的只读取证顺序，**不要直接跑 `run-script open_h5`**。
- 别碰：`AGENTS.md` L10 红线；`ttskill` 任何凭证字段；`refresh_all.py` 组顺序；14 只缺口代码在 P1-2 补齐前不要改 `holdings-data.json` 份额；`docs/data-ledger.json` 的 `fund_jjcc.asof` 保持 `null`。
- **定稿清单（页面 v881 真渲染，持仓 asOf 2026-11-09，测算 2026-11-10）**：进度金额＝`liveMonthly×_ME`（`_ME=2`，11-10 未到 20 日故 11 月不计期）；补齐＝进度金额−实际金额。022438 **362**／016452 **779**／012761 **632**／023917 **631**／000307 **430**／511360 **834**／511260 **416**，合计 **4,084**。活期宝 000912 实际 **5,121**，覆盖后余 **1,037**；排除两只场内 ETF 后可立即执行＝**5 只 / 2,834**。整体合计行「进度滞后 **+13,471**」是**超前**，由 012920 +9,774／001015 +1,333／160422 +341 等超配标的贡献，与「逐只补齐」不矛盾：本口径是**新增投入**，不是从超配标的调仓。

### 2026-11-10 · 用户授权 B：接交易入口（受控例外，本机执行链） · 已交接
- 改了什么：用户 11:08 明确选 B。`AGENTS.md` L10 **保留原红线原句**、追加四条受控例外；新增 `edit_work/_trade_entry_v1.py`（默认 dry-run、`--open` 才打开、金额锁定 4,084、逐项验 `results[].opened`、零凭证输出）与 `edit_work/_audit_trade_entry_v1.py`（静态硬卡 + 检测器自测）；`docs/PIPELINES.md` 增 P7、`docs/PITFALLS.md` 增 P16/P17、本文件追加本条、README「当前进度/下一步」同步。**未改** `index.html`、`data/*.json`、`docs/data-ledger.json`、`gate.py`、`refresh_all.py`；chip 仍 v881。tag `fw2_trade_entry_v1_20261110`。
- 新增资产：`_trade_entry_v1.py`、`_audit_trade_entry_v1.py`、`_trade_input_v1.json`（输入快照，无凭证）。**都不进 `push_gh_v39.py` 的 FILES**（本机链，docs 与本机脚本只存本地）。
- 未验证的假设：①`opened=true` 只证明 `Start-Process` 成功（L465）；**11:15 复核到 5 个 `msedge` 进程在 `--open` 时段启动（11:15:26–11:15:46，只取进程名 / ID / StartTime，**未读命令行**以免接触凭证 URL），数量与 5 只成功打开吻合 → 系统层面窗口已启动**；但「窗口是否在前台可见、会话隔离下用户能否看到」仍未取证，待核实；②H5 网页版是否支持指纹确认（官方文档只写「密码和最终确认」，待核实）；③URL hash 内凭证 envelope 出现在 Windows 进程命令行的实际暴露面（官方实现，只读代码推断，未做进程列表取证，待核实）；④预填 `amount` 是否真的显示在页面上（只证实参数进入 URL query，未做页面渲染取证，待核实）；⑤prod 环境 `purchase_check_failed` 无 diagnostics（L481/L603 仅 test 附带），**根因无法归因，待核实**。
- **执行记录（2026-11-10 11:08，tag `fw2_trade_entry_v1_20261110`）**：`_audit_trade_entry_v1.py` `AUDIT=PASS 34/34` → `_trade_entry_v1.py` `CHECK=PASS`（prod、登录态有效、7 项合计 4,084）→ `--open` 实测 `OUTCOME=partially_opened`、`OPENED_COUNT=5/7`、`NEEDS_LOGIN=False`、`OPEN=PARTIALLY_OPENED`。**已打开 5 只**：016452 779 / 012761 632 / 023917 631 / 000307 430 / 022438 362（合计 **2,834 元**预填）。**未打开 2 只**：511360 834、511260 416，`reason=purchase_check_failed` —— 官方话术是「暂时无法确认该基金是否可购买，请稍后重试」，**不是** `purchase_unavailable`（后者才是「该基金当前暂不可购买」）；此前「场内 ETF 会被 `purchase_unavailable` 拦下」的推断被实测**证伪**，见 P18。`CLI_STATUS=ok / CLI_EXIT=0 / PROC_RC=0` 却只有 5 只打开，正是 P16 的实证。`run-script` 单次调用、无重试、全程未打印任何凭证或带凭证 URL。
- 下一步：`& py _audit_trade_entry_v1.py`（`AUDIT=PASS`）→ `& py _trade_entry_v1.py`（`CHECK=PASS`）→ `& py _trade_entry_v1.py --open`（逐项看 `ITEM n ... opened=`，收尾 `OPENED_VERIFIED`）。**换口径 / 换标的 / 改金额须重新授权**，因为 `PLAN` 是审计锁定的常量。
- 别碰：`AGENTS.md` L10 原红线原句（护栏锚点，只能追加例外不能删）；`ttskill` 任何凭证字段与带凭证 H5 URL；`_trade_input_v1.json` 的 `env` 固定 prod、禁改 test；`refresh_all.py` 组顺序；14 只缺口代码在 P1-2 补齐前不要改 `holdings-data.json` 份额。
- **实证契约（2026-11-10）**：`open_h5.mjs` L620–624 批量返回 `{status:"batch", outcome, opened_count, total, needs_login, results:[{index,opened,reason}], message}`；L634 批量时 `exitCode` 不因零打开置 1 → **退出码 0 ≠ 成功**；`run-script` CLI 把该 JSON 包在顶层 `stdout` 字段（外层 `status/exit_code/stderr`），已用 `items:[]` 空数组安全探测证实（不打开页面、不读凭证）；L540–541 URL hash 含 `access_token/session_id/device_private_key_pem` 的 base64url envelope（60 s 过期），L454–461 用 `Start-Process -FilePath $env:TTSKILL_H5_OPEN_URL` 打开。

## 已交接（近 7 天）

### 2026-11-10 · v881b fund_monthly 发布文件滞后 · 已完成并发布
- 改了什么：`refresh_all.py` 加 mtime 复算（`fw2_v881b_monthly_cache_race`）；`gate.py` 加 900s 预算（`fw2_v881b_gate_timeout`）；重算 `data/fund-monthly.json`（1,330,695 B）。
- 新增资产：无（修的是既有链路）。
- 未验证的假设：无。
- 下一步：已发布 head `583a76c925ab`，仅待用户强刷验收。
- 别碰：`data/_hist_cache` 里 001194/004788 的末点（11-09）。


### 2026-11-13 · v924 自选组合回测（下拉挑基 + 逐只参数 + 逐只权重）

- **改了什么**：`edit_work/index.html` 升 v924（tag `fw2_v924_bt_custom_per_fund`）。自选组合面板从「66 项平铺复选框」改成「输代码/名称 + datalist → 加一只」+ 逐只参数行（权重% / 止盈带宽% / 止损% / 网格步长% / 规则启用 / 移除），合计实时算；新增 `cfg.pf` 落 localStorage，`btTargets` 加 `customWMode='manual'`，`btPF` 只对 `pool='custom'` 读 `cfg.pf`；抽屉新增「自选权重」三选一；顺带修杠铃 11 只并入可选池、`btTypePile` 先认杠铃档位、`BT_CACHE` 未加载不误标「无日频」。
- **未验证的假设**：①「每只一行」的布局在更窄的移动端视口（<420px）下 4 个输入框会换行，未做真机验证；②`000912` 这类货币基金在自选组合里默认 `on=false`（内置预设 sl=0），若用户勾上「规则」并填了止损，会按用户值执行——未逐一跑过全组合。
- **下一步 + 别碰**：接手先跑 `edit_work/check_js.py` + `check_html_comments.py`，再本地 8791 真渲染：策略执行 → 组合回测 → 自选组合回测，加 5 只核对逐只默认值/合计/阈值表。**别碰**：`BT_PF_CONST`（杠铃内置预设，改了会让持仓组合回测偏离 5.08% 基准）；`btPF` 里的 `cfg2.pool === 'custom'` 判断（去掉会让两模式串味）。


### 2026-11-13 · v925 自选组合逐只参数改表格 + 网格金额逐只化

- **改了什么**：`edit_work/index.html` 升 v925（tag `fw2_v925_bt_pf_table`）。逐只参数改 12 列宽表（名称/权重/止盈带宽/止损/网格步长/**网格金额¥/档**/投入/档位/来源/实测波动·回撤/规则/操作）；新增 `cfg.pf[code].ga` 并让 `btPF` 返回 `ga`、网格买入改用 `pfg.ga`（未填回落抽屉 gridAmt）；新增 `btCuRef()` 参考列；`syncDerived()` 就地刷新派生列与合计；阈值表加「网格金额/档」。
- **未验证的假设**：①表格 12 列在 <420px 移动视口只能横向滑动（未做真机验证，也没有 sticky 首列）；②`ga` 只影响网格买入金额，备用金上限 `gridFund` 仍是组合级、未逐只化；③货基 `gs=0` 时网格金额输入框仍可填（只是提示「不触发」），是否要禁用未问用户。
- **下一步 + 别碰**：接手跑 `check_js.py` + `check_html_comments.py`，本地 8791 进「策略执行 → 组合回测 → 自选组合回测」核对表格 12 列与「网格金额」；再用 `001015 ga=1500` 跑一次，流水网格应逐笔 ¥1,500。**别碰**：`btPF` 里 `cfg2.pool === 'custom'` 前置（去掉会让杠铃被自选值污染，基准 5.08%/41 笔会漂）；`syncDerived` 不得改成重渲染面板（会把输入焦点打掉）。


### 2026-11-13 · v926 自选组合参数合并成一张表

- **改了什么**：`edit_work/index.html` 升 v926（tag `fw2_v926_bt_one_table`）。①表格上方新增灰底「组合级参数」横条 7 项（备用金模式/上限、目标年化、回撤预算、无风险利率、季度再平衡、按标的分设阈值），id 沿用 `btIn_xxx` 故无需改绑定；②抽屉在 `pool=custom` 下条件渲染，只剩建仓口径 + 标的池切换 + 一句提示，被移走的 5 个全局值改隐藏域；③按钮文案 custom 下「模式与说明 ⚙」；④`customWMode` 在 custom 下恒 `manual`；⑤撤掉 `gridFund===10000→0`、`ddBudget===35→20` 两条每次读取都重跑的静默迁移。
- **未验证的假设**：①<420px 移动视口未验（表格 min-width 940 + 参数条 flex 折行，预计能折但未实测）；②名称列 sticky 仍未做（用户提过未表态）；③localStorage 里 `customWMode` 的旧值 `eq`/`fixed` 仍残留，`go()` 已强制 manual 故不生效，是否清理未定；④货基 `gs=0` 时网格金额框仍可编（只提示「网格步长 0 · 不触发」），是否禁用未问用户。
- **下一步 + 别碰**：接手跑 `check_js.py` + `check_html_comments.py`，本地 8791 进「策略执行 → 组合回测 → 自选组合回测」核参数条 7 项与抽屉瘦身；再切「持仓组合回测」核 5.09%/41 笔。**别碰**：①不要再给 `gridFund`/`ddBudget` 加自动迁移（P53）；②组合级参数条不要塞回表格 `tbody`（横滚会切碎，v926 第一版已踩）；③`btPF` 里 `cfg2.pool === 'custom'` 前置（去掉杠铃会被自选值污染）。


### 2026-11-13 · v927 参数表列序重排

- **改了什么**：`edit_work/index.html` 升 v927（tag `fw2_v927_bt_col_order`）。自选组合参数表 12→13 列：基金名称 / 基金代码（新列）/ 档位 / 来源 / 权重 / 止盈带宽 / 止损 / 网格步长 / 网格金额 / 投入 / 实测波动·回撤 / 规则 / 操作；名称列只放基金名、代码独立成列；thead/tfoot colspan/min-width 同步（940→1010、12→13）。
- **未验证的假设**：①13 列在 <420px 移动视口仍靠横滑（未真机验）；②名称列仍无 sticky（用户提过未表态）；③`sub` 里的「· 无日频」现在跟着代码列显示，若某只名称超长会挤压代码列（未测极端长名）。
- **下一步 + 别碰**：接手跑两个 checker，本地 8791 进「策略执行 → 组合回测 → 自选组合回测」读 `#btCuTbl` 的 thead 应有 13 项、`tfoot td.colSpan===13`。**别碰**：改列数时 thead、行内 td、tfoot colspan 三处必须同步（漏一处表头/合计就错位）。


### 2026-11-13 · v927 发布闭环（数据侧 P34 处置）

- **改了什么**：只有数据，前端零改动。首跑发布被闸门拦下（`fund_monthly FAIL verify_dual_source:F verify_acc_nav:F`），唯一不一致＝`017436` 的 2026-11 累计净值（文件 2.1215 vs 源A 重建 2.0703，QDII 净值晚到，P34 型）。按 P34 处置链：`gen_fund_monthly.py`（81 只 / 7,382 行，1,330,839 B）→ `gen_fund_daily.py`（182,009 行，9,123,740 B，月末对拍通过）→ `gate.py --datasets fund_monthly --check` = `GATE=PASS`（三项全 P）→ `push_gh_v39.py` 发出 `[200] caifu/index.html (4496286)` + `[200] data/fund-monthly.json (1330839)` + `[200] data/fund-daily.json (9123740)`，`master head sha = e4921b428b67`。
- **未验证的假设**：①`gen_fund_monthly.py` 日志里 720001 显示「3620 条净值, 181 页」说明该只走了全量重抓（缓存命中逻辑对这只未生效），未深究是否只有它；②本次只复检 `fund_monthly` 数据集，其它数据集（现价/宏观）本轮未重跑闸门，沿用上次 PASS。
- **下一步 + 别碰**：`_verify_online_v927.py` 已 ALL PASS（BYTE_MATCH True / 9 锚点 / 旧标题×0 / 017436 本地线上均 2.0703 / Pages v927），接手只需等用户页面强刷验收。**别碰**：①不要手改 `fund-monthly.json` / `fund-daily.json` 的 nav/acc 去凑闸门（P34 明令禁止）；②不要给 `verify_acc_nav` 加 QDII 白名单（会把「晚到」和「真错」一起放过）；③再次遇到 `GATE=FAIL` 先读「发布文件不一致=N」逐只明细，判晚到还是真错，再决定刷数据而不是绕闸门。

### 2026-11-15 · v936 单只刹车卡（策略 v2.0 的 A 段）

- **改了什么**：`edit_work/index.html` 升 v936（tag `fw2_v936_brake`）。策略执行「资产配置」tab 顶部新增「单只刹车 · 10 年峰值回撤」卡：`BRAKE_T`（11 只阈值，停加＝10 年 mdd×0.3、减半＝×0.6，国债豁免/活期宝不设）＋ `brakePeakDD()`（10 年窗口用字符串切年份避开 Date 时区偏移）＋ `brakeCardHtml()`（6 列，峰值日作回撤副行，全表 `white-space:nowrap`）；挂载点 `var html = renderStratTodo() + brakeCardHtml();`。**同时修掉分红假回撤**：`__NAV_SERIES__` 建序列只 push `row.nav`，而 `funds[].retBasis='acc'`（实测 012761 红利）应按累计净值算——新增独立 `window.__NAV_ACC__`（只收 acc 系列），`brakePeakDD` 优先读它；**不动 `__NAV_SERIES__`**（那是持仓「买入峰值/最大回撤」的既有口径，v883 已验）。
- **未验证的假设**：①`__NAV_ACC__` 只供刹车卡，其它用 `__NAV_SERIES__` 的模块（持仓峰值/最大回撤、净值曲线）仍是单位净值口径——红利类持仓的「买入后最大回撤」仍含分红干扰，本轮未改也未告知用户；②012920 / 016452 最后一根净值是 2026-11-12（asOf 11-13），比别的标的晚一天，卡上未标注；③2026-06-22 是 6 只标的的共同峰值日，只做了数据核对、未做行情归因（不回测也不臆断原因）。
- **下一步 + 别碰**：接手先跑 `check_js.py`（期望 20 块 `ALL OK`）与 `check_html_comments.py`（期望 211 处 0 隐患），再跑 `_verify_brake_card.py`（期望 11 行与卡面一致、误差 <0.05 点）；本地 8791 进「策略执行 → 资产配置」读 `tbody tr` 应 11 行、状态四档齐全。**别碰**：①不要为了"统一"把 `__NAV_SERIES__` 改成 acc 口径（会动 v883 验过的历史回撤数字）；②`BRAKE_T` 的数不要按 `calc_brake_table.py` 里旧常量 `CAP_STOP=20 / CAP_HALF=40` 重算（那是上一版口径，终版是 0.3 / 0.6）；③卡片 10 年窗口不要改成按行数取（序列起点前段缺失会让窗口漂移）。
### 2026-11-18 · v972（V11 池 5% + 区间提示）
- **改了什么**：`edit_work/index.html` v972（`btCfg` 默认 `v11Pct:5`、迁移 `fw2_v972_v11_p5`、注册表/抽屉/规则卡文案、四处兜底、徽标、`fw2_v972_regime_note`）；`docs/SIGNAL_INVENTORY.md` 新增 14.5；README 三节 + `ver: v972`。
- **未验证的假设**：规则卡「6 个三年滚动窗口 Calmar 胜 5/6」里的窗口全部为 20bps、杠铃 11 只、一次性建仓；定投/底仓口径下的池比例优劣未测。
- **下一步 + 别碰**：强刷 `?t=v972live` 按 README「下一步」五条核；别碰 `btRun` 引擎主体与 `_navToday()`；回退用 `localStorage.removeItem('fw2_v972_v11_p5')` 后手动把 `v11Pct` 改回 10。
### 2026-11-18 · v973（默认 3 年区间换窗 + 分段口径三数）
- **改了什么**：`edit_work/index.html` v973（`btCfg` 默认起止 `2023-07-03/2026-07-03`、迁移 `fw2_v973_start3y`（只换旧默认对）、注册表 V11 加 `seg`、规则卡渲染「分段口径」行 + 页脚补法说明、`fw2_v972_regime_note` 新增 2023 起点分支、徽标 v973、抽屉/规则卡数字换成新窗）；`docs/SIGNAL_INVENTORY.md` 新增 14.6；README 三节 + `ver: v973`。
- **未验证的假设**：①新默认窗的「典型 3 年」定位是口径判断，不是统计结论——它仍只有一个起始点；②分段口径只有 V11 有实测，其余信号（T2/T7/T16/T9/T10/W3/S4/S-TREND/V1）未按段单独跑，规则卡上不显示数字。
- **下一步 + 别碰**：强刷 `?t=v973live` 按 README 六条核；补单信号分段口径需逐信号 12 次回测（约 8–10 分钟/个）；别碰 `btRun` 引擎主体与 `_navToday()`。
### 2026-11-18 · v974（T7/T16 六段分段口径）
- **改了什么**：`edit_work/index.html` v974（注册表 T7/T16/V11 加 `seg`，口径改为「边际」；页脚改写；徽标 v974）；`docs/SIGNAL_INVENTORY.md` 新增 14.7；README 三节 + `ver: v974`。
- **未验证的假设**：①未触发段的「±0.00」等于该开关在该段没有成交样本，不代表「开了也没用」——是条件没满足；②每段只跑一次，未做重复校验；③边际只在池5 默认口径下成立，池10/池0 下未复测。
- **下一步 + 别碰**：T2/T9/T10/W3-S4/S-TREND/V1 尚未补分段口径；T16 在牛A −1.45pct，是否改默认为关需用户拍板（改默认会影响全部历史数字口径）。别碰 `btRun` 引擎主体与 `_navToday()`。
### 2026-11-18 · v975 + v976（T16 改默认关 · 五个信号补分段口径）
- **改了什么**：v975 把 **T16 卖出后破位减半** 默认改关（`postSellHalf: false` + 反迁移 `fw2_v975_t16_off` + 四处文案）；v976 给 **T2 峰值回撤止盈 / T10 杠铃失衡 / W3-S4 趋势确认 / S-TREND 破位拦截 / V1 波动赶底过滤** 填 `seg`（六段边际），并按新基线重测 T7 / V11；徽标 v976（`281198be`）；`docs/SIGNAL_INVENTORY.md` 新增 14.8；README `ver: v976`。
- **未验证的假设**：①每段每个开关只跑一次，未做重复抽样（T10 牛A 与 T2 牛A 曾复跑一次结果一致）；②W3/S4「熊市保险」的因果只核到「累计买入 ¥59,181→¥21,806、笔数 42→18」这一层，未逐笔核对被拦的是哪些买入日；③边际只在池5 基线成立，池10/池0 未复测；④T10 的 +21.79pct 依赖内部回收资金反复再平衡，未核其是否受「备用金/网格」口径影响。
- **下一步 + 别碰**：要不要把 W3/S4 做成「条件化启用（仅熊市/年线之下）」需用户拍板；5/10 年窗口与层3 纪律全关组仍缺。**别碰** `btRun` 引擎主体与 `_navToday()`；跑分段务必显式写全 8 个开关——开关状态会跨运行残留，本轮因此先得到一组假的「池0=池5」。
### 2026-11-19 · v994（观察窗可切换 · 纳入清单可勾选 · 筛选池全量扩样本）
- **改了什么**：`edit_work/index.html` → v994（4,842,542 B，commit `bf8d767b`，blob `837e1653`，已发布）。①观察窗：`ENT_WIN_KEY='fw2_bt_entwin'`／`ENT_WIN_ALLOW=[60,120,250]`／`btEntWin()`（默认 120）／`btFacWin(w)`；`btRun` 改传 `btEntryWin`，卡头 chips（当前项深底白字），证据记录加 `ewin`——**观察窗故意不进 cfg**（它只改统计口径不改成交，进 cfg 会让 `btParamHash` 指纹随非策略参数变，历史证据就没法按指纹对照）。②纳入清单：`LOGIC_GATE_KEY='fw2_bt_gate_ids'`／`LOGIC_GATE_CAND=['T7','T8','T13','T15','R3','V11']`／`logicGateIds()`（过滤到候选池、默认回落 T8/T15）／`logicGateToggle(id)`；硬闸判断改 `logicGateIds().indexOf(id)>=0`；⑧ 层 BT4 出 6 个可勾选 chip（T7 回撤补仓 / T8 估值加仓 / T13 网格跟踪 / T15 跟踪指数 PE 分位 / R3 网格 / V11 狙击），名字取 `SIGNAL_REGISTRY[id].name` 不手写。③扩样本：`POOL_CODES`／`btPoolLoad()`（fetch `./screen-pool.json`，**线上正确路径 `caifu/screen-pool.json`，`caifu/data/…` 是 404**）／`btPoolSamples()`（每只区间内每月首个交易日当假买点，跳过 <200 行标的）／`btPoolCardHtml()`（假 trades 交给**同一个** `btEntryStats` 复用分档/交叉/基准），并跑 `btEntrySig(E,2000)` 走 `btSigCardHtml({sig:SG},cfg,{noPersist:true,pool:true})`——**不写 `fw2_bt_sig_latest`**（那是买点闸判据）。门禁 `check_js` ALL OK、`check_html_comments` 237 处 0 隐患。
- **实测（3 年窗 2023-07-03→2026-07-03、观察窗 120 日）**：主结果仍 13.67/−5.91/2.04/103 笔、指纹 `deef15c1` 不变；池样本 **1,455**（40 只×36 月，279 笔按区间末截断）、基准 63,696 个（68.54%/+13.27%）、抽样平均 **+24.00%**（超额 +10.73 pct）；池 15 档 p＝`0.02|0.54|0.14|0.68|0.91|0.62|0.19|0.06|0.05|0.07|0.28|0.51|0.41|0.72|0.49`，最小 0.02 仍 > α=0.0033 → **扩样本救不回显著性，问题在因子本身**；唯一接近档「自身净值分位·低位」Δ −11.73 pp（区间 −21.09~−2.04）＝池里低位买入反而更差。观察窗切 60 日后主卡最小 p 从 0.182 降到 **0.072**（表头与池卡同步变「60 日」）。
- **未验证的假设**：①池卡基准口径与主卡不同（池＝40 只全交易日 63,696 个；主卡＝交易涉及标的），两者不可横比（卡内已写明）；②池 40 只是 2026-11 筛选结果，回溯天生带选择偏差（卡内已写明）；③块重抽只按「买入月份」分块，同月跨标的样本仍共享行情，未按标的二次聚类；④线上首次进入若初始化被网络抖动打断，⑧ 层可能 blank（本轮遇到一次，注入 `renderLogicView()` 立即恢复，43,947 字符），属既有初始化时序问题、非 v994 引入。
- **下一步 + 别碰**：下一步（需用户拍板）⑴拦截判据从 Bonferroni 换 BH-FDR，看 0.02 那档是否进「边缘显著」——放宽后误纳风险上升，必须与拦截逻辑一起改；⑵池卡接进 ⑧ 层准入视图（现在只在持仓回测页出）；⑶PE 历史轨（需先建指数 PE 日序列）。**别碰** `btRun` 引擎主体与 `btParamHash`；改 chips 候选池要同步 `LOGIC_GATE_CAND` 与 `logicGateIds` 的默认回落，否则旧存储值会被静默丢弃。

### 2026-11-19 · v995（池卡接 ⑧ 层 · PE 历史轨接入分档 · 修 4 笔档假显著）
- **改了什么**：`edit_work/index.html` → v995（4,851,942 B，commit `04397b80`，blob `80d37919`，已发布）；`edit_work/data/pe-hist.json` 重生成（634,166 B，commit `939fba06`，blob `39232a66`）；`edit_work/gen_pe_hist.py`（LG 3→8、ASOF 改 today）；`docs/data-ledger.json`（`pe_hist` note 改 10 指数口径）。
  ①**池卡进 ⑧ 层**（tag `fw2_v995_pool_in_gate` / `fw2_v995_pool_cache`）：`btPoolCardHtml` → `btPoolCardHtmlRaw` + 外层缓存（key＝区间+观察窗+池清单；只缓存 length>200 的正常结果）；`btPoolLoad` 回调双写 `#btPoolWrap` 与 `#btPoolWrapLogic`；`btFacWin` 同步两处；新增 `logicPoolHostHtml()`，在 `L.k==='trace' && !_btCfgMode` 时插进 `renderLogicView` 组装链；无 `window.__btLast` 出提示「去持仓回测跑一次（只读，不重跑，不写证据台账）」。
  ②**PE 历史轨**（tag `fw2_v995_pe_hist`）：`BT_PE_MAP` 4 只（001015→000300 / 012761→000015 / 160422→399673 / 017644→000852）、`btPePctAt()` 二分取「≤买入日最后一个点」且只认 `basis==='pe_ttm'`；`dims` 第 5 维「跟踪指数 PE 分位」；返回 `peCov{mapped,covered,total,codes}`；`btEntCardHtml` 加 `peNote` + 缺口段改写（旧文案「指数 PE 分位不参与…等台账补上」已删）。
  ③**显著性门槛 4 → 8**（`btEntrySig` 的 dims 与 cross 两处），卡面写明「进入判定的每档需 ≥8 笔」；单标的维度（覆盖标的 <2 只）跳过判定并在卡面标「已跳过」。
- **实测（本地 `:8765`，3 年窗 2023-07-03→2026-07-03、观察窗 120 日）**：主结果 13.67/−5.91/2.04/103 笔、指纹 `deef15c1` 不变；PE 维覆盖 **9/54 笔**（三档 4/2/3 笔，全标「样本少」）；主口径 sig 修后回到 **15 档、α=0.0033、「没有一档能和其余档区分开」**；池卡 1,455 抽样、PE 覆盖 **31**（只来自 017644 中证1000 一只）、单标的 → 显示「已跳过：跟踪指数 PE 分位（样本只来自 1 只标的）」；⑧ 层 `#btPoolWrapLogic` 27,028 字符、`renderLogicView()` 连调 13ms/9ms（缓存命中，非 5 秒重算）。门禁 `check_js` ALL OK、`check_html_comments` 237 处 0 隐患、`verify_manifest` PASS。
- **未验证的假设**：①PE 分位沿用 pe-hist 生成时的「向前 10 年窗」口径，与页面「分位·10 年」卡一致，但**月频**取点会放大买入日与估值日最多一个月错位；②`017644` 的中证1000 映射来自 `screen-pool.json` 的 `benchName`，未逐份招募说明书复核；③池卡 PE 三档（11/10/10 笔，胜率 72.73%/100%/90%）是同标的连续月份，**不可当横截面结论**（卡面已写明）；④上证50/上证180 因乐咕 429 未落，扩 PE 覆盖只完成 5/8。
- **下一步 + 别碰**：下一步 ⑴等限流解除重跑 `gen_pe_hist.py` 补上证50/上证180；⑵筛选池补 `benchName`（40 只仅 1 只有）才能让池侧 PE 维有横截面意义；⑶买点闸 Bonferroni → BH-FDR 仍待用户拍板。**别碰** `btRun` 引擎主体与 `btParamHash`；改 `btEntrySig` 门槛时务必同步 dims 与 cross 两处，否则交叉表会残留 <8 笔档（本轮 4 笔档假显著就是这么冒出来的）；`pe-hist.json` 发布路径固定 `caifu/data/pe-hist.json`（`caifu/pe-hist.json` 是 404）。

### 2026-11-19 · v996（策略执行 tab 切换卡顿修复 · index 4,856,184 B `c403770`/`e568dad`）
- **改了什么**：`edit_work/index.html`（tag `fw2_v996_tab_fast`）——①新增 `btOutKey(cfg,data)`＝参数指纹|池|数据日|观察窗；②`go(force)` 命中 `window.__btCache` 只重建视图、不命中且已有旧结果且非手点 → 只出黄框提示并 return；③`runBtn` 改 `go(true)`；④`switchStratTab` 视觉先行（curPool → `.st-tab` active → `.st-pane` display → `btSave`），删 `pane0.textContent=''`，`if(pool)` 自动跑改 rAF 内 `__btGo()`；⑤`btLoad().then(...)` 包进 `_kick` + rAF，提示先绘制；⑥复用路径不重复 `btEvidenceWrite`。
- **未验证的假设**：①后台标签 rAF 1,935–2,004ms 判为**后台节流**而非真机卡顿，依据是同步耗时 0ms / renderStrategyView 39ms；未在用户前台真机复测切换耗时；②`__btCache` 存的是 `btRun` 返回的 `res` 对象引用，重渲染是否对其产生可变副作用（如补字段）未逐字段核对，仅实测两次往返结果字符数一致（22,046）；③「首次进入自动跑一次」沿用旧行为，未确认用户是否更希望手动触发。
- **下一步 + 别碰**：下一步 ⑴线上强刷 `?t=v996live` 验收六条（见 README「下一步」首条）；⑵买点闸 BH-FDR 仍待拍板；⑶PE 扩上证50/上证180。**别碰** `btRun` 引擎主体、`btParamHash`（缓存 key 依赖它，改了会让所有旧缓存失配——这是预期行为，但别在没核对 key 拼接的情况下动它）；`btEntWin()` 故意没进 `btParamHash`，若有人把它塞进 cfg 会让 key 少一维、观察窗切换误判复用。

### 2026-11-19 · v997–v1000（回测页本地缓存 + 口径差异横幅 + 图表懒挂载 + 结果页快照 + 分池缓存 · index 4,869,492 B `5391f12`/`9456b0d`）
- **改了什么**：`edit_work/index.html`（tag `fw2_v997_idb_cache`）——①`_idbOpen/_idbGet/_idbPut` + `btLoad()` 重写（`fundDaily` 13MB 走 IndexedDB、6 小时内直读，带 `__btLoadP` 去重）；②启动预热 IIFE 把 `lastResult`（约 10MB）读回 `__btCache`；③`go(force)` 的 `_stale` 分支直接复用上次结果并按旧 cfg 渲染；④`out.innerHTML` 前插新旧口径差异横幅 + 重算按钮；⑤`switchStratTab('bt')` 每次 `renderBacktest()` 重建骨架（约 39ms）让口径条跟上当前设置。
- **未验证的假设**：①IndexedDB 写入 13MB / 10MB 的耗时未单独计量（首次 7.1s → 刷新后 3.2s 是端到端结果，未拆分「IDB 读」与「渲染」各占多少）；②`fundDaily` 用 6 小时 TTL 代替「比对 asOf」，若数据日当天更新而用户在 6 小时内刷新，可能看到上一天的数据（页面「数据 asOf」会如实显示，未做强制校验）；③预热固定在 DOMContentLoaded +1.2s，若用户在 1.2s 内就点进回测页会走「无缓存→自动跑」的旧路径（未复测该竞态）；④`_stale` 时 `cfg` 被换成旧口径，`btSave` 已在之前写过当前口径，二者不会互相覆盖（未二次核对写存储时序）。
- **下一步 + 别碰**：下一步 ⑴**回测引擎分片**（`btRun` 逐日循环 + `btEntrySig` 的 2000 次重抽仍在主线程，点「重算」仍占 10–60 秒）；⑵买点闸 BH-FDR 待拍板；⑶筛选池补 `benchName`。**别碰** `btParamHash`（`btOutKey` 依赖它，改了会让 IDB 里所有旧结果失配）；改 `btEntrySig` 阈值须同步 dims 与 cross 两处；`_FD_TTL` 若要调小，注意 13MB 重下载会退回「每次进去都等网络」。旧版 `btLoad` 以块注释留在文件内，删除前先确认新路径在线上稳定。

**v998 追加（同一轮）**：`mountLazyChart(id, option)`（紧随 `mountChart` 定义，tag `fw2_v998_lazy_chart`），`btPosChart`/`btDDChart`/`btMonChart`/`btAttrChart` 四张非首屏图改用懒挂载（`IntersectionObserver`，`rootMargin:'300px'`；容器已在视口附近则直接画）。实测本地「投资逻辑 → 持仓回测」到结果出现 **2,643ms**（v997 同路径 2,294ms，差异在测量粒度与首帧差异，图表 init 并非主要成本——**结论：2–3 秒的大头是 22k 字符 HTML 的构建/解析/布局，不是图表**）。滚动到「① 分标的持仓市值」后 `btPosChart` 已生成 canvas（截图 `D:\Temp\v998_lazy.png`）。

**v999 追加（同一轮）**：tag `fw2_v999_html_persist`。① 渲染完成后把整页 `out.innerHTML` 存 `window.__btHtml` 并 `_idbPut('lastHtml', …)`；② `renderBacktest()` 占位优先回填该快照；③ `go()` 里「正在复用上次结果…」不再覆盖已有快照（原来会把刚铺好的内容换成一行提示）；④ 启动预热同时 `_idbGet('lastHtml')` 读回。**实测**：同一会话切 tab **17ms**（22,234 字符立即在页上）；刷新后第一次点进 **18ms**（18,850 字符，含旧口径横幅）。图表由随后的 `go()` 补齐（`btChart` canvas 正常生成，截图 `D:\Temp\v999_first.png`）。仍未解决：手点「运行回测 / 用当前口径重算」那一次仍是 10–60 秒主线程同步计算。

**v1000 追加（同一轮）**：tag `fw2_v1000_pool_cache` / `fw2_v1000_custom_pool`。
- **改了什么**：① `window.__btCacheByPool` + `window.__btHtmlByPool`，IDB 键改 `lastResult:<pool>` / `lastHtml:<pool>`（旧单键按 key 里 `指纹|pool|…` 归类迁移）；② `go()` 的命中/复用/写入全部按 `_btPoolKey(c)` 分池，跨池不再互相顶替；③ 未算过的组合（`!_hit && !_stale && !force`）不再 `btRun`，改为「还没算过 + 用当前口径运行回测」按钮——原来这里直接进 60–90 秒主线程阻塞，就是用户说的「点自选回测整页卡死」；④ `btCfg()` 里 `scope==='custom'` 强制 `pool='custom'`（`btSave` 有意跳过 pool，导致切到自选后 `btCfg('custom')` 仍返回母版 `barbell`，标题写「持仓回测」而引擎跑自选池）。
- **未验证的假设**：自选组合为空（`customCodes=[]`）时 `btRun` 仍会出一份「只有备用金」的结果（本地实测 1.27%/Calmar −0.12），未核对该结果对用户是否有意义。
- **下一步 + 别碰**：手点「运行回测 / 用当前口径重算」仍是 10–60 秒同步计算，待做分片或 Worker；`btSave` 跳过 `pool` 是 v988j 有意为之（⑧-B/⑧-C 池固定），不要改成写 diff。

**v1001 追加（接 v1000 之后，同一轮）**：tag `fw2_v1001_empty_state`，commit `548bab7` / blob `da6cfc0` / 4,870,874 B。
- **改了什么**：空态文案重写——①标题「这个口径还没有算过——不是数据丢了」；②列出当前口径（组合/标的数/区间/本金）；③说明「以前这个位置显示的是另一个组合的结果（共用一份缓存、互相顶替）」；④按钮「运行回测（约 20–90 秒）」，点击即置灰并改「正在算…」；⑤说明跑完存本机、以后切回来秒开。
- **未验证的假设**：用户 5 只标的口径（160422/096001/539001/012761/001015 各 20%、¥100,000、2021-07-05→2026-07-03、指纹 `7119fcf2`）真实耗时「20–90 秒」是估计，未实测（线上空组合实测 3.1 秒）。
- **下一步 + 别碰**：btRun 仍是同步大函数（逐日模拟 + 2,000 次块重抽），要分片/Worker 才能让「运行回测」不阻塞 UI；不要在空态里加「自动跑」——用户口径明确是「需要测算我自己会重新选择并测算」。

### 2026-11-19 · v1002（回测参数归位到 ⑧ 层 · index 4,872,699 B `dedb138`/`d6be06a`）
- **改了什么**：`edit_work/index.html`（tag `fw2_v1002_param_move`）——①`renderBacktest()` 删掉 `btCuPanelHtml(cfg)`，两个回测 tab 不再出「自选组合·基金与逐只参数」宽表与「组合级参数」条；②`renderBtCfgHost()` 在 `sc==='custom'` 时挂整块 `btCuPanelHtml(btCfg('custom'))`（⑧-C 自选回测）；③⑧-B 不再额外加组合级参数条（`btParamsHtml` 非 custom 分支本就渲染 `gridExt/gridFund/tgtAnn/ddBudget/rf/rebal/perFund`，再叠一份会出现同屏两份同 id）；④`btCuPanel` 交互绑定从 `renderBacktest` 的 IIFE 提成模块级 `btCuBindPanel(panel)`，⑧ 层渲染后调用；⑤`rerun(true)` 补 `renderBtCfgHost()`，加/删标的即时重绘 ⑧ 层。徽标 v1002。
- **未验证的假设**：①第 1 次在 ⑧-C 加标的后 `fw2_bt_custom` 读到 `{}`（第二次复测正常写入 `customCodes`+`pf`），未彻查是否点击链时机导致 `__btCfgScope` 未就绪；②`btCuBindPanel` 搬到模块级后，仅实测「添加一只 → 表出现 1 行」，未逐项点击删除/等权重排/预置杠铃/legacy 切换；③⑧-A 母版页未回归（未测 plan scope 是否有布局位移）。
- **下一步 + 别碰**：下一步 ⑴线上强刷 `?t=v1002live` 按 README「下一步」首条验收五条；⑵`btRun` 同步阻塞仍是最大遗留；⑶买点闸 BH-FDR 待拍板。**别碰** `btSave` 里 `pool`/`mode` 的跳过逻辑（v988j 有意：⑧-B/⑧-C 池固定，不写 diff）；也别把 `btParamsHtml` 的 custom 分支隐藏域改回可见——那会让 ⑧-C 出现两套逐只/组合级控件。

### 2026-11-19 · v1003（⑧ 回测验证拆四页 · index 4,875,599 B `e5d31ba`/`4a03c46`）

- **改了什么**：`edit_work/index.html` tag `fw2_v1003_bt8_split` —— ⑧ 层二级页签由两页（准入规则 / 回测口径）拆为四页：⑧-A 流程参数 / ⑧-B 持仓回测参数 / ⑧-C 自选回测参数 / 准入规则与证据；参数页只放参数，删掉与之 id 重名的「运行回测」（`btRunBtn` / `btRunSum` 各只剩回测页 1 处）；准入页闸门横幅补「T8 估值加仓」中文名；并把回测页「运行回测 / 全部参数⚙ / 重置为标准口径」改内联 onclick（v999 快照回填会让 JS 绑定失效，实测点击无反应）。README frontmatter 与三节已同步。
- **未验证的假设**：① 窄屏（467px）「可投资金(¥)」行尾被截断，推断宽屏正常，未在 1920 实测；② `btScopePanelHtml()` 已无调用点，推断为死代码，未删；③ ⑧-B / ⑧-C 改参数能正确落到各自 scope，本轮只读状态条「覆盖 N 项」，未做写盘→回读的端到端。
- **下一步 + 别碰**：跑 `python edit_work/verify_manifest.py`（应 PASS）；线上强刷 `?t=v1003live`，验四个页签与回测页「运行回测」可用。别碰：`btRun` 同步执行（10–60 秒阻塞，待分片 / Worker）；买点闸 Bonferroni → BH-FDR 仍待用户拍板。

### 2026-11-19 · v1004（投资逻辑默认落 ① 选品 · index 4,877,648 B `712905d`/`de7e175`）

- **改了什么**：`edit_work/index.html` tag `fw2_v1004_logic_default` —— `logicCur()` 首次渲染强制 `fw2_logic_view='sel'`；`switchStratTab('logic')` 从别的模块进入时重置为 `sel` 并重绘。README frontmatter 与三节已同步。
- **未验证的假设**：无（两场景已在本地 :8765 实测：刷新、切走再切回都落 ①）。
- **下一步 + 别碰**：线上强刷 `?t=v1004live` 复验 ①②③。别碰：`btRun` 同步执行（10–60 秒阻塞）；买点闸 Bonferroni → BH-FDR 待拍板。

### 2026-11-19 · v1005（投资逻辑规则表改八列 · index 4,878,222 B `0291e4c`/`a7b0a1b`）

- **改了什么**：`edit_work/index.html` tag `fw2_v1005_logic_cols` —— `logicRowHtml` 由「5 列主行 + 下一行灰字备注」改为单行 8 列（代码/中文名 · 作用·方向 · 三态 · 引擎 · 实测 · 口径 · 动作 · 备注），①–⑧ 八层共用；表格外包 `overflow-x:auto` + `min-width:1300px`，colgroup 定宽，最后一列给足 240px。README frontmatter 与三节已同步。
- **未验证的假设**：1920 实屏未直接截图（用 `wrap.style.width='1700px'` 模拟量得 ⑤ 最长行 153px、⑧ BT4 159px），真实宽屏观感待用户确认；④ / ⑤ / ⑧ 的长行（206 / 224 / 212px）是长文本折行所致，未做截断或折叠。
- **下一步 + 别碰**：线上强刷 `?t=v1005live` 复验八列与不存在备注行。别碰：`btRun` 同步执行；`logicRowHtml` 的 `table-layout:fixed` 列宽若再调，必须同时校验最后一列不为 0（否则文字逐字竖排）。

### 2026-11-19 · v1006（⑧ 准入页 A+B+C 优化 · index 4,886,491 B `bdcf0dd`/`e674daf`）

- **改了什么**：`edit_work/index.html` tag `fw2_v1006_bt_table`（A：BT 表四列 + 层卡/页顶统计剔除元规则；B：chips 移出表格到 `<details>`）+ `fw2_v1006_bt_evidence`（C：证据台账补 nFund/Calmar/当前口径标记）+ D（版本与证据字段化）。README frontmatter 与三节已同步。
- **未验证的假设**：① `nFund` 只对 `pool==='custom'` 计算（`customCodes` 长度或 `pf` 键数），杠铃池显示 `—`（未去核杠铃实际只数，避免猜）；② 宽屏 1700 为 CSS 模拟量测，未在 1920 实屏截图；③ 证据台账「当前口径」比对用的是 `btCfg('hold')` / `btCfg('custom')` 现算 hash，若用户在 ⑧-A 母版改过参数，⑧-B 记录会被判「旧口径」——这是有意的（母版改动确实改变了继承口径）。
- **下一步 + 别碰**：线上强刷 `?t=v1006live` 复验四列与折叠块。别碰：`btRun` 同步执行；`logicSet` 仍是 BT 状态写入通道（现无入口可点，但 localStorage 里存量 BT 三态未清，页面已不再显示）。

### 2026-11-19 · v1007（数据管理模块对齐最新结构 + 41 数据集全量刷新 · index 4,888,663 B master `46d9d0f46b97`）

- **改了什么**：`edit_work/index.html` tag `fw2_v1007_dm_sync`（导航副标题去「39 数据集」硬编码、ops 文案按 `rows.length` 动态、hero 补「实时抓取 1」chip、自动化三处改「未核验·请到自动化面板确认」）+ `fw2_v1007_dm_local`（新增第五张卡「本机前端状态」，localStorage 三份 + IndexedDB 缓存四行）；`edit_work/data/data-mgmt.json` 重生成（41 项 · 2026-11-19 19:58:10 · refreshFailed=[]）；`gen_kr_export.py`（YoY 阈值 -70~150，`ushf.krExport` 首次落数）；`refresh_holdings_ttskill.py` + `_audit_holdings_linkage.py` + `_audit_capbal_kpi.py`（新标的在途机制 `fw2_v1007_onway`）；8 个审计脚本过期断言修正（pe_chain / chart_const / chart_tokens / sig_type / capbal K08 / alloc_color A19 / lag_color B25 / firstload F01 / var_paren E5 / nav_freshness D02 / plan_merge A01）+ `handoff_check.py` 版本正则；26 处 CSS 兜底对齐（漂移 347→311，两版基线均下调）。README frontmatter 与「当前进度 / 下一步」已同步。
- **未验证的假设**：① 日频自动化是否仍在调度**未核实**（`list_cron_jobs(enabled=true)` 本机 0 条，WorkBuddy 侧 `b1109994-…` 无法从本机查询），页面已按「待确认」表述，需用户到自动化面板确认；② `023422` 的 firstBuy* 需等 QDII 确认（预计 11-20）才会由刷新脚本自动写入，本轮未手工补、也不允许编造；③ 「本机前端状态」卡的 IndexedDB 行按当前浏览器缓存显示（净值 2026-11-16 103 只），换浏览器会变，非数据滞后。
- **下一步 + 别碰**：线上强刷 `?t=v1007live` 复验 6 chips / 41 行 0 滞后 / 本机卡四行 / 副标题无数字。别碰：`btRun` 同步执行；`_audit_sec_daily_v877.py` 仍未挂 gate（`verify_manifest` 既有 WARN，本轮按「不扩大范围」未处理）；买点闸 Bonferroni → BH-FDR 待拍板。

## 2026-11-19 · v1008

- **改了什么**：`edit_work/index.html`（`fw2_v1008_rule_to_bt8`，徽标 v1008，4,167,795 B）——「本次回测执行的规则」从回测结果区（`renderBacktest`）移除，抽成全局 `btRuleCardHtml(cfg, opts)` 后挂到「投资逻辑 → ⑧ 回测验证 → 准入规则与证据」页；顺带删掉原段尾误拼 `pfHtml` 的死代码（无副作用）。
- **未验证的假设**：⑧ 页不传回测结果时，规则卡的网格步进/止损阈值按 `cfg.gridStep`（默认 3）/ `cfg.sl`（默认 8）降级显示；若你改过 ⑧-A 母版再进 ⑧ 页，数字应随母版变（已实测默认口径为「每跌 −3%」「浮亏 ≥−8%」，非默认值未逐档复测）。
- **下一步 + 别碰**：线上强刷 `?t=v1008live` → 徽标 v1008；持仓回测 / 自选回测结果区不再有规则卡；⑧ 准入页有 20 条（开 9 / 关 11）。别碰：刹车卡与顶部 12 指数条本轮按用户拍板保留；`_audit_sec_daily_v877.py` 仍未挂 gate。

### 2026-11-25 · v1115（深跌买入接入「已终止指数 · 幸存者偏差校正」卡 · 已发布 master `d1e2fb452c13`）

- **改了什么**：`edit_work/index.html` 加 `fw2_v1115_dd_term_card`——`var TERM = window.__DD_TERM`、`termItemHtml` / `termBodyHtml` / `termCardHtml` / `loadTerm`，`shellHtml()` 末尾 `+ termCardHtml()`，`mount()` 里 `loadTerm()`，徽标 v1114→v1115；`edit_work/_globals_baseline.json` 登记 `__DD_TERM`（assign 2 / refs 3）。卡片把 `index-term.json` 3 只（801862 / 399305 / OMXI15_OLD）单列为 3 个纵向样本块，不并入 63 只、不参与全池选池；801862 展示全历史峰值 1,521.13@2000-11-22 → 终止 10.11、−99.34%、`final_100`、`engineStress`（页面 runBT 默认反弹卖出：6 买 / 3 卖 / 3 未平、期末 48,777.14、−51.22%、MDD 58.43%）、`pathStress` −96.03%/−94.46%；399305/OMX 明确标不可回测/不可精确回测。README frontmatter v1115 与「当前进度 / 关键文件 / 下一步」三节已同步；`docs/FRONTEND.md` 已补 §10.14；`data-mgmt.json` 补登 chan-hs300 / index-dd / index-val / index-term 四行（46 行，`_audit_dm_v845` FAIL=False）。已发布：`caifu/index.html` 5,327,663 B / SHA256 `59050bf5...` 与 `caifu/data/index-term.json`（3 只，200）随 master `d1e2fb452c13` 上线。
- **未验证的假设**：①538 视口真渲染 `#ddTermCard` 507/507、3 个样本块无横溢已截图核对；宽屏 1900 未实拍。②卡底「全池 59 只 19 买 / 17 卖 / 88.2% / 174,819.61」是页面当前参数实测 2016+ 口径，不能当 1999 起全历史无偏胜率。③`engineStress` 是单指数 `runBT`，`pathStress` 是持有到终止压力，两者都不是 59 只共享资金池结果。④`final_100` 只是终止前快照，不是 1999-2017 每周完整进出名单；OMX `final_12_of_15` 也不是危机前完整 15 只权重。
- **下一步 + 别碰**：线上 `?t=v1115live` 已验徽标 v1115、深跌买入页 `#ddTermCard` 507/507、3 个样本块顶/底两段真实截图；本地 `check_js` / 注释 332 / globals PASS 278 / manifest PASS 41 / `index_term,manifest` 双 PASS 已过。**全量 gate 例外**：`gate.py --check` 被 fund_monthly 既有的双源/累计净值 FAIL 阻断（78 个发布文件不一致，本轮未改基金数据），发布按 `SKIP_GATE=1` 前端轨；HTML/36 审计全过。下一轮若修 fund_monthly，先跑 `refresh_all.py` 月频组再谈全量 GATE=PASS。别碰：`index-dd.json` 63 只口径；把 3 只并进全池；把 `pathStress` / `engineStress` 当全池结果；把 `final_100` 当完整历史；`loadTerm` 的 cache no-store。**已发布，线上 v1115，勿回退到 v1112。**

### 2026-11-25 · v1116（801862 终止样本接入 2016+ 全池对照 · 已发布 master `25bafab229fc`）

- **改了什么**：`edit_work/data/index-term.json` 新增 `poolStress`（`baseline59` / `withTerm60` / `delta` / `termTrades` / `caveat`）；`edit_work/index.html` 徽标 v1115→v1116，新增 `termPoolHtml()`（tag `fw2_v1116_dd_term_pool`），在 `termBodyHtml()` 的 3 个样本块后加「全池对照 · 801862 按终止日强平」块；`verify_index_term.py` 加 `poolStress` 硬断言。59 只基线 **19 买/17 卖/88.2%/174,819.61** 逐位复现页面；60 只含 801862（2017-01-20 按 10.11 强平）为 **20 买/18 卖/83.3%/169,687.26**，差额 **−5,132.35**（胜率 −4.9pp、MDD +0.82pp），只多一笔 95 档 2016-11-23 13.60→2017-01-20 10.11（−25.66%，58 天），其余 59 只逐笔路径未变。已发布：`caifu/index.html` 5,330,270 B / SHA `DC1519...`、`caifu/data/index-term.json` 线上 compact 215,121 B（与本地 224,906 B 语义一致），master `25bafab229fc`；线上 `?t=v1116live` 徽标 v1116、`#ddTermCard` 507/507、全池对照块顶/底截图核对。
- **未验证的假设**：①801862 在 2016-11-23 已约 −99.08%，这段只覆盖终止前 58 天，60 只对照只证明 2016+ 池的边际影响，不能代表 1999-2016 长期崩塌；②59 只基线逐位复现页面，但 60 只只做了离线同口径复算，未在页面新增 `scope`；③终止日仍按「最后收盘强平」单一口径，未与 successor 拼接/首日补档对照；④宽屏 1900 未实拍。
- **下一步 + 别碰**：①补 399305/OMX 日线；②补 801862 1999-2017 周度完整进出名单；③统一终止日口径；④宽屏 1900 实拍；⑤全量 gate 的 fund_monthly 既有 FAIL 单独修。别碰：`baseline59` 必须保持 174,819.61 / 19/17/88.2；`withTerm60` 必须保持 169,687.26 / 20/18/83.3；`poolStress` 不是页面 `scope`；3 只仍不进 63 只。

### 2026-11-25 · v1114（index-term v2：801862 全历史日线 + 终止前 100 只；OMX 最终 12 只）

- **改了什么**：`edit_work/data/index-term.json` 升到 v2（约 213KB，3 只）：801862 由 1,680 点末端扩到 **Wind 全历史日线 4,130 点**（1999-12-30→2017-01-20；与同花顺 1,680 个重叠点逐日一致，最大差 <0.01），峰值修正为 **1,521.13@2000-11-22**，终止 10.11、−99.34%；成员补成 **2017-01-16 终止前最终 100 只**（`final_100`）；新增 `pathStress`：六档首次触发 70% 2004-12-31 / 75% 2005-03-30 / 80% 2005-07-08 / 85% 2008-08-12 / 90% 2008-10-10 / 95% 2011-12-14，70-90 五档粗算 **−96.03%**、70-95 六档 **−94.46%**；另按页面 `runBT` 默认反弹卖出复算 `engineStress`：**6 买 / 3 卖 / 3 未平，期末 48,777.14，−51.22%，MDD 58.43%**（3 笔 2006-06-07 反弹卖出，85/90/95 三档按终止收盘计价）。OMX 补 **2009-01-02 最终 12 只**（`final_12_of_15`），三大银行单列 `crisisBanks`（合计 73.2%，仅 Kaupthing 37.72% 可核实）。`verify_index_term.py` 同步升硬断言（`INDEXTERM=PASS`）；README frontmatter `v1114` 与三节、`docs/data-ledger.json`、`docs/DATA_LEDGER.md` 已同步。**未改 index.html、未发布、未进 push_gh_v39.py。**
- **未验证的假设**：①`pathStress` 是“每档 2 万、首触买入、终止 10.11 强平、未计费用/分红”的**持有到终止**路径压力，`engineStress` 是按页面 `runBT` 默认反弹卖出的**单指数**复算，两者都**不是 59 只全池共享资金结果**，不能直接替换全池胜率；②801862 的 `final_100` 只是终止前快照，不是 1999-2017 每周完整进出名单；③OMX 的 `final_12_of_15` 是 2009-01-02 最终官方调整后的名单（最多 15 只），不是危机前完整 15 只权重；④399305 仍是 3 个点位 + 22 只跨时点累计名单，未补日线/同日快照；⑤终止日“强平 / 拼接 successor / 首日补档”三种口径仍未统一。
- **下一步 + 别碰**：跑 `python edit_work/verify_index_term.py`、`python edit_work/gate.py --datasets index_term,manifest --check`（均应 PASS）；801862 单指数已按页面 `runBT` 复算（`engineStress`），若要把偏差真正算进全池，仍需把 801862 全历史路径接进 59 只共享资金池逐笔重跑；再补 399305/OMX 日线与统一终止口径。别碰：`index-dd.json` 63 只口径；把 `pathStress` 或 `engineStress` 当全池结果；把 `final_100` 当完整历史；399305 的“非70%”标签；OMX 未核实的点位日期。**当前未发布**，不要写进已发布清单或线上页面。



### 2026-11-25 · v1113（已终止指数 + 历史成分数据集 · index-term v1）

- **改了什么**：新增 `edit_work/data/index-term.json`（schema `index-term-v1`，3 只：801862 申万活跃股指数 / 399305 深市基金指数 / OMXI15_OLD OMX Iceland 15 旧指数）与 `edit_work/verify_index_term.py`（`INDEXTERM=PASS`）；`edit_work/gate.py` 增加 `index_term` 数据集；`docs/data-ledger.json` 增第 41 条（manual、无 producer、未 publish）；`docs/DATA_LEDGER.md` 增手工轨 index-term 节；README frontmatter（ver v1113）与三节同步。**未改 index.html、未发布、未进 push_gh_v39.py。**
- **未验证的假设**：①801862 只有 2010-03-01 起日线，2000-07 高点用月度收盘 1,483.56 补点；1999-2010 无日线，不能复算 2005 首次触 70% 后的完整逐档路径；②801862 的“周换手率前 100、每周轮换”来自公开报道/编制规则，完整 100 只历史名单未拿到，`members` 只有 300226 上海钢联两次进出的样本事件；③399305 的 22 只成分是 2017-07-09 中国基金报/证券时报系报道的跨时点累计名单，不是同日快照；④OMX 只有 5 个关键点位，2009-04 低点 212.05 的日期未核实；⑤终止日强平 / 拼接 successor / 首日补档三种口径尚未统一，当前只记录 801862 的“最后收盘强平”。
- **下一步 + 别碰**：跑 `python edit_work/verify_index_term.py` 与 `python edit_work/gate.py --datasets index_term,manifest --check`（均应 PASS）；若要扩样本，先补 801862 2005-2010 日线与完整 100 只周度成员，再谈无偏胜率。别碰：`index-dd.json` 的 63 只口径；801862 的 `price.d` 首点 20000731（月度高点补点，不是日线连续）；399305 的“非70%”标签；OMX 未核实的点位日期。**当前未发布**，不要把它写进已发布清单或线上页面。

### 2026-11-25 · v1117（深跌买入出厂默认改为 10 万 / 每档 5,000 · 已发布 master `bd9a3f462c37`）

- **改了什么**：`edit_work/index.html` 的 `window.__DD_STATE` 初值 `capital:10000, perBuy:500` → `100000 / 5000`（tag `fw2_v1117_dd_defaults`）；同步 `__ddReset` 复位值、`ruleCardHtml` 的 `|| 5000 / || 100000` 兜底、空态文案「每档 ¥5,000」；徽标 v1116→v1117。`termBodyHtml` 的 59 只全池提醒补「10 万 / 每档 2 万」参数标注，避免被误读成新默认。**零计算改动**：`runBT` / `runPoolBT`、档位/卖出规则、index-dd/index-term 数据与 59/60 只口径未动。README frontmatter 与「当前进度 / 关键文件 / 下一步」、`docs/FRONTEND.md` §10.1 与新增 §10.15 已同步。已发布：`caifu/index.html` 5,330,725 B / SHA256 `EB0200E7...`，master `bd9a3f462c37`；线上 `?t=v1117live` 徽标 v1117。
- **未验证的假设**：①`ST` 只挂 `window`、不写 localStorage，已打开的页面不会自动变，必须刷新/重进；②本地与线上 538 视口已成为 509/509、chips「每档 ¥5,000 / 资金池 ¥100,000」、输入 100000/5000；宽屏 1900 未实拍；③新默认单指数（931775 中证全指房地产，2016-11-23→2026-11-24）跑出 3 买 / 2 卖 / 在仓 1、期末 100,961.25、+0.96%、MDD −3.01%，这只是该指数口径，不是默认 10 只组合/全池的结论；④默认 10 只组合 135,829.03 与全池 174,819.61 仍是每档 2 万的实验值，未按 5,000 重算。
- **下一步 + 别碰**：①打开页面刷新后复核输入框与 chips；②若要默认 10 只组合/全池按新每档 5,000 重算，需另开一版并同步 README/FRONTEND（不要手改旧数字）；③宽屏 1900 实拍；④全量 gate 的 fund_monthly 既有 FAIL 单独修。别碰：`__DD_STATE` 是唯一出厂入口，不要另加 localStorage 默认覆盖；`__ddReset` 与 `ruleCardHtml` 兜底必须与初值一致；`index-term` 的 10 万/2 万对照不改。**已发布，勿回退 v1116 默认。**

### 2026-11-25 · 策略×信号审计（文档，非发布）

- **改了什么**：新增 `docs/STRATEGY_SIGNAL_AUDIT_2026-11-25.md` 与 `docs/strategy_signal_audit_2026-11-25.csv`（59 条逐条判定）；生成脚本 `edit_work/_audit_signal_registry_2026_11_25.py`。未改 `edit_work/index.html`、未改三态、未交易、未升版。
- **未验证的假设**：当前持仓/信号为 2026-11-25 页面快照（信号数据日 2026-11-23）；20 日样本外未做显著性；V11 ATR 用净值近似未做 OHLC 复核；实际组合 18,068 与目标 50,000 的口径差异未由账本逐笔复核。
- **下一步 + 别碰**：先看报告 §0/§1/§5/§8；P0 是先统一资金口径、定义 T4/T13/R7/T1 优先级与执行状态，再谈改信号。别碰：`__DD_STATE` v1117 默认、`index-term` 终止样本 10 万/2 万对照、59 条注册表原始 ID（新增只加不改）。

### 2026-11-25 · 资金口径定稿（文档，非发布）

- **改了什么**：用户拍板「策略资金按 5 万计划」；已写入 `docs/STRATEGY_SIGNAL_AUDIT_2026-11-25.md`（头部决策、§1.3、§8 P0-1）、`docs/FRONTEND.md` §6 顶部、README「当前进度 / 待决 / 下一步」。口径：`STRATEGY_SNAP.totalTarget=50000` 为唯一策略基准；18,068 只是到位进度 36.1%；V11 狙击池 5%＝¥2,500（策略口径，回测按回测预算）；DD 10 万/5,000、终止样本 10 万/20,000 是独立实验；T9 的 100,000 不是策略基数。未改代码、未改三态、未交易、未升版。
- **未验证的假设**：`STRATEGY_SNAP.totalTarget=50000` 仍是 2026-09-17 的静态快照；`SIGNALS_CFG.barbell` 的权重分母、`rulesBudget()`、`btCfg` 默认预算是否都实际取 5 万，未逐处打断点复核；V11 注册表 `def` 仍写“池 10%”，本轮只记待改、未改页面。
- **下一步 + 别碰**：①按报告 §8 P0-1 把 5 万口径写进页面标注（V11 文案改“池 5%＝¥2,500”）；②T4/T13/R7/T1 优先级另开一版；③V11 文案与引擎默认同改时需升版、真渲染截图、发布。别碰：`__DD_STATE` v1117 默认；`index-term` 10 万/2 万对照；`STRATEGY_SNAP` 五处同源载体的金额；59 条注册表原始 ID。

### 2026-11-25 · v1122（V11 赔率公式统一 · 已发布 master `ddb7082df76d`）

- **改了什么**：`edit_work/index.html` 徽标 v1121→v1122（tag `fw2_v1122_v11_formula_unified`）；配置回测新增 `seriesBy[*].p1260`/`lo1260` 单调队列（前 1260 根、不含当日），`v11Gate` 改为 `(p1260−nav)/(nav−lo1260)`，门槛默认 2.5；`_SNP.den` 固定 `'leg1260'`，`SIGNALS_CFG.v11Den` 同步，旧 `atr/leg20/leg60` 退役；注册表 V11 `modeled/thr`、`LOGIC_WHERE.V11`、配置回测参数说明、投资逻辑清单改为 1260 日窗口，`act` 旧 3×ATR 收益标为历史；`gen_v11_signal.py` docstring 改成以 `bt_signal.entry_signal` 为准、`bt_v11.py` 为旧研究引擎；README frontmatter 与三节、`docs/FRONTEND.md` §10.19 注 + 新增 §10.20 已同步。
- **未验证的假设**：①配置回测 V11 分支要 `window.SCREEN_POOL` 已加载才有点位；本次本地配置回测结果里 V11 未产生交易（筛选池未就绪 / 新公式在 2023-07 起区间未达 2.5），不代表分支未接线；离线按同一算法复算末日赔率 159949 3.466463 / 513050 30.300000 / 513180 14.580645 / 510300 1.128902 / 588000 1.879310 与 `v11-signal.json` 逐位一致。②统一后尚未用新公式重跑配置回测替换旧 3×ATR 收益结论；注册表 `act` 已明写旧数字失效。③宽屏 1900 未实拍（1430 已截图核）。
- **下一步 + 别碰**：已发布 → `verify_sync --gh-only`；线上实测徽标 v1122 与文案通过；若要重跑旧收益结论，另开一版并同步 README/FRONTEND。别碰：`p250` 别删（V2/M6/T7 仍在用）；`v11Gate` 与 `v11Prep()` 不要各写一套；`_SNP.den` 不要再加回 `atr/leg20/leg60`；运行回测 2,500/625/4 仓仍是 5 万策略池 5% 口径。

### 2026-11-25 · v1123（聪明的钱插入锚点修正 · 已发布 master `8fa7d5cf59d3`）

- **改了什么**：`edit_work/index.html` 徽标 v1122→v1123（tag `fw2_v1123_sm_insert_anchor`）；页尾脚注加 `id="sigFootNote"`，`#view-smartmoney` 搬移锚点由 `body.querySelector('.dc-note')`（误命中 V11 迁移提示）改为 `#sigFootNote`，兜底取最后一个 `.dc-note`。DOM 顺序恢复为阈值来源 → V11 提示 → 七标签 → 筛选条 → 各 pane → 聪明的钱 → 页尾脚注；标签组不再被两张 ETF 表压到后面。README frontmatter 与三节、`docs/FRONTEND.md` §10.21、`docs/PITFALLS.md` P-v1123 已同步。线上 `?t=v1123live&final=1` 实测徽标 v1123、`view-smartmoney` 位于 `sigThroughPane` 后 / `sigFootNote` 前、17 行；raw `caifu/index.html` 5,369,050 B / SHA256 `D964FCE5…` 与本地一致。
- **未验证的假设**：①CDP 1430/1900 截图里阈值来源与表头文字不落墨，但 532 原生截图同一页可见、DOM `color`/`display` 正常，判断为 emulation 截图图层问题，不是页面样式；②本次只修插入锚点，未改聪明的钱表格数据、口径或 ETF 份额逻辑；③宽屏真实用户窗口下的最终观感以线上刷新后为准。
- **下一步 + 别碰**：打开线上页刷新后进「交易信号 → 聪明的钱」，应看到七标签与筛选条在顶部、两张 ETF 表在其后；若仍有错位，先查 `#sigBody` 子节点顺序而不是改 CSS。别碰：`#sigFootNote` 不要删/改名；`#view-smartmoney` 不要复制第二份；不要用第一个 `.dc-note` 当页尾锚点。

### 2026-11-26 · v1123 交接文件（给 WorkBuddy 继续 · 未改代码、未发布）

- **改了什么**：新增 `docs/HANDOFF_v1123.md`（线上 URL、master、SHA256、正确 DOM 顺序、只读验收脚本、发布门禁、下一步选项、别碰清单）；未改 `edit_work/index.html`、未改数据、未重新发布。
- **未验证的假设**：CDP 宽屏截图“文字不落墨”仅判断为截图工具图层问题，未用第二款浏览器独立复核；聪明的钱 17 行是两张表合计，不是单表 17 行。
- **下一步 + 别碰**：WorkBuddy 接管后先跑只读验收（徽标 v1123 / `#sigBody` 顺序 / 17 行 / 控制台），再按交接文件第七节拍板；别碰 `#sigFootNote`、`#view-smartmoney`、标签组在内容前的位置，不要顺手重跑数据链。

### 2026-11-26 · v1129（我的持仓新增账户口径对账卡 · 已发布 master `b74d35610526`）

- **改了什么**：`edit_work/index.html` 徽标 v1128→v1129（tag `fw2_v1129_hold_recon`）；`#hdSummary` 后新增 `#hdRecon`，`buildRows()` 后新增 `holdReconData()` / `renderHoldRecon()`，`renderHoldings()` 在 `renderDiscipline(all)` 前调用；四格＝账户总资产 20,565.55 / 确认份额×净值 18,067.10 / 在途 2,498.46 / 明细市值合计 15,688.38；`<details>` 展开 18 只逐只差异，012920 红底 −4,870.71、标记「份额待重建」。同步 `docs/FRONTEND.md` §10.27、`docs/PITFALLS.md` P-v1129、README 三节。
- **未验证的假设**：①账户口径「权重用确认份额×净值、总值用 holding_total」仍是页面临时约定，未获用户拍板；②012920 的 shares 与账户市值差 −4,870.71，只确认了「份额未随对账单重建」，未确认是哪一笔卖出未重建；③逐只四舍五入差 6.46 与在途差 6.46 同额但来源不同，未逐笔核到分。
- **下一步 + 别碰**：先线上 `?t=v1129live&final=1` 验收徽标、四格与 18 行差异表；再拍板账户口径，补 012920 新对账单后跑 `rebuild_holdings.py`；继续清单 1.2/1.3/1.4。别碰：`HOLDINGS_SEED` 与 `holdings-data.json` 不手改；`state.portfolio` 的份额字段是 `qty` 不是 `shares`；`holdings.marketValue` 合计不可当组合市值；对账卡不改市值/信号/资产配置计算。


### 2026-11-26 · v1133（阶段1三件套：资金口径条 / 四桶目标vs实际 / 新钱分配路线 · 已发布 master `2fb40563cdce`）

- **改了什么**：`edit_work/index.html` 徽标 v1129→v1133（tag `fw2_v1130_capital_labels` / `fw2_v1131_bucket_target_vs_actual` / `fw2_v1132_new_money_route` / `fw2_v1133_caliber_split_note`）；`#capCaliber` 顶部常驻四 chip；`bucketCardHtml()` 四桶四格；`newMoneyRouteHtml()` 缺口比例表；两卡脚注拆分 5 万主基准与表标题 62,000 预算。同步 `docs/FRONTEND.md` §10.28、`docs/PITFALLS.md` P-v1130/P-v1131/P-v1133、README 三节。
- **未验证的假设**：①「5 万是否唯一主基准」仍未拍板，页面只做口径拆分，未改 `fw2_capital_budget_v1` / `STRATEGY_SNAP.totalTarget`；②四桶实际合计 17,669 是发布时点，线上复核已随报价变为 17,839，不能当固定快照；③四桶偏离带 5pp 只用于展示，未验证 T10 真触发时的实际再平衡动作；④顶部口径条是否算「全站」，未获用户验收（当前只顶部一条，未逐模块加 chip）。
- **下一步 + 别碰**：线上 `?t=v1133live&final=1` 验收徽标 v1133、四 chip、四桶四格、新钱表与两段脚注；拍板 5 万 vs 62,000 后，再决定是否重算表标题/四桶分母；随后进入阶段 2（act 信号状态 / 冲突优先级 / 按类型 SLA / 今日待办 Top 5）。别碰：四桶卡只展示不交易；`slotBand` 不要换成 `band`；`#capCaliber` 不要改回 `nowrap+overflow-x`；`HOLDINGS_SEED` / `holdings-data.json` 不手改；012920 仍等新对账单。


### 2026-11-26 · v1134（资产配置表标题预算 62,000→50,000 · 已发布 master `2f710c46c1dc`）

- **改了什么**：`edit_work/index.html` 徽标 v1133→v1134（tag `fw2_v1134_budget_50000`）；`RULES_KEY` 后新增 `budgetMigrate50000` 一次性迁移（仅 `fw2_capital_budget_v1===62000` 时改写 50000，其他自填值保留）；四桶卡/新钱路线脚注由「5 万策略主基准（待拍板）」改为「2026-11-26 已拍板，表标题预算同步为 50,000」。同步 `docs/FRONTEND.md` §10.29、`docs/PITFALLS.md` P-v1134、README 三节。index 5,402,004 B / SHA256 `1FFB71C4CDDFB2A8F30194E8F195BAD266424CF58201A7ECEB6209EB4E77628D` / 纯 LF；提交 `2f710c46c1dc`。
- **未验证的假设**：①线上 `localStorage` 迁移后立即变 50000，已在当前浏览器实测；其他设备若从未存过 62000，则输入框为空、表标题回退 50,000（未逐设备验证）；②新钱缺口 32,161 是截图时点动态值，不是固定快照；③538 视口下资产配置表当前为用户此前选择的「完整 14 列」，表格列挤压属既有列显隐状态，不是本版引入，未强改用户偏好。
- **下一步 + 别碰**：线上 `?t=v1134live&final=1` 验收徽标 v1134、`localStorage=50000`、标题「计划 ¥ 50000」、四桶目标 ¥50,000 与两卡脚注；随后进入阶段 2（act 信号状态 / 冲突优先级 / 按类型 SLA / 今日待办 Top 5）。别碰：迁移只认恰好 62000；不要把 5 万写死进 `rulesBudget()`；不要改 `STRATEGY_SNAP.totalTarget`（本来就是 50000）；不要覆盖其他自填预算；`HOLDINGS_SEED` / `holdings-data.json` 不手改，012920 仍等新对账单。


### 2026-11-26 · v1135（预算迁移加一次性守卫 · 已发布 master `0df99aa5f7a2`）

- **改了什么**：`edit_work/index.html` 徽标 v1134→v1135（tag `fw2_v1135_budget_migrate_once`）；`budgetMigrate50000` 新增 `fw2_budget_migrated_50000_v1` 守卫：标记不存在时才检查并迁移，迁移后写标记；标记存在直接 return。目的：v1134 只按值迁移，用户以后主动设回 62000 会被再次改掉。index 5,402,443 B / SHA256 `204327165DDB3D0D76593470924E1B82AC137AC315C9FAEA4DC0C8E2679764C2` / 纯 LF；提交 `0df99aa5f7a2`。同步 `docs/FRONTEND.md` §10.29（改为 v1134–v1135）、`docs/PITFALLS.md` P-v1135、README 三节。
- **未验证的假设**：①线上当前浏览器标记已写为 1，已在 v1135live 实测；②其他设备首次加载 v1135 时若预算仍是 62000，会迁移并写标记（未逐设备验证）；③新钱缺口 32,161 仍是截图时点动态值，不是固定快照；④538 视口下资产配置表当前为用户此前选择的「完整 14 列」，表格列挤压属既有列显隐状态，不是本版引入。
- **下一步 + 别碰**：线上 `?t=v1135live&final=1` 验收徽标 v1135、`fw2_capital_budget_v1=50000`、`fw2_budget_migrated_50000_v1=1`、标题「计划 ¥ 50000」；再主动设回 62000 刷新，验证守卫保持 62000；随后进入阶段 2。别碰：不要删 `fw2_budget_migrated_50000_v1` 守卫；不要把 5 万写死进 `rulesBudget()`；不要改 `STRATEGY_SNAP.totalTarget`（本来就是 50000）；`HOLDINGS_SEED` / `holdings-data.json` 不手改，012920 仍等新对账单。


### 2026-11-26 · v1136（交易信号 act 四态 + 窄屏横滑修复 · 已发布 master `e9cd2a423c37`）

- **改了什么**：`edit_work/index.html` 徽标 v1135→v1136（tag `fw2_v1136_act_state`）。新增 `fw2_act_state_v1` 四态状态机（待执行/执行中/已执行/已过期）、9 列表格、执行按钮、执行状态汇总、近 14 日过期折叠；`renderTodayTodo` 只计 pending+doing。连带修 9 列把 `.dc-card` 撑到 1212px 导致 538 视口看不到执行列的问题：`.dc-card/.dc-body/.sig-wt-area{min-width:0}` + `.table-wrap{max-width:100%}` + 移动端横滑提示。index 5,412,170 B / SHA256 `319D97BF0AFCEF20523184989A583B5B8266B669A0C2980AAC5351C6EAC4BDB9` / 纯 LF；提交 `e9cd2a423c37`。同步 `docs/FRONTEND.md` §10.30、`docs/PITFALLS.md` P-v1136、README 三节。
- **未验证的假设**：①线上当前浏览器 `fw2_act_state_v1` 为空，首次加载会新建 94 条 pending，已在 v1136live 实测；其他设备首次加载同逻辑，未逐设备验证；②「知道了」仍保留在 pending/doing act 行（7 天免打扰，不改执行状态），只从已执行行隐藏；是否彻底移除未拍板；③同指数合并/观察折叠组内 act 行默认折叠，94 条 act 中当前仅 55 个可见按钮，其余需点「展开全部 N 只」；④`renderTodayTodo` 仍只统计持仓 `sig.hold`，未纳入筛选/市场；⑤538 视口下资产配置表完整 14 列的既有挤压未改。
- **下一步 + 别碰**：线上 `?t=v1136live&final=1` 验收徽标 v1136、`待执行 94`、横滑可见执行列、开始→完成→刷新保持→撤销；随后进入 2.2 同日冲突优先级 → 2.3 按信号类型 SLA → 2.4 今日待办 Top5。别碰：`fw2_act_state_v1` 不要并进 `fw2_logic_v1`；`signalEvalAll` 判定/lvl/阈值/排序/三态不改；`.dc-card/.dc-body/.sig-wt-area` 的 `min-width:0` 与 `.table-wrap` 的 `max-width:100%` 不要删；012920 仍等新对账单；全量 gate 仍受 `fund_daily` 既有 FAIL 阻断，发布走 `SKIP_GATE=1`。

### 2026-11-26 · v1137（同日冲突优先级 + 买入门禁 · 已发布 master `1105444f55f5`）

- **改了什么**：`edit_work/index.html` 徽标 v1136→v1137（tag `fw2_v1137_act_priority`）。新增 `ACT_PRIO` / `actPrioOf` / `actTargetKey` / `actConflictMap` / `actConflictHtml`；同一 `pool|code|name` 的 act 行按 rank 排序（T4/R6 硬止损 10 → T2 20 → R7 30 → T1 40 → T3 45 → T16 50 → P2/TREND-DN/S-TREND 55/60 → T7/W2/S2 70 → T8 75 → T13/R3 80 → V11 85；S1/T15 不排序），买入行被更高 rank 且 `pending/doing` 的风控/拦截/卖出项压制时，执行列 disabled「开始」+「先 T4 硬止损」；筛选条可点「同日冲突 21 组 · 查看顺序」，表下 `<details id="sigConfBox">` 列 21 组与优先级口径。index 5,424,386 B / SHA256 `B5CC7E62DAEC7E4E01223A9D1072E72E03DA0D4F250C9BB53E89C560CCEF587A` / 纯 LF；提交 `1105444f55f5`。同步 `docs/FRONTEND.md` §10.31、`docs/PITFALLS.md` P-v1137、README 三节。
- **未验证的假设**：①T4 点「完成」后 T13 立即恢复可点（同日门禁），未做冷却期；T4 是否真硬止损仍待拍板；②T7/T13 同日加仓只在面板提示「先算合计」，未落金额/笔数上限，当前数据也无 T7+T13 同组样本；③R7/T1 同日只卖一笔的排序已预置，但当前无同组多卖样本、R7 实盘未落地；④`actTargetKey` 按 `pool|code|name`，同一代码跨池暂不合并；当前无跨池样本；⑤21 组里只有 13 条默认可见 disabled，其余在折叠组内；⑥538 视口下资产配置表完整 14 列挤压是既有偏好。
- **下一步 + 别碰**：线上 `?t=v1137live&final=1` 验收徽标 v1137、筛选条「待执行 95 · 同日冲突 21 组」、面板 21 组、000307 组 T4 1/3 / TREND-DN 2/3 / T13 3/3、T13 置灰「先 T4 硬止损」；随后 2.3 按信号类型 SLA → 2.4 今日待办 Top5。别碰：`ACT_CONF` 是局部变量不是 `window.ACT_CONF`；`ACT_PRIO` 按 `sig.split(' ')[0]` 的规则码匹配，改信号代码（首个 token）必须同步改键，只改中文描述不影响；`blockedBy` 只认 `pending/doing`，不要把 T4 `done` 说成永久禁买；`actStateKey` 不要和 `actTargetKey` 混用；`fw2_act_state_v1` 结构不改；全量 gate 仍受 `fund_daily` 既有 FAIL 阻断，发布走 `SKIP_GATE=1`。

### 2026-11-26 · 多资产/多策略完善度分析（只读，未改工程/未发布）

- **改了什么**：无代码/数据改动。读 README 入口、`handoff_check`、47 数据集清单、`holdings-data.json`、`STRATEGY_SNAP`（11 只/5 万）、`docs/STRATEGY_SIGNAL_AUDIT_2026-11-25.md`、v1136/v1137 记录。实测 refreshFailed=['fund_jjcc','index_daily','macro_extra']。
- **未验证的假设**：①按份额×净值权威口径重算四桶＝16.84/64.70/16.44/2.01（四桶内 17,292.05、计划外 775.05、012920=10,283.5），与 v1117 审计 18.5/63.8/15.7/2.0 同源但时点不同；②「缺资产类别」是从计划 11 只 vs 常见多资产类别推导，非用户已确认需求。
- **下一步 + 别碰**：若继续，先拍板「先闭环再扩容」——组合级回撤闸门 / R2 定投决策 / R7 实盘再平衡优先于新增资产类别与策略。别碰：本轮只读，未改任何 JSON/HTML/三态；`marketValue` 字段对 012920 不可信，汇总一律份额×nav。
### 2026-11-26 · v1138 交易信号按信号类型 SLA（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1138 + tag `fw2_v1138_act_sla`，已发布提交 `9837dd4de1b8`（5,433,445 B / SHA256 `7E6BD8A0CD37746F116D2FA970690D562A16C0AAE374AEA89BFFB645F96F8D4B` / 纯 LF）。①新增 `ACT_SLA` / `actSlaOf` / `actSlaAge` / `actSlaState` / `actSlaCount` / `actSlaHtml`：风控/卖出 T+1、拦截复核 T+1、网格/补仓/加仓 T+2、观察 T+5、季频/宏观 90 日、T10 不设；非 T 代码默认月频 90 日。②`trHtml` 执行列在状态徽章下显示 SLA，仅 pending/doing；`done/expired` 不显示且不计超时。③筛选条新增 `.sig-sla-sum`，点开 `#sigSlaBox` 列超时/复核滞后；表下面板放在 `actConflictHtml` 之前。只改渲染/提示，不改判定/阈值/状态/交易。
- **未验证的假设**：①SLA 默认档位是审计 §5.6 的落地默认，用户尚未逐档拍板；②日龄按周一至周五计、不含法定节假日，不是交易所日历；③`actSlaCount` 只统计 pending/doing，已执行/已过期不计超时；④`actSlaHtml` 只列 `over` 行，`due` 只进行内/汇总计数；⑤本地 95/21 与线上 99/23 的 act 基数不同，**未归因**，两者不是同一快照，勿对拍；⑥初版 M16/M18 误落 T+2 已修正，市场 5 条全 `SLA 月频`。
- **下一步 + 别碰**：线上 `?t=v1138live&final=1` 验收徽标 v1138、筛选条「待执行 99 · 同日冲突 23 组 · 查看顺序」+「SLA 超时 1 · 复核滞后 20 · 查看时限」、面板 21 条、市场 5 条 `SLA 月频`、T4 019441 行 `SLA T+1 · 今日到期`、T13 行 `SLA T+2` + 灰色开始。随后 2.4 今日待办 Top5。别碰：`ACT_SLA` 非 T 默认分支；`ACT_PRIO` 首 token 键；`ACT_CONF` 局部变量；`fw2_act_state_v1` 结构；不要给 `signalEvalAll` 加 SLA 判定；全量 gate 仍受 `fund_daily` 既有 FAIL 阻断，发布走 `SKIP_GATE=1`。

### 2026-11-26 · v1139 今日待办 Top5（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1138→v1139 + tag `fw2_v1139_today_top5`，已发布提交 `de32c11b0b23`（5,447,611 B / SHA256 `7553D4E1A36006F9CED372CFB52F13F65A8B3475F9104780863D9A2EEC469EB8` / 纯 LF）。①`#todayTop5` 默认收起的 `<details>`，位于 `#todayBand` 后、`#pfSrcNote` 前；展开态存 `fw2_tt5_open`。②`TT5_POOL_RANK` / `todayTop5Data()` / `renderTodayTop5()`：三池 act 合并、`code|sig` 去重优先持仓、排除 done/expired/padRow；排序 ACT_PRIO → SLA → 日龄 → doing → 池；5 张横滑卡。③`trHtml` 加 `data-sigkey`；卡片点击切 `showView('signal')` 对应 tab、轮询目标行并高亮；700ms 复查防重建替换，tab/pane 按实际 display 重试。④`renderTodayTodo` 开头与 `actStateSet` 末尾刷新 Top5；holdings 分支回页刷新。⑤首屏 chips 改「持仓行动 / 持仓补仓点 / 持仓接近」，避免与三池 97 条误读。同步 README 三节、`docs/FRONTEND.md` §10.33、`docs/PITFALLS.md` P-v1139、本文件。
- **未验证的假设**：①前 5 全 T4 是当前数据 + 排序结果，不代表未来买入信号不会进前 5；②“持仓 56 / 自选 0 / 筛选 45”是本轮快照，与 v1138 条目 55/27/5 不是同一时点，未归因差异；③538 视口默认只完整显示 3 张、第 4 张部分，横滑可看第 4–5 张，未在真机触屏上验证滑动惯性；④`fw2_tt5_open` 只在当前浏览器验证，其他设备首次默认收起；⑤后台标签截图空白是 `v43fade` 动画冻结，已用强制 opacity 取证，未改页面 CSS；⑥线上 `?t=v1139live3&final=1` 已核 97 条 / 5 卡 / 点击高亮，未做 1900 宽屏实拍。
- **下一步 + 别碰**：线上 `?t=v1139live3&final=1` 强刷验收徽标 v1139、Top5 默认收起、chips「持仓行动 56 条」、展开 5 卡、点首卡切持仓 tab 高亮 019441 T4；确认后进入 P1「估值缺数据降级」，再排 P1 证据分级。别碰：`#todayTop5` 不要改常显；`todayTop5Data` 的 `code|sig` 去重；`ACT_PRIO` 首 token 键；`sig-row-hit` 的 700ms 复查与 tab/pane 重试；`fw2_tt5_open` 只存 `'1'`；不要新增 `window.__todayTop5`；012920 仍等对账单；全量 gate 仍受 `fund_daily` 既有 FAIL 阻断，发布走 `SKIP_GATE=1`。

### 2026-11-26 · v1140 ERP 10Y 固定 3%（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1139→v1140 + tag `fw2_v1140_erp_fix3`，已发布提交 `e83bfaa15704`（5,450,389 B / SHA256 `3058ADD8C8F363630247040457DA33D2F72488FFA23C8AE14642700F38AD7BDC` / 纯 LF）。①新增顶层 `ERP_FIX_Y10=3.0` / `erpFixed3(e)`，把 ERP 序列按 `[date,E/P,3.00,E/P−3.00]` 重算并对全序列算 10 年分位，不挂 `window`。②ERP 卡四格改为 E/P 7.70 / 固定 10Y 3.00 / ERP 4.70 / 分位 43.1，指向改「均衡偏债」，新增「口径」行；图表 legend/柱/线走固定序列。③M9 改 `erpFixed3`，分位 43.1 / ERP 4.70 / 10Y 固定 3.00，级别 watch、方案「【不动】暂不操作 · 定投照常」；数据日改为 ERP 末点 `2026-10-15`，不再取 `updatedAt`。④`cycleEngine` / `pxCycleAndSigs` 的 `erpPct` 同步固定序列。**未动**：M16 格雷厄姆、M11 中美利差、股息率比较仍用真实 10Y；`macro-data.json` / `MACRO_SNAP` 原始 erp 未改。同步 README 三节、`docs/FRONTEND.md` §10.34、`docs/PITFALLS.md` P-v1140、本文件。
- **未验证的假设**：①历史 M9 快照仍按原始 `erpPct`（82.1），当前页 43.1，二者不可对拍；`gen_macro_snap.py` / `gen_signals_hist.py` 尚未改。②固定 3% 是全历史重算，不是只替换当前点；若你本意只是当前点替换、历史分位仍用真实 10Y，需要再改口径。③`ERP=4.70` / 分位 43.1 来自 `macro-data.json` 123 点现算，末点 2026-10-15；数据未刷新到今日，M9 行有 stale 标记。④538 视口 ERP 卡四格为单列（响应式），M9 表内横滑 1180 只看左列，不是裁切 bug。⑤线上 `verify_sync --gh-only` 已见 GitHub 字节一致，但长清单仍在跑，未等完整 PASS 尾行。
- **下一步 + 别碰**：先做 P1「估值缺数据降级」——000834 / 022438 / 020712 / 000307 等缺估值持仓，T3/T8/T15 只显示「数据缺失」不显示 act，P4 覆盖率作数据闸门；再做 P1「证据分级」A+/A−/A? + 59 条机制归并。别碰：ERP 卡以外的 M16/M11/股息率不要用固定 3%；不要改 `macro-data.json` 原始 `erp.cur.y10`；不要把 M9 数据日改回 `updatedAt`；不要为截图删 `v43fade`；历史快照未重算前不要与当前页对拍；全量 gate 仍受 `fund_daily` 既有 FAIL 阻断，发布走 `SKIP_GATE=1`。

### 2026-11-26 · v1141 审计 P1（估值缺数据降级 + 证据分级 + 机制归并 · 已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1140→v1141 + tag `fw2_v1141_ev_tier`，已发布提交 `48d862d70c52`（5,459,968 B / SHA256 `3621EBF8C979D00C1976793435326D1A12594BD2E69091B71421FEC344AAC826` / 纯 LF）。①`signalEvalAll` 持仓 T15 增 `else rows.hold.push(valMissRow(base, 'T15 跟踪指数PE分位', valNaKinds(name)))`，缺 PE 分位不再静默消失，`watch` / 不出 act / 品类豁免文案；T3/T8 共用同一占位。②P4 注册表与信号行改「覆盖率（数据闸门） / 非交易信号」，当前覆盖率未低于 50%，无真实行。③新增 `SIG_EV_TIER / SIG_EV_NOTE / SIG_MECH / sigEvTier / sigEvLabel / sigEvBadge / logicEvStats / logicMechHtml`；59 条拆 A+ 7 / A− 9 / A? 8 / A· 2 / C 33；总纲普通规则表加「证据」列（11 列 / min-width 1988px）；A 卡加摘要行与「生效≠有 alpha」说明；10 个机制族归并、成员表带代码+中文名；`logicEffNoteHtml` 改写「A− 9 条只作实验/观察」。④回测规则卡 `_rRowHtml` 改用同一套证据徽标，删除旧「证据 A/B/C」映射。同步 README 三节、`docs/FRONTEND.md` §10.35、`docs/PITFALLS.md` P-v1141、本文件。
- **复核更正（v1142 尝试已回退，不另发版）**：曾据「000834 无净值序列」假设在 `one()` 早退分支加 T3/T8/T15 缺失兜底，徽标升 v1142；真实渲染发现 000834 仍不在默认表，进一步展开纳指100 同指数族后看到它本就有 11 条信号行，说明 `one()` 正常返回、兜底不触发。根因是同指数族折叠，不是缺数据。已删除该兜底并回退徽标，`index.html` 5,459,968 B / SHA256 `3621EBF8C979D00C1976793435326D1A12594BD2E69091B71421FEC344AAC826` 与 v1141 完全一致；未提交、未发布。
- **未验证的假设**：①T15 占位只覆盖走到 `signalEvalAll` 持仓段的标的；`000834` 复核更正为「纳指100 同指数族折叠隐藏」——它有完整净值、11 条信号行，T3/T8/T15 均为缺失占位且 0 条估值 act，默认排第 10 只被折叠，点「展开全部 12 只」可见；先前「fund-daily 无 ≥20 点序列、`one()` 早退」的假设已证伪，v1142 兜底实测不触发并已完整回退（SHA256 与 v1141 一致，不另发版）。②P4 代码已改但覆盖率未 <50%，线上无 P4 行，未做触发截图，不能声称已线上触发。③A+/A−/A? 分级来自审计 CSV 与本次映射，未重跑样本外统计验证；A 只表示测过，不等于可信。④机制族合计 59 依赖 `SIG_MECH` 手写映射，未来增删信号若不同步会少条。⑤证据徽标 11 个是当前买入层可见行数，非全 59 行；全表需逐层切换核对。⑥线上 538 只量了 `bodyW=529/bodyC=529`，未做 1900 宽屏实拍。
- **下一步 + 别碰**：线上 `?view=tg&t=v1141live1&final=1` 点「投资总纲」验收 v1141 徽标、证据列、A 卡摘要、10 族归并；切「④ 买入节奏」核对 T7/T13/V11=A+、W3/S4=A−、R2=A?；切信号页 T15 看 7 条缺失 0 act；`000834` 点「展开全部 12 只」核对 11 行 / T3/T8/T15 缺失 / 0 估值 act；回测规则卡表头「证据」且全文无裸 `证据 A/B/C`。下一步：拍板 P1 第 5 项 R2 定投（月投或仅手动参考），再做 P2 9–12（组合级风险闸门 / 实际组合 −30%/−44.6%/−60% 压力测试 / 终止风险闸门 / 样本外跟踪 ≥1 年）。别碰：`signalEvalAll` 判定/阈值/三态；`SIG_EV_TIER` 之外复制分级；`SIG_MECH` 与审计 CSV 59 行集合；T15 占位不要升 act；不要再按「无净值」给 `000834` 加 `one()` 兜底，也不要手改它的 holdings/fund-daily；不要把 P4 代码改动说成线上触发；历史 M9 仍按原始 `erpPct`，未重算前不要与当前页对拍；全量 gate 仍受 `fund_daily` 既有 FAIL 阻断，发布走 `SKIP_GATE=1`。

### 2026-11-26 · v1142 R2 定投关 + RB/BW/L1/TREND 手动参考（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1141→v1142 + tag `fw2_v1142_r2_manual`，已发布提交 `8ac16b51f999`（5,464,312 B / SHA256 `A50A464A5BF869ADBFAD7AFDAB694E333AEAF4C49AD27B3E5F1838077CA69370` / 纯 LF）。①`SIGNAL_REGISTRY.R2` 改「off（2026-11-26 拍板：不月投 · 实盘一次性）」；RB/BW 改「on（仅信号 · 手动参考）」，`act/modeled` 补不自动执行。②投资总纲加执行口径黄条；RB/BW 市场行、L1 四条、TREND-UP/DN 的 `thrAct/thr/plan` 全部改手动参考；`sigRowHtml` 加行级「手动参考」小徽标。③新增 `dcaManualOnly()`，R2 只有 `on` 才算非手动；首屏标签「定投节奏 · 手动参考」，结论「不自动月投 · 触发只提示，不自动下单」。④趋势策略横幅/四磁贴补手动参考与明面执行口径；个基趋势行动列改「行动参考（手动）」并移第 2 列，文案改「不自动月投 / 减速·暂缓（手动参考）/ 不加仓」，列宽 152、两条建议 `<br>` 分行。⑤全站清 53 处「定投照常」→「不自动月投」、8 处「维持定投」→「不加仓」、1 处「月定投照常执行」→「月投不自动执行」。同步 README 三节、`docs/FRONTEND.md` §10.36、`docs/PITFALLS.md` P-v1142、本文件。
- **未验证的假设**：①RB 行当前市场信号页未出现（`data-sigkey` 无 `:RB:`），原因未核实，不能断言 bug；②78 个行级「手动参考」徽标是否视觉过密尚未拍板，本轮保留逐行显示；③M1–M17「定投照常」已统一改写，但 M 系是否应独立于 R2 仍属展示口径，未改其判定；④线上首次净值加载约 70 秒，非页面报错，但未在多网络环境复测；⑤538 视口行动参考列完整，1900 宽屏未实拍；⑥`012920` 账户市值 5,412.79 与份额×净值 10,283.50 的差仍挂账，未重建份额。
- **下一步 + 别碰**：线上 `?view=signal&t=v1142live1&final=1` 验收徽标 v1142；首次加载等 60–90 秒，切「趋势策略」看总说明、四磁贴「手动参考」、个基趋势表头「行动参考（手动）」与 012920「不自动月投」；再点「投资总纲」看黄条。P2-10 已出 `docs/P2_STRESS_TEST_2026-11-26.md`：**012920 页面口径 56.92% / −44.6% 拖累 −25.39pp，账户口径 26.32% / −11.74pp，结论翻转；先重建 012920 份额，再定 P2-9 闸门阈值**（草案单只 20% 上限、压力 ≤20pp、实际回撤 15% 冻结 / 20% 评估，只提示不自动卖）。别碰：`signalEvalAll` 判定/lvl/阈值/三态；`dcaManualOnly` 只在 R2=`on` 时返回 false；RB/BW 的 `on` 是档案启用，不要为文案改成 `obs`；L1/TREND 不要写「暂停定投」；M 系文案已清理但不要反向改回「定投照常」；012920 份额仍等对账单；全量 gate 仍受 `fund_daily` 既有 FAIL 阻断，发布走 `SKIP_GATE=1`。

### 2026-11-26 · v1143 012920 份额对账 + 活期宝拆行（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1142→v1143，tag `fw2_v1143_012920_share_fix` + `fw2_v1143_recon_note_fix`；GitHub `caifu/index.html` 5,466,535 B 字节一致 / SHA256 `BF00FE1569230D1A77C7AC328B9EE02F835D1EBC9E1A3E1807D618C055C7335D`。①`TRADE_QUERY` 两笔 confirmed 卖出（11-05 1,621.57 份 / 5,120.84 / 净值 3.1699；11-25 1,621.57 份 / 4,877.17 / 净值 3.0228），对账单 2026-10-29 持有 5,045.18 → 余 1,802.04 份；旧 3,423.61 只扣第一笔。②成本按原单位成本 2.6164 等比结转 4,714.86，11-25 净值 2.9747 → 市值 5,360.53；与账户 `holding_list` 5,360.53 / constantProfit 645.74 一致。③第二笔赎回款落 020097 中加货币E 4,877.17；活期宝拆 000912 2,843.63 + 020097 4,877.17 = 7,720.80；total 20,541.42 / 决策权重 18,036.08 / 在途 2,505.37。④`refresh_holdings_ttskill.py` 按 `holding_hqb` 明细逐只建 cash 行，`buy_codes` 排除 `acct_hqb`；`_audit_capbal_kpi.py` 现金豁免改按 `assetType='cash'` 动态识别，020097 补 `firstBuyDate=2026-11-25` / `firstBuyNav=1.0`。⑤对账卡 `mvGap=0` 时改说“已对平；逐只差额正负相抵，合计等于在途 2,505.37”，删除“其余 733.01 为逐只四舍五入”。同步 README 三节、`docs/FRONTEND.md` §10.37、`docs/PITFALLS.md` P-vP210 重写 + P-v1143、`docs/P2_STRESS_TEST_2026-11-26.md` 重写为 29.72% / −13.26pp。
- **未验证的假设**：①`holding_total` 为 2026-11-26 约 15:30 快照，收盘后净值可能再变；`navDate=2026-11-25` 对 012920，11-26 净值未出。②020097 无 `ledger-import` 现金流、无 `meta-bundle` 画像、无 `FUND_LX_RAW` 理杏仁链接，发布审计 3 条 WARN（不阻断），现金行未补假记录。③`total 20,541.42` 与 `12,820.62 fund + 7,720.80 hqb` 逐分相加为 20,541.42，但其他基金逐只净值时点可能仍差 ≤0.03。④`P2-9` 阈值未拍板、未写入代码；29.72% 只表示单只超 20%，不表示压力 20pp 已破。⑤`push_gh_v39.py` 在推完 index / holdings-data / nav-hold 后，拉后续文件清单时 `IncompleteRead` 崩溃；index 已 200 且 `verify_sync --gh-only` 首段字节一致，未重跑整包。⑥020097 在顶部 ticker 显示为「020097 —」（无名称/净值），属现金行不参与基金行情，未改 ticker。
- **下一步 + 别碰**：下一步＝①线上 `?t=v1143live1&final=1` 验收徽标 v1143、对账卡四格、活期宝两行、012920 1,802.04 / 5,360.53 / 账户 constantProfit +645.74；②拍板 P2-9 是否按“单只 20% / 压力 20pp / 实际回撤 15% 冻结·20% 评估，只提示不自动卖”上线只读卡片；③P2-11 终止风险闸门（801862/OMX）、P2-12 样本外跟踪 ≥1 年；④78 个手动参考徽标是否过密、RB 行为何未出现在市场信号页。别碰：`signalEvalAll` 判定/lvl/阈值/三态；不要把 020097 并回 000912；不要手改 012920 shares/marketValue；不要把 29.72% 说成压力超 20pp；不要给 020097 编现金流/画像；全量 gate 仍受 `fund_daily` 既有 FAIL 阻断。

### 2026-11-26 · v1144 P2-9 组合风险闸门只读卡（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1143→v1144，tag `fw2_v1144_p2_gate_readonly`；GitHub `caifu/index.html` 5,471,885 B / SHA256 `636483281D092AC4AC56FF4053A09CCEE871345117F799355F38322CCE3E0891` / 纯 LF；`push_gh_v39.py`（`SKIP_GATE=1`）只 `[200] caifu/index.html`，其余 42 项 unchanged。①`#hdP2Gate` 在 `#hdRecon` 之后，新增三格只读卡；②单只集中度＝最大非现金持仓 `calc` / 决策权重 `calcSum`，上限 20%，当前 012920 29.72%（超 9.72pp，账户 26.10%）；③压力拖累＝最大单只 × P2-10 的 44.6% / `calcSum`，上限 20pp，当前 −13.26pp 未超；④实际回撤 15% 冻结 / 20% 评估，组合高水位未建立，显示「待建立 / 无法判定」；⑤只读，不拦买入、不自动卖、不写状态、不接交易按钮。
- **未验证的假设**：①44.6% 是 P2-10 给 012920 的历史峰回撤情景，不是对任何最大单只都成立的普适压力；最大单只换成其他标的时，卡片仍按同一 44.6% 机械测算，属草案近似；②组合高水位序列未建立，实际回撤项没有真实判定，只能「待建立」；③020097 无 `ledger-import` 现金流、`meta-bundle` 画像、`FUND_LX_RAW` 理杏仁链接，3 条 WARN 不阻断；④线上首屏加载 60–90 秒，尚未在弱网复测；⑤`check_hold_consistency` C 项仍是 18,036.08 + 2,505.37 = 20,541.45 vs total 20,541.42（差 0.03，分位四舍五入）。
- **下一步 + 别碰**：下一步＝①线上 `?t=v1144live1&final=1` 强刷验收徽标 v1144、对账卡后三格卡、012920 红灯与 −13.26pp；②拍板是否接执行层（单只 20% 置灰买入 / 压力 20pp 冻结新增 / 实际回撤只提示）；③P2-11 终止风险闸门（801862/OMX）、P2-12 样本外跟踪 ≥1 年。**refreshFailed 只读取证**：`fund_jjcc` 日志 `HTTPError 514 Frequency Capped`，成功率 42% <60%，按设计保留旧文件；`index_daily` 日志 8 个指数全部 `JSONDecodeError`，源返回非 JSON，保留 11-23 旧文件；`macro_extra` 日志 `ModuleNotFoundError: No module named 'akshare'`，未生成。三项均未改数据、未重跑刷新。别碰：不要把只读卡改成拦买入/自动卖；不要把「压力未超 20pp」说成「集中度没问题」；不要让实际回撤在无高水位时显示「通过」；不要为清 `refreshFailed` 手改 `data-mgmt.json`；不要把 `P2_GATE_CFG` 写进 `signalEvalAll` 或三态。

### 2026-11-27 · v1146 P2-11 终止风险闸门只读卡（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1145→v1146，tag `fw2_v1146_term_gate_readonly`；GitHub `caifu/index.html` 5,481,094 B / SHA256 `27AD952B929DE3C7500C0576475307D92BC6BE83AC5004EB51485112D148D478` / 纯 LF。①`#hdTermGate` 加在 `#hdP2Gate` 之后、持仓表之前，三格只读卡：3 只终止样本 / 2 只跌超 97%、5 类越跌越买未接过滤、24 只非现金持仓 / 0 只接入存续性；②脚注写 801862 峰值 1,521.13 → 终止 10.11、−99.34%、6 买 / 3 卖 / 3 未平、期末 48,777.14、−51.22%、MDD 58.43%；③`renderHoldTermGate()` 优先 `window.__DD_TERM`，否则 fetch `data/index-term.json`；不新增 window 顶层键；④只读，不冻结买入、不自动卖、不写交易状态、不改 `signalEvalAll`/阈值/三态/`data/*.json`；⑤同步 README 三节/frontmatter、`docs/FRONTEND.md` §10.40、`docs/PITFALLS.md` P-v1146、`docs/P2_STRESS_TEST_2026-11-26.md`。
- **未验证的假设**：①宽屏 1280 只做 DOM 几何复核（三格 315/315/315、卡高 213px），没有拿到真实宽屏截图——截图管线仍按 538 物理窗口裁切；538 有本地与线上真实截图。②24 只非现金持仓是当前 `state.portfolio` 动态数；如果持仓增减，卡片会跟着变，不是写死。③801862/OMX 是历史终止样本，不代表当前 24 只持仓的存续性判定。④`verify_sync.py` 原先的 `定投照常` 标记自 v1142 起就是陈旧期望，本轮改成 `不自动月投` 后才 PASS；已对比 v1144/v1145 备份确认不是 v1146 回归。
- **下一步 + 别碰**：下一步＝①线上 `?view=holdings&t=v1146live1&final=1` 强刷验收 v1146、P2 卡下方只读卡、三格数字与 801862 脚注；②拍板 P2-11 是否接执行，并定义存续性 / 长期相对强弱 / 成分结构恶化的阈值与数据源；③压力 20pp、实际回撤 15/20% 是否接执行仍待拍板。别碰：`signalEvalAll` 判定/阈值/三态；`data/*.json`；不要把这套只读卡改成买入冻结；不要把 801862/OMX 历史反例当当前持仓判定；不要把「2 只跌超 97%」写成 3 只全跌超 97%。

### 2026-11-27 · v1145 P2-9 单只 20% 买入冻结（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1144→v1145，tag `fw2_v1145_p2_gate_exec`；GitHub `caifu/index.html` 5,476,431 B / SHA256 `59F7EF20296CD5BBB22E51FD9377A5A030F077304D8AFD3E7682E57F0FE41D8F` / 纯 LF。①按用户「按照你建议继续」，只把最大非现金持仓且单只 >20% 的买入类信号冻结：T7 回撤补仓 / W2 回撤买入 / S2 回撤买入 / T8 估值加仓 / T13 网格跟踪（网格买入）/ R3 网格买 / V11 狙击；卖出/拦截/观察与其他标的不冻；压力 20pp、实际回撤仍只读。②新增 `p2BuyBlockOf(d,code)`，并把 `p2GateData` / `p2BuyBlockOf` 挂到已有 `window.SIGNALS_CFG`，解决跨 IIFE 词法不可见、`try/catch` 吞成静默 false 的问题；信号页整页缓存 `_P2GD`。③ T3 估值止盈 / T8 估值加仓 合并行仅 `vp <= valLow` 认买，高位 T3 估值止盈不误冻。④执行列 disabled「开始」+ 下方「买入冻结」+ `.sig-cap-freeze` 徽标；卡片标题「组合风险闸门 · 单只生效」、徽标「单只 20% 已生效 · 其余只读」、压力/回撤副行标「只读」。⑤`.hold-p2 .hr-cell .s` 改换行，修 538 视口「账户 26.10%」被截断。同步 README 三节/frontmatter、`docs/FRONTEND.md` §10.39、`docs/PITFALLS.md` P-v1145 三条、`docs/P2_STRESS_TEST_2026-11-26.md`。
- **未验证的假设**：①真实数据 012920 当前无行动档买入行（T7 回撤补仓为接近、T1 阶梯止盈同触互斥），线上日常可能看不到冻结按钮；验收是用临时测试参数强制 T7 回撤补仓进入行动档，刷新即还原。②T8 估值加仓 合并行已复核闭环：默认三态 T3 估值止盈=观察、T8 估值加仓=关，合并行按「任一未关即显示、其余降观察」处理，所以默认显示「观察」、P2 的 T8 估值加仓 分支默认不可见，不是 `actConflictMap` 降档；临时覆盖三态并强制 `valLow=100` 后，可见 disabled「开始」+「买入冻结」+ 徽标，反向设 `valLow=30/valHigh=50` 让 T3 估值止盈 触发时按钮恢复可点、无冻结。截图 `D:\Temp\v1145_t8_left.png` / `v1145_t8_right.png` / `v1145_t8_exec.png`。③`push_gh_v39.py` 首次全量 gate 卡在 `verify_acc_nav.py` 十分钟无输出，已停止并以 `SKIP_GATE=1` 发布；`verify_sync --gh-only` 首项字节一致、标记串扫描无 FAIL，但 `watchlist_check` 子进程触发 `WinError 4551 应用程序控制策略已阻止此文件` 崩溃，未拿到完整结论；字节一致不受影响。④3 条 ledger WARN（020097/000834/023422 等缺画像/现金流/理杏仁）与 v1144 相同，无 FAIL。⑤未改任何 `data/*.json`、`signalEvalAll`、三态、交易状态。
- **下一步 + 别碰**：下一步＝①线上 `?view=signal&t=v1145live1&final=1` 强刷验收 v1145、P2 卡单只生效、012920 买入行置灰「开始」+「买入冻结」；②拍板压力 20pp 是否接冻结、实际回撤 15/20% 是否只提示；③P2-11 终止风险闸门（801862/OMX）、P2-12 样本外跟踪 ≥1 年；④3 个 refreshFailed 与 8 个超 7 天手工数据另案。别碰：`signalEvalAll` 判定/阈值/三态；不要把压力/回撤接成执行；不要冻结卖出/拦截/观察；不要把 T3 估值止盈 的高位止盈当 T8 估值加仓 买入冻；不要只改注释不改 `window.SIGNALS_CFG` 挂载；不要把 `opened`/`disabled` 说成成交或已卖。

### 2026-11-27 · v1147 P2-11 终止风险接执行（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1146→v1147，tag `fw2_v1147_term_gate_exec`；GitHub `caifu/index.html` 5,498,191 B / SHA256 `8FA71AC5384E9BA897B0A2920C9965F6D5D10D525BAC1BB9404B924A56496130` / 纯 LF，master `37f8e03b04f3`。①新增 `TERM_GATE_CFG` / `_TG` / `_tgRet3` / `_tgBenchSeries` / `_tgTermSample` / `_tgRiskOfHolding` / `_tgBuild` / `termGateReady` / `termBuyBlockOf` / `termRiskOf`，挂到已有 `window.SIGNALS_CFG`，不新增顶层键。②硬命中：终止样本同名/同码、净值断档 >45 天、`sgzt` 终止/清盘/清算、规模 <0.5 亿；软命中：画像 `r3y` 落后近似基准 ≥30pp、前十集中度 ≥70% 且落后 ≥20pp、`sgzt=暂停申购`；数据不足只记录不冻结。③T7 回撤补仓 / T13 网格跟踪（网格买入）/ T12 距历史低点 / T8 估值加仓 过 `termBuyBlockOf`；T12 只提示；执行列 `(_termblk || _p2blk || _blk)`，冻结显示「终止风险冻结」，按钮 disabled，行动方案加 `.sig-term-freeze`；终止风险优先于 P2-9 文案。④卡片改「终止风险闸门 · 买入门禁」，徽标「已接执行 · 0 只冻结 / N 只冻结」；三格与脚注改写。⑤基金 3 年收益改读画像 `r3y`，修掉 160422 份额折算造成的 −33.3% 假跌。同步 README 三节/frontmatter、`docs/FRONTEND.md` §10.41、`docs/PITFALLS.md` P-v1147、`docs/P2_STRESS_TEST_2026-11-26.md`。
- **未验证的假设**：①当前 24 只非现金持仓 0 冻结、3 年可算 17 / 数据不足 7；数据不足 7 只（022438 / 022676 / 023917 / 020712 / 019737 / 019736 / 023422）均因画像缺 `r3y`，未补画像、未伪造收益。②当前所有 T13 行动买入行已被 T4 硬止损或 P2-9 012920 集中度先挡住，真实数据没有「原本可点、被终止风险新冻结」的行；UI 冻结只用临时覆盖验证，不能声称线上日常出现冻结按钮。③V1 波动赶底 不在当前持仓信号表、深跌买入在研究页，二者未接门禁；卡内「深跌买入（研究页）」是范围说明。④软命中当前也直接冻结；是否只硬命中冻结、软命中只提示，未拍板。⑤P2-9 与 P2-11 同时命中时当前只显示终止风险原因，是否同屏两条原因未拍板。⑥宽屏 1280 真实截图未取得（`bu.cdp` 报 `Session with given id not found`），只做 538 真实截图与几何核验。⑦`termGateReady` 直开信号页最多等 12 秒，两个序列都未就绪时 `asOf` 为空、只跳过存续性，弱检查仍用画像 `r3y`。
- **下一步 + 别碰**：线上 `?view=holdings&t=v1147live1&final=1` 强刷验收徽标 v1147、卡三格 3 只 / 5 类 / 24 只 0 冻结 / 17 可算 7 不足；`?view=signal&t=v1147live2&final=1` 主世界核对 `ready:true,total:24,frozen:0,three:17,short:7,asOf:"2026-11-25"`。下一步拍板软命中是否冻结、V1/深跌买入研究页是否接门禁、P2-9/P2-11 同屏原因；再排 P2-12 样本外跟踪 ≥1 年。别碰：`signalEvalAll` 判定/阈值/三态；`data/*.json`；不要用 `__NAV_SERIES__` 单位净值反推基金 3 年收益；不要把「数据不足」说成通过；不要把冻结买入说成已卖/已成交。

### 2026-11-27 · v1148 P2-11 三边界收口（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1147→v1148，tags `fw2_v1148_term_soft_prompt` / `fw2_v1148_term_double_reason` / `fw2_v1148_term_badge_block`；GitHub `caifu/index.html` 5,506,882 B / SHA256 `191860149D08D8D4AA35B8FB2A5DD4C51DF5D2892105A571223BE9C91CB4CEC9` / 纯 LF，master `6dba068c10d6`。①V1 波动赶底 接信号页门禁（`_termApplies` 加 `^V1 `，`termRiskOf` 对未持仓按画像+净值补算）；深跌买入研究页加 `termGateOfIndex` 与第 11 列「终止风险门禁」，表头「冻结 N 只 · 可买 M 只」，硬命中行浅红底并从可买只数扣除。②`gate=hard`、`frozenList` 只硬命中、`termBuyBlockOf` 仅 hard 返回冻结；软命中只显示琥珀 `.sig-cap-warn`「终止风险提示 · 只提示不冻结」，按钮仍可点。③双闸门 `_waitTxt` 拼两条、`_waitLbl`「买入冻结 · 2 条闸门」、行动方案并列两颗红徽标；硬命中 `actPlan` 统一「【不动】买入冻结 · 不买入（原因）」。④卡片改「已接执行 · N 冻结 · N 提示」「6 类」，改正 v1147 把规模 <0.5 亿误列硬命中。⑤`verify_sync.py` 旧标记 `const actPlan` 同步为 `let actPlan`（v1148 需重新赋值），并加 v1148 标记。同步 README 三节/frontmatter、`docs/FRONTEND.md` §10.42、`docs/PITFALLS.md` P-v1148、`docs/P2_STRESS_TEST_2026-11-26.md`。
- **未验证的假设**：①V1 三态当前为「关」，默认信号页 0 条 V1 行；门禁路径是用临时覆盖 `logicSigMark` 的合成行验证，未把 V1 默认改成开。②双闸门 012920 与 V1 硬/软均为主世界合成行，未改数据/未写状态；真实 24 只持仓仍 0 硬 / 0 软，线上日常看不到冻结/提示。③深跌页 `loading/na` 分支未做真实断网/缺文件注入，只按代码路径核对。④线上首屏 60–90 秒未在弱网复测；宽屏 1280 真实截图未取得，仍以 538 视口为准。⑤3 条 ledger WARN、2 条 FUND_LX/meta WARN 与 v1145/v1146/v1147 相同，无 FAIL。
- **下一步 + 别碰**：线上 `?view=holdings&t=v1148live1&final=1` 验终止卡「0 冻结 · 0 提示」「6 类」；`?view=signal&t=v1148live2&final=1` 验徽标与 58 行（V1 0 行）；策略执行 → 深跌买入验第 11 列「冻结 0 · 可买 4」。下一步＝①拍板压力 20pp / 实际回撤 15–20% 是否接执行；②P2-12 样本外跟踪 ≥1 年；③若要日常看到 V1 行，把 V1 三态设为观察/生效。别碰：`signalEvalAll` 判定/阈值/三态；`data/*.json`；不要把软命中接回冻结；不要用 `__NAV_SERIES__` 单位净值反推 3 年收益；不要把「数据不足」说成通过；不要把冻结买入说成已卖/已成交。
### 2026-11-27 · v1153 T2b 条件化峰值回撤止盈 + T17 单只超配削峰（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1152→v1153，tag `fw2_v1153_t2b_t17`；GitHub `caifu/index.html` 5,544,982 B / SHA256 `15C6D986BD3535DAE367F9B095568DA0B738BDC32BE2B1B357B3F0E201C0947C` / 纯 LF，master `220ab8236080`；同发 `caifu/data/data-mgmt.json`（`logic_state` 源描述 59→61）。①按 012920 复盘结论新增 **T2b 条件化峰值回撤止盈**（峰涨 ≥50% 且单只决策权重 ≤20% 时启用，自峰回撤 10% 卖半、15% 再减半、破 MA200 清剩余）与 **T17 单只超配削峰**（超配 9.72pp / 29.72%，卖约 ¥1,753 / 589.41 份降回 20%，只出建议不自动卖）。②`SIGNALS_CFG` 增 `tpPeakArm2/tpPeakDD2/tpPeakDD2b/singleCap`；`SIGNAL_REGISTRY`、`signalEvalAll`、`_SELL`、`ACT_PRIO`、`ACT_SLA`、`LOGIC_EFF/MEAN/WHERE`、`LOGIC_LAYERS`、`SIG_MECH` 全部补条目；全站计数 59→61。③修 `LOGIC_SIG_RX` 为 `T\d+b?`（否则 T2b 被截成 T2、被 T2 关态连带隐藏）；加 `LOGIC_DEFAULT_ON={T2b:1,T17:1}` 避免新规则落「观察」。④同步 README 三节/frontmatter、`docs/FRONTEND.md` §10.46、`docs/PITFALLS.md` P-v1153。
- **未验证的假设**：①T2b 的 50%/10%/15% 与 T1/T2 反事实（T2-only 约 +45.8%、T1+T2 约 +30.7%）是单只近似，忽略税费与同日互斥，**不是组合级回测结论**。②T17 用决策权重 29.72% 作分母；账户总资产 26.10%（约 ¥1,252）只同屏对照，两者口径尚未拍板。③T2b 在 012920 上因超配只出 `near` 并提示先 T17；削峰后下一刷新才会转 `act`，该先后顺序未获你确认。④`check_globals` 有 13 个窗口读取次数变化（SIGNALS_CFG 60→93 等），新增/消失均为 0，属新增引用不是新全局键。⑤线上只做了 raw 字节与关键词核验（`HAS_V1153 / HAS_T2B / HAS_T17 / HAS_61` 全 True），未在线上真实点击逐行；真渲染证据来自本地 538 截图，线上文件与本地逐字节一致。
- **下一步 + 别碰**：下一步＝①线上 `?view=signal&t=v1153live1&final=1` 与 `?view=tg&t=v1153live2&final=1` 验收两行与 61 条；②拍板削峰分母与「先 T17 后 T2b」顺序；③按原顺序做第 2 项策略工厂 v1（先波动率目标 + 趋势跟踪）、第 3 项标的池统一为「发现层」、第 4 项网格独立化。别碰：`signalEvalAll` 既有 T/W/S 判定/阈值/三态；不要全局默认打开 T2；T17 不自动卖、不写交易状态；不要用账户 P&L 近似替代 A+ 回撤口径；不要手改 `data/*.json`；改任一侧 DMCONFIG `src` 必须同步另一侧，否则 `_audit_dm_v845` 会以 `driftKeys` 拒绝发布。
### 2026-11-27 · v1154 策略工厂 v1：波动率目标 / 趋势跟踪（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1153→v1154，tag `fw2_v1154_strategy_factory`；GitHub `caifu/index.html` 5,567,607 B / SHA256 `551C6A4E5AA84EB518744DEB2B47BEF3C723F18887A2CD7BD3E14BFC57E15AB5` / 纯 LF，master `7f6ef64f0b8a`。策略执行新增第 8 个子页签「策略工厂」（`data-st="sf"` / `#stp-sf`），v1 落两套：**波动率目标**（目标年化波动 15%/窗口 20 日，按已实现波动率缩放仓位，不加杠杆）与**趋势跟踪**（50/200 双均线只做多）；复用 `data/v11-bt-data.json` 15 只 ETF 前复权日线，`t−1` 信号、`t` 收盘调仓，单边费 0.05%、现金 2.25%；输出 8 项 KPI + 净值曲线 + 买入持有对比 + 结论。默认 510300 2016-01-04→2026-11-25：波动率目标 ¥69,511/+39.02%/MDD −40.89%/均仓 81.1%；趋势跟踪 ¥85,031/+70.06%/MDD −27.12%/12 次调仓；买入持有 +43.20%/MDD −44.75%。同步 README 三节/frontmatter、`docs/FRONTEND.md` §10.47、`docs/PITFALLS.md` P-v1154；`_audit_plan_merge_v895` 的 A01 由 7 tab 扩为 8 tab 并新增 A01f。
- **未验证的假设**：①`v11-bt-data.json` 只到 2026-11-25，KPI 是该数据日的快照，数据刷新后会变；②价格序列按源「前复权」口径，未单独核分红调整与跟踪误差；③费率为 0.05%/边、现金 2.25% 是研究假设，不是用户真实 ETF 佣金；④趋势跟踪 12 次调仓是 50/200 在该标的结果，未对全部 15 只做参数扫描；⑤线上只核了 raw 字节与 `v1154`/`stp-sf`/`T2b` 标记，未在线上逐项点击，真渲染证据来自本地 538 截图，线上与本地逐字节一致；⑥`check_globals` 13 项读取次数变化、新增/消失均为 0。
- **下一步 + 别碰**：下一步＝①线上 `?view=strategy&t=v1154live1&final=1` 验收 8 tab、默认两套结果与 15 只下拉；②拍板动量轮动/参数敏感性/结果落盘/组合级回测的先后；③第 3 项标的池统一为「发现层」、第 4 项网格独立化与核心-卫星去重。别碰：`day` 的 base 换算、`t−1` 信号与 `t` 收盘成交、费率/现金假设；不要接实盘/下单、不写交易状态、不新增 window 全局键；不要把工厂塞进 `v11Prep`。

### 2026-11-27 · v1155 发现层统一候选登记（已发布）

- **改了什么**：`edit_work/index.html` 徽标 v1154→v1155，tag `fw2_v1155_discovery_layer`；GitHub `caifu/index.html` 5,575,970 B / SHA256 `98C2D6ED22F0F4636A7E49EEA5D05CB1041D5CBCB141599A526E294152931B9F` / 纯 LF，master `24488b30d3d7`。新增 `edit_work/gen_discovery.py` → `data/discovery-registry.json`（42,844 B），四源 121 只（V11 15/就绪 3、深跌 55/≥70 4、自选 11、筛选 40，跨源同码 0）；投资总纲页尾新增只读「发现层」卡（5 列、前 12 条、chips 六格、两个跳转按钮），fetch 后只回填 `#tgDiscBody`。同发 `caifu/data/data-mgmt.json`（26,930 B）与新增 JSON；`push_gh_v39.py` / `docs/data-ledger.json` / 两端 DMCONFIG 各补一行（frontN=48/genN=48/driftKeys=0）。同步 README 三节/frontmatter、`docs/FRONTEND.md` §10.48、`docs/PITFALLS.md` P-v1155。
- **未验证的假设**：①发现层只做四源登记，持仓与策略工厂候选是否纳入未拍板；②当前是手工轨，V11/深跌日更后不会自动重跑，可能滞后 1 个数据日；③跨源同码 0 是按当前四源代码集合实测，未来加源可能变化；④线上只核了卡内文本与 `/caifu/data/discovery-registry.json` 可读，未逐条点击 121 行（页面只展示前 12 条）；⑤`meta.asOf` 取四源最大数据日（2026-11-26），深跌实际只到 11-24，卡头写「最新数据日」不写「全部同一天」。
- **下一步 + 别碰**：下一步＝①线上 `?view=tg&t=v1155live1&final=1` 验收 chips/前 12 条/两个跳转；②拍板是否纳入持仓与策略工厂、是否进 `refresh_all.py` 自动链、条目是否预填预算；③按原顺序做第 4 项「网格独立化、核心-卫星不重复」。别碰：发现层不接预算/不写交易状态；不登记 <30% 回撤；计数读 `meta.counts`；`index-dd.end` 必须格式化；不要把 `gen_discovery.py` 的 `load()` 改回只查 `data/`；改 DMCONFIG 一侧必须同步另一侧。
