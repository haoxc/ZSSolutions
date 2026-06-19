---
aliases:
  - Solution Proposal Skills Research
  - Claude Code 解决方案Skill调研
tags: [知识体系, AI工具, Claude Code, Skill, 调研]
title: Claude Code 解决方案写作Skill调研(Solution Proposal Skills Research)
description: 调研 Claude Code 生态中可用于解决方案/提案写作的 Skill 和插件——本地已有资源 + 第三方 marketplace + 组合方案
type: reference
create-date: 2026-06-19
---

# Claude Code 解决方案写作 Skill 调研

> 一句话结论：**没有现成的、开箱即用的成品 Skill**，但有三类资源可以直接使用或组合——第三方成品、已有 Skill 串联、参考案例按需定制。

## 核心可用资源

### 1. 第三方 Skill/插件（可安装）

| Skill | 来源 | 核心能力 | 安装方式 |
|-------|------|---------|---------|
| `proposal-writer` | `@gonzih/skills-sales` (npm) | 销售提案：执行摘要 + 方案匹配 + 定价 + ROI + 后续步骤 | npm 或市场安装 |
| `pitchcraft` | SkillsMP 市场 | 5 段说服框架 (Hook→Context→Proposal→Evidence→Ask)，含 **Solution Selling** 模式 | SkillsMP 安装 |
| `contracts & proposals` | `alirezarezvani/claude-skills` | 合同与提案工具包 | `/plugin marketplace add` → install |
| `rfp-responder` | 同上 | RFP/招标书响应生成 | 同上 |
| `deal-desk` | 同上 | 交易结构设计与提案 | 同上 |
| `doc-coauthoring` | SkillsMP | 结构化文档共创（Context→Refinement→Reader Test，3 阶段） | SkillsMP 安装 |
| `research-proposal` | `luwill/research-skills` | 学术研究提案，中英双语，Nature Reviews 风格，最少 40 篇参考文献 | GitHub 安装 |

安装示例（alirezarezvani 市场）：
```
/plugin marketplace add alirezarezvani/claude-skills
/plugin install engineering-skills@claude-code-skills
```

### 2. 已有 Skill 组合方案

用本地的 Superpowers 家族三个 Skill **串联**完成方案写作：

```
brainstorming（模糊需求 → 清晰 spec）
  → writing-plans（spec → 可执行计划）
  → pitchcraft 或 doc-coauthoring（计划 → 提案文档）
```

三个 Skill 的定位：
- **brainstorming**：需求澄清、范围收敛、风险预判
- **writing-plans**：分阶段计划、产出物清单、依赖关系
- **pitchcraft/doc-coauthoring**：结构化文档输出

### 3. 参考案例：多 Agent 协作写提案

来源：[Classmethod 2026.04](https://dev.classmethod.jp/en/articles/ishikawa_make-proposal/)。非技术销售用 Claude Code 搭建 6 人 AI 团队：

```
Researcher + Designer + Critic（并行）
  → Structure Coordinator（整合）
    → Writer ⇄ Editor-in-Chief（反馈循环）
```

关键发现：
- **Critic（魔鬼代言人）** 和 **Editor-in-Chief 的反驳循环** 对质量提升最大
- 高质量输入决定高质量输出：最花时间的是构建逼真的客户场景和需求信息
- 从 3 人团队扩展到 6 人后，TCO 对比从 2 列变成 3 种场景 + 4 种成本偏高情况的坦诚披露

## 评价与建议

### 推荐路径（按场景）

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 快速出稿，英文提案 | `proposal-writer` + `pitchcraft` | 成品，直接装 |
| 中文环境，定制化 | 自己建 `hxc-solution-writer` Skill | 可控性强 |
| 一次性使用 | brainstorming + writing-plans 串联 | 不建 Skill，直接写 |
| 学术/研究报告 | `research-proposal` | 专门的学术写作流程 |

### 本地自建 Skill 的定位空间

第三方 Skill 偏通用框架，缺少：
- 新能源/电力行业领域知识注入
- 中文方案书的排版规范（国标、行标）
- JBFG 项目特有的评审标准

→ **建议自建 `hxc-solution-writer`**，在 `pitchcraft` 通用框架上叠加行业模板和中文排版规则。

## 关联

- [[Claude Code沙箱配置与故障处理]] — Claude Code 运行环境配置
