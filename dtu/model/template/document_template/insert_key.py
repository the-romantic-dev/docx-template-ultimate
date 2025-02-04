from dataclasses import dataclass

from docx.text.paragraph import Paragraph
from docx.text.run import Run


@dataclass
class InsertKey:
    paragraph: Paragraph
    run: Run
    key: str
