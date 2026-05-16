# stock-research

> 像素先森 v3.1 上市公司深度分析 Pipeline —— 一个 Claude Code Skill

把一家上市公司从「股票代码」变成一份带**投资评级、目标价、置信度**的客观深度分析报告。

## 它做什么

输入 `深度分析 SOFI`，自动跑三阶段流水线：

| 阶段 | 动作 | 产出 |
|------|------|------|
| **Phase 1 采集** | 后台子 agent，强制 WebFetch ≥ 5 次打开 10-K / IR PDF / Damodaran / 同业财报 | `数据台账.md`（DS-5 ≥ 20 条） |
| **Phase 2 写作** | 主会话分 3 段 Write | 15k 字深度报告（11 模块 + 15 红队节点 + 5 XML schema） |
| **Phase 3 质检** | `qa_check.py` 校验字数 / 节点 / schema | 评级 + 目标价 + 置信度简报 |

## 设计哲学

1. **能打开的 PDF 一定打开** —— WebFetch 是强制动作，不是预算选项。一手财报数字（DS-5）才是研报的硬底气。
2. **红队节点是反叙事偏误的免疫系统** —— 15 个 RT 节点主动唱反调，每个落在一个具体会计科目 / 估值假设 / 数据缺口上。
3. **目标价三方交叉验证** —— 相对估值 + 绝对估值 + 情景概率加权，收敛才给数。
4. **置信度诚实挂钩数据缺口** —— 没核实的关键信息（如做空报告原文）必须显式声明并下调置信度。

## 安装

```bash
git clone https://github.com/Mrpixelraf/stock-research.git ~/.claude/skills/stock-research
```

下次新 Claude Code session 即可用「深度分析 XXX」「company deep dive on XXX」触发。

## 结构

```
stock-research/
├── SKILL.md                      # 触发器 + 三阶段工作流
├── references/
│   ├── phase1-brief.md           # Phase 1 采集子 agent brief 模板
│   └── report-spec.md            # 11 模块 + 15 红队节点 + 5 XML schema 规范
└── scripts/
    └── qa_check.py               # Phase 3 结构质检脚本
```

## License

MIT
