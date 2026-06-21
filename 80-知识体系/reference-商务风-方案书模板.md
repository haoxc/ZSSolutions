---
aliases: [商务风方案书模板, reference.docx]
tags: [docx, template, reference]
description: 商务风 Pandoc reference.docx 模板——用于生成方案书/投标书的样式基准
type: 资产
ref-url:
create-date: 2026-06-21
---

## 文件位置

```
模板源: ~/.hermes/skills/docx-publishing/templates/reference.docx
MCP默认: ~/.hermes/mcp-servers/docx-builder/reference.docx
Vault备份: 80-知识体系/reference-商务风-方案书模板.docx
```

## 样式规格

### 页面

| 属性 | 值 |
|------|-----|
| 纸张 | A4 (21.0 × 29.7 cm) |
| 上/下边距 | 2.54 cm |
| 左/右边距 | 3.17 cm |

### 标题体系

| 样式 | 字体 | 字号 | 加粗 | 颜色 | 段前 | 段后 |
|------|------|------|------|------|------|------|
| Heading 1 | 黑体 / Calibri | 22pt | ✓ | #1B3A5C | 24pt | 12pt |
| Heading 2 | 黑体 / Calibri | 16pt | ✓ | #2B5C8A | 18pt | 8pt |
| Heading 3 | 黑体 / Calibri | 14pt | ✓ | #333333 | 12pt | 6pt |
| Heading 4 | 黑体 / Calibri | 12pt | ✓ | #333333 | 10pt | 4pt |

### 正文/辅助

| 样式 | 字体 | 字号 | 颜色 | 行距 | 其他 |
|------|------|------|------|------|------|
| Normal (正文) | 宋体 / Times New Roman | 12pt (小四) | #333333 | 1.5x | 首行缩进 0.74cm (2字符) |
| Body Text | 宋体 / Times New Roman | 10.5pt (五号) | #666666 | 1.5x | |
| Block Text | 宋体 / Times New Roman | 10.5pt | #666666 | 1.3x | |
| Source Code | 等线 / Consolas | 8.5pt | #333333 | 1.1x | |
| Table | 宋体 / Times New Roman | 10.5pt | #333333 | 1.15x | |
| List Bullet/Number | 宋体 / Times New Roman | 12pt | #333333 | 1.5x | |

### 特殊样式

| 样式 | 字体 | 字号 | 颜色 | 对齐 |
|------|------|------|------|------|
| Title (封面标题) | 黑体 / Calibri | 26pt | #17365D | 居中 |
| Subtitle | 宋体 / Times New Roman | 14pt | #4F81BD | 居中 |
| Header (页眉) | 宋体 / Times New Roman | 9pt | #666666 | |
| Footer (页脚) | 宋体 / Times New Roman | 9pt | #666666 | |
| TOC Heading (目录标题) | 黑体 / Calibri | 18pt | #1B3A5C | 居中 |

## 色系

```
深度海军蓝: #1B3A5C    — Heading 1, TOC Heading
中蓝:       #2B5C8A    — Heading 2
标题深色:   #17365D    — Title
副标题蓝:   #4F81BD    — Subtitle
正文深灰:   #333333    — Normal, Heading 3/4, Table
辅助灰:     #666666    — Body Text, Block Text, Header/Footer
```

## 包含的样式总数: 34 段落 + 1 表格

额外包含 Tok 系列代码高亮样式（KeywordTok, DataTypeTok 等），用于 Pandoc 语法高亮。

## 使用方法

### Pandoc CLI
```bash
pandoc source.md \
  --reference-doc=reference-商务风-方案书模板.docx \
  --toc --toc-depth=3 --number-sections \
  --metadata lang=zh-CN \
  -o output.docx
```

### MCP 工具
默认已集成在 `docx-builder` MCP server 中，`build_docx` 工具默认使用此模板。

### python-docx 后处理
模板只提供样式基准。封面页、页眉页脚、图片嵌入、表格美化仍需 python-docx 后处理。

## 来源

基于 Pandoc 默认模板 → python-docx 定制，参考 JBFG 方案书实际使用反馈调整。
