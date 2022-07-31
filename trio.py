import rich
from haystackparser.trio_parser import parser







# with open("haystackparser/trio.lark", "r", encoding="utf-8") as file:
#     grammar = file.read()



def test():
    with open("test.trio", "r", encoding='utf-8') as f:
        tree = parser.parse(f.read()+'\n')

    rich.print(tree)


if __name__ == '__main__':
    test()
