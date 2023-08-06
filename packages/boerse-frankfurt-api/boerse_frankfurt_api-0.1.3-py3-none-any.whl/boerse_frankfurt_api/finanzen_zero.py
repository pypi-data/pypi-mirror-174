import requests
import urllib

scheme = "https"
host = "mein.finanzen-zero.net"

base_url = f"{scheme}://{host}"

class FinanzenZeroUnauthorizedError(Exception):
    pass

def authenticate(username: str, password: str):
    pass



"https://mein.finanzen-zero.net/extapis/findata/chart?period=Maximum&instruments=1330,1174954,1330,814"

def getChartData() -> dict():
    filename = "/extapis/findata/chart"


def getDetail(ISIN: str):
    filename = f"/api/instrument/detail/{ISIN}"
    url = urllib.parse.urljoin(base_url, filename)
    result = requests.get(url)

    if result.status_code == 403:
        res = result.json()
        if "status" in res and "message" in res:
            raise FinanzenZeroUnauthorizedError(res["message"])
        else:
            raise Exception(res)

    if not result.ok:
        raise Exception(result.content)

    return result.json()