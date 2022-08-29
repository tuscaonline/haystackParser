import re
from . import resources
from importlib.resources import as_file, files
from .exception import UnitNotFound

import logging

class Unit:
    _unitsDb = {}
    _haystackUnitDb = {}

    def __init__(self, symbol: str) -> None:
        if not(len(self._unitsDb) >0 ):
            self.loadUnitFile()
        self._orig_Symbol= symbol
        self._unit = self._get_unit(symbol)

    def loadUnitFile(self):
        logging.debug('load unitdb')
        source = files(resources).joinpath('units.txt')
        with as_file(source) as file:
            unitfile = file.open('r', encoding='utf-8')

        for row in unitfile:
            if row.startswith("//") or row.strip() == '':
                continue
            elif row.startswith("-- "):
                name, dimension = re.match(r"^-- (.+) \((.+)\)", row).groups()
                if(dimension == "null"):
                    dimension = None
                # print(f'DIMENSION: {name}, {dimension}')
            else:
                temp = row.strip().split(";")
                alias = temp[0].split(",")
                alias = list(map(lambda x: x.strip(), alias))
                canonical = alias[0]
                if len(alias) > 1:
                    alias = alias[1:]
                dim = None
                ratio = None

                if len(temp) > 1:
                    if(temp[1].strip() != ''):
                        dim = temp[1].strip()
                if len(temp) > 2:
                    if(temp[2].strip() != ''):
                        ratio = float(temp[2].strip())
                unitPrint = alias[-1]
                    
                self._unitsDb[canonical] = {
                    "alias": alias.copy(),
                    "dimension": dimension,
                    "ratio": ratio,
                    "print": unitPrint
                }

                if(not ratio and dim==dimension):
                    # add dimension at alias list
                    alias.append(dimension)

                self._haystackUnitDb[canonical] = canonical

                for symbol in alias:
                    self._haystackUnitDb[symbol] = canonical
                
    

    def _get_unit(self, symbole: str) -> dict:
        self._canonical = self._haystackUnitDb.get(symbole, None)
        if self._canonical:
            return self._unitsDb[self._canonical]

        raise UnitNotFound(f'Unit {symbole} is not in haystack database')

    @property
    def canonical(self):
        """Get Canonical form of the symbole"""
        return self._canonical

    @property
    def symbol(self):
        """Get symbol in parameter"""
        return self._orig_Symbol

    @property
    def print(self):
        """Get symbol for printing"""
        return self._unit['print']

    @property
    def dimension(self):
        """Get dimension for conversion op """
        return self._unit['dimension']

    @property
    def ratio(self):
        """Get ratio for conversion op """
        return self._unit['ratio']

    @property
    def alias(self):
        """Get alias of the unit"""
        return self._unit['alias']

    def __repr__(self) -> str:
        return f"Dimension : {self.dimension} ; Original Symbol : {self.symbol} ; Canonical: {self.canonical}"