
# https://project-haystack.org/doc/docHaystack/Kinds
from abc import ABC, abstractmethod
from datetime import date, datetime, time
from math import isinf, isnan
import re
from haystackparser.unitDb import Unit


from .exception import ZincFormatException


NAME_CHARS = r"^[a-z][a-zA-Z0-9_]+$"
JSON_KIND = '_kind'


class Kind(ABC):
    """Classe de base des tag"""

    def __init__(self) -> None:
        super().__init__()

    @property
    @abstractmethod
    def value(self) -> any:
        raise NotImplementedError()

    @abstractmethod
    def __repr__(self, type, value) -> str:
        return f'TYPE: {type} |VAL: {value}'

    @abstractmethod
    def zincValue(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def jsonValue(self) -> dict:
        raise NotImplementedError()


class Marker(Kind):
    """Marker is a singleton used to create "label" tags.
    Markers are used to express typing information."""
    @property
    def value(self) -> any:
        return "M"

    def __repr__(self) -> str:
        return super().__repr__('marker', self.value)

    @property
    def zincValue(self) -> str:
        return "M"

    @property
    def jsonValue(self) -> dict:
        return {
            JSON_KIND: "marker"
        }


class NA(Kind):
    """NA is a singleton for not available.
    It fills a similar role as the NA constant in the R language as
    a place holding for missing or invalid data values.
    In Haystack it is most often used in historized data to indicate
    that a timestamp sample is in error."""
    @property
    def value(self) -> any:
        return "NA"

    def __repr__(self) -> str:
        return super().__repr__('na', self.value)

    @property
    def zincValue(self) -> str:
        return "NA"

    @property
    def jsonValue(self) -> dict:
        return {
            JSON_KIND: "na"
        }


class Remove(Kind):
    """Remove is a singleton used in dicts to indicate removal of a tag.
    It is reserved for future HTTP ops that perform entity updates."""
    @property
    def value(self) -> any:
        return "R"

    def __repr__(self) -> str:
        return super().__repr__('remove', self.value)

    @property
    def zincValue(self) -> str:
        return "R"

    @property
    def jsonValue(self) -> dict:
        return {
            JSON_KIND: "remove"
        }


class Bool(Kind):
    """Bool is the truth data type with the two values true and false."""

    def __init__(self, value: bool) -> None:
        self.value = value
        super().__init__()

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, value: bool) -> None:
        self._value = value

    def __repr__(self) -> str:
        return super().__repr__('Bool', self.value)

    @property
    def zincValue(self) -> str:
        return 'T' if self.value else 'F'

    @property
    def jsonValue(self) -> dict:
        return{
            JSON_KIND: self.value
        }


class Number(Kind):
    """Number is an integer or floating point value with an optional unit of measurement.
    Implementations should represent a number as a 64-bit IEEE 754 floating point and provide 52 bits of lossless integer representation."""

    def __init__(self,  value: float = None, unite: str = None) -> None:
        self.value = value
        self.unit = unite

        super().__init__()

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    @property
    def unit(self) -> Unit:
        if(self._unit):
            return self._unit
        else:
            return None

    @unit.setter
    def unit(self, unite: str) -> None:
        if(unite):
            self._unit = Unit(unite)
        else:
            self._unit = None

    def __repr__(self) -> str:
        return super().__repr__('Number', self.value)

    @property
    def zincValue(self) -> str:
        if isnan(self.value):
            return 'NaN'
        if isinf(self.value):
            return "INF" if self.value > 0 else "-INF"
        if(self.unit):
            return f'{self.value}{self.unit.symbol}'
        else:
            return f'{self.value}'

    @property
    def jsonValue(self) -> dict:
        value = self.value
        if isnan(self.value):
            value = 'NaN'
        if isinf(self.value):
            value = "INF" if self.value > 0 else "-INF"
        if self.unit:
            return{
                JSON_KIND: "number",
                "val": value,
                "unit": self.unit.symbol
            }
        else:
            return{
                JSON_KIND: "number",
                "val": value,
            }


class Str(Kind):
    """Str is a sequence of zero or more Unicode characters.
Implementations must fully support at least the Basic Multilingual Plane (plane 0),
which covers all the 16-bit code points. All text formats must be encoded using
UTF-8 unless explicitly specified otherwise (such as via a charset parameter
in an HTTP Content-Type).
Strings are encoded using double quotes and C style backslash escapes:

"haystack"         // Zinc, Trio, JSON
"Line 1\nLine 2"   // Zinc, Trio, JSON with backslash escape newline
Note that Zinc and Trio require the "$" character to be backslash escaped.

Strings are also used for enumerated types. Enumerations define their range via the enum type.
"""

    def __init__(self,  value: str) -> None:
        self._value = value.replace('\$', '$')
        super().__init__()

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        return super().__repr__('Str', self.value)

    @property
    def zincValue(self) -> str:
        escaped = self.value.translate(str.maketrans({
            "$":  r"\$",
        }))
        return escaped

    @property
    def jsonValue(self) -> dict:
        return{
            JSON_KIND: 'str',
            "val": self.value
        }


class HaystackUri(Kind):
    """Uri is the data type used to represent Universal Resource
    Identifiers according to RFC 3986.

Encodings:

// Zinc, Trio use back tick quotes
`http://project-haystack.org/`

// JSON
{ "_kind": "uri", "val": "http://project-haystack.org/" }"""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__()

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        return super().__repr__('uri', self.value)

    @property
    def zincValue(self) -> str:
        return f'`{self.value}`'

    @property
    def jsonValue(self) -> dict:
        return {
            JSON_KIND: 'uri',
            "val": self.value
        }


class Ref(Kind):
    """"""

    def __init__(self,  value: str, displayname: str = None) -> None:
        self.value = value
        self.displayname = displayname
        super().__init__()

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, val) -> any:
        if not re.match(r"^@[a-zA-Z0-9_:\-\.~]+$", val):
            raise ZincFormatException(f'Ref tag name {val} malformed')
        self._value = val

    @property
    def displayname(self):
        return self._displayname

    @displayname.setter
    def displayname(self, displayname: str):
        self._displayname = displayname

    def __repr__(self) -> str:
        return super().__repr__('Ref', self.value)

    @property
    def zincValue(self) -> str:
        if self._displayname:
            return f'{self.value} "{self.displayname}"'
        return f'{self.value}'

    @property
    def jsonValue(self) -> dict:
        if self._displayname:
            return {
                JSON_KIND: 'ref',
                "val": self.value[1:],
                "dis": self.displayname
            }
        return {
            JSON_KIND: 'ref',
            "val": self.value[1:]
        }
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Ref):
            return self.value == __o.value
        return super().__eq__(__o)


class Symbol(Kind):
    """Symbols are the data type for def identifiers.

Symbols follow the same naming conventions as refs - 
only ASCII letters, digits, underbar, colon, dash, period, or tilde. Although only a subset of these punctuation characters are used today. Dashes are used for conjunct symbols and the colon is used for feature key symbols.

Symbols are encoded using "^" as a prefix:"""

    def __init__(self,  value: str) -> None:
        self.value = value
        super().__init__()

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, val) -> any:
        if not re.match(r"^\^[a-zA-Z0-9_:\-\.~]+$", val):
            raise ZincFormatException(f'Ref symbol name {val} malformed')
        self._value = val

    def __repr__(self) -> str:
        return super().__repr__('Symbol', self.value)

    @property
    def zincValue(self) -> str:
        return f'{self.value}'

    @property
    def jsonValue(self) -> dict:
        return {
            JSON_KIND: 'ref',
            "val": self.value[1:]
        }


class HaystackDate(Kind):
    """Date is an ISO 8601 calendar date. It is encoded as YYYY-MM-DD:"""

    def __init__(self, value: date) -> None:
        self.value = value
        super().__init__()

    @property
    def value(self) -> date:
        return self._value

    @value.setter
    def value(self, date: date) -> None:
        self._value = date

    def __repr__(self) -> str:
        return super().__repr__('date', self.value)

    @property
    def zincValue(self) -> str:
        return f'{self.value}'

    @property
    def jsonValue(self) -> dict:
        return {
            JSON_KIND: 'date',
            "val": self.value.isoformat()
        }


class HaystackTime(Kind):
    """Time is an ISO 8601 time of day. It is encoded as hh:mm:ss.sss:"""

    def __init__(self,  value: time) -> None:
        self.value = value
        super().__init__()

    @property
    def value(self) -> time:
        return self._value

    @value.setter
    def value(self, time: time) -> None:
        self._value = time

    def __repr__(self) -> str:
        return super().__repr__('time', self.value)

    @property
    def zincValue(self) -> str:
        return f'{self.value}'

    @property
    def trioValue(self) -> str:
        return f'{self.name}:{self.zincValue}'

    @property
    def jsonValue(self) -> dict:
        return{
            JSON_KIND: 'time',
            "val": self.value.isoformat()
        }


class HaystackDateTime(Kind):
    """DateTime is an ISO 8601 timestamp paired with a timezone name. Haystack requires all timestamps to include a timezone. Timezone names are standardized in the timezone database (city name from zoneinfo database). Implementations should support DateTime precision at least down to the millisecond."""

    def __init__(self,  value: time = None) -> None:
        self.value = value
        super().__init__()

    @property
    def value(self) -> time:
        return self._value

    @value.setter
    def value(self, date: datetime) -> None:
        self._value = date

    @property
    def tz(self):
        return self._value.tzinfo

    @property
    def city(self):
        zone = str(self.tz).split('/')

        if len(zone) == 2:
            return zone[1]
        else:
            if zone[0] == "None":
                return None
            return zone[0]

    def __repr__(self) -> str:
        return super().__repr__('datetime', self.value)

    @property
    def zincValue(self) -> str:
        if self.city:
            return f'{self.value.isoformat()} {self.city}'
        else:
            return f'{self.value.isoformat()}'

    @property
    def jsonValue(self) -> dict:
        if self.city:
            return{
                JSON_KIND: 'dateTime',
                "val": self.value.isoformat(),
                "tz": f"{self.city}"
            }
        else:
            return{
                JSON_KIND: 'dateTime',
                "val": self.value.isoformat()
            }


class Coord(Kind):
    """Coord is a specialized data type to represent a geographic coordinate as 
    a latitude and longitude. Haystack uses a special atomic type for coordinates 
    to optimize historization of geolocation for transportation applications 
    (versus a collection data type such as dict).
    Latitude and longitude are represented in decimal degrees.
    Implementations should support precision down to the micro-degree (6 decimal places)
    which provides accuracy to ~100mm and can be packed into a 64-bit integer.
    Coord is encoded using positive/negative latitude, longitude in decimal degrees"""

    def __init__(self,  lat: float = None, lng: float = None) -> None:

        self._set_value(lat, lng)

        super().__init__()

    @property
    def value(self) -> dict:
        return self._value

    def _set_value(self, lat: float, lng: float) -> any:
        self._value = {
            "lat": lat,
            "lng": lng
        }

    @property
    def lat(self) -> float:
        return self._value['lat']

    @lat.setter
    def lat(self, value: float) -> None:
        self._value['lat'] = value

    @property
    def lng(self) -> float:
        return self._value['lng']

    @lng.setter
    def lng(self, value: float) -> None:
        self._value['lng'] = value

    @value.setter
    def value(self, lat: float, lng: float) -> dict:
        self._value = {
            "lat": lat,
            "lng": lng
        }

    def __repr__(self) -> str:
        return super().__repr__('coord', self.value)

    @property
    def zincValue(self) -> str:
        return f'C({self.value["lat"]},{self.value["lng"]})'

    @property
    def jsonValue(self) -> dict:
        return {
            JSON_KIND: 'coord',
            "lat": self.value["lat"],
            "lng": self.value["lng"]
        }


class XStr(Kind):
    """XStr is a tuple of a "type name" and string encoded value. 
    The type name must follow tag naming rules except it must start
    with an ASCII upper case letter (A-Z). XStrs provide a mechanism
    for vendors to round trip specific string encoded atomic values.
    The type name is not currently standardized by Project Haystack. 
    However it should be assumed that future versions of this specification
    may standardize a set of XStr type names."""

    def __init__(self,  type: str = None, value: str = None,) -> None:
        self._value = {
            "value": None,
            "type": None
        }
        self.type = type
        self.value = value
        super().__init__()

    @property
    def value(self) -> dict:
        return self._value

    @property
    def type(self) -> str:
        return self._value['type']

    @type.setter
    def type(self, value: str) -> None:
        if (not re.match(r"^[A-Z][a-zA-Z0-9_]+$", value)):
            raise ZincFormatException(
                f'type name "{value}" is incorrect'
            )

        self._value['type'] = value

    @property
    def value(self) -> str:
        return self._value['value']

    @value.setter
    def value(self, value: str) -> None:
        self._value['value'] = value

    def __repr__(self) -> str:
        return super().__repr__('coord', self.value)

    @property
    def zincValue(self) -> str:
        return f'{self.type}("{self.value}")'

    @property
    def jsonValue(self) -> dict:
        return{
            JSON_KIND: 'xstr',
            "type": self.type,
            "value": self.value
        }
