---
aliases:
  - ARS
  - Academic Research Skills
  - 学术研究管线
title: 学术研究技能套件(ARS, Academic Research Skills)
tags:
  - AI工具
  - ClaudeCode
  - 学术研究
  - 论文写作
description: >-
  ARS (Academic Research Skills) 是面向 Claude Code 的学术研究技能套件，覆盖
  文献调研→论文写作→同行评审→修订→定稿的完整管线。4 个核心 skill（deep-research /
  academic-paper / academic-paper-reviewer / academic-pipeline）、27 种模式、39
  智能体合奏。
type: concept
create-date: 2026-06-19
update-date: 2026-06-19
source: https://github.com/Imbad0202/academic-research-skills
status: stable
---

# 学术研究技能套件 (ARS, Academic Research Skills)

> 面向 Claude Code 的生产级学术研究全流程管线，由台湾开发者 Cheng-I Wu (吳政宜) 创建，GitHub 6.4k+ stars。License: CC-BY-NC 4.0。

## 核心定位

ARS 将学术出版流程拆解为四个独立阶段，各自封装为 Claude Code skill，由 `academic-pipeline` 编排成端到端管线。核心设计哲学：**AI 是副驾驶（copilot），不是飞行员**——所有关键决策需人确认。

## 四个 Core Skills

| Skill                     | 版本     | 智能体 | 职责                                                       |
| ------------------------- | ------ | --- | -------------------------------------------------------- |
| `deep-research`           | 2.11.0 | 13  | 文献综述、研究问题澄清 (Socratic)、PRISMA 系统评价、Semantic Scholar 事实核查 |
| `academic-paper`          | 3.2.0  | 12  | 论文起草、大纲、摘要、格式转换、引用校验、修订指导、AI 使用声明、反驳审计                   |
| `academic-paper-reviewer` | 1.10.0 | 7   | 模拟同行评审（EIC + 3 评审人 + Devil's Advocate + 编辑综合），0-100 评分   |
| `academic-pipeline`       | 3.13.0 | 编排  | 10 阶段管线编排器，协调上述三个 skill 的顺序执行                            |

## 完整管线流程

```
deep-research (socratic / full)
  → academic-paper (plan / full)
    → 完整性检查 (Stage 2.5) ← 第一道强制门
      → academic-paper-reviewer (full / guided)
        → academic-paper (revision)
          → academic-paper-reviewer (re-review, 最多 2 轮)
            → 最终完整性检查 (Stage 4.5) ← 第二道强制门
              → academic-paper (format-convert → 最终输出)
                → 流程总结 + AI 自评报告
```

## 关键机制

### 完整性检查门 (Integrity Gates)
- Stage 2.5 和 Stage 4.5 两道**强制门**
- 每次检查 7 种 AI 故障模式（基于 Lu et al. 2026, *Nature*）
- 合规失败 → 三级用户覆盖阶梯 (override ladder)，自动生成披露附录

### 引用真实性验证 (v3.11+)
- 四索引交叉验证：Semantic Scholar + OpenAlex + Crossref + arXiv
- 确定性验证门独立于 LLM 评审运行
- 本地 SQLite 缓存（90 天 TTL），跨草稿复用
- Levenshtein 相似度匹配阈值 ≥0.70

### 反谄媚机制 (Anti-Sycophancy)
- Devil's Advocate 智能体必须在反驳评分 ≥4/5 时才让步
- 帧锁定检测（检测用户是否在引导 AI 改变结论）

### 跨模型验证 (可选)
- 设置 `ARS_CROSS_MODEL` 环境变量启用非 Anthropic 验证器
- 支持 GPT-5.5 / Gemini 3.1 Pro 等

## 快捷命令

安装后提供 10 个 `/ars-*` 命令：

| 命令                    | 功能                                               |
| --------------------- | ------------------------------------------------ |
| `/ars-full`           | 端到端完整管线                                          |
| `/ars-outline`        | 仅输出论文大纲                                          |
| `/ars-plan`           | Socratic 对话式规划章节结构                               |
| `/ars-abstract`       | 仅输出摘要                                            |
| `/ars-lit-review`     | 文献综述模式                                           |
| `/ars-citation-check` | 引用格式与真实性校验                                       |
| `/ars-format-convert` | 格式转换（LaTeX/DOCX/PDF）                             |
| `/ars-disclosure`     | AI 使用声明生成（ICLR/NeurIPS/Nature/Science/ACL/EMNLP） |
| `/ars-revision`       | 按评审意见修订论文                                        |
| `/ars-revision-coach` | 修订指导（提供 Response Letter 框架）                      |

## 成本参考

- 一篇 15,000 词的完整管线运行 ≈ **$4-6**（API 调用费用）

## 安装方式

```bash
# 通过 Claude Code 插件系统
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills
```

或手动克隆并复制 skill 目录到 `~/.claude/skills/`。

## 适用范围

- 学术论文写作（中英文均支持，默认语言跟随用户输入）
- 系统文献综述（PRISMA 兼容）
- 同行评审模拟与修订
- 研究问题澄清与方案设计

## 关联笔记

- [[Claude Code 解决方案写作Skill调研(Solution Proposal Skills Research)]]
- [[80-知识体系|知识体系 MOC]]
