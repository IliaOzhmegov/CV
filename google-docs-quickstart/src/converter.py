import json

from typing import Dict
from pathlib import Path


class Converter:
    LONG_DIVIDER = '%' + '-' * 79 + '\n'
    SHORT_DIVIDER = '%' + '-' * 59 + '\n'
    INDENT = 2

    def __init__(self, content: Dict):
        self.__content = content.copy()
        self.__path = ''

    def __str__(self) -> str:
        return json.dumps(self.__content, indent=4)

    def _generate_header(self, name: str, environment: str = 'cventries') -> str:
        output = self.LONG_DIVIDER
        output += '%\t' + name + '\n'
        output += self.LONG_DIVIDER
        output += fr'\cvsection{{{name}}}' + '\n'*3

        output += self.LONG_DIVIDER
        output += '%\tCONTENT\n'
        output += self.LONG_DIVIDER

        output += fr'\begin{{{environment}}}' + '\n'*2
        output += self.SHORT_DIVIDER
        return output

    @staticmethod
    def _generate_footer(environment: str = 'cventries') -> str:
        return fr'\end{{{environment}}}' + '\n'

    def convert_and_save(self, path='cv') -> None:
        self.__path = path
        Path(self.__path).mkdir(exist_ok=True)

        self._generate_exp_page()
        self._generate_edu_page()
        self._generate_wri_page()
        self._generate_ski_page()

        print(f"Successfully Converted and save at {self.__path}")

    def _generate_ski_page(self):
        name = 'SKILLS'
        env = 'cvskills'
        rows = self.__content[name]
        columns = list(rows[0].keys())

        output = self._generate_header(name=name, environment=env)

        for row in rows:
            indent = self.INDENT
            output += ' '*indent + r'\cvskill' + '\n'
            indent += self.INDENT
            for column in columns:
                content = ', '.join(row[column]) if isinstance(row[column], type(list())) else row[column]
                output += ' ' * indent + f'{{{content}}}\n'

            output += '\n' + self.SHORT_DIVIDER

        output += self._generate_footer(environment=env)

        with open(self.__path + '/' + name.lower() + '.tex', 'w') as f:
            f.write(output)

    def _generate_exp_page(self):
        self._generate_page(name='experience')

    def _generate_edu_page(self):
        self._generate_page(name='education')

    def _generate_wri_page(self):
        self._generate_page(name='writings')

    def _generate_page(self, name: str) -> None:
        name = name.upper()
        rows = self.__content[name]
        # Since Python3.7 when you use json.load it preserves the order for dictionary
        columns = list(rows[0].keys())

        itemize_description_on = False
        cventry_type = r'\cventryshort'
        if 'Description' in columns and isinstance(rows[0]['Description'], type(list())):
            columns = columns[:-1]
            itemize_description_on = True
            cventry_type = r'\cventry'

        output = self._generate_header(name)

        for row in rows:
            indent = self.INDENT
            output += ' ' * indent + cventry_type + '\n'
            indent += self.INDENT
            for column in columns:
                field_content = ''.join(row[column]) if isinstance(row[column], type(list())) else row[column]
                output += ' ' * indent + f'{{{field_content}}}\n'

            # That's for long itemized description
            if itemize_description_on:
                output += ' ' * indent + '{\n'
                indent += self.INDENT
                output += ' ' * indent + r'\begin{cvitems}' + '\n'
                indent += self.INDENT
                for responsibility in row["Description"]:
                    responsibility = responsibility.replace("%", "\%")
                    output += ' ' * indent + f'\item{{{responsibility}}}\n'
                indent -= self.INDENT
                output += ' ' * indent + r'\end{cvitems}' + '\n'
                indent -= self.INDENT
                output += ' ' * indent + '}\n'

            output += '\n' + self.SHORT_DIVIDER

        output += self._generate_footer()

        with open(self.__path + '/' + name.lower() + '.tex', 'w') as f:
            f.write(output)


if __name__ == '__main__':
    with open('../data_output/document.json', 'r') as f:
        cv = json.load(f)

    c = Converter(cv)
    c.convert_and_save()