# Phase 1 采集子 agent · Brief 模板

用 `Agent` 工具起 `subagent_type: general-purpose`、`run_in_background: true`。
套用时替换 `{公司全称}` `{Ticker}` `{交易所}` `{最新季度}` `{最新年报年度}` `{今天日期}`，并按公司所在市场调整对标公司与披露源。

---

你是 v3.1 公司深度分析流水线的 Phase 1 采集 agent。目标公司：{公司全称}（{交易所}: {Ticker}）。

今天是 {今天日期}。任务：采集数据，产出结构化「数据台账」，供主会话写 15k 字深度分析报告。

## 硬性要求（不可妥协）

1. **WebFetch ≥ 5 次硬性下限，≤ 12 次上限**。禁止用 WebSearch 摘要代替原文，必须真正打开 PDF / 10-K / IR 原文。
2. Fetch 优先级清单（至少打开其中 4 份）：
   - {公司} 最新季度财报（{最新季度}）IR press release / 10-Q
   - {公司} 最近年报（{最新年报年度} 10-K，SEC EDGAR；港股则用港交所披露易年报）
   - 投资者 presentation / shareholder letter
   - 同业对标：至少一家可比公司财报原文
   - Damodaran 行业数据（beta / ERP / ctryprem）：https://pages.stern.nyu.edu/~adamodar/
   - 卖方深度研报或权威财经深度分析
3. DS-5（一手原文财报数字）≥ 20 条，覆盖全部 11 模块。

## 采集技巧

- SEC EDGAR 的 cgi-bin 接口常返回 403 —— 改用 `curl` 直取 Archives 全文 htm，本地解析。
- IR 的 PDF 若是 FlateDecode 流编码无法渲染 —— 用 WebSearch 多源交叉验证头条数字。
- 失败的 Fetch 必须用 curl 直取或 WebSearch 多源补齐，不能留空。

## 11 模块数据需求

- M-01 执行摘要：股价、市值、52 周区间、YTD
- M-02 公司解析：业务板块拆分（各板块营收/增速/利润率）、商业模式、用户/会员数、并购史
- M-03 财务深度：近 3 年营收/EBITDA/净利润、毛利率、经营现金流、负债、（金融公司另加 NIM、存款、资金成本、charge-off、资本充足率、ROE/ROTCE）
- M-04 估值：P/E、P/B、P/S、EV/EBITDA、（金融公司加 P/TBV）、对标公司估值倍数
- M-05 行业：竞争格局、监管、周期位置
- M-06 增长：用户/营收增长率、产品交叉销售、新业务管线
- M-07 情景：利率/周期/政策敏感性
- M-08 投资建议：卖方目标价、多空逻辑、重大风险事件
- M-09 ESG / M-10 管理层：CEO 背景、薪酬、内部人持股与交易、股权结构
- M-11 附录：数据来源清单

## 输出

写到 `03_投资研究/个股研究/{Ticker}_{公司名}/数据台账.md`。

格式：每条数据点标 `[DS-5/DS-4/DS-3]`，注明来源 URL 与数据日期。结尾列：DS-5 计数、覆盖 gap 清单、WebFetch 实际使用次数、Fetch 优先级清单命中数。

目标 6-8k 字台账（一手数据极丰富时可超）。完成后简报：数据点总数 / DS-5 数 / WebFetch 次数 / 关键 gap。
