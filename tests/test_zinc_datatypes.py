import re
import pytest
from haystackparser.exception import ZincFormatException
from haystackparser.zinc_datatypes import MARKER, Ref, Symbol, ZincNumber

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
    assert ref.unit == ['square_meter','m²']
    assert ref.__repr__() == "12.34m²"

def test_ZincNumber_2():
    ref = ZincNumber(12.34, "therm")

    assert ref.value == 12.34
    assert ref.unit == ['therm']
    assert ref.__repr__() == "12.34therm"