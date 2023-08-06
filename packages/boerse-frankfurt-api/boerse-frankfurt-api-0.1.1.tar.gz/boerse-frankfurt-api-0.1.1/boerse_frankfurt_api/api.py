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


def history(startDate: datetime.datetime,
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