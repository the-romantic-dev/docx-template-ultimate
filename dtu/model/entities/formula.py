from copy import copy

import lxml.etree
from lxml import etree
from lxml.etree import _Element
from docx.docx_namespaces import m, w

from converter.omml_converter import latex2omml

namespaces = {
    "w": w,
    "m": m
}


def _merge_math_elements(omml_parts: list[_Element]) -> _Element:
    parent_math_element: _Element = lxml.etree.Element(f"{{{m}}}oMath")
    for op in omml_parts:
        children = op.getchildren()
        for child in children:
            parent_math_element.append(child)
    return parent_math_element


def get_rPr(run_element: _Element):
    rPr = run_element.find('w:rPr', namespaces)
    if rPr is None:
        rPr = etree.Element('{' + namespaces['w'] + '}rPr')
        run_element.insert(0, rPr)
    return rPr


def get_math_rPr(run_element: _Element):
    mrPr = run_element.find('m:rPr', namespaces)
    if mrPr is None:
        mrPr = etree.Element('{' + namespaces['m'] + '}rPr')
        run_element.insert(0, mrPr)
    return mrPr


def get_sz(rPr_element: _Element):
    sz = rPr_element.find('.//w:sz', namespaces)
    if sz is None:
        sz = etree.SubElement(rPr_element, '{' + namespaces['w'] + '}sz')
    return sz


def get_szCs(rPr_element: _Element):
    szCs = rPr_element.find('.//w:szCs', namespaces)
    if szCs is None:
        szCs = etree.SubElement(rPr_element, '{' + namespaces['w'] + '}szCs')
    return szCs


def create_b(rPr_element: _Element):
    b = rPr_element.find('.//w:b', namespaces)
    if b is None:
        b = etree.SubElement(rPr_element, '{' + namespaces['w'] + '}b')
    return b


def create_bCs(rPr_element: _Element):
    bCs = rPr_element.find('.//w:bCs', namespaces)
    if bCs is None:
        bCs = etree.SubElement(rPr_element, '{' + namespaces['w'] + '}bCs')
    return bCs


def set_rPr_font_size(rPr_element, font_size: int):
    sz = get_sz(rPr_element)
    sz.set('{' + namespaces['w'] + '}val', str(font_size))

    szCs = get_szCs(rPr_element)
    szCs.set('{' + namespaces['w'] + '}val', str(font_size))

def create_msty(mrPr_element: _Element):
    msty = mrPr_element.find('.//m:sty', namespaces)
    if msty is None:
        msty = etree.SubElement(mrPr_element, '{' + namespaces['m'] + '}sty')
    return msty

def change_math_element_style(math_element: _Element, font_size: int, bold: bool):
    run_elements = math_element.findall('.//m:r', namespaces)
    rPr_elements = [get_rPr(r) for r in run_elements]
    mrPr_elements = [get_math_rPr(r) for r in run_elements]
    for rPr in rPr_elements:
        if bold:
            create_b(rPr)
            create_bCs(rPr)

        set_rPr_font_size(rPr, font_size=font_size)
    for mrPr in mrPr_elements:
        if bold:
            msty = create_msty(mrPr)
            msty.set('{' + namespaces['m'] + '}val', "bi")


class Formula:
    def __init__(self, formula_parts: list[str | _Element] | str | _Element, font_size: int = 24, bold: bool = False):
        if isinstance(formula_parts, list):
            self._formula_parts = formula_parts
        else:
            self._formula_parts = [formula_parts]
        self._omml = None
        self.font_size = font_size
        self.bold = bold

    def _get_omml_parts(self) -> list[_Element]:
        omml_parts: list[_Element] = []
        for part in self._formula_parts:
            if isinstance(part, str):
                omml_parts.append(latex2omml(part))
            elif isinstance(part, _Element):
                omml_parts.append(copy(part))
        return omml_parts

    @property
    def oMath(self) -> _Element:
        if self._omml is not None:
            return self._omml
        omml_parts = self._get_omml_parts()
        for math_element in omml_parts:
            change_math_element_style(math_element, font_size=self.font_size, bold=self.bold)
        result = _merge_math_elements(omml_parts)
        return result
