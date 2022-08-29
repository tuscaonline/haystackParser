
from linecache import lazycache
from haystackparser.exception import RefNotFound
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

def test_create_tag():
#     myNumberTag = Tag('nombre', Number(23.4))
#     assert myNumberTag.value.value == 23.4
#     myStrTag = Tag('chaine', Str('chaine un longue'))
#     assert myStrTag.value.value == 'chaine un longue'

#     myRefTag = Tag('reference', Ref("@refer.1"))
#     assert myRefTag.value.value == "@refer.1"

    myEntity = Entity(Ref('@entity1', "Essais"))
    myEntity2 = Entity(Ref('@entity2', "Essais"))
    myEntity3 = Entity(Ref('@entity3', "Essais"))

    myOntology = Ontology([myEntity, myEntity2, myEntity3])

    assert myOntology[0] == myEntity
    assert myOntology[1] == myEntity2
    assert myOntology[2] == myEntity3
    assert myOntology[0:2] == [myEntity, myEntity2]
    assert myOntology[Ref('@entity3', "Essaais")] == myEntity3
    with pytest.raises(RefNotFound, 
        match='Reference @entite not found'):
        myOntology[Ref('@entite', "Essaais")]

    