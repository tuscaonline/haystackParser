
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

    newOntology = myOntology[3:4]
    assert newOntology[0] == myentie4
    with pytest.raises(EntityNotFound, match= f'Entity @aze not found' ):
        test = newOntology[Ref("@aze")]