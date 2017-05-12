import requests

from nearest_ubike_station.models import Station


def get_ubike_stations_data():

    url = "http://data.taipei/youbike"
    r = requests.get(url)
    data = r.json()
    ret_code, ret_value = data['retCode'], data['retVal']
    ret_value = [
        {
            'station'   :   ret_value[i]['sna'],
            'num_ubike' :   ret_value[i]['sbi'],
            'lat'       :   ret_value[i]['lat'],
            'lng'       :   ret_value[i]['lng']
        } for i in ret_value.keys()
    ]
    return ret_value

def update_data(ret_value):

    for i in ret_value:
        station, created = Station.objects.update_or_create(
                station=i['station'],
                defaults = i
        )
