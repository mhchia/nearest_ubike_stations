import requests

from .forms import GetUbikeStationForm

class ErrorCode:

    ALL_STATIONS_FULL = 1
    OK = 0
    INVALID_LAT_OR_LNG = -1
    LOCATION_NOT_IN_TAIPEI = -2
    SYSTEM_ERROR = -3

def response(code, response=[]):

    data = {
            "code"  :   code,
    }
    data["result"] = [] if code != ErrorCode.OK else response
    return data

def is_in_taipei_city(lat, lng):

    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}".format(lat, lng)
    r = requests.get(url)
    try:
        address_components = r.json()['results'][0]['address_components']
        for i in address_components:
            if "Taipei City" == i["long_name"]:
                return True
    except IndexError, e:
        raise GoogleAPIError("")
    return False

