import re
from pathlib import Path

from lxml import etree as lxml_etree
from lxml.etree import _Element

from dtu.document.xml_namespaces import m, w


def is_math_element(element):
    return element.tag == f"{{{m}}}oMath"


def elements_from_xml(xml: str, namespaces: dict[str, str]) -> list[_Element]:
    namespace_attributes = " ".join([f"xmlns:{key}=\"{value}\"" for key, value in namespaces.items()])
    rooted_xml = f"""
            <root {namespace_attributes}>
                {xml}
            </root>
    
    """
    root_element = lxml_etree.fromstring(rooted_xml)
    parsed_elements = []
    for elem in root_element.iterchildren():
        parsed_elements.append(elem)
    return parsed_elements


def replace_in_xml(xml: str, key: str, data: str) -> str:
    def replace_func(match):
        content = match.group()
        open_bracket = content.index('>')
        close_bracket = content.rindex('<')
        return content[:open_bracket + 1] + str(data) + content[close_bracket:]

    pattern = f'>[^<>]*{re.escape(key)}[^<>]*</'
    return re.sub(pattern, replace_func, xml)


def get_xml_from_file(txt_path: Path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        formula_xml = file.read()
    return formula_xml


def get_element_from_xml_template(txt_path: Path, keys: str | list[str], replacements: str | list[str]):
    xml = get_xml_from_file(txt_path)
    if not isinstance(keys, list):
        keys = [keys]
    if not isinstance(replacements, list):
        replacements = [replacements]
    if len(keys) != len(replacements):
        raise ValueError("Число ключей не совпадает с числом вставок")
    for i in range(len(keys)):
        xml = replace_in_xml(xml, key=keys[i], data=replacements[i])
    element = elements_from_xml(xml, {"m": m, "w": w})[0]
    return element
