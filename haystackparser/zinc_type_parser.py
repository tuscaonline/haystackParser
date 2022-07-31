import datetime
from decimal import Decimal
import re
from zoneinfo import ZoneInfo
from .zinc_datatypes import Uri, ZincNumber, Ref, Symbol
from haystackparser.exception import ZincFormatException
import iso8601

def zinctype__STR(string: str):
    string = string[1:len(string)-1] # Remove unwanted quote
    escaped = string.translate(str.maketrans({"-":  r"\-",
                                            "]":  r"\]",
                                            "\\": r"\\",
                                            "^":  r"\^",
                                            "$":  r"\$",
                                            "*":  r"\*",
                                            ".":  r"\."}))

    return escaped


def zinctype__URI(uri: str):
    uri = uri[1:len(uri)-1] # Remove unwanted quote
    return Uri(uri)

def zinctype__REF(ref: str) -> Ref:
    _ref = ref.split(" ",1)
    if(len(_ref)==2):
        _comment = _ref[1][1:len(_ref[1])-1]
    else:
        _comment = None
    _nom = _ref[0]
    return Ref(_nom, _comment)

def zinctype__SYMBOL(symbol:str):
    return Symbol(symbol)

def zinctype__BOOL(BOOL:str):
    if(BOOL == 'T'):
        return True
    elif (BOOL == 'F'):
        return False
    else:
        raise ZincFormatException(f'The boolean parsing fail, the key is : {BOOL}')

def zinctype__NUMBER(chaine:str):
    regex_number = r"(^-?[\d]+\.?[\d]*(?:[eE][+-]?\d+)?)(.*)"
    if(chaine=="NaN"):
        return Decimal('NaN')
    elif(chaine=="INF"):
        return Decimal('INF')
    elif(chaine=="-INF"):
        return Decimal('-INF')
    else:
        number = re.match(regex_number, chaine)
        if(number.groups()[1]==""):
            try:
                return Decimal(number.groups()[0])
            except:
                raise ZincFormatException(f'The number parsing fail, the key is : {chaine}')
        else:
            return ZincNumber(number.groups()[0], number.groups()[1])


def zinctype__DATE(chaine:str):
    _date= datetime.date.fromisoformat(chaine)
    return _date

def zinctype__TIME(chaine:str):
    _time= datetime.time.fromisoformat(chaine)
    return _time

def zinctype__DATETIME(chaine:str):
    chaine = chaine.split(' ')
    tz = None
    if(len(chaine)>1):
        tz = ZoneInfo(chaine[1])
    _datetime= iso8601.parse_date(chaine[0], tz)
    return _datetime