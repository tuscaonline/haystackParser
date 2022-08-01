from decimal import Decimal
import re
import pytest
from haystackparser.exception import ZincFormatException
from haystackparser.zinc_datatypes import MARKER, NULL, Coords, Ref, Symbol, Tag, Unite, XStr, ZincNumber, toDms

def test_Ref_1():
    ref = Ref('@est', 'Commentaire test')

    assert ref.name == "est"

def test_Ref_2():
    ref = Ref('est', 'Commentaire test')

    assert ref.name == "est"

def test_Ref_3():
    ref = Ref('e.st', 'Commentaire test')

    assert ref.name == "e.st"

def test_Ref_4():
    ref = Ref('.st', 'Commentaire test')

    assert ref.name == ".st"

def test_Ref_5():
    with pytest.raises(ZincFormatException, 
    match='reference format is incorrect : !.st') as exception:
        ref = Ref('!.st', 'Commentaire test')
    
def test_Ref_6():
    ref = Ref('@.st', 'Commentaire test')

    assert ref.name == ".st"
    assert ref.comment == 'Commentaire test'

def test_Ref_7():
    ref = Ref('@zer', 'Commentaire pas fun')

    assert ref.__str__() == 'Ref("@zer", "Commentaire pas fun")'


def test_Symbol_1():
    ref = Symbol('^est')

    assert ref.name == "est"

def test_Symbol_2():
    with pytest.raises(ZincFormatException, 
    match='Symbol format is incorrect : !est') as exception:
        ref = Symbol('^!est')

def test_ZincNumber_1():
    ref = ZincNumber(12.34, "m²")

    assert ref.value == 12.34
    assert ref.unit.canonical == 'square_meter'
    assert ref.__repr__() == "12.34m²"

def test_ZincNumber_2():
    ref = ZincNumber(12.34, "therm")

    assert ref.value == 12.34
    assert ref.unit.canonical == 'therm'
    assert ref.__repr__() == "12.34therm"

def test_Unite():
    ref = Unite("m²")
    assert ref.canonical == 'square_meter'
    assert ref.alias == ['m²']
    assert ref.getPrintUnit() == 'm²'

def test_Coords():
    coord = Coords('37.545827', '-77.449189' )
    assert coord.lat == 37.545827
    assert coord.lng == -77.449189
    assert coord.__repr__() == """Latitude: 37° 32' 44.9772"N, Longitude: 77° 26' 57.0804"W"""

def test_toDms():
    coord = toDms(37.545827)
    assert coord[0] == 37
    assert coord[1] == 32
    assert coord[2] == 44.977200000009816
    

def test_toDms2():
    coord = toDms(-37.545827)
    assert coord[0] == -37
    assert coord[1] == 32
    assert coord[2] == 44.977200000009816

def test_XStr():
    xstr = XStr("Color", 'red' )
    assert xstr.type == "Color"
    assert xstr.val == 'red' 
    assert xstr.__repr__() == 'Color("red")'

def test_Tag():
    tag = Tag('nOm2_1', NULL)
    assert tag.name == 'nOm2_1'
    assert tag.val == NULL

def test_TagMalformed():
    tag = 'NOm2_1'
    with pytest.raises(ZincFormatException, match=f'Tag name : {tag} is malformed'):
        tag = Tag(tag, NULL)

def test_TagMalformed2():
    tag = '!Om2_1'
    with pytest.raises(ZincFormatException, match=f'Tag name : {tag} is malformed'):
        tag = Tag(tag, NULL)

def test_TagMalformed3():
    tag = 'nOaém2_1'
    with pytest.raises(ZincFormatException, match=f'Tag name : {tag} is malformed'):
        tag = Tag(tag, NULL)