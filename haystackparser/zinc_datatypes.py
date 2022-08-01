from decimal import Decimal
import re

from haystackparser.exception import ZincFormatException
from haystackparser.zinc_units import getHaystackUnits

REF_CHARS = r"^[a-zA-Z0-9_:\-\.~]+$"
NAME_CHARS = r"^[a-Z][a-zA-Z0-9_]+$"


class Ref:
    """ Class to represent @ref """

    def __init__(self, name: str, comment: str = None) -> None:
        if name.startswith("@"):
            name = name[1:]
        if not (isinstance(name, str) and re.match(REF_CHARS, name)):
            raise ZincFormatException(
                f"reference format is incorrect : {name}")
        self.name = name
        self.comment = comment

    def __repr__(self) -> str:
        return f'Ref("@{self.name}", "{self.comment}")'


class Symbol:
    """Class to represent symbol type ^elec-meter"""

    def __init__(self, name: str) -> None:
        if name.startswith('^'):
            name = name[1:]
        if not (isinstance(name, str) and re.match(REF_CHARS, name)):
            raise ZincFormatException(
                f"Symbol format is incorrect : {name}")
        self.name = name

    def __repr__(self) -> str:
        return f'Symbol("^{self.name}")'


class _Singleton:
    def __copy__(self) -> '_Singleton':
        return self

    def __deepcopy__(self, memo: '_Singleton') -> '_Singleton':
        # A singleton return himself
        return self

    def __hash__(self) -> int:
        return hash(self.__class__)


class _MarkerType(_Singleton):
    """A singleton class representing a Marker."""

    def __repr__(self) -> str:
        return 'MARKER'


MARKER = _MarkerType()


class _NAType(_Singleton):
    """A singleton class representing a NA."""

    def __repr__(self) -> str:
        return 'NA'


NA = _NAType()


class _RemoveType(_Singleton):
    """A singleton class representing a Remove."""

    def __repr__(self) -> str:
        return 'REMOVE'


REMOVE = _RemoveType()

class _NullType(_Singleton):
    """A singleton class representing a Remove."""

    def __repr__(self) -> str:
        return 'NULL'


NULL = _NullType()


class ZincNumber:

    def __init__(self,  number: Decimal, unit) -> None:
        self.value = Decimal(number)
        _unit = getHaystackUnits(unit)
        self.unit = Unite(unit)

        # self.quantiy = self.value * ureg(self.unit[0])
    def __repr__(self) -> str:
        return f'{self.value:.2f}{self.unit.getPrintUnit()}'


class Uri:
    def __init__(self, uri: str) -> None:
        self.value = uri
        pass

    def __repr__(self) -> str:
        return f'Url "{self.value}"'


class Unite:
    def __init__(self, unit: str) -> None:
        _unit = getHaystackUnits(unit)
        self.canonical = _unit.get('canonical')
        self.alias = _unit.get('alias')
        self.dimension = _unit.get('dimension')

    def getPrintUnit(self) -> str:
        if(self.alias):
            return self.alias[-1]
        else:
            return self.canonical

    def __repr__(self) -> str:
        return f'{self.getPrintUnit()}'


class Coords:
    def __init__(self, latitude, longitude) -> None:
        self.lat = float(latitude)
        self.lng = float(longitude)

    def __repr__(self) -> str:
        lat = toDms(self.lat)
        lng = toDms(self.lng)

        return (
            f'Latitude: {abs(lat[0])}° {lat[1]}\' {lat[2]:.4f}\"{"S" if lat[0]<0 else "N"}, '
            f'Longitude: {abs(lng[0])}° {lng[1]}\' {lng[2]:.4f}\"{"W" if lng[0]<0 else "E"}'
        )


def toDms(dDec: float):
    d = int(dDec)
    m = int(60 * abs(dDec-d))
    s = 3600 * abs(dDec-d) - 60 * m
    return d, m, s

class XStr:
    def __init__(self, type:str, val: str) -> None:
        self.type = type
        self.val = val
    def __repr__(self) -> str:
        return(
            f'{self.type}("{self.val}")'
        )

class Tag:
    def __init__(self, name:str, val: any) -> None:
        regexName = r'^(^[a-z][a-zA-Z0-9_]*)$'
        test = re.match(regexName, name)
        if(not test):
            raise ZincFormatException(f'Tag name : {name} is malformed')
        self.name = name
        self.val = val

    def __repr__(self) -> str:
        return(
            f'{self.name} : {self.val}'
        )
    
    def __rich_repr__(self):
        yield self.name
        yield 'valeur', self.val

class Entity:
    def __init__(self, val: list[Tag] ) -> None:
        self.val = val

    def __repr__(self) -> str:
        chaine = 'Entity:\n'
        for line in self.val:
            chaine += f'{line}\n'
        return(
            chaine.strip()
        )
    def __rich_repr__(self):
        yield  self.val

class Ontology:
    def __init__(self, val: list[Entity]) -> None:
        self.val = val

    def __repr__(self) -> str:
        chaine = 'Ontology:\n'
        for line in self.val:
            chaine += f'{line}\n'
        return(
            chaine.strip()
        )
    
    def __rich_repr__(self):
        return self.val