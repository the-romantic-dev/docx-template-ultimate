import lxml.etree
from lxml import etree as lxml_etree
from lxml.etree import _Element
from sympy import Matrix

from dtu.namespaces import m as m_ns, w as w_ns
from dtu.converter import latex2omml
from .braces import BraceType, braces
from ..util import elements_from_xml, is_math_element
from dtu.sympy_prettifier.latex import rational_to_latex


def matrix_from_elements(elements: list[list[_Element]], alignment: str, brace_type: BraceType = None):
    oMath = lxml_etree.Element(f"{{{m_ns}}}oMath")
    m = lxml_etree.SubElement(oMath, f"{{{m_ns}}}m")

    cols = len(elements[0])
    mPr = elements_from_xml(
        xml=f"""
            <m:mPr>
                <m:mcs>
                    <m:mc>
                        <m:mcPr>
                            <m:count m:val="{cols}" />
                            <m:mcJc m:val="{alignment}" />
                        </m:mcPr>
                    </m:mc>
                </m:mcs>
                <m:ctrlPr>
                    <w:rPr>
                        <w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math" />
                        <w:i />
                    </w:rPr>
                </m:ctrlPr>
            </m:mPr>
        """,
        namespaces={"w": w_ns, "m": m_ns}
    )[0]
    m.append(mPr)

    for row in elements:
        mr = lxml.etree.SubElement(m, f"{{{m_ns}}}mr")
        for element in row:
            me: _Element = lxml.etree.SubElement(mr, f"{{{m_ns}}}e")
            if is_math_element(element):
                children = element.getchildren()
                me.extend(children)
            else:
                raise ValueError("It is not oMath element")
    if brace_type is None:
        return oMath
    else:
        return braces(oMath, brace_type)


def matrix_from_sympy(matrix: Matrix, brace_type: BraceType = BraceType.PARENTHESES) -> _Element:
    def matrix_latex(_matrix: Matrix):
        matrix_as_list = _matrix.tolist()

        for row in matrix_as_list:
            for i in range(len(row)):
                row[i] = rational_to_latex(row[i])

        if not matrix_as_list or not isinstance(matrix_as_list[0], list):
            return "Ошибка: Входные данные должны быть вложенным списком."

        rows = len(matrix_as_list)
        cols = len(matrix_as_list[0])

        latex_matrix = "\\begin{matrix}\n"

        for i, row in enumerate(matrix_as_list):
            if len(row) != cols:
                return "Ошибка: Все строки должны иметь одинаковую длину."

            latex_matrix += " & ".join(row)

            if i < rows - 1:
                latex_matrix += " \\\\\n"
            else:
                latex_matrix += "\n"

        latex_matrix += "\\end{matrix}"

        return latex_matrix

    matrix_omml = latex2omml(matrix_latex(matrix))
    return braces(matrix_omml, brace_type=brace_type)
