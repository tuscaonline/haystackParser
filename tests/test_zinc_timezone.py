from zoneinfo import ZoneInfo
import pytest
from haystackparser.exception import TimeZoneNotFound
from haystackparser.zinc_datetime import _loadTz, getHaystackTz


def test_loadTzParis():
    test = getHaystackTz('Paris')
    assert ZoneInfo("Europe/Paris") == test

def test_loadTzMars():
    with pytest.raises(TimeZoneNotFound, 
        match='Timezone Mars not found'):
        getHaystackTz('Mars')