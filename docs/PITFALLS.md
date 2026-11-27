# 踩坑台账（PITFALLS）

> 按**症状**索引，不按时间。每条给「怎么证伪 → 根因 → 修法 → tag」。
> 新增一条的判断标准：**下次遇到同样症状，能靠这条少走 30 分钟**。
> 症状优先写页面上/日志里看到的那句话，别写成抽象结论。

## P1 页面「明明是空的/旧的」，但数据文件明明更新了

- 症状：JSON 的 `updatedAt` 是今天，页面卡片仍空 / 仍是旧值。
- 证伪：`Edit` 前端 `mbGet()` 读的是 `data/meta-bundle.json`（首屏），bundle 没重打就是旧快照。
- 根因：bundle 是「四合一静态包」，不是实时读取；链里没有任何步骤强制重打它（v787b 之前是纯手工步骤）。
- 修法：跑 `_make_bundle.py`；`refresh_all.py` 已在 `SERIAL_AFTER` 末位挂组（`fw2_v787b_bundle_sched`），v881 起 `--only macro` 也会自动追加 bundle 组（`fw2_v881_bundle_in_chain`）。
- tag：`fw2_v787b_bundle_sched`、`fw2_v881_bundle_in_chain`

## P2 同一份文件里，新加的键第二天就没了

- 症状：今天接的卡有数，明天刷新后空白，且日志全绿。
- 证伪：看 `macro-data.json` 顶层键是否还在；不在=被全量重写者抹掉。
- 根因：`gen_macro_snap.py` 用 `d = {...}` 整体重建 `macro-data.json`，任何新子键写入者若没挂进 macro 组、或排在它之前，都会被抹（v472 ushf/cbRates、v812b globalCli、v813b 守卫只判「今天抓过没」不判「数据还在」）。
- 修法：①新键写入者必须挂进 `GROUPS['macro']` 且排在 `gen_macro_snap.py` **之后**；②组尾 `_rebuild_macro_snap.py` 同步 index.html 内嵌快照；③守卫必须能自愈（检测到键被抹则忽略当日哨兵重抓）。
- tag：`fw2_v472`、`fw2_v812b`、`fw2_v813b`

## P3 派生文件停在上一交易日，但源头两路都是对的（共享缓存竞态）

- 症状：`verify_dual_source` 报「发布文件不一致 1」，而同一行又写「两源一致」。
- 证伪：比对 mtime 序列——`fund-monthly.json` < `_hist_cache/*.json` < `fund-daily.json`，说明月度按旧缓存算完、日频后又把当天净值写进同一缓存。
- 根因：`refresh_all.py` 里 fund-monthly 与 fund-daily 是并行组、共用 `data/_hist_cache`；月度几秒算完，日频 17 分钟后才结束，链里没有后置重算。
- 修法：串行阶段按 mtime 判定「缓存比产物新则复算一次」（`fw2_v881b_monthly_cache_race`）。实例：001194 由 4.084（11-06）→ 4.182（11-09）。
- tag：`fw2_v881b_monthly_cache_race`

## P4 闸门红，但数据其实是对的（校验器假红）

- 症状 A：某月永远 FAIL，明细里月份数是 0。
  - 根因：verifier 用 Wind 的 `YYYY-MM` 整串去匹配产物里的 `YYYY-MM-01` → 命中 0 → `n<3` 恒 FAIL。
  - 修法：`cmp_month()` 统一月份键格式（`fw2_v881_verifier_monthkey`）。
- 症状 B：`rc=124 [TIMEOUT]` 被记成 FAIL。
  - 根因：`gate.py run()` 默认 300s，两个联网逐只校验器实测 480s/473s。
  - 修法：`TIMEOUT_BY_SCRIPT` 给 900s（`fw2_v881b_gate_timeout`）。
- 共同危害：假红会训练出「反正会红，加 SKIP_GATE」的习惯，真校验一起作废。**先修机制，再谈数据。**
- tag：`fw2_v881_verifier_monthkey`、`fw2_v881b_gate_timeout`

## P5 某个历史数据从无生产者，重跑链也不会自愈

- 症状：某序列 `points` 全空、`cur` 全 null；脚本里 `try: json.load(...) except: 留空数组`。
- 证伪：全仓搜该文件名——若只有「读」没有「写」，即结构性缺口（v881 的 `amt_month_raw.json`）。
- 根因：脚本写好但从未有生产者；异常被吞，表现为「静默空数组」而不是报错。
- 修法：补生产者脚本 `_rebuild_amt_raw.py`（三道对拍：三所行数/交集交易日/两锚点），并把它挂进增量维护（`refresh_amt30.py` 的 (c2)/(d2)）。
- tag：`fw2_v881_amt_month_producer`

## P6 口径文案与实际计算窗口不一致

- 症状：卡面写「近 120 个月」，出来的分位却像全历史。
- 证伪：用同一条算式反证三个窗口（全序列 366 月 69.9% / 近 120 月 23.3% / 近 60 月 0.0%），看哪个与文案匹配。
- 根因：文案先写、计算后改，两者没同源。
- 修法：计算窗口以文案为准并写进代码注释（`amt_pct120`）；改窗口必须同时改文案。
- tag：`fw2_v881_amt_pct120`

## P7 数据日期不同源（卡片日期 vs 曲线末点）

- 症状：卡头写 11-07，曲线末点却是 11-09。
- 根因：`asOf` 由上层覆盖，但曲线取序列末点；两者没绑定。
- 修法：`asOf()` 统一取序列末点或显式覆盖，前端所有「数据截至」都走同一函数。
- tag：`fw2_v878` 系列

## P8 换版本后线上仍是旧的（缓存/SW 层）

- 症状：本地改了、raw 也对，浏览器打开还是旧页。
- 根因：`sw.js` 长期不在发布清单（v695）→ 浏览器无从感知新版本；或 Pages CDN 滞后。
- 修法：`sw.js` 进 FILES 必发；验收加 `?v=<版本>`；必要时强刷。
- tag：`fw2_v695_sw`

## P9 台账/持仓「三模块数字不一样」

- 症状：我的持仓 / 资金平衡 / 策略执行 三处市值差几十到上千。
- 根因：某入口绕过了 `holdRows()`，改回「流水份额 × t.nav」旧口径（v637 曾差 1114.09）。
- 证伪：`check_hold_consistency.py`（内嵌 seed 与 holdings-data 逐字段 / 5 个入口必须经 holdRows / Σmv 与账户 total 闭合 ±0.5）。
- 修法：所有市值一律 `shares × nav`，`holdCore` 唯一真源；该检查已挂发布前硬卡（`fw2_v696_hold_core`）。
- tag：`fw2_v696_hold_core`

## P10 某个 AI「明明做过」的事，换 AI 后当成新问题重做一遍

- 症状：新接手的 AI 说「这个数据没来源 / 需要重新写个取数脚本」，而工程里已有生产者与口径；或反过来，它自信地报出一串早已过期的数量/日期。
- 根因：**工具自带的记忆不跨工具**。豆包工作的经验库在 `…\agent_mode\workspace\experience\`、会话记忆在 `…\workspace\.sessions\`；Trae / 千问办公各有自己的与工程无关的存储。这些都不在项目目录里，换工具＝全部消失。留在项目目录里能被继承的，只有 `README.md`（断点+路由）、`docs/` 四件套（操作知识）、`AGENTS.md`+垫片（规则）、以及代码本身。
- 证伪：让新 AI 说出「这条数据由哪个脚本生产、进哪个组」，说不出来就是没接上；再说「我查一下」然后去 grep 全仓——说明它没读台账。
- 修法：①凡「这次学到的」必须落进 `docs/`（口径进 DATA_LEDGER、命令进 PIPELINES、坑进本文、状态进 INBOX），**不许只留在某个 AI 的对话或经验库里**；②新 AI 开工先跑 `handoff_check.py`，用输出反驳自己的假设；③README 只放断点/路由，数量与日期一律不进 README（它们会腐烂，见 P11 口径类问题的同源教训）。
- tag：`fw2_v881c_handoff`

## P13 按「读 README 顶部的关键入口表」开工，从 L1 读却只看到版本史

- 症状：`AGENTS.md` L17 / `docs/AGENT_PROMPT.md` L23 / README「下一步」都写「读 README.md **顶部**的『关键入口』表」，照做从 L1 开始读，先撞进几百行倒序 changelog，找不到表；或误把整份 README 当版本史读完（正好违反同一条规则）。
- 证伪：`Grep '^## 关键入口' README.md` → 命中 **L678**（文件共 836 行 / 438,767 字符，`handoff_check.py` 第 1 段独立复核）；本会话内该节还从 L672 漂到 L678（并行 AI 在编辑），**行号不是稳定锚点**。
- 根因：v881c 把「关键入口」节追加在 README 中后段，前面是 frontmatter + 倒序 changelog，三处规则措辞却仍沿用「顶部」。用户口述交接话逐字来自 `AGENT_PROMPT.md` L23，不是个人笔误。
- 修法：①按标题 Grep 定位后跳读该节约 6 行路由表，**不要从 L1 顺序读**；②根治需把 `AGENTS.md` L17 / `AGENT_PROMPT.md` L23 / README「下一步」三处「顶部」统一改成「按标题定位」，改前确认没有并行 AI 正在编辑这三份文件（本轮未改，登记不擅动）；③`AGENTS.md` 是三步（FRONTEND 作第 2 步子项）、`AGENT_PROMPT.md` 是四步，编号不同但内容一致，别当成规则冲突。
- tag：`fw2_handoff_selfcheck_20261110`

## P14 PowerShell here-string 经管道喂给 python 的中文变成 `??`

- 症状：`@'...'@ | & python -` 里写了中文路径，报 `OSError: [Errno 22] Invalid argument: 'D:\workbuddy??\????\edit_work\index.html'`；同一段源码里 `startswith('## 关键入口')` 恒返回 `[]`，但 Grep 工具能命中该行。
- 证伪：把源码里的中文全部换成相对路径后，同一命令 `AUX_RC=0` 且数值正确 → 不是路径不存在、也不是 python 版本问题，是**源码中的中文字符在传输环节被替换**。
- 根因：PowerShell 5.1 的 here-string 经管道传给原生进程时使用系统 ANSI 编码（推断，未做字节级取证）。`[Console]::OutputEncoding = UTF8` + `$env:PYTHONIOENCODING='utf-8'` 只修输出，不修输入源码。
- 修法：①python 源码内**不出现中文**——先 `Set-Location` 到项目根，路径一律用相对路径；②中文匹配改用 `'\uXXXX'` 转义或直接交给 Grep 工具；③确需中文路径时写成独立 `.py` 文件再执行，不要走 stdin 管道。
- tag：`fw2_handoff_selfcheck_20261110`
- 编号说明：本地 `docs/PITFALLS.md` 仅有 P1–P10，而 P10 L85 引用了「P11 口径类问题」（本地无该条，是否曾存在于云端备份**未核实**）。本轮未踩到口径类坑、不编造，故 P11/P12 留白，新坑顺延 P13 起。

## P15 只看 `refresh_holdings_ttskill.py` 就断言「ttskill 只有只读能力」

- 症状：被问「能不能从出方案一路做到下单」，grep 工程内 ttskill 调用点只看到 `ACCOUNT_HOLDING` / `TRADE_QUERY` 的 `trade_list`/`trade_detail`，就下结论「没有下单接口、做不到」；或反过来，看到 skill 名 `FUND_TRADE_ENTRY` 就以为可以直调 `commit_order` 替用户提交。
- 证伪：`ttskill skill list --json` → 本机 39 个 enabled skill，含 `FUND_TRADE_ENTRY` 1.0.1（带 `scripts/open_h5.mjs`）；读其 `SKILL.md`（`%LOCALAPPDATA%\TTFund\ttfund-skills\skills\FUND_TRADE_ENTRY\1.0.1\SKILL.md`）L9/L51/L53/L104/L152/L154 确认设计为「Agent 打开已鉴权 H5 + 预填代码/金额，用户在页面完成银行卡、协议、密码与最终确认」，`commit_order` 明令 Agent 不直接调用；`opened=true` 也只代表页面打开，不代表成交。
- 根因：工程只用 ttskill 的**查询类** skill 做数据刷新；CLI 能力包是独立安装的，**工程调用点 ≠ CLI 全部能力**。把「本工程没用到」当成「工具不支持」，是以偏概全；把「工具支持」当成「规则允许」，是另一半错误。
- 修法：①判断外部工具能力先列能力清单（`skill list --json`）再读对应 `SKILL.md`，不要只 grep 本仓调用点；②「能不能做」分三层答：**工程现状 / 工具能力 / 规则是否允许**，三者结论可以不同；③`ttskill status --json` 的 `auth` 含 token/Cookie，只取 `has_token`、`is_expired` 等布尔值，禁止打印凭证串（该 SKILL.md L27）；④`AGENTS.md` L10「不连接真实券商 / 不自动下单 / 不保存真实凭证」未经用户明确授权不得改，也不得擅自把生产交易入口接进工作台；⑤多基金 `items` 返回 `status=batch` 不是「全部打开」，验收必须逐项断言 `results[].opened`。
- tag：`fw2_trade_entry_boundary_20261110`

## P16 `run-script` 退出码 0 却一个页面都没打开，结果还藏在 `stdout` 字段里

- 症状：调 `ttskill run-script FUND_TRADE_ENTRY open_h5 --input ...` 后进程 `rc=0`，就宣称「交易页已打开」；或者直接把 CLI 打印的顶层 JSON 当批量结果解析，取不到 `results` 就报「无输出」。
- 证伪：用 `{"env":"prod","intent":"purchase","items":[]}` 做安全探测（空数组在 `openPurchaseBatch` L583 就抛错，**不打开页面、不读凭证**），CLI 返回的是 `{status:"failed", exit_code:1, stdout:"", stderr:"多 基金入口仅支持..."}` —— 脚本自身的 JSON 在**顶层 `stdout` 字段**，不是顶层对象。再读 `open_h5.mjs` L634：`if (!result.opened && !["diagnostic","batch"].includes(result.status)) process.exitCode = 1`，**批量状态被豁免**，所以 7 项全失败时进程照样 0。
- 根因：①CLI 对 `run-script` 做了一层包装（外层 `status/exit_code/stdout/stderr`），脚本 `console.log(JSON.stringify(result))` 只是内层字符串；②官方 SKILL.md L142 早就写了「CLI 退出码为 0 不等于页面打开成功」，L104 写了「`status=batch` 仅表示已生成汇总，不表示全部打开」——两处都在，但没写进校验器就等于没有。
- 修法：①解析两层：`top = json.loads(cli_stdout)` → `inner = json.loads(top['stdout'])`；②逐项断言 `inner['results'][i]['opened'] is True` 且项数等于清单数，**空 results 必须判 FAIL**（空 PASS 假绿）；③结论只认 `opened_n`，不看 `rc`、不看 `status=batch`、不看 `inner['opened']` 单值；④`_audit_trade_entry_v1.py` 的 C/D 组把这些写成静态硬卡，并配检测器自测正反例。
- tag：`fw2_trade_entry_v1_20261110`

## P17 想「把交易按钮接进工作台页面」，但静态站点调不到本机 CLI

- 症状：用户说「连接天天基金，从出方案到最终投资全做完」，接手的 AI 直接在 `index.html` 里加按钮、写 fetch 去调 `ttskill`，结果线上 404 / 浏览器沙箱拦截；或反过来把它当成「做不到」而整条链放弃。
- 证伪：`push_gh_v39.py` 的 `FILES` 是 `index.html` + `data/*.json`，工作台跑在 `andylauxiaoyang.github.io/investment-workbench/caifu/`；`ttskill.cmd` 只存在于本机 `%LOCALAPPDATA%\TTFund\ttskill-base\bin\`。浏览器里的静态页面没有任何本机进程通道。工程侧 grep 也证实 `index.html` 从未出现 ttskill 调用。
- 根因：把「接交易入口」默认理解成「改前端」，但这条能力属于**本机执行链**，与站点发布链是两条互不相交的链。
- 修法：①本机链落 `edit_work/_trade_entry_v1.py`，**不进发布清单**；②前端最多出「可复制的执行清单」，不放任何能触发交易的控件；③每次写回都注明「本机链 vs 站点链」，避免下一个 AI 把本机脚本误挂进 `refresh_all.py` 或 `push_gh_v39.py`；④`docs/` 与本机脚本按 v881c 约定只存本地，只读远端的 AI 读不到，交接时要显式给路径。
- tag：`fw2_trade_entry_v1_20261110`

## P18 把 `purchase_check_failed` 说成「这只基金买不了」

- 症状：批量打开 7 只、两只返回 `purchase_check_failed`，接手的 AI 直接汇报「场内 ETF 不支持买入 / 该产品暂停申购」，把**预检请求失败**当成**业务结论**。
- 证伪：2026-11-10 实测 511360 / 511260 的 `reason=purchase_check_failed`；`open_h5.mjs` L392 表明它是「预检异常且非登录失效」的兜底 reason，L369 的 `purchase_unavailable` 才是 `EnableSg/EnableRg` 均 false 的业务结论。官方 SKILL.md L59/L131-132 明写「`purchase_check_failed` 不代表产品不存在或暂停申购」。此前按「场内 ETF 类型不符」推断会命中 `purchase_unavailable`，**被实测证伪**。
- 根因：①两个 reason 都导致 `opened=false`，容易被合并成一句「买不了」；②prod 环境不返回 diagnostics（L481 `diagnostic 仅支持测试环境`、L603 仅 `env==='test'` 附带），**没有可归因的数据**，于是用「听起来合理的故事」补空——正是 `AGENTS.md` 规则 6 禁止的那类臆断。
- 修法：①逐项原样输出 `reason`，按官方固定话术翻译，不自行升级结论；②严格区分事实（预检失败）/ 推测（可能与产品类型有关）/ 无法验证（prod 无 diagnostics）；③根因要查证只能走 test 环境 `diagnostic:true`，那是开发联调、不得用于对客流程；④把「部分打开」逐项写进交接条，别只报合计数。
- tag：`fw2_trade_entry_v1_20261110`

## P19 改「一个标的 / 一个目标金额」只改一处，计划集立刻分叉

- 症状：用户说「安全垫里活期宝目标定 5,000，511360 删掉」，接手的 AI 只改资产配置表那一处（或只在 `STRATEGY_SNAP.assets` 里换一条），页面资产配置表看着对了，但「月度定投表 / 首次执行单 / 逐标的执行卡 / 半杠铃磁贴 / 纪律核查提示」里仍显示已删标的，或金额合计对不上；更隐蔽的是 `barbell.funds` 与 `ALLOC_DEF` 计划集不一致，`_audit_cross_module.py` 只给 INFO 不 FAIL。
- 证伪（2026-11-10 实证）：`511360` 在 `index.html` 共 25 处，其中**计划配置**占 10 处：`STRATEGY_SNAP` 一段 9,077 字符的单行 JSON 里就有 3 个对象（`assets` / `plan` / `first`），加 `firstInvest` 合计常量；另有 `ALLOC_DEF`、`roleCodes`、`SIGNALS_CFG.barbell.funds`（一条里 3 个字面量）、`heldBadge` 弹药池、再平衡建仓提示。剩下 15 处是 `FUND_PROFILES_MIRROR` / `FUND_LX_RAW` / URL 映射 / `data/*.json` / 历史注释——**这些不该删**。
- 根因：①这套 5 万/11 只计划是 v120 起**内联在 `index.html` 的手写主源**（无独立生成器、无 `data/*.json` 产物），`docs/DATA_LEDGER.md` 的 34 个数据集里根本没有它，按「查台账找唯一生产者」会扑空；②`FRONTEND.md` L13 把 `STRATEGY_SNAP` 归进「内嵌快照（构建期注入）」，但这条**没有外部源文件**，改它不会被重打覆盖——与 `SEC_DAILY` / `FUND_PROFILES_MIRROR` 不同类；③`monthlyNominal 4169` 不是 `plan.build` 数字项之和（3752），而是「11 只按 target÷12 的名义月投额」（9×417+2×208），**拿 plan 之和去断言它会误判并错改常量**；本次是 5000→5000 等量替换，名义总额不变，`firstInvest 4500→3938` 才是真要跟着减的（首投单 ⑧ 562→0）。
- 修法：①用 `edit_work/_apply_alloc_cash_v882.py` 的清单式精确替换（每条断言 `count==1`，先备份 `index_bak_v881_pre_cash.html`），**禁止全局 `replace_all`**——中文短串会命中画像镜像、注释、changelog；②JSON 单行对象用花括号配平提取（`extract_obj`）而非手写整串，避免序列化差异；③改完做四层自证：JSON 可解析 + `assets=11` + `Σtarget=50,000` + `Σfirst.amount==firstInvest` + 计划段 `511360=0`；静态硬卡全链；CDP 真渲染逐行按表头 x 断言列位（组头行 13 td / 普通行 11 td，重复列必 FAIL）；两态颜色回归；④`barbell.funds` 与 `ALLOC_DEF` 必须同批改，否则半杠铃档位实际权重会漏算现金。
- 附带坑（P14 变体）：PowerShell 5.1 here-string 经管道给 python 时，脚本里的中文字面量会变 `??`，用 `b.count("'000912', '活期宝'")` 检查会返回**假 0**；验收脚本里的中文匹配一律改用列索引 / `chr` / 独立 `.py` 文件，别在 here-string 里写中文。
- tag：`fw2_alloc_cash_v882_20261110`

## P20 双通道对拍不一致时「下沉旧源」，把已披露的新净值丢掉

- 症状：「我的持仓」表净值日期 6 号 / 9 号混杂；用户问「数据源、取数逻辑有问题吗」，并特别提醒 **QDII 要理解时间差**、但**国内 A500 不该只到 6 号**。接手的 AI 很容易走两个极端：把所有 11/06 一律当 bug（误伤 QDII），或一律当「上游披露慢」（放走真 bug）。
- 证伪（2026-11-10 实证，含一次自我纠正）：①`holdings-data.json` `syncedAt=2026-11-09T20:36:17+0800`，24 只 `navDate` 分布 11-05(4)/11-06(14)/11-09(6)；②`data/fund-daily.json`（`meta.asOf=2026-11-09`）里 022438 / 022676 / 023917 / 012761 的序列**末点已是 11-09**，说明东财当时就披露了 11-09 净值，不是上游慢；③实跑 `nav_eastmoney()` / `nav_pingzhong()` 当下（11-10）两通道**都返 11-09 且一致**，一度让我误判为「11-09 20:36 同步太早，事后源站才更新」——**别用事后重放当下接口值去反推历史时点**；④决定性证据是 `_refresh_logs/refresh_holdings_group.log` L7-18 八行 WARN：`022438 east=1.0728 ping=1.0737，保留旧净值` 等，`east` 正是 11-09 新净值、`ping` 正是 11-06 旧净值。
- 根因：`refresh_holdings_ttskill.py` 旧写法 `if 不一致: x = None` → `src = x or y`。把较新的 `nav_eastmoney` 置空后 `or` 回落较旧的 `nav_pingzhong`，写出旧 `nav` / `navDate`；日志「**保留旧净值**」与行为不符（不是保留 `h` 原值，而是**写入** ping 的值，只因它恰好等于旧值才看起来像保留），把事故掩盖了整整一轮。8 只中招：4 只国内指数（022438 / 022676 / 023917 / 012761）停 11-06，4 只 QDII（019173 / 019737 / 019736 / 008971）停 11-05。注意 020712 日经225 QDII 是 11-09、其余 QDII 是 11-06 —— 差异来自各基金公司披露节奏，**不是**「QDII 一律 T+2」。
- **QDII 时差的正解**：判据不是「距今天几天」，而是 **`navDate` 与该 code 的 `fund-daily` 序列末点比较**：相等＝正常时差（序列本身只到 11-06），落后＝镜像没拿到（真 bug）。按自然日设统一阈值必然同时误伤与漏报。
- 修法：①`choose_nav(x, y, fd)` 取 `navDate` 较新通道，要求 `fd_latest_map()`（`data/fund-daily.json` 末点）确认日期与净值；②★这个仲裁是**同口径**（fund-daily 的 `navSource` 同为东财 lsjz，与 `nav_eastmoney` 同源），只判「谁更新」、不判「净值对不对」，**禁止把它当独立第二源**（项目红线），已在代码文档字符串写明；pingzhongdata 追平后自动恢复双源逐值对拍；③仲裁不了返回 `src=None`，调用方 `if src:` 才写盘，**真正**保留原值，不静默下沉；④静态硬卡 `_audit_nav_freshness_v883.py` 分「国内 FAIL / 海外 WARN」并挂 `push_gh_v39.py`，含 8 组日志实证的动态自测与旧写法防回归；⑤页面 `navDateVerdict()` 分层标注（海外 title 解释 T+1~T+2、国内早于 `state._pfAt` 标「·滞后」），别让用户自己猜。
- 附带坑（检测器自身）：①**别把注释/文档字符串里引用旧写法当反例判成回归**——B01 初版用 `'x = None' not in src` 直接假红，改用行锚正则 `^\s*x\s*=\s*None\s*$`；②`src = x or y` 本身合法（`choose_nav` 一致分支、新增基金建档的 else 分支都用它），只卡 `x = None` 那一行 + 主链必须调 `choose_nav`；③探针别写死「4 只滞后标的」清单，日频链补齐后会假红，改用「国内行 navDate < 账户同步日」动态算 expected（v849 审计写死版本号同型）。
- tag：`fw2_v883_nav_stale_20261110`
- **已发布（2026-11-10，线上 v884）**：v883 修复随 v884 发布（v884 = v882 安全垫 + v883 双通道修复 + v884 参照修正）。完整 `refresh_all.py` 后 4 只国内基金 `navDate` 补齐至 11-09，硬卡 `AUDIT=PASS 36/36`；发布前又抓到 v883 参照回归（用 `state._pfAt` 当滞后参照致 8 只国内全误标「·滞后」），已用 v884 `domNavMax` 修正（见 `FRONTEND.md` §7）。

## P21 日频自动化 rrule 会「二次漂移」，改一次 ≠ 永久修好

- 症状：收尾时准备写「等今晚 21:30 自动化自愈」，却没实证调度真源；`automation_update view` 一查发现 `BYHOUR=20`（**实际 20:30**），而 prompt 首句、页面 `verify_sync` 标记串「每晚 21:30 自动」全写 21:30。11-07 刚把同一字段从 20 改回 21 并 `view` 回读过，11-10 又漂回 20。
- 证伪：不能拿 prompt 首句、页面文案、或 11-07 的「已修复」记忆当证据——那些是宣称／历史；唯一真源是 `automation_update view` 返回的 `rrule` + `nextRunAt`。11-07 回读的 `nextRunAt=1794231000000`＝2026-11-09 21:30，只能证明**当时**改对了，不能证明 11-10 仍对。
- 根因：①调度配置在服务端，本地 `index.html` / README / docs 没有任何副本能锚住它 ⇒ 改一次不等于永久修好；②二次漂移的物理成因（时区换算 / 编辑器默认值 / 同步覆盖）本轮未查证，**不编造**。
- 修法：①只改 rrule（`automation_update update` 仅传 id + rrule，其余字段省略保留），**不改 prompt / 页面 / 硬卡文案**——10-13 起 cron `30 21 * * *`、页面 `verify_sync` 标记串都是 21:30，改文案会踩硬卡并制造第三处漂移；②改完必 `view` 回读确认持久化，并把 `nextRunAt` 换算成北京时间（本次 `1794317400000`＝**2026-11-10 21:30 +08:00** / UTC 13:30）；③把「接手／收尾必 `automation_update view`」写进 `PIPELINES.md` P9 约束⑥与 `INBOX.md`，靠流程反复实证兜住，而不是靠一次修改。
- 附带关联（**推测，勿当结论**）：11-09 持仓 `syncedAt=20:36:17` 落在 20:30 档，可能是刷新过早让 pingzhongdata 未追平、放大了双通道不一致窗口；但 v883 bug 的根因是旧 `x = None` 下沉旧源（日志铁证），时间早只是环境诱因的推测，**未取证**。
- tag：`fw2_v883_rrule_drift2_20261110`
- **已复位（2026-11-10）**：收尾实证后已 `automation_update update` 仅传 id+rrule（`BYHOUR=21;BYMINUTE=30`），`view` 回读 `nextRunAt=1794317400000`＝2026-11-10 21:30 +08:00，发布 v884 时调度真源已为 21:30 档。**仍建议每个 AI 接手／收尾都实证一次**（见 P9 约束⑥），因为这不是「改一次永久修好」的字段。

## P22 资产配置表「共桶主题」：子行目标列显 `—` 与小计求和的两层口径

- 症状：把两个主题（如 标普500 + 纳指100）合并成一个「限额预算桶」共用 5,000 时，子行目标金额/占比该显示什么？小计又该显示什么？容易直接把子行目标也写成 5,000（重复计入）或把小计 `tt` 也屏蔽成 `—`（桶目标凭空消失）。
- 证伪（2026-11-10 实测）：`STRATEGY_SNAP.assets['016452'].target=5000` 是桶承载者，017641/096001/019441 不在 SNAP（计划外、target=0）；`thGroups` 按 `theme` 聚合，同 theme ≥2 只自动出小计行，小计 `tt = Σ assetOf(code).target` → 只要 016452 承载 5000、其余子行 target=0，小计目标**自然**=5,000，无需任何特殊处理；子行显示 `—` 只是由 `CAP_ONLY_THEMES` 白名单在 `it.m` 分支把 `tgtDisp` 置 `null`。
- 根因：把「桶目标」和「子行目标」当成同一层——其实桶目标写在 SNAP 单只承载者上、小计靠求和自然得出，子行根本不持有目标值，硬给子行赋 5,000 才是重复计入。
- 修法：①新增 `var CAP_ONLY_THEMES` 白名单，只屏蔽**子行**目标列（`tgtDisp = capOnly ? null : tgt`），**不要**在 `thGroups` 小计 `tt` 的求和处加白名单判断；②主题归并只在 `ALLOC_DEF` 主题字段 + extra 块 `xth` 两处同批，**禁动全局 `code→theme` 映射表**（持仓页/热力图家族聚合依赖它）；③列对齐陷阱见 P9 / v872：首组小计行带 `grpTds` 是 13 列、被合并子明细行是 11 列，CDP 断言用列集合判定（见 `PIPELINES.md` P10）。
- tag：`fw2_v885_us_broad`
- **已发布（2026-11-10，线上 v885）**：用户截图问格式，A/B/C 三方案对比后定 C 变体（限额制）。CDP `ALLOC_US_V885=PASS`：小计 `目标=5,000 占比=10.00% 进度=834 实际=258 滞后=-576`、四只子行目标列 `—`、无独立标普500/纳指100 小计。

## P23 合法行型一变，静态审计锚点必须同步重定目标（v886 同轮三连假红/假锚）

- 症状：v886 删掉基金明细行改指数家族聚合后，三个 alloc 审计立即爆 5+3 个 FAIL——但**渲染本身是对的**。反过来的风险更危险：不跑审计直接发布，锚点失效的审计从此空转（空 PASS 假绿）。
- 三类真实踩法（2026-11-10 实录）：①**把定义当调用**——`offOf(tgt, mv, held)` 在 21057 行是函数**定义**，旧明细行删除后它仍唯一存在，`assert 'offOf(tgt, mv, held)' not in s` 必假红；正确口径=「该串仅出现 1 次（定义）」。②**end marker 多打一个字符**——文件里行尾是 `</tr>';`，end marker 写成 `</tr>');`（多个 `)`）→ `s.find` 一路找到 57 万字符外，td 计数得 229；字符串锚点要逐字符与文件对拍。③**正则贪心跨界**——探针解析「名称+N 只同指数」拼接串：`纳指100`+`11 只同指数`→`纳指10011 只同指数`，`\d+只同指数$` 把名字尾部 `100` 一起吃掉，得 `纳指`；结构化内容必须读 `<b>` 子元素，禁解析 textContent 拼接串。
- 修法：①合法行型/模板变更与审计重锚**同一改动集**内完成，发布前审计必须重新全绿；②阈值型断言（如 `offOf(` 计数 ≥4）在行型减少时同步降（≥3），并在断言名里写明理由（「v886 明细行已删」）；③每条 FAIL 先分「渲染坏了」还是「审计锚点过时」——同读探针+DOM，别急着回滚代码。
- ④**锚点注释带尾注时查找串不能含 ` */`**（v887 实录）：文件里注释是 `/* fw2_v887_active_fund_row：中文说明 */`，审计用 `tds_between('/* fw2_v887_active_fund_row */', ...)` 精确匹配闭合 → `find=-1` 假红；带尾注的锚点查找串要省略闭合符。⑤**GitHub contents API 对 >1MB 文件返回 `content=""`**（encoding=none），`base64.b64decode` 得 0 字节不报错——临时核验脚本以为拿到空文件；权威回读必须走 `git/blobs/{sha}`（push 流水线既有口径），且 0 字节「成功」比报错更危险。
- tag：`fw2_v886_idx_alloc`

## P24 小计/明细同屏的探针断言：按「小计＋紧随明细块」配对，禁止全局恰 1（v888 实录）

- 症状：v888 给「主动权益」加小计行后，探针断言「全局恰 1 个小计行」FAIL（实测 3 个）。渲染本身是对的。
- 根因：**`idxFamily` 兜底家族横跨多档位组**（主动权益散布在 进攻/主题 2 只、另两组各 1 只 + 计划外）——小计是**组内聚合**，跨档位不可加总，每个含该家族的位置各出一个小计是正确设计。探针把「全表唯一」错当不变量。
- 修法：①小计断言改**结构配对**——每个小计行向下收集连续 6 位码明细行成块，对拍「小计 vs 块内明细和」，并断言无孤儿明细（每个明细行恰属一个块）；②**整元显示舍入容差**：各明细独立四舍五入到整元，之和与和的舍入可差 ±1/行（实测 10,997 vs 10,996），容差 = ceil(明细行数/2)，探针注明是显示层噪声非口径错误——若业务要求账面严格配平须改渲染口径（「小计=明细显示值求和」），属数据口径变更须单独拍板；③行名解析别用 textContent 拼接串的贪心正则（P23③ 同源），行型判定用「代码列 6 位码 / gsub 含『只同指数』/『只标的·小计』」三分。
- tag：`fw2_v888_active_subtotal`

## P25 rowspan 计数必须按「渲染行数」不是「items 数」——聚合家族 1 行、展开家族 N 行（v889 实录）

- 症状：v889 删小计行时把 rowspan 公式从 `(fam==='主动权益') ? 1+rows.length : 1` 改成 `rowspan += g.rows.length`（以为"数 items"更简单），CDP 探针 V2 当场 FAIL：组首行 `cols=[2..12,12,12]`——组头 rowspan 比实际渲染行数多 1（底仓/缓冲 5 items 只渲染 4 行：A500指数 2 只→1 行），后续行整体右移两列、末尾 2 格溢出表外（x=1543/1556 > 表头最右 1452，v872 同款）。
- 根因：**`idxGroups[].rows` 是原始 items，指数家族不论几只只渲染 1 行聚合行**——`rows.length` ≠ 渲染行数。正确公式恒为 `(fam==='主动权益') ? rows.length : 1`（主动权益逐只展开数明细、指数家族恒 1）。
- 修法：①rowspan 公式改动时**必须先枚举每种家族的「渲染行数」函数**（聚合=1、展开=N、小计结构=1+N），不能凭"行数=items 数"直觉；②探针 V2 的逐行按表头 x 归位断言再次证明是 row-span 类改动的唯一可靠拦截（本次静态审计全绿、node 语法过，只有 CDP 抓到）；③修正后把公式写进审计 B10 锚点（count==2），防止下次再"简化"。
- tag：`fw2_v889_active_flat`

## P26 配色层「后置覆盖」两处特异性陷阱（v890 实录）

- 症状：新增橙点缀规则若放在 head 的 style 块、或只写普通选择器，会**静默不生效**——页面不报错，只是没变色，静态审计也看不出来。
- 三个真因：① **`#view-smartmoney .sm-sec-hd .bar` 定义在 body 后段（line 19941，(1,2,0)）**，head 里同特异性的规则会被它盖掉 → 配色规则必须放 `</body>` 前最后一个 style 块；② **原 `.btn-primary:hover` 是 (0,2,0)**，只写 `.btn-primary { background:橙 }` (0,1,0) 时鼠标一悬停就翻回琥珀底＋黑字 → 必须把 `.btn-primary` 与 `.btn-primary:hover` 写进**同一条规则**一起覆盖；③ 懒渲染 / 弹窗内元素（`.mcmp-add`、聪明钱小色条）在首屏视图 DOM 里根本不存在 → 首屏 CDP 与静态层都测不到，需**动态注入临时测试节点**读 computed 实证，验完即移除。
- 修法：①新增配色规则统一后置到最后一个 style 块，并逐项 CDP 读 computed（不是只看 CSS 文本）；②hover / focus / active 等伪类态单独验一遍（真实 `Input.dispatchMouseEvent` 触发 `:hover`）；③懒渲染元素用临时 DOM 节点验证后置覆盖；④**双层对比度复扫**：静态 CSS 层 `_audit_contrast_css_v852.py` ＋ CDP 渲染态九视图 `_audit_contrast.py`，只跑一层必漏（v852 教训）。
- 探针自身两处假红（口径错，非渲染 bug）：`--brand-ink` 真值是 `#3a55d6` 不是 `#3F5DF8`；computed 的 rgba 保留 `.10` 写法而非 `0.1`。另有一次「资产配置表 0 行」是**数据异步加载竞态**，须轮询等表格渲染后再取快照。**审计口径须与被审对象同构**（P23 同源）。
- tag：`fw2_v890_orange_accent`


## P27 硬卡「建了但没挂链」＝每晚 rc=1 却页面全绿（v891 实证）

- 症状：`_audit_dm_v845.py` 报 `FAIL=True / unregistered=['data/sec-daily.json']`；`runner_2026-11-09.log` L66 `[_gen_data_mgmt] rc=1`、L106「fw2_v845 发布清单数据文件漏登」。但线上数据管理页 `refreshFailed=[]`、所有条目绿，`handoff_check.py` 也报「无失败步骤」。
- 根因（三层叠加）：① v877 把 `data/sec-daily.json` 加进 `push_gh_v39.py` FILES，两端 DMCONFIG 没同步登记；② `_audit_dm_v845.py` 与生成器内 `fw2_v845` 自检**从未挂进 `push_gh_v39.py` 审计链**（只有注释提到生成器），发布闸门看不到它；③ `SCRIPT_TO_DM` 没有 `_gen_data_mgmt.py` 的映射，`REFRESH_BAD_STEPS` 里即便记了失败步骤也不会落到任何 DM 行 ⇒ 页面无红标。生成器写盘在硬卡之前（`open(OUT,'w')` 先于 `sys.exit(1)`），所以状态文件每天照样是新的，看起来更健康。
- 修法：①补登 + 双份 DMCONFIG 同步；②把 `_audit_dm_v845.py` 作为**无条件硬卡**插进 `push_gh_v39.py` 的 subprocess 审计链末位（FAIL → `SystemExit(1)`）；③新增数据集时同步页面里所有写死的条数文案（本次 5 处：2 处用户可见、3 处注释），注释一律改「按 DMCONFIG 条数」防再次漂移。
- 判别口径：**「审计脚本存在」≠「审计生效」**。查链路要同时看 ①谁调用它 ②失败时是否阻断 ③失败能否被状态页看见。三者缺一即静默失效。
- tag：`fw2_v891_dm_sync` / `fw2_v891_dm_audit_gate`

## P28 条件授权要先实证前提，别把「没实际用途」当结论（v892 实证）
- 用户答复「如果没有实际用途可删除」是**带条件的授权**，不是无条件删除令。直接删 `sources.json` 会连拆三处真实消费：① `refresh_all.py` 死规则① `_ASOF_FILES` 读 `sources.json.updated` 给数据集标数据日期；② `_audit_pe_chain_v846.py` 硬卡要求 `push_gh_v39.py` FILES 含 `sources.json` 且文件保留 `singleSource`／「单源」（该审计已挂日频链 pe-chain-audit 组）；③ `verify_sync.py` 标记串清单比对线上/本地。删整份 ⇒ 日频链与发布链双双红。
- 判别口径：**「文件没被页面 fetch」≠「文件没用途」**。本工程大量数据文件由静态硬卡 / 健康校验 / 标记串清单消费，前端零引用只是其中一层。查用途要按四段接通思路枚举：生成器、日频链、发布清单、校验／审计脚本。
- 正确落地：条件不成立时，只删**确实零消费且失真的部分**（`_note` 里「任何输出数据必须在本表登记」这句宣称，实际仅登记 7 个数据集、与数据管理 39 项展示粒度不同），保留有用途本体，并把 3 处消费依据写进交接文档，让用户能一句话改判。
- 顺带实证的既有红：`_audit_pe_chain_v846.py` 的 `peDate 单一数据日 ['2026-11-09','2026-11-10']` 在 11-10 21:38 日频日志里已存在，与本轮改动无关；该审计不在发布链内，不阻断发布。**别把无关联的红当成通过，也别顺手改它**（属数据口径，需单独拍板）。
- 另一次误判：PowerShell `Get-Content -Tail` 的控制台折行把 `- tag：...` 与 `## P27` 显示成连在一起，据此推断「标题粘连」并写锚点修复 → 断言 0 命中。文件真实字节是正常 3 个 LF。**从终端折行显示推断文件结构之前，先读原始字节**。
- tag：`fw2_v892_dm_caliber`


## P29 加一列 ≠ 只改表头：列索引会把静态硬卡与历史探针一起拖偏（v893 实证）
- 资产配置表从 13 列加到 14 列，至少五处必须同步：colgroup、thead、四类行模板、合计行、CSS `th:nth-child` 居中规则。**只改表头和主循环会整行右移一列**（v872 已实证：百分比落进「进度滞后」、`-100.0%` 溢出表外，页面不报错）。
- 更隐蔽的是「被审计/探针引用的列索引」：`_audit_alloc_cols.py` 把表头 13 列与行模板 11 td 写死；`_probe_alloc_color.py` 按 `col 9/11/12` 逐格断言进度滞后/调仓/偏移；`_audit_alloc_lag_color_v874.py` B27 反过来把探针里的 `c['col'] == 9` 当锚点卡死。**加列后这些数字全部失效**——不改，`push_gh_v39.py` 直接拒绝发布；只改探针不改审计，B27 也会红。
- 判别口径：**列数变化是全局索引变更**，先 `grep` 所有 `nth-child` / `col ==` / `== 13` / `== 11` / `len(ths)`，逐项判断是「当前渲染链」还是「历史配方资产」，两类都要重锚，别只修跑得最响的那条。
- 同源性比列数更容易漏：新增列若各写一套取数（列值 / 进度金额 / 合计），三处迟早漂移。v893 抽 `_dcaMonthly` 唯一实现并让进度金额、合计由它派生，静态硬卡 D01–D04 卡死「唯一实现 + 退役旧函数 + 累计同源」。
- tag：`fw2_v893_dca_monthly_col`

## P29 改列名＝改接口，别只改表头（v894）

- **现象**：把「进度金额」改「累计应投」、「实际金额」改「实际已投」，只改 `<th>` 看似零风险，但 `_audit_alloc_cols.py` 用 `ths[8]=='进度金额'` 定位、`_probe_alloc_progress.py` 用 `col('实际金额')` 定位。漏改前者发布链直接红，漏改后者探针静默取到 `-1` 列却可能空跑。
- **配方**：动列名先全仓 grep 该词在 `*.py` 的出现，分三类处理——① 生效审计/探针：同步重锚；② 历史版本配方资产：保留原样作版本史实；③ 长 changelog 注释：确认不是精确标记串后保留。改完加「旧列名表头清零 + 新列名到位」静态硬卡，并用 CDP 按表头 x 归位复验。
- **第二层坑（宣称≠实现）**：「实际已投」这个名字暗示「投进去多少本金」，但该列真实值是市值（含浮盈亏）。改名本身会把一个准确的旧名换成不准确的错名。故必须同步把真实口径写进可见说明并加静态硬卡，而不是只做字符串替换。v697d「累计投入错名」是同一类。

## P30 「融合」不是搬家：先判同源，再防两个静默失效（v895）

- **判同源**：用户说「把定投执行模块融合进资产配置」，直觉是把整块搬过去。源码实证 `stratCompute().alloc[code] === liveMonthly(code)`、`gapOf()` 就是主表「调仓金额」，月度定投表 5 列里有 2 列 + 2 处附注全是重复；剩下的 `planNote` / `S.plan[]` 又是 2026-09-29 的 5 万口径静态参数（现行 10 万 CAP），表头还写着已被 v486 废弃的「差额÷剩余月」文案。**若原样搬家，等于把重复值和过时口径一起摆到实时数据旁边。** 正确做法＝去重 + 旧口径折叠存档 + 明确标注非执行依据。
- **静默失效①（class 抢占）**：新增内容放在主表之前时，别复用 `.strat-note`——历史 CDP 探针统一取「第一个 `.strat-note`」作口径说明，会读到新卡文本却不报错。判别方法：新增 class 前先 grep 有哪些探针/审计用 `querySelector` 取该 class 的**第一个**。
- **静默失效②（折叠态丢失）**：`el.innerHTML = html` 重写会重置所有子节点状态。异步净值回来会再调一次 `renderStrategyView()`，用户刚展开的 `<details>` 被莫名收起。修法＝状态挂 window 级变量 + `el` 上 `toggle` **捕获**监听（toggle 不冒泡但捕获阶段经过祖先，且 `el` 本身不被重写）+ 写入后恢复。注意别把监听绑在会被重写的子节点上。
- **探针口径**：Chromium 对未 `open` 的 `<details>` 内容区用 `content-visibility` 隐藏但**保留布局高度**（实测 h=60），故「是否折叠」只能看 `open` 属性，不能看 `getBoundingClientRect().height`；驱动展开用真实 `summary.click()` 才能让 `toggle` 事件派发、验证状态记录链路。
- **第三层坑（锚点窗口 / 正例锚点）**：① `_audit_alloc_color_v873.py` A13 卡「`classList.add('na')` 必须紧跟 `el.innerHTML` 且相距 < 900 字符」，把新代码块插在两者之间会撑破窗口、发布被拒，而代码本身完全正确。**别放宽阈值**（等于掩盖真实漂移），应调整新代码顺序到锚点之后并加硬卡卡死顺序（G04）。② 删旧渲染块时，块内可能同时是**另一条审计的正例锚点**：v875 `_audit_var_paren_v875.py` E2.18 把 `color:var(--up,#b91c1c);...` 正确闭合形态当正例，该串只存在于被删的定投表里，删完发布链即红。修法＝让迁移后的同功能代码（`ddwOf()`）沿用同款 token 正确形态，而不是改审计清单（E05 卡死）。**删块前先 grep 该块内的特征串被哪些审计/探针引用。**


## P31 名字改错了要「改回来」时，注释区的史实旧值会被误判成残留（v896）

- **现象**：v894 把第 10 列改名「实际已投」，v896 按用户拍板 A 回正为「实际市值」。配方脚本末自检写「旧列名全文只剩 1 处（v894 史实注释）」，实际跑出 2 处 → 断言失败。**这不是页面 bug**：第 2 处正是脚本自己刚追加的 v896 回正映射注释 `实际已投→实际市值`。前 5 步已全部落盘，若按「重跑补丁」处理会因锚点已变更二次失败。
- **正确分区**：现役表头 / 口径说明 / 渲染模板属「必须清零区」；表头注释、docs changelog、历史配方、版本冻结探针属「史实保留区」。断言必须按**精确形态**判定现役区（`实际已投 = 当前持仓市值`、`目标 − 实际已投`、`实际已投 − 累计应投`、`<th>实际已投</th>` 四种），再加一条反向硬卡保证史实注释没被误删（E06）。**全局 `replace_all` 在这里等价于删护栏。**
- **第二层坑（新硬卡自身口径错）**：为证明「取数零改动」新增 E07，凭印象把 `_dcaMonthly` 写成 `return liveMonthly(code)`，而源码真实形态是 `return (typeof liveMonthly === 'function' ? (liveMonthly(code) || 0) : 0);` → 发布链假红。处理同 P30 第三层：**读源码按真实形态重锚，不删断言、不放宽阈值**。同一轮里「断言漏算自己新增的内容」和「锚点凭印象写」是两类不同的假红，别混为一谈。
- **业务侧根因**：改列名时先问「这个名字描述的是不是这个数」。v894 把一个准确的名字（实际金额）改成不准确的名字（实际已投），虽当场在可见说明标注了真实口径，仍挡不住快速扫表时的误读——尤其该列被 `进度滞后` 与 `调仓金额` 两个公式引用，误读会直接进决策。名实不符时**优先改名字匹配数值**，不要靠加免责小字。

## P32 对比卡片「数字都对、方向是反的」——差值符号 × 配色 × 分母 × 日期标签 × 风险预算五处静默错（v897 修四处 / v898 修第五处）

- **症状族**：组合回测页「最大回撤 −12.25%」下方挂着**绿色** `+2.06 pct`；总收益 66.59% 比同期对照「高出一大截」；净值曲线副标写「3281 个**交易日**」；截止日下拉怎么点都到不了 2026-09-28 之后；档位表四档市值加总比期末市值少 1,328.45 而表里没有现金行。
- **①方向×配色**：`card()` 统一「正数＝好＝绿」染色，但回撤是负数指标，传参写成 `S.hold.mdd - S.strat.mdd` ⇒ 策略回撤更浅时得**正数**，绿了。判别法：**凡「两个负数相减」的差值，先手算一遍符号再看颜色**；同页「年化波动」用 `hold.vol - strat.vol` 是对的——**同一段代码里只有一张卡反了**，别顺手把对的一起改。修法：差值一律按「策略 − 对照」，负数指标则配合 `h` 的语义（越大越好）统一定义，勿按指标类型各写一套。
- **⑥风险预算替用户编（v898 修）**：面板里「回撤预算」默认写 35%，文案还括注「可忍 25–35%」——这是**代码替用户假设风险偏好**。后果不是显示错，而是**结论错**：会把 −12.25% 的回撤读成「只用掉 35%–49% 预算、还有大半没用」，而用户实际可忍是 20%（占用 66.4%，已用掉三分之二）。判别法：**凡「预算/容忍度/目标」这类偏好参数，只能来自用户明说，且必须有输入框可改；代码默认值一旦被写进结论文案就必然漂移**。修法：默认改 20%、清掉「可忍 25–35%」的替用户设定、占用卡给「余量/越界」方向色、Calmar 卡给出 `目标年化/回撤预算` 达标线；存量 localStorage 里恰好等于旧默认 35 的值做一次性迁移并在页面上明示（不静默改用户数据）。
- **⑦简版 Calmar 把「跑赢定存」算成超额（v899 修）**：面板原来用 `年化/|回撤|` 定义 Calmar、达标线 `目标年化/回撤预算`，没扣无风险利率。严格口径应为 `(年化 − 无风险)/|回撤|`、达标线 `(目标年化 − 无风险)/回撤预算`。判别法：**凡风险调整收益指标，先问「分子扣没扣无风险」**——本例同一组数据两套数：简版 1.44 vs 达标 0.50（+0.94）；严格版 1.32 vs 达标 0.42（+0.90），差别不大但口径必须一致，否则将来换标的时误差会放大。修法：`calmarS=(ann−rf)/|mdd|`，rf 走输入框（默认中国货币网 10Y 国债，不写死）。
- **⑧渲染函数里误用别处的局部 helper，异常被 `try/catch {}` 吞掉（v899 自伤）**：改 `renderBacktest` 的口径文案时调用了 `fmtN()`，而 `fmtN` 是 `btRun` 的局部函数 ⇒ 抛 `ReferenceError`，但 `switchStratTab` 的兜底是 `try { renderBacktest(); } catch (e) {}`，于是**页面只是空白、控制台无报错**，看起来像「tab 没切换」。判别法：**改渲染函数时，凡新引用的 helper 先确认它在同一作用域**；遇到「点了没反应且无报错」，先把那个空 catch 改成 `console.error` 再复现（本次就是这样抓到 `fmtN is not defined` 和第二轮的 `rfUsed is not defined`）。修法：口径行里改用函数内自算的 `ddLine`；卡片的 rf 改用 `S.rfUsed`（stats 上带过来的值）。**交付文件里的空 catch 未改**（改动面大，另立条目）。
- **②分母覆盖**：`ret = endV / cfg.budget - 1` 把分母钉在 5 万，而 `gridUsed`（预算外备用金）真在参与买卖 ⇒ 48.74% 被显示成 66.59%（虚高 17.9 pct）。判别法：**凡收益率卡，先问「分子里的钱从几个来源来、分母写全了没有」**。修法：`capBase = budget + gridUsed` 作主口径 + 并列「仅本金」口径，两个都显示；**未动用的备用金余量既不算进期末市值也不算进分母**（若算进分子会出现「没进场也赚钱」的假高收益），并在 UI 一行写清。
- **③日期标签口径**：区间 distinct 净值日期 3281（货基 `007866` 贡献 339 个周末点）、日历日 3346、工作日 2390——文案把净值日期数写成「交易日」。判别法：**任何「N 个交易日」先分别数三条数（distinct 净值日期 / 日历日 / 工作日）再落笔**。注意年化本身可能没问题：`annRet` 用 `365.25/n`，n 与日历日是同一量级，所以「5.85% 是对的、错的是文案」这种混合情况要分开判，不要一看到标签错就认为数值也错。
- **④硬编码日期上限**：`inp('end')` 的 `max` 与 `btCfg()` 默认同写 `2026-09-28`，数据 asOf 已到 2026-11-10 ⇒ 少跑 6 周且选不到更晚日期。修法：渲染时读 `BT_CACHE.meta.asOf`，**数据到齐后再 `setAttribute('max', asOf)`**——只做前者不够，首屏渲染时缓存还是空的，会落回占位值（本轮实测 `max` 停在 `2026-12-31`，补了到齐后回写才对上 `2026-11-10`）。再加一行「数据 asOf X，截止日落后 N 天」提示，用户才知道自己少跑了哪段。
- **⑤分类表加总缺口**：四档 = 41.39+32.01+5.72+13.42 = 92.55%，剩下 7.45% 是未部署现金，但表里只有四行 ⇒ 与期末市值天然差 1.58%。判别法：**分组表必须有一条「使 sum = 期末市值」的兜底行（现金/未部署），并且合计行与期末市值同源**，否则任何一次核对都会被判「表算错了」。
- **一般化**（可复用到任何自建统计面板）：审计顺序＝① 指数/负数指标的方向与符号 → ② 分母覆盖与资金口径 → ③ 日期标签与抽样粒度 → ④ 分类表加总闭合 → ⑤ 颜色语义。**前四项任一处错，卡片都「看起来很专业」**，只能靠交叉核对抓出来；详见 experience `backtest-stats-panel-fidelity-audit.md`。

⑨ **面板文案读的是 `renderBacktest()` 入口的 `cfg` 快照，而 `go()` 用新收集的 `c` 跑回测**（v900 修）
- 症状：把「目标年化」从 10 改成 25 再点运行，输入框 `value` 确实是 25，结论条仍写「目标 10.00%、达标线 0.42」；反过来改回 10 也不更新。用户看到的是「输入框与面板不一致」。
- 证伪：`fgrep btSave(c)` 之后紧接的是 `var out`，中间没有重读配置；而拼文案用的 `tgt = +cfg.tgtAnn` 里的 `cfg` 是函数入口 `var cfg = btCfg();` 的**一次性快照**（`btSave` 只写 localStorage，不会回写这个变量）。把 `cfg` 打进 `console.error` 就能看到它停在旧值。
- 修法：`btSave(c)` 之后立刻 `cfg = btCfg();`（tag `fw2_v900b_bt_cfg_refresh`）。同批把 `renderStrategyView` 的 `try { renderBacktest(); } catch (e) {}` 改成 `console.error('BT_RENDER_ERR', e && e.message, e && e.stack)`（tag `fw2_v900c_no_silent_catch`）——空 catch 是这类错误长期隐身的根因（见 ⑧）。
- 验证：页面上把目标年化 10→25→10 来回改并点运行，结论条随之在「✗ 未达标｜目标 25.00%，缺 5.85pct｜达标线 1.17」与「✓ 达标｜目标 10.00%｜达标线 0.42」之间切换；色条 `rgb(4,120,87)`。

## P33 `handoff_check.py` 在默认 GBK 控制台中途 OSError 22 崩掉（v897 顺手修）

- 症状：`& py handoff_check.py` 只输出到第 1 段（README 断点）就停在 `OSError: [Errno 22] Invalid argument`，第 2–7 段全看不到；同一命令加 `PYTHONIOENCODING=utf-8` 或重定向到文件则正常。
- 根因：脚本 `print` 的「最近日志」里带历史符号（`|` 与旧 verify_sync 告警行里的全角/emoji），Windows 控制台默认代码页为 GBK 时写盘失败，**而它正是 AGENTS「开工第三步」的唯一出口** ⇒ 新接手的 AI 会以为工程状态读不到。
- 修法（已落盘）：脚本 `import` 之后加 `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`；这是**兜底不改内容**的最小修，绝不改成删符号（那些符号是日志原文）。
- 判别：先看它是否「打印到固定段落就停」——停在某段之后且退出码非 0＝编码问题，不是数据问题，别去查台账。
- tag：`fw2_v897_handoff_enc`

## P34 QDII 净值滞后一日 → 月频末点停在 D-1，源补发后闸门立刻 FAIL（2026-11-11 实证）

- **症状**：`push_gh_v39.py` 首行直接 `!!! GATE 未通过，拒绝推送 !!!`，明细 `fund_monthly FAIL verify_dual_source:F verify_acc_nav:F`，尾部 `发布文件不一致=5`（该次实为 2 只基金 + 3 只货币型预期跳过）。奇怪的是同一条命令一小时前刚跑过 `GATE=PASS`。
- **证伪路径**：①`verify_acc_nav.py` 全量跑，逐只打印，锁定 `163813`（文件 2026-11 = 1.0625，源A 重建 = 1.0587）与 `501226`（2.2686 vs 2.2727）；②直接打东财 lsjz 接口查最近 5 个交易日，发现 `2026-11-10` 两只有官方值（1.0587 / 2.2727），而本地 `fund-daily.json` 末点是 `2026-11-09`（1.0625 / 2.2686）——**不是算错，是数据晚到**；③`meta.asOf` 写的是全市场最大日期 2026-11-10，所以从 meta 上看不出这两只缺了一天。
- **根因**：QDII 净值 T+1/T+2 才公布，晚 17:00–18:00 才落官方值；白天刷新时这两只只能拿到 D-1，月频「不完整月」行取的也是 D-1。等官方补发后，闸门用**当刻**源重建去比对**当时**写下的文件，必然不一致。这是「源会往前长、文件是快照」的固有错位，不是校验器误报。
- **修法（按顺序）**：`gen_fund_daily.py` → `gen_fund_monthly.py` → `gate.py --datasets fund_monthly --check` 确认 `GATE=PASS` → 再 `push_gh_v39.py`。日频重跑会顺带更新 181,812 行（对拍通过），月频 81 只 / 7,382 行。
- **别做**：不要为了过闸门手改那两行 nav/acc（会破坏「文件值 = 源可重建值」的契约，下次刷新又对不上）；不要给 `verify_acc_nav` 加白名单放行 QDII——那会把「晚到」和「真错」一起放过。
- **预防**：QDII 占比高的日子（净值发布日 17:00 后）先跑一次基金刷新再发布；看到 `GATE=FAIL` 先读「发布文件不一致=N」与逐只明细，判断是晚到还是真错。

## P35 带宽再平衡的下带，在单边下跌里等于逆势接刀（v903 选型，2026-11-12）

- **症状**：把再平衡从「档位级」改成「标的级 ±25% 双边」后，回撤从 −13.6% 降到 −8.6%，但 2021-02-18 起点（沪深300 高点）那段年化从 10.74% 掉到 7.06%，Calmar 反而从 0.75 掉到 0.63。
- **证伪**：同一份数据只去掉「下带补仓」（只上带），该段年化 5.42%（更差）；再叠加停用止盈则回到 6.22%、Calmar 0.87。说明落差的来源不是实现错误，而是「跌破下限就补仓」在单边下跌中持续加仓下跌资产。
- **根因**：带宽再平衡的双边是对称的，但两侧的经济含义不对称——上带＝止盈（减配赢家），下带＝接刀（加仓输家）。框架里没有「趋势/估值」过滤，下带只能按机械规则补。
- **修法**：只上带（`cur > tgt*(1+band)` 才卖，跌破不动），并把减出的钱停在现金。实测四段 Calmar 全部高于原档位级：0.58 / 0.73 / 0.87 / 1.52（原 0.36 / 0.47 / 0.75 / 1.12）。
- **别做**：不要为了「年化好看」把下带加回来而不加过滤——那等于把 2021 段的 −3.68pct 年化损失重演一遍。

## P36 参数语义变了却不迁移旧值，等于用旧尺子量新东西（v903，2026-11-12）

- **症状**：v903 把 `cfg.band` 从「档位偏离提示带宽（默认 5pct）」改成「单标的减配带宽（默认 25%）」，本地实测升级后页面仍读 localStorage 里的旧 `band=5`，减配按 5% 触发。
- **影响**：实验 V12（5% 带宽双边）再平衡 91 笔 vs 25% 版的 24 笔，换手放大近 4 倍；只上带版同样会被打得更碎，等于把「季度检查」变成近似月度绞肉机。
- **证伪**：读 `localStorage.getItem('fw2_bt_cfg_v1')` 可见 `band:5`，而 `btCfg()` 默认已是 25 —— 差异只能来自存量配置。
- **修法**：`btCfg()` 里加迁移 `if (+d.band > 0 && +d.band <= 10) { d.band = 25; }`，并 `console.warn('BT_BAND_MIGRATED', ...)` 留痕（不静默改配置）。
- **预防**：任何「同名参数换了语义或量纲」的改动，都要在读取处加阈值迁移 + 留痕，并在 README/FRONTEND 写明新旧语义；只改默认值不改迁移，老用户永远拿不到新默认。

## P37 两个闸门进程并行读写同一份 `_hist_cache`，会读出半截 JSON 报「意外跳过」（2026-11-12）

- **症状**：`gate.py --check` 手动跑一次 `GATE=PASS`（11 个数据集全过）；紧接着 `push_gh_v39.py` 内部再跑 gate，同一份数据变成 `verify_acc_nav ACCNAV=FAIL`，原因是 `★意外跳过（必须排查）: ['019155']`。
- **证伪**：①`verify_acc_nav.py --only 019155` 单跑立刻 `ACCNAV=PASS`（源A/源B 各 39 月、交集 39、不一致 0）；②`data/_hist_cache/019155.json` 的 mtime 落在两个 gate 进程重叠的那几分钟（89,232 B 写完整后用）。说明失败来自读到了正在被写的那份文件，不是数据错。
- **根因**：`verify_acc_nav` 按既有缓存重建源A，缓存缺失/为空即判「意外跳过」。两个进程同时刷新同一只基金的缓存时，后到的读进程可能读到未写完的文件 → 「源A 缓存为空」。
- **修法**：发布时**只让一个进程跑 gate**——手动 `gate.py --check` 通过后不要再并行任何校验，直接跑 `push_gh_v39.py` 让它内部 gate 单独跑完；被拦时先用 `--only <code>` 复验该只，PASS 即判竞态，重推即可。
- **别做**：不要因为这个报错去改白名单、把 019155 塞进「预期跳过」——那是把它从「必须排查」降级成「允许缺数据」，真错会被一起放过。

## P38 · 回测收益率的分子分母不同源 → 「仅本金口径」系统性高估

**症状**：主表把「总收益率」从 `retBase`（= `endV / cfg.budget − 1`）换成含追加的 `ret` 后，同一组数据出现 96.74% 与 74.11% 两个数，差 22.6pct；用户会以为「只按本金算更赚」。

**证伪**：核对 `btRun` 里两处口径——`ret = (endV / capBase − 1)*100`，`capBase = cfg.budget + gridUsed`；`retBase = (endV / cfg.budget − 1)*100`。**分子 `endV` 只有一个**（含动用备用金产生的全部收益），分母却有两个。用 `期末市值 / 总投资金额 − 1` 手工对账，74.11% 自洽、96.74% 不自洽。

**根因**：`endV` 无法拆分「多少收益来自本金、多少来自备用金」，所以任何「只用本金当分母、却仍用全资产当分子」的比率都是错配，不是"另一种口径"。

**修法**：主表只用同源口径（`ret`，分母 = 总投资金额）；把"仅本金"退化为一对**可核对的事实行**（`其中动用备用金 ¥X` / `备用金未用尽 ¥Y`），不给比率。tag `fw2_v905_bt_cmp7_tp_rename`（`_apply_bt_v905c.py`）。

**通用判据**：任何「收益率 / 占比」上线前，先问分子和分母是否来自**同一资产池**；不是就改成事实陈述（金额），别造一个看起来精确的百分比。

### P39 · `null` 当哨兵却被 `!= null` 排除

- **症状**：把"不限额"编码为 `fund === null` 后，页面上该资金池一次都没动用，累计值恒为 0，主表金额倒退回本金，且**没有任何报错**。
- **证伪**：把哨兵改成 `Infinity` 或加临时 `console.log(cfg)` 看池子判定分支；若日志里 `pool` 永远是 `'cash'` 而开关确实是开的，就是判定条件写错。
- **根因**：`null != null` 的宽松比较结果是 `false`，所以 `x != null` 本意是"不是 null/undefined"，恰好把哨兵判死。同理 `null < 500` 为 `true`（被当作 0），会让 `need < amt` 提前 return。
- **修法（v906，tag `fw2_v906_bt_fund_unlimited`）**：判定改 `Px.gridFund !== 0`（0＝预算内、null＝不限额、正数＝有上限）；`need` 用 `Infinity`；扣减前 `if (Px.gridFund !== null)`；`gridOk` 对 `null` 直接 true。
- **教训**：用 `null` 表达三态之一时，所有 `!= null` / `<` 比较都要逐个回读；宽松比较会静默给出错的布尔值。

### P40 · ECharts 精简构建里 heatmap / scatter 静默失效

- **症状**：`setOption` 传 `type:'heatmap'`（或 `scatter` / `custom`），画布只出坐标轴和浅色底，**没有格子、没有散点，控制台也不报错**，看像"数据为空"。
- **证伪**：`echarts.getInstanceByDom(el).getOption().series.length` 为 **0** —— series 被丢弃，不是数据问题。再逐个类型打表实测：`line` / `bar` / `pie` → 1，`heatmap` / `scatter` / `custom` → 0（本页 `echarts.version` = 5.6.0）。
- **根因**：页面引的是**按需打包的精简构建**，未注册这三种 chart；未注册类型在 `setOption` 阶段被静默过滤，不抛异常，所以只有"空白"这一个症状。
- **修法（v910，tag `fw2_v910_bt_process_charts`）**：月度收益热力图改用 `bar` 正负双色 + 0 基线（信息量等价：哪几个月最难受）。若确实需要矩阵，得换完整版 echarts 或补注册，别靠猜。
- **教训**：用任何非 line/bar/pie 的 ECharts 图表前，先跑一行 `series.length` 断言再往下写；"空白但不报错"优先怀疑图表类型未注册，而不是数据为空。

### P42 · 同一份文件上午 gate PASS、下午 FAIL：数据校验器拿"在线源"比"内嵌快照"

**症状**：`index.html` 只改了样式/文案（一个字节的数据都没动），`push_gh_v39.py` 的 gate 却在 `fund_monthly` 上红：
```
[verify_dual_source] DUALSOURCE=FAIL
[verify_acc_nav] rc=1 尾部: 累计净值比对点数=7161  源间不一致=0  发布文件不一致=1
fund_monthly   FAIL   verify_dual_source:F verify_acc_nav:F verify_wind:P
```
而同一份文件几小时前（v911）刚 PASS 过。

**证伪**：`verify_acc_nav.py` 单跑，抓 `✗` 行 → `✗ 发布文件 2026-11 文件=2.0288 源A重建(2026-11-11)=2.1215`，具体到 `[FAIL] 017436 华宝纳斯达克精选股票发起式(QDII)A`。再看 `data/fund-daily.json` 里该代码最后一天 = **2026-11-10（2.0288）**，而校验器的"源A"是**在线接口**，当天早上已放出 11-11 的 2.1215。
→ 不是数据错、不是页面错，是**本地日频落后在线源一天**。

**根因**：QDII / 海外基金净值披露晚于 A 股，本地 `refresh_all.py` 每晚固定跑一次；若发布时间在"第二次披露之后、下一次刷新之前"，内嵌快照必然落后在线源一天以上，两个校验器的 `发布文件不一致` 就亮红。属**时序竞态**，与代码改动无关。

**修法（按顺序）**：
1. 先单跑校验器抓 `✗` 行，确认是"同一只基金、同一个月锚、差一天"；
2. `python refresh_all.py --only fund-monthly,fund-daily --no-publish`（**必须带 `--no-publish`**，否则它自己会推）；
3. 重跑 `verify_dual_source.py` + `verify_acc_nav.py`，两个都 PASS 再发；
4. 发布前确认内嵌数据块没被刷新脚本吃掉页面改动（`ver-badge` / tag / 新标题仍在）。

**别做的**：不要为了过闸门去改校验器的阈值或加白名单——它抓到的正是"页面数据比源旧"，是真问题，只是成因在时间不在代码。也别手改 `data/*.json` 补那一天。

**tag**：`fw2_v912_bt_chart_titles`（2026-11-12 首例）

## P41 · 图表只占左侧一块、右侧空白、x 轴标签只剩一两个

- **症状**：图表内容压在最左边一条窄带、右侧大片空白；类目标签只剩一两个或叠成一坨；分类轴（归因 / 持仓）的名称垂直堆叠。而 `getOption()` 里类目数、点数都是对的，所以不是数据问题。
- **证伪**：比较 **`el.getBoundingClientRect().width`** 与 **`canvas.getBoundingClientRect().width`**，两者不等就是布局尺寸不同步。
  - **别用 `canvas.width` 比**：那是绘图缓冲像素（CSS 宽 × `devicePixelRatio`）。实测 `canvas.width=763` 对容器 `509`、`1026` 对 `684`（DPR 均为 1.5），看着像"canvas 宽了 1.5 倍"，其实完全正常。**第一轮就是被这个差值骗了，诊断方向带偏一整轮**。
- **根因**：ECharts 只在 `init()` 时读一次容器尺寸，之后**不会**自动跟随容器变化。窗口缩放、抽屉展开/收起、所在面板从 `display:none` 变可见，都会让容器宽度变化而 canvas 停在旧值。`#btChart` 在 v904 单独挂过 `ResizeObserver`（`window.__btChartRO`），v910 新增的四图**没挂** —— 所以症状是"新图破、老图正常"。
- **修法（v911，tag `fw2_v911_chart_resize`）**：把观察收进全局 `mountChart`：`init` 后 `new ResizeObserver(() => c.resize()).observe(el)` 并立刻 `c.resize()` 校正一次；`dispose` 旧实例前先 `charts[id].__ro.disconnect()`。一处修复覆盖所有图。
- **验收断言**：①`el.getBoundingClientRect().width === canvas.getBoundingClientRect().width`（±2px）；②把容器 `style.width` 压到 6px 再清空 → `chart.getWidth()` 必须 6 → 509 跟着回来，且类目标签数恢复。
- **教训**：凡"新加的图表异常、老的正常"，第一件事查新图有没有漏挂 ResizeObserver；图表尺寸类问题的第一证据永远是 **CSS 尺寸对比**，不是 `canvas.width`。

## P43 · 自选池「加了不生效」三连坑（v913）

**症状**：①新启用的「自选基金」tab 永远是空池，但 `watchlist-data.json` 明明有 11 只；②手动加入的基金被标成「筛选池」来源；③回测切「杠铃+自选池」只多纳入手动加的那只，自选表 11 只全没进来；④新增标的在结果里几乎不起作用（权重 1%~2%）。

**证伪与根因**（逐个独立）：

1. **空池**：`loadPoolData()` 的调用点只有「重新加载 / 首次进基金数据页」，`showTab` 的 `pool-watch` 分支只 `renderPoolWatch()` 不加载 → `window.POOL_WATCHLIST` 恒 `undefined`。死代码期间没暴露，是因为入口本来没人点。
2. **来源错标**：`added` 这个 localStorage 桶同时存「筛选池转入」与「手动加入」，渲染时统一写 `source:'筛选池'`。
3. **回测漏自选表**：`loadPoolData` 定义在基金数据闭包里，回测代码在另一闭包，`typeof loadPoolData === 'function'` 为 false → 预加载静默不执行。**别用「同文件就是同作用域」的直觉判断闭包**，本页几十个 IIFE。
4. **权重无感**：原标的 `w` 是刻意设的（016452 纳指、511260 国债 = 5，普通标的 = 10），新增标的按 `w=1` 参与归一 → 实际权重 1/38 ≈ 2.6%，乘档位 35% 后约 0.9% 预算，看着像没纳入。

**修法（v913，tag `fw2_v913_watch_pool` / `fw2_v913_watch_add` / `fw2_v913_bt_pool`）**：①`showTab` 的 `pool-watch` 分支补 `loadPoolData()`，并在 fetch 回调里按当前 tab 补渲；②按 `manual` 标记拆来源与计数；③回测闭包自带 `btEnsureWatchPool()`（相对路径 fetch + 到位后 `__btGo()` 重跑）；④新增标的 `w` 取该档非零 w 的中位数；⑤`watch` 模式档位目标在有标的的档位间归一，避免某档空着只用 35% 预算。

**验收断言**：①自选 tab 行数 = 自选表未持仓部分 + added 未持仓部分（剔除 removed）；②摘要行 `计划 / 实际建仓 / w=0 候选 / 缺日频代码` 四数与「按标的阈值」表只数闭合（实测杠铃 13/11/2/0、杠铃+自选池 16/14/2/0、仅自选池 3/3/0/0）。

**tag**：`fw2_v913_watch_pool` / `fw2_v913_watch_add` / `fw2_v913_bt_pool`（2026-11-12 首例）

## P44 · 表格首列「内容全空白」——sticky 在无横向滚动时吞掉单元格内容（v915）

**症状**：自选基金池第一列整列空白（名称/代码/来源都不显示），而同一行第二列起的「档位/家族」和数字完全正常。表格有边框、有行高、首列还占着 139px 宽，就是没有一个字。背景色（`--panel-3` 灰）照画。

**证伪三层（都正常 → 说明不是数据/样式问题）**：
1. DOM：`td.textContent` 完整（`国富全球科技互联混合(QDII)人民币A006373自选表 · 08-03`），`span.offsetWidth=124 / offsetHeight=38`；
2. 样式：`color rgb(16,24,40)`、`display:inline-block`、`visibility visible`、`opacity 1`、`overflow visible`；
3. 命中：`document.elementFromPoint()` 在该坐标返回的就是那个 `span`——**没有任何覆盖层**。
4. 决定性实验：把整格换成 `<span style="color:#b91c1c;font-weight:700">测试纯文字ABC123</span>`，仍然不显示 → 与列内样式无关。

**根因**：`#view-data .dc-tbl td:first-child{position:sticky;left:0;background:var(--panel-3);z-index:1}`。当表格 `scrollWidth < clientWidth`（**没有真实横向滚动**）时，Chromium 对 table 里的 sticky 单元格会裁掉其内容层，只保留背景。有横向滚动时（如 64 列宽表 4955px）一切正常——所以同一个组件在窄屏好、宽屏坏。

**修法（v915，tag `fw2_v915_watch_nostick`）**：对不需要冻结列的表格单独关掉——
```css
#view-data #dcPoolWatchWrap .dc-tbl td:first-child{position:static;left:auto;background:var(--panel-3)}
#view-data #dcPoolWatchWrap .dc-tbl th:first-child,
#view-data #dcPoolWatchWrap thead th{position:static}
```
**注意表头要连 `top:0` 一起关**：只把 `left` 改 `auto`、保留 `position:sticky;top:0` 时，表头首列文字同样不显示（同一个机制）。

**验收断言**：`table.scrollWidth < wrap.clientWidth` 且首列 `td.textContent` 非空时，首列必须有可见文字——直接看渲染截图，不要只看 `textContent`（本次三层 DOM 检查全绿仍未发现，必须截图）。

**教训**：`position:sticky` 的首列在「宽表 + 窄屏」场景是必需品，在「窄表 + 宽屏」场景却是地雷。给某张表加 sticky 前先问它到底会不会横向滚动；两个方向的尺寸都要截图验证。


## P45 · 自选池「按基金类型分档」全落进攻档 —— 画像根本没加载（v916）

**症状**：004945（长信中证500指数增强A，`type=指数型-股票`、`family=中证500`）在回测「按标的阈值」表的「档位」列显示**进攻**，档位汇总「底仓/缓冲 40% ¥0.00 / 0.00% / −40.00pct」，即 base 分支完全没命中；同一台机器上自选池「档位/家族」列整列显示「—」。

**走过的弯路（两条都白费力）**：
1. 解析内嵌镜像 `window.FUND_PROFILES_MIRROR` 时用 `s.find("};")` 截取 → JSON 内层 `}` 就截断，`JSONDecodeError`；正确做法是找 `window.FUND_PROFILES_MIRROR = `（带空格）起点，再 `json.JSONDecoder().raw_decode(raw)` 解第一个对象（尾部还有其它语句，`json.loads` 会报 `Extra data`）。
2. 用 `bu.js("window.__poolProfileE('004945')")` 验证 → 恒 `null`。`bu.js` 与页面主 world 不是同一 JS 上下文（`window.SIGNALS_CFG` 同样读不到），**window 变量不能当证据**，只能读渲染结果。

**根因**：`loadFundProfiles()` 只在「基金数据」页的渲染入口被调用一次。直接从「策略执行」页跑回测时 `FUND_PROFILES` 恒为 `null`，`poolProfileE()` 回退到 `window.SCREEN_POOL`；该 code 不在筛选池快照里（screen-pool 只有 40 只）时直接返回 `null` → `type/family` 全空 → 类型规则逐条落空 → 全部掉进最后一条「进攻」兜底。**这不是 v916 新引入的**：v913 的 `btRolePile(e.role)` 同样拿不到 role，只是当时进池的 3 只（006373/270042/007817）本来就该归进攻，碰巧对上了，缺陷被"正确结果"掩盖。

**修法（`fw2_v916_bt_watchw`）**：在 `poolProfileE` 开头按需同步吃内嵌镜像（零网络，与 `loadFundProfiles` 的镜像快路径同源；fetch 兜底链不动）：
```js
if (!FUND_PROFILES && window.FUND_PROFILES_MIRROR && window.FUND_PROFILES_MIRROR.funds) {
  FUND_PROFILES = window.FUND_PROFILES_MIRROR; FUND_PROFILES_LOADED = true;
}
```

**验收断言**：①自选池「档位/家族」列**不得出现「—」**（本地实测 3 行全有值：进攻/主题 科技/AI、纳指100、通信/5G）；②手动加入 004945 后，仅自选池模式摘要「计划 4 只 / 实际建仓 4 只」，交易流水出现 `2021-01-04 … 建仓 base 预算 ¥2,500（＝5%×50,000）`、`2022-04-26 … 止损 base 清仓` → base 分支命中。

**教训**：任何「另一个页面先被访问过才就绪」的全局快照，都要在使用点做懒加载兜底。否则测试路径（直接进功能页）与用户路径（先逛列表页）会得出不同结论，而碰巧正确的旧数据会把缺陷藏起来。另外：`window.SCREEN_POOL` 这类兜底源字段不全（无 type），不能当作 profile 的等价替代。

**v917 补充（tag `fw2_v917_watch_cols_aligned`）**：自选池按用户要求回到完整 61 列后，表格重新产生真实横向滚动（`.table-wrap` 实测 `4566/509`），v915 那三条 `position:static` 覆盖整段删除、恢复冻结首列，并在 `scrollLeft=1200` 与最右端两种位姿下验证首列文字可见。

**判据升级（写死成规则）**：`position:sticky;left:0` 的首列是否安全，取决于**这张表实际有没有横向滚动**，不是取决于视口宽——
- `table.scrollWidth`（或包裹层 `.table-wrap` 的 `scrollWidth`）`> clientWidth` → sticky 安全且必要（冻结列可读）；
- 两者相等（无横滚）→ sticky 会裁掉内容层，必须对该表关掉 `left`（表头连 `top` 一起关）。
改列集、改视口、改容器宽度都可能翻转这个判据，**每次都要重新量一次 `scrollWidth / clientWidth`**，不要复用上一次的结论。

## P46 · 「自选组合回测」四个易错点（v918）

**症状 1**：切到自选组合后，tab 高亮和摘要对不上（卡片写「持仓组合回测」变黑，摘要却写「仅自选池」）。
根因：v913 遗留 `cfg.pool` 有 `watch` / `barbell_watch` 两个值，若高亮写成 `cfg.pool === v` 就两个卡都不亮；若把旧值都当 `barbell` 又变成「亮持仓卡、跑自选池」。
修法：高亮 = `v==='barbell' ? cfg.pool==='barbell' : cfg.pool!=='barbell'`，并在面板顶部对旧模式加黄条 +「切换到自选组合」按钮（`data-cu-legacy`）。

**症状 2**：点「预置杠铃 11 只」却选中 13 只、摘要写「计划 13 只」。
根因：`SIGNALS_CFG.barbell.funds` 有 13 只，其中 022676 / 007866 的 `w = 0`（在「持仓组合」里本来就不建仓）。
修法：预置时 `filter(f => (+f.w||0) > 0)`，与持仓组合的 11 只对齐。

**症状 3**：面板里只有「持仓」「自选」两池，筛选池始终 0 项且不报错。
根因：筛选池不在内嵌镜像里，靠 `btEnsureScreenPool()` 异步 `fetch('./screen-pool.json')`；本地直接开 `index.html`（`file://`）或无网络时会失败。
修法：`btEnsureScreenPool` 两步兜底（相对路径 → raw.githubusercontent），成功后调 `window.__btCuRefresh()` 重刷列表；离线且两步都失败时列表静默少 40 项——验收时一定要数 `items`，只看「面板出来了」不够。

**症状 4**：勾了基金但结果区「档位/目标」还是杠铃的 40/35/10/15。
根因：`btTargets` 的 custom 分支只改了 `funds`，没改 `return` 里的 `target`。
修法：custom 必须重建 `tgtOut`（四档目标＝勾选基金按 `btTypePile` 汇总的真实占比），并透传 `customN/customWMode/eqPct`。验收判据：勾 3 只全为「进攻」时，档位表目标列应为「进攻/主题 100%」。

**验收基线**：列表 66 项（持仓 23 / 自选 3 / 筛选 40）；等权 3 只每只 33.33%、建仓 ¥16,667；固定 5% 每只 ¥2,500；持仓组合必须仍是 5.08%，逐项对齐 v917。

## P47 · 只删 UI、不压回配置：界面已无该选项，页面仍按旧值跑（v919）

**症状**：把某个下拉选项删掉（或改名）后，老用户的 `localStorage` 里仍留着旧值（如 `mode='real'`、`pool='watch'`），页面渲染时没有该选项可显示，但计算分支仍按旧值走 —— 表现为「界面说 A、结果按 B 算」，且刷新不会自愈（因为旧值一直在）。

**根因**：`btCfg()` 的合并顺序是「默认值 d ← localStorage c 覆盖」，删掉 UI 只是让用户改不回来，不会改写已存的值。

**修法（写死成规则）**：**任何删除/改名枚举值的改动，都必须在 `btCfg()` 合并之后加一行就地压回**：
```js
d.mode = 'fixed';   // v919：real 已下线，旧配置一律回退
```
同类先例：`band` 的 v903 迁移（≤10 → 25）、`ddBudget` 的 35→20 迁移、`pool` 旧值归到「自选组合」高亮。判据：**改完必须手工往 localStorage 塞一个旧值、重载、断言被压回**，只看「新装用户正常」不算验过。

**本次实证**：塞 `mode='real'` → 重载后 `savedMode=fixed`、年化 5.08%（固定预算基准），而不是按台账口径。

## P48 · 宽表三件套：sticky 首列盖住最右列 / auto 布局压缩列宽致折行 / 行高不一致（v920）

**症状**：23 列宽表在 506px 容器里横滑时出现两个独立故障：
1. 滚到最右（`scrollLeft=max`）时，sticky 首列（`position:sticky;left:0;z-index:3`，宽 210px）压在表格内容之上，把最后一列「差异归因」左半截盖住 —— 用户滑到头也读不到归因前半句；DOM 文本完整，只有人眼看不见。
2. 某些数字（`+¥12957.61`）在指定 92px 的列里折成两行，该行高 48px、其余 10 行 30px；表格列宽在 `table-layout:auto` 下只是「权重建议」，被内容挤压后长数字就换行。

**根因**：①sticky 元素在滚动容器里固定于 left:0，它遮挡的是**滚动内容**，不是容器本身，所以「滚到最右」并不能让它让位；②auto 布局下 `td{width:92px}` 不是硬约束，等宽数字 + 加粗后 min-content 超宽即折行；③折行只在个别行发生，抽查首行看不出问题。

**修法**：
1. 宽表要么**不做 sticky 首列**（本表选择：横滑丢上下文，但不遮内容），要么给表尾加与首列等宽的空白单元格做占位；
2. 给整表加 `white-space:nowrap`（写在 `table` 的 style 上即可继承），让 auto 布局用 min-content 撑宽该列而不是折行；
3. 验收**逐行量** `tr.getBoundingClientRect().height`，断言全部等于同一值（本表 30px）；只看首行或只看 DOM 文本都不算验过。

**本次实证**：去 sticky 前 `screenshot(scrollLeft=max)` 归因列只剩尾半句；改后归因「止损清仓 · 网格×4」完整可读。折行修前 11 行 `h=[30,30,…,48,…,30]`，加 nowrap 后全 30。

**顺带（数字口径）**：`stats.buyAmt/sellAmt` 原用取整后的 `t.amt` 累加，41 笔累计误差 0.09 —— 明细表逐只求和 36,717.91 与组合级 36,718.00 对不上。凡要「逐只求和＝合计」的表，统计源必须用 `t.raw` 而不是显示用的 `t.amt`。

## P49 · 渲染函数引用回测函数内的局部变量：整页红字「回测失败：xxx is not defined」（v921）

**症状**：改完计算层，页面不是数字错、而是整块报错「回测失败：rfUsed is not defined」，`#btOut` 只剩这一句、一张表都没有。

**根因**：`rfUsed` 是 `btRun()` 里的 `var`（v899 加的无风险利率），`perFund` 同在 `btRun` 内所以能读；但脚注 ④ 写在 `renderBacktest()` 的字符串拼接里，那是另一层作用域，读不到 `btRun` 的局部变量 → ReferenceError 被 `go()` 的 try/catch 捕获成红字。

**修法**：渲染层要用回测结果里的值时，一律走 `stats`（`S.xxx`）——v899 已把利率存成 `stats.rfUsed`，写 `S.rfUsed || 0` 即可。判据：**改完必须真渲染跑一次回测**，只跑 `check_js` 不够（语法合法、运行时才炸）。同型先例：v781b 的 `fetchJson` 在另一个 IIFE 闭包内、v595 系列的 `holdRows` 未导出。


## P50 · v924 自选组合「逐只参数」五连坑（2026-11-13）

**症状**：①面板合计恒显示「合计 0%」；②`000912` 英大现金宝A / `511260` 十年国债ETF 在下拉里搜不到；③`000912` 名称列显示成代码、`511260` 档位显示「进攻」；④面板每行都标「无日频」；⑤杠铃持仓组合回测年化从基准 5.08% 漂到 5.39%、备用金从 20 笔 ¥10,000 变 25 笔 ¥12,500。

**证伪与根因**：
1. **合计恒 0%**：面板 HTML 首屏写死文本「合计 0%」，重建 DOM 后 `syncPanel` 刷的是**旧节点**（旧的已不在文档里）→ 新节点永远是初值。修：合计改为在渲染 HTML 时直接算 `sumW0/sumTxt/sumCol`，并输出到 `id="btCuPfSum"`（不依赖事后刷新）。
2. **两只选不到**：`btCustomUniverse` 只收 持仓台账 / 画像 / 自选 / 筛选 四源，这两只属**杠铃池**、不在台账 → universe 追加 `push(code,'barbell',...)`，可选池 66→68 项，来源标签多一个「杠铃」。
3. **档位判错**：`btTypePile` 里「画像 type 含『指数』→ 进攻」排在前面，把十年国债ETF 抢成「进攻」；`000912` 不在画像表则落到默认。修：把「先查 `SIGNALS_CFG.barbell.funds` 的 `pile`」提到**函数最前面**——用户显式配置的档位优先于类型推断。
4. **误标「无日频」**：首屏面板渲染早于 `btLoad`，`BT_CACHE` 还是空 → `hasSeq=false`，68 只全标「无日频」。修：`hasSeq = (BT_CACHE && BT_CACHE.rowsByCode) ? !!… : true`——**"还不知道"不能用 false 表达**。
5. **杠铃被污染**（最严重）：`go()` 无条件写 `c.pf`（自选面板的逐只参数）进 localStorage，杠铃模式复用同码标的（如 `001015` 被写成 sl 25 / bd 10）→ 年化漂移。修两处：`btPF` 里读用户值加 `cfg2.pool === 'custom'` 前置；`go()` 只在 `c.pool === 'custom'` 写 pf、否则 `c.pf = cfg.pf || {}` 保留原值（也不能写空，否则 localStorage 里 custom 的参数被清掉）。

**修后实测**（50,000 / 2021-01-04→2026-11-11）：杠铃零回归 年化 **5.09%**（基准 5.08%，差异来自数据末端日期）、**41 笔**、备用金 **20 笔 ¥10,000**、明细 11 行、`001015` 阈值仍 **−12%**（未被自选值污染）；自选 5 只 `001015` 显示 ±10%/−25%、`000912` 现金/不参与、`511260` 对冲/−8%/1.5%，明细档位 底仓/底仓/进攻/安全垫/对冲。

**教训**：①DOM 重建后确认刷新目标是**新节点**（用 id/引用校验，别信"我改了 HTML"）；②新入口的可选池必须覆盖旧入口的全部来源（"预置按钮能带进来的，下拉也必须能搜到"）；③档位/类型这类多规则抢判的函数，**用户显式配置放最前**；④跨模式共享同一 localStorage 字段，写入前必须带模式前置条件；⑤反向：读也必须带前置条件，否则另一模式的旧值会静默生效。

tag：`fw2_v924_bt_custom_per_fund`


## P51 · 卡片改表格时「派生列」不会自动刷新（2026-11-13）

**症状**：v925 把逐只参数从卡片改成表格后，改「权重 20→30」，同行的「投入¥」与「合计」仍停在旧值——只有等 260ms 防抖重跑结束、面板被重建后才更新；而重建会把正在编辑的输入框焦点打掉，等于"要么不刷新、要么打断输入"。

**根因**：`change` 处理器走的是 `rerun(false)`，只重跑 `btRun` 不重建面板；派生列（投入¥ / 占投入% / 合计）原先靠面板重渲染重算，改表格后这条路径断了。

**修法**：新增 `syncDerived()`——按内存里的 `btCuPfOf(code)` 直接改三处 DOM 文本（`[data-cu-amt]` / `[data-cu-gapct]` / `#btCuPfSum`，后者连颜色一起按 100% 三态改），表行用 `data-cu-row="code"` 定位；`change` 里先 `syncDerived()` 再 `rerun(false)`。**注意 setter 不要写成重渲染**，否则焦点丢失。

**判据**：改权重后立刻读 `[data-cu-amt]` 应为新值、`#btCuPfSum` 应在同一帧变色（实测 20→30 得 ¥15,000 / 110% 红字）。

**教训**：任何"表格里的输入框 + 同行派生数字"的组合，都要显式实现**就地刷新**；指望"重跑一次就顺带刷新 UI"的写法，一定会在"不重建 DOM"的分支里漏掉。

tag：`fw2_v925_bt_pf_table`


## P52 · 把参数 input 从抽屉搬到表格：id 复用可行，但重复渲染会读到"最后一个"（2026-11-13）

**症状**：v926 把组合级参数（备用金上限、目标年化、回撤预算、无风险利率、季度再平衡、按标的分设阈值）从「全部参数」抽屉搬进表格上方的横条，抽屉里若不删同名 input，页面上就有两个 `btIn_gridFund`。

**根因**：`go()` 用 `document.getElementById('btIn_'+k)` 按 id 取值——同名 id 返回的是**文档顺序里第一个**，而 `change` 委托只认事件目标。等于"输入框 A 被编辑、读值读到 B"，症状是"改了没反应 / 改了跳到别的值"。

**修法**：搬家时**必须让同一 id 全页唯一**。本轮用条件渲染：`pool=custom` 抽屉不渲染这 7 个 input（只留 5 个隐藏域给兜底值），`pool=barbell` 抽屉完整渲染而表格不渲染（`btCuPanelHtml` 只在非 barbell 时挂载）。

**判据**：`document.querySelectorAll('#btIn_gridFund').length === 1`；改一格后摘要行立刻跟着变。

**教训**：单文件 HTML 里"参数 DOM 搬家"最省事的做法是**保留 id 原地不动**（`go()` 与 `change` 委托都不用改），但前提是新旧位置不会同时渲染——只要有一个模式会两边都画，就必须显式条件化，否则静默读到错的那一个。

tag：`fw2_v926_bt_one_table`

## P53 · 「旧默认值迁移」每次读取都重跑 → 用户填的值被静默改回（2026-11-13）

**症状**：v926 在表格里把「备用金上限」填成 10000，摘要仍写「备用金不限额」、localStorage 里值也是 0；把「回撤预算」填 35 会变回 20。用户视角＝"这个格子改了没用"。

**根因**：`btCfg()` 里两条老迁移：
```js
if (+d.ddBudget === 35) { d.ddBudget = 20; ddMigrated = true; }
if (+d.gridFund === 10000) { d.gridFund = 0; gfMigrated = true; }
```
迁移写的是内存 `d`，标记 `d.gfMigrated` 也没落盘；而 `go()` 里 `btSave(c)` 保存的是**从 DOM 重新收集的 `c`**，不含这两个标记 → 下一次 `btCfg()` 又从 localStorage 读到 10000/35 且无标记 → 再迁一次。链路里 `btSave(c) → cfg = btCfg() → 渲染摘要` 就发生在一帧内，所以填完立刻被打回。

**修法**：v926 整段撤掉这两条迁移（无配置时 `d` 的默认值本来就是 `gridFund: 0` / `ddBudget: 20`，迁移只为老用户服务，而老用户早在 v906/v898 就迁过了）。表格里填什么就是什么。

**判据**：填 10000 → localStorage `fw2_bt_cfg_v1` 里 `gridFund` 为 10000、摘要「备用金上限 ¥10000.00」。（本轮实测：修前被打回 0，修后存住。）

**教训**：任何"读到旧默认就改写"的迁移，**必须一次性**——标记要落盘、且保存路径要带上标记；否则用户越想改成那个值，越改不上，而且没有任何报错。默认值已经是新值的字段，干脆别做迁移。

tag：`fw2_v926_bt_one_table`

## P54 · 指标接回测：预热段只能进 seq、不能进 allDays（v934）

**症状**：年线信号开关打开后，区间前约 10 个月（200 个交易日）完全不触发，看起来像"开关没生效"。

**根因**：`btRun` 里最初只取 `r.d >= start && r.d <= end` 的行建 `seq`。MA200 要 200 个点，前 200 天 `ma.l = null` 被直接跳过 —— 2021-01-04 起跑的回测，要到 2021-10 才第一次有年线。

**修法（v934 `fw2_v934_sig_year`）**：`_rowsAll = rows.filter(r.d <= end)`；`seq` 用 `_rowsAll.filter(r.d < start).slice(-260).concat(rows)` 建；`allDays` **仍只收 `rows`**（区间内）。回测区间、净值曲线、收益分母一律不变。

**验收**：2021-01-04 起跑，`511260` 应在 **2021-01-29** 就出现清仓（实测 0.07 年后清仓），而不是"整段没信号"。

**教训**：任何"需要 N 期历史"的指标接进回测，都必须单独准备预热窗口；把预热行混进交易日集合，会让区间起点悄悄前移、分母跟着变。

## P55 · 「破 20 日线清仓」对低波动档是纯伤害（v934 口径缺陷，待拍板）

**症状**：`511260` 十年国债在 **2021-01-29**（区间第 0.07 年）被 MA20 清仓，此后 5 年不回补：策略 `+0.24%` vs 对照 `+22.97%`，单只白丢 22.73pct。同一组合里 022438 / 160422 却因清仓明显改善。

**根因**：破线清仓是趋势策略，前提是"跌下去还会跌"。国债 ETF 波动 2%、长期上行，短期破 MA20 多为噪音；再叠加"清仓后不回补"，就把一次噪音变成永久离场。

**现状**：按用户「先只跑通一个信号」的要求，**不做静默修正**。三个选项待拍板：①对冲档只留 MA200 减半、去掉 MA20 清仓；②整档豁免信号（货基 `nav` 恒 1 本就不触发）；③加"重回年线之上再接回"（当前`sigOff` 置位后不回补）。

**先例**：任务 #22「债 / 短融 / 国债 W7、S3 距低点信号豁免」——同类判断已经做过一次，这里只是同一件事在新规则上重演。

**教训**：接"普惠型"规则前，先在低波动标的上单独看形状，再决定是否全档适用。

## P56 · `(function(){ … })()` 漏写调用括号 → 页面把函数源码当数字打印

**症状**：结论条出现「触发 2 笔减半 / **function () { var _e = 0; P.trades.forEach(...) }** 笔清仓」，摘要行同样。

**根因**：`stats` 对象字面量里写成 `sigExit: (function(){ … })`，末尾少 `()`，于是 `stats.sigExit` 存的是函数；渲染端 `(S.sigExit || 0)` 对函数做字符串拼接，走的是 `Function.prototype.toString`。

**修法**：补 `()` 即可（`_apply_v934_sigyear.py` 已改）。

**教训**：`check_js` 语法检查**通过**（少一对括号完全合法），只有真渲染读 DOM 才暴露。判据就是"数字位置冒出 `function (` 字样"——凡拼接数字的地方出现源码，第一件事查 IIFE 调用括号。

## P57 · 线上核验锚点不能按「运行时拼接后的显示文案」写（v934 发布）

**症状**：`_verify_online_v934.py` 断言 `MA200 破线减半 / MA20 破线清仓` 时 `count=0` → `ONLINE_V934=FAIL`，但同一跑里 `BYTE_MATCH True`、其余 8 个锚点全中、Pages 200 同字节。看着像「线上少了功能」，其实是断言写错。

**证伪**：`_probe_v934_anchor.py` 打出所有含「破线」的源码片段，结论条那段是 `'</b>：MA' + S.sigMa + ' 破线减半 / MA' + S.sigMaS + ' 破线清仓 · 触发…'`——`MA200 / MA20` 是**运行时拼进去**的，静态文件里根本不存在「MA200 破线减半」这串。

**修法**：字节断言只取**静态存在**的片段（`破线减半 / MA`、`破线期间网格与定投暂停、清仓后不回补，T+1 成交。`、`破 MA200 减半 / 破 MA20 清仓`（这句在滚动窗口注记里是硬编码的，count=2））；「拼出来的数字」（MA200/MA20、笔数）交给**真渲染读 `#btOut`** 验，别让字节断言去赌运行时字符串。

**教训**：写断言前先 `Select-String -AllMatches` 或切片实测，别凭「页面上看到的那样」直接抄。已知 v933 也踩过一次（tag 写成 `fw2_v932_drip`，实际只有 `fw2_v932`）——这是同一个病，第二次犯。


## 回测数字跨会话对不上（0.1–0.8pct 漂移）——2026-11-18 结案

- **症状**：同一套参数、同一段区间，今天跑出的年化/回撤与几天前文档记录差 0.1–0.8pct，方向还一致偏正；看起来像"引擎被改坏了"或"数据被修订了"。
- **证伪顺序（照做，别先改代码）**：
  1. 把**旧版** index.html 拷到 `edit_work/_probe.html`，`python -m http.server 8765` 起本地服务（数据走相对 `data/fund-daily.json`），用**显式全参**复跑同一段。若与今日逐位相同 → 代码无漂移，别再怀疑代码。
  2. 用 GitHub API 取旧提交的 `caifu/data/fund-daily.json`，与本地逐只逐日比 `nav/acc`（不是只比行数，行数相同但值可能被"修正"）。若 0 处差异 → 数据无修订。
  3. 剩下唯一可能：**记录那次运行的参数状态与文档写的不一样**。页面开关持久化在 `fw2_bt_cfg_v1`，残留会静默带入（v971 曾残留 `v11Bet=20`，14.7 曾出现"池0=池5"的假相等）。
- **根因**：口径不是由文档保证，而是由"那次运行的实际 cfg"决定；不显式写全就等于赌上一轮没留残留。
- **修法（固化）**：任何跑批前把 `budget/feeBps/addDD/postSellHalf/tpPeak/rebalSlot/stGate/v1Gate/v11Gate/v11Pct/v11Odd/v11Bet/v11Max/trendGate/trendBearOnly/trendBearMode/bearSlow/bearSlowB/bearBuildGate/bearSlowPct` 写全（`localStorage` 或 DOM 均可）+ 显式 `start/end`；跨会话引用绝对值前，先用同会话重测替代旧记录。
   - **机制层修法（v984 起，2026-11-18）**：运行条新增 `#btResetStd`「重置为标准口径」，一键把 `BT_DEFAULTS`（出厂默认快照，在合并 localStorage 之前捕获）+ 会话标准覆盖写回 `fw2_bt_cfg_v1` 并立即重跑；本地与线上各自「污染→点重置」双验证回到 13.67/−5.91/2.04/103。以后引用任何绝对值前，先点它，而不是凭记忆写 20 个字段。
   - **v985 追加**：旁边再加「口径预设 3/5/10 年」——切窗口也走同一个 `applyStd()`，不会再出现「只改起始日、忘改截止日」。三档跑出 13.67 / 9.25 / 5.33，与表2 逐位一致（`docs/SIGNAL_INVENTORY.md` 14.17）。
- **判读**：同一次会话内的 A/B 相对比较不受此影响；只有跨会话引用绝对数值会踩。

## P58 · verify_sync 报「[资料库] cmp 未 PASS: 」但冒号后面什么都没有（比对器缺件）

- **症状**：`verify_sync.py` 全量跑末尾只有一行 `- [资料库] cmp 未 PASS:`，下面空白，看不出是页面真不一致还是工具坏了；GitHub 端却全 OK。
- **证伪**：①`Test-Path edit_work\cmp_lib.py` → False 就是缺件；②手工 `python cmp_lib.py a.html b.html` → 直接 `No such file`；③若文件在，再看回拉文件大小（`_libpull_verify\*.html`）与本地差多少字节。
- **根因**：`lib_check` 用 `subprocess.run([PY, cmp_lib.py, ...])`，脚本不存在时 rc=2 且 stdout 为空，而旧的失败分支只把 `out[:800]` 拼进消息、丢弃 stderr → 报错等于没报。
- **修法**：①重建 `cmp_lib.py`（剥平台注入 `inject.js` / `pnid` 注释 / 节点号属性，属性排序，空白归一，逐块比）；②`lib_check` 先 `os.path.isfile` 判缺件，失败消息带 `rc`、两端字节数与 `stderr`；③判据写成「PASS / FAIL 都要说人话」。
- **顺带教训（v1034 实测）**：资料库覆盖节点别再用 `op_` token 通道（30 分钟寿命、2026-11-17 那份已报 10034），插件 5.11.3 自带 `page/import_html.py --node-block-id <id>` 走平台内部请求即可；另 `import_html._file_meta` 已拆成 `_file_size/_read_file`，老脚本要加 hasattr 兼容。本地 index.html 曾有两处孤立 span 闭合标签（从资料库回拉时平台删掉了配对开标签），会让语义比对凭空多出差异块——先 `span 开/闭` 计数，再谈页面内容差异。
- **tag**：`fw2_v1034_orphan_span`

## P59 · 浏览器核验时读到 `window.__NAV_SERIES__` / `holdRows` 全是 undefined（不等于页面没有）

- **症状**：`bu.js("typeof window.__NAV_SERIES__")` 返回 `undefined`、`Object.keys(...).length` 为 0；同一时刻页面表格里「买入最大回撤」「波动率」却都有数值。容易误判成「数据没加载 / 新列算错了」。
- **证伪**：①同一段 JS 里读 DOM（`verBadge`、表头文字）都正常，只有页面 `window` 上的属性读不到；②换 `document.querySelector` 读数值一切正常；③页面上肉眼可见的数值与按 `fund-daily.json` 离线复算一致。
- **根因**：`bu.js()` 在浏览器隔离上下文（isolated world）执行，只能共享 DOM，不共享页面主 world 的 JS 全局。页面 IIFE 挂在 `window` 上的 `__NAV_SERIES__` / `__NAV_ACC__` / `__ALLOC_NAV__` / `holdRows` 在隔离 world 里一律 `undefined`。
- **修法**：核验「页面内部数据」不要读 `window`。优先级：①读渲染出来的 DOM（表格单元格、title、innerText）；②需要原始序列就对 `edit_work/data/*.json` 离线复算，再和 DOM 数值逐只对拍；③确实要在页面里取全局，只能让页面自己把值写进 DOM/`data-*` 属性，或改用 CDP main-world 求值（`bu.cdp`），不要据此判断「数据缺失」。
- **顺带教训（v1035 实测）**：新列验收要「DOM 数值 + 离线复算」双证。本次 23 只有值逐只与 Python 复算一致（最大差 < 0.05pp），另 2 只「—」经查是现金货基与 `fund-daily` 无序列，属预期空值——若只靠 `window` 探测会误报成「整列没算」。
- **tag**：`fw2_v1035_hold_vol_col`

## P60 · 线上核验持仓「健康度」时读到「高集中」而不是「回撤深」（数据未就绪的降级，不是 bug）

- **症状**：强刷线上 `?t=v1036live` 后立刻读 DOM，012920 健康度显示「高集中」；同一份代码本地（数据已齐）显示「回撤深」。
- **证伪**：①读 `#discSum` 尾部，此时写的是「数据截至 **未更新**（行情快照）」；等 10–15 秒再读，变成具体时刻，健康度随之变「回撤深」；②该行「买入最大回撤」列同时是「—」（`__NAV_SERIES__` 未到，`r.mdd` 为 null）。两条一起出现即可判定是数据未就绪。
- **根因**：`healthOf` 的持仓质量段依赖 `r.mdd` / `r.vol`，净值序列拉取完成前它们是 null，判定自然落到下一档（高集中或正常）。属有意降级（宁可先不给结论，也不按日涨跌瞎判）。
- **修法**：核验时先等数据齐（看 `#discSum` 里「数据截至」是否已是具体时间、表格「买入最大回撤」是否已有数值），再读健康度；不要把「先高集中后回撤深」记成新口径的 bug，也不要为此改成「mdd 未知就标待核对」（那会让整列在慢网下灰一片）。
- **tag**：`fw2_v1036_health_two_tier`

## P61 持仓表横向滚动容器是 `.table-wrap`，不是 `#hdTable`

- **症状**：在 bu 里设 `document.getElementById('hdTable').scrollLeft = 0`，读回 0，但页面视觉纹丝不动、仍停在中间几列；误判成「复位没生效」。
- **证伪**：读 `getComputedStyle(table.parentElement).overflowX` → `auto`、`parentElement.scrollWidth 748 / clientWidth 483`，且 `wrap.scrollLeft` 才是真正被拖动的那一个；table 自身 `scrollWidth == clientWidth`，不可滚。
- **根因**：`.table-wrap` 承担 `overflow-x:auto`（v5xx 起为 18 列 auto 布局服务），`<table>` 只是内容块。
- **修法**：写 `#hdTable` 所在 `parentElement` 的 `scrollLeft`；v1037 的 `fw2_v1037_slim_scroll` 即按此写（切换精简列后复位到最左）。同理，任何「定位到某列」的脚本都要 beforescroll 到 wrap。

## P62 · 「1x 截图上小字被裁 / 被压扁」多半是视觉错觉，先 2x 放大再动 CSS（v1039）

- **症状**：v1038 体检在 538px 宽视口截图看到顶部 ticker 文字上沿缺 3–4px，直接判定「容器 24px + 行高 21.7px 裁切」，并已写好 CSS 补丁（`.ticker-mask` 改 flex 居中 + 窄屏 24→26px）。
- **证伪**：`bu.js` 给 `#ticker` 临时加 `zoom:2` 后再截图 → `LIVE` 四字母与中文全部完整、上下均无裁切；同时读几何 `.ticker` h=24 / `.ticker-mask` h=21.7 top=0.6 / `.ticker-track` h=17 top=4.1，17px 行盒装 11px 字体本就有余量（(21.7−17)/2 = 2.35px 上下留白）。
- **根因**：11px 字在 24px 条里只占一半高度，1x 像素下抗锯齿把上下笔画糊掉，肉眼读成「被切」——不是布局裁切。
- **修法**：撤掉该 CSS 改动、保持原布局。判「小字被裁 / 被压扁 / 行高过小导致重叠」类视觉缺陷，一律先 `zoom:2`（或临时 `position:fixed` + `transform:scale(2)`）放大取证，再决定是否动 CSS；**别**拿 1x 截图的观感直接改行高或容器高度。反向同理：`zoom` 放大后若字形超界，才是真裁切。

## P63 改含反斜杠的 JS 文本：非 raw 字符串会吃掉反斜杠、错位引号

- **症状**：打完补丁 `check_js.py` 报「1 个块语法错误」，`node --check` 输出 `SyntaxError: Invalid or unexpected token`；出错行里那段 Windows 路径命令字符串的**成对反斜杠变成了单个**，并且出现「半句 + 整句」重复、引号提前闭合。
- **证伪/定位**：把第 N 个 `<script>` 块单独落盘跑 `node --check`，打印出错行前后 6 行——重复片段与引号位置一眼可见。只盯着 check_js 打印的「块 N FAIL + 行号」看不出问题在哪。
- **根因**：①锚点里 JS 文本含成对反斜杠（Windows 路径写法），Python 普通三引号字符串把它解码成单个反斜杠，写回后 `\b` 成了退格控制字符、`\'` 成了无效转义；②`rep(old, new)` 的 old 只截到句子中段，而 new 里又抄了整句，替换后原句尾部仍在，拼成「半句 + 整句」。
- **修法**：凡改含反斜杠的文本一律用 `r'''…'''`；old 与 new 的边界要整行对齐——要么两者都是完整句子，要么 new 只补「外层包装」、不复制正文；改完立刻跑 `check_js.py`，失败就 `Copy-Item` 备份回滚后重跑，不要在坏文件上继续叠补丁。（v1041 踩到，回滚备份后重跑即修复）

## P64 组头/提示行里塞长清单：窄视口下按钮被推到横滚区外，等于没给入口

- **症状**：v1042 首版把「被折叠的 11 只基金 + 各自信号名」全拼进信号页组头一行，本地真渲染截图里文字从组头一路延伸到视口右边缘之外（表格 `min-width:1080px`、视口 540px），「展开全部 12 只」按钮排在文本末尾，**在视口内根本看不见**；同一句提示在观察档每行重复渲染一次，全表冒出 122 个 `data-sig-fam` 按钮。
- **证伪/定位**：`bu.js` 读 `.sig-fam-note` 的 `innerText` 与 `getBoundingClientRect().width`（1058px vs 视口 540px），再 `querySelectorAll('[data-sig-fam]').length` 数按钮——两个数一比就知道「信息在、入口不在」。
- **根因**：表格是横向滚动容器（P61），td 实际宽度 1058px，`white-space:nowrap` 让内容不被截断而是溢出到横滚区；把可交互元素放在长文本末尾，等于把入口藏到用户不会滚到的地方。
- **修法**：①提示只留「几只 / 只列谁 / 另有几只带动作」的短句（本项目实测 ≤60 字），完整清单放 `title` 悬停；②按钮**前置**到提示文本之前；③`opts.watchRow` 这类「同一条信息被逐行平铺」的场景要显式跳过提示，别指望 CSS 去重；④交付前必须真渲染截图 + 读几何宽度核对，不能只看 `innerText` 有内容就判断「已显示」。

## P65 Python 补丁脚本：raw 三引号前多打一个引号，会把多余引号吃进字符串

- **症状**：`_v1042_patch.py` 跑到第 3 个锚点时 `s.count(old) == 0` 报 `ANCHOR FAIL`，而该行在源码里肉眼可见存在。
- **根因**：写锚点时用了「r + 四个单引号」的写法（多打了一个分界引号），Python 把 raw 三引号之后紧跟的那个单引号当成字符串首字符，于是 old 比源码多一个前导引号，永远匹配不上；换用 raw 三双引号写法后一次通过。
- **修法**：①锚点文本含单引号时用 raw 三双引号，含双引号时用 raw 三单引号，**不要多打分界引号**；②每个 `rep()` 都断言 `count == 1` 再替换，失败立即 `sys.exit(1)` 且**不要写文件**（本轮正是靠「校验通过才写」避免了半截文件）；③失败修正后重跑整个脚本，不要在已部分写入的文件上叠补丁；④注释里也不要出现三个连续单引号，否则同样会提前闭合字符串。

## 2026-11-24 · 「重置为标准口径」点了没反应（v1082）

- **症状**：⑧-C 自选回测参数页点「重置为标准口径」，输入框不变、提示不出、存档也没变（`fw2_bt_custom` 仍 `{}`）。
- **证伪/定位**：`window.__btStd` 存在、点击确实触发；插桩 `Storage.prototype.setItem` 记录到两次写：先 `{budget:62000,start,end,band,gridFund}`（栈：`btApplyStd`），紧接 `{}`（栈：`go ← renderBacktest`）。
- **根因**：①`btApplyStd` 只写盘不 `renderBtCfgHost()`，用户看不到任何变化；②`go()` 用 `btCfg(__btScopeName || 'hold')` 取参、却 `btSave(c)` 按 `__btCfgScope`（参数页档）落盘 —— 人在 ⑧-C 点重置时两档不同，hold 档参数被写进 custom 覆盖表，等于把刚重置的项清空。
- **修法**：`btSave(c, scope)` 增显式 scope；`go()` 传 `window.__btScopeName || 'hold'`；`btApplyStd` 写盘后重画参数区并 `btToast` 回执。
- **别碰**：不要用 `__btCfgScope` 决定 `go()` 的落盘档；不要去掉 `renderBtCfgHost()` 那次重画（否则「点了没用」立刻复发）。

## 2026-11-24 · 覆盖档的「重置」写成标准值，反而破坏了「继承母版」（v1083）

- **症状**：⑧-B／⑧-C 点「重置为标准口径」后，`fw2_bt_custom` 里多出 `{budget, start, end, band, gridFund}` 五条覆盖——看着「已经等于标准口径」，实际是把这套值**钉死**在本档，母版以后改了它不跟。
- **根因（v1082 遗留的口径问题）**：`btApplyStd` 只有一条路径：组装 `cc = BT_DEFAULTS + 标准值` → `btSave(cc)`，对覆盖档就是「写 diff」，没有「清 diff」这条路。
- **修法**：`btApplyStd(win)` 按 `__btCfgScope` 分流——`plan` 走原「写标准值」；`hold`/`custom` 走「写 `{}`（带 `win` 时只写 `{start,end}`）→ `renderBtCfgHost()` → `btToast` 报清掉几条 → 重跑」，按钮名同步改「清空覆盖 · 继承母版」。
- **别碰**：非 `plan` 分支末尾的 `return`（漏了会继续往下写标准值，覆盖立刻又回来）；`win` 分支（漏了 3/5/10 年预设失效）。
- **验证口径**：造一条覆盖（本地改预算 11111 得 `{budget:11111}`）→ 点按钮 → 应得 `{}` 且输入框回母版值；点「10 年」→ 应只剩 `{start,end}`。

## 2026-11-24 · 缠论子模块的头部与图表整张消失（v1085）

- **症状**：宏观环境第 5 个 tab 点进去，头部（名称/PE/PB）不见了，图表区一片空白；`#chanChart` 量到 0×0，canvas 数 0，但 `renderChanModule()` 确实被执行、HTML 也插进了 `macroBody`。
- **证伪/定位**：DOM 里卡片都在，但前两张 `offsetHeight=0` 且 `display:none`；查样式规则发现命中宏观模块的「按区域隐藏 `.mc-mod`」逻辑——`__mcApply` 会按 region 规则隐藏第 1 张与第 4 张 `.mc-mod` 卡。
- **根因**：模块卡片沿用了宏观其它卡片的 `class="mc-mod card"`。缠论模块是独立模块、不参与宏观的区域卡片规则，被误伤。
- **修法**：模块内 6 处卡片全改 `class="card"`（彻底不给 `mc-mod`）；同时把异步数据到达后的重绘守卫改成「有 `chanChart` 或 `chanLoading` 才渲染」，避免数据回来时用户已切走/占位已替换导致空白。
- **别碰**：不要为了「跟别的卡长得一样」再加回 `mc-mod`；不要把 `__chanMount()` 放到 `renderMacro` 之外（必须在 innerHTML 落地后调用，否则 canvas 容器无尺寸）。
- **验证口径**：进 tab 后 `#chanChart.clientWidth/clientHeight` 应为非零（本地 487×520）、`canvas` 数 ≥1；切到别的宏观 tab 再切回来，图表应重建而非空白。

## 2026-11-24 · 回撤档位模块的三处「看不见」（v1086）

- **症状一（图表空）**：`#ddChart` 有 `_echarts_instance_`、zrender 根 div 在、`setOption` 无异常、容器 479×230，但 `canvas` 数 0，页面留一块 230px 空白；同页其它图 40 个 canvas 正常。
- **证伪/定位**：在 `#ddChart` 上打诊断属性（`typeof window.echarts` = object、曲线 2430 点、`setOption` 前后无 error），确认不是「没数据 / 没 echarts / 抛错」，而是 init 之后 painter 没挂上 canvas。原因未查明（同页 ECharts 用法与其它模块一致）。
- **修法**：不再纠缠 ECharts —— 改为自绘 SVG（`drawChart` 内拼 path + text）。若日后要回 ECharts，先复现本症状再改，别直接换回去交差。
- **症状二（check_js 单块报错）**：新增 HTML 注释里写了「下方独立 `<script>`」，`check_js.py` 按 `<script` 切块，把注释内容当成代码开头，块 12 报 `Invalid or unexpected token`。
- **修法**：HTML 注释里不要出现 `<script>` / `</script>` 字样（改写「脚本块」）。`<style>` 字样目前不触发，但同样建议避开。
- **症状三（整页空白，容易误判为模块不显示）**：被遮挡/后台窗口里 `#view-strategy` 计算出的 `opacity` 停在 0——`.view.active{animation:v43fade .22s}` 的 CSS 动画被浏览器暂停在首帧。
- **证伪**：`getBoundingClientRect` 有尺寸、`innerHTML` 有内容、`elementFromPoint` 命中 svg，但 `getComputedStyle(...).opacity === '0'`。
- **修法（仅核验用）**：截图前临时 `v.style.animation='none'; v.style.opacity='1'`；**不要改产品 CSS**——真实用户前台窗口动画正常。

## 2026-11-24 · 组合回测的两个小坑（v1087）

- **症状一（切「回测方式」界面没变）**：把 `回测方式` 选到「多指数组合（共用资金）」后，参数区仍显示「单指数 + 指数下拉」，chips 不出现，点运行还按单指数跑。
- **定位**：`#stp-dd` 的 change 委托只做 `window.__ddSet(k, t.value)`——它只改状态、从不重画（`code` 那条能变，是因为点行走的是另一条带 `renderDdModule()` 的分支）。
- **修法**：change 分支里 `if (k === 'scope') window.renderDdModule();`。以后再往参数区加「会改变布局的开关」，都要在同一处判断重画。
- **症状二（逐笔表日期变成 20170508）**：组合回测逐笔明细的「买入日/卖出日」打印成 8 位数字，单指数模式看着正常。
- **定位**：`ymd(s)` 用 `s.length === 8` 判断，字符串成立、整数没有 `.length` → 走进 `(s || '—')` 直接吐出数字；组合引擎的 `trades.bd/sd` 直接存 `axis[k]` 整数，单指数模式历史上也受影响但没暴露。
- **修法**：`ymd` 内先 `String(s == null ? '' : s)` 再判长度。教训：凡「可能来自 JSON 数字」的日期/代码，别对值本身取属性，先转字符串。

## 2026-11-24 · 中证官网估值只有 20 个交易日，别拿它算分位（v1088）

- **症状**：想做截图里的「PE 28.39 · 时间分位 82.52% · 数值分位 59.23%」，把中证估值文件读进 DataFrame 只有 20 行，最早的只到一个月前；换接口（`perf/index-daily-value`、`index/indexValue/queryIndexValue`）直接 404。
- **证伪**：`pd.read_excel(BytesIO(响应))` 得 `(20, 10)`、文件仅 8,192 B；同一 URL 对 12 个代码 200、`399006` 404；两个猜测接口返回 `{"status":404,...}`；akshare 1.19.3 里 `index_value_hist_funddb` 已不存在（`AttributeError`）。
- **根因**：中证官网的估值文件是**每日覆盖的快照**（滚动最近 20 个交易日），历史估值没有公开文件/接口；乐咕月频只覆盖沪深300/中证500/中证1000 三只。
- **修法（v1088 采用）**：口径分层——当前 PE/股息率用官网 20 日快照；价格分位用自家日收盘自算并**明标「价格数值分位，不是 PE 分位」**；PE 10 年分位只对有三只月频源的指数给值，其余显示灰色「—」并在卡下写明原因。**不要再尝试的路径**：东财 push2his（WAF 已拒）、上述两个 csindex 接口（404）。

## 2026-11-24 · 蛋卷分位不能冒充「乐咕 10 年分位」，两种 PE 也不能横比（v1089）

- **症状**：补 PE/PB 分位时，蛋卷 `index_eva/dj` 有现成的 `pe_percentile / pb_percentile`，眼看能一把补齐 8 只；但同一页已经有乐咕 10 年月频分位（3 只）与中证官网市盈率2（12 只），三个数放一起会互相打架——000300 蛋卷 PE 13.43、中证市盈率2 14.90、乐咕 12.64。
- **证伪**：把三方分位对拍——蛋卷 PE 65.6% / PB 19.5% vs 乐咕 10 年月频 64.5% / 20.7%，同向且差 <2pp，说明**分位口径基本一致**（可放心当分位用）；但现值差 1.5 倍量级（13.43 vs 14.90），说明**现值口径不同源**（股本/加权方式不同）。
- **根因**：分位是可比的相对位置，现值是可比的绝对倍数；把两套现值放同一列横比，会得出「传媒 PE 32.97 vs 官网 26.88」这种伪结论。
- **修法**：①页面按来源分层标注——蛋卷覆盖的 8 只写「蛋卷估值中心」，其余 5 只标 ※ 并写「中证官网市盈率2（20 日快照）、无分位」；②脚注写死「两种 PE 口径不同，不要横向比较倍数，只看同一只的分位」；③生成器 `gen_index_val.py` 里 `peSrc` 字段落地，前端据此打 ※，不靠人工记忆。
- **另记**：乐咕 `legulegu.com/api/stockdata/index-basic-pe|pb` 用 akshare 的 `hash_code` + `py_mini_racer` 生成当天 token 直连，实测 `401 invalid_token` → `429`（HTML 限流页）→ `504`，连续三次都拿不到数据 → **不要把它当备用源反复重试**，会白白耗掉时间与 IP 信誉。

## 2026-11-24 · 自建表在宽屏被 `width:100%` 拉满、列间距发散、表头贴边（v1090）

- **症状**：同一张「今日跨档提醒」在 538 窄屏看着还行，到你 1770 宽的屏幕上列与列之间空出一大片、表头挤到右边缘、行高也松——像是「表没做完」。
- **证伪**：量 `table` 的 `getBoundingClientRect().width` 与容器宽度对比：表宽 ≈ 容器宽（约 1900），且 `<col>` 只给了 `min-width` 没给上限 → 说明不是列宽写错，是「表跟着容器无限变宽」。
- **根因**：`table{width:100%; min-width:XXX}` 只理财下限，没有上限约束；宽屏时每一列按比例分掉所有剩余空间，字号 11~12px 的短文本自然显得空旷。
- **修法**（`fw2_v1090_dd_tbl`）：①统一走公共骨架 `ddTbl()`，`table-layout:fixed` + `colgroup` 像素列宽（列宽不随视口变）；②加 `max-width:1180px` 封顶，多余空间留在卡片右侧；③窄屏保留 `.dd-tblwrap{overflow-x:auto}` 横滑（与投资总纲一致，不再压字号硬塞）。**判断标准**：宽屏下表宽应为常数（本项目 6 张表都是 1180），行与行同列位置 `uniq=1`。
- **别学错**：`max-width` 写在 `table` 上而不是 `.dd-tblwrap` 上才有这个效果；写到外壳只会让滚动区变窄、表宽不变。

## 2026-11-24 · 「封顶不拉满」被用户否掉：要铺满就靠加列，别靠留白（v1091）

- **症状**：v1090 给自建表加 `max-width:1180px` 后，宽屏确实不再把列拉散，但卡片右侧留一大片空白——用户一句话打回：「投资总纲是铺满屏幕。这个也铺满全屏，但是可以加入更多的列字段」。
- **证伪**：量 `table` 与卡片宽——v1090 是 1180 vs 卡片 1458（差 278 全在右侧）；改后是 1458 vs 1458，差 0。
- **根因**：`table-layout:fixed; width:100%` 会把多余空间按比例分给各列；空间多而列少 → 空；空间多而列多 → 刚好。封顶只是把「空」换成「右侧留白」，都填不满。
- **修法**：删 max-width，改成「加列」——本项目五张表分别补到 4/10/10/10/8 列（距下档、历史最高收盘+日期、数据日、现价、今日/昨日档位、口径·数据日等），并把 `min-width` 提到列宽之和（940/1060/1220/1282/916），窄屏仍由 `.dd-tblwrap` 横滑。**判断标准**：`table宽 == 卡片内容宽` 且 `body.scrollWidth ≤ innerWidth`（页面不横溢），两者同时成立才算对。
- **别学错**：①不能把 `min-width` 写小于列宽之和（fixed 布局会压列，右对齐数字贴边）；②stale 这类长串（「⚠ 至 2025-12-31」）别塞进 130px 窄列，日期另设「数据日」列，图标只留 ⚠。

## 2026-11-24 · 「全指数」扩池：先探源，再决定能扩多大（v1094）

- **症状**：想把握手 13 只的「回撤档位」扩成真正的全指数，结果取数一半失败、另一半取到的序列停在 2016 年。
- **证伪过程**：对 60 个候选代码逐只打三类源——中证官网 `index-perf` 前 18 次返回数据、**之后整段 403**（WAF/频控，退避重试 3 次仍 403）；腾讯 `fqkline`（同一参数字符串）**整段 501 Not Implemented**；新浪 `CN_MarketData.getKLineData?datalen=6000` 对 42 只 A 股指数全部返回到当日，但**对 10 只返回到 2016-06 / 2019-01 就停**（000922/000929/000930/000931/000936/000937/000813/000949/000985/000807），对 hkHSI/hkHSTECH/usNDX 一律 null。
- **根因**：三个源各自「能拿到什么」不同，且都会**静默降级**——新浪断尾不报错、腾讯返回 501 时上层只看到异常、中证 403 与「代码不存在」返回同一形态。直接把失败的当「没这只」、把断尾的当「当前回撤」，会得到看起来正常、实际是 2016 年数据的表。
- **修法**：`gen_index_dd.py` 加两道硬判——①末点必须落在 `updatedAt` 前 7 天内，否则先补中证深历史、再补腾讯近段、仍不行才 `carry` 上一版序列（`src=carry`）；②断尾且无补源的一律**排除出池**，不写进 `indices`。前端 `stale` 行标 ⚠ 并在卡下写明「数据止于 …」。
- **教训**：扩池这种「数量翻几倍」的改动，先把**每个候选的末点日期**打出来再决定纳入，不要只看「有没有数据」。同理，任何 `src` 字段都必须能追溯到具体源名（sina / csi / tx / carry），别用「已更新」这种无法证伪的说法。

## 2026-11-24 · 拿「深历史」时，两家源各有一个会静默污染的坑（v1095）

- **症状**：把境外/断尾指数补进「全指数」池后，某只指数的 `start` 变成 `20000101`、`high` 出现在 2015-06-12 却明显偏离同类、或序列中间出现 1800+ 天空档；另一种是整条序列错一天（峰值日期比新浪/中证早一天，逐日同值率从 96.7% 掉到 0%）。
- **证伪**：①看 `index-dd.json` 里该代码的前 3 个（日期, 收盘）——出现 `20000101 / 1000.0` 就是中证官网占位行；②取同一指数的新浪/中证序列，按日期求交后统计 `|差|>0.01` 的比例——如果 0% 同值但数值整体对得上邻日，就是时间戳口径错。
- **根因**：①中证 `index-perf` 会在序列头部塞一条 `2000-01-01 / close=1000` 的占位基准行（000985、932000、931775、931151 等均有），它既不是真实交易日也不是真实收盘；②雪球 kline 的毫秒时间戳是「UTC 16:00 ＝ 次日 0 点 CST」，用 `gmtime`/`utcfromtimestamp` 取日期会整体前移一天。
- **修法**：`csi_series()` 丢弃 `tradeDate <= 2000-01-01`；雪球日期一律 `datetime.fromtimestamp(ts/1000 + 8*3600).date()`；`merge()` 前先算重叠同值率（`|差|>0.01` 的比例 `>10%` 拒合并）。雪球还必须先 `GET https://xueqiu.com/` 拿 cookie（不拿直接 400）。
- **tag**：`fw2_v1095_dd_overseas`

## 2026-11-24 · 「补源」先证伪再动手：三条路全是假可用（v1096）

- **症状**：想扩境外（日经225/DAX/KOSPI）、想补 7 只无源估值、想接汇率让境外进组合池——每个方向都能搜到「某 API 有数据」的说法，实际全部拿不到可用序列。
- **证伪（本轮实测，2026-11-24）**：
  1. 雪球符号：`.N225`/`.GDAXI`/`.KS11` 各 0 根；`NKY` 有 1173 根但末值 17.92（是只股票，不是日经指数）——**看到「有根数」不代表是指数**。
  2. 东财 `push2.eastmoney.com/api/qt/stock/get`：连 `1.000300`（已知可用代码）也 `RemoteDisconnected`。
  3. 中证估值 xls（`stock_zh_index_value_csindex`）：本轮 403，**连此前取过的 000300 也 403** → 是限频/封禁，不是代码不存在；隔几分钟重试仍 403。
  4. 汇率：FRED `fredgraph.csv?id=DEXCHUS` 超时、`DEXHKUS` 断连；雪球 `USDCNY/USDCNH/HKDCNY/FXUSDCNY/FX_USDCNY` 全 0 根；新浪 `fx_susdcny`/`fx_shkdcny` 返回 `null`；腾讯 `param=USDCNY,day,,,3000` 回 `param error`；stooq 回 HTML 不是 CSV。
- **根因**：这些源要么本就不覆盖该标的（雪球无日经/DAX/KOSPI 指数），要么对本机 IP 限频（中证、东财）。「有 API 文档」≠「现在能取到」。
- **修法**：扩池/补估值/接汇率前，先跑一次单请求探源并记录「根数 + 起止日 + 末值」；0 根或不合理末值就判死，别接进生成器。等源恢复再重试同一请求（中证估值优先试 931637、000823）。
- **tag**：`fw2_v1096_dd_search`

## 2026-11-25 · 策略子页 KPI 用 `.sh-grid` 被 320px 最小高度撑出大片空白（v1121）

- **症状**：V11 狙击页顶部 5 格 KPI 下方一大片空白（用户截图「这个面积太大了」），5 个格子自己只有 59px 高，卡片却被撑到 320px。
- **证伪**：量 `#stp-v11` 的 KPI 容器：`gridTemplateColumns` 是 5 列没错，但容器 `height≈320`；往上查祖先 `#view-strategy .sh-grid` 带 `flex:1 1 320px`，而 `.dc-card{display:flex;flex-direction:column}` 让它成为纵向 flex 子项 → **不是 KPI 格子高，是容器吃了 `flex-basis:320px` 的剩余空间**。
- **根因**：复用了「深跌买入」的 `sh-grid` 体系；那套网格在 `#view-strategy` 下是「可伸缩填充」，V11 策略卡又是纵向 flex，于是 5 个小格子被放在 320px 高的容器里，下方全空。
- **修法**（`fw2_v1121_v11_run_kpi`）：V11 专用 `.v11-kpi`——`display:grid; grid-template-columns:repeat(5,minmax(0,1fr))`，`.v11-kpi .sh-cell{min-height:0;padding:8px 10px}`，`@media(max-width:767px)` 2 列且末格跨两列。实测 1430 宽 5×216.53px、行高 58.85px、策略卡总高约 229px；532 宽 2×231px。**别学错**：不要在 `#view-strategy` 里直接改 `.sh-grid` 的 `flex`（深跌买入/其它子页共用）；不要只给格子设 `height`，容器仍会被 flex-basis 撑开。

## 2026-11-25 · ECharts canvas 在截图/CDP 管线里「有像素但截不到」（v1121）

- **症状**：V11 运行回测的 ECharts 图在页面上肉眼可见，但 `bu.screenshot` 与 CDP `Page.captureScreenshot` 都截成整块空白；DOM 检测 canvas 有像素（蓝色 1,437 / max alpha 255）。
- **证伪**：`elementFromPoint` 命中 canvas、祖先 `opacity=1/visibility=visible`、无 CSS 遮挡；换 `echarts.init(el,null,{renderer:'svg'})` 仍回落 canvas（该构建可能不含 SVG painter）→ 说明不是布局/图层，是 **canvas 合成不进截图管线**。
- **修法**：`v11DrawChart()` 直接拼原生 `<svg>`（蓝色账户总资产实线 + 橙色持仓市值虚线 + 5 档 y 轴 + 6 个日期刻度 + 顶部图例），不依赖 ECharts；改后 1430/532 截图均可见。**判断标准**：截图里必须能数出折线、坐标刻度和图例；只测 canvas 的 `getImageData` 不算交付验证。
- **别学错**：不要为了截图去改页面 `opacity`/`z-index`；不要相信「canvas 有像素」作为可见性证据；本项目 V11 运行回测的图已固定走 SVG，别再改回 ECharts。

## 2026-11-25 · 新增发布数据文件被 `data-mgmt` 审计硬卡（v1121）

- **症状**：`push_gh_v39.py` 报 `publishedDataFiles=41 unregistered=['data/v11-bt-data.json'] ... FAIL=True`，并明确「v891 数据管理登记审计 FAIL，拒绝发布」；页面与数据都改好了，就是发不出去。
- **证伪**：`_audit_dm_v845.py` 的 `unregistered` 只列这一个文件；`data-mgmt.json` 里搜不到 `v11_bt_data`；`_gen_data_mgmt.py` 的 `DMCONFIG` 也没有该键。
- **根因**：v891 起 data-mgmt 审计是发布链无条件硬卡：凡进 `push_gh_v39.py` 的 `caifu/data/*.json` 必须在 `_gen_data_mgmt.py` 的 `DMCONFIG` 有登记、并重建 `data-mgmt.json`，否则 `publishedDataFiles` 与登记清单对不上。
- **修法**：在 `DMCONFIG` 补条目（`key='v11_bt_data'`、`file='data/v11-bt-data.json'`、`freq='日'`、`track='手工轨（未挂链）'`、`src`/`script`/`verifier`、`time=['meta','asOf']`）→ `& py _gen_data_mgmt.py` → `& py _audit_dm_v845.py`（期望 `FAIL=False`、`unregistered=[]`）→ 重跑 `push_gh_v39.py`。**不要**用 `SKIP_GATE=1` 绕过审计硬推数据文件。

### P-v1122 V11 赔率两套公式（p250/3×ATR vs 1260 日窗口最低收盘）

- **症状**：同一只 ETF 在扫描表里的 `odds` 与配置回测 V11 的触发不一致；V11 页面文案说「前高空间/回撤腿」，注册表却写 `(前高250−nav)/(3×ATR14)`。
- **证伪/根因**：扫描 `bt_signal.entry_signal` 与运行回测 `v11Prep()` 都用 1260 日窗口最低收盘；`v11Gate` 是后建的回测分支，留在 `p250/3×ATR14` 旧口径，另加 `leg20/leg60` 实验键。门限 2.5 相同、分母不同 → 触发数不同。
- **修法**：v1122 在配置回测里新增 `p1260/lo1260` 单调队列（前 1260 根、不含当日），`v11Gate` 改 `(p1260−nav)/(nav−lo1260)`；`_SNP.den` 固定 `leg1260`，旧三档退役；注册表/参数说明/逻辑清单同步改口径，旧 3×ATR 收益数字标历史。tag `fw2_v1122_v11_formula_unified`。
- **验证**：离线复算末日赔率 159949 3.466463 / 513050 30.300000 / 513180 14.580645 / 510300 1.128902 / 588000 1.879310，与 `data/v11-signal.json` 逐位一致；`check_js`/`check_globals`/`verify_strategy_sync`/`verify_manifest`/`_audit_plan_merge_v895` 全 PASS。
- **坑**：配置回测 V11 分支要 `window.SCREEN_POOL` 已加载才有点位；若只在策略页跑，筛选池没加载 → `_SNP.list` 空、V11 零交易，别误判成公式没接线。`p250` 不能删，V2/M6/T7 还在用。

### P-v1123 「聪明的钱」被插到标签组之前（模块组像被埋进表格）

- **症状**：点「交易信号 → 聪明的钱」，页面顶部是阈值来源，紧接着直接出现「我的持仓 ETF 动向」「国家队宽基 ETF 动向」；七个页签与「全部 / 只看有动作 / 只看接近」筛选条被推到两张表后面，首屏看不到模块组。
- **证伪/根因**：`#sigBody` 的 DOM 顺序实测为 `dc-src → view-smartmoney → dc-note(V11 提示) → v-tabs → sigLvlBar → …`。`renderSignalDash()` 搬移 `#view-smartmoney` 时用 `body.querySelector('.dc-note')` 找页尾，命中的却是正文里的 V11 迁移提示（同样带 `.dc-note`），于是整节插到了标签组之前。标签组没消失，只是被压到后面。
- **修法**：页尾脚注加 `id="sigFootNote"`；锚点改为 `#sigFootNote`，兜底取最后一个 `.dc-note`。tag `fw2_v1123_sm_insert_anchor`。
- **验证**：`view-smartmoney` 的 `previousElementSibling` 为 `sigThroughPane`、`nextElementSibling` 为 `sigFootNote`；标签组与筛选条的 top 均小于 `view-smartmoney`；532 视口真渲染可见阈值来源 → V11 提示 → 七标签 → 筛选条 → 聪明的钱表头/17 行；切「趋势策略」时 `display:none`、切回恢复。
- **坑**：`.dc-note` 是通用提示类，不是页尾专用；任何「取第一个 `.dc-note` 当页尾」的写法都会复发。加提示条时不要给页尾锚点改名。

### P-v1124 数据管理 45 vs 47 仍全绿 / last-sell 审计与生成器口径打架

- **症状**：数据管理页只显示 45 项骨架，生成器实际 47 项；`_audit_dm_v845.py` 却 `FAIL=False`。同时发布链被 `_audit_last_sell_link.py` 的 012920 两源日期/净值差异阻断，但生成器明确允许「T16 卖出后破位减半冲突以账户确认为准」。
- **证伪**：`_audit_dm_v845.py` 打印 `frontN=45 genN=47 sameKeys=False driftKeys=0`，`FAIL=False`——key 集合不同但无同名键值漂移，旧审计只查了 `driftKeys`。last-sell 侧 012920 同一笔 qty=1621.57，台账申请日 11-05/nav 3.1699/amt 5120.84，账户确认日 11-25/nav 3.0228/amt 4877.17，审计却要求逐值相等。
- **根因**：①前端兜底 `DMCONFIG` 漏登 `logic_state` / `v11_bt_data`；②`_audit_dm_v845.py` 的 `_fail` 漏判 `sameKeys`；③last-sell 审计把「两源逐值相等」当硬卡，与 `gen_last_sell.py` L21-22 的既定口径自相矛盾。
- **修法**：①前端 `DMCONFIG` 补两项，45→47；②`_audit_dm_v845.py` 增加 `keyDiff` 并把 `keys_drift` 硬卡，`sameKeys=False` 必须 FAIL；③`_audit_last_sell_link.py` 改为 `crossCheck` 字段真实性 + 份额守恒 + 锚完整 + 时效仍 FAIL，nav/date/amt 差异降为 WARN；④补 `SCRIPT_TO_DM` 映射，`refreshFailed` 修正为 `['fund_jjcc','index_daily']`。
- **验证**：`_audit_dm_v845` → `frontN=47 genN=47 sameKeys=True driftKeys=0 FAIL=False`；`_audit_last_sell_link` → `FAIL=0 WARN=4`（012920 三条差异如实列出）；`_verify_online_v1124.py` → `ONLINE_V1124=PASS / FAILS=0`；线上数据管理展开 47/47，失败项 2 行可见。
- **坑**：`driftKeys=0` 不等于 key 集合一致；`sameKeys` 必须单独判。`refreshFailed` 只放真实上游/生成失败，审计脚本自身报错、口径 WARN、已补回的瞬断都不算。上游失败保留旧值是设计行为，手改 `data/*.json` 会让审计与页面再次失真。

### P-v1125 配置回测开着 V11 狙击却跑出 0 笔（筛选池未就绪）

- **症状**：配置回测开着 V11 狙击，点「运行回测」正常出结果，但 V11 狙击是 0 笔，页面无报错；`window.SCREEN_POOL` 为空或只加载了一部分。
- **证伪**：在 `go()` 里读 `window.__btDbgGo`（临时探针）会看到 `cV11=true / cfgV11=true / sp=false`；`#btOut` 停在「正在跑组合模拟…」。完成后 `res.trades` 里没有 `src='狙击池'` 的成交。用 `window.SCREEN_POOL=null` 复现最稳。
- **根因**：`btEnsureScreenPool()` 只有 fire-and-forget，没有完成回调；配置回测 `_kick()` 直接 `btLoad()`，不检查 `SCREEN_POOL`。池为空时 `_SNP.list=[]`，V11 分支静默空跑，结果看起来「正常」。另外 `{funds:{}}` 是 truthy，旧判据会把空对象当「已就绪」。
- **修法**：`btEnsureScreenPool(cb)` 增加 `._wait` 回调队列，就绪判据要求 `funds` 至少 1 只；`_kick` 开头守卫：V11 开着且池为空/空对象 → 显示「V11 狙击需要先加载筛选池」→ 加载成功 `setTimeout(_kick,0)` 续跑，失败显示红色拦截卡并 `return`。提示不受旧快照 `force` 限制。tag `fw2_v1125_sp_wait`。
- **验证**：失败路径 `SCREEN_POOL=null` + 拦截请求 → 红色拦截卡、`__BT_SP_LOADING=false`、不进入回测；成功路径 → 自动加载 40 只并续跑，完成 245 笔 / 狙击池 154 笔（首笔 2021-01-27 001198 ¥625）。`check_js` / `check_html_comments` / `check_globals` 全过。
- **坑**：①旧快照存在时若仍用 `if (force || !(_snap && _snap.html))` 包住守卫提示，用户点运行会毫无反馈；守卫提示必须无条件覆盖。②续跑不要用 `requestAnimationFrame`：自动化/被遮挡标签页 rAF 会暂停，测试会误判「守卫没执行」；用 `setTimeout`。③截图全白不是页面坏了：被遮挡窗口的 `.view.active` 入场动画停在 `opacity:0`，需强制 `animation:none / opacity:1` 再截。④失败后 `__BT_SP_LOADING` 必须复位，否则下一次点击会被加载中判断吞掉。

### P-v1126 只刷宏观组却把数据管理旧失败清成 ok；`MACRO_SNAP` 静默改 index 字节

- **症状**：`verify_nky` 实时价 FAIL 想只刷宏观，跑 `python refresh_all.py --only macro --no-publish` 后 `data-mgmt.json` 的 `refreshFailed` 变成只有 `['macro_extra']`，原来的 `fund_jjcc` / `index_daily` 两项变成 `ok`；`index.html` 字节数也变了，徽标却仍是上一版。
- **证伪**：看 `data-mgmt.json` 的 `refreshFailed` 与逐项 `refreshStatus`——若 `fund_jjcc` / `index_daily` 明明上游仍失败却显示 `ok`，就是 `DM_FROM_CHAIN=1` 只喂了本次 macro 组的失败集。对比 `index.html` 与发布前备份，差异只在 `window.MACRO_SNAP` 一行。
- **根因**：①`_gen_data_mgmt.py` 在 `DM_FROM_CHAIN=1` 时只认本次链的 `REFRESH_BAD_STEPS`，未继承其它组的旧失败；②`refresh_mkt_snap.py` / `_rebuild_macro_snap.py` 会把最新宏观快照写回 `index.html`，属于数据链正常行为，但会改字节，不升版就出现「徽标旧、内容新」。
- **修法**：①用 `DM_FROM_CHAIN=1 REFRESH_BAD_STEPS='gen_fund_jjcc.py;gen_index_bench.py;gen_macro_extra.py'` 重建，保持 `refreshFailed=['fund_jjcc','index_daily','macro_extra']`；②本轮把徽标升 v1126 + tag `fw2_v1126_macro_nky_refresh`，只声明数据刷新，不改计算/信号；③发布前把 `index/macro/meta-bundle/data-mgmt/nav-hold` 一起看 diff，`nav-hold` 也由 `gen_nav_hold.py` 从 fund-daily 重建（24 只 / 33,797 行 / `missing=[]`）。
- **验证**：`data-mgmt` 47/47、`sameKeys=True`、`driftKeys=0`、`FAIL=False`；`data-mgmt` 26,255 B；`NKYCHECK=PASS`（但 `nky_live_cross` 因独立源 `RemoteDisconnected` 按本地底线降级，是降级 PASS）；`gate.py --datasets macro,nky,manifest --check` 三组 PASS；发布 master `592a65ec967e` / index 5,372,746 B / `verify_sync --gh-only` PASS；线上徽标 v1126、nky 57,498.94。
- **坑**：①`refresh_all --only macro` ≠「只动 macro-data」，它还会改 `index.html`、`data-mgmt`、`meta-bundle`、`nav-hold`；②Pages CDN 有传播延迟，发布后首次检查可能仍是旧字节（本轮约 3 分钟），先看 GitHub 字节而不是页面；③nky 是单源 `sina` 实时值，独立源不可达时是降级 PASS，不要说成双源确认；④`gen_macro_extra.py` 缺 `akshare` 仍 rc=1，`macro_extra` 失败要如实保留。

### P-v1127 持仓信号按市值排序：别把 T10 汇总和同指数合并组当单只金额

- **症状**：把「持仓信号」标目改成按持仓金额降序后，第一项变成 `T10 杠铃档位（四档）`（它不是基金，没有市值），或同指数合并组（如 12 只纳指100 只剩 1 只代表）按代表自身 98 元排在很后面，但家族合计约 690 元，看起来「排序不对」。
- **证伪**：看 `state.portfolio` 里没有 `T10` 这个 code；合并组的 `famHidden` 成员仍在 `targets` 里，但当前只渲染代表。排序若用 `T10`/代表自身金额，就会得到上述结果；这是口径问题，不是排序函数失效。
- **根因**：`T10` 是组合汇总合成目标，不是单只基金；同指数合并组是「一个指数家族只显示一只代表」，显示金额天然不等于家族合计。
- **修法**：本轮明确口径——`T10` 保持置顶；同指数合并组按**所显示代表基金自身市值**排，不按家族合计；只用 `state.portfolio` 的 `mvCny`/`mv`/`marketValue`，按 6 位代码汇总，禁手填。若用户要「无信号兜底沉底」或「同指数组按家族合计排序」，另开一版改合并选择/组位，不要在本排序函数里悄悄改。
- **验证**：本地 `?t=v1127test&final=1` 真实 DOM 顺序 `T10 杠铃档位（四档）`（汇总置顶）→012920 5,412.79 → 活期宝 2,843.63 → 001015 2,069.72 → 160422 1,347.88 → 000307 1,073.14 → 022438 445.26 → 012761 397.84 → 023917 391.12 → 020712 319.91 → 000746 190.61 → 019441 98.25 → 017641 18.94；截图 `D:\Temp\v1127_hold_order.png`。`check_js` / `check_html_comments` / `check_globals` / `verify_strategy_sync` / `verify_manifest` / `verify_sync --gh-only` 均 PASS。
- **坑**：`_mvByCode` 只读 `state.portfolio`，不要改成读 `data/*.json`——`state.portfolio` 已是 `holdRows` 同源的人民币市值；活期宝 000912 是无信号兜底，按市值排会到第二位，这是该口径的正常结果，不是错行；自选/筛选/市场组不套用本排序。

### P-v1128 现金/货基兜底卡：用宽泛「现金」正则会误伤现金流基金

- **症状**：隐藏活期宝后，`华夏国证自由现金流ETF发起式联接A`（023917）也从持仓信号消失，或它本来有信号却变得不稳定。
- **证伪**：看 `state.portfolio` 里 023917 的 `name` 含「现金流」但不含「货币/活期宝/现金宝」，且 `assetType` 不是 `cash`；再看 `ddByCode` 里 000912 的 `kind` 是 `money`。若两者被同一正则命中，就是正则过宽。
- **根因**：`_cashHold` 若写成 `/现金/`，会把「现金流」「现金分红」等权益基金误判为现金类；它们不是货基，不能从信号里删。
- **修法**：只用 `assetType==='cash'` + 名称 `/货币|活期宝|现金宝/`，再合并 `ddByCode[code].kind==='money'`；`ddKeys` 在补空标目前过滤，保留真实有信号的基金。
- **验证**：本地 `?t=v1128test2&final=1` 持仓组 `活期宝`/`000912` 命中 false，023917 仍在；线上 `?t=v1128live&final=1` 徽标 v1128，首屏 T10 汇总→012920→001015→160422→000307，无活期宝；截图 `D:\Temp\v1128_online.png`。
- **别碰**：`signalEvalAll` 判定、`byCode` 行序、表内行序、自选/筛选/市场组；活期宝在「我的持仓」仍需正常显示；T10 三态关闭不属本版。

### P-v1129 对账卡把确认市值算成 0：`state.portfolio` 的份额字段是 `qty` 不是 `shares`

- **症状**：第一版 `#hdRecon` 显示「确认份额×净值 ¥0.00」，闭合差变成 +18,067.09，看起来像账户总资产多出一整个组合。
- **证伪**：在页面读 `state.portfolio[0]`，有 `qty` / `mvCny` / `nav`，没有 `shares`；而 `HOLDINGS_SEED.holdings[0]` 有 `shares` / `marketValue` / `pendingBuy`。`holdRows()` 的口径是 `qty×nav`，不是 `.shares`。
- **根因**：`state.portfolio` 经 normalize 后字段名改为 `qty`；`holdReconData()` 直接读 `.shares` 得到 `undefined`，`Σ(undefined×nav)` 归零。
- **修法**：`holdReconData()` 优先读 `HOLDINGS_SEED.holdings` 原始行，`state.portfolio` 只在种子缺失时兜底且用 `qty`；确认市值按 6 位代码汇总，不把 `T10` 汇总当单只。修正后恢复 18,067.10 / 20,565.55 / 2,498.46。
- **验证**：本地 `?t=v1129test3&final=1` 与线上 `?t=v1129live&final=1` 均显示闭合差 0.00；`check_hold_consistency` C 项 PASS；18 行差异表 012920 首行 −4,870.71；截图 `D:\Temp\v1129_online_recon.png` / `_table.png`。
- **坑**：①`holdings.marketValue` 合计 15,688.38 不是组合市值，不能与 total 直接对拍；②012920 的 −4,870.71 是卖出后份额未重建，不是页面计算错，必须等新对账单跑 `rebuild_holdings.py`；③不要在 `renderHoldings()` 里重复计算一套市值，仍以 `holdRows()` 为唯一市值口径。


### P-v1130 资金口径条 `fmt is not defined` 与第 4 个 chip 被裁

- **症状**：`#capCaliber` 在本地 `?t=v1130test` 为空；换 `v1130test2` 后条出现，但 538 视口第 4 个 chip「回测」被切掉；再换 `v1130test3` 才完整。
- **证伪**：控制台报 `fmt is not defined`，说明 `renderCapitalCaliber()` 调了全局 `fmt` 但该函数所在 script 块作用域看不到后面的全局声明；看 `.capital-caliber` 的 computed `overflow-x` 为 `auto`、`white-space` 为 `nowrap`，内容宽超过 529px。
- **根因**：①`fmt` 是后面另一段 script 的全局函数，当前块不可见；②口径条第一版用 `overflow-x:auto; white-space:nowrap`，四 chip 横向排不开。
- **修法**：①在 `renderCapitalCaliber()` 内定义局部 `money()`，用 `toLocaleString('zh-CN')` 格式化，不依赖全局 `fmt`；②`.capital-caliber` 改 `flex-wrap: wrap`，去掉 `nowrap` 横向裁切。
- **验证**：538 视口高 61.39px、四 chip 全部显示；`signal/strategy/data/capbal/holdings` 五页均有 `#capCaliber`，5 个子节点（1 lead + 4 chips）；截图 `D:\Temp\v1130_cap_top3.png`。
- **坑**：不要把 `renderCapitalCaliber()` 挪到全局 `fmt` 所在的 script 块——它会依赖 `HOLDINGS_SEED`/`SHOWVIEW` 的加载时序；局部 `money()` 是最小改法。

### P-v1131 四桶偏离带取错：`band` 是 R7 单只 25pp，`slotBand` 才是 T10 四档 5pp

- **症状**：第一版四桶卡显示底仓 −21.4pp 却标「结构在带内」，脚注写「结构偏离带默认 ±25pp」。进攻/主题 +28.3pp 才告警，安全垫 +6.1pp 与对冲 −13.0pp 都被判在带内。
- **证伪**：页面读 `barbellActual().cfg`，`band=25`、`slotBand=5`；`band` 是 R7 单只再平衡阈值，`slotBand` 是 T10 四档偏离带。四桶是四档，不是单只。
- **根因**：`bucketCardHtml()` 第一版写 `var band = Number(act.cfg.band) || 5;`，变量名相同但语义不同，25 覆盖了 5。
- **修法**：改为 `var band = Number(act.cfg.slotBand) || 5;`，并加注释「T10 四档偏离带，不是 R7 单只 band」。
- **验证**：四格全部标「结构偏离 ≥5pp」；脚注 ±5pp；仍不触发 T10 再平衡。截图 `D:\Temp\v1131_bucket2.png`。
- **坑**：`band` 与 `slotBand` 在别处「双向写同值」是历史遗留，不能据此认为两者等价；四桶卡必须读 `slotBand`。

### P-v1133 五万卡与六万二表标题并排：不标口径就会被读成同一笔钱

- **症状**：v1132 线上策略页，四桶卡写「策略目标 ¥50,000 / 到位 35.3%」，紧接下方资产配置表标题写「计划 ¥62,000」；两个数都没有解释，用户会问「到底按 5 万还是 6 万 2」。
- **证伪**：`STRATEGY_SNAP.totalTarget=50000`；表标题取 `fw2_capital_budget_v1` 预算输入 62,000；两者不是同一条链，但同屏相邻。
- **根因**：5 万是策略主基准，62,000 是资产配置表自己的计划拆解预算；审计阶段已把「5 万是否唯一主基准」列为待拍板，v1132 第一版只写了「5 万策略目标」，没有提示 62,000 的存在。
- **修法**：v1133 在两卡脚注加显式拆分：「金额到位分母＝5 万策略主基准（是否唯一主基准仍待拍板）；下方资产配置表标题的预算金额若不同，那是该表自己的计划拆解口径，不能与本卡 5 万到位率对拍。」新钱路线同步写「路线分母同为 5 万，若改用表标题预算需重算」。
- **验证**：线上 `?t=v1133live&final=1` 两段脚注可见；四桶/新钱数值未变；表标题仍 62,000，未被单边改成 5 万。
- **坑**：v1133 时未拍板，不要单边改数；2026-11-26 用户已拍板改成 50,000，v1134 用一次性迁移处理（只认恰好 62000），详见 P-v1134。别把 5 万写死进 `rulesBudget()`，也不要覆盖其他自填预算。


### P-v1134 只改代码默认，62,000 预算仍在：localStorage 才是表标题真源

- **症状**：按用户要求把表标题改成 50,000，先改 `rulesBudget()` 默认或 placeholder，刷新后标题仍显示 62,000。
- **证伪**：`localStorage.getItem('fw2_capital_budget_v1')` 返回 `62000`；`rulesBudget()` 有值就直接返回该值，代码默认 0 根本不会生效；`#stratBudgetIn.value` 也是 62000。
- **根因**：62,000 是用户此前在标题输入框输入并持久化的用户值，不是代码常量；`fw2_v935_nobudget` 之后代码默认是 0（未填回退 `STRATEGY_SNAP.totalTarget=50000`）。
- **修法**：在 `RULES_KEY` 定义后加 `budgetMigrate50000` IIFE，仅当值恰好 `62000` 时写回 `'50000'`；不要放进 `rulesBudget()` getter（每次读取都会写 localStorage）；不要无条件改成 5 万，否则会覆盖 55000/80000 等自填值；清空输入仍保留 `rulesSaveBudget()` 删键语义。
- **验证**：本地 62000 → 强刷 → 50000；55000 → 强刷 → 仍 55000；线上 `?t=v1134live&final=1` 徽标 v1134、`localStorage=50000`、表标题「计划 ¥ 50000」、四桶目标 ¥50,000，两卡脚注「已拍板」。截图 `D:\Temp\v1134_budget_50000.png` / `D:\Temp\v1134_online_budget.png`。
- **坑**：第一次为了测试迁移在迁移代码里挂 `window.__BUDGET_MIGRATED_50000__`，`check_globals.py` 立即 FAIL（新增未登记全局键）；已删掉，改由 localStorage 值观察结果。


### P-v1135 按值迁移没有守卫：用户主动设回 62000 会被再次改掉

- **症状**：v1134 迁移后用户在标题输入框把预算改回 62000，刷新一次又变 50000。
- **证伪**：`budgetMigrate50000` 每次加载都执行，只判断 `localStorage.fw2_capital_budget_v1 === 62000`，没有记录「已经迁移过」。
- **根因**：把「一次性迁移」写成了「每次加载按值归一」，无法区分历史旧值 62000 与用户主动设置的新 62000。
- **修法**：加 `fw2_budget_migrated_50000_v1` 标记；标记为 `'1'` 直接 return；未标记时才检查并迁移，迁移后写标记。不要把这个标记写进 `fw2_capital_budget_v1`，也不要让 `rulesBudget()` getter 承担迁移。
- **验证**：清标记 + 62000 → 刷新 → 50000 + 标记 1；标记 1 + 62000 → 刷新 → 保持 62000；恢复 50000 → 刷新 → 50000。线上 `?t=v1135live&final=1` 徽标 v1135、`localStorage=50000`、标记 1、表标题 50000。截图 `D:\Temp\v1135_budget_50000.png` / `D:\Temp\v1135_online_budget.png`。
- **坑**：不要因为「已经迁移过」就删守卫判断；删掉后用户以后每次设 62000 都会被静默改回 50000。


### P-v1136 9 列状态表把卡片撑破：538 视口只能看到左 3 列，执行/操作列不可达

- **症状**：v1136 在 538×643 视口打开交易信号页，表格只显示「信号 / 当前值 / 阈值」，右侧「状态 / 执行 / 行动方案 / 数据日 / 来源 / 操作」看不到；页面本身也不能左右滑。DOM 里执行按钮存在，但用户点不到。
- **证伪**：`document.body.scrollWidth=529`、`innerWidth=529`（页面没有横向滚动空间）；`.dc-card` 实测宽 1212px、`.table-wrap.clientWidth=1180`，均大于视口；`#sigLvlBar.getBoundingClientRect().x` 为负值；`window.scrollTo(600,0)` 后 `scrollX` 仍 0。说明不是“用户没滑”，是卡片被内容撑宽后又被视口裁掉。
- **根因**：`.dc-grid` 的网格项默认 `min-width:auto`，其最小内容宽度被 `table{min-width:1180px}` 顶到 1180；`.dc-card`/`.dc-body` 逐层被撑开，`.table-wrap{overflow-x:auto}` 因自身 clientWidth 已等于内容宽而永远不会出现滚动条。表格的 `min-width` 是必要的（列宽固定），错在容器没有 `min-width:0`。
- **修法**：`.dc-card{min-width:0}`、`.dc-card .dc-body{min-width:0}`、`.sig-wt-area{min-width:0;max-width:100%}`、`.table-wrap{max-width:100%}`。这样 `.table-wrap` 被父级约束到 449px，`scrollWidth=1180`，横滑成立；再加移动端提示 `.sig-scroll-hint`「左右滑动表格查看：状态 / 执行 / 行动方案 / 数据日 / 来源 / 操作」。
- **验证**：修后 `wrap.clientWidth=449 / scrollWidth=1180`；`scrollLeft=330` 截图可见「行动 / 待执行 + 开始」；`scrollLeft=max` 截图可见「行动方案 / 数据日 / 来源 / 知道了」；线上 `?t=v1136live&final=1` 同口径；截图 `D:\Temp\v1136_online_tablemid.png` / `v1136_online_tableright.png`。
- **坑**：①不要再给 `.table-wrap` 加固定宽度或用页面级横滚兜底——body 只有 529，滚不动；②不要只给 `.table-wrap` 加 `overflow-x:auto` 而不加 `min-width:0`，网格项仍会被最小内容撑开；③以后再加列，先量 `.dc-card` 是否 ≤ 视口、`.table-wrap.clientWidth < scrollWidth`，再看表头，不能只看 DOM 有按钮就判“可用”。

### P-v1137 同日冲突面板写 21 组、页面只有 13 个置灰按钮：不是丢条，是折叠组

- **症状**：v1137 筛选条写「同日冲突 21 组」，面板 summary 写「当前待让位 21 条（含折叠组）」，但 `document.querySelectorAll('.sig-exe-btn[disabled]').length` 只有 13；用户容易以为 8 条冲突信号没渲染。
- **证伪**：21 是 `ACT_CONF` 的组数（同一 `pool|code|name` 同组），13 是当前**默认展开**行里可见的 disabled 按钮数；同指数合并/观察折叠组内的 T13 行已写入状态和冲突图，只是默认折叠，点组头「展开全部 N 只」就能看到。用 `ACT_CONF` 逐组 `items.length` 求和可复现 21 组 / 25 个 `sig-prio` 徽标，说明不是丢行。
- **根因**：`actConflictMap` 按目标聚合，不按“当前可见行”聚合；`trHtml` 只为实际渲染出来的行画按钮。冲突计数和可见按钮计数是两套口径，不能用后者反推前者。
- **修法/用法**：保持两套口径并在面板写明「含折叠组」；验收时同时记录 `groups=21`、`badges=25`、`disabled=13`、`totalButtons=55`，不要只报一个数。要改「只看有动作时自动展开所有带行动组」，属 2.2 之外的展开策略，需另开一版。
- **坑**：①`ACT_CONF` 是 `renderSignalDash()` 内局部变量，不是 `window.ACT_CONF`；页面探针不要读 `window.ACT_CONF`，读不到不等于没生成，改用 `#sigConfBox` 的 `<li>` 数或筛选条文本。②`ACT_PRIO` 用 `sig.split(' ')[0]` 的规则码匹配；改信号代码（首个 token）不同步改 `ACT_PRIO` 键，会静默落到 `rank:99`（未定义优先级），排序和门禁都错；只改代码后的中文描述不影响匹配。③`blockedBy` 只认 `pending/doing`；T4 `doing` 时 disabled 仍是 13，T4 `done` 后才 13→12。T4 是同日门禁，不是“清仓后永久禁买”，别把 `done` 说成硬止损已生效。④`actTargetKey` 现按 `pool|code|name`，同一代码跨池暂不合并；当前数据无跨池样本，未来若出现，需先决定是否改键，不要直接改 `actStateKey`（状态键里还含信号名）。
- **验证**：本地/线上均为 21 组、25 徽标、13 disabled、55 总按钮；`#sigConfBox.open=true` 时面板高 449.6px、列表 360px 滚动；T4 完成路径 disabled 13→12；截图 `D:\Temp\v1137_online_panel.png` / `v1137_online_badge.png` / `v1137_online_blocked.png`。
### P-v1138 初版 SLA 把宏观月频（M16/M18）落进 T+2，误报 2 条超时

- **症状**：v1138 首版面板显示「执行超时 3 条」，其中除 T4 019441 外，还有 M16 格雷厄姆股债比、M18 换手率（数据日 2026-10-15，日龄 30），两条都被标 `SLA T+2 · 超 28 日`，与「月频可放宽」的审计口径相反。
- **证伪**：`ACT_SLA` 里没有 M 代码；`actSlaOf` 首版对所有未知码回退 `{limit:2,label:'T+2'}`。市场信号 5 条 act 全部命中 T+2，而 `XOV/P2` 已显式配 90 日，说明是默认分支错，不是数据问题。
- **根因**：只给 T 系列与 XOV/P2 配了 SLA，漏了 REGIME 熊市档、M9 股债性价比、M12 全球金融压力、M16 格雷厄姆股债比、M18 换手率 这一类非 T 代码；默认分支把「未知」等同于「买入 T+2」。
- **修法**：`actSlaOf` 优先查 `ACT_SLA`；查不到时按首字符分流——`T` 开头回退 T+2（仅未知 T 规则），其它一律回退 `{limit:90,label:'月频',kind:'macro'}`；面板口径补「REGIME 熊市档 / M9 股债性价比 / M12 全球金融压力 / M16 格雷厄姆股债比 / M18 换手率 等按月频 90 日复核，不当作每日动作」。
- **坑**：①`details` 收起时 `innerText` 只返回 summary，`#sigSlaBox li` 的 `innerText` 会是空串；核对列表用 `textContent` 或先 `open=true`。②SLA 日龄按周一至周五计、不含法定节假日，不是交易所日历；节假日前后可能差 1–2 日，页面已注明，不能把它当精确 T+1。③`actSlaCount` 只统计 pending/doing；`done/expired` 不计，T4 完成后「超时 1」会变 0，这是预期，不是丢失。④`actSlaHtml` 只列 `over` 行；`due`（今日到期）只在行内和 summary 计数，不逐条铺开，避免 37–42 行把面板撑爆。
- **验证**：修正后本地 `SLA 超时 1 · 复核滞后 20`、面板 21 条（1 T4 + 20 TREND/S-TREND），市场 5 条全 `SLA 月频`；线上 `?t=v1138live&final=1` 同口径（超时 1 / 复核 20 / 面板 21，今日到期 42）；截图 `D:\Temp\v1138_sla_panel_final.png` / `v1138_online_panel.png`。

### P-v1139 Top5 点击后高亮丢失 / 空白截图不是样式坏了

- **症状 A（高亮丢失）**：v1139 首版点 Top5 卡片能切到交易信号，但目标行偶尔不高亮或滚动到旧位置；再点一次又正常。**根因**：`renderSignalDash()` 是异步的，点击时可能还有最后一次 `innerHTML` 重建，把刚贴了 `sig-row-hit` 的行整行替换；另外 tab 的 `.active` 与旧 DOM 不同步时，代码会在旧 DOM 上点空，随后把隐藏 pane 里的行误当目标。**修法**：点击后 700ms 复查目标行，若被替换则重贴高亮/重找；tab 未激活或 pane 不可见时点击重试（≤40 次 / 200ms），最终校验 active tab 必须等于 `tabKey`。**验证**：线上点首卡 → `view-signal` + `hold` tab + `hold:019441:T4 硬止损`；筛选池卡 001076 / S2 能切 `screen` tab。
- **症状 B（截图空白）**：用 CDP 在 538 视口截图本地持仓页时，标题/资金口径条正常，下面全白，DOM 里 `#todayBand` 有高度、有文本。**证伪**：`#todayBand` 父级 `#view-holdings` 的 `opacity=0`、`animation=v43fade`、`transform=translateY(6px)`；卡片可见性全 visible，说明不是布局或数据问题，是后台标签页冻结了入场动画（fade 停在 0）。**修法**：这是截图环境的坑，不是页面 bug，不要为它改 CSS；在后台标签截图前先把目标 view 的 `animation='none' / opacity='1' / transform='none'`，或用前台真实标签截图。**别碰**：不要删 `v43fade`，前台用户看到的是正常入场动画。
- **症状 C（两套计数被当矛盾）**：首屏 chips「行动信号 56 条」与 Top5 summary「三池去重 97 条」并排，容易以为其中一个是错的。**根因**：`renderTodayTodo()` 只统计 `sig.hold`；Top5 统计 hold + watch + screen。**修法**：chips 可见文案改为「持仓行动 / 持仓补仓点 / 持仓接近」，hint 写明仅持仓池、自选/筛选另计，三池去重见 Top5。**别碰**：不要把 chips 直接改成 97（那会把 `sig.hold` 的纪律/加仓计数口径一起改掉）；不要把 Top5 改成只统计持仓（2.4 的目标就是三池合并）。
- **症状 D（前 5 全 T4 被误认为丢买入）**：当前数据前 5 全 `T4 硬止损`，第 6 条才是 000307。**根因**：`ACT_PRIO.rank` 风控/卖出 rank 10，SLA 超时/到期又排在日龄前；买入/网格 rank 70–85，自然排后。**这是排序结果，不是去重错误**。要“风控 + 买入配额”需另定规则，本轮没有擅自改。
- **验证**：本地 `?t=v1139local11&final=1` 538 视口 97 条 / 5 卡 / 无横溢；线上 `?t=v1139live3&final=1` 徽标 v1139、同款 97 / 5 卡 / 新 chips；点首卡命中 `hold:019441:T4 硬止损`。截图 `D:\Temp\v1139_local11_collapsed.png` / `v1139_local11_open.png` / `v1139_online_final_collapsed.png` / `v1139_online_final_open.png` / `v1139_online_final_click.png`。

### P-v1140 ERP 固定 3% 只做前端派生 / M9 数据日不要取 updatedAt

- **症状 A（M9 数据日与 ERP 卡不一致）**：固定 3% 后 M9 行显示 ERP 4.70 / 分位 43.1，但数据日仍是 `2026-11-26`，而 ERP 卡数据截至 `2026-10-15`；用户会以为 M9 是当天新算的。**根因**：`M9` 的 `dd` 原先取 `mc9.updatedAt`（宏观快照生成日），不是 `erp.points` 末点。**修法**：`dd: ((_erp9.points && _erp9.points.length) ? _erp9.points[_erp9.points.length - 1][0] : (mc9.updatedAt || ''))`，现在显示 `2026-10-15` 并带 stale 标记。**别碰**：`updatedAt` 仍可用于其他「快照刷新」文案，但不要把 M9 的「数据日」再改回去。
- **症状 B（以为改了原始宏观数据）**：页面上 10Y 变成 3.00%，`macro-data.json` 里仍是 1.6516，`MACRO_SNAP.erp.cur.y10` 也仍是 1.6516。**这不是没生效**：`erpFixed3()` 只在前端派生 `[date,E/P,3.00,E/P−3.00]`，原始数据保留给 M16/M11/股息率。**别碰**：不要为了 ERP 卡去改 `macro-data.json` 或 `MACRO_SNAP`，否则会同时污染 M16 格雷厄姆股债比、M11 中美利差、资产价格页股息率比较；也不要重跑 `gen_macro_snap.py` 只为了这个 3%。
- **症状 C（历史 M9 与当前页不一致）**：`gen_signals_hist.py` / 历史 `signals-hist.json` 的 M9 仍按原始 `erpPct`（82.1）生成，当前页是 43.1。**当前处理**：这是已知挂账，历史归档未按固定 3% 重算；查历史 M9 时不要与当前页对拍，看到 82.1 不等于页面回归。若要历史一致，需单独改生成器并重建历史快照，属于另一版。
- **症状 D（后台标签截图整页空白）**：CDP 538 截图 ERP 卡时，页面只有底栏、上面全白。**根因**：后台标签的 `.view` 入场动画 `v43fade` 被冻结在 `opacity:0` / `translateY(6px)`；DOM 里卡片有文本、有高度，不是数据或布局坏了。**修法（截图专用）**：先把 `.view` 的 `animation='none'、opacity='1'、transform='none'` 再截，或在前台真实标签截图；**不要**为截图删 `v43fade`。
- **症状 E（M9 行在 538 视口被裁）**：M9 行右列只看到「增配股至70-80% / 减股至20-30%」的一部分。**这不是单元格溢出**：M9 行 9 个 cell 的 `clientWidth==scrollWidth`（129/152/199/82/117/223/105/93/70），是 `.table-wrap` 449 可视 / 1180 内容的内层横滑；`body.scrollWidth=529==clientWidth`，页面本身无横溢。**别碰**：不要为 M9 单独加宽表或缩字号；需要看右列时滑表内横条。
- **验证**：本地 `?t=v1140local3&final=1` 与线上 `?t=v1140live1&final=1` 徽标 v1140；`erpFixed3` 末点 `['2026-10-15',7.7,3,4.7]` / `pct=43.1`；M9 行 `2026-10-15`；M16 仍 `10Y 1.65`；全页无旧 `82.1%` / `6.05%`；538 无页面横溢。截图 `D:\Temp\v1140_erp_card_538.png` / `v1140_m9_538_final.png` / `v1140_online_erp2.png` / `v1140_online_m9f.png`。
### P-v1141 缺估值不是「没触发」/ 裸 A 不是「可信」/ P4 代码改了不等于线上有行

- **症状 A（T15 在缺 PE 分位的持仓上整行消失）**：v1141 前，持仓 022438 / 020712 / 000307 在 T15 组里没有行；页面看起来像「T15 没触发」，实际是 `signalEvalAll` 的 T15 段只写了 `if (_peT) rows.hold.push(...)`，缺 PE 分位时没有任何 `else`。**修法**：补 `else rows.hold.push(valMissRow(base, 'T15 跟踪指数PE分位', valNaKinds(name)))`，与 T3/T8 共用占位：`watch`、`src='估值缺失·占位'`、`act='【不动】暂不操作 · 定投照常'`。**别碰**：不要给缺失行编一个分位，也不要把占位升成 act；这会让「数据缺失」重新变成「有交易建议」。
- **症状 B（同一规则在总纲是 A+、在回测页是裸 A）**：总纲新增 `A+ 正边际` 后，回测规则卡仍显示「证据 A = 已回测有对照数字」，同一个 A 在两页表示「测过」与「可信」两种意思，用户无法判断。**根因**：`_rRowHtml` 残留旧的 `g.ev` 三档映射，没跟总纲统一。**修法**：`_rRowHtml` 改用 `sigEvBadge({id})`，表头「等级」改「证据」，`_rHint/_rFoot` 改为 `A+/A−/A?/A·/C`，写明「裸 A 只表示测过，不等于可信」。**验证**：全文正则 `证据 [ABCD]` 命中 0。
- **症状 C（P4 说改好了，信号页却没有 P4 行）**：P4 注册表已改成「覆盖率（数据闸门）」，但信号页没有 P4 行。**这不是漏渲染**：P4 只在穿透覆盖率 <50% 时生成行，当前覆盖率未低于 50%，所以本来就不该有行。**别碰**：不要把 P4 强制插进信号表来“证明改好了”；也不要把代码改动说成线上已触发。要验证只能等覆盖率真的低于 50%，或另做构造数据的单测（本轮未做）。
- **症状 D（000834 默认看不到，被误判成「缺数据 / one() 早退」）**：`holdings-data.json` 有 000834（shares 1.6 / marketValue 37.53），但默认持仓信号页没有它，容易被写成「fund-daily 无 ≥20 点净值序列、`one()` 早退」。**已证伪**：`fund-daily` 有完整净值，`one()` 正常返回；真正原因是纳指100 同指数族（12 只）默认只列 1 只代表，000834 排第 10 只被 `famHidden`。点组头「展开全部 12 只」后可见 11 条信号行：`T3 估值止盈 / T8 估值加仓` 与 `T15 跟踪指数PE分位` 均为「估值数据缺失 / 观察 / 【不动】暂不操作」，0 条估值 act；另有 `T13 网格跟踪` 与 `TREND-DN 空头破位` 各 1 条 act（非估值信号）。**教训**：看到标的不在默认表，先查同指数族折叠与 `sigFamShow`，再查数据源；不要先假定缺数据。v1142 曾按错误假设加 `one()` 兜底，实测不触发，已完整回退（5,459,968 B / SHA256 与 v1141 完全一致，不另发版）。**别碰**：不要再按「无净值」加兜底、手改 holdings 或伪造净值。
- **症状 E（机制归并数与 59 条对不上）**：`SIG_MECH` 新增/改名信号后，chips 合计仍写 59，但成员表少一条或某条没有中文名。**根因**：59 是审计 CSV 的固定集合，`SIG_MECH` 是另一份手写映射；两处不同步就会静默少条。**修法**：改信号代码/名称时同时改 `SIG_MECH` 与 `docs/strategy_signal_audit_2026-11-25.csv`，并保持每行「代码 + 中文名」；验收时数成员表行数与 chips 合计，不要只看标题写 59。
- **症状 F（把「生效」读成「有 alpha」）**：总纲普通规则表里 A− 9 条仍显示「生效」，容易被读成「这 9 条也在赚钱」。**修法**：A 卡摘要与 `logicEffNoteHtml` 已写明「上方『生效』是档案状态，不等于会动钱，也不等于有 alpha；A− 9 条只作实验/观察」。**别碰**：不要把 A− 行从表里删掉；删了就看不出「在跑但负边际」，也失去后续复核对象。
- **验证**：本地 `?view=tg&t=v1141local7&final=1` 538 视口 `bodyW=529/bodyC=529`，`#tg-logic` 4 张表、1 个证据表头、11 个证据徽标、机制成员表 10 行合计 59；`?view=signal&t=v1141local9&final=1` T15 11 行 / 7 缺失 / 0 act，T3/T8 同；`000834` 需点「展开全部 12 只」后核 11 行 / T3/T8/T15 缺失 / 0 估值 act；线上 `?view=tg&t=v1141live1&final=1` 点「投资总纲」后同口径。截图 `D:\Temp\v1141_ev_summary.png` / `v1141_ev_col.png` / `v1141_ev_buy2.png` / `v1141_t15_missing2.png` / `v1141_000834_rows_final.png` / `v1141_000834_t15_final.png`。
- **发布**：提交 `48d862d70c52` / index 5,459,968 B / SHA256 `3621EBF8C979D00C1976793435326D1A12594BD2E69091B71421FEC344AAC826` / 纯 LF；`check_js` 22 块 ALL OK、`check_html_comments` 357 处 0 隐患、`check_globals` PASS（282 键 / 431 赋值点，新增 0 / 消失 0 / 变化 7）、`check_hold_consistency` PASS=9 WARN=2 FAIL=0；GitHub raw 字节一致。

### P-v1142 「手动参考」不是「已生效」/ 趋势行动列别放第 4 列

- **症状 A（R2 关，但页面仍写「定投降档」「定投照常」）**：`R2` 在 `logic-state.json` 已是 `off`，却仍有 RB/BW/L1/TREND 行写「全组合定投降一档」「定投可加速一档」、个基趋势行动列写「定投照常」「超卖·维持定投」。**根因**：这些文案仍按「有月度定投通道」的旧前提写，R2 关时没有执行通道。**修法**：RB/BW 注册表改 `on（仅信号 · 手动参考）`，四条 `thrAct/thr/plan` 全部改写；`dcaManualOnly()` 只有 R2=`on` 才非手动；行级徽标只做展示；个基趋势行动列改「不自动月投 / 减速·暂缓（手动参考）/ 不加仓」。全站「定投照常 / 维持定投」清 61 处。**别碰**：不要为了「看起来一致」把 RB/BW 的 `on` 改成 `obs`；`on` 是档案启用，不是自动执行；也不要改 `signalEvalAll` 判定来让文案一致。
- **症状 B（「手动参考」徽标很多，被当成 78 条都在生效）**：信号页 `#view-signal` 文本中「手动参考」出现 78 次，是因为每个 L1/TREND 行都带徽标，不代表 78 条新规则。**解释**：徽标只标「这一行触发时只改提示、不自动下单」；实际行数仍按信号引擎出数。**未决**：是否只在组头/规则卡显示，避免视觉过密，尚未拍板；本轮保留逐行徽标。
- **症状 C（个基趋势行动列在 538 视口被裁成半行）**：列原在第 4 位，`min-width:96px`，538 视口只看到「减速/暂缓（手」半截，且「（手动参考）；超卖·不加仓」挤成一行断在词中间。**根因**：12 列表格内容宽 1,000+px，内层横滑；第 4 列起点约 x=402，右边界超出 538 视口；96px 也放不下「行动参考（手动）」。**修法**：行动参考列移到第 2 列（基金之后），`min-width:152px`，两条建议用 `<br>` 分行；表头完整显示「行动参考（手动）」。**别碰**：不要缩字号或删指标列来硬塞；表仍走内层横滑，页面本身无横溢。
- **症状 D（本地 127.0.0.1 仍显示旧文案）**：`index.html` 已改，`127.0.0.1:8791` 强刷后仍显示旧「定投照常」，`hasNew=false`。**根因**：该 origin 的 Service Worker 仍控制页面，查询参数变化不一定触发新脚本。**修法**：换用 `localhost:8791` 或先注销该 origin 的 SW；本轮用 `127` + 新 `t` 仍被旧缓存拦过一次，改 `localhost` 后正常。**别碰**：不要把「页面没变」误判成代码没写入；先查 `navigator.serviceWorker.controller` 和脚本里是否含新标记。
- **验证**：本地 `?view=signal&t=v1142local9&final=1` 徽标 v1142、`#dcaGear` 文本、趋势面板表头/首两行、全页 `定投照常` 0；线上 `?view=signal&t=v1142live1&final=1` 徽标 v1142、切「趋势策略」同口径；截图 `D:\Temp\v1142_trend_final.png` / `v1142_online_trend_table.png` / `v1142_tg_note_center.png`。
- **发布**：提交 `8ac16b51f999` / index 5,464,312 B / SHA256 `A50A464A5BF869ADBFAD7AFDAB694E333AEAF4C49AD27B3E5F1838077CA69370` / 纯 LF；`check_js` 22 块 ALL OK、`check_html_comments` 358 处 0 隐患、`check_globals` PASS（282 键 / 432 赋值点，新增 0 / 消失 0 / 变化 8）、`check_hold_consistency` PASS=9 WARN=2 FAIL=0；`verify_sync --gh-only` 字节一致 5,464,312 B。

### P-vP210 同一只基金两套市值，压力测试会翻转（v1143 已收口）

- **症状（历史，2026-11-26 上午）**：页面/信号用 `shares×nav` 显示 10,283.50，占 18,067.10 的 **56.92%**；账户 `marketValue` 5,412.79，占 20,565.55 的 **26.32%**；差 −4,870.71。**根因不是四舍五入，是 012920 只扣了第一笔卖出**：3,423.61 份只减了 11-05 的 1,621.57 份，11-25 第二笔 1,621.57 份没扣。
- **后果（历史）**：−44.6% 峰回撤在页面口径 −25.39pp（破 20pp）、账户口径 −11.74pp（未破）；同一套“单只 >20% / 压力 >20pp”闸门在两套口径间翻转。
- **修法（v1143 已执行）**：`TRADE_QUERY` 两笔 confirmed 卖出 → 余 1,802.04 份，成本按原单位成本 2.6164 等比结转 4,714.86，11-25 净值 2.9747 → 市值 5,360.53；同时 `holding_hqb` 拆出 020097 4,877.17（第二笔赎回款落点），活期宝 7,720.80；`total` 刷新为 20,541.42，在途 2,505.37。**现在只有一套口径**：012920 占决策权重 29.72%、账户 26.10%；−44.6% 拖累 −13.26pp / −11.64pp，压力 20pp 未破，单只 20% 仍破。
- **别碰**：不要手改 `holdings-data.json` shares/marketValue 让两个数对上；不要把 020097 并回 000912；不要把在途 2,505.37 塞进决策权重；不要用账户总资产 20,541.42 去除决策权重 18,036.08；不要把“压力未破 20pp”说成“集中度没问题”；不要把“只补现金不部署”说成“补足 5 万摊薄完成”（现金会到 79.37%）。
- **验证**：`docs/P2_STRESS_TEST_2026-11-26.md` v1143 重写版；`check_hold_consistency` C 项 18,036.08 + 2,505.37 = 20,541.45 vs total 20,541.42（差 0.03）；账户 `holding_list` 012920 5,360.53 / constantProfit 645.74。
- **历史数字只作教训**：旧 56.92% / −25.39pp / 10,283.50 / 3,423.61 已作废，不得再当当前值引用。

### P-v1143 活期宝不是单只 000912；现金行漏算会把在途做假

- **症状 A（total 减 core 差 4,870.70，现金行仍是 2,843.63）**：`012920` 市值已降到 5,412.79，但 `holdCore` 与 `total` 仍差 4,870.70，`check_hold_consistency` C 项 FAIL；现金行 000912 只有 2,843.63，而账户 `hqb=7,720.80`。**根因**：012920 第二笔赎回款 4,877.17 落到 **020097 中加货币E**，不在 000912；旧 `CASH_CODES` 只认 `000912/007866`，`holding_hqb` 的第二只货基没有建行，于是差额被自动算进 `pendingBuy`（在途从 2,498.46 变 7,382.54）。
- **修法**：`refresh_holdings_ttskill.py` 按 `holding_hqb` 明细逐只补建 `assetType='cash'` 行；`CASH_CODES` 加 020097；`buy_codes` 排除 `acct_hqb` 全代码；`_audit_capbal_kpi.py` 的现金豁免改 `assetType='cash'` 动态识别。`total` / `marketValue` / `hqb` 由 `ACCOUNT_HOLDING` 刷新，`pendingBuy` 回到 2,505.37。
- **症状 B（对账卡同句自相矛盾）**：`mvGap=0` 时卡片仍显示「账户明细市值合计与总资产差 ¥0.00，主因 000307 差 +733.01；其余 ¥733.01 为逐只四舍五入」。**根因**：v1129 的旧文案假设 `mvGap = 最大单只负差 + 四舍五入残差`；v1143 刷新后 `ΣmarketValue = total`，`mvGap=0`，旧句把“在途正差”误当“四舍五入”。**修法**：`Math.abs(mvGap)<0.05` 时改说“已对平；逐只差额正负相抵，合计等于在途 2,505.37”；只有 `mvGap≠0` 才列主因，删除“其余为四舍五入”断言（tag `fw2_v1143_recon_note_fix`）。
- **别碰**：不要把 020097 并进 000912（账户 000912 本身仍是 2,843.63，合并会把归属说错）；不要给 020097 编 `ledger-import` 现金流或理杏仁链接（现金行，缺就如实 WARN）；不要为过 `F09` 把现金行算进 `firstBuyRefresh.total`；不要把 `pendingBuy` 手改成 2,498.46。
- **验证**：`holding_total.total=20,541.42 / hqb=7,720.80 / fund=12,820.62`；`holding_list` 012920 `assetValue=5,360.53 / holdProfit=2,158.54 / constantProfit=645.74`；C 项 18,036.08 + 2,505.37 = 20,541.45 vs 20,541.42；26 只 `ΣmarketValue` = total；截图 `D:\Temp\v1143_recon.png` / `v1143_recon_card.png`。

### P-v1145 跨 IIFE 调不到 P2 函数，冻结静默失效

- **症状**：代码里已写 `p2BuyBlockOf`，页面 `typeof holdP2GateData` 也返回 `function`，但交易信号页 012920 的买入行按钮仍是可点的「开始」，没有任何冻结；控制台无报错。
- **根因**：`holdP2GateData` / `p2BuyBlockOf` 定义在持仓脚本 IIFE 内，交易信号页是另一个 IIFE，词法作用域不共享；信号页 `_p2Gate()` 的 `try/catch` 把 `ReferenceError` 吞成 `false`，于是 `_p2blk` 恒 null。`typeof` 在主世界能看到它，只是因为脚本块本身是 `window` 作用域下的函数声明可见性，**不等于信号页能调用**。
- **修法**：定义后显式挂到已存在的 `window.SIGNALS_CFG`（`p2GateData` / `p2BuyBlockOf`），不新增顶层键；信号页只读命名空间并整页缓存。tag `fw2_v1145_p2_gate_exec`。
- **验证**：主世界 `window.SIGNALS_CFG.p2BuyBlockOf(d,'012920')` 返回 `{conc:29.721,cap:20}`；`'000912'` 返回 null；强制 T7 回撤补仓进入 act 后按钮 disabled=true、`.sig-exe-wait`=「买入冻结」。
- **别碰**：不要把 `try/catch` 的兜底 false 当“没超限”的证据；不要改为新增 `window.__p2*` 顶层键（会破 282 键基线）；不要让信号页直接裸调 `p2BuyBlockOf`。

### P-v1147 用单位净值反推基金 3 年收益，份额折算会造出 −33% 假跌并误冻买入

- **症状**：P2-11 初版用页面 `__NAV_SERIES__` 单位净值直接算 3 年收益，160422 华安创业板50ETF联接A 得到「3 年 −33.33%」，相对 510300 沪深300ETF 落后 43.5pp，软命中并准备冻结；但该基金实际并非弱于基准。
- **根因**：`nav-hold.json` 原始单位净值 2023-11-24 为 1.3563、2026-11-25 为 1.6486，真实约 +21.6%；`fund-daily` / `__NAV_SERIES__` 给 2023-11-24 的值是 2.4729，呈 −33.3%。这是份额折算/单位口径变化造成的假跌，不是真实亏损，也不是数据缺失。基金 3 年收益不能从单位净值反推。
- **修法（v1147）**：基金 3 年收益优先读 `fund-profiles.json` 的 `r3y`（东财口径，已处理份额折算/分红）；画像缺 `r3y` 只记「画像缺 3 年收益 / 数据不足」，不冻结、不伪装通过。基准仍用 `bench-long.json` 的 ETF 净值序列算 3 年（510300 / 513500 / 518880 / 511010），日经无同风格基准返回 null。
- **验证**：修复后 `termBuyBlockOf('160422')=null`；24 只非现金持仓 `frozen=0`、`threeYear=17`、`dataShort=7`。另用临时覆盖验证冻结分支：`termBuyBlockOf('160422')` 返回合成终止样本时，T13 行按钮 `disabled:true`、执行列「终止风险冻结」，刷新即还原。
- **别碰**：不要再用 `__NAV_SERIES__` / `fund-daily` 单位净值反推基金 3 年收益，也不要为了“让 160422 通过”改 `nav-hold.json` 或 `fund-daily.json`；基准可以继续用 ETF 净值序列，但基金自身收益必须走画像 `r3y`。`r3y` 缺失就是数据不足，不能拿反推值补。

### P-v1149 实际回撤不能拿当前权重倒推：历史快照里有成本基数重算跳变

- **症状**：想接「实际回撤 15% 冻结 / 20% 评估」时，直觉做法是用 59 次 `holdings-data.json` 历史快照的 P&L 序列算组合回撤；但序列在 2026-11-26 出现一次跳变，早期算出来的回撤无法解释，容易被当成真实暴跌或“刚好 0%”。
- **根因**：历史快照里 012920 的成本基数在 11-26 早段是 8,957.53，同日晚段修正为 4,714.86（两笔 confirmed 卖出后份额重建）；`capital-balance.json` 的 `tx` 为空、`ledger-import.json` 只有 012920 的 26 笔流水，无法还原完整出入金。P&L 序列受成本基数与流水缺失双重影响，不是可审计的组合净值曲线。
- **修法（v1149）**：**实际回撤不接执行**，回撤格继续「待建立 / 无法判定」；不建影子组合、不用当前权重倒推、不补 0%。只把 **压力 20pp** 接进买入冻结：`stressBad = stressPp > stressCap`，`p2BuyBlockOf` 只冻最大单只。tag `fw2_v1149_p2_stress_exec`。
- **验证**：P2 卡真实显示「P2-9 已生效 · 实际回撤待建」、压力格「−13.26pp · 未超 · 买入不冻结 · 已接执行」；合成 `stressPp=21.5` 时 `p2BuyBlockOf` 返回 `flags:["conc","stress"]`，012920 冻结、其他代码 null；`check_globals` 仍 282 键（新增 0）。
- **别碰**：不要用当前持仓权重 × 历史净值倒推“如果当时持有”的组合回撤；不要把 11-26 成本基数跳变当真实收益暴跌；不要在缺高水位时把回撤灯改绿/红；不要为了“让回撤有数”手改 `holdings-data.json` 或补假流水。要接实际回撤，先定「从今日起新建真实高水位、历史段不可判」或接受账户 P&L 近似口径。

### P-v1151 补记不能把 A+ 基准日前移；导入不能先写后验

- **症状**：账本里补记一条早于 2026-11-26 的总资产后，高水位突然变成更早那天的数值，A+ 的初始基准 20,541.42 被绕过；或者导入 JSON 格式不对，页面提示失败但本机已有快照/流水被改了一半。
- **根因**：①`_p2DdState` 原来用 `rows[0].date` 作为 `baseDate`，任何更早快照都会把基准日和高水位起点前移。②导入若先写 localStorage 再校验，坏 schema 也会落盘；或先写快照后写流水，任一步失败就留下半套账本。
- **修法（v1151）**：①`_p2DdState` 保存的 `baseDate` 优先，`savedBase` 存在时丢弃 `k < savedBase` 的快照；`_p2DdAddSnap` 明确拒绝 `date <= baseDate`（只允许 `baseDate < date <= _p2Today()`）。②`_p2DdImport` 先 `JSON.parse` + `schema` + 逐条字段校验，再合并；本机有账本时 `baseDate` 不后移，早于基准日的导入快照忽略并计数；同日期快照以导入为准；出入金按 id 去重；最后才写流量/快照，写失败返回错误。③当前数据日自动快照不可删，改值用同日补记覆盖。
- **验证**：本地补记 11-27 20,000 → 2/20、HWM 20,541.42、−2.64%；同日覆盖 21,000 → HWM 21,000；删除 11-27 → 回 1/20；补记 11-26 99,999 被拒、状态未变；导入 11-24 26,000 + 11-27 24,000 + 重复 x2 → 11-24 忽略、流水 2 笔、HWM 24,000；坏 schema 导入后账本不变。538 展开区 `scrollWidth=clientWidth=475`。
- **别碰**：不要放宽 `date <= baseDate`；不要用补记把基准日改成更早以“多攒几天”；不要先写 localStorage 再校验导入；不要把 `_p2DdState` 的 `savedBase` 删掉（会退回“最早快照即基准”）；不要允许删除当前数据日快照后还期待它不自动回来。

### P-v1150 本机账本只记打开日、不可回填；出入金调整不能和基准日重复计入

- **症状**：接上实际回撤后，页面只显示「样本 1/20」，过几天仍可能停在 1；或者登记基准日当天的一笔转入后，回撤立刻被放大很多，像是凭空多跌了一截。
- **根因**：①`p2DrawdownData` 只在持仓/信号页调用 `holdP2GateData` 时执行，`_p2DdState` 只写「当天」一条快照；没打开工作台的数据日不会补，历史 total 也没有手工补记入口，所以样本可能长期停在 1/20。②基准日快照的 total 已经包含当天转入/转出，如果 `_p2DdRecalc` 在基准日再应用一次 `flow`，HWM 会被重复抬高，回撤被高估。
- **修法（v1150）**：`P2_DD_CFG` 固定 `minDays:20`；`_p2DdState` 按数据日期去重、同日只更新 total；`_p2DdRecalc` **基准日不应用当日出入金**，之后才 `hwm = max(prevHwm + flow, total)`；页面提示明确「只记银行卡↔账户；基金申赎/转换不算；登记日总资产需已包含该笔资金，否则会暂时高估回撤；只存本机浏览器，换设备不自动带走」；`_p2DdExport()` 可导出 JSON 留档。
- **验证**：本地 1 条 11-26 / 20,541.42 → 1/20、0 笔；注入 20 个数据日、HWM 24,500 → −16.16%，信号页 7 条全组合买入冻结；登记 11-24 +5,000 → −30.37% 且追加「减仓评估」，删除后回 −16.16%；1 条快照的信号页「回撤 −」/「全组合」计数 0。
- **别碰**：不要为了凑 20 天填假 total 或假流水；不要把基金内部申赎/转换算成外部现金流；不要把基准日当天的出入金重复计入；不要用系统日期替代 `state._pfAt`；不要降低 `minDays=20` 就宣称已接冻结；不要冻结卖出/拦截/观察；不要自动卖或写交易状态；不要新增 window 顶层测试钩子。

### P-v1148 V1 行默认不出现是三态关，不是门禁失效；双徽标不换行会读成一串

- **症状**：v1148 已把 `V1 波动赶底` 接进门禁，但合成 V1 行注入后 `table.sig-tbl` 里找不到，页面 `innerText` 也没有「测试基金软命中/硬命中」；容易误判为 `_termApplies` 或 `termRiskOf` 没接上。双闸门合成行则出现「…；卖出/拦截不碰买入冻结 · 单只 29.72%…买入冻结 · 净值断档…」连成一串。
- **根因**：①V1 在投资总纲三态里是「关」，`logicSigMark` 对 `V1` 返回 `off`，`_lgF` 在源头整行过滤；行没进表，门禁自然无从渲染。②`.sig-cap-freeze` / `.sig-cap-warn` 原为 `inline-block`，在行动方案格里接在正文后同一行；两条徽标宽度超过列宽就挤压换行，读成一串。
- **修法**：①测试前临时覆盖 `window.logicSigMark`，对合成 V1 代码返回空字符串；或把 V1 三态设为观察/生效。不要为了测试把 V1 默认改成开。②CSS 加 `.sig-tbl .sig-plan .sig-cap-freeze, .sig-tbl .sig-plan .sig-cap-warn { display:block; width:fit-content; max-width:100%; margin-top:4px; }`；tag `fw2_v1148_term_badge_block`。
- **验证**：覆盖三态后 `888888` V1 软命中 `.sig-cap-warn=true`、`freeze=0`、无可点按钮；`999999` 硬命中行动方案「【不动】买入冻结 · 不买入」；`012920` 双闸门 `freeze=2`、`wait="买入冻结 · 2 条闸门"`，截图中两条原因各占一行。
- **别碰**：不要把 V1 默认三态改成「开」来绕过测试；不要用 `bu.js` 直接读主世界 `SIGNALS_CFG`（隔离世界读不到，需注入 `<script>` 写隐藏 DOM）；不要把 `inline-block` 改回。

### P-v1146 verify_sync 仍期待 v1142 前旧文案「定投照常」，发布后误报缺标记

- **症状**：v1146 发布后 `python edit_work\verify_sync.py --gh-only` 报 `FAIL —— [GitHub] caifu/index.html 缺标记 '【不动】暂不操作 · 定投照常'`，但本地与线上页面都正常、`不自动月投` 文案存在。
- **根因**：`verify_sync.py` 的 v634 标记列表还停留在 v1142 前的 `【不动】暂不操作 · 定投照常`；v1142 已按 R2=关把全站 53 处「定投照常」改成「不自动月投」，标记检查却没同步，于是从 v1142 起就一直是陈旧期望。不是页面丢文案，也不是 v1146 新卡导致。
- **修法**：把 `verify_sync.py` 里该标记改成 `【不动】暂不操作 · 不自动月投`；复跑 `verify_sync --gh-only`，结论 PASS（GitHub 六文件字节一致）。
- **验证**：先在本地 `edit_work/index.html` 搜 `定投照常` 为 0、搜 `不自动月投` 命中；再对比 v1144/v1145 备份同样没有旧文案，确认是脚本陈旧而非本版回归。
- **别碰**：不要为了过校验把页面文案改回「定投照常」（会违背 R2=关的拍板）；不要把这条 FAIL 当页面发布失败；不要删标记检查来“修绿”。

### P-v1145 浏览器脚本隔离世界读不到主世界全局

- **症状**：`bu.js` 里 `typeof window.SIGNALS_CFG === 'undefined'`、`typeof holdP2GateData === 'undefined'`，误判“函数没挂上”。
- **根因**：浏览器自动化脚本运行在隔离世界，`window` 与页面主世界不是同一个对象；只有 `document` 共享。
- **修法**：用 `document.createElement('script')` 注入一段主世界脚本，把结果写到 DOM 属性或 `document.documentElement.dataset`，再由隔离世界回读；或直接在页面 DOM 上读渲染结果验收。
- **别碰**：不要根据隔离世界的 `typeof` 结论改页面代码。

### P-v1145 执行按钮文案重复「买入冻结」

- **症状**：按钮本身写「买入冻结」，下方 `.sig-exe-wait` 也写「买入冻结」，行动方案格再有徽标，视觉上同一句话出现三次。
- **修法**：按钮保留「开始」并 disabled，下方状态行写「买入冻结」，方案格写「买入冻结 · 单只 29.72% > 20%」，脚注解释；三层分工不重复同一句式。
- **别碰**：不要把按钮文案改回「买入冻结」；不要把 `.sig-exe-wait` 删掉只留 disabled（色弱/窄屏下不易识别原因）。

### P-v1145 T3/T8 合并行被三态降成观察，P2 的 T8 分支看不见

- **症状**：强制 `valLow=100` 让 T3 估值止盈 / T8 估值加仓 的数据层 `lvl=act`，页面仍显示「观察」，执行列没有「买入冻结」；再强制 `ACT_PRIO`、刷新、缓存都不生效，容易误判为 `actConflictMap` 对 mixed 行降档。
- **根因**：`logicSigMark` 对多码行按「任一规则生效即保留，全部关才隐藏，其余按观察」处理。`logic-state.json` 当前 T3 估值止盈=obs、T8 估值加仓=off，合并行于是被降为 `watch`；`_lgLv` 只看三态结果，不看数据层 `lvl`。这不是冲突优先级问题，也不是 P2 代码问题。
- **修法/验证**：不改代码。测试时临时覆盖 `window.logicSigMark` 对 T3/T8 返回空串，并强制 `valLow=100`；真实渲染命中 disabled「开始」+「买入冻结」+「买入冻结 · 单只 29.72% > 20%」徽标。再设 `valLow=30/valHigh=50` 让 T3 估值止盈 触发，按钮恢复可点、无冻结。刷新即还原。截图 `D:\Temp\v1145_t8_left.png` / `v1145_t8_right.png` / `v1145_t8_exec.png`。
- **别碰**：不要把 T3/T8 合并行改成两条独立行来绕三态；不要把三态结果误当 P2 判定；不要把该行默认显示「观察」说成 P2 已冻结；只有用户把 T3 估值止盈 或 T8 估值加仓 设为生效，才可能看到 T8 估值加仓 的买入冻结。

### P-v1144 只写 .hold-recon .hr-grid 会漏掉新卡；三格被拉成整行

- **症状**：`#hdP2Gate` 的 `.hr-grid` 三个格子全部占满整行（实测每格 477px，实际容器 509px），三格纵向堆叠；CSS 计算值却是 `repeat(2, minmax(0,1fr))`，看似“媒体查询生效了”。
- **根因**：`.hold-recon .hr-grid` 带 `display:grid`，但新卡 class 是 `hold-p2`，没有 `hold-recon`；只写 `.hold-p2 .hr-grid { grid-template-columns: ... }` 不会命中 `display:grid`，`.hr-grid` 仍是普通块级容器，子元素按块级占满整行。**不是媒体查询错，也不是内容太长。**
- **修法**：`.hold-p2 .hr-grid` 必须自带 `display:grid` + `gap:9px`；宽度 ≤980px 时两列、第 3 格 `grid-column:1/-1`；≤520px 单列（tag `fw2_v1144_p2_gate_readonly`）。
- **验证**：539×650 真渲染，三格 `234 / 234 / 477px`；`#hdP2Gate` 文本 29.72% / −13.26pp / 待建立；截图 `D:\Temp\v1144_p2_viewport2.png`。
- **别碰**：不要为了“让三格一行”把第 3 格 `grid-column` 去掉（538 会挤成三列 160px，标签截断）；不要把 `display:grid` 写回只依赖 `.hold-recon`。

### P-v1151d 数据债三项：旧接口、pandas DLL、统计局 HTML

- **症状 1**：`index_daily` 刷新失败，腾讯 `web.ifzq.gtimg.cn/appstock/app/fqkline/get` 返回 HTTP 501 + WAF HTML；换东财 `push2his` 单次可 200，连续调用 `curl rc=56` 空返回。
- **修法 1**：腾讯改 `proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get?param=sh000300,day,,,1300,qfq`；备源用新浪 `CN_MarketData.getKLineData`；`000922/000985` 新浪只到 2019/2016，回退中证指数官网 `csindex-home/perf/index-perf`。`curl` 加 `--http1.1` + 3 次重试；15:10 前把当日从对拍样本剔除，只写双源共同确认的最后日期。
- **别碰**：不要把腾讯当日盘中线直接写进 `index-daily.json`；不要用东财 `push2his` 当主源（连续调用必断）。

- **症状 2**：`macro_extra` 报 `ModuleNotFoundError: akshare`；`py` 3.12 有 akshare，但 `import pandas` 报 `DLL load failed while importing hashtable: 应用程序控制策略已阻止此文件`；隔离安装 `_pydeps` 同样失败。
- **根因**：Windows 应用控制策略拦截 pandas 的 `_libs` DLL，不是缺包、不是版本冲突，重装无效。
- **修法 2**：生成器改纯标准库 `urllib`；东财 `datacenter-web` 取出口/社零/固投，新浪 `MacPage` 取用电量；工业利润、地产投资改取国家统计局官方月度文章。`gen_pb_ratio.py` 同样改为直连乐咕乐股，不再 import akshare。
- **别碰**：不要再往 `edit_work/_pydeps` 装 pandas/akshare 试图绕过；不要用 `py -m pip` 重装当修复。

- **症状 3**：统计局文章正文正则匹配不到「利润总额…同比增长 16.0%」，但浏览器看得到。
- **根因**：HTML 标签把数字/百分号切断，`利润总额` 与 `同比增长` 之间插入 `<span>` 等标签；直接对原 HTML 跑正则会漏。
- **修法 3**：先 `html.unescape(re.sub('<[^>]+>', ' ', text))`，再 `re.sub(r'\s+', ' ', ...)`，最后正则；列表页按绝对 URL 去重，避免同一篇在列表重复 3 次被当 3 期。
- **别碰**：不要用标题里的百分比当正文值（标题只用于定位文章和月份）；不要把「工业增加值」当「工业利润」——两者都在统计局发布，但指标不同。

- **症状 4**：单独跑 `_gen_data_mgmt.py` 后 `refreshFailed` 仍是旧三项。
- **根因**：该脚本只在 `DM_FROM_CHAIN=1` 时按本次链结果重写；单独跑会继承旧状态。
- **修法 4**：本轮用 `DM_FROM_CHAIN=1` + `REFRESH_BAD_STEPS=''` 重生成，`refreshFailed=[]`；但这只是模拟链成功，**不等于完整 `refresh_all.py` 跑过**。下一次 21:30 全链后要再复核一次。
- **别碰**：不要把 `refreshFailed=[]` 当成“三项已全链验证通过”；不要手改 `data/data-mgmt.json` 消红。

### P-v1152 · 数据管理页源描述与生成器漂移，导致发布被 v891 审计拒绝

- **症状**：`push_gh_v39.py` 在 `_audit_dm_v845` 处报 `frontN=47 genN=47 sameKeys=True driftKeys=4`、`FAIL=True`、`PUSH_RC=1`，拒绝发布；没有 Git push。
- **根因**：本轮只改了 `_gen_data_mgmt.py` 的四条 `src` 描述（`index_daily` / `macro_extra` / `fund_jjcc` / `pb_ratio`），`index.html` 内的 DMCONFIG 仍是旧文案，形成四键双份真相漂移；审计按字段对拍，drift 即 FAIL。
- **修法**：把 `index.html` 四处 DMCONFIG `src` 同步成生成器文案，并升徽标 `v1152`（只改文案，不动判定/布局）；复跑 `_audit_dm_v845.py` 得 `driftKeys=0`、`FAIL=False`，再发布。
- **别碰**：不要只改 `data-mgmt.json` 或只改生成器；不要为过审把 `driftKeys` 检查删掉/放宽；下次改任一侧 `src`，必须同步另一侧再发布。


### P-v1153 · 新增 T2b 后页面只见 T17、不见 T2b（正则截码 + 三态连带隐藏）

- **症状**：`SIGNALS_CFG` / `SIGNAL_REGISTRY` 已含 T2b，`signalEvalAll` 也生成行，但信号页只有 T17；投资总纲「⑤ 退出纪律」层同样看不到 T2b。隔离环境读 `window.SIGNALS_CFG` 返回空，一度误判“脚本没执行”。
- **证伪**：注入 `<script>` 到页面主世界读 `document.defaultView.SIGNALS_CFG` 与 DOM 行文本，确认对象与行生成都在；再查 `LOGIC_SIG_RX` 分组结果，发现 `T2b 条件化…` 被 `T\d+` 匹配成 `T2`。
- **根因**：`LOGIC_SIG_RX` 用 `T\d+`，把 `T2b` 截成 `T2`；`logicStateEff` 对 `T2` 读旧 `logic-state.json` 默认「关」，于是整条 T2b 被按 T2 的关态降档/隐藏。另：新规则无存档键时默认落「观察」，也会让 `act` 降档。
- **修法**：①正则改 `T\d+b?`；②`LOGIC_LAYERS` 把 T2b 放进「⑤ 退出纪律」、T17 放进「② 资产结构」；③新增 `LOGIC_DEFAULT_ON={T2b:1,T17:1}`，`logicStateEff` 对无键新规则默认「生效」；④`SIG_MECH` 补两族，全站计数 59→61；⑤`_gen_data_mgmt.py` 的 `logic_state.src` 同步 61，否则 `_audit_dm_v845` 报 `driftKeys=1` 拒绝发布。
- **别碰**：不要用 `bu.js` 的全局对象检查判断脚本未执行（隔离执行环境读不到页面主世界）；不要把 T2b 改回裸 `T2b` 靠 `T2` 三态管理；不要让新规则默认落「观察」再宣称已生效。
### P-v1154 · 策略工厂三处坑：tab 闸门写死 7 个 / day 不是 YYYYMMDD / 回撤方向写反

- **症状 1**：`push_gh_v39.py` 在 `_audit_plan_merge_v895` 处报 `A01 现役 7 个 tab` FAIL，拒绝发布；页面本身 8 个 tab 正常。
- **根因 1**：A01 把期望列表写死为 `['alloc','bt','bt','param','dd','v11','review']`，新增 `sf` 必然不匹配。
- **修法 1**：把期望列表扩为 8 个（`sf` 在 `v11` 后），并新增 A01f 断言 `data-st="sf"` / `#stp-sf` / `name === 'sf'` / `sfBacktest` / 两策略中文名；其余 40 项未放宽，41/41 PASS。
- **症状 2**：若按 `YYYYMMDD` 解析 `v11-bt-data.json` 的 `day`，日期全部错到 1970 年代，回测区间为空或起点错乱。
- **根因 2**：`meta.note` 已写明 `day＝距 meta.base 的自然日数`，`base=2015-01-01`，`day=4` 是 2015-01-05。
- **修法 2**：`sfDayStr` / `sfDayNum` 一律以 `meta.base` 做 `Date.UTC` 加减；不要复用 V11 之外的日期假设。
- **症状 3**：结论卡出现「最大回撤更浅」同时又说「两项都输」的自相矛盾。
- **根因 3**：触发条件写成 `s.mdd > b.mdd`，而 MDD 是负数，`>` 表示更浅（更好），被误当成「更差」。
- **修法 3**：改为 `s.total < b.total && s.cagr < b.cagr` 才提示「累计和年化都跑输」，回撤优劣单独按 `s.mdd > b.mdd` 描述。
- **别碰**：不要用当天收盘价反推当天信号（必须 `t−1` 信号、`t` 收盘成交）；不要给策略工厂接实盘/下单或写交易状态；不要新增 window 全局键。

## P-v1155 发现层 v1155（2026-11-27）

- **症状 1**：`gen_discovery.py` 明明跑成功，`counts.watch=0 / screen=0`，登记表只有 V11 与深跌。
- **根因 1**：`watchlist-data.json` 与 `screen-pool.json` 在 `edit_work/` 根目录，不在 `edit_work/data/`；`load()` 只拼 `DATA` 时读不到，静默返回 `None`，循环 0 条。
- **修法 1**：`load(name)` 依次尝试 `data/name` 与 `ROOT/name`；重跑后 `watch=11 / screen=40`。以后新增源先确认落盘目录，不要默认都在 `data/`。

- **症状 2**：538 视口下发现层表最右「说明」列被横切，右侧内容不可见；1280 正常。
- **根因 2**：表格 `min-width:620px` 且 6 列，538 卡内只能显示前 5 列；横滑虽可用，但用户看不到说明。
- **修法 2**：把「说明」并入「标的」单元格第二行（小字灰色），表格降为 5 列、`min-width:460px`；538 实测完整可见、无横溢。**别改回 6 列 + 620。**

- **症状 3**：深跌条目的「数据日」显示 `20261124`，与 V11 的 `2026-11-26` 格式不一致。
- **根因 3**：`index-dd.json` 的 `indices[].end` 是 `YYYYMMDD`，V11 的 `dataDate` 是 ISO。
- **修法 3**：前端 `fd()` 对 8 位数字做 `YYYY-MM-DD` 切片；不要改源数据格式（会破坏 `index-dd` 其它消费方）。

- **症状 4**：`push_gh_v39.py` 报 `publishedDataFiles=42 unregistered=['data/discovery-registry.json']`，拒绝发布。
- **根因 4**：新数据只进了 `FILES` 与台账，没进 `index.html` DMCONFIG / `_gen_data_mgmt.py`；`_audit_dm_v845` 以两端 key 集合比对。
- **修法 4**：四处同时登记（FILES / ledger / 前端 DMCONFIG / 生成器 DMCONFIG），再 `DM_FROM_CHAIN=1 python _gen_data_mgmt.py` 重建 `data-mgmt.json`；期望 `frontN=48 genN=48 driftKeys=0 FAIL=False`。

- **症状 5**：V11 的 563360 / 159201 赔率为 `None`，若按 `(odds or 0)` 渲染会显示「赔率 0.00」，像真实的极差赔率。
- **根因 5**：这两只历史样本不足，V11 未生成赔率/止损；0 是缺省值不是计算结果。
- **修法 5**：`odds is None` 时写「赔率 —（数据不足）」、说明「历史样本不足，赔率/止损未生成」、`strength=0` 仅用于排序。**不要把缺数据说成 0 赔率。**

- **别碰**：发现层不接预算/不写交易状态；不登记 <30% 回撤指数；计数读 `meta.counts` 不写死；`gen_discovery.py` 不写 `data/*.json` 源文件；改 `index.html` 后先跑 `check_js` / `check_html_comments` / `check_globals` / `verify_manifest` / `_audit_dm_v845`。


### P-v1156 · 网格计划三处坑：tab 列数写死 8 / 截图空白不等于 CSS 空白 / 改步进后 T13 行“消失”

**症状 1**：新增第 9 个页签后，538 视口 9 个 tab 分成两行，第 9 个「网格计划」掉到第二行。
- **根因**：`#stratTabs` 的窄屏媒体查询仍写 `repeat(8,minmax(0,1fr))`，新增第 9 个按钮没有列。
- **修法**：改 `repeat(9,minmax(0,1fr))`，同时把 gap 4→3px、字号 10→9.5px、padding 7px 2px→7px 1px；改完必须真实 538 截图确认单行，不能只改桌面栅格。
- **别碰**：以后再加 tab，必须同步媒体查询列数与桌面 `grid-template-columns`。

**症状 2**：BrowserUse 截图整片空白，误以为 `#stp-gd` CSS 塌了；实际 DOM 已有 `.gd-kpi` 文本。
- **根因**：页面刚导航/数据尚未完成渲染时截图，或前台 tab 未聚焦强制重绘；不是布局空白。
- **修法**：先等 `page_info().ph > 1000`，再 `click_xy` 聚焦/重绘后截图；用 `elementFromPoint` 或 `get_page_text` 证明 DOM 有内容，再判断视觉。**不要把空白截图当 CSS 证据**。

**症状 3**：把 012920 步进从 3% 改到 5% 后，交易信号页找不到该只 T13 行，误判“T13 联动失效/行丢失”。
- **根因**：5% 时该行从「接近」落到「观察」，而观察组默认折叠在「显示观察 N 条」里；DOM 中仍有该行。
- **修法**：先展开观察组再查；本次已实测文案变「距上次买入跌 5% / 还需跌 14.0%」，证明逐只配置已生效。恢复全局后回 3%。
- **别碰**：不要为“让行可见”把观察行强行提到行动组；判定档位由 `SIGNALS_CFG` 决定，不改展示凑数。

**症状 4**：`_audit_plan_merge_v895.py` 的 A01 写死 8 个 tab，新增第 9 个后发布前 FAIL。
- **根因**：审计断言是结构白名单，不随前端自动扩展。
- **修法**：A01 期望列表扩为 `alloc, bt, bt, param, dd, v11, sf, gd, review`，新增 A01g 断言 `data-st="gd">网格计划<`、`#stp-gd`、`name === 'gd'`、`gdRender`、`fw2_grid_plan_v1`；其余 40 项未放宽，42/42 PASS。
- **别碰**：不要用“去掉 tab 断言”换发布通过。

**症状 5（文档事故）**：本轮用 `Write` 只写新章节，导致 `docs/FRONTEND.md` 被覆盖成 4 KB。
- **根因**：`Write` 是整文件覆盖，不是追加；对已有长文档必须先 `Read`/追加，禁止用 `Write` 只传增量。
- **修法**：已从 `D:\Temp\FRONTEND.md.bak_v1055pre` 恢复主体（73,139 B / 509 行），并补 §10.49–§10.51 当前摘要；v1056–v1155 的 §10.x 明细仍缺，文件头已标注“恢复说明”，后续从备份/README/INBOX 逐版补回。
- **别碰**：不要再对 `FRONTEND.md` / `INBOX.md` / `PITFALLS.md` 用 `Write` 传单节；追加一律 `open(...,'a')` 或 `Edit` 精确替换。


### P-v1157（2026-11-27）：网格已用 / 发现层六源 / 策略工厂 v2

**症状 1**：`ttskill invoke TRADE_QUERY --body '{"body":...}'` 在 Windows PowerShell 下报参数解析失败，JSON 引号被剥掉。
- **根因**：`ttskill` 是独立可执行入口，PowerShell 会把内联 JSON 重新分词，双引号不保证原样传入。
- **修法**：先把 `{"body":{...}}` 写进临时 JSON 文件，再 `--body D:\Temp\trade_query_body.json`；返回取 `data.raw_result.body.trade_list_result.trades`。窗口固定 `2024-01-01`、`statu=2`、`pageSize=500`，`totalCount>=500` 判可能截断，保留旧值并 `ok=false`。
- **别碰**：不要为了“一次查全”去掉单页 500 上限判断；不要把 `confirmCount` 字符串直接 `sum()`。

**症状 2**：`gen_grid_usage.py` 写 `holdings-data.json.gridUsage` 后，前端仍读不到，`gdUsage` 返回空。
- **根因**：前端读的是内嵌 `window.HOLDINGS_SEED`，只改外部 JSON 不调 `_sync_holdings_inline.py` 不会同步。
- **修法**：生成器写完必须调 `_sync_holdings_inline.py`，把整个 holdings-data dump 进 `HOLDINGS_SEED`；`gdUsage` 只读 `window.HOLDINGS_SEED.gridUsage`，不新增 `window.__GRID_USAGE__`（`check_globals` 会拦新顶层键）。
- **别碰**：不要把 `gridUsage` 写成独立 `data/grid-usage.json`（会多一处发布登记与同步口径）。

**症状 3**：策略工厂组合级回测的基准直接用了组合自身再平衡曲线，导致“跑赢基准”虚高。
- **根因**：基准若也按月度再平衡，和策略承担相同的换手与权重漂移，失去可比性。
- **修法**：`sfPortBacktest` 的基准固定为「起点可用标的等权买入持有、不再平衡」；组合侧才做月度首个交易日再平衡。
- **别碰**：不要把基准改成等权再平衡；不要把 `t−1` 信号改到 `t` 收盘才知道。

**症状 4**：`docs/FRONTEND.md` 用 `Write` 只传新章节，整文件被覆盖成 4 KB。
- **根因**：`Write` 是整文件覆盖，不是追加。
- **修法**：已从 `D:\Temp\FRONTEND.md.bak_v1055pre` 恢复主体，补 §10.46 索引与 §10.49–§10.52；本轮 v1157 用 `read_text + append` 写入。
- **别碰**：对 `FRONTEND.md` / `INBOX.md` / `PITFALLS.md` 禁止 `Write` 单节；追加用 `open(...,'a')` 或 `Edit`。

### P-v1158（2026-11-27）：网格起算日 / 策略工厂同日收盘前视 / 两个 v1156 遗留渲染 bug

**症状 1**：策略工厂注释写「信号只用截至前一交易日收盘」，但动量 Top3/60 旧结果 −24.58% / MDD −56.66%，改成 t−1 后同一参数变 −19.86% / −55.77%。
- **根因**：`sfPortBacktest` 用 `idx[c][day]` 当下标，p1 取当日收盘、p0 取 `ii-look`，等于用当日收盘价判断当日信号再按当日收盘成交。
- **修法**：`bi=ii-1` 作 p1、`jj=bi-look` 作 p0；`ii<1` 或 `jj<0` 直接跳过；成交仍按当日收盘。旧数字全部作废，敏感性重跑（新最高 Top5/120 +160.70% / Calmar 0.31）。
- **别碰**：不要把 p1 改回 `ii`；不要改成「次日开盘成交」而不重算全表；不要把旧 −24.58% 写进任何新文档。

**症状 2**：点「网格计划」页签，按钮高亮但 `#stp-gd` 高度 0、`innerHTML` 长度 0，无 `GD_RENDER_ERR`。
- **根因**：`switchStratTab` 末尾懒渲染白名单是 `alloc/review/param/dd/v11/sf`，v1156 新增的 `gd` 没加进去；tab 只切显示，`gdRender` 从未执行。
- **修法**：白名单补 `|| name === 'gd'`；`__stratPaneRender` 内已有 `gdRender` 分支和 try/catch。验收必须看 `#stp-gd.offsetHeight > 0`，不能只看按钮 active。
- **别碰**：不要用「页面加载时预渲染全部 pane」绕过；v1017 懒渲染是性能约定，补名单才是正解。

**症状 3**：本地/线上 `?view=strategy` 控制台报 `ReferenceError: renderStrategyView is not defined`，策略页看着有内容但实际是静态骨架。
- **根因**：早期 script 块在 `DOMContentLoaded` 即按 URL 的 `view=strategy` 调 `renderStrategyView()`；该函数在文档靠后的策略块末尾才 `window.renderStrategyView = ...`，此时尚未导出。用 `window.STRATEGY_SNAP` 判断会误判：`bu.js` 可能在隔离执行上下文，看不到页面全局；正确证据是 DOM 高度、控制台错误与页内 dataset 标记。
- **修法**：分派处改 `if (typeof window.renderStrategyView === 'function') window.renderStrategyView(); else window.addEventListener('load', ..., {once:true})`；验收看控制台无 ReferenceError 且 `#view-strategy` 高度 >0。
- **别碰**：不要把整个策略块提前到 `<head>`；不要把 `STRATEGY_SNAP` 巨型赋值拆成异步 fetch，会改变首屏可用时点。

**症状 4**：给策略工厂页脚加「固定起点池」条件文案后，点策略工厂报 `SF_RENDER_ERR cfg is not defined`，整页空白。
- **根因**：页脚在 `sfShellHtml()` 里只渲染一次，该函数没有 `cfg` 参数；误把 `sfResultHtml(R,cfg)` 的作用域当成页脚作用域。
- **修法**：页脚改成不依赖 `cfg` 的双口径静态说明；`sfResultHtml` 内才用 `cfg.poolmode` 拼结果头。
- **别碰**：不要在 `sfShellHtml` 里读运行后的 cfg；shell 在首次进 tab 时就要能独立渲染。

**验证口径（v1158）**：`check_js` 22 块 ALL OK；`check_html_comments` 377 处 0 隐患；`check_globals` 282 键 / 434 赋值点 PASS；`check_hold_consistency` PASS=9 WARN=2 FAIL=0；`verify_manifest` 43 数据集 PASS（1 项既有 W2）；`_audit_dm_v845` FAIL=False；`_audit_plan_merge_v895` 42/42 PASS；`verify_sync --gh-only` 六文件字节一致。本地 538 与线上均实测：012920 默认 ¥0/10k/0 笔，设 since=2025-01-01 变 17 笔 ¥8,700；策略工厂 Top3/60 出 −19.86%，固定池出 +59.52%。

## P-v1159 改了默认选项，页面打开仍是旧口径（保存结果覆盖默认）

- 症状：`sfShellHtml` 已把「组合池」默认改成 fixed（`selected` 也加了），打开策略工厂仍显示「当时可用池」，结果头「池 15只」。
- 证伪：看 `#sfRunMsg` 是否写「已恢复本机保存的最近一次结果」；是＝页面在用 `sfSaved()` 的旧 cfg 覆盖表单，不是 `selected` 没生效。
- 根因：`sfRender` 的恢复分支先 `sfApplyCfg(saved.cfg)`，旧缓存 `poolmode='pit'` 把 select 改回 pit；HTML 的 `selected` 只在首次 `innerHTML` 时有效。只改默认值、不改恢复逻辑，新默认永远看不到。
- 修法：`sfSave` 写入 `ver:'v1159'`；`sfRender` 恢复时只在 `saved.ver !== 'v1159'` 且 poolmode 为 pit/缺省时，把 cfg 改 fixed 并按同参数 `sfRun()` 重算一次；带 ver 的手选 pit 正常恢复。**不要**用 `savedAt` 日期判断（时区会错），也不要在每次恢复时无条件改 fixed（会把手选 pit 吃掉）。
- 验证：旧缓存首开 → 表单 fixed、结果「池 7只」；手选 pit 并运行 → 重载仍 pit「池 15只」。
- tag：`fw2_v1159_sf_default_fixed`

## P-v1160 网格页只看 5 / 22、¥5,000，但配置明明写了 7 只（过滤误伤，不是迁移失败）

- **症状**：`localStorage.fw2_grid_plan_v1.funds` 已是七只（012920/001015/160422/000307/022438/012761/023917），页面 KPI 却是「已启用 5 / 22」「上限 ¥5,000」「一次全触发 ¥2,500」，卡片总数 22；期初预期 7 / 22、¥6,000。
- **证伪**：先读 `localStorage` 看七只是否写入；已写入＝迁移成功，问题在卡生成/过滤。再读 DOM 卡片代码：`012761`、`023917` 不在 `[data-gd-card]`。别先怪 `gdMigratePreset`。
- **根因（两处叠加）**：①旧过滤 `/货币|活期宝|现金/` 命中 023917「华夏国证自由现金流ETF发起式联接A」名称里的「现金」；②旧过滤 `status === 'off'` 把台账状态 off、但 `holdRows` 账户镜像仍有份额的 012761/023917 整卡排除。两只各 ¥500，正好少 ¥1,000 / 2 只。
- **修法**：新增 `gdIsCashRow(r)`——现金只认 `assetType==='cash'`（含 `_h.assetType`）或 `cat==='现金'`，名称只认「活期宝 / 货币基金 / 现金宝」；新增 `gdIsGridRow(r)`——`status==='off'` 仅当 `shares<=0 && mv<=0` 才排除；`gdCardsHtml` 与 `gdRender` 共用，页面 24 卡 / 7 启用 / ¥6,000 / ¥3,500。
- **验证**：本地/线上 538 真实渲染 KPI 与 7 个勾选码一致；012920 取消→6 / ¥4,500、再勾→7 / ¥6,000；「全部恢复默认」仍 7 / ¥6,000；线上 T13 七只带「预算内（逐只计划）」，012761/023917 有行，020712/000746/019441/017641 为「已关闭」。
- **别碰**：不要用宽泛 `/现金/`（023917 会被误伤；含「现金」但非现金的基金同样会被误伤）；不要用 `status==='off'` 一刀切隐藏账户仍有份额的基金；不要把 `assetType` 当成 `holdRows` 顶层字段（实际在 `r._h.assetType`）；不要改全局 `gridFund=10,000` 来凑页面数字。
- tag：`fw2_v1160_grid_budget_6000`；验收截图 `D:\Temp\v1160_gd_538.png` / `v1160_gd_card_538.png` / `v1160_online_gd_538.png`。

## P-v1161 波动率卡显示 19/28/24，但总资产口径应是 12/18/15（现金被漏掉 + 覆盖率分母错）

- **症状**：`#volKpi` 60/120/250 日显示 **19.18% / 28.71% / 24.47%** 全高位；同一持仓离线按总资产（含 37.6% 现金）算却是 **12.00% / 17.98% / 15.31%**。页脚覆盖率一处 62%、另一处 100%。
- **证伪**：先用 `holdings-data.json` 的 `marketValue/total` 加 `nav-hold.json` 全日期复算 `Σw*r / Σw`（现金按 0）；若得 12/18/15，说明页面漏了现金权重，不是数据源不同。再查 `portReturns`：旧实现只遍历有净值序列的行，现金 `000912/020097` 在 `serMap` 无序列时直接跳过，`a.w` 只累计非现金，`a.s/a.w` 把「非现金部分」归一成 100%。
- **根因（两处）**：①`portReturns` 没把 `assetType==='cash'` 作为 0 收益/满权重计入，总资产组合被当成非现金组合；②`CACHE.meta.cov = inc/W.total`，`inc` 只统计有序列的行——现金有序列时覆盖率被抬到 100%，没序列时只剩 62.4%，且标签写「非现金覆盖」但分母是总资产。另：`riskContribs` 传了含现金的 `wrows` 与归一化后的非现金 `pr`，`wsum` 含现金，贡献合计只有 62.4%，不是 100%。
- **修法**：`portWeights` 增 `isCash`；`portReturns` 先收集全部净值日，现金在每个日期加 `w*0` 与 `w`，非现金按自身日历加收益/权重，最后 `a.s/a.w`；`CACHE.vol` 用总资产 `pr`；另算 `prNC=portReturns(非现金)` 供 `riskContribs`，并只传非现金 `wrows`，贡献合计 100%；`CACHE.meta.cov=inc/ncTotal`（`ncTotal` 非现金总市值），`cashW=cash/W.total`；页脚印「非现金净值覆盖 X%；现金 Y% 按 0 波动计入」。
- **验证**：本地/线上 538 均 12.00/17.98/15.31，20 日 13.03 vs 沪深300 14.36；风险贡献 012920 63.6% / 160422 14.1% / 001015 10.7% / 022438 2.3% / 022676 2.1%，合计 100%；覆盖率 100%、现金 37.6%；538 `body.scrollWidth=clientWidth`，参考带 10.5px 换行完整。`check_js` 22 块 ALL OK、注释 382 处 0 隐患、`check_globals` 282 键 / 434 赋值点 PASS、`check_hold_consistency` PASS=9 WARN=2 FAIL=0、`verify_manifest` PASS；`verify_sync --gh-only` 首段确认 5,635,501 B 字节一致（全量标记扫描超过 5 分钟已停止，未跑完）。
- **别碰**：不要把 `portReturns` 的现金 0 波动删掉；不要把 `riskContribs` 的 `prNC` 换回总资产 `pr`（会把贡献合计压到 62.4%）；不要用 `inc/W.total`；不要把 10%/15% 当交易冻结阈值；不要接 P2-9/P2-11/网格。
- tag：`fw2_v1161_vol_monitor` / `fw2_v1161_vol_top`；验收截图 `D:\Temp\v1161_vol_538c.png` / `v1161_vol_foot_538d.png` / `v1161_topalert3_538.png` / `v1161_online_top_538b.png`。

## P-v1162 清仓 what-if 显示 5.69/5.09/5.80，本地却是 6.15/7.20/6.51（现金日历污染估值日）

- **症状**：同一份持仓与净值，线上 538 的「清仓」行 60/120/250 日显示 **5.69% / 5.09% / 5.80%**，本地显示 **6.15% / 7.20% / 6.51%**；20% 与 15% 两档两边都是 10.52/15.33/13.10、9.34/13.19/11.32，KPI 也都 12.00/17.98/15.31，只有清仓档分叉。
- **证伪**：在页面主世界用同一份 `HOLDINGS_SEED` + `__NAV_SERIES__` 复算清仓：若 `allDs` 并入现金行日期，得 5.69/5.09/5.80；若只取非现金净值日、现金在这些日期按 0，得 6.15/7.20/6.51。再查 `__NAV_SERIES__`：000912 有 4,114 个日期（货币基金含周末），020097 有 878 个；清仓后 012920 收益消失，现金-only 日期的 0 收益把年化压低；20%/15% 档 012920 仍有收益，差异被掩盖。
- **根因**：`portReturns` 的 `allDs` 由全部 `wrows` 的 `serMap` 日期并集生成，包含 `isCash` 行的货币基金日历；`annVolOf` 按「最后 N 个日收益」取窗口，现金-only 日期的 0 收益被当成交易日计入。
- **修法**：`allDs` 循环加 `if (o.isCash) return;`，估值日只取非现金净值日；现金行仍在这些日期加 `o.w*(r[d]||0)` 与 `o.w`。修后本地/线上清仓档统一 6.15/7.20/6.51，KPI 与 20%/15% 档不变。
- **验证**：本地 `?t=v1162local4` 与线上 `?t=v1162live2` 均显示 6.15/7.20/6.51；`#volWhatIf` 483×129、`scrollWidth=483`，`body 529/529` 无横向溢出；`check_js` 22 块 ALL OK、注释 383 处 0 隐患、`check_globals` PASS、`check_hold_consistency` PASS=9 WARN=2 FAIL=0、`verify_manifest` PASS、`_audit_plan_merge_v895` 42/42。
- **别碰**：不要把货币基金日历并回 `allDs`；不要只用 `__NAV_SERIES__` 的日期覆盖做判断（要看 `isCash`）；不要把清仓档 6.15% 当「卖出后一定实现」的预测，它是历史样本机械重算。
- tag：`fw2_v1162_vol_whatif`（`v1162b`）；验收截图 `D:\Temp\v1162_online_whatif_final_538.png` / `v1162_whatif_538b.png`。

## P-v1163 把「10%」当成波动率线 / 把 20% 当成回撤预算（口径混用）

- **症状**：v1161/v1162 页面上有「<10 正常 / 10–15 预警 / ≥15 高位」参考带，用户问「10% 是什么硬指标」，并明确「年化收益率目标 10%，波动率 20% 以内」；若继续用 10%/15%，会把收益目标误读成波动率上限。
- **证伪**：先看 `WIN` / `WINS` / `VOL_WARN` / `VOL_HIGH` 常量与 `#volFoot` 原文——10%/15% 是展示带，不是交易阈值；再去 `tgThesis` 看 `tgtAnn` 默认 10、`ddBudget` 默认 20，确认 10 是收益目标、20 是回撤预算，二者都不是波动率线。
- **根因**：v1161 把 10% 借来当「预警线」以配合首屏提示，但页面没有区分「收益目标」与「波动率阈值」，导致同一数字被两种含义复用。
- **修法**：`VOL_CAP=20` 单列为波动率上限；`#volTopAlert` 只在 ≥20% 显示；`band/chip` 改二元「正常 / 超上限」；`#volKpi` 的 10% 改从 `tgThesis().tgtAnn` 读取并标注「投资总纲，非本卡指标」；`#volFoot` 明写 20% 只读监控、不冻结买入。
- **验证**：线上 538 三格 12.00/17.98/15.31 全绿「正常」，首屏无超限条；KPI 行同时出现「20% 上限」与「年化收益目标 10%（投资总纲，非本卡指标）」；`#volFoot` 完整可见；what-if 三档数值未变。
- **别碰**：不要把 `VOL_CAP=20` 与 `tgThesis.ddBudget=20` 当成同一个 20%；不要把 20% 接买入冻结（当前只监控）；不要把 10% 写回 `VOL_WARN` 当波动率线。
- tag：`fw2_v1163_vol_cap20`；验收截图 `D:\Temp\v1163_online_vol_538.png` / `v1163_online_foot_538.png` / `v1163_vol_top_538.png`。

## P-v1164 把「当前权重回溯 6.44%」当账户实际年化 / 波动率卡读不到总纲全局

- **症状**：页面上首次出现「组合年化收益 +6.44%」，容易被读成账户真实收益；同时波动率卡原本依赖 `window.tgThesis()`，在持仓视图下总纲模块未渲染时该全局不存在，`volCap` 取不到。
- **证伪**：用 Python 对同一份 `__NAV_SERIES__` + 当前权重复算，6.44% 对应「按当时可用净值归一」的当前权重回溯，不是账户实际持仓；再用账户 `holdProfit/cost` 复算，得累计 +7.75498%、年化 +7.34%。`capital-balance.json` 的 `tx=0`、`ledger-import.json` 缺 11-06 至 11-25，说明资金加权 IRR 不可算，不能用 6.44% 冒充。
- **根因（两处）**：①`annRetOf` 用的是当前权重重放历史，早期缺 012920 等权重时 `portReturns` 按当时可用净值归一，权重被抹掉，不是账户真实持仓；②`draw()` 直接调 `window.tgThesis`，总纲未渲染时该函数未挂全局。
- **修法**：新增 `actualRetOf(W,asOf)`，用 `holdProfit/cost` + 首笔买入到最新净值折算；`portWeights` 汇总 `cost/profit/firstBuyDate`；`CACHE.meta.act` 存实际、`CACHE.meta.ann` 保留回溯参考；`draw()` 直接读 `localStorage.fw2_tg_thesis.volCap`（默认 20），不再依赖 `window.tgThesis`；总纲四键化，`volCap` 范围 1–80。
- **验证**：538 DOM 读数「组合实际年化收益 +7.34%（账户持有收益/成本 2025-11-05→2026-11-25） · 目标 10% · 低于目标 2.66pct」；页脚实际与 6.44% 参考两套口径完整；真实 UI 写 22 后卡联动「22% 上限内，最高 120日 17.98%（距上限 4.02pct）」、`tgGoalTxt` 变「≤22% 波动」，再改回 20 恢复。
- **别碰**：不要把 +7.34% 写成资金加权 IRR 或已实现收益；不要把 6.44% 当账户实际持仓；不要只改 `tgThesis` 而不改卡内 `localStorage` 读取（持仓视图会回退 20）；不要把 `volCap` 与 `ddBudget=20` 混为同一个 20%。
- tag：`fw2_v1164_tgt_volcap_return`；验收截图 `D:\Temp\v1164_act_kpi2_538.png` / `v1164_act_foot_538.png` / `v1164_tg_table_values_538.png`。
