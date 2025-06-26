from django.urls import path
from . import api_views

urlpatterns = [
    path('berechnung/', api_views.berechnung_api, name='berechnung_api'),
    path('gebaeude/<int:gebaeude_id>/berechnung/', api_views.gebaeude_berechnung, name='gebaeude_berechnung'),
]