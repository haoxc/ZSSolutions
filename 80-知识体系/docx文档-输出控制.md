---
aliases: []
tags: []
description:
type:
ref-url:
create-date: 2026-06-21 09:10
---
## 内容

- **语言风格**
	- 语言去工程化、增商务感——保留技术硬度，但每章开头加"价值锚点"，便于评标专家快速抓重点
	- 叙述化文本：用连贯的自然段落把要点讲清楚，段与段之间有逻辑过渡，而不是用一条条短语堆砌。下面我把方案改写为可直接生成 Word 的段落式正文
- **图表类型** 
	- ASCII 字符画图
	- 专业矢量图(Mermaid 流程/时序/甘特图 + Vega-Lite 统计图)


## 核心步骤

###  步骤 1 安装工具

把上面 ` ```markdown ` 代码块内的全部内容存为 `proposal.md`，按下列流程生成商务风 `.docx`。
步骤 1 安装工具

```bash
# Pandoc + 图表渲染工具
brew install pandoc        # macOS；Windows 用 choco install pandoc
npm install -g @mermaid-js/mermaid-cli mermaid-filter
pip install vl-convert-python
```


### 步骤 2 生成商务样式模板（一次性）
```bash
pandoc -o reference.docx --print-default-data-file reference.docx
```

打开 `reference.docx`，按商务风修改并保存（不删内容、只改样式）：

- 标题 1-3：微软雅黑、深蓝 `#1F4E79`、加粗
- 正文：宋体小四、行距 1.5
- 表格：套用"网格型浅色-着色 1（蓝）"，表头蓝底白字
- 插入封面页 + 页眉（公司 Logo）+ 页脚（页码）

### 步骤 3 一键转换

```bash
pandoc proposal.md \
  -o 冀北风光储数智化解决方案_V2.docx \
  --reference-doc=reference.docx \
  --toc --toc-depth=3 \
  --number-sections \
  -F mermaid-filter
```