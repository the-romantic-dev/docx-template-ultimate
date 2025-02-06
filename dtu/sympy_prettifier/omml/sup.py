from dtu.namespaces.xml_namespaces import m, w
from lxml.etree import _Element, Element, SubElement
from dtu.xml.util import is_math_element, elements_from_xml


def sup(math_element: _Element, sup_element: _Element) -> _Element:
    if not is_math_element(math_element):
        raise ValueError("Not math elem")

    omath = Element(f"{{{m}}}oMath")
    sSup = SubElement(omath, f"{{{m}}}sSup")
    sSupPr = elements_from_xml(
        """
        <m:sSupPr>
            <m:ctrlPr>
                <w:rPr>
                    <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math" />
                    <w:i />
                </w:rPr>
            </m:ctrlPr>
        </m:sSupPr>
        """,
        namespaces=dict(m=m, w=w)
    )[0]
    sSup.append(sSupPr)
    e = SubElement(sSup, f"{{{m}}}e")
    for child in math_element.iterchildren():
        e.append(child)

    _sup = SubElement(sSup, f"{{{m}}}sup")
    for child in sup_element.iterchildren():
        _sup.append(child)
    return omath
