---
aliases:
  - DOCX Generation Skills Research
  - Markdown转Word工具调研
  - ck:DOCX生成 Skill调研
tags:
  - 知识体系
  - 工具调研
  - 方案撰写
title: Claude Code DOCX生成Skill调研(Markdown-to-Word Skills Research)
description: >
  调研 Claude Code 生态中 Markdown→DOCX 生成的知名 Skill——覆盖 Anthropic 官方 skill、社区插件、中文排版专用工具，含 JBFG 方案书导出场景的选型建议
type: reference
create-date: 2026-06-19
status: 草稿
source: Web 搜索 + 官方仓库 + npm/mcpmarket/skillsmp
---

# Claude Code DOCX生成Skill调研(Markdown-to-Word Skills Research)

## 结论

**JBFG 方案书导出 DOCX 推荐：huashu-md-html（出版级中文排版）+ Anthropic 官方 docx skill（轻量场景）组合。** huashu-md-html 在 158 页书籍项目上验证过，含中文字体预设和自动化目录/页眉/页码；Anthropic 官方 skill 适合简单导出和后续编辑（tracked changes、comments）。两者互补，不需二选一。

---

## 一、核心候选方案

### 1.1 Anthropic 官方 DOCX Skill

| 维度 | 详情 |
|------|------|
| **来源** | `github.com/anthropics/skills` → `document-skills/docx/` |
| **安装** | 内置，Claude Code 自动激活 |
| **创建方式** | `docx-js`（JavaScript/TypeScript 编程式生成） |
| **编辑方式** | 解包 ZIP → 编辑 OOXML XML → 重新打包 |
| **依赖** | pandoc / docx (npm) / LibreOffice / Poppler / defusedxml |
| **中文支持** | 基础（依赖 docx-js 的字体设置能力，无中文排版预设） |

**三个工作流：**

| 任务 | 工具链 |
|------|--------|
| **读取/分析** | pandoc 提取文本 + 批注 |
| **创建新文档** | docx-js 编程生成 |
| **编辑现有文档** | unpack.py → 编辑 XML → pack.py → validate.py |

**适用场景**：通用 DOCX 创建、带 tracked changes 的协同编辑、已有 reference.docx 模板的格式控制。

**局限**：无中文排版预设（首行缩进、中文字体族、行距），需在 JS 代码中手动配置每个段落和表格样式，中文长篇文档工作量较大。

### 1.2 huashu-md-html（出版级中文排版）

| 维度 | 详情 |
|------|------|
| **来源** | `github.com/alchaincyf/huashu-md-html` |
| **定位** | 万物→MD → 精美 HTML → 出版级 DOCX，四能力流水线 |
| **核心技术** | `python-docx` + 出版社预设 |
| **验证规模** | 158 页书籍，57 张图，9 章，单命令生成 |

**排版预设（开箱即用）：**

| 元素 | 效果 |
|------|------|
| 页面 | A5 (176×240mm) 或 A4 可选 |
| 章标题 | 24pt + 彩色分隔线 |
| 引用块 | emoji 自动着色（💡 琥珀 / ✅ 青 / ⚠️ 玫瑰） |
| 代码块 | 浅灰背景 + 橙色侧边栏 + JetBrains Mono |
| 表格 | 表头着色 + 灰边框 |
| 封面/TOC/页眉 | 长篇项目自动生成 |

**优势**：中文排版已内置，A4 学术/标书风格可直接用或微调预设；在一个 158 页实际项目上验证过可靠性。

**局限**：依赖 Python 环境，预设风格偏出版/书籍，调整为标书风格需要修改 python-docx 样式参数。

### 1.3 @clipg/w2w（中文 + LaTeX 专用）

| 维度 | 详情 |
|------|------|
| **来源** | `npm install -g @clipg/w2w`，Skill 安装 `npx skills add CliPg/md2word` |
| **定位** | Markdown→DOCX，LaTeX 公式 → OMML Word 原生公式 |
| **中文控制** | 字体族、字号、行高、首行缩进、对齐方式逐元素可配 |
| **字体映射** | 自动映射中文描述（「三号黑体」「五号宋体」）到程序参数 |

**优势**：中文字体映射是最精准的——直接用中文习惯描述字体（三号/四号/小四），不需要了解 CSS 或 python-docx 的内部参数名。LaTeX→OMML 对含公式的技术方案书有价值。

**局限**：npm 生态，功能聚焦于排版转换，缺少封面/TOC/页眉等长篇文档自动化。

### 1.4 Artifactry（多格式导出插件）

| 维度 | 详情 |
|------|------|
| **来源** | `github.com/jeremy193a/artifactry`（v0.3.0, 2026-05） |
| **安装** | `/plugin marketplace add artifactry` |
| **输出格式** | DOCX / PDF / PPTX / PNG-JPG carousel |
| **模板** | `reference.docx` 模板控制样式 |
| **组装能力** | frontmatter 路由 + `{{ include: }}` 片段注入 |

**优势**：多格式一键导出（同一份 Markdown 出 DOCX + PDF + PPTX），reference.docx 模板方式适合有现成标书模板的场景。

**局限**：依赖 Claude Code 插件系统，中文排版需在 reference.docx 中预定义样式（首次配置成本较高）。

### 1.5 Markwell（双向转换 CLI）

| 维度 | 详情 |
|------|------|
| **来源** | `npm install -g markwell` |
| **定位** | 双向文档转换器，Markdown ↔ DOCX |
| **特色** | 批量 glob 处理 + YAML 主题配置 |

**适用场景**：批量文档转换、需要 DOCX→MD→DOCX 往返的场景。对 JBFG 单次长篇导出 overkill。

---

## 二、横向对比

| 维度 | Anthropic 官方 | huashu-md-html | @clipg/w2w | Artifactry |
|------|:---:|:---:|:---:|:---:|
| **中文排版** | ⚠️ 需手动配置 | ✅ 内置预设 | ✅ 逐元素可控 | ⚠️ 依赖模板 |
| **长篇稳定性** | ⚠️ 未验证 | ✅ 158 页验证 | ⚠️ 未验证 | ⚠️ 未验证 |
| **Cover/TOC 自动** | ❌ 需编程 | ✅ 自动 | ❌ | ⚠️ 依赖模板 |
| **表格处理** | ✅ docx-js 完整 API | ✅ 表头着色 | ⚠️ 基础 | ✅ 继承模板 |
| **数学公式** | ❌ | ❌ | ✅ LaTeX→OMML | ❌ |
| **安装复杂度** | 低（内置） | 中（Python+pip） | 低（npm） | 中（插件系统） |
| **标书适配** | ⚠️ | ✅ 近学术/出版 | ✅ 中文字体映射 | ✅ 模板驱动 |
| **后续编辑** | ✅ Track Changes | ❌ | ❌ | ❌ |

---

## 三、JBFG 方案书导出场景分析

### 场景特征

- 长篇 Markdown（~12,000 字，8 章 + 5 附录）
- 大量表格（选型表、指标表、风险矩阵、报价明细）
- ASCII 架构图 6 张（导出前需转为 PNG/SVG）
- 中文为主，术语含英文缩写
- 面向正式投标，需专业排版（A4、标题层级、目录、页眉页脚）
- 导出后可能需要客户侧修订（tracked changes 有价值）

### 推荐策略：两阶段流水线

```
第一阶段：生成初稿（huashu-md-html）
  Markdown → python-docx → A4 标书初稿（中文排版/封面/TOC/页码/表格样式）
        │
        │ 人工检查：架构图占位替换为矢量图、表格分页调整
        │
第二阶段：协同编辑（Anthropic 官方 skill）
  DOCX 初稿 → unpack XML → 微调格式 → 添加 tracked changes 标记
```

### 为什么不单一选择

- **仅用官方 skill**：需手动编程配置所有中文字体/段落样式，12000 字的方案书排版代码量接近正文本身
- **仅用 huashu-md-html**：排版效果好但不支持 tracked changes，客户侧修订流程需另想办法
- **仅用 @clipg/w2w**：中文排版控制最精细但缺长篇自动化（TOC/页眉/封面），适合短篇
- **仅用 Artifactry**：需要先制作 reference.docx 模板——如果客户提供了标书模板则最优，否则首次投入大

---

## 四、关联

- JBFG 方案书：[[冀北风光储数智化生产支撑与数字孪生解决方案-V1]]
- 方案撰写规范调研：[[方案书撰写规范与章节结构调研(Proposal Writing Standards Research)]]
- 父目录：[[80-知识体系|知识体系]]
