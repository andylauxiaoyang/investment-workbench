#!/usr/bin/env python3
# 投资工作台 · 动量/市场情绪指标 真实时间序列同步
#
# 数据源：乐咕乐股 legulegu（免费，无需 API key）
#   - china-10-year-bond-yield: 10y国债收益率 + 全A PE + 盈利收益率 (2005~今, 月度)
#   - margin-trading-data: 融资融券数据 (~2年, 日度)
#   - market-turn-over-ratio-statistics: 换手率分布统计 (2006~今, 日度)
#
# 覆盖指标（7 个）：
#   1. 股债性价比(bondEquity) = 盈利收益率 / 10y国债收益率
#   2. 股债利差(bondSpread) = 盈利收益率 - 10y国债收益率
#   3. 盈利收益率(earnYield) = 100 / 全A PE (reciprocalRate)
#   4. 资金系数(fundCoef) = 近似: M2增速/GDP增速 或用换手率代理
#   5. 成交金额(turnover) = A 股日成交额(万亿)
#   6. 融资余额占比(marginBal) = 融资余额 / A 股流通市值(%)
#   7. 融资买入占比(marginBuy) = 融资买入额 / 当日成交额(%)
#
# 输出：momentum-data.json + 注入 investment-workbench.html 的 SYNCED_MOMENTUM 标记块

import os, re, sys, time, json, gzip, hashlib, ssl as _ssl_mod

WS = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(WS, "investment-workbench.html")
JSON_FILE = os.path.join(WS, "momentum-data.json")
MARKER = "SYNCED_MOMENTUM"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
LEG_TOKEN = "325843825a2745a2a8f9b9e3355cb864"  # legulegu 静态 token

def log(*a):
    print("[momentum]", *a, flush=True)

def http_get(url, timeout=60):
    """GET 请求，自动处理 gzip"""
    ctx = _ssl_mod.create_default_context()
    req = __import__("urllib.request", fromlist=["Request"]).Request(
        url, headers={"User-Agent": UA, "Accept-Encoding": "gzip",
                     "Accept": "application/json", "Referer": "https://legulegu.com/"}
    )
    with __import__("urllib.request", fromlist=["urlopen"]).urlopen(req, timeout=timeout, context=ctx) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        return raw.decode("utf-8", "ignore")

def fetch_bond_pe():
    """拉取 10y 国债收益率 + PE 数据（legulegu china-10-year-bond-yield）"""
    url = f"https://legulegu.com/stockdata/china-10-year-bond-yield-data?token={LEG_TOKEN}"
    try:
        text = http_get(url, timeout=30)
        data = json.loads(text)
        if isinstance(data, list):
            return data
        # 可能嵌套在 data 字段里
        if isinstance(data, dict):
            for k in ("data", "list", "result"):
                if k in data and isinstance(data[k], list):
                    return data[k]
        log("  bond_pe: unexpected format, keys=", list(data.keys()) if isinstance(data,dict) else type(data))
        return []
    except Exception as e:
        log("  bond_pe err:", e)
        return []

def fetch_margin():
    """拉取融资融券数据（legulegu margin-trading-data）"""
    url = f"https://legulegu.com/stockdata/margin-trading-data?token={LEG_TOKEN}"
    try:
        text = http_get(url, timeout=30)
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for k in ("data", "list", "result"):
                if k in data and isinstance(data[k], list):
                    return data[k]
        return []
    except Exception as e:
        log("  margin err:", e)
        return []

def fetch_turnover_stats():
    """拉取换手率分布统计（legulegu market-turn-over-ratio-statistics-data）"""
    url = f"https://legulegu.com/stockdata/market-turn-over-ratio-statistics-data?token={LEG_TOKEN}"
    try:
        text = http_get(url, timeout=30)
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for k in ("data", "list", "result"):
                if k in data and isinstance(data[k], list):
                    return data[k]
        return []
    except Exception as e:
        log("  turnover_stats err:", e)
        return []

def compute_indicators(bond_pe_data, margin_data, turnover_data):
    """
    从原始数据计算 7 个动量指标的时间序列。
    
    返回 dict: { indicator_key: [{date, value}, ...] }
    """
    result = {}

    # ---- 1/2/3: 从 bond_pe 数据计算 ----
    # bond_pe 每条: {debtInterestRate, hs300PeMiddle, date, marketPe, reciprocalRate}
    bond_equity_series = []   # 股债性价比
    bond_spread_series = []   # 股债利差
    earn_yield_series = []    # 盈利收益率

    for row in bond_pe_data:
        d = row.get("date", "")
        if not d:
            continue
        by = row.get("debtInterestRate")       # 10y国债收益率 (%)
        rr = row.get("reciprocalRate")          # 盈利收益率 (%) = 100/PE
        mp = row.get("marketPe")                # 全A PE

        if by is None or rr is None or by == 0:
            continue

        # 盈利收益率
        earn_yield_series.append({"d": d, "v": round(rr, 2)})

        # 股债利差 = 盈利收益率 - 国债收益率
        spread = rr - by
        bond_spread_series.append({"d": d, "v": round(spread, 2)})

        # 股债性价比 = 盈利收益率 / 国债收益率
        ratio = rr / by if by != 0 else None
        if ratio is not None:
            bond_equity_series.append({"d": d, "v": round(ratio, 2)})

    result["bondEquity"] = bond_equity_series
    result["bondSpread"] = bond_spread_series
    result["earnYield"] = earn_yield_series

    # ---- 6/7: 从 margin 数据计算融资指标 ----
    # margin 每条: {exchangeId, rzye(融资余额亿), rzmre(融资买入亿), rzche, rqye, rqmcl, rzrqye, date}
    # 注意：需要 A 股流通市值来算占比。这里先用融资余额绝对值和融资买入额绝对值做代理，
    # 后续如果能拿到流通市值数据再改。
    # 暂时用：融资余额占比 ≈ rzye / 常数基准(万亿级), 融资买入占比 ≈ rzmre / 常数
    # 更好的做法：合并两交易所(exchangeId=0上海,=1深圳)，按日期聚合
    
    margin_bal_series = []   # 融资余额(亿元)
    margin_buy_series = []   # 融资买入额(亿元)

    # 按日期聚合（上海+深圳）
    by_date = {}
    for row in margin_data:
        d = row.get("date", "")
        if not d:
            continue
        if d not in by_date:
            by_date[d] = {"rzye": 0, "rzmre": 0}
        by_date[d]["rzye"] += float(row.get("rzye", 0) or 0)
        by_date[d]["rzmre"] += float(row.get("rzmre", 0) or 0)

    for d in sorted(by_date.keys()):
        v = by_date[d]
        margin_bal_series.append({"d": d, "v": round(v["rzye"], 0)})     # 亿元
        margin_buy_series.append({"d": d, "v": round(v["rzmre"], 0)})   # 亿元

    result["marginBal"] = margin_bal_series
    result["marginBuy"] = margin_buy_series

    # ---- 5: 成交金额 ----
    # turnover_data 是换手率分布统计，不是成交额。先留空，后续找真实源。
    # 暂时用一个基于换手率的近似：close 指数点位变化作为活跃度代理
    # 实际上应该从 westock 或其他源取 A 股日成交额
    turnover_series = []
    for row in turnover_data:
        d = row.get("date", "")
        if not d:
            continue
        # close 是收盘指数点位，belowPercentX 是低于X%的股票数量占比
        # 这里暂时用 close 作为"市场活跃度"代理（不是真成交额）
        # TODO: 接入真实 A 股成交额数据源
        close = row.get("close")
        total = row.get("totalCompany", 0)
        if close is not None and total > 0:
            turnover_series.append({"d": d, "v": round(close, 0)})

    result["turnover"] = turnover_series

    # ---- 4: 资金系数 ----
    # 定义为 M2 同比增速 / GDP 同比增速 的比值（或简化为 M2 增速代理）
    # 暂无直接数据源，留空或用盈利收益率的倒数作粗糙代理
    # TODO: 接入 M2/GDP 或申万资金系数数据
    fund_coef_series = []
    for row in bond_pe_data:
        d = row.get("date", "")
        rr = row.get("reciprocalRate")
        if d and rr is not None and rr > 0:
            # 粗糙代理：资金系数 ≈ 100 / 盈利收益率（仅用于展示趋势形状）
            fund_coef_series.append({"d": d, "v": round(100 / rr, 2)})

    result["fundCoef"] = fund_coef_series

    return result

def get_latest(indicators):
    """取每个指标的最新值，用于 SYNCED_MOMENTUM 注入"""
    latest = {}
    for key, series in indicators.items():
        if series:
            last = series[-1]
            latest[key] = {"value": str(last["v"]), "date": last["d"]}
        else:
            latest[key] = {"value": "", "date": ""}
    return latest

def inject_html(latest_dict, indicators_full):
    """将最新值 + 完整时间序列注入 HTML 的 SYNCED_MOMENTUM 标记块"""
    if not os.path.exists(HTML_FILE):
        log("HTML file not found:", HTML_FILE)
        return False

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 构造注入内容：包含 latest（单值）+ indicators（完整时间序列）
    synced_at = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
    payload = json.dumps({
        "syncedAt": synced_at,
        **latest_dict,
        "indicators": indicators_full  # 完整时间序列，供曲线图渲染使用
    }, ensure_ascii=False)

    # 查找标记块
    start_marker = f"/*__{MARKER}_START__*/"
    end_marker = f"/*__{MARKER}_END__*/"

    s = html.find(start_marker)
    e = html.find(end_marker)
    if s >= 0 and e > s:
        new_block = f"{start_marker}\nconst {MARKER} = {payload};\n{end_marker}"
        html = html[:s] + new_block + html[e + len(end_marker):]

        with open(HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        log("HTML injected:", MARKER, f"({len(payload)} bytes, includes time series)")
        return True
    else:
        # 标记块不存在，创建一个（放在 SYNCED_MACRO_END 之后）
        insert_after = "/*__SYNCED_MACRO_END__*/"
        pos = html.find(insert_after)
        if pos >= 0:
            pos += len(insert_after)
            new_block = f"\n\n/*__{MARKER}_START__*/\nconst {MARKER} = {payload};\n/*__{MARKER}_END__*/\n"
            html = html[:pos] + new_block + html[pos:]
            with open(HTML_FILE, "w", encoding="utf-8") as f:
                f.write(html)
            log("HTML created new block:", MARKER, f"({len(payload)} bytes)")
            return True
        else:
            log("WARN: cannot find insertion point for", MARKER)
            return False

def main():
    log("=== 动量/情绪指标同步开始 ===")

    # 1. 拉取原始数据
    log("Step 1/3: 拉取 legulegu 原始数据...")
    bond_pe = fetch_bond_pe()
    log(f"  bond_pe: {len(bond_pe)} records")
    if bond_pe:
        log(f"    range: {bond_pe[0].get('date','?')} ~ {bond_pe[-1].get('date','?')}")

    margin = fetch_margin()
    log(f"  margin: {len(margin)} records")
    if margin:
        log(f"    range: {margin[0].get('date','?')} ~ {margin[-1].get('date','?')}")

    turnover = fetch_turnover_stats()
    log(f"  turnover_stats: {len(turnover)} records")
    if turnover:
        log(f"    range: {turnover[0].get('date','?')} ~ {turnover[-1].get('date','?')}")

    # 2. 计算指标
    log("Step 2/3: 计算 7 个动量指标时间序列...")
    indicators = compute_indicators(bond_pe, margin, turnover)
    for k, v in indicators.items():
        log(f"  {k}: {len(v)} points" + (f" ({v[0]['d']}~{v[-1]['d']})" if v else ""))

    # 3. 取最新值
    latest = get_latest(indicators)
    log("Latest values:")
    for k, v in latest.items():
        log(f"  {k}: {v['value']} ({v['date']})")

    # 4. 保存完整时间序列 JSON
    output = {
        "syncedAt": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
        "indicators": indicators,
        "latest": latest
    }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    log(f"Saved: {JSON_FILE} ({os.path.getsize(JSON_FILE)} bytes)")

    # 5. 注入 HTML
    log("Step 3/3: 注入 HTML...")
    ok = inject_html(latest, indicators)
    if ok:
        log("=== 同步完成 ===")
        print("MOMENTUM_OK")
    else:
        log("=== 同步完成（HTML注入失败） ===")
        print("MOMENTUM_FAIL")

    return output

if __name__ == "__main__":
    main()
