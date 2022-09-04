
from datetime import datetime
from math import isinf, isnan
from zoneinfo import ZoneInfo
from haystackparser.kinds import NA, Marker, Ref, Remove
from haystackparser.trio_parser import parse


class Test_trio():
    def test_parse_ref(self):
        trio = """
id: @test "test"
test: @essais
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[0].id.displayname == "test"
        assert ontology[Ref('@test')]['test'].kind == Ref('@essais')

    def test_parse_marker(self):
        trio = """
id: @test "test"
test: M
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == Marker()

    def test_parse_NA(self):
        trio = """
id: @test "test"
test: NA
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == NA()

    def test_parse_REMOVE(self):
        trio = """
id: @test "test"
test: R
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == Remove()

    def test_parse_BOOL_True(self):
        trio = """
id: @test "test"
test: T
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == True

    def test_parse_BOOL_False(self):
        trio = """
id: @test "test"
test: F
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == False

    def test_parse_NUMBER(self):
        trio = """
id: @test "test"
test: 23
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == 23.0

    def test_parse_NUMBER_float(self):
        trio = """
id: @test "test"
test: 23.1
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == 23.1

    def test_parse_NUMBER_float_m(self):
        trio = """
id: @test "test"
test: 23.1m
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == 23.1
        assert ontology[Ref('@test')]['test'].kind.unit == 'm'

    def test_parse_NUMBER_INF(self):
        trio = """
id: @test "test"
test: INF
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert isinf(ontology[Ref('@test')]['test'].kind.value)

    def test_parse_NUMBER_minus_INF(self):
        trio = """
id: @test "test"
test: -INF
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert isinf(ontology[Ref('@test')]['test'].kind.value)

    def test_parse_NUMBER_minus_Nan(self):
        trio = """
id: @test "test"
test: NaN
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert isnan(ontology[Ref('@test')]['test'].kind.value)

    def test_parse_str(self):
        trio = """
id: @test "test"
test: "A long string "
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == "A long string "

    def test_parse_uri(self):
        trio = """
id: @test "test"
test: `http://project-haystack.org/`
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref(
            '@test')]['test'].kind == "http://project-haystack.org/"

    def test_parse_Symbol(self):
        trio = """
id: @test "test"
test: ^elec-meter
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == "^elec-meter"

    def test_parse_DATE(self):
        trio = """
id: @test "test"
test: 2020-07-17
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == "2020-07-17"

    def test_parse_TIME(self):
        trio = """
id: @test "test"
test: 14:30:00
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == "14:30:00"

    def test_parse_DateTime(self):
        trio = """
id: @test "test"
test: 2020-07-17T16:55:42.977-04:00 New_York 
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind.city == "New_York"
        assert ontology[Ref('@test')]['test'].kind.value == datetime(2020, 7, 17, 16,
                                                                      55, 42, 977000, ZoneInfo('America/New_York'))

    def test_parse_COORD(self):
        trio = """
id: @test "test"
test: C(37.5458266,-77.4491888) 
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind.lat == 37.5458266
        assert ontology[Ref('@test')]['test'].kind.lng == -77.4491888

    def test_parse_XSTR(self):
        trio = """
id: @test "test"
test: Color("red")
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind.value == "red"
        assert ontology[Ref('@test')]['test'].kind.type == "Color"

    def test_parse_unquoted_str(self):
        trio = """
id: @test "test"
test2:  A long string 
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test2'].kind == "A long string"

    def test_parse_marker_no_comma(self):
        trio = """
id: @test "test"
test2
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test2'].kind == Marker()

    def test_parse_marker_multiline(self):
        trio = """
id: @test "test"
test2:
    bonjour le monde
    comment allez vous
test
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test'].kind == Marker()
        assert ontology[Ref('@test')]['test2'].kind == """bonjour le monde
comment allez vous
"""

    def test_parse_entity(self):
        trio = """
id: @test "test"
test2:  A long string 
---
id: @test2 "test deux"
mark
"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test2'].kind == "A long string"
        assert ontology[Ref('@test2')]['mark'].kind == Marker()

    def test_parse_list(self):
        trio = """
id: @test "test"
test2: ["aze",2,3]

"""
        ontology = parse(trio)
        assert ontology[0].id == Ref('@test')
        assert ontology[Ref('@test')]['test2'].kind.value[0] == "aze"
        assert ontology[Ref('@test')]['test2'].kind.value[1] == 2
        assert ontology[Ref('@test')]['test2'].kind.value[2] == 3

    def test_parse_dict(self):
        trio = """
id: @test "test"
test2:{test:"test", num:2.3 }

"""
        ontology = parse(trio)
        assert ontology[Ref('@test')]['test2'].kind.toJson == {
            'test': {'_kind': 'str', 'val': 'test'},
            'num': {'_kind': 'number', 'val': 2.3}
        }
