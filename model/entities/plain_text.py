from dataclasses import dataclass


@dataclass
class PlainText:
    text: str
    bold: bool = False
    italic: bool = False
    size: int = 24
    font: str = "Times New Roman"
