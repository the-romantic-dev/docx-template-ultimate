from __future__ import annotations

import re

from PIL import Image
from docx.document import Document as DocumentType
from docx.shared import Length
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from lxml.etree import _Element

KEY_PATTERN = r'\{\{(.+?)\}\}'


def can_replace_paragraph(paragraph: Paragraph):
    ignorable_tags = ["proofErr", "pPr"]
    tags = []
    for child in paragraph._p.iterchildren():
        tag = short_tag(child)
        tags.append(tag)
    count = 0
    for tag in tags:
        if tag not in ignorable_tags:
            count += 1
    return count <= 1


def short_tag(element: _Element):
    return element.tag.split("}")[-1]


def keys_in_run(run: Run):
    """ Возвращает все ключи, находящиеся в тексте Run """
    text = run.text
    matches = re.findall(KEY_PATTERN, text)
    return matches


def replace_paragraph_with_elements(paragraph: Paragraph, elements: list[_Element]):
    """Заменяет параграф в документе переданными элементами."""
    paragraph_element = paragraph._p
    for elem in reversed(elements):
        paragraph_element.addnext(elem)
    body_element = paragraph_element.getparent()
    body_element.remove(paragraph_element)


def get_document_elements(document: DocumentType) -> list[_Element]:
    """Возвращает все элементы тела документа, кроме игнорируемых."""
    ignored_tags = {"sectPr"}
    body_element = document._element.body
    return [child for child in body_element.iterchildren() if short_tag(child) not in ignored_tags]


def add_picture(picture_path: str, run: Run):
    run.clear()
    doc: DocumentType = run._parent._parent._parent

    with Image.open(picture_path) as img:
        original_width, original_height = img.size

    left_margin = doc.sections[0].left_margin
    right_margin = doc.sections[0].right_margin

    width = Length(doc.sections[0].page_width - left_margin - right_margin)
    height = Length(int((width / original_width) * original_height))

    run.add_picture(picture_path, width=width, height=height)
