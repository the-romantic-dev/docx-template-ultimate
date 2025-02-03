from pathlib import Path
from sympy import latex
import latex2mathml.converter
from lxml import etree

xslt_path = Path(__file__).parent / "MML2OMML.XSL"


def latex2omml(latex_expr: str) -> etree._Element:
    """
    Преобразует математическое выражение из LaTeX в OMML (Office Math Markup Language).

    :param latex_expr: Строка с LaTeX-формулой.
    :return: Строка с форматом OMML (XML), который поддерживает Microsoft Word.

    :raises FileNotFoundError: Если XSLT-файл `MML2OMML.XSL` не найден.
    :raises etree.XMLSyntaxError: Если входной LaTeX не может быть преобразован в корректный MathML.
    :raises etree.XSLTApplyError: Если XSLT-преобразование не удалось.
    """
    if not xslt_path.exists():
        raise FileNotFoundError(f"XSLT-файл не найден: {xslt_path}")

    # Преобразование LaTeX → MathML
    mathml_output = latex2mathml.converter.convert(latex=latex_expr)

    try:
        tree = etree.fromstring(mathml_output)
    except etree.XMLSyntaxError as e:
        raise ValueError("Ошибка при разборе MathML: " + str(e))

    # Преобразование MathML → OMML
    xslt = etree.parse(xslt_path.as_posix())
    transform = etree.XSLT(xslt)

    try:
        new_dom = transform(tree)
    except etree.XSLTApplyError as e:
        raise RuntimeError("Ошибка при применении XSLT-преобразования: " + str(e))

    return new_dom.getroot()


def sympy2omml(sympy_expr):
    latex_output = latex(sympy_expr)
    return latex2omml(latex_output)
