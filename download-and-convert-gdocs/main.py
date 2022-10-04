import glob

from src.getter import Getter
from src.parser import Parser
from src.converter import Converter


def main():
    g = Getter()
    raw_input = g.download_and_get()

    p = Parser(raw_input)
    parsed_input = p.parse()

    c = Converter(parsed_input)
    c.convert_and_save(path=glob.glob('**/my-awesome-cv/cv/sections', recursive=True)[0])


if __name__ == '__main__':
    main()
