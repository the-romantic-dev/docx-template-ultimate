from copy import copy

from docx.text.paragraph import Paragraph
from docx.text.run import Run


def copy_run(run: Run) -> Run:
    new_elem = copy(run._r)
    new_run = Run(r=new_elem, parent=run._parent)
    return new_run


def copy_paragraph(paragraph: Paragraph) -> Paragraph:
    new_elem = copy(paragraph._p)
    new_paragraph = Paragraph(p=new_elem, parent=paragraph._parent)
    return new_paragraph
