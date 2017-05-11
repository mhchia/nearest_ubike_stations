# -*- coding: utf-8 -*-
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.cache import cache_page

from nearest_ubike_station.models import Station

from .exceptions import GoogleAPIError
from .forms import GetUbikeStationForm
from .utils import ErrorCode, is_in_taipei_city, response


# Create your views here.

@cache_page(60 * 1)
def get_ubike_station(request):

    if request.method == 'GET':
        try:
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
        except:
            return JsonResponse(response(ErrorCode.SYSTEM_ERROR))
