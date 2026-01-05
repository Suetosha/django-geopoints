from django import forms
from django.contrib import admin
from django.contrib.gis.geos import Point as GeosPoint
from .models import Point, Message


class PointAdminForm(forms.ModelForm):
    latitude = forms.FloatField(label="Широта (Latitude)", required=False)
    longitude = forms.FloatField(label="Долгота (Longitude)", required=False)

    class Meta:
        model = Point
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.coordinates:
            self.initial['longitude'], self.initial['latitude'] = self.instance.coordinates.tuple

    def save(self, commit=True):
        instance = super().save(commit=False)
        lat = self.cleaned_data.get('latitude')
        lon = self.cleaned_data.get('longitude')

        if lat is not None and lon is not None:
            instance.coordinates = GeosPoint(lon, lat)

        if commit:
            instance.save()
        return instance


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    form = PointAdminForm
    list_display = ('name', 'user', 'get_coords', 'created_at')
    exclude = ('coordinates',)
    fields = ('user', 'name', 'latitude', 'longitude')

    def get_coords(self, obj):
        if obj.coordinates:
            return f"{obj.coordinates.y}, {obj.coordinates.x}"
        return "-"

    get_coords.short_description = 'Широта, Долгота'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'point', 'created_at')
