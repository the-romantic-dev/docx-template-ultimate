from enum import Enum, auto
from functools import wraps
from pathlib import Path

from docx.document import Document
from docx.document import Document as DocumentType

from document_template import DocumentTemplate
from dtu.model.entities.formula import Formula
from dtu.model.entities.paragraph import Paragraph as MyParagraph
from dtu.model.entities.table import Table
from dtu.model.template.template_filler import TemplateFiller


class InsertType(Enum):
    TEXT = auto()
    FORMULA = auto()
    IMAGE = auto()
    DOCUMENT = auto()
    TABLE = auto()
    ELEMENTS_LIST = auto()
    TEMPLATE_FILLER = auto()


def _get_key(func):
    name = func.__name__
    fill_str = name[:6]
    if not fill_str == "_fill_":
        raise NameError("Filler function must start with _fill_")
    key = name[6:]
    return key


def _insert(template: DocumentTemplate, key: str, data, insert_type: InsertType):
    if data is None:
        template.delete_key(key)
        return
    match insert_type:
        case InsertType.FORMULA:
            if not isinstance(data, Formula):
                raise ValueError("For InsertType.FORMULA insert data must be Formula type")
            template.insert_formula(key=key, formula=data)
        case InsertType.TEXT:
            if not isinstance(data, str):
                raise ValueError("For InsertType.TEXT insert data must be str type")
            template.insert_text(key=key, text=data)
        case InsertType.IMAGE:
            if not isinstance(data, Path):
                raise ValueError("For InsertType.IMAGE insert data must be Path type")
            template.insert_picture(key=key, picture_path=data)
        case InsertType.DOCUMENT:
            if not isinstance(data, Document):
                raise ValueError("For InsertType.DOCUMENT insert data must be Document type")
            template.insert_data_from_document(key=key, document=data)
        case InsertType.TEMPLATE_FILLER:
            if not isinstance(data, TemplateFiller):
                raise ValueError("For InsertType.TEMPLATE_FILLER insert data must be TemplateFiller type")
            data.fill()
            doc = data.template.document
            template.insert_data_from_document(key=key, document=doc)
        case InsertType.TABLE:
            if not isinstance(data, Table):
                raise ValueError("For InsertType.TABLE insert data must be Table type")
            template.insert_table(key=key, table=data)
        case InsertType.ELEMENTS_LIST:
            error = ValueError(
                "For InsertType.ELEMENTS_LIST insert data must "
                "be list[Table | Formula | MyParagraph | DocumentType] type")
            if not isinstance(data, list):
                raise error
            else:
                for elem in data:
                    if not isinstance(elem, Table | Formula | MyParagraph | DocumentType):
                        raise error
            template.insert_elements_list(key=key, elements_list=data)


def filler(func, insert_type: InsertType):
    func._is_filler = True
    key = _get_key(func)

    @wraps(func)
    def wrapper(self):
        data = func(self)
        if not isinstance(self, TemplateFiller):
            raise TypeError(f"Object {self} is not TemplateFiller")
        _insert(template=self.template, key=key, data=data, insert_type=insert_type)
        return data

    return wrapper


def formula(func):
    return filler(func, insert_type=InsertType.FORMULA)


def image(func):
    return filler(func, insert_type=InsertType.IMAGE)


def document(func):
    return filler(func, insert_type=InsertType.DOCUMENT)


def text(func):
    return filler(func, insert_type=InsertType.TEXT)


def table(func):
    return filler(func, insert_type=InsertType.TABLE)


def elements_list(func):
    return filler(func, insert_type=InsertType.ELEMENTS_LIST)


def template_filler(func):
    return filler(func, insert_type=InsertType.TEMPLATE_FILLER)
