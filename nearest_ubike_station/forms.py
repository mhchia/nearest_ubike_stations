from django import forms

class GetUbikeStationForm(forms.Form):

    lat = forms.FloatField(min_value=-90.0, max_value=90.0)
    lng = forms.FloatField(min_value=-180.0, max_value=180.0)
