from dataclasses import dataclass
from enum import Enum, auto
from docx.document import Document as DocumentType
from docx.oxml import CT_R
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from lxml.etree import _Element
from model.element_creator import copy_run
from model.template.util import short_tag


class KeyParseState(Enum):
    TEXT = auto()
    OPEN_BRACE = auto()
    KEY = auto()
    CLOSE_BRACE = auto()


@dataclass
class RunReplaceData:
    source_runs: list[Run]
    text_part: str


def _get_run_replace_data_list(docx: DocumentType) -> dict[Paragraph, list[RunReplaceData]]:
    """
    Проходит по всему документу и ищет ключи для вставки. Если ключ для вставки разделен на несколько Run,
    он его собирает в один, если в одном Run несколько ключей - разделяет на несколько Run.

    Все данные собираются для дальнейшей вставки в документ в виде dict[Paragraph, list[RunReplaceData]].
     """

    result = {}
    current_item = ''
    split_runs = []

    def append_and_reset(_paragraph_split: list):
        nonlocal current_item, split_runs
        if current_item:
            _paragraph_split.append(RunReplaceData(split_runs, current_item))
            current_item = ''
            split_runs = []

    def is_next_element_run(run: Run):
        suited_tags = ['r', "proofErr"]
        curr_elem: CT_R = run._r
        next_element: _Element = curr_elem.getnext()
        if next_element is None:
            return False
        tag_name = short_tag(next_element)
        if tag_name in suited_tags:
            return True
        return False

    paragraphs: list[Paragraph] = docx.paragraphs
    for p in paragraphs:
        runs = p.runs
        paragraph_split = []
        state = KeyParseState.TEXT
        for r in runs:
            for char in r.text:
                match state:
                    case KeyParseState.TEXT:
                        if char == '{':
                            append_and_reset(paragraph_split)
                            current_item = char
                            split_runs = [r]
                            state = KeyParseState.OPEN_BRACE
                        else:
                            current_item += char
                            if r not in split_runs:
                                split_runs.append(r)

                    case KeyParseState.OPEN_BRACE:
                        current_item += char
                        if r not in split_runs:
                            split_runs.append(r)
                        if char == '{':
                            state = KeyParseState.KEY
                        else:
                            append_and_reset(paragraph_split)
                            state = KeyParseState.TEXT

                    case KeyParseState.KEY:
                        current_item += char
                        if r not in split_runs:
                            split_runs.append(r)
                        if char == '}':
                            state = KeyParseState.CLOSE_BRACE

                    case KeyParseState.CLOSE_BRACE:
                        current_item += char
                        if r not in split_runs:
                            split_runs.append(r)
                        if char == '}':
                            append_and_reset(paragraph_split)
                            state = KeyParseState.TEXT
                        else:
                            state = KeyParseState.KEY
            if not is_next_element_run(r):
                append_and_reset(paragraph_split)
        result[p] = paragraph_split
    return result


def isolate_key_runs(document: DocumentType):
    """
    В итоге должен получиться документ, где любой ключ находится в одном Run и является единственным текстом в нем.
    Делается это для дальнейшего упрощения работы и отсутствия сайд-эффектов при вставке контента по ключу
    """
    replace_dict: dict[Paragraph, list[RunReplaceData]] = _get_run_replace_data_list(document)
    run_replacements_dict: dict[Run, list[Run]] = {}
    runs_to_remove = []

    def add_replacement(_old_run: Run, replacement: Run):
        if _old_run in run_replacements_dict:
            run_replacements_dict[_old_run].append(replacement)
        else:
            run_replacements_dict[_old_run] = [replacement]

    for paragraph, rrd_list in replace_dict.items():
        for rrd in rrd_list:
            if rrd.text_part == rrd.source_runs[0].text:
                continue
            else:
                old_run = rrd.source_runs[0]
                new_run = copy_run(old_run)
                new_run.text = rrd.text_part
                add_replacement(old_run, new_run)
                runs_to_remove.extend(rrd.source_runs)
    for old_run, replacements in run_replacements_dict.items():
        for rep in reversed(replacements):
            old_run._r.addnext(rep._r)
    for run in set(runs_to_remove):
        parent = run._r.getparent()
        parent.remove(run._r)



