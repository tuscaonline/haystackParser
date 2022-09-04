import logging
from pprint import pprint
import rich

from haystackparser import resources
from haystackparser import grammar as grammarResource
from importlib.resources import as_file, files
from lark import Lark, logger
from haystackparser import grammar



logger.setLevel(logging.DEBUG)



source = files(grammar).joinpath('trio.lark')
with as_file(source) as file:
    grammarFile = file.open('r', encoding='utf-8')

parser = Lark(grammarFile, start='start', debug=True)




if __name__ == '__main__':
    test = """
test:M
test:NA
test:R
id: @test "test"
test:T
test:F
azer :233.333m2
azer: "zqaeaz"
test:`http://project-haystack.org/`
test:@foo-bar
test:^elec-meter 
test:2020-07-17 
test:14:30:00 
test:2020-07-17T16:55:42.977-04:00 New_York
test:C(37.5458266,-77.4491888)
test:Color("red")
test: Bonjour le monde
"""

    myStruct = parser.parse(test)
    rich.print(myStruct)
    pass
