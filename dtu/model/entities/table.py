import random

import lxml.etree as letree
from lxml.etree import _Element

from docx.docx_namespaces import w, w14
from prettifier.elements.util import elements_from_xml
from model.entities.formula import Formula


def create_element(tag: str, nsmap: dict = {"w": w}, attr: dict = {}) -> _Element:
    return letree.Element(tag, nsmap=nsmap, attrib=attr)


def rand_hex():
    return f"{random.randint(0, 0xFFFFFFFF):08X}"


rsidR = rand_hex()
rsidTr = rand_hex()


def create_col_element(data: str | Formula, color: str = None):
    tc = create_element(tag=f"{{{w}}}tc")
    tcPr = elements_from_xml(
        xml="""
                <w:tcPr>
                    <w:tcW w:w="0" w:type="auto" />
                </w:tcPr>
        """, namespaces={"w": w}
    )[0]
    tc.append(tcPr)
    if color is not None:
        """<w:shd w:val="clear" w:color="auto" w:fill="FFFF00" />"""
        shd = letree.SubElement(
            tcPr, f"{{{w}}}shd",
            attrib={
                f"{{{w}}}val": "clear",
                f"{{{w}}}color": "auto",
                f"{{{w}}}fill": color,
            })
    p = create_element(
        tag=f"{{{w}}}p",
        attr={
            f"{{{w14}}}paraId": rand_hex(),
            f"{{{w14}}}textId": rand_hex(),
            f"{{{w}}}rsidR": rsidR,
            f"{{{w}}}rsidRDefault": rand_hex()
        }
    )
    tc.append(p)
    if isinstance(data, str):
        run_elem = elements_from_xml(
            xml=f"""
                <w:r>
                    <w:rPr>
                    </w:rPr>
                    <w:t>{data}</w:t>
                </w:r>
            """,
            namespaces={"w": w}
        )[0]
        p.append(run_elem)
    elif isinstance(data, Formula):
        p.append(data.oMath)
    return tc


class Table:
    def __init__(self, table_data: list[list], color_fills: dict[tuple[int, int], str]):
        self.table_data = table_data
        self.rows = len(table_data)
        self.cols = len(table_data[0])
        self.color_fills = color_fills
        for t in table_data:
            if len(t) != self.cols:
                raise ValueError("Не у всех строк одинаковая ширина")

    def row_element(self, row_index: int):
        data = self.table_data[row_index]
        tr = create_element(
            tag=f"{{{w}}}tr",
            attr={
                f"{{{w}}}rsidR": rsidR,
                f"{{{w14}}}paraId": rand_hex(),
                f"{{{w14}}}textId": "77777777",
                f"{{{w}}}rsidTr": rsidTr
            }
        )
        trPr = elements_from_xml(
            xml="""
                        <w:trPr>
                            <w:jc w:val="center" />
                        </w:trPr>
                    """,
            namespaces={"w": w}
        )[0]
        tr.append(trPr)
        for i, d in enumerate(data):
            color = None
            if (row_index, i) in self.color_fills:
                color = self.color_fills[(row_index, i)]
            tr.append(create_col_element(d, color=color))
        return tr

    @property
    def table_element(self):
        default_width = 200
        tbl: _Element = create_element(tag=f"{{{w}}}tbl")
        tblPr = elements_from_xml(
            xml="""
                <w:tblPr>
                    <w:tblStyle w:val="Table Grid" w:type="table" />
                    <w:tblW w:w="0" w:type="auto" />
                    <w:jc w:val="center" />
                    <w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1"
                        w:lastColumn="0" w:noHBand="0" w:noVBand="1" />
                    <w:tblBorders>
                        <w:top w:val="single" w:sz="4" w:space="0" w:color="auto" />
                        <w:left w:val="single" w:sz="4" w:space="0" w:color="auto" />
                        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto" />
                        <w:right w:val="single" w:sz="4" w:space="0" w:color="auto" />
                        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto" />
                        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto" />
                    </w:tblBorders>
                </w:tblPr>
            """,
            namespaces={"w": w}
        )[0]
        tbl.append(tblPr)
        tblGrid = create_element(tag=f"{{{w}}}tblGrid")
        tbl.append(tblGrid)
        gridCols = [create_element(tag=f"{{{w}}}gridCol", attr={f"{{{w}}}w": f"{default_width}"}) for _ in
                    range(self.cols)]
        for g in gridCols:
            tblGrid.append(g)
        for i in range(self.rows):
            tbl.append(self.row_element(i))
        return tbl
