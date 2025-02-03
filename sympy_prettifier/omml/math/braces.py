from enum import Enum

from lxml import etree as lxml_etree
from lxml.etree import _Element

from document.xml_namespaces import m, w
from ..util import is_math_element, elements_from_xml


class BraceType(Enum):
    PARENTHESES = 0
    BRACKETS = 1
    STRAIGHT = 2
    CURLY = 3
    LEFT_CURLY = 4
    UP_ROUND = 5
    DOUBLE_STRAIGHT = 6


def braces(math_element: _Element, brace_type: BraceType = BraceType.PARENTHESES) -> _Element:
    if not is_math_element(math_element):
        raise ValueError("Элемент не является частью уравнения Word")

    brace_elements = elements_from_xml(
        xml="""
        <m:begChr/>
        <m:endChr/>""",
        namespaces={'m': m}
    )
    match brace_type:
        case BraceType.BRACKETS:
            brace_elements[0].set(f"{{{m}}}val", "[")
            brace_elements[1].set(f"{{{m}}}val", "]")
        case BraceType.STRAIGHT:
            brace_elements[0].set(f"{{{m}}}val", "|")
            brace_elements[1].set(f"{{{m}}}val", "|")
        case BraceType.DOUBLE_STRAIGHT:
            brace_elements[0].set(f"{{{m}}}val", "‖")
            brace_elements[1].set(f"{{{m}}}val", "‖")
        case BraceType.CURLY:
            brace_elements[0].set(f"{{{m}}}val", "{")
            brace_elements[1].set(f"{{{m}}}val", "}")
        case BraceType.LEFT_CURLY:
            brace_elements[0].set(f"{{{m}}}val", "{")
            brace_elements[1].set(f"{{{m}}}val", "")
        case BraceType.UP_ROUND:
            brace_elements[0].set(f"{{{m}}}val", "⌈")
            brace_elements[1].set(f"{{{m}}}val", "⌉")
        case _:
            brace_elements = []

    md: _Element = lxml_etree.Element(f'{{{m}}}d')
    me: _Element = lxml_etree.Element(f'{{{m}}}e')
    omath: _Element = lxml_etree.Element(f'{{{m}}}oMath')
    dPr = elements_from_xml(
        xml="""
            <m:dPr>
                <m:ctrlPr>
                    <w:rPr>
                        <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math" />
                        <w:i />
                    </w:rPr>
                </m:ctrlPr>
            </m:dPr>
        """,
        namespaces={'m': m, 'w': w}
    )[0]
    if len(brace_elements) > 0:
        dPr.insert(0, brace_elements[1])
        dPr.insert(0, brace_elements[0])
    for child in math_element.iterchildren():
        me.append(child)
    md.append(dPr)
    md.append(me)
    omath.append(md)
    return omath
