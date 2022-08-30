
#

import re
from collections.abc import MutableSequence
from typing import List, Union
from unittest import IsolatedAsyncioTestCase
from uuid import uuid4

from haystackparser.exception import EntityNotFound, RefNotFound, ZincFormatException
from haystackparser.kinds import Kind, Ref


class Tag:
    def __init__(self, tagName: str, data: Kind) -> None:
        if(not re.match(r'^(^[a-z][a-zA-Z0-9_]*)$', tagName)):
            raise ZincFormatException(f'Tag name : {tagName} is malformed')
        self._name = tagName
        self._value = data

    @property
    def name(self)-> str:
        return self._name

    @property
    def value(self)-> Kind:
        return self._value

    def __repr__(self) -> str:
        return(f'Tag -> type: {type(self.value)}; name: {self.name}; value: {self.value}')



class Entity:
    def __init__(self, id: Ref = None) -> None:

        if(id != None):
            self.id = id # ref
        else:
            self.id = Ref(f'@{uuid4()}')

        self._tags: list[Tag] = []

    @property
    def id(self) -> Ref:
        """Id of the tag"""
        return self._id

    @id.setter
    def id(self, id: Ref ) -> None:
        self._id = id


    @property
    def tags(self) -> list[Kind]:
        """Tags List"""
        return self._tags

    def addTag(self, tag: Tag):
        self._tags.append(tag)

    def __repr__(self) -> str:
        out = f'Entity : ref -> {self._id}\n'
        for tag in self.tags:
            out += f'{tag}\n'
        return(out)


class Ontology(MutableSequence):
    def __init__(self, initvalue=None) -> None:
        self._data: List[Entity]= []
        if initvalue is not None:
            self._data = list(initvalue)
        super().__init__()
    
    def insert(self, index: int, value: Entity) -> None:
        raise NotImplementedError('insert')
        return super().insert(index, value)

    def __getitem__(self, index: Union[int, Ref, slice]) :
        if isinstance(index, int):
            return self._data[index]
        elif isinstance(index, Ref):
            # issume one entity ref is unic
            for data in self._data:
                if data.id == index:
                    return data
            raise EntityNotFound(f'Entity {index.value} not found')
        elif isinstance(index, slice):
            return self.__class__(self._data[index])
        raise NotImplementedError('__getitem__')

    


    def __setitem__(self, index: int, value: Entity) -> None:
        raise NotImplementedError('__setitem__')
    
    def __setitem__(self, index: slice, value: list[Entity]) -> None: 
        raise NotImplementedError('__setitem__')
        
    def __delitem__(self, index: int) -> None:
        raise NotImplementedError('__delitem__')

    def __delitem__(self, index: slice) -> None: 
        raise NotImplementedError('__delitem__')

    def __len__(self) -> int:
        return super().__len__()

    def append(self, value: Entity) -> None:
        if isinstance(value, Entity):
            self._data.append(value)
        else:
            raise TypeError()
