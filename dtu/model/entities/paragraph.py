import lxml.etree
from lxml.etree import _Element

from dtu.namespaces import w
from .formula import Formula
from .plain_text import PlainText


def create_run(plain_text: PlainText) -> _Element:
    run = lxml.etree.Element(f"{{{w}}}r")
    rPr = lxml.etree.SubElement(run, f"{{{w}}}rPr")

    lxml.etree.SubElement(rPr, f"{{{w}}}rFonts", attrib={
        f"{{{w}}}ascii": plain_text.font,
        f"{{{w}}}hAnsi": plain_text.font,
        f"{{{w}}}cs": plain_text.font
    })

    lxml.etree.SubElement(rPr, f"{{{w}}}sz", attrib={f"{{{w}}}val": str(plain_text.size)})
    lxml.etree.SubElement(rPr, f"{{{w}}}szCs", attrib={f"{{{w}}}val": str(plain_text.size)})

    if plain_text.bold:
        lxml.etree.SubElement(rPr, f"{{{w}}}b")
        lxml.etree.SubElement(rPr, f"{{{w}}}bCs")
    if plain_text.italic:
        lxml.etree.SubElement(rPr, f"{{{w}}}i")
        lxml.etree.SubElement(rPr, f"{{{w}}}iCs")
    t = lxml.etree.SubElement(run, f"{{{w}}}t")
    t.text = plain_text.text
    return run


def create_paragraph() -> _Element:
    p = lxml.etree.Element(f"{{{w}}}p")
    lxml.etree.SubElement(p, f"{{{w}}}pPr")
    return p


class Paragraph:
    def __init__(self, content: list[PlainText | Formula]):
        self.content = content

    @property
    def element(self):
        p = create_paragraph()
        for c in self.content:
            if isinstance(c, PlainText):
                r = create_run(c)
                p.append(r)
            elif isinstance(c, Formula):
                omath = c.oMath
                p.append(omath)
        return p

