
import re
from importlib.resources import as_file, files
from typing import List, Union

import dateutil.parser as dateutil
from lark import Lark
from lark.lexer import Token
from lark.tree import Tree

from . import grammar
from .exception import ParseError, RuleError
from .kinds import (NA, Bool, Coord, HaystackDate, HaystackDateTime,
                    HaystackDict, HaystackList, HaystackTime, HaystackUri,
                    Marker, Number, Ref, Remove, Str, Symbol, XStr)
from .ontology import Entity, Ontology, Tag
from .zinc_datetime import parse_datetime

source = files(grammar).joinpath('trio.lark')
with as_file(source) as file:
    grammarFile = file.open('r', encoding='utf-8')


parser = Lark(grammarFile,  start='start',
              debug=True,
              )


def parse(trio: str) -> Ontology:
    tree = parser.parse(trio)
    myOntology = Ontology()
    for entity in tree.children:
        if entity.data.type == 'RULE' and (entity.data.value == 'first_entity' or entity.data.value == 'entity'):
            myEntity = Entity()
            myOntology.append(myEntity)
            for tag in entity.children:
                if tag.data.type == 'RULE':
                    if tag.data.value == 'tag':

                        name, value = parseTagRule(tag.children)
                        if name == 'id':
                            if not isinstance(value, Ref):
                                raise ParseError(
                                    f'id tag is always a Ref line: {tag.data.line} column : {tag.data.column} ')
                            myEntity.id = value
                        else:
                            myEntity.append(Tag(name, value))
                    elif tag.data.value == 'marker':
                        myEntity.append(Tag(tag.children[0].value, Marker()))
                    elif tag.data.value == 'multiline':
                        name = None
                        myStr = ''
                        for token in tag.children:
                            if token.type == "NAME":
                                name = token.value
                            elif token.type == "TRIO_UNQUOTED_STR":
                                myStr += str(token.value).strip() + "\n"
                        myEntity.append(Tag(name, Str(myStr)))

        else:
            raise RuleError('Rule not implemented')

    return myOntology


def parseTagRule(input: List[Union[Token, Tree]]):
    name = None
    value = None
    for row in input:
        if isinstance(row, Token):
            if row.type == 'NAME':
                name = row.value
            else:
                value = parseScalar(row)

        elif isinstance(row, Tree):
            if isinstance(row.data, Token) and row.data.type == "RULE" and row.data.value == "scalars":

                for token in row.children:
                    value = parseScalar(token)
            elif row.data == "list":
                _value = []
                for _row in row.children:
                    _value.append(parseScalar(_row))
                value = HaystackList(_value)
            elif row.data == "dict":
                _value = HaystackDict()
                for _row in row.children:
                    tagName, tagValue = parseTagRule(_row.children)
                    _value[tagName] = tagValue
                value = _value

    return name, value


def parseScalar(token: Token):
    if token.type == "zinctype__REF":
        _match = re.match(
            r"(?P<ref>^@[0-9a-zA-Z_:\-.~]+)( \"(?P<desc>.*)\")?", token.value)
        value = Ref(_match.groupdict().get("ref", None),
                    _match.groupdict().get("desc", None))
    elif token.type == "zinctype__MARKER":
        value = Marker()
    elif token.type == "zinctype__NA":
        value = NA()
    elif token.type == "zinctype__REMOVE":
        value = Remove()
    elif token.type == "zinctype__BOOL":
        if token.value == 'T':
            value = Bool(True)
        else:
            value = Bool(False)
    elif token.type == "zinctype__NUMBER":
        value = parseNumber(token.value)

    elif token.type == "zinctype__STR":
        value = Str(token.value[1:-1])

    elif token.type == "zinctype__URI":
        value = HaystackUri(token.value[1:-1])

    elif token.type == "zinctype__SYMBOL":
        value = Symbol(token.value)

    elif token.type == "zinctype__DATE":
        value = HaystackDate(dateutil.parse(token.value).date())

    elif token.type == "zinctype__TIME":
        value = HaystackTime(dateutil.parse(token.value).time())

    elif token.type == "zinctype__DATETIME":
        value = HaystackDateTime(parse_datetime(token.value))

    elif token.type == "zinctype__COORD":
        regex = r"^C\((?P<lat>[+-]?\d*\.\d*)\,(?P<lng>[+-]?\d+\.\d*)\)"
        _match = re.match(regex, token.value)
        lat = _match.groupdict().get('lat')
        lng = _match.groupdict().get('lng')
        value = Coord(float(lat), float(lng))

    elif token.type == 'zinctype__XSTR':
        regex = r"^(?P<type>[A-Z][a-zA-Z\d0-9]+)\(\"(?P<val>\w+)\"\)"
        _match = re.match(regex, token.value)
        type = _match.groupdict().get('type')
        val = _match.groupdict().get('val')
        value = XStr(type, val)

    elif token.type == "TRIO_UNQUOTED_STR":
        value = Str(token.value.strip())

    return value


def parseNumber(nb: str):
    if nb == "INF":
        return Number(float('INF'))
    elif nb == "-INF":
        return Number(float("-INF"))
    elif nb == "NaN":
        return Number(float("NaN"))
    else:
        _match = re.match(
            r"(?P<number>^-?[\d]+\.?[\d]*(?:[eE][+-]?\d+)?)(?P<unit>.*)", nb)

        return Number(float(_match.groupdict().get('number', None)),
                      _match.groupdict().get('unit', None))
