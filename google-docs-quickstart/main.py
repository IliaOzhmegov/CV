from src.getter import Getter


def main():
    g = Getter()
    raw_input = g.download_and_get()
    print(raw_input)


if __name__ == '__main__':
    main()
