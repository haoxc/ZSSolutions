---
title: Word 模板生成规则说明书
aliases:
  - JBFG://模板/生成规则
tags: [pjx/jbfg/模板, 生成规则, 排版规范]
description: >
  从 generate_templates.py 中提取的 Word 模板生成规则——section 分节规则、表格规则、图片占位规则、样式继承规则、修订记录位置规则
type: spec
status: 定稿
---

# Word 模板生成规则说明书

> 本文定义 JBFG 方案书 Word 模板的**生成规则**，而非样式值。
> 样式值见 [[排版规范说明书]]。
> 规则适用于 `generate_templates.py` 及未来同类脚本。

---

## 规则 1：Section 分节规则

### 1.1 节划分

每个 Word 模板固定划分为以下节（section），不可增减顺序：

| 节索引 | 内容 | 页码 | Header/Footer | 起始方式 |
|:------:|------|:----:|:-------------:|:--------:|
| 0 | 封面 | 无 | 无 | 文档起始 |
| 1 | 目录 | 罗马数字 Ⅰ,Ⅱ,Ⅲ… | 无（`is_linked_to_previous = False`） | 新页（section break） |
| 2+ | 正文各章 | 阿拉伯数字 1,2,3… | 有（公司名+章标题） | 每章一个 section break |

### 1.2 章节起始规则

- **封面**：文档起始，无特殊处理
- **目录**：`page_break()` + `add_body_section()`（创建新节，不与封面共用 header/footer）
- **正文第一章**：`add_chapter(is_first=True)` — 不插入 section break（因 body section 已由调用方创建）
- **正文第二章起**：`add_chapter(is_first=False)` — 先 `add_body_section()` 再 `doc.add_heading()`

### 1.3 规则代码

```python
def add_body_section(doc):
    """每个新节强制统一页面设置"""
    sec = doc.add_section()
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.54)
    sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(3.17)
    sec.right_margin = Cm(3.17)
    sec.header_distance = Cm(1.5)
    sec.footer_distance = Cm(1.5)
    return sec

def add_chapter(doc, title, is_first=False):
    """每章前插 section break（首章除外）"""
    if not is_first:
        add_body_section(doc)
    doc.add_heading(title, level=1)
```

---

## 规则 2：表格生成规则

### 2.1 通用规范

| 项目 | 规则 |
|------|------|
| **类型** | Word 原生表格（`doc.add_table()`），禁止 Markdown 伪表格 |
| **标题位置** | 表上方居中，宋体 10.5pt 加粗 |
| **表头** | 首行，深蓝底（`#1B3A5C`）白字，居中，加粗。暗标版改为深灰底（`#4D4D4D`） |
| **表身** | 宋体 10.5pt，深灰字（`#333333`） |
| **外边框** | 1.5pt 深蓝（`#1B3A5C`） |
| **内边框** | 0.5pt 浅灰（`#CCCCCC`） |
| **列宽** | 等分（总版心宽 14.66cm ÷ 列数） |
| **编号** | `表 X-Y`（X=章号，Y=该章序号） |

### 2.2 生成函数签名

```python
def add_word_table(doc, headers, rows, caption=None, is_color=True):
    """headers: [str] — 表头字符串列表
       rows: [[str]] — 数据行列表
       caption: str — 表标题（可选）
       is_color: bool — True=彩色(深蓝表头) / False=灰度(深灰表头)
    """
```

### 2.3 使用约束

- 表格后紧跟正文段落，不隔页
- 表名与表格之间不分页（暂未实现，需 Word 中手动设置"与下段同页"）
- 过长的表格（>10 行）考虑拆分为多个子表

---

## 规则 3：图片占位规则

### 3.1 占位规范

| 项目 | 规则 |
|------|------|
| **容器** | 单单元格 Word 表格（虚线边框 `dashed`、`#999999`、0.75pt） |
| **背景** | 浅灰底纹（`#F5F5F5`） |
| **提示文字** | 居中，宋体 11pt，灰色 `#666666` |
| **最小高度** | 5cm（典型架构图）或 8cm（复杂图） |
| **标题位置** | 图下方居中 |
| **标题格式** | 宋体 10.5pt 加粗 |
| **编号** | `图 X-Y`（X=章号，Y=该章序号） |

### 3.2 生成函数签名

```python
def add_image_placeholder(doc, caption_text, width_cm=14, height_cm=5):
    """caption_text: str — 含编号的图标题，如 '图 3-1  逻辑架构'
       width_cm / height_cm: int — 建议尺寸
    """
```

### 3.3 典型使用场景

| 图类型 | 建议尺寸 |
|--------|:--------:|
| 系统总体架构图 | 14cm × 6cm |
| 逻辑分层架构 | 14cm × 8cm |
| 部署拓扑图 | 14cm × 6cm |
| 数据流向图 | 14cm × 5cm |
| AI 引擎架构 | 14cm × 5cm |

---

## 规则 4：修订记录位置规则

### 4.1 定位

- **模板 A（完整应标版）**：修订记录位于**最后一章正文之后、附录之前**
- **模板 B（技术方案版）**：**不包含**修订记录

### 4.2 理由

| 位置 | 理由 |
|:----:|------|
| 封面之后 ❌ | 评审人第一眼应看到方案内容而非修改历史 |
| 目录之后 ❌ | 目录应直接定位正文 |
| 正文末尾 ✅ | 需要追溯版本时自然翻到末尾查找 |
| 附录之前 | 附录为参考材料，修订记录属于文档元数据，优先于参考材料 |

### 4.3 表格结构

| 版本 | 修订日期 | 修订内容 | 修订人 |
|:----:|:--------:|----------|:------:|
| V1.0 | 2026-XX-XX | 初稿编制 | （空） |

---

## 规则 5：样式继承规则

### 5.1 父子模板关系

```
模板 A（完整应标版）— 父模板
   ├── 删除报价/商务章节 → 派生为技术交流版
   ├── 删除商务 + 表头切灰度 → 派生为模板 B（技术方案版）
   ├── 删除商务 + 限制暗标规范 → 暗标适配版
   └── 翻译英文 + 替换字体 → 国际版
```

### 5.2 继承原则

| 资产 | 继承方式 |
|------|---------|
| 页面设置（页边距/纸张） | 全部继承 |
| 样式家族（Heading 1-4/Normal） | 全部继承（修改值见规则 1.3） |
| 颜色主题（CMYK 色板） | 派生版可替换（如 B 版灰度化表头） |
| 内容结构（章节骨架） | 子集化——B 版只取技术章节 |
| 页眉页脚 | 修改页眉文字（保留页码格式） |

### 5.3 扩展规则

新项目使用此模板体系时：
1. 复制 `generate_templates.py`，修改 `add_content_a()` / `add_content_b()` 中的章节内容和表格数据
2. 保留 `_setup_doc()`、`add_body_section()`、`add_word_table()`、`add_image_placeholder()` 等基础设施函数
3. 封面信息改为新项目名称

---

## 规则 6：生成脚本结构约定

### 6.1 文件结构

```python
# ═══════════════════
#  1. Imports + 常量
# ═══════════════════

# ═══════════════════
#  2. Helpers: font, paragraph, border, cell
# ═══════════════════

# ═══════════════════
#  3. Helpers: section, chapter, table, image
# ═══════════════════

# ═══════════════════
#  4. Cover pages
# ═══════════════════

# ═══════════════════
#  5. Style configuration
# ═══════════════════

# ═══════════════════
#  6. Header / Footer
# ═══════════════════

# ═══════════════════
#  7. Content skeletons
# ═══════════════════

# ═══════════════════
#  8. Template generators (main)
# ═══════════════════

# ═══════════════════
#  9. Entry point
# ═══════════════════
```

### 6.2 函数职责边界

| 函数 | 职责 | 不做什么 |
|------|------|---------|
| `add_body_section()` | 创建节 + 设置统一页边距 | 不操作 header/footer |
| `add_chapter()` | 插入 section break + H1 | 不添加内容、不设置 header |
| `add_word_table()` | 生成完整 Word 表格（含标题） | 不操作节属性 |
| `add_image_placeholder()` | 生成占位框 + 图标题 | 不操作节属性 |
| `add_cover_page_*()` | 生成封面 | 不操作样式 |
| `configure_styles()` | 设置全局样式家族 | 不添加内容 |
| `add_header_footer()` | 设置节的头/尾 | 不修改内容 |
| `add_content_*()` | 编排全部章节内容 | 不管理节结构 |

---

## 规则 7：验证清单

每次修改生成脚本后，运行以下验证：

- [ ] 模板 A 封面 → 目录 → 正文各章 → 修订记录 → 附录，顺序正确
- [ ] 模板 B 封面 → 目录 → 正文各章（无修订记录、无报价章节）
- [ ] 每章通过 section break 新起一页（非简单 page break）
- [ ] 所有表格为 Word 原生表格（打开 docx 检查能否编辑单元格）
- [ ] 所有图片占位框有虚线边框和灰底背景
- [ ] 页码体系：前置罗马数字、正文阿拉伯数字从 1 开始
- [ ] 封面无页码
- [ ] Header/Footer 在正文各节正确继承
- [ ] File size: 模板 A ≥ 45KB, 模板 B ≥ 40KB（含表格和占位框）

---

## 关联

- 模板 A 内容结构：[[模板A-完整应标版]]
- 模板 B 内容结构：[[模板B-技术方案版]]
- 排版样式值：[[排版规范说明书]]
- 生成脚本：`generate_templates.py`
- 评估与决策：[[综合评估报告]]
