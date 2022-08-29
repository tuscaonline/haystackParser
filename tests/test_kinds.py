
from datetime import date, time, datetime
from dis import dis
from math import nan
import math
from zoneinfo import ZoneInfo
import pytest
from haystackparser.exception import ZincFormatException
from haystackparser.kinds import Bool, Coord, HaystackDate, HaystackDateTime, HaystackTime, Marker, NA, Number, Ref, Remove, Str, HaystackUri, Ref, Symbol, XStr


def test_create_marker():
    myMarker = Marker()
    assert type(myMarker) == Marker
    assert myMarker.value == 'M'
    assert str(myMarker) == 'TYPE: marker |VAL: M'
    assert myMarker.jsonValue == {
        "_kind": "marker"
    }
    assert myMarker.zincValue == 'M'


def test_create_NA():
    myNa = NA()
    assert type(myNa) == NA
    assert myNa.value == f'NA'
    assert str(myNa) == f'TYPE: na |VAL: NA'
    assert myNa.jsonValue == {
        "_kind": "na"
    }
    assert myNa.zincValue == 'NA'


def test_create_Remove():
    myRemove = Remove()
    assert type(myRemove) == Remove
    assert myRemove.value == f'R'
    assert str(myRemove) == f'TYPE: remove |VAL: R'
    assert myRemove.jsonValue == {
        "_kind": "remove"
    }
    assert myRemove.zincValue == 'R'


def test_create_Bool_True():
    tag = Bool(True)
    assert type(tag) == Bool
    assert tag.value
    assert str(tag) == f'TYPE: Bool |VAL: True'
    assert tag.jsonValue == {
        "_kind": True
    }
    assert tag.zincValue == 'T'


def test_create_Bool_False():

    tag = Bool(False)
    assert type(tag) == Bool
    assert not tag.value
    assert str(tag) == f'TYPE: Bool |VAL: False'
    assert tag.jsonValue == {
        "_kind": False
    }

    assert tag.zincValue == 'F'


def test_number():
    tag = Number(23.9)
    assert type(tag) == Number
    assert tag.value == 23.9
    assert tag.zincValue == "23.9"
    assert tag.jsonValue == {
        "_kind": "number",
        "val": 23.9
    }
    assert tag.unit == None


def test_numberNan():
    tag = Number(float('nan'))
    assert type(tag) == Number
    assert math.isnan(tag.value)
    assert tag.zincValue == "NaN"
    assert tag.jsonValue == {
        "_kind": "number",
        "val": "NaN"
    }


def test_numberInf():
    tag = Number(float('inf'))
    assert type(tag) == Number
    assert math.isinf(tag.value)
    assert tag.zincValue == "INF"
    assert tag.jsonValue == {
        "_kind": "number",
        "val": "INF"
    }


def test_numberMinusInf():
    tag = Number(float('-inf'))
    assert type(tag) == Number
    assert math.isinf(tag.value)
    assert tag.zincValue == "-INF"
    assert tag.jsonValue == {
        "_kind": "number",
        "val": "-INF"
    }


def test_number_int():
    tag = Number(23)
    assert type(tag) == Number
    assert tag.value == 23
    assert tag.zincValue == "23"
    assert tag.jsonValue == {
        "_kind": "number",
        "val": 23
    }
    assert tag.unit == None


def test_number_unite():
    tag = Number(23, "m2")
    assert type(tag) == Number
    assert tag.value == 23
    assert tag.zincValue == "23m2"
    assert tag.jsonValue == {
        "_kind": "number",
        "val": 23,
        "unit": "m2"
    }
    assert tag.unit.canonical == 'square_meter'


def test_str():
    name = 'str1'
    tag = Str('Une chaine un peu longue \$ \n')
    assert type(tag) == Str
    assert tag.value == 'Une chaine un peu longue $ \n'
    assert tag.zincValue == 'Une chaine un peu longue \$ \n'
    assert tag.jsonValue == {
        "_kind": "str",
        "val": 'Une chaine un peu longue $ \n',
    }


def test_uri():
    name = 'uri1'
    tag = HaystackUri('http://project-haystack.org/')
    assert type(tag) == HaystackUri
    assert tag.value == 'http://project-haystack.org/'
    assert tag.zincValue == '`http://project-haystack.org/`'
    assert tag.jsonValue == {
        "_kind": "uri",
        "val": 'http://project-haystack.org/',
    }


def test_ref_malformed():
    value = '@reftest!'
    with pytest.raises(ZincFormatException,
                       match=f'Ref tag name {value} malformed') as exception:
        ref = Ref(value)


def test_ref():
    value = '@reftest'

    ref = Ref(value)

    assert ref.value == value
    assert ref.zincValue == value
    assert ref.jsonValue == {"_kind": "ref", "val": "reftest"}

def test_ref_displayname():
    value = 'reftest'
    displayname = 'display reftest'

    ref = Ref("@"+ value, displayname)

    assert ref.value == "@"+value
    assert ref.zincValue == f'@{value} "{displayname}"'
    assert ref.jsonValue == {"_kind": "ref", "val": value, "dis": displayname}

def test_symbol():
    value = '^elec-meter'

    ref = Symbol(value)

    assert ref.value == value
    assert ref.zincValue == value
    assert ref.jsonValue == {"_kind": "ref", "val": "elec-meter"}


def test_Date():
    value = date(2022, 8, 3)

    ref = HaystackDate(value)

    assert ref.value == value
    assert ref.zincValue == value.isoformat()
    assert ref.jsonValue == {"_kind": "date", "val": value.isoformat()}


def test_Time():
    value = time(14, 30, 00)

    ref = HaystackTime(value)

    assert ref.value == value
    assert ref.zincValue == value.isoformat()
    assert ref.jsonValue == {"_kind": "time", "val": value.isoformat()}


def test_DateTime():
    value = datetime(2022, 8, 3, 14, 30, 00, tzinfo=ZoneInfo("GMT0"))

    ref = HaystackDateTime(value)

    assert ref.value == value
    assert ref.zincValue == value.isoformat() + ' GMT0'
    assert ref.jsonValue == {
        "_kind": "dateTime",
        "val": value.isoformat(),
        "tz": "GMT0"
    }
    assert ref.tz == ZoneInfo("GMT0")
    assert ref.city == 'GMT0'


def test_DateTimeNoumea():
    value = datetime(2022, 8, 3, 14, 30, 00, tzinfo=ZoneInfo("Pacific/Noumea"))

    ref = HaystackDateTime(value)

    assert ref.value == value
    assert ref.zincValue == value.isoformat() + ' Noumea'
    assert ref.jsonValue == {
        "_kind": "dateTime",
        "val": value.isoformat(),
        "tz": "Noumea"
    }
    assert ref.tz == ZoneInfo("Pacific/Noumea")
    assert ref.city == 'Noumea'


def test_DateTimeUtc():
    value = datetime(2022, 8, 3, 14, 30, 00, tzinfo=ZoneInfo("UTC"))

    ref = HaystackDateTime(value)

    assert ref.value == value
    assert ref.zincValue == value.isoformat() + ' UTC'
    assert ref.jsonValue == {
        "_kind": "dateTime",
        "val": value.isoformat(),
        "tz": "UTC"
    }
    assert ref.tz == ZoneInfo("UTC")
    assert ref.city == 'UTC'


def test_DateTimeNaive():
    value = datetime(2022, 8, 3, 14, 30, 00)

    ref = HaystackDateTime(value)

    assert ref.value == value
    assert ref.zincValue == value.isoformat() + ''
    assert ref.jsonValue == {
        "_kind": "dateTime",
        "val": value.isoformat(),
    }
    assert ref.tz == None
    assert ref.city == None


def test_create_DateTime():
    mydate = HaystackDateTime()
    assert mydate.value == None
    mydate.value = datetime(2022, 8, 3, 14, 30, 00)
    assert mydate.value == datetime(2022, 8, 3, 14, 30, 00)


def test_coords():
    mycoord = Coord(23.43, 12.32)
    assert mycoord.value == {
        "lat": 23.43,
        "lng": 12.32
    }
    assert mycoord.lat == 23.43
    assert mycoord.lng == 12.32
    assert mycoord.zincValue == "C(23.43,12.32)"
    assert mycoord.jsonValue == {
        "_kind": "coord",
        "lat": 23.43,
        "lng": 12.32,
    }


def test_XSTR():
    xstr = XStr("Color", "red")
    assert xstr.value == "red"
    assert xstr.type == "Color"

    assert xstr.zincValue == 'Color("red")'
    assert xstr.jsonValue == {
        "_kind": "xstr",
        "type": "Color",
        "value": "red",
    }


def test_coords_badname():
    tagName = "color"
    with pytest.raises(ZincFormatException,
                       match=f'type name "{tagName}" is incorrect') as exception:
        xstr = XStr(tagName, "red")
