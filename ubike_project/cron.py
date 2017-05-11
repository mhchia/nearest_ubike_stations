from nearest_ubike_station.models import Station
from utils import get_ubike_stations_data, update_data

def update_ubike_stations_data():

    data = get_ubike_stations_data()
    update_data(data)
