"""
Generate Word template files (.dotx) for JBFG proposal:
  - Template A: Comprehensive Bid Version (完整应标版)
  - Template B: Technical Solution Version (技术方案版)
"""

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_ORIENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

# ── Color Palette ──
C_PRIMARY   = RGBColor(0x1B, 0x3A, 0x5C)  # Deep navy
C_SECONDARY = RGBColor(0x2B, 0x5C, 0x8A)  # Medium blue
C_ACCENT    = RGBColor(0x2E, 0x75, 0xB6)  # Standard blue
C_BODY      = RGBColor(0x33, 0x33, 0x33)  # Dark gray body text
C_GRAY      = RGBColor(0x66, 0x66, 0x66)  # Gray
C_LIGHT     = RGBColor(0x99, 0x99, 0x99)  # Light gray
C_WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
C_TABLE_HDR = RGBColor(0xD6, 0xE4, 0xF0)  # Light blue for table header
C_TABLE_HDR_BW = RGBColor(0xD9, 0xD9, 0xD9)  # Light gray for B&W

FONT_CN = '宋体'
FONT_H = '黑体'
FONT_EN = 'Times New Roman'
FONT_CODE = 'Consolas'


def set_font(run, name_cn=FONT_CN, name_en=FONT_EN, size=12, bold=False, color=C_BODY):
    """Set both CN and EN font properties on a run."""
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = name_en
    r = run._element
    rPr = r.find(qn('w:rPr'))
    if rPr is None:
        rPr = parse_xml(f'<w:rPr {nsdecls("w")}></w:rPr>')
        r.insert(0, rPr)
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}></w:rFonts>')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), name_cn)
    rFonts.set(qn('w:ascii'), name_en)
    rFonts.set(qn('w:hAnsi'), name_en)


def set_paragraph_spacing(paragraph, before=0, after=0, line_spacing=None, line_rule=None):
    """Set paragraph spacing."""
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line_spacing is not None:
        if line_rule:
            pf.line_spacing_rule = line_rule
        pf.line_spacing = Pt(line_spacing)


def add_heading_styled(doc, text, level=1):
    """Add a heading with custom style."""
    h = doc.add_heading(text, level=level)
    return h


def add_cover_page_a(doc):
    """Template A: Full cover page with company branding."""
    # Confidentiality bar
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(60)
    run = p.add_run('■ 机  密  ·  仅限指定收件人  ■')
    set_font(run, FONT_H, FONT_EN, 11, bold=True, color=C_WHITE)
    # Add shading to paragraph
    pPr = p._element.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1B3A5C" w:val="clear"/>')
    pPr.append(shd)

    # Spacer
    doc.add_paragraph()

    # Company logo placeholder
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('[ 公司 Logo ]')
    set_font(run, FONT_H, FONT_EN, 20, bold=True, color=C_PRIMARY)

    # Spacer
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(24)

    # Main title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('冀北风光储数智化生产支撑\n与数字孪生解决方案')
    set_font(run, FONT_H, FONT_EN, 28, bold=True, color=C_PRIMARY)
    set_paragraph_spacing(p, before=0, after=6)

    # Subtitle
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('USDF 统一空间数据底座——新能源场站的空间对象操作系统')
    set_font(run, FONT_CN, FONT_EN, 16, bold=False, color=C_GRAY)

    # Divider line
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before=12, after=12)

    # Info block
    info_lines = [
        '编制单位：止善科技（北京）有限公司',
        '编制日期：2026 年    月',
        '版    本：V1.0',
        '文件编号：JBFG-SOL-2026-001',
    ]
    for line in info_lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(line)
        set_font(run, FONT_CN, FONT_EN, 14, color=C_BODY)

    # Bottom copyright
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before=48, after=0)
    run = p.add_run('© 2026 止善科技（北京）有限公司. All Rights Reserved.')
    set_font(run, FONT_CN, FONT_EN, 9, color=C_LIGHT)


def add_cover_page_b(doc):
    """Template B: Minimal cover page for technical review."""
    # Top color bar
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pPr = p._element.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1B3A5C" w:val="clear"/>')
    pPr.append(shd)
    run = p.add_run(' ' * 80)
    set_font(run, FONT_CN, FONT_EN, 14, color=C_PRIMARY)

    # Large spacer
    for _ in range(6):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=12, after=0)

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('冀北风光储数智化生产支撑\n与数字孪生  技术方案')
    set_font(run, FONT_H, FONT_EN, 28, bold=True, color=C_PRIMARY)

    # Divider
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before=12, after=12)

    # Version info
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('V1.0  |  2026 年    月')
    set_font(run, FONT_CN, FONT_EN, 14, color=C_GRAY)

    # Spacer
    for _ in range(6):
        p = doc.add_paragraph()
        set_paragraph_spacing(p, before=12, after=0)

    # Bottom bar
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pPr = p._element.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1B3A5C" w:val="clear"/>')
    pPr.append(shd)
    run = p.add_run(' ' * 80)
    set_font(run, FONT_CN, FONT_EN, 14, color=C_PRIMARY)

    # Bottom text
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, before=6, after=0)
    run = p.add_run('止善科技（北京）有限公司  |  Confidential')
    set_font(run, FONT_CN, FONT_EN, 9, color=C_LIGHT)


def configure_styles_a(doc, is_color=True):
    """Configure all styles for Template A."""
    style = doc.styles

    # ── Normal ──
    normal = style['Normal']
    normal.font.name = FONT_EN
    normal.font.size = Pt(12)
    normal.font.color.rgb = C_BODY
    rPr = normal.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}></w:rFonts>')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), FONT_CN)
    pf = normal.paragraph_format
    pf.first_line_indent = Pt(24)  # ~2 characters
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(22)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # ── Heading 1 ──
    h1 = style['Heading 1']
    h1.font.name = FONT_EN
    h1.font.size = Pt(18)
    h1.font.bold = True
    h1.font.color.rgb = C_PRIMARY
    rPr = h1.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}></w:rFonts>')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), FONT_H)
    pf = h1.paragraph_format
    pf.space_before = Pt(18)
    pf.space_after = Pt(12)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.first_line_indent = Pt(0)
    pf.keep_with_next = True

    # ── Heading 2 ──
    h2 = style['Heading 2']
    h2.font.name = FONT_EN
    h2.font.size = Pt(14)
    h2.font.bold = True
    h2.font.color.rgb = C_SECONDARY
    rPr = h2.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}></w:rFonts>')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), FONT_H)
    pf = h2.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.first_line_indent = Pt(0)
    pf.keep_with_next = True

    # ── Heading 3 ──
    h3 = style['Heading 3']
    h3.font.name = FONT_EN
    h3.font.size = Pt(13)
    h3.font.bold = True
    h3.font.color.rgb = C_BODY
    rPr = h3.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}></w:rFonts>')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), FONT_H)
    pf = h3.paragraph_format
    pf.space_before = Pt(6)
    pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.first_line_indent = Pt(0)
    pf.keep_with_next = True

    # ── Heading 4 ──
    h4 = style['Heading 4']
    h4.font.name = FONT_EN
    h4.font.size = Pt(12)
    h4.font.bold = True
    h4.font.color.rgb = C_BODY
    rPr = h4.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}></w:rFonts>')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), FONT_H)
    pf = h4.paragraph_format
    pf.space_before = Pt(6)
    pf.space_after = Pt(3)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.first_line_indent = Pt(0)
    pf.keep_with_next = True


def add_header_footer_a(section):
    """Add header and footer for Template A body pages."""
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = hp.add_run('止善科技  |  冀北风光储数智化生产支撑与数字孪生解决方案')
    set_font(run, FONT_CN, FONT_EN, 9, color=C_GRAY)

    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Insert page number field
    run = fp.add_run('- ')
    set_font(run, FONT_EN, FONT_EN, 9, color=C_GRAY)
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    run2 = fp.add_run()
    run2._element.append(fldChar1)
    instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    run3 = fp.add_run()
    run3._element.append(instrText)
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run4 = fp.add_run()
    run4._element.append(fldChar2)
    run5 = fp.add_run(' -')
    set_font(run5, FONT_EN, FONT_EN, 9, color=C_GRAY)


def add_header_footer_b(section):
    """Add header and footer for Template B body pages."""
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = hp.add_run('冀北风光储数智化生产支撑与数字孪生  技术方案')
    set_font(run, FONT_CN, FONT_EN, 9, color=C_GRAY)

    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run('- ')
    set_font(run, FONT_EN, FONT_EN, 9, color=C_GRAY)
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    run2 = fp.add_run()
    run2._element.append(fldChar1)
    instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    run3 = fp.add_run()
    run3._element.append(instrText)
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run4 = fp.add_run()
    run4._element.append(fldChar2)
    run5 = fp.add_run(' -')
    set_font(run5, FONT_EN, FONT_EN, 9, color=C_GRAY)


def add_content_skeleton_a(doc):
    """Add content structure placeholders for Template A."""
    sections = [
        ('修订记录', [
            ('版本记录表', '| 版本 | 修订日期 | 修订内容 | 修订人 |\n|------|----------|----------|--------|\n| V1.0 | 2026-XX-XX | 初稿编制 |  |'),
        ]),
        ('第一章  项目概述', [
            ('1.1  项目背景', '冀北风光储基地概况、新型电力系统要求、数字化向数智化演进的行业趋势……'),
            ('1.2  需求理解（SCQA 精炼版）', 'S (现状) → C (挑战) → Q (核心问题) → A (方案概要)……'),
            ('1.3  方案总纲', '[插入一页纸架构图]'),
            ('1.4  术语定义', '[术语表]'),
        ]),
        ('第二章  平台建设思想与顶层设计', [
            ('2.1  核心思想：空间对象操作系统', 'USDF——新能源场站的空间对象操作系统……'),
            ('2.2  四大架构约束', '可靠 / 扩展 / AI 友好 / 实施效能……'),
            ('2.3  顶层原理一：三通道分流', 'P1暂态 / P2稳态 / P3历史……'),
            ('2.4  顶层原理二：不可越层规则', '展示层不直连时序库、采集层不直写业务库……'),
            ('2.5  顶层原理三：空间是统一维度', '空间坐标是唯一能将异构对象统一索引的维度……'),
            ('2.6  方法论：从指标反推架构', '每一个架构决策都对应一个可检验的非功能指标……'),
            ('2.7  平台能力的四个支柱', '门户集成 / 元数据驱动 / 2D3D联动 / 样式主题……'),
        ]),
        ('第三章  总体技术架构', [
            ('3.1  设计理念与架构原则', 'USDF 底座 + 五业务域……'),
            ('3.2  逻辑架构（四层）', '展示层 → 业务层 → 平台层 → 采集层……'),
            ('3.3  部署拓扑（三级 + 安全分区）', '中心云 → 场站边缘（I区/II区/III区）→ 设备层……'),
            ('3.4  数据分层与流向', '采集 → Kafka → 存储/缓存 → API……'),
            ('3.5  关键技术选型与对比', '[技术选型对比表]……'),
            ('3.6  AI 引擎架构', '边缘推理 + 云端训练 + 人机协同……'),
            ('3.7  数据治理体系', '主数据 → 元数据 → 血缘 → 质量……'),
            ('3.8  统一 API 与开发者生态', '北向 API + gRPC + Kafka + 多语言 SDK……'),
            ('3.9  国产化适配', '[国产化清单]……'),
        ]),
        ('第四章  业务子系统方案', [
            ('4.1  一体化数智场站平台 (F1)', '全要素数据建模 / 三维可视化 / 高频数据接入……'),
            ('4.2  功率-能量协同优化 (F2)', '稳态多源协同 / 暂态快速调频 / 安全防误……'),
            ('4.3  构网型透明场站 (F3)', '并网性能评价 / 发电性能评价……'),
            ('4.4  智能运维系统 (F4)', '升压站巡视 / 光伏运维 / 输电线路 / 储能安全……'),
            ('4.5  数字运维管理平台 (F5)', '360°监控 / AI诊断 / 运维门户 / 生产运营……'),
        ]),
        ('第五章  系统非功能特性', [
            ('5.1  性能指标承诺', '34 项指标逐项承诺值 + 分层 SLA……'),
            ('5.2  可靠性设计', 'MTBF ≥10000h 的架构保障……'),
            ('5.3  安全性', '等保二级 + 电力二次安防……'),
            ('5.4  可扩展性设计', '多场站统一调度 / 功能模块可插拔 / 低代码建模……'),
            ('5.5  开放 API 与开发者生态', '北向 API + SDK……'),
        ]),
        ('第六章  项目实施计划', [
            ('6.1  分阶段交付', '4 个月三阶段……'),
            ('6.2  里程碑与交付物', 'M1-M4……'),
            ('6.3  团队配置', '[团队配置表]……'),
        ]),
        ('第七章  风险管控', [
            ('7.1  技术风险', '8 项技术风险及应对……'),
            ('7.2  业务风险', '5 项业务风险及应对……'),
            ('7.3  实施风险', '5 项实施风险及应对……'),
        ]),
        ('第八章  报价与服务', [
            ('8.1  项目报价', '[报价明细表]……'),
            ('8.2  服务保障', '质保期 / SLA / 响应时间 / 交付物……'),
        ]),
    ]

    for title, subsections in sections:
        doc.add_heading(title, level=1)
        for sub_title, placeholder_text in subsections:
            doc.add_heading(sub_title, level=2)
            p = doc.add_paragraph(placeholder_text)


def add_content_skeleton_b(doc):
    """Add content structure placeholders for Template B (technical focus)."""
    sections = [
        ('第一章  项目概述', [
            ('1.1  项目背景', '冀北风光储基地概况、新型电力系统要求、行业趋势……'),
            ('1.2  需求理解', 'S (现状) → C (挑战) → Q (核心问题) → A (方案概要)……'),
        ]),
        ('第二章  平台建设思想与顶层设计', [
            ('2.1  核心思想：空间对象操作系统', 'USDF——新能源场站的空间对象操作系统……'),
            ('2.2  四大架构约束', '可靠 / 扩展 / AI 友好 / 实施效能……'),
            ('2.3  三条顶层原理', '三通道分流 / 不可越层 / 空间统一维度……'),
            ('2.4  方法论：从指标反推架构', '每一个架构决策都对应一个可检验的非功能指标……'),
        ]),
        ('第三章  总体技术架构', [
            ('3.1  逻辑架构（四层）', '展示层 → 业务层 → 平台层 → 采集层……'),
            ('3.2  部署拓扑', '中心云 → 场站边缘 → 设备层……'),
            ('3.3  数据分层与流向', '采集 → Kafka → 存储 → API……'),
            ('3.4  关键技术选型', '[技术选型对比表]……'),
            ('3.5  AI 引擎架构', '边缘推理 + 云端训练 + 人机协同……'),
        ]),
        ('第四章  业务子系统方案', [
            ('4.1  一体化数智场站平台 (F1)', '全要素数据建模 / 三维可视化 / 高频数据接入……'),
            ('4.2  功率-能量协同优化 (F2)', '稳态多源协同 / 暂态快速调频 / 安全防误……'),
            ('4.3  构网型透明场站 (F3)', '并网性能评价 / 发电性能评价……'),
            ('4.4  智能运维系统 (F4)', '升压站巡视 / 光伏运维 / 输电线路 / 储能安全……'),
            ('4.5  数字运维管理平台 (F5)', '360°监控 / AI诊断 / 运维门户 / 生产运营……'),
        ]),
        ('第五章  系统非功能特性与实施', [
            ('5.1  性能指标承诺', '34 项指标逐项承诺值 + 分层 SLA……'),
            ('5.2  可靠性设计', 'MTBF ≥10000h 的架构保障……'),
            ('5.3  安全性', '等保二级 + 电力二次安防……'),
            ('5.4  可扩展性设计', '多场站统一调度 / 功能模块可插拔……'),
            ('5.5  项目实施计划', '4 个月三阶段交付……'),
        ]),
    ]

    for title, subsections in sections:
        doc.add_heading(title, level=1)
        for sub_title, placeholder_text in subsections:
            doc.add_heading(sub_title, level=2)
            p = doc.add_paragraph(placeholder_text)


def generate_template_a(output_dir):
    """Generate Template A: Comprehensive Bid Version (.docx sample)."""
    doc = Document()

    # Page setup
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)
    section.header_distance = Cm(1.5)
    section.footer_distance = Cm(1.5)

    # Configure styles
    configure_styles_a(doc, is_color=True)

    # Cover page
    add_cover_page_a(doc)

    # Page break
    doc.add_page_break()

    # Revision history
    doc.add_heading('修订记录', level=1)
    p = doc.add_paragraph('| 版本 | 修订日期 | 修订内容 | 修订人 |')
    p = doc.add_paragraph('|------|----------|----------|--------|')
    p = doc.add_paragraph('| V1.0 | 2026-XX-XX | 初稿编制 |  |')

    doc.add_page_break()

    # TOC placeholder
    doc.add_heading('目录', level=1)
    p = doc.add_paragraph('[ 此处插入自动目录：引用 → 目录 → 自动目录 ]')

    doc.add_page_break()

    # New section for body (page numbering reset)
    new_section = doc.add_section()
    new_section.page_width = Cm(21.0)
    new_section.page_height = Cm(29.7)
    new_section.top_margin = Cm(2.54)
    new_section.bottom_margin = Cm(2.54)
    new_section.left_margin = Cm(3.17)
    new_section.right_margin = Cm(3.17)
    add_header_footer_a(new_section)

    # Content skeleton
    add_content_skeleton_a(doc)

    # Save
    path = os.path.join(output_dir, 'JBFG-应标版样张.docx')
    doc.save(path)
    print(f"[OK] Template A saved: {path}")


def generate_template_b(output_dir):
    """Generate Template B: Technical Solution Version (.docx sample)."""
    doc = Document()

    # Page setup - same margins
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)
    section.header_distance = Cm(1.5)
    section.footer_distance = Cm(1.5)

    # Configure styles (same family but table header in gray for B&W)
    configure_styles_a(doc, is_color=False)

    # Cover page (simplified)
    add_cover_page_b(doc)

    doc.add_page_break()

    # TOC placeholder
    doc.add_heading('目录', level=1)
    p = doc.add_paragraph('[ 此处插入自动目录：引用 → 目录 → 自动目录 ]')

    doc.add_page_break()

    # New section for body with header/footer
    new_section = doc.add_section()
    new_section.page_width = Cm(21.0)
    new_section.page_height = Cm(29.7)
    new_section.top_margin = Cm(2.54)
    new_section.bottom_margin = Cm(2.54)
    new_section.left_margin = Cm(3.17)
    new_section.right_margin = Cm(3.17)
    add_header_footer_b(new_section)

    # Content skeleton (technical focus)
    add_content_skeleton_b(doc)

    # Save
    path = os.path.join(output_dir, 'JBFG-技术方案版样张.docx')
    doc.save(path)
    print(f"[OK] Template B saved: {path}")


if __name__ == '__main__':
    output_dir = r'C:\Users\haoxc\HXC_DATA\80_Knowledges\ZSSolutions\03-项目课题\26.0618-数智化生产支撑系统(JBFG)\20-解决方案\模板体系'
    generate_template_a(output_dir)
    generate_template_b(output_dir)
    print(f"\n[DIR] Output directory: {output_dir}")
    print("[TIP] These are .docx sample files. To create .dotx templates,")
    print("    open in Word and save as 'Word Template (*.dotx)'.")
