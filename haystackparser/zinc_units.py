from importlib.resources import as_file, files

from haystackparser.exception import UnitNotFound

from . import resources

_units = {}

_haystackUnitDb = {}


def load_units():
    if(len(_haystackUnitDb) < 1):
        source = files(resources).joinpath('units.txt')
        with as_file(source) as file:
            with file.open('r', encoding='utf-8') as rdr:
                for line in rdr.readlines():
                    if (line.startswith("-") or line.startswith("//") or line.strip()==''):
                        continue

                    _unit, *_dim = line.strip().split(';')
                    canonical, *alias = _unit.split(',')
                    alias = list(map(lambda x: x.strip(), alias))
                    _dim = list(map(lambda x: x.strip(), _dim))
                    _units[canonical] = {
                        'canonical': canonical,
                        'alias': alias,
                        'dimension': _dim
                    }
                    if not alias:
                        _haystackUnitDb[canonical] = canonical
                    else:
                        for symbole in alias:
                            _haystackUnitDb[symbole] = canonical
    pass


def getHaystackUnits(unit: str)-> dict:
    load_units()
    canonical = getCanonical(unit)
    return _units[canonical]

 


def getCanonical(unit: str)-> str:
    load_units()

    canonical = _haystackUnitDb.get(unit, None)
    if (canonical):
        return canonical

    raise UnitNotFound(f'Unit {unit} is not in haystack database')
