
from datetime import date, datetime, time
from decimal import Clamped
from linecache import lazycache
from re import M
from zoneinfo import ZoneInfo
from haystackparser.exception import DontChangeTagName, DuplicateEntity, DuplicateTag, EntityNotFound, RefNotFound, TagNotFound
from haystackparser.kinds import NA, Bool, Coord, HaystackDate, HaystackDateTime, HaystackDict, HaystackList, HaystackTime, HaystackUri, Marker, Number, Ref, Remove, Str, Symbol, XStr
from haystackparser.ontology import Entity, Grid, Ontology, Tag
import pytest


class Test_Ontology:
    def test_add_Entity(self):
        myOntology = Ontology()
        myentie = Entity(Ref("@aze"))
        myOntology.append(myentie)
        with pytest.raises(TypeError):
            myOntology.append("aze")
        assert myOntology[0] == myentie

    def test_get_Entity_by_ref(self):
        myOntology = Ontology()
        myentie = Entity(Ref("@aze"))
        myentie2 = Entity(Ref("@aze2"))
        myOntology.append(myentie)
        myOntology.append(myentie2)
        assert myOntology[Ref("@aze2")] == myentie2
        assert myOntology[Ref("@aze")] == myentie

    def test_get_by_slice(self):
        myOntology = Ontology()
        myentie = Entity(Ref("@aze"))
        myentie2 = Entity(Ref("@aze2"))
        myentie3 = Entity(Ref("@aze3"))
        myentie4 = Entity(Ref("@aze4"))
        myOntology.append(myentie)
        myOntology.append(myentie2)
        myOntology.append(myentie3)
        myOntology.append(myentie4)

        newOntology = myOntology[2:4]
        assert newOntology[0] == myentie3
        with pytest.raises(EntityNotFound, match=f'Entity @aze not found'):
            test = newOntology[Ref("@aze")]

    def test_set_item(self):
        myentie = Entity(Ref("@aze"))
        myentie2 = Entity(Ref("@aze2"))
        myentie3 = Entity(Ref("@aze3"))
        myentie4 = Entity(Ref("@aze4"))
        myOntology = Ontology([myentie, myentie2, myentie3, myentie4])
        myentie6 = Entity(Ref('@aze4'))
        myOntology[Ref("@aze4")] = myentie6
        assert myOntology[Ref("@aze4")] != myentie4
        assert myOntology[Ref("@aze4")] == myentie6

    def test_add_duplicate_item(self):
        myentie = Entity(Ref("@aze"))
        myentie2 = Entity(Ref("@aze2"))
        myentie3 = Entity(Ref("@aze3"))
        myentie4 = Entity(Ref("@aze4"))
        myentie4b = Entity(Ref("@aze3"))
        myOntology = Ontology([myentie, myentie2, myentie3, myentie4])
        with pytest.raises(DuplicateEntity, match='Entity with ref @aze3 already in ontology'):
            myOntology.append(Entity(Ref("@aze3")))
        with pytest.raises(DuplicateEntity, match='Entity with ref @aze3 already in ontology'):
            myOntology = Ontology(
                [myentie, myentie2, myentie3, myentie4, myentie4b])

    def test_len(self):
        myentie = Entity(Ref("@aze"))
        myentie2 = Entity(Ref("@aze2"))
        myentie3 = Entity(Ref("@aze3"))
        myentie4 = Entity(Ref("@aze4"))
        myOntology = Ontology([myentie, myentie2, myentie3, myentie4])
        assert len(myOntology) == 4

    def test_del(self):
        myentie = Entity(Ref("@aze"))
        myentie2 = Entity(Ref("@aze2"))
        myentie3 = Entity(Ref("@aze3"))
        myentie4 = Entity(Ref("@aze4"))
        myOntology = Ontology([myentie, myentie2, myentie3, myentie4])
        del myOntology[Ref("@aze2")]
        assert myOntology[Ref('@aze4')] == myentie4
        with pytest.raises(EntityNotFound):
            test = myOntology[Ref("@aze2")]


class Test_Entity:
    def test_create(self):
        myEntity = Entity()
        myEntity.id = Ref("@ret", "Test")
        assert myEntity.id == Ref("@ret")

    def test_notTag(self):
        with pytest.raises(TypeError, match='Entity accept only Tag '):
            myEntity = Entity()
            myEntity.id = Ref("@ret", "Test")
            myEntity.append('test')

    def test_add_tag(self):
        myEntity = Entity()
        myEntity.id = Ref("@ret", "Test")
        tag = Tag('test', NA())
        myEntity.append(tag)
        assert myEntity[0] == tag

    def test_add_duplicate_tag(self):
        myEntity = Entity()
        myEntity.id = Ref("@ret", "Test")
        tag = Tag('test', NA())
        tag2 = Tag('test', Marker())
        myEntity.append(tag)
        with pytest.raises(DuplicateTag, match='Tag with name test already in entity @ret'):
            myEntity.append(tag2)

    def test_get_tag_by_name(self):
        myEntity = Entity()
        myEntity.id = Ref("@ret", "Test")
        tag = Tag('test', NA())
        tag2 = Tag('test2', Marker())
        myEntity.append(tag)
        myEntity.append(tag2)
        assert myEntity['test2'] == tag2

    def test_set_tag_by_index(self):
        myEntity = Entity()
        myEntity.id = Ref("@ret", "Test")
        tag = Tag('test', NA())
        myEntity.append(tag)
        tag2 = Tag('test', Marker())

        myEntity[0] = tag2
        assert myEntity[0] == tag2

    def test_set_tag_dontChangeName(self):
        myEntity = Entity()
        myEntity.id = Ref("@ret", "Test")
        tag = Tag('test', NA())
        myEntity.append(tag)
        tag2 = Tag('test1', Marker())
        with pytest.raises(DontChangeTagName):
            myEntity[0] = tag2

    def test_set_tag_by_Name(self):
        myEntity = Entity()
        myEntity.id = Ref("@ret", "Test")
        tag = Tag('test', NA())
        myEntity.append(tag)
        tag2 = Tag('test', Marker())

        myEntity['test'] = tag2
        assert myEntity[0] == tag2

    def test_set_tag_by_Name_dontchange(self):
        myEntity = Entity()
        myEntity.id = Ref("@ret", "Test")
        tag = Tag('test', NA())
        myEntity.append(tag)
        tag2 = Tag('test1', Marker())
        with pytest.raises(DontChangeTagName):
            myEntity['test'] = tag2

    def test_del_tag_by_Name(self):
        myEntity = Entity()
        myEntity.id = Ref("@ret", "Test")
        tag = Tag('test', NA())
        tag2 = Tag('test1', Marker())
        tag3 = Tag('test2', Marker())
        myEntity.append(tag)
        myEntity.append(tag2)
        myEntity.append(tag3)
        del myEntity["test1"]
        with pytest.raises(TagNotFound):
            test = myEntity['test1']

    def test_del_tag_by_index(self):
        myEntity = Entity()
        myEntity.id = Ref("@ret", "Test")
        tag = Tag('test', NA())
        tag2 = Tag('test1', Marker())
        tag3 = Tag('test2', Marker())
        myEntity.append(tag)
        myEntity.append(tag2)
        myEntity.append(tag3)
        del myEntity[1]
        with pytest.raises(TagNotFound):
            test = myEntity['test1']

    def test_create_tag_with_list(self):
        tag = Tag('test', NA())
        tag2 = Tag('test1', Marker())
        tag3 = Tag('test2', Marker())
        myEntity = Entity(Ref("@test"), [tag, tag2, tag3])
        assert myEntity['test'] == tag


class Test_Tag:
    def test_create(self):
        myTag = Tag('test', NA())
        assert myTag.name == 'test'

    def test_error_type(self):
        with pytest.raises(TypeError, match='Please Use only Kinds'):
            myTag = Tag('test', "NA()")

    def test_access_tag(self):
        myTag = Tag('test', Number(34.3))
        assert myTag.name == 'test'
        assert myTag() == 34.3
        assert myTag.kind == 34.3


class Test_TrioDumper:
    def test_one_entity(self):

        entity1 = Entity(Ref('@entity1', "Entity  name"), [
            Tag('number1', Number(43.0)),
            Tag('str1', Str('String 1'))
        ]
        )
        myOntology = Ontology([entity1])
        trioStr = myOntology.trio_dumper()

        trioExpect = """id:@entity1 "Entity  name"
number1:43.0
str1:"String 1"
"""
        assert trioStr == trioExpect

    def test_two_entity(self):

        entity1 = Entity(Ref('@entity1', "Entity  name"), [
            Tag('number1', Number(43.0)),
            Tag('str1', Str('String 1'))
        ]
        )
        entity2 = Entity(Ref('@entity2', "Entity  name"), [
            Tag('number1', Number(43.0)),
            Tag('str1', Str('String 2'))
        ]
        )
        myOntology = Ontology([entity1, entity2])
        trioStr = myOntology.trio_dumper()

        trioExpect = """id:@entity1 "Entity  name"
number1:43.0
str1:"String 1"
---
id:@entity2 "Entity  name"
number1:43.0
str1:"String 2"
"""
        assert trioStr == trioExpect

    def test_tree_entity(self):

        entity1 = Entity(Ref('@entity1', "Entity1  name"), [
            Tag('number1', Number(1.0)),
            Tag('str1', Str('String$ 1'))
        ]
        )
        entity2 = Entity(Ref('@entity2', "Entity2  name"), [
            Tag('number2', Number(2.0)),
            Tag('str2', Str('String$ 2'))
        ]
        )
        entity3 = Entity(Ref('@entity3', "Entity3  name"), [
            Tag('marker3', Marker()),
            Tag('na3', NA()),
            Tag('remove3', Remove()),
            Tag('bool3', Bool(True)),
            Tag('number3', Number(3.0)),
            Tag('str3', Str('String$ 3')),
            Tag('uri3', HaystackUri('http://project-haystack.org/')),
            Tag('ref3', Ref("@entity1")),
            Tag('symbol3', Symbol("^elec-meter")),
            Tag('date3', HaystackDate(date(2020, 7, 17))),
            Tag('time3', HaystackTime(time(14, 30, 0))),
            Tag('datetime3', HaystackDateTime(
                datetime(2020, 7, 17, 14, 30, 0, 930000, ZoneInfo('Pacific/Noumea')))),
            Tag('gps3', Coord(-22.292697, 166.449519)),
            Tag('xstr3', XStr('Color', 'red')),
            Tag('list3',
                HaystackList([
                    Number(1.0),
                    Str("two"),
                    Number(3.0),
                ])
                ),
            Tag('dict3',
                HaystackDict(
                    {
                        'x': Number(1.0),
                        'y': Str("4.0")
                    }
                )
                )

        ]
        )
        myOntology = Ontology([entity1, entity2, entity3])
        trioStr = myOntology.trio_dumper()

        trioExpect = """id:@entity1 "Entity1  name"
number1:1.0
str1:"String\$ 1"
---
id:@entity2 "Entity2  name"
number2:2.0
str2:"String\$ 2"
---
id:@entity3 "Entity3  name"
marker3:M
na3:NA
remove3:R
bool3:T
number3:3.0
str3:"String\$ 3"
uri3:`http://project-haystack.org/`
ref3:@entity1
symbol3:^elec-meter
date3:2020-07-17
time3:14:30:00
datetime3:2020-07-17T14:30:00.930000+11:00 Noumea
gps3:C(-22.292697,166.449519)
xstr3:Color("red")
list3:[1.0, "two", 3.0]
dict3:{x:1.0, y:"4.0"}
"""
        assert trioStr == trioExpect


class Test_Grids:
    def test_create(self):
        entity1 = Entity(Ref('@entity1', "Entity1  name"), [
            Tag('number1', Number(1.0)),
            Tag('str1', Str('String$ 1'))
        ]
        )
        entity2 = Entity(Ref('@entity2', "Entity2  name"), [
            Tag('number2', Number(2.0)),
            Tag('str2', Str('String$ 2')),
            Tag('list3',
                HaystackList([
                    Number(1.0),
                    Str("two"),
                    Number(3.0),
                ])
                ),
            Tag('dict3',
                HaystackDict(
                    {
                        'x': Number(1.0),
                        'y': Str("4.0")
                    }
                )
                )
        ]
        )
        myOntology = Ontology([entity1, entity2])
        myGrid = Grid(myOntology)
        assert myGrid.toZinc() == \
            """ver:"3.0"
id, number1, str1, number2, str2, list3, dict3
@entity1 "Entity1  name", 1.0, "String\$ 1"
@entity2 "Entity2  name", , , 2.0, "String\$ 2", [1.0, "two", 3.0], {x:1.0, y:"4.0"}
"""
