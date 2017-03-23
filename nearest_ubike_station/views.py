# -*- coding: utf-8 -*-
import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View

from nearest_ubike_station.models import Station
from .forms import GetUbikeStationForm


class GoogleAPIError(Exception):

    pass

# Create your views here.

class UbikeStation(View):

    def post(self, request):

        return HttpResponse("HA")

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
            except GoogleAPIError:
                pass
            return JsonResponse({'1':s})
    return JsonResponse({})

