from django.urls import path
from . import views

urlpatterns = [
    # Hauptseiten
    path('', views.startseite, name='startseite'),
    path('uber-tool/', views.uber_tool, name='uber_tool'),
    path('entwicklerteam/', views.entwicklerteam, name='entwicklerteam'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('hilfe/', views.hilfe, name='hilfe'),
    
    # Wizard-Schritte
    path('allg-angaben/', views.allg_angaben, name='allg_angaben'),
    path('baukrper/', views.baukrper, name='baukrper'),
    path('baukoerper-kp/', views.baukoerper_kp, name='baukoerper_kp'),
    path('baukrper-kp-2/', views.baukrper_kp_2, name='baukrper_kp_2'),
    path('bauteil/', views.bauteil, name='bauteil'),
    path('bauteil-kp/', views.bauteil_kp, name='bauteil_kp'),
    path('pv/', views.pv, name='pv'),
    path('lftung/', views.lftung, name='lftung'),
    path('beleuchtung/', views.beleuchtung, name='beleuchtung'),
    path('beleuchtung-2/', views.beleuchtung_2, name='beleuchtung_2'),
    path('waermequellen/', views.waermequellen, name='waermequellen'),
    path('sdf/', views.sdf, name='sdf'),
    path('gwp/', views.gwp, name='gwp'),
    path('ergebnis/', views.ergebnis, name='ergebnis'),
    
    # Ergebnis-Seiten
    path('einfach-ergebnis/', views.einfach_ergebnis, name='einfach_ergebnis'),
    path('ergebnis-pdf/', views.ergebnis_pdf, name='ergebnis_pdf'),
]