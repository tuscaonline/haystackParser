
from datetime import date, time, datetime
from dis import dis
import json
from math import nan
import math
from zoneinfo import ZoneInfo
import pytest
from haystackparser.exception import ZincFormatException
from haystackparser.kinds import Bool, Coord, HaystackDate, HaystackDateTime, HaystackDict, HaystackList, HaystackTime, Marker, NA, Number, Ref, Remove, Str, HaystackUri, Ref, Symbol, XStr


class Test_Marker:
    def test_create(self):
        myMarker = Marker()
        assert type(myMarker) == Marker
        assert myMarker == Marker()

    def test_value(self):
        myMarker = Marker()
        assert myMarker.value == 'M'

    def test_jsonValue(self):
        myMarker = Marker()
        assert myMarker.toJson == {
            "_kind": "marker"
        }

    def test_jsonValue(self):
        myMarker = Marker()
        assert myMarker.toZinc == 'M'


class Test_NA:

    def test_create(self):
        myNa = NA()
        assert type(myNa) == NA
        assert myNa.value == f'NA'
        assert myNa.toJson == {
            "_kind": "na"
        }
        assert myNa.toZinc == 'NA'
        assert myNa == NA()


class Test_NA:

    def test_create(self):
        myRemove = Remove()
        assert type(myRemove) == Remove
        assert myRemove.value == f'R'
        assert myRemove.toJson == {
            "_kind": "remove"
        }
        assert myRemove.toZinc == 'R'
        assert myRemove == Remove()


class Test_Bool:
    def test_create_True(self):
        tag = Bool(True)
        assert type(tag) == Bool
        assert tag.value
        assert tag.toJson == {
            "_kind": True
        }
        assert tag.toZinc == 'T'

    def test_create_False(self):

        tag = Bool(False)
        assert type(tag) == Bool
        assert not tag.value
        assert tag.toJson == {
            "_kind": False
        }

        assert tag.toZinc == 'F'


class Test_Number:
    def test_number(self):
        tag = Number(23.9)
        assert type(tag) == Number
        assert tag.value == 23.9
        assert tag.toZinc == "23.9"
        assert tag.toJson == {
            "_kind": "number",
            "val": 23.9
        }
        assert tag.unit == None

    def test_numberNan(self):
        tag = Number(float('nan'))
        assert type(tag) == Number
        assert math.isnan(tag.value)
        assert tag.toZinc == "NaN"
        assert tag.toJson == {
            "_kind": "number",
            "val": "NaN"
        }

    def test_numberInf(self):
        tag = Number(float('inf'))
        assert type(tag) == Number
        assert math.isinf(tag.value)
        assert tag.toZinc == "INF"
        assert tag.toJson == {
            "_kind": "number",
            "val": "INF"
        }

    def test_numberMinusInf(self):
        tag = Number(float('-inf'))
        assert type(tag) == Number
        assert math.isinf(tag.value)
        assert tag.toZinc == "-INF"
        assert tag.toJson == {
            "_kind": "number",
            "val": "-INF"
        }

    def test_number_int(self):
        tag = Number(23.0)
        assert type(tag) == Number
        assert tag.value == 23.0
        assert tag.toZinc == "23.0"
        assert tag.toJson == {
            "_kind": "number",
            "val": 23.0
        }
        assert tag.unit == None

    def test_number_unite(self):
        tag = Number(23.0, "m2")
        assert type(tag) == Number
        assert tag.value == 23.0
        assert tag.toZinc == "23.0m2"
        assert tag.toJson == {
            "_kind": "number",
            "val": 23.0,
            "unit": "m2"
        }
        assert tag.unit.canonical == 'square_meter'


class Test_Str:
    def test_create(self):
        tag = Str('Une chaine un peu longue \$ \n')
        assert type(tag) == Str
        assert tag == 'Une chaine un peu longue $ \n'

    def test_value(self):
        tag = Str('Une chaine un peu longue \$ \n')
        assert tag.value == 'Une chaine un peu longue $ \n'

    def test_json(self):
        tag = Str('Une chaine un peu longue \$ \n')
        assert tag.toJson == {
            "_kind": "str",
            "val": 'Une chaine un peu longue $ \n',
        }

    def test_zinc(self):
        tag = Str('Une chaine un peu longue \$ \n')
        assert tag.toZinc == '"Une chaine un peu longue \$ \n"'


class Test_uri:
    def test_create(self):
        tag = HaystackUri('http://project-haystack.org/')
        assert type(tag) == HaystackUri
        assert tag == 'http://project-haystack.org/'

    def test_value(self):
        tag = HaystackUri('http://project-haystack.org/')
        assert tag.value == 'http://project-haystack.org/'

    def test_json(self):
        tag = HaystackUri('http://project-haystack.org/')
        assert tag.toJson == {
            "_kind": "uri",
            "val": 'http://project-haystack.org/',
        }

    def test_zinc(self):
        tag = HaystackUri('http://project-haystack.org/')
        assert tag.toZinc == '`http://project-haystack.org/`'


class Test_Ref:
    def test_malformed(self):
        value = '@reftest!'
        with pytest.raises(ZincFormatException,
                           match=f'Ref tag name {value} malformed') as exception:
            ref = Ref(value)

    def test_create(self):
        value = '@reftest'
        ref = Ref(value)
        assert ref == value
        assert ref == Ref('@reftest')

    def test_value(self):
        ref = Ref('@reftest')
        assert ref.value == '@reftest'

    def test_json(self):
        ref = Ref('@reftest')
        assert ref.toJson == {"_kind": "ref", "val": "reftest"}

    def test_zinc(self):
        ref = Ref('@reftest')
        assert ref.toZinc == '@reftest'

    def test_with_displayname(self):
        value = 'reftest'
        displayname = 'display reftest'
        ref = Ref("@" + value, displayname)
        assert ref.value == "@"+value
        assert ref.toZinc == f'@{value} "{displayname}"'
        assert ref.toJson == {"_kind": "ref",
                              "val": value, "dis": displayname}


class Test_Symbol:
    def test_create(self):
        value = '^elec-meter'

        ref = Symbol(value)

        assert ref.value == value
        assert ref.toZinc == value
        assert ref.toJson == {"_kind": "ref", "val": "elec-meter"}


class Test_Date:
    def test_Date(self):
        value = date(2022, 8, 3)

        ref = HaystackDate(value)

        assert ref.value == value
        assert ref.toZinc == value.isoformat()
        assert ref.toJson == {"_kind": "date", "val": value.isoformat()}

    def test_Time(self):
        value = time(14, 30, 00)

        ref = HaystackTime(value)

        assert ref.value == value
        assert ref.toZinc == value.isoformat()
        assert ref.toJson == {"_kind": "time", "val": value.isoformat()}

    def test_DateTime(self):
        value = datetime(2022, 8, 3, 14, 30, 00, tzinfo=ZoneInfo("GMT0"))

        ref = HaystackDateTime(value)

        assert ref.value == value
        assert ref.toZinc == value.isoformat() + ' GMT0'
        assert ref.toJson == {
            "_kind": "dateTime",
            "val": value.isoformat(),
            "tz": "GMT0"
        }
        assert ref.tz == ZoneInfo("GMT0")
        assert ref.city == 'GMT0'

    def test_DateTimeNoumea(self):
        value = datetime(2022, 8, 3, 14, 30, 00,
                         tzinfo=ZoneInfo("Pacific/Noumea"))

        ref = HaystackDateTime(value)

        assert ref.value == value
        assert ref.toZinc == value.isoformat() + ' Noumea'
        assert ref.toJson == {
            "_kind": "dateTime",
            "val": value.isoformat(),
            "tz": "Noumea"
        }
        assert ref.tz == ZoneInfo("Pacific/Noumea")
        assert ref.city == 'Noumea'

    def test_DateTimeUtc(self):
        value = datetime(2022, 8, 3, 14, 30, 00, tzinfo=ZoneInfo("UTC"))

        ref = HaystackDateTime(value)

        assert ref.value == value
        assert ref.toZinc == value.isoformat() + ' UTC'
        assert ref.toJson == {
            "_kind": "dateTime",
            "val": value.isoformat(),
            "tz": "UTC"
        }
        assert ref.tz == ZoneInfo("UTC")
        assert ref.city == 'UTC'

    def test_DateTimeNaive(self):
        value = datetime(2022, 8, 3, 14, 30, 00)

        ref = HaystackDateTime(value)

        assert ref.value == value
        assert ref.toZinc == value.isoformat() + ''
        assert ref.toJson == {
            "_kind": "dateTime",
            "val": value.isoformat(),
        }
        assert ref.tz == None
        assert ref.city == None

    def test_create_DateTime(self):
        mydate = HaystackDateTime()
        assert mydate.value == None
        mydate.value = datetime(2022, 8, 3, 14, 30, 00)
        assert mydate.value == datetime(2022, 8, 3, 14, 30, 00)


class Test_Coord:
    def test_create(self):
        mycoord = Coord(23.43, 12.32)
        assert mycoord.value == {
            "lat": 23.43,
            "lng": 12.32
        }
        assert mycoord.lat == 23.43
        assert mycoord.lng == 12.32
        assert mycoord.toZinc == "C(23.43,12.32)"
        assert mycoord.toJson == {
            "_kind": "coord",
            "lat": 23.43,
            "lng": 12.32,
        }


class Test_XStr:
    def test_create(self):
        xstr = XStr("Color", "red")
        assert xstr.value == "red"
        assert xstr.type == "Color"

        assert xstr.toZinc == 'Color("red")'
        assert xstr.toJson == {
            "_kind": "xstr",
            "type": "Color",
            "value": "red",
        }

    def test_badname(self):
        tagName = "color"
        with pytest.raises(ZincFormatException,
                           match=f'type name "{tagName}" is incorrect') as exception:
            xstr = XStr(tagName, "red")


class Test_HaystackList:
    def test_create(self):
        val1 = Marker()
        val2 = Number(234.3)
        val3 = Str('Hello')
        myList = HaystackList([val1, val2, val3])
        assert myList[0] == val1
        assert myList[1] == 234.3

    def test_create_with_err(self):
        val1 = Marker()
        val2 = Number(234.3)
        val3 = Str('Hello')
        with pytest.raises(TypeError, match='Use only kind'):
            myList = HaystackList([val1, "CED", val2, val3])

    def test_len(self):
        val1 = Marker()
        val2 = Number(234.3)
        val3 = Str('Hello')
        myList = HaystackList([val1,   val2, val3])
        assert len(myList) == 3

    def test_set(self):
        val1 = Marker()
        val2 = Number(234.3)
        val3 = Str('Hello')
        myList = HaystackList([val1, val2, val3])
        myList[1] = val3
        assert myList[1] == "Hello"

    def test_del(self):
        val1 = Marker()
        val2 = Number(234.3)
        val3 = Str('Hello')
        myList = HaystackList([val1, val2, val3])
        del myList[1]
        assert myList[1] == "Hello"

    def test_value(self):
        val1 = Marker()
        val2 = Number(234.3)
        val3 = Str('Hello')
        myList = HaystackList([val1, val2, val3])
        assert myList.value == [val1, val2, val3]

    def test_zincvalue(self):
        val1 = Marker()
        val2 = Number(234.3)
        val3 = Str('Hello')
        val4 = Ref("@test")
        myList = HaystackList([val1, val2, val3, val4])
        assert myList.toZinc == '[M, 234.3, "Hello", @test]'


class Test_HaystackDict:
    def test_NameMalformed(self):
        test = HaystackDict()
        with pytest.raises(NameError, match='Name Assais malformed'):
            test["Assais"] = 1

    def test_create_without_kind(self):
        test = HaystackDict()
        with pytest.raises(TypeError, match='Use only kind'):
            test["essais"] = 1

    def test_create(self):
        test = HaystackDict()
        test['ref'] = Ref('@test')
        test['nombre'] = Number(32.2)

        assert test['nombre'] == 32.2
        assert test['ref'] == Ref('@test')

    def test_create_dict(self):
        testRef = Ref('@test')
        testNumber = Number(32.2)

        test = HaystackDict({
            "ref": testRef,
            "nombre": testNumber
        }
        )
        test['ref'] = testRef
        test['nombre'] = testNumber

    def test_value(self):
        test = HaystackDict()
        testRef = Ref('@test')
        testNumber = Number(32.2)
        test['ref'] = testRef
        test['nombre'] = testNumber
        assert test.value == {
            "ref": testRef,
            "nombre": testNumber
        }

    def test_zinc_value(self):
        test = HaystackDict()
        testRef = Ref('@test')
        testNumber = Number(32.2)
        test['ref'] = testRef
        test['nombre'] = testNumber
        assert test.toZinc == r'{ref:@test, nombre:32.2}'

    def test_json_value(self):
        test = HaystackDict()
        testRef = Ref('@test')
        testNumber = Number(32.2)
        test['ref'] = testRef
        test['nombre'] = testNumber
        assert test.toJson == {
            'ref': {
                '_kind': 'ref',
                'val': 'test'
            },
            'nombre': {
                '_kind': 'number', 'val': 32.2
            }
        }
