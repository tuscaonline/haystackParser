from decimal import Decimal
from pyclbr import Class
import re
from haystackparser.exception import ZincFormatException
from haystackparser.zinc_units import getHaystackUnits

REF_CHARS = r"^[a-zA-Z0-9_:\-\.~]+$"
NAME_CHARS= r"^[a-Z][a-zA-Z0-9_]+$"

class Ref:
    """ Class to represent @ref """
    def __init__(self, name:str, comment:str=None) -> None:
        if name.startswith("@"):
            name = name[1:]
        if not (isinstance(name, str) and re.match(REF_CHARS, name)):
            raise ZincFormatException(
                f"reference format is incorrect : {name}")
        self.name = name
        self.comment = comment

    def __str__(self) -> str:
        return f'Ref("@{self.name}", "{self.comment}")'

class Symbol:
    """Class to represent symbol type ^elec-meter"""
    def __init__(self, name:str) -> None:
        if name.startswith('^'):
            name= name[1:]
        if not (isinstance(name, str) and re.match(REF_CHARS, name)):
            raise ZincFormatException(
                f"Symbol format is incorrect : {name}")
        self.name = name
    def __str__(self) -> str:
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

class ZincNumber:
    def __init__(self,  number:Decimal, unit) -> None:
        try:
            self.value = Decimal(number)
        except:
            raise ZincFormatException(f'The number parsing fail, the key is : {chaine}')
        self.unit= getHaystackUnits(unit) 
        # self.quantiy = self.value * ureg(self.unit[0])
    def __repr__(self) -> str:
        return f'{self.value:.2f}{self.unit[-1]}'

class Uri:
    def __init__(self, uri: str) -> None:
        self.value = uri
        pass
    def __str__(self) -> str:
        return f'Symbol("^{self.name}")'    