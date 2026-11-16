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

## 待接手

### 2026-11-16 · v941 破线动作改「冻结买入」（退役清仓，用户拍板 A）· **已发布 commit `80fa8b77d9b7`**
- 改了什么：`edit_work/index.html`（徽标 v941，4,584,530 B，tag `fw2_v941c_bk_freeze`）——①`btCfg()` 默认对象尾部 `bkExitAct: 'freeze'` + 归一化（非 `'exit'` 一律 `'freeze'`）；②`_SG` 透传 `bkExitAct`；③`P.pos` 加 `bkFrozen: false`；④判定期分叉：破线达标后 `if (_SG.bkExitAct === 'exit') { pp.bkPend = 'exit'; return; }` 走旧清仓路径，否则 `pp.bkFrozen = true`（**不卖、不清 `sigOff`**）；⑤紧随的解冻块 `if (_below) pp.bkRst = 0; else pp.bkRst++; if (pp.bkRst >= 3) { pp.bkFrozen = false; pp.bkRst = 0; }`，**不 return**（保证减半档继续工作）；⑥定投 `_sigMute` 加 `pp.bkFrozen`、网格买入条件加 `!pp.bkFrozen`；⑦`go()` 收参 `c.bkExitAct`；⑧抽屉加 `sel('bkExitAct','破线动作',[freeze / exit])`，「清仓判据」→「破线阈值」、「本次回测不清仓」→「本次回测关闭破线动作」、勾选标题改「连 2 日破 MA200 冻结买入 · 重站连 3 日解冻」；⑨结论条 / 运行条 / 刹车触发明细表头与脚注 / 明细表 hint / 刹车卡页脚 / 长说明② / 灰字全部按 act 分叉（freeze 不再显示「N 笔清仓」「买回间隔」）。
- 发布与线上核验（**已完成**）：commit `80fa8b77d9b7`（只含 `caifu/index.html`）；raw 回读 **BYTE_MATCH True**（4,584,530 B、sha256 `9c748b16e853565e`）；12/12 锚点命中；线上 `caifu/` 真渲染 freeze 口径 **14.07/1.81/34.40 + 4 笔减半 / 0 清仓**，与本地逐位一致。
- 新增资产：`D:\Temp\v941c_ab.json`（freeze vs exit × 两区间）、`v941c_drip.json`（定投口径 4 组）；截图 `D:\Temp\v941c_drawer2.png`、`v941c_conclbar.png`；备份 `D:\Temp\index_v941_pre_pub.html`（4,584,530 B）；策略文档 `策略大脑_v2.0_刹车与分位规则_待确认.md` §2 / §3 表头 / §4 整节 / §6 步 6 / §8 已同步为「冻结买入」口径。
- 未验证的假设：①**已实证**——`bkExitAct='exit'` 短 13.85/1.55/39.63（10 减半/32 清仓）、长 5.39/0.52/36.44（9/74）**逐位等于 v940 线上基准**（零回归）；`freeze` 短 **14.07%/1.81/预算 34.40%（maxDD −6.88、水下 97、4 减半/0 清仓）**、长 **5.18%/0.56/31.85%（maxDD −6.37、水下 830、5 减半）**。②**推断（待核实）**——一次性口径下 `freeze` 与 v941「清仓整档关」组逐位等价（已建满仓 + gridExt 关无网格可拦，冻结没有可拦的买入），故 A 的实盘价值只在定投/网格场景；drip 对照仅作方向（短 10.19%/1.00/−8.60 vs 3.88%/0.26/−8.86；长 4.24%/0.20/−13.22 vs **−3.45%/−0.13/−39.17**），未逐笔核对。③**未做**——引擎未输出「冻结次数 / 共冻结多少天」，刹车触发明细在 freeze 口径下只列减半，破线冻结在页面上**没有留痕计数**。
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
