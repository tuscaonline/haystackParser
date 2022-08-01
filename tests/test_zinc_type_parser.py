from datetime import datetime, date, time
from haystackparser import zinc_type_parser
from haystackparser.exception import UnitNotFound, ZincFormatException
from haystackparser.zinc_datatypes import Coords, Ref, Symbol, XStr
import pytest
from zoneinfo import ZoneInfo


def test_parse_zinctype__STR():
    resultat = zinc_type_parser.zinctype__STR('"aqza &"é"fqsd$ "')

    assert resultat == 'aqza &"é"fqsd\$ '


def test_parse_zinctype__URI():
    resultat = zinc_type_parser.zinctype__URI('`https:\\\\www.google.fr`')

    assert resultat.value == 'https:\\\\www.google.fr'


def test_zinctype__REF():
    _ref = Ref('@ref')
    assert _ref.name == zinc_type_parser.zinctype__REF('@ref').name


def test_zinctype__REF_Comment():
    _ref = Ref('@ref2', "Commentaire de test")
    parser = zinc_type_parser.zinctype__REF('@ref2 "Commentaire de test"')
    assert _ref.name == parser.name
    assert _ref.comment == parser.comment


def test_zinctype__SYMBOL():
    _symbol = Symbol('^est')
    parser = zinc_type_parser.zinctype__SYMBOL('^est')
    assert _symbol.name == parser.name


def test_zinctype__BOOL_True():
    assert zinc_type_parser.zinctype__BOOL('T')


def test_zinctype__BOOL_False(): 
    assert not zinc_type_parser.zinctype__BOOL('F')


def test_zinctype__BOOL_Error():
    with pytest.raises(ZincFormatException,
                       match='The boolean parsing fail, the key is : Fazd'):
        zinc_type_parser.zinctype__BOOL('Fazd')


def test_zinctype__NUMBER_NaN():
    nombre = zinc_type_parser.zinctype__NUMBER("NaN")
    assert nombre.is_nan()


def test_zinctype__NUMBER_INF():
    nombre = zinc_type_parser.zinctype__NUMBER("INF")
    assert not nombre.is_signed() and nombre.is_infinite()


def test_zinctype__NUMBER_MINUSINF():
    nombre = zinc_type_parser.zinctype__NUMBER("-INF")
    assert nombre.is_signed() and nombre.is_infinite()


def test_zinctype__NUMBER_12_3E1():
    nombre = zinc_type_parser.zinctype__NUMBER("12E13")
    assert nombre == 12E13


def test_zinctype__NUMBER_ERR():
    with pytest.raises(UnitNotFound,
                       match='Unit Ea13 is not in haystack database'):
        zinc_type_parser.zinctype__NUMBER("12Ea13")


def test_zinctype__NUMBER_12_3E2():
    nombre = zinc_type_parser.zinctype__NUMBER("-12E+13")
    assert nombre == -12E+13


def test_zinctype__NUMBER_EGP():
    quantity = zinc_type_parser.zinctype__NUMBER("-12EGP")
    assert quantity.value == -12
    assert quantity.unit.canonical == 'egyptian_pound'
    assert quantity.__repr__() == '-12.00EGP'


def test_zinctype__NUMBER_percent():
    quantity = zinc_type_parser.zinctype__NUMBER("-12%")
    assert quantity.value == -12
    assert quantity.unit.canonical == 'percent'


def test_zinctype__DATE():
    _date = zinc_type_parser.zinctype__DATE('2022-12-21')
    assert type(_date) == date
    assert _date == datetime(2022, 12, 21).date()


def test_zinctype__DATE():
    _date = zinc_type_parser.zinctype__TIME('12:32:12.321')
    assert type(_date) == time
    assert _date == time(12, 32, 12, 321000)


def test_zinctype__DATETIME():
    _date = zinc_type_parser.zinctype__DATETIME('2010-01-08T05:00:00Z')
    assert type(_date) == datetime
    assert _date == datetime(2010, 1, 8, 5, 0, 0,tzinfo= ZoneInfo('UTC'))

def test_zinctype__DATETIMEUTC():
    _date = zinc_type_parser.zinctype__DATETIME('2010-01-08T05:00:00Z')
    assert type(_date) == datetime
    assert _date == datetime(2010, 1, 8, 5, 0, 0,tzinfo= ZoneInfo('UTC'))

def test_zinctype__DATETIMEGMT():
    _date = zinc_type_parser.zinctype__DATETIME('2010-01-08T05:00:00.123+08:00')
    assert type(_date) == datetime
    assert _date.isoformat() == '2010-01-08T05:00:00.123000+08:00'

def test_zinctype__DATETIMENoumea():
    _date = zinc_type_parser.zinctype__DATETIME('2010-01-08T05:00:00 Noumea')
    assert type(_date) == datetime
    assert _date == datetime(2010, 1, 8, 5, 0, 0,tzinfo= ZoneInfo('Pacific/Noumea'))


def test_zinctype__COORD():
    coord = zinc_type_parser.zinctype__COORD('C(37.5458,-77.4491)')
    assert type(coord)==Coords
    assert coord.lat == 37.5458
    assert coord.lng == -77.4491

def test_zinctype__XStr():
    xstr = zinc_type_parser.zinctype__XStr('Color("red")')
    assert type(xstr)==XStr
    assert xstr.type == 'Color'
    assert xstr.val  == 'red'