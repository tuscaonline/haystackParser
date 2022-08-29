import pytest
from haystackparser.unitDb import Unit
from haystackparser.exception import UnitNotFound

def test_checkUnits():
    unit = Unit('Af')
    assert unit.canonical == "afghani"


def test_checkUnitsM3():
    unit= Unit('µg/m³')
    assert unit.canonical== "micrograms_per_cubic_meter"


def test_checkUnitsNm():
    unit= Unit('N/m')
    assert unit.canonical == "newtons_per_meter"

def test_errorUnits():
    with pytest.raises(UnitNotFound, match='Unit Stroumph is not in haystack database'):
        Unit('Stroumph')

 

 