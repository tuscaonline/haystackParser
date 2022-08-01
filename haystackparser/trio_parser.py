
import logging
from lark import Lark, logger, Transformer, v_args, Tree
from lark.indenter import Indenter
from importlib.resources import files, as_file

from haystackparser.zinc_type_parser import zincTokenParser
from . import grammar


logger.setLevel(logging.DEBUG)


class TreeToJson(Transformer):

    def tag(self, item):
        tag={
            'tag': zincTokenParser(item[0]),
            'value': zincTokenParser(item[1])
        }
 
        return tag

    def marker(self, item):
        return {
            'marker': zincTokenParser(item[0])
        }

    @v_args(tree=True)
    def tag_multiline(self, item):
        multistring = ''
        tagName = None
        for children in item.children:
            if(not tagName):
                tagName = zincTokenParser(children)
                continue
            multistring += children.value.strip() + '\n'
        return {
            'tag': tagName,
            'value': multistring
        }

class TreeIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 2

source = files(grammar).joinpath('trio.lark')
with as_file(source) as file:
    grammar = file.open('r', encoding='utf-8')


parser = Lark(grammar, parser='lalr', start='start',
              debug=True, postlex=TreeIndenter(),
              transformer=TreeToJson())

