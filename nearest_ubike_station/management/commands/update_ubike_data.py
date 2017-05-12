import requests

from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler

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

    Station.objects.all().delete()
    print(Station.objects.all().count())
    for i in ret_value:
        s = Station(**i)
        s.save()
    print(Station.objects.all().count())

def update_ubike_stations_data():

    data = get_ubike_stations_data()
#    print(data)
    update_data(data)

class Command(BaseCommand):
    #def handle_noargs(self, **options):
    def handle(self, *args, **options):
        sched = BlockingScheduler()

        @sched.scheduled_job('interval', minutes=1)
        def timed_job():
            try:
                update_ubike_stations_data()
                print("[UPDATED] updated ubike stations data.")
            except:
                print("[FAILED UPDATE]")

        sched.start()
