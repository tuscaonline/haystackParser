from codecs import unicode_escape_decode
from importlib.resources import files, as_file
import csv

from haystackparser.exception import UnitNotFound

from . import resources

_units=[]

_haystackUnitDb= {}

def load_units():
    if(len(_haystackUnitDb)<1):
        source = files(resources).joinpath('units.txt')
        with as_file(source) as file:
            with file.open('r', encoding='utf-8') as rdr:
                for line in rdr.readlines():
                    if line.startswith("-"):
                        continue
                    canonical, *alias = line.rstrip().split(',')
                    _units.append([canonical, *alias])
                    if not alias:
                        _haystackUnitDb[canonical] = canonical
                    else:
                        for symbole in alias:
                            _haystackUnitDb[symbole] = canonical





 
def getHaystackUnits(unit:str):
    load_units()

    for row in _units:
        if(unit in row):
            return row
    raise UnitNotFound(f'Unit {unit} is not in haystack database')

def getCanonical(unit:str):
    load_units()
    
    canonical = _haystackUnitDb.get(unit, None)
    if (canonical):
        return canonical

    raise UnitNotFound(f'Unit {unit} is not in haystack database')


