"""
Generate a Pandoc-compatible reference DOCX template for JBFG proposal.

This creates an empty DOCX with ONLY style definitions (no body content).
Pandoc --reference-doc reads the style definitions and applies them to
the output, mapping:
  - Pandoc "Normal"      → docx "Normal"
  - Pandoc "Heading 1-4" → docx "Heading 1-4"
  - Pandoc "Body Text"   → docx "Body Text"
  - Pandoc "Compact"     → docx "Compact"
  - Pandoc "Source Code" → docx "Source Code"
  - Pandoc "First Para"  → docx "First Paragraph"
  - Pandoc "Block Text"  → docx "Block Text"
  - Pandoc "Table"       → docx "Table"

Font scheme from generate_templates.py:
  - Body: 宋体 (SimSun) / Times New Roman
  - Heading: 黑体 (SimHei) / Times New Roman
  - Code:  Consolas
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

# ── Color Palette (from generate_templates.py) ──
C_PRIMARY   = RGBColor(0x1B, 0x3A, 0x5C)  # Deep navy
C_SECONDARY = RGBColor(0x2B, 0x5C, 0x8A)  # Medium blue
C_BODY      = RGBColor(0x33, 0x33, 0x33)  # Dark gray body text
C_GRAY      = RGBColor(0x66, 0x66, 0x66)  # Gray
C_TABLE_HDR = RGBColor(0xD6, 0xE4, 0xF0)  # Light blue table header
C_CODE_BG   = RGBColor(0xF5, 0xF5, 0xF5)  # Light gray code background
C_BORDER    = RGBColor(0xCC, 0xCC, 0xCC)  # Border gray

FONT_CN  = '宋体'
FONT_H   = '黑体'
FONT_EN  = 'Times New Roman'
FONT_CODE = 'Consolas'


def set_east_asian_font(style_or_run, cn_font, en_font=None):
    """Set East Asian font on a style or run's rPr."""
    if en_font and hasattr(style_or_run, 'font'):
        style_or_run.font.name = en_font
    rPr = style_or_run.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}></w:rFonts>')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), cn_font)
    if en_font:
        rFonts.set(qn('w:ascii'), en_font)
        rFonts.set(qn('w:hAnsi'), en_font)


def set_paragraph_spacing(style, before=0, after=0, line_spacing=None, line_rule=None,
                           first_line_indent=None, alignment=None, keep_with_next=False):
    """Configure paragraph spacing on a style."""
    pf = style.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line_spacing:
        pf.line_spacing = line_spacing
    if line_rule:
        pf.line_spacing_rule = line_rule
    if first_line_indent is not None:
        pf.first_line_indent = Pt(first_line_indent)
    if alignment:
        pf.alignment = alignment
    if keep_with_next:
        pf.keep_with_next = True


def get_or_create_style(doc, name, base='Normal'):
    """Get an existing style or create a custom one."""
    try:
        return doc.styles[name]
    except KeyError:
        from docx.enum.style import WD_STYLE_TYPE
        # Determine style type from name
        if name.startswith('Heading'):
            stype = WD_STYLE_TYPE.PARAGRAPH
        elif name == 'Table':
            stype = WD_STYLE_TYPE.TABLE
        else:
            stype = WD_STYLE_TYPE.PARAGRAPH
        style = doc.styles.add_style(name, stype)
        style.base_style = doc.styles[base]
        return style


def configure_all_styles(doc):
    """Configure all styles needed for Pandoc reference-doc."""
    s = doc.styles

    # ── Normal (body text) ──
    n = s['Normal']
    n.font.size = Pt(11)
    n.font.color.rgb = C_BODY
    set_east_asian_font(n, FONT_CN, FONT_EN)
    set_paragraph_spacing(n, before=0, after=0,
                          line_spacing=Pt(22),
                          line_rule=WD_LINE_SPACING.EXACTLY,
                          first_line_indent=24,
                          alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)

    # ── Heading 1 (章) ──
    h = s['Heading 1']
    h.font.size = Pt(18)
    h.font.bold = True
    h.font.color.rgb = C_PRIMARY
    set_east_asian_font(h, FONT_H, FONT_EN)
    set_paragraph_spacing(h, before=24, after=12,
                          line_spacing=Pt(30),
                          line_rule=WD_LINE_SPACING.EXACTLY,
                          first_line_indent=0,
                          keep_with_next=True)

    # ── Heading 2 (节) ──
    h = s['Heading 2']
    h.font.size = Pt(15)
    h.font.bold = True
    h.font.color.rgb = C_SECONDARY
    set_east_asian_font(h, FONT_H, FONT_EN)
    set_paragraph_spacing(h, before=18, after=8,
                          line_spacing=Pt(26),
                          line_rule=WD_LINE_SPACING.EXACTLY,
                          first_line_indent=0,
                          keep_with_next=True)

    # ── Heading 3 (小节) ──
    h = s['Heading 3']
    h.font.size = Pt(13)
    h.font.bold = True
    h.font.color.rgb = C_BODY
    set_east_asian_font(h, FONT_H, FONT_EN)
    set_paragraph_spacing(h, before=12, after=6,
                          line_spacing=Pt(24),
                          line_rule=WD_LINE_SPACING.EXACTLY,
                          first_line_indent=0,
                          keep_with_next=True)

    # ── Heading 4 (子节) ──
    h = s['Heading 4']
    h.font.size = Pt(12)
    h.font.bold = True
    h.font.color.rgb = C_BODY
    set_east_asian_font(h, FONT_H, FONT_EN)
    set_paragraph_spacing(h, before=10, after=4,
                          line_spacing=Pt(22),
                          line_rule=WD_LINE_SPACING.EXACTLY,
                          first_line_indent=0,
                          keep_with_next=True)

    # ── Body Text (图注、术语表等) ──
    bt = get_or_create_style(doc, 'Body Text')
    bt.font.size = Pt(10.5)
    bt.font.color.rgb = C_GRAY
    set_east_asian_font(bt, FONT_CN, FONT_EN)
    set_paragraph_spacing(bt, before=0, after=6,
                          line_spacing=Pt(18),
                          line_rule=WD_LINE_SPACING.EXACTLY,
                          first_line_indent=0,
                          alignment=WD_ALIGN_PARAGRAPH.CENTER)

    # ── Compact (table cell compact text) ──
    cp = get_or_create_style(doc, 'Compact')
    cp.font.size = Pt(9)
    cp.font.color.rgb = C_BODY
    set_east_asian_font(cp, FONT_CN, FONT_EN)
    set_paragraph_spacing(cp, before=1, after=1,
                          line_spacing=Pt(14),
                          line_rule=WD_LINE_SPACING.EXACTLY,
                          first_line_indent=0)

    # ── Source Code (code blocks) ──
    sc = get_or_create_style(doc, 'Source Code')
    sc.font.size = Pt(8.5)
    sc.font.color.rgb = C_BODY
    set_east_asian_font(sc, '宋体', FONT_CODE)
    set_paragraph_spacing(sc, before=0, after=0,
                          line_spacing=Pt(13),
                          line_rule=WD_LINE_SPACING.EXACTLY,
                          first_line_indent=0)

    # Add shading to Source Code style (via XML)
    pPr = sc.element.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F5F5F5" w:val="clear"/>')
    pPr.append(shd)

    # ── First Paragraph (chapter opening, no indent) ──
    fp_style = get_or_create_style(doc, 'First Paragraph')
    fp_style.font.size = Pt(11)
    fp_style.font.color.rgb = C_BODY
    set_east_asian_font(fp_style, FONT_CN, FONT_EN)
    set_paragraph_spacing(fp_style, before=0, after=0,
                          line_spacing=Pt(22),
                          line_rule=WD_LINE_SPACING.EXACTLY,
                          first_line_indent=0,
                          alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)

    # ── Block Text (blockquote) ──
    bq = get_or_create_style(doc, 'Block Text')
    bq.font.size = Pt(10)
    bq.font.color.rgb = C_GRAY
    set_east_asian_font(bq, FONT_CN, FONT_EN)
    set_paragraph_spacing(bq, before=4, after=4,
                          line_spacing=Pt(18),
                          line_rule=WD_LINE_SPACING.EXACTLY,
                          first_line_indent=0)

    # ── Table style ──
    table_style = get_or_create_style(doc, 'Table', base='Normal')
    # Set table paragraph defaults
    tf = table_style.paragraph_format
    tf.space_before = Pt(2)
    tf.space_after = Pt(2)
    tf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    tf.line_spacing = Pt(16)


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(out_dir, '参考模板.docx')

    doc = Document()
    configure_all_styles(doc)

    # Add a single dummy paragraph so the document isn't completely empty
    # (Pandoc needs at least one paragraph to read style context)
    doc.add_paragraph('参考模板', style='Normal')

    doc.save(output_path)
    print(f'Reference template saved to: {output_path}')
    print(f'File size: {os.path.getsize(output_path):,} bytes')


if __name__ == '__main__':
    main()
