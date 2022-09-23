import json
import dill

from collections import OrderedDict

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def parse_section(value):
    elements = value.get('paragraph').get('elements')
    section_name = ''
    for elem in elements:
        section_name += read_paragraph_element(elem).strip()
    return section_name


def parse_paragraphs(elements):
    paragraphs = []
    for value in elements:
        for elem in value.get('paragraph').get('elements'):
            paragraph = read_paragraph_element(elem).strip()
            paragraphs.append(paragraph)
    return paragraphs if len(paragraphs) > 1 else paragraphs[0]


def parse_table(value):
    table = value.get('table')
    parsed_table = []
    for row in table.get('tableRows'):
        parsed_table.append([])
        cells = row.get('tableCells')
        for cell in cells:
            paragraphs = parse_paragraphs(cell.get('content'))
            if len(paragraphs) > 0:
                parsed_table[-1].append(paragraphs)
    return parsed_table


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
            :param elements:
            :type structured_text: OrderedDict
            :param structured_text:

    """
    i = 0
    structured_text = {}
    while i + 1 < len(elements):
        if 'paragraph' in elements[i] and 'table' in elements[i+1]:
            section_name = parse_section(elements[i])
            table_content = parse_table(elements[i+1])
            structured_text[section_name] = table_content
            i += 1
        i += 1
    return structured_text


def main():
    with open('data_jar/doc_content.pkl', 'rb') as inp:
        doc_content = dill.load(inp)

    structured_text = read_structural_elements(doc_content)
    with open("data_output/document.json", 'w') as f:
        f.write(json.dumps(structured_text, indent=4))


if __name__ == '__main__':
    main()
