
from zoneinfo import ZoneInfo, available_timezones


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


    pass
