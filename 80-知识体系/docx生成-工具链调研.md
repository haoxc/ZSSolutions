---
aliases: [docx生成调研, 出版级docx]
tags: [tools, docx, publishing]
description: 出版级 docx 生成的工具链调研与对比——pandoc / python-docx / docxtpl / docxcompose
type: 知识
ref-url:
create-date: 2026-06-21
---

## 出版级 docx 定义

对技术方案书（投标级）而言，"出版级"指：

- **字体/字号/色彩**：标题/正文/注释三级字体体系，中西文混排字体回退
- **段落排版**：精确行距（固定值/倍数）、段前段后间距、首行缩进、孤行控制
- **多级标题**：自动编号、目录（TOC）深度≥3 级、图表目录（TOF）
- **页眉页脚**：首页不同、奇偶页不同、页码（连续/分节）、公司信息
- **表格**：样式化表头（底色+粗体）、交替行底色、统一边框线型
- **图表**：嵌入式图像、居中、统一宽度、图题（Caption）自动编号
- **封面页**：项目名/客户/公司/日期/版本
- **章节控制**：分节符（下一页/连续）、不同节独立页眉页脚
- **交叉引用**：论文级需要，投标方案书暂不强求

---

## 工具链对比

### 1. Pandoc — MD→DOCX 核心转换引擎

| 维度   | 评分    | 说明                                          |
| ---- | ----- | ------------------------------------------- |
| 中转能力 | ★★★★★ | 从 Markdown AST 到 OOXML，处理段落/标题/列表/表格/脚注/代码块 |
| 样式控制 | ★★★☆☆ | 依赖 `--reference-doc`，只能继承已定义样式，无法创建新样式      |
| 图表   | ★★☆☆☆ | Mermaid 需外部渲染为 PNG 后引用；原生不支持 SVG 嵌入         |
| 中文   | ★★★★☆ | lang=zh-CN 可触发中文标点压缩和换行规则                   |
| 维护   | ★★★★☆ | Haskell 编写，稳定但升级慢（当前环境 2.12，最新 3.7）         |

**关键限制**：Pandoc 的 reference.docx 机制是"样式继承"而非"样式定义"——它只使用模板中已存在的样式名称。模板中未定义的样式（如自定义表格样式）无法通过 Pandoc 参数注入。

**结论**：Pandoc 擅长"内容→结构"转换，但不擅长"结构→排版"精修。适合做 pipeline 第一阶段。

---

### 2. python-docx — OOXML 精细控制

| 维度       | 评分    | 说明                                                     |
| -------- | ----- | ------------------------------------------------------ |
| API 覆盖   | ★★★★☆ | Document/Paragraph/Run/Table/Section/Header/Footer 全覆盖 |
| OOXML 直操 | ★★★★★ | `paragraph._element` / `parse_xml()` 可做任何 Word 能做的事    |
| 图像嵌入     | ★★★★☆ | `run.add_picture()` + 尺寸控制                             |
| 中文字体     | ★★★★★ | `rFonts.eastAsia` 属性完美支持中文字体指定                         |
| 页眉页脚     | ★★★★☆ | 分节控制 + 域代码（PAGE 字段）                                    |
| 维护       | ★★★★☆ | 活跃开发，v1.2.0                                            |

**已在实际 pipeline 中验证的能力**：
- 封面页：OOXML 级 `body.insert()` 插入段落 + 分节符
- 页眉/页脚：PAGE 域代码 + 左右 tab 分割
- 图像嵌入：扫描段落文本→匹配图号→替换为 `add_picture()`
- 表格美化：`tblPr/tblBorders` XML 注入 + 交替行底色
- 元数据：`core_properties` 设置

**痛点**：
- 操作 Word 编号（多级列表）需 OOXML 直操，API 层面不友好
- TOC 字段代码手工注入后在 Word 中需 F9 刷新
- 无内置 markdown 解析，需 Pandoc 完成"文字→结构"的转换

---

### 3. docxtpl — Jinja2 模板引擎

| 维度   | 评分    | 说明                          |
| ---- | ----- | --------------------------- |
| 模板能力 | ★★★★★ | Jinja2 语法全支持，循环/条件/过滤/宏     |
| 学习曲线 | ★★★☆☆ | 需准备模板 .docx，在其中嵌入 Jinja2 标签 |
| 适用场景 | ★★★★☆ | 同一模板反复生成不同内容的场景（如周报、报价单）    |
| 灵活性  | ★★★☆☆ | 模板确定后结构固定，难以动态插入章节          |

**vs python-docx**：docxtpl 是"模板驱动的渲染"，python-docx 是"程序化的构建"。前者适合固定结构 + 数据填充，后者适合动态结构 + 排版精修。

**对我们的适用性**：方案书结构多变（每份方案章节不同），docxtpl 的模板约束反而成为负担。不考虑作为主方案。

---

### 4. docxcompose — 文档拼接

| 维度   | 评分    | 说明                 |
| ---- | ----- | ------------------ |
| 功能   | ★★★☆☆ | 将多个 .docx 按顺序拼接为一个 |
| 页码连续 | ★★★★☆ | 自动处理分节和页码连续        |
| 样式合并 | ★★☆☆☆ | 源文档样式名冲突时行为不确定     |
| 适用场景 | ★★★☆☆ | 多人协作各写一章→最终拼接      |

**对我们的适用性**：如果是单作者流程，不需要 docxcompose。但若未来需要"每章独立生成→最终合并"的流水线，可以作为第三阶段工具。

---

### 5. 其他方案

| 工具 | 评价 |
|------|------|
| ReportLab | PDF 生成王者，但不支持 .docx |
| WeasyPrint | HTML/CSS→PDF，同样不产生 docx |
| libreoffice --headless | `soffice --convert-to docx` 可做 MD→ODT→DOCX，排版保真度差 |
| unoconv | 同样基于 LibreOffice UNO，稳定性差 |
| marko (npm) | JS 生态的 MD→DOCX，功能有限，不推荐 |

---

## 推荐方案：Pandoc + python-docx 混合 pipeline（当前方案已验证）

```
MD 源文件
  │
  ├─ 预处理（Python）
  │   ├─ YAML frontmatter 剥离
  │   ├─ WikiLink → 纯文本
  │   ├─ ASCII 图 → 图片引用（绝对路径）
  │   └─ 注释清除
  │
  ├─ Pandoc 转换
  │   ├─ gfm → docx
  │   ├─ --reference-doc（模板样式继承）
  │   ├─ --toc --toc-depth=3
  │   ├─ --number-sections
  │   └─ --metadata（标题/作者/关键词）
  │
  └─ python-docx 后处理
      ├─ 封面页（OOXML body.insert）
      ├─ 页眉/页脚（PAGE 域代码）
      ├─ 图片嵌入（扫描→替换）
      ├─ 表格美化（XML 边框+底色）
      └─ 元数据注入
```

### 为什么不用纯 python-docx？

Markdown→DOCX 的"结构映射"工作量巨大：标题层级识别、列表嵌套、表格解析、引用链接、脚注处理。Pandoc 已完美解决这些，没必要重新发明。

### 为什么不用纯 Pandoc？

出版级排版需要 Pandoc AST 表达不了的东西：分节页眉页脚、封面页、表格交替行底色。这些必须在 OOXML 层操作。

---

## 出版级增强清单

当前 pipeline 的输出质量检查（已有）：

- [x] 文件大小 > 100KB
- [x] 页眉非空
- [x] 页脚含 PAGE 域
- [x] 图片嵌入 ≥ 7 张
- [x] 无残留 ASCII 图
- [x] 表头粗体
- [x] 目录页存在
- [x] 多节（≥2）

可增强的方向：

| 增强项 | 技术方案 | 优先级 |
|--------|----------|--------|
| 多级编号（1.1, 1.1.1） | Pandoc `--number-sections` 已支持 | ✓ 已实现 |
| 图表自动编号 | Pandoc Lua filter: 计数 `Image`→改写 alt text | 中 |
| 图表目录（TOF） | Pandoc Lua filter + 自定义样式 | 中 |
| 交叉引用 | python-docx 插入书签 + REF 域 | 低 |
| 水印（机密/草稿） | OOXML `v:background` | 低 |
| PDF/A 归档 | 另需 LibreOffice 转换 | 低 |
| 电子签名 | 第三方服务，非 docx 生成范畴 | 不纳入 |

---

## 环境现状

```
pandoc:      2.12 (C:\Program Files\Pandoc\)
python-docx: 未在 venv（通过 conda 安装？）→ 需确认
docxtpl:     未安装
docxcompose: 未安装
```

**升级建议**：Pandoc 2.12（2021）→ 3.x（2024+），新版本对 docx writer 有增强：
- 更好的 `--reference-doc` 表格样式继承
- 新增 `--from gfm-raw_html` 等扩展
- Lua 过滤器 API 更稳定

---

## 结论

**Pandoc + python-docx 混合 pipeline 是出版级 docx 生成的最优解**。分工清晰：

1. Pandoc 负责内容结构转换（MD→DOCX）
2. python-docx 负责排版精修（封面/页眉页脚/图片/表格）
3. 质量验证脚本把关交付标准

此方案已在冀北风光储方案中实战验证，输出质量达标。
