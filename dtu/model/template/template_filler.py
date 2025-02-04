from pathlib import Path

from document_template import DocumentTemplate


class TemplateFiller:
    def __init__(self, template: DocumentTemplate):
        self.template: DocumentTemplate = template

    def fill(self):
        methods = [getattr(self, method_name) for method_name in dir(self)
                   if callable(getattr(self, method_name))]
        for method in methods:
            if hasattr(method, '_is_filler') and method._is_filler:
                method()

    @classmethod
    def filler_method(cls, func):
        func._is_filler = True
        return func

    def save(self, save_path: Path, document_name: str = "output.docx", add_pdf: bool = True):
        self.template.save(save_path, document_name, add_pdf)
