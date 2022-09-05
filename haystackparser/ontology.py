
#

import re
from collections.abc import MutableSequence
from typing import Any, List, Union
from uuid import uuid4

from haystackparser.exception import (DontChangeTagName, DuplicateEntity, DuplicateTag, EntityNotFound, TagNotFound,
                                      ZincFormatException)
from haystackparser.kinds import (NA, Bool, Coord, HaystackDate, HaystackDateTime, HaystackDict, HaystackList,
                                  HaystackTime, HaystackUri, Kind, Marker, Number, Ref,
                                  Remove, Str, Symbol, XStr)
from haystackparser.util import populateListWithNone

Kinds = Union[Marker, NA, Remove, Bool, Number, Str,
              HaystackUri, Ref, Symbol, HaystackDate,
              HaystackTime, HaystackDateTime, Coord, XStr,
              HaystackDict, HaystackList
              ]


class Tag:
    def __init__(self, tagName: str, data: Kinds) -> None:
        if(not re.match(r'^(^[a-z][a-zA-Z0-9_]*)$', tagName)):
            raise ZincFormatException(f'Tag name : {tagName} is malformed')
        self._name = tagName
        if not (isinstance(data, Kind) ):
            raise TypeError('Please Use only Kinds')
        self._value = data

    @property
    def name(self) -> str:
        return self._name

    @property
    def kind(self) -> Kinds:
        return self._value

    def __call__(self) -> Kinds:
        return self.kind

    def trio_dumper(self) -> str:
        return f'{self.name}:{self.kind.toZinc}'

class Entity(MutableSequence):
    def __init__(self, id: Ref = None, initValue: List[Tag] = None) -> None:
        self._tags: list[Tag] = []

        if(id != None):
            self.id = id  # ref
        else:
            self.id = Ref(f'@{uuid4()}')
        if initValue != None:
            for tag in initValue:
                self._addTag(tag)

    @property
    def id(self) -> Ref:
        """Id of the tag"""
        return self._id

    @id.setter
    def id(self, id: Ref) -> None:
        self._id = id

    def insert(self, index: int, value: Tag) -> None:
        raise NotImplementedError('Use append')

    def __getitem__(self, index: Union[int, slice,  str]) -> Tag:
        if isinstance(index, int) or isinstance(index, slice):
            return self._tags[index]
        elif isinstance(index, str):
            idx, tag = self._getTagByName(index)
            return tag
        else:
            raise NotImplementedError()

    def __setitem__(self, index: Union[int, str, slice], value: Tag) -> None:
        if isinstance(index, int):
            if self._tags[index].name == value.name:
                self._tags[index] = value
            else:
                raise DontChangeTagName()
        elif isinstance(index, str):
            idx, data = self._getTagByName(index)
            if self._tags[idx].name == value.name:
                self._tags[idx] = value
            else:
                raise DontChangeTagName()

        elif isinstance(index, slice):
            raise NotImplementedError(
                "Update Entity by slice is unsupported")
        else:
            raise TypeError('Function only accept Int, slice or str in index')

    def __delitem__(self, index: Union[int, str, slice]) -> None:
        if isinstance(index, int) or isinstance(index, slice):
            del self._tags[index]
        elif isinstance(index, str):
            idx, data = self._getTagByName(index)
            del self._tags[idx]
        else:
            raise TypeError('Function only accept Int, slice or Ref in index')

    def __len__(self) -> int:
        return len(self._tags)

    def _getTagByName(self, name: str):
        for idx, tag in enumerate(self._tags):
            if tag.name == name:
                return idx, tag
        raise TagNotFound(
            f'Tag with {name} not found in entity {self.id.value}')

    def _addTag(self, value: Tag):
        """add a tag to the entity, Raise an error if a tag with same name exist"""
        if not isinstance(value, Tag):
            raise TypeError('Entity accept only Tag ')

        try:
            idx, tag = self._getTagByName(value.name)
            raise DuplicateTag(
                f'Tag with name {value.name} already in entity {self.id.value}')
        except TagNotFound:
            self._tags.append(value)

    def append(self, value: Tag) -> None:
        self._addTag(value)

    def trio_dumper(self) -> str:
        trioStr= ''
        trioStr += f'id:{self.id.toZinc}\n'
        for tag in self._tags:
            trioStr += f'{tag.trio_dumper()}\n'
        return trioStr

    @property
    def tags(self):
        return self._tags

class Ontology(MutableSequence):
    def __init__(self, initvalue: List[Entity] = None) -> None:
        self._entities: List[Entity] = []
        if initvalue is not None:
            for data in initvalue:
                self._add_entity(data)

    def insert(self, index: int, value: Entity) -> None:
        raise NotImplementedError('Please Use Append methode')

    def __getitem__(self, index: Union[int, Ref, slice]):
        if isinstance(index, int):
            return self._entities[index]
        elif isinstance(index, Ref):
            # issume one entity ref is unic
            idx, data = self._getEntityByRef(index)
            return data
        elif isinstance(index, slice):
            return self.__class__(self._entities[index])
        else:
            raise TypeError('Function only accept Int, slice or Ref in index')

    def __setitem__(self, index: Union[int, Ref, slice], value: Entity) -> None:
        if isinstance(index, int):
            self._entities[index] = value
        elif isinstance(index, Ref):
            idx, data = self._getEntityByRef(index)
            self._entities[idx] = value
        elif isinstance(index, slice):
            raise NotImplementedError(
                "Update Ontology by slice is unsupported")
        else:
            raise TypeError('Function only accept Int, slice or Ref in index')

    def __delitem__(self, index: Union[int, Ref, slice]) -> None:
        if isinstance(index, int) or isinstance(index, slice):
            del self._entities[index]
        elif isinstance(index, Ref):
            idx, data = self._getEntityByRef(index)
            del self._entities[idx]
        else:
            raise TypeError('Function only accept Int, slice or Ref in index')

    def __len__(self) -> int:
        return len(self._entities)

    def append(self, entity: Entity) -> None:
        self._add_entity(entity)

    def _getEntityByRef(self, index: Ref) -> Entity:
        if not isinstance(index, Ref):
            raise TypeError('Use only Ref in index')

        for idx, data in enumerate(self._entities):
            if data.id == index:
                return idx, data
        raise EntityNotFound(f'Entity {index.value} not found')

    def _add_entity(self, entity: Entity):
        """add an entity, raise an error if an another entity with same id  in ontology"""
        if not isinstance(entity, Entity):
            raise TypeError('Ontologie accept only Entity')

        try:
            self._getEntityByRef(entity.id)
            raise DuplicateEntity(
                f'Entity with ref {entity.id.value} already in ontology')
        except EntityNotFound:
            self._entities.append(entity)

    def trio_dumper(self) -> str:
        trioStr= ''
        for idx, entity in enumerate(self._entities):
            if idx > 0:
                trioStr += '---\n'
            trioStr += f'{entity.trio_dumper()}'
        return trioStr

    @property
    def entities(self):
        return self._entities

class Grid:
    def __init__(self, ontology: Ontology) -> None:
        self._columns: List[str] = []
        self._row:List[List[Kinds]] = []
        self.updateGrid(ontology)


    def _addColumn(self, columnName):
        if not columnName in self._columns:
            self._columns.append(columnName)

    def updateGrid(self, ontology: Ontology ):
        for entity in ontology.entities:
            self._addColumn('id')
            _row:List[Kinds] = []
            _row =  populateListWithNone(_row, len(self._columns))
            _row[self._columns.index('id')] =  entity.id
            for tag in entity.tags:
                self._addColumn(tag.name)
                _row =  populateListWithNone(_row, len(self._columns))
                _row[self._columns.index(tag.name)] = tag.kind

            self._row.append(_row)

 

    def toZinc(self) -> str:
        _str = 'ver:"3.0"\n'
        for col in self._columns:
            _str += f'{col}, '
        _str = _str[0:-2] + "\n"
        for row in self._row:
            for kind in row:
                if isinstance(kind, Kind):
                    _str += f'{kind.toZinc}, '
                else:
                    _str += ', '
            _str = _str[0:-2] + "\n"
        return _str