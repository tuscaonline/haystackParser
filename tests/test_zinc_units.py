import pytest
from haystackparser.zinc_units import getCanonical, getHaystackUnits
from haystackparser.exception import UnitNotFound

def test_checkUnits():
    unit= getHaystackUnits('Af')
    assert unit.get('canonical') == "afghani"


def test_checkUnitsM3():
    unit= getHaystackUnits('µg/m³')
    assert unit.get('canonical') == "micrograms_per_cubic_meter"


def test_checkUnitsNm():
    unit= getHaystackUnits('N/m')
    assert unit.get('canonical') == "newtons_per_meter"
    assert unit.get('alias') == ["N/m"]
    assert unit.get('dimension') == ["kg1*sec-2"]
 
def test_errorUnits():
    with pytest.raises(UnitNotFound, match='Unit Stroumph is not in haystack database'):
        getHaystackUnits('Stroumph')

def test_getCanonical():
    unit= getCanonical('N/m')
    assert unit == "newtons_per_meter"

def test_getCanonicalError():
    with pytest.raises(UnitNotFound, match='Unit Stroumph is not in haystack database'):
        unit= getCanonical('Stroumph')