import pytest
from haystackparser.zinc_units import getCanonical, getHaystackUnits
from haystackparser.exception import UnitNotFound

def test_checkUnits():
    unit= getHaystackUnits('Af')
    assert unit == ["afghani","AFN","Af"]


def test_checkUnitsM3():
    unit= getHaystackUnits('µg/m³')
    assert unit == ["micrograms_per_cubic_meter","µg/m³"]


def test_checkUnitsNm():
    unit= getHaystackUnits('N/m')
    assert unit == ["newtons_per_meter","N/m"]
 
def test_errorUnits():
    with pytest.raises(UnitNotFound, match='Unit Stroumph is not in haystack database'):
        getHaystackUnits('Stroumph')

def test_getCanonical():
    unit= getCanonical('N/m')
    assert unit == "newtons_per_meter"

def test_getCanonicalError():
    with pytest.raises(UnitNotFound, match='Unit Stroumph is not in haystack database'):
        unit= getCanonical('Stroumph')