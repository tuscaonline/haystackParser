
from linecache import lazycache
from re import M
from haystackparser.exception import EntityNotFound, RefNotFound
from haystackparser.kinds import Number, Ref, Str
from haystackparser.ontology import Entity, Ontology, Tag
import pytest


# def ontology():
    

#     myEntity = Entity(Ref('@entity1', "Essais"))
#     myEntity.addTag(Tag('nombre', Number(23.4)))
#     myEntity.addTag(Tag('chaine', Str('chaine un longue')))
#     myEntity.addTag( Tag('reference', Ref("@refer.1")))


#     myEntity2 = Entity(Ref('@entity2', "Essais"))
#     myEntity2.addTag(Tag('nombre', Number(253.4)))
#     myEntity2.addTag(Tag('chaine', Str('chaine un longue3')))
#     myEntity2.addTag( Tag('reference', Ref("@refer.2")))

#     myOntolgy = Ontology()
#     myOntolgy.addEntity(myEntity)
#     myOntolgy.addEntity(myEntity2)
#     return myOntolgy

def test_add_tag():
    myOntology = Ontology()
    myentie = Entity(Ref("@aze"))
    myOntology.append(myentie)
    with pytest.raises(TypeError):
        myOntology.append("aze")
    assert myOntology[0]== myentie

def test_get_tag_by_ref():
    myOntology = Ontology()
    myentie = Entity(Ref("@aze"))
    myentie2 = Entity(Ref("@aze2"))
    myOntology.append(myentie)
    myOntology.append(myentie2)
    assert myOntology[Ref("@aze2")] == myentie2
    assert myOntology[Ref("@aze")] == myentie


def test_get_by_slice():
    myOntology = Ontology()
    myentie = Entity(Ref("@aze"))
    myentie2 = Entity(Ref("@aze2"))
    myentie3 = Entity(Ref("@aze3"))
    myentie4 = Entity(Ref("@aze4"))
    myOntology.append(myentie)
    myOntology.append(myentie2)
    myOntology.append(myentie3)
    myOntology.append(myentie4)

    newOntology = myOntology[3:4]
    assert newOntology[0] == myentie4
    with pytest.raises(EntityNotFound, match= f'Entity @aze not found' ):
        test = newOntology[Ref("@aze")]