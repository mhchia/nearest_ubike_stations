from django import forms
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from nearest_ubike_station.models import Station


class StationForm(forms.ModelForm):

    class Meta:
        model = Station
        fields = ['name', 'num_bikes', 'lat', 'lng']

# Create your views here.

def get_ubike_station(request):

    s = {1:2}
    return JsonResponse(s)

def get_ubike_station_by_pk(request, pk):

    station = Station.objects.get(pk=int(pk))
    station.name = "<del> shit </del>"
    return render(request, "station.html", {'station' : station})

def create_station(request):

    if request.method == 'POST':
        form = StationForm(request.POST)  # fill params in request into form, then we can use form.is_valid() to check whether the paramters are correct.
        if form.is_valid():
            new_station = form.save()
            return HttpResponseRedirect('/ubike/' + str(new_station.pk))
    form = StationForm()
    print(form.is_valid())
    return render(request, 'create_station.html', {'form': form })
