from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
import json

from .models import Gebaeude, Ort, Bauteil, PVAnlage, Lueftung, Beleuchtung, Waermequelle
from .berechnungen import berechne_energiebilanz


@csrf_exempt
def berechnung_api(request):
    """
    API-Endpoint für Live-Berechnungen
    Akzeptiert GET-Parameter und gibt JSON-Ergebnis zurück
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Nur GET-Requests erlaubt'}, status=405)
    
    try:
        # Parameter aus GET-Request extrahieren
        params = request.GET
        
        # Gebäude-Daten aus Parametern erstellen (Mock-Objekt)
        class MockGebaeude:
            def __init__(self, params):
                self.laenge_ns = float(params.get('laenge_ns', 20))
                self.breite_ow = float(params.get('breite_ow', 15))
                self.geschosse = int(params.get('geschosse', 3))
                self.geschosshoehe = float(params.get('geschosshoehe', 2.8))
                self.personendichte = float(params.get('personendichte', 15))
                self.gebaeudeart = params.get('geb_klasse', 'buero')
                
                # Fensterflächen
                self.fensterflaeche_nord = float(params.get('fenster_nord', 0))
                self.fensterflaeche_sued = float(params.get('fenster_sued', 0))
                self.fensterflaeche_ost = float(params.get('fenster_ost', 0))
                self.fensterflaeche_west = float(params.get('fenster_west', 0))
                
                # g-Werte
                self.g_wert_nord = float(params.get('g_wert_nord', 0.6))
                self.g_wert_sued = float(params.get('g_wert_sued', 0.6))
                self.g_wert_ost = float(params.get('g_wert_ost', 0.6))
                self.g_wert_west = float(params.get('g_wert_west', 0.6))
            
            @property
            def hoehe(self):
                return self.geschosse * self.geschosshoehe
            
            @property
            def grundflaeche(self):
                return self.laenge_ns * self.breite_ow
            
            @property
            def bgf(self):
                return self.grundflaeche * self.geschosse
            
            @property
            def nf(self):
                return self.bgf * 0.85
            
            @property
            def volumen(self):
                return self.bgf * self.geschosshoehe
        
        gebaeude = MockGebaeude(params)
        
        # U-Werte aus Parametern
        bauteile_dict = {}
        for typ in ['wand_nord', 'wand_sued', 'wand_ost', 'wand_west', 'dach', 'bodenplatte']:
            u_wert_key = f'u_wert_{typ}'
            if u_wert_key in params and params[u_wert_key]:
                try:
                    bauteile_dict[typ] = float(params[u_wert_key])
                except ValueError:
                    pass
        
        # Standard-Klimadaten (München)
        klimadaten = {
            'heizgradtage': 3500,
            'solarstrahlung_nord': 300,
            'solarstrahlung_sued': 1100,
            'solarstrahlung_ost': 700,
            'solarstrahlung_west': 700,
        }
        
        # Ort aus Parameter
        ort_name = params.get('ort')
        if ort_name:
            try:
                ort = Ort.objects.get(name=ort_name)
                klimadaten = {
                    'heizgradtage': ort.heizgradtage,
                    'solarstrahlung_nord': ort.solarstrahlung_nord,
                    'solarstrahlung_sued': ort.solarstrahlung_sued,
                    'solarstrahlung_ost': ort.solarstrahlung_ost,
                    'solarstrahlung_west': ort.solarstrahlung_west,
                }
            except Ort.DoesNotExist:
                pass
        
        # Mock-Daten für andere Komponenten
        pv_data = None
        lueftung_data = None
        beleuchtungen_data = []
        waermequellen_data = []
        
        # Berechnung durchführen
        ergebnis = berechne_energiebilanz(
            gebaeude, bauteile_dict, pv_data, lueftung_data,
            beleuchtungen_data, waermequellen_data, klimadaten
        )
        
        return JsonResponse(ergebnis)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def gebaeude_berechnung(request, gebaeude_id):
    """
    API-Endpoint für Berechnung eines spezifischen Gebäudes
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Nur GET-Requests erlaubt'}, status=405)
    
    try:
        gebaeude = get_object_or_404(Gebaeude, id=gebaeude_id)
        
        # Bauteile sammeln
        bauteile_dict = {bt.typ: bt.u_wert for bt in gebaeude.bauteile.all()}
        
        # Klimadaten
        klimadaten = {
            'heizgradtage': gebaeude.ort.heizgradtage,
            'solarstrahlung_nord': gebaeude.ort.solarstrahlung_nord,
            'solarstrahlung_sued': gebaeude.ort.solarstrahlung_sued,
            'solarstrahlung_ost': gebaeude.ort.solarstrahlung_ost,
            'solarstrahlung_west': gebaeude.ort.solarstrahlung_west,
        }
        
        # Andere Komponenten
        try:
            pv_data = gebaeude.pv_anlage
        except:
            pv_data = None
            
        try:
            lueftung_data = gebaeude.lueftung
        except:
            lueftung_data = None
        
        beleuchtungen_data = list(gebaeude.beleuchtungen.all())
        waermequellen_data = list(gebaeude.waermequellen.all())
        
        # Berechnung durchführen
        ergebnis = berechne_energiebilanz(
            gebaeude, bauteile_dict, pv_data, lueftung_data,
            beleuchtungen_data, waermequellen_data, klimadaten
        )
        
        return JsonResponse(ergebnis)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)