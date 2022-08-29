from pprint import pprint
import rich

from haystackparser import resources
from haystackparser import grammar as grammarResource
from importlib.resources import as_file, files
from lark import Lark

from haystackparser.unitDb import Unit


import logging

logging.basicConfig(level=logging.DEBUG)



# with open("haystackparser/trio.lark", "r", encoding="utf-8") as file:
#     grammar = file.read()



def test():
    unit = Unit("m2")
    unit2 = Unit("m")
    unit3 = Unit("m3")

    pprint(unit)
    pprint(unit2)
    pprint(unit3)



if __name__ == '__main__':
    test()
