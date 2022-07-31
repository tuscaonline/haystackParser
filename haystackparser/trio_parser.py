
import logging
from lark import Lark, logger, Transformer, v_args, Tree
from lark.indenter import Indenter
from importlib.resources import files, as_file
from . import grammar


logger.setLevel(logging.DEBUG)


class TreeToJson(Transformer):
    @v_args(inline=True)
    def string(self, s):
        return s[1:-1].replace('\\"', '"')

    def tag(self, item):
        print(f'tag: {item}')
        return item

    def marker(self, item):
        print(f'marker: {item}')
        return item

    @v_args(tree=True)
    def tag_multiline(self, un):
        print(f'tag_multiline: un: {un} ' )
        return un

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

