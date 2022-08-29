
#

import re
from typing import MutableSequence, Union
from uuid import uuid4

from haystackparser.exception import RefNotFound, ZincFormatException
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
    """A more or less complete user-defined wrapper around list objects."""

    def __init__(self, initlist: list[Entity]=None):
        self.data:list[Entity] = []
        if initlist is not None:
            # XXX should this accept an arbitrary sequence?
            if type(initlist) == type(self.data):
                self.data[:] = initlist
            elif isinstance(initlist, Ontology):
                self.data[:] = initlist.data[:]
            else:
                self.data = list(initlist)

    def __repr__(self):
        return repr(self.data)

    def __lt__(self, other):
        return self.data < self.__cast(other)

    def __le__(self, other):
        return self.data <= self.__cast(other)

    def __eq__(self, other):
        return self.data == self.__cast(other)

    def __gt__(self, other):
        return self.data > self.__cast(other)

    def __ge__(self, other):
        return self.data >= self.__cast(other)

    def __cast(self, other):
        return other.data if isinstance(other, Ontology) else other

    def __contains__(self, item):
        return item in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key: Union[int, Ref, slice]):
        if isinstance(key, slice):
            return self.__class__(self.data[key])
        elif isinstance(key, Ref):
            filtered = list(filter(lambda entity: entity.id == key, self.data))
            if len(filtered)==0:
                raise RefNotFound(f'Reference {key.value} not found')
            elif len(filtered) > 1:
                raise RefNotFound(f'Reference {key.value} not unic in ontology')

            return filtered[0]
 
        else:
            return self.data[key]

    def __setitem__(self, i, item):
        self.data[i] = item

    def __delitem__(self, i):
        del self.data[i]

    def __add__(self, other):
        if isinstance(other, Ontology):
            return self.__class__(self.data + other.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(self.data + other)
        return self.__class__(self.data + list(other))

    def __radd__(self, other):
        if isinstance(other, Ontology):
            return self.__class__(other.data + self.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(other + self.data)
        return self.__class__(list(other) + self.data)

    def __iadd__(self, other):
        if isinstance(other, Ontology):
            self.data += other.data
        elif isinstance(other, type(self.data)):
            self.data += other
        else:
            self.data += list(other)
        return self

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __imul__(self, n):
        self.data *= n
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]
        return inst

    def append(self, item):
        self.data.append(item)

    def insert(self, i, item):
        self.data.insert(i, item)

    def pop(self, i=-1):
        return self.data.pop(i)

    def remove(self, item):
        self.data.remove(item)

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return self.data.count(item)

    def index(self, item, *args):
        return self.data.index(item, *args)

    def reverse(self):
        self.data.reverse()

    def sort(self, /, *args, **kwds):
        self.data.sort(*args, **kwds)

    def extend(self, other):
        if isinstance(other, Ontology):
            self.data.extend(other.data)
        else:
            self.data.extend(other)