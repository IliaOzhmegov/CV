from math import ceil
from typing import List, Dict
from collections import namedtuple


class Parser:

    def __init__(self, raw_input):
        self.__raw_input = raw_input
        self.__parse_section_as = {'EXPERIENCE': self.__parse_experience,
                                   'EDUCATION': self.__parse_education,
                                   'WRITINGS': self.__parse_writings,
                                   'SKILLS': self.__parse_skills}

    def parse(self) -> Dict:
        elements = self.__raw_input

        i = 0
        structured_text = {}
        while i + 1 < len(elements):
            if 'paragraph' in elements[i] and 'table' in elements[i+1]:
                section_name = self.__parse_section(elements[i])
                f = self.__parse_section_as[section_name]
                i += 1
                table_content = f(elements[i])
                structured_text[section_name] = table_content
            i += 1

        print('Successfully Parsed!')
        return structured_text

    def __parse_section(self, value):
        elements = value.get('paragraph').get('elements')
        section_name = ''
        for elem in elements:
            section_name += self.__read_paragraph_element(elem).strip()
        return section_name.strip()

    @staticmethod
    def __read_paragraph_element(element):
        text_run = element.get('textRun')
        if not text_run:
            return ''
        content = text_run.get('content')
        # if paragraph is a link, it extracts it and makes it in LaTeX format
        if 'textStyle' in text_run and 'link' in text_run['textStyle']:
            url_link = text_run.get('textStyle').get('link').get('url')
            return r'\href{' + url_link + '}{' + content + '}'
        return content

    def __parse_experience(self, value):
        return self.__parse_unit(value, ['Organization', 'Location', 'Position', 'Dates', 'Description'])

    def __parse_education(self, value):
        return self.__parse_unit(value, ['University', 'Location', 'Degree', 'Dates', 'Description'])

    def __parse_writings(self, value):
        return self.__parse_unit(value, ['Journal', 'Location', 'Title', 'Dates'])

    def __parse_skills(self, value):
        return self.__parse_unit(value, ['Category', 'Skills'])

    def __parse_unit(self, value, names: List[str]) -> List[Dict]:
        step = ceil(len(names)/2)
        named_tuple = namedtuple('named_tuple', names)

        list_of_items = []
        rows = value.get('table').get('tableRows')
        for i in range(0, len(rows), step):
            attributes = []
            for j in range(i, i+step):
                cells = [self.__parse_paragraphs(cell.get('content')) for cell in rows[j].get('tableCells')]
                while '' in cells:
                    cells.remove('')

                attributes.extend(cells)

            tmp_tuple = named_tuple._make(attributes)
            list_of_items.append(tmp_tuple._asdict())

        return list_of_items

    def __parse_paragraphs(self, elements):
        paragraphs = []
        for value in elements:
            for elem in value.get('paragraph').get('elements'):
                paragraph = self.__read_paragraph_element(elem).strip()
                paragraphs.append(paragraph)

        # There is a need to combine neighboring paragraphs with a paragraph that contains a link
        i = 0
        while i < len(paragraphs):
            if 'href' in paragraphs[i]:
                # to avoid segmentation fault
                i_before = max(i-1, 0)
                i_after = min(i+1, len(paragraphs)-1)

                i_min = min(i_before, i)
                i_max = max(i, i_after)

                chunks = [paragraphs.pop(k) for k in range(i_max, i_min-1, -1)]
                completed = ' '.join(chunks[::-1])
                paragraphs.insert(i_min, completed)
            i += 1
        return paragraphs if len(paragraphs) > 1 else paragraphs[0]


def main():
    import dill

    with open('../data_jar/doc_content.pkl', 'rb') as inp:
        doc_content = dill.load(inp)

    p = Parser(doc_content)
    structured_text = p.parse()
    # print(json.dumps(structured_text, indent=4))
    # with open("data_output/document.json", 'w') as f:
        # f.write(json.dumps(structured_text, indent=4).replace('\\\\', '\\'))
        # f.write(json.dumps(structured_text, indent=4))


if __name__ == '__main__':
    main()
