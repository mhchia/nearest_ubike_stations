# -*- coding: utf-8 -*-
import requests
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from nearest_ubike_station.models import Station

from .exceptions import GoogleAPIError
from .forms import GetUbikeStationForm


# Create your views here.

def response(code, response=[]):

    data = {
            "code"  :   code,
    }
    data["result"] = [] if code != ErrorCode.OK else response
    return data


class ErrorCode:

    ALL_STATIONS_FULL = 1
    OK = 0
    INVALID_LAT_OR_LNG = -1
    LOCATION_NOT_IN_TAIPEI = -2
    SYSTEM_ERROR = -3

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

def get_ubike_station(request):

    if request.method == 'GET':
        form = GetUbikeStationForm(request.GET)
        if form.is_valid():
            lat = form.cleaned_data['lat']
            lng = form.cleaned_data['lng']
            try:
                s = is_in_taipei_city(lat, lng)
                if s == False:
                    return JsonResponse(response(ErrorCode.LOCATION_NOT_IN_TAIPEI))
                q = Station.objects.exclude(num_ubike=0).annotate(
                        distance=(F('lat') - lat) * (F('lat') - lat) + (F('lng') - lng) * (F('lng') - lng)
                    ).order_by('distance')
            except GoogleAPIError:
                return JsonResponse(response(ErrorCode.SYSTEM_ERROR))
            q = [{'station': i.station, 'num_ubike': i.num_ubike} for i in q]
            return JsonResponse(
                response(ErrorCode.OK, q)
            )
        return JsonResponse(response(ErrorCode.INVALID_LAT_OR_LNG))
