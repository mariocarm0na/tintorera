"""Genera CV-Nuria-Chavarria.docx a partir de cv-nuria-chavarria.html.
Formato apto para ATS: una columna, sin tablas ni cuadros de texto, contacto en el cuerpo
(no en encabezado), estilos Heading reales y viñetas de lista estándar."""
import re, html, sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

here = Path(__file__).parent
src = (here / "cv-nuria-chavarria.html").read_text(encoding="utf-8")
body = src.split("<body>", 1)[1].split("</body>", 1)[0]
txt = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

INK = RGBColor(0x0D, 0x18, 0x38); PINK = RGBColor(0xD8, 0x1B, 0x50); MUTED = RGBColor(0x40, 0x47, 0x5F)
doc = Document()
sec = doc.sections[0]
sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
sec.top_margin = sec.bottom_margin = Cm(1.4); sec.left_margin = sec.right_margin = Cm(1.7)
st = doc.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(10); st.font.color.rgb = INK
st.paragraph_format.space_after = Pt(2); st.paragraph_format.line_spacing = 1.1
for name, size in (("Title", 24), ("Heading 1", 12.5), ("Heading 2", 10.5)):
    s = doc.styles[name]; s.font.name = "Arial"; s.font.size = Pt(size); s.font.bold = True; s.font.color.rgb = INK
doc.styles["Heading 1"].paragraph_format.space_before = Pt(10)
doc.styles["Heading 1"].paragraph_format.space_after = Pt(3)
doc.styles["Heading 2"].paragraph_format.space_before = Pt(6)
doc.styles["Heading 2"].paragraph_format.space_after = Pt(0)
doc.core_properties.title = "Nuria Chavarría - CV"; doc.core_properties.author = "Nuria Chavarría"

for m in re.finditer(r'<h1>(.*?)</h1>|<p class="headline">(.*?)</p>|<p class="contact">(.*?)</p>|<h2>(.*?)</h2>|<h3>(.*?)</h3>|<p class="meta">(.*?)</p>|<li>(.*?)</li>|<p>(.*?)</p>', body, re.S):
    h1, headline, contact, h2, h3, meta, li, p = m.groups()
    if h1: doc.add_paragraph(txt(h1), style="Title")
    elif headline:
        r = doc.add_paragraph().add_run(txt(headline)); r.bold = True; r.font.size = Pt(11.5); r.font.color.rgb = PINK
    elif contact: doc.add_paragraph(txt(contact))
    elif h2: doc.add_paragraph(txt(h2), style="Heading 1")
    elif h3: doc.add_paragraph(txt(h3), style="Heading 2")
    elif meta:
        r = doc.add_paragraph().add_run(txt(meta)); r.font.color.rgb = MUTED
    elif li: doc.add_paragraph(txt(li), style="List Bullet")
    elif p: doc.add_paragraph(txt(p))

out = here / "CV-Nuria-Chavarria.docx"; doc.save(out); print(out)
