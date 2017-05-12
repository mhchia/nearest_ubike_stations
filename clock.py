from apscheduler.schedulers.blocking import BlockingScheduler

from nearest_ubike_station.models import Station
from .utils import get_ubike_stations_data, update_data


sched = BlockingScheduler()

def update_ubike_stations_data():

    data = get_ubike_stations_data()
    update_data(data)

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    update_ubike_stations_data()
    print("[UPDATED] updated ubike stations data.")

sched.start()
