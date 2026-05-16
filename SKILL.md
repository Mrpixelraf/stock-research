---
name: stock-research
description: 把「像素先森 v3.1 上市公司深度分析 Pipeline」固化为可一条命令触发的三阶段工作流——后台子 agent 强制采集一手财报（WebFetch ≥ 5）、主会话分段写 15k 字深度报告（11 模块 + 15 红队节点 + 5 XML schema）、python 质检。Use when user says 深度分析、用我的框架分析、研报、company deep dive、deep dive、个股研究、estimate fair value of a stock. 适用于美股/港股/A 股上市公司的客观估值与投资评级。
---

# stock-research · v3.1 公司深度分析 Pipeline

把一家上市公司从「股票代码」变成一份带评级、目标价、置信度的客观深度分析报告。三阶段流水线，每阶段在安全边界内独立可重试。

## 使用时机

- 用户说「深度分析 XXX」「用我的框架分析 XXX」「给我一份 XXX 的研报」「company deep dive on XXX」
- 用户给出一个股票代码 / 公司名并要求估值、投资评级、目标价
- **不触发**：只问「XXX 股价多少」「XXX 财报哪天发」这类单点查询——直接答即可，不必走 Pipeline

## 为什么是三阶段（硬约束的由来）

单 agent 端到端「一口气写 30-50k 字」会失败：工具权限不足、超时、monolithic Write 超限。拆成三阶段后每个子步骤在安全边界内、独立可重试。**这是踩过坑的结论，不要回退成单 agent。**

## 工作流

### Phase 1 · 合并采集（后台子 agent，10-15 分钟）

用 `Agent` 工具起一个 **general-purpose 子 agent**，`run_in_background: true`。brief 模板见 `references/phase1-brief.md`，套用时只换公司名/代码/财报年度。

铁律：
- **WebFetch ≥ 5 次硬性下限，≤ 12 次上限**。写成「≥ N 次」，禁止写成「≤ N 次预算」——否则 agent 会偷懒用 WebSearch 摘要代替原文，DS-5 直接归零。
- 必须真正打开 PDF / 10-K / IR 原文。优先级清单 Top 6：最新季报 IR PDF、最近年报（10-K / 港交所年报）、投资者 presentation、同业对标公司财报、Damodaran 行业数据、卖方深度研报——至少打开 4 份。
- 产出 `数据台账.md`，每条数据点标 `[DS-5/DS-4/DS-3]`（DS-5=一手原文财报数字，DS-4=权威二手，DS-3=媒体摘要），注明来源 URL 与日期。目标 DS-5 ≥ 20 条。

子 agent 完成后若 **DS-5 < 10 或 gap > 7**，立刻再起一个 Phase 1.5 PDF 深挖补丁 agent 补齐，再进 Phase 2。

### Phase 2 · 主会话分段 Write（15-30 分钟）

读 `数据台账.md`，按 `references/report-spec.md` 的 11 模块结构，**分 3 次 Write** 落盘（不要一次性 Write 全文，会超限）：

- **Write 1**：封面 + 元数据 + M-01 执行摘要 + M-02 公司解析 + M-03 财务深度（嵌 RT-01~08）
- **Write 2**：M-04 估值 + M-05 行业 + M-06 增长 + M-07 情景（嵌 RT-09~13）
- **Write 3**：M-08 投资建议 + M-09 ESG + M-10 管理层 + M-11 附录 + RT-14~15 + 5 个 XML schema

分段技巧：Write 1 末尾留 `<!-- SEG2 -->` 锚点，后两段用 `Edit` 替换锚点续写。

目标：15k 中文字 / 11 模块全 / 15 红队节点全 / 5 XML schema 全 / DS-3 以下占比 < 15%。

### Phase 3 · 质检 + 沉淀

跑 `scripts/qa_check.py <报告路径>` 校验中文字数、RT 节点数（须 15）、XML schema 数（须 5）、模块数（须 11）。

然后简报回用户：评级 / 目标价 / 置信度 / 关键 gap / 字数。若字数不达标或红队节点缺失，回 Phase 2 补。

## 输出规范

- **目录**：`03_投资研究/个股研究/{代码}_{公司名}/`
- **文件**：`数据台账.md` + `{YYYY-MM-DD}_{Ticker}_{公司}_深度分析报告.md`
  - ✅ `2026-05-16_SOFI_SoFi_深度分析报告.md`
  - ❌ `深度分析报告.md`（无 Ticker，上传 Notebooks 后无法区分）
- **报告本体**：见 `references/report-spec.md` —— 11 模块 + 15 红队节点 + 5 XML schema

## 关键原则

1. **能打开的 PDF 一定打开** —— WebFetch 是强制动作不是预算选项。这是「上市公司财报识别及分析」的核心能力，不打开 PDF 等于把最硬的本事挂着不用。
2. **红队节点是反叙事偏误的免疫系统** —— 15 个 RT 节点必须真的「唱反调」，不能写成对管理层叙事的复述。每个 RT 要落在一个具体的会计科目 / 假设 / 数据缺口上。
3. **目标价必须三方交叉验证** —— 相对估值 + 绝对估值（DCF / 剩余收益）+ 情景概率加权，三者收敛才给目标价。
4. **置信度要诚实** —— 关键数据缺口（如做空报告原文未核实）必须在 RT-14 显式声明并下调置信度。
5. **黑客松倒计时 > 报告优雅度** —— 结构完整优先于辞藻。

## 完整示例

输入：`深度分析 SOFI` →
1. 起 Phase 1 子 agent（后台）→ 产出 `SOFI_SoFi/数据台账.md`（DS-5 ≥ 45 条，WebFetch 8 次）
2. 主会话 3 段 Write → `2026-05-16_SOFI_SoFi_深度分析报告.md`（评级增持 / 目标价 $18 / 置信度中等）
3. `qa_check.py` 校验 → 简报：中文 7.4k 字、RT 15/15、XML 5/5、模块 11/11

## 验收（触发测试）

- ✅「深度分析 NVDA」→ 触发
- ✅「用我的框架给我一份台积电研报」→ 触发
- ✅「company deep dive on Palantir」→ 触发
- ❌「英伟达今天股价多少」→ 不触发（单点查询，直接答）
