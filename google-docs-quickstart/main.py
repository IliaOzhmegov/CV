from src.getter import Getter
from src.parser import Parser


def main():
    g = Getter()
    raw_input = g.download_and_get()

    p = Parser(raw_input)
    parsed_input = p.parse()
    print(parsed_input)


if __name__ == '__main__':
    main()
