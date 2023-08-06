import requests
import urllib
import datetime
import time
from enum import Enum

# https://www.boerse-frankfurt.de/indices/dax

host = "https://api.boerse-frankfurt.de"
api_version = 1

history_path = "tradingview/lightweight/history/single"

class Indication(Enum):
    Xetra = "XETR"
    Ariva = "ARIVA"


class Resolution(Enum):
    minute = "M"
    hour = "H"
    day = "D"
    month = "MO"


def construct_url(path: str) -> str:
    url = urllib.parse.urljoin(host, f"v{api_version}/")
    return urllib.parse.urljoin(url, path)


def history_raw(startDate: datetime.datetime,
            endDate: datetime.datetime,
            isin: str,
            indicator: Indication = Indication.Xetra,
            resolution: Resolution = Resolution.day,
            isKeepResolutionForLatestWeeksIfPossible: bool = False):
    is_ask_price = False
    sd = int(time.mktime(startDate.timetuple()))
    ed = int(time.mktime(endDate.timetuple()))
    url_path = urllib.parse.urljoin(history_path, f"?resolution={resolution.value}&isKeepResolutionForLatestWeeksIfPossible={isKeepResolutionForLatestWeeksIfPossible}&from={sd}&to={ed}&isBidAskPrice={is_ask_price}&symbols={indicator.value}:{isin}")
    url = construct_url(url_path)

    r = requests.get(url)

    if not r.ok:
        return []

    return r.json()

def history(startDate: datetime.datetime,
            endDate: datetime.datetime,
            isin: str,
            indicator: Indication = Indication.Xetra,
            resolution: Resolution = Resolution.day,
            isKeepResolutionForLatestWeeksIfPossible: bool = False) -> []:
    """
    returns a tuple of time value list. The time is the unix time in milliseconds
    """
    res = history_raw(startDate, endDate, isin, indicator, resolution, isKeepResolutionForLatestWeeksIfPossible)
    if len(res) == 0 or type(res[0]) is not dict:
        return [], []

    if "quotes" not in res[0]:
        return [], []

    # to keep it simple do not use numpy
    time = []
    value = []
    count = res[0]["quotes"]["count"]
    tv = res[0]["quotes"]["timeValuePairs"]

    for v in tv:
        time.append(v["time"] * 1000)
        value.append(v["value"])

    return time, value







