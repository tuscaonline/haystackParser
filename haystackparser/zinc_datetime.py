
import re
from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones

import dateutil.parser as dateutil

from haystackparser.exception import TimeZoneNotFound

tz_db = {}  

def _loadTz():
    for row in available_timezones():
        haystack_canonical = row.split('/')
        tz_db[haystack_canonical[-1]] = row
 

def getHaystackTz(tz:str):
    if (len(tz_db)<1):
        _loadTz()        
    try:
        return ZoneInfo(tz_db[tz])
    except Exception:
        raise TimeZoneNotFound(f'Timezone {tz} not found')


def parse_datetime(chaine: str):
    regexTime = "(?P<date>^\d{4}\-\d{2}\-\d{2})[T ](?P<time>\d{2}:\d{2}:\d{2}(?:\.\d+)?)(?P<offset>[Zz]?(?:[+-]\d{2}:\d{2})?)\s?(?P<timezone>[\w\d+-]+)?"
    _dateStruct = re.match(regexTime, chaine)
    _dateStruct = _dateStruct.groupdict()
    _dateStr = f'{_dateStruct.get("date")}'
    _timeStr = f'{_dateStruct.get("time")}'
    _dateTimeStr = f'{_dateStr}T{_timeStr}'
    _offsetStr = f'{_dateStruct.get("offset", None)}'
    _timezoneStr = f'{_dateStruct.get("timezone", None)}'
    if(_timezoneStr != 'None'):
        # If Timezone is present we don't care about offset
        tz = getHaystackTz(_timezoneStr)
        return datetime.fromisoformat(_dateTimeStr).replace(tzinfo=tz)
    else:
        return dateutil.parse(_dateTimeStr + _offsetStr)
