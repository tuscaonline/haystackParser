
from decimal import Clamped
from linecache import lazycache
from re import M
from haystackparser.exception import DontChangeTagName, DuplicateEntity, DuplicateTag, EntityNotFound, RefNotFound, TagNotFound
from haystackparser.kinds import NA, Marker, Number, Ref, Str
from haystackparser.ontology import Entity, Ontology, Tag
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