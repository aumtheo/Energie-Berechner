from django.test import TestCase, Client
from django.urls import reverse
from .models import Gebaeude, Ort, Bauteil
from .berechnungen import berechne_heizwaermebedarf, berechne_energiebilanz


class OrtModelTest(TestCase):
    def setUp(self):
        self.ort = Ort.objects.create(
            name='Test Stadt',
            temperatur_mittel=9.0,
            heizgradtage=3500,
            solarstrahlung_nord=300,
            solarstrahlung_sued=1100,
            solarstrahlung_ost=700,
            solarstrahlung_west=700,
            solarstrahlung_horizontal=1000,
        )

    def test_ort_str(self):
        self.assertEqual(str(self.ort), 'Test Stadt')


class GebaeudeModelTest(TestCase):
    def setUp(self):
        self.ort = Ort.objects.create(
            name='Test Stadt',
            temperatur_mittel=9.0,
            heizgradtage=3500,
            solarstrahlung_nord=300,
            solarstrahlung_sued=1100,
            solarstrahlung_ost=700,
            solarstrahlung_west=700,
            solarstrahlung_horizontal=1000,
        )
        self.gebaeude = Gebaeude.objects.create(
            name='Test Gebäude',
            ort=self.ort,
            gebaeudeart='buero',
            laenge_ns=20,
            breite_ow=15,
            geschosse=3,
            geschosshoehe=2.8,
        )

    def test_gebaeude_properties(self):
        self.assertEqual(self.gebaeude.hoehe, 8.4)
        self.assertEqual(self.gebaeude.grundflaeche, 300)
        self.assertEqual(self.gebaeude.bgf, 900)
        self.assertEqual(self.gebaeude.nf, 765)
        self.assertEqual(self.gebaeude.volumen, 2520)

    def test_gebaeude_str(self):
        self.assertEqual(str(self.gebaeude), 'Test Gebäude')


class BerechnungenTest(TestCase):
    def setUp(self):
        self.ort = Ort.objects.create(
            name='Test Stadt',
            temperatur_mittel=9.0,
            heizgradtage=3500,
            solarstrahlung_nord=300,
            solarstrahlung_sued=1100,
            solarstrahlung_ost=700,
            solarstrahlung_west=700,
            solarstrahlung_horizontal=1000,
        )
        self.gebaeude = Gebaeude.objects.create(
            name='Test Gebäude',
            ort=self.ort,
            gebaeudeart='buero',
            laenge_ns=20,
            breite_ow=15,
            geschosse=3,
            geschosshoehe=2.8,
        )

    def test_heizwaermebedarf_berechnung(self):
        bauteile_dict = {
            'wand_nord': 0.3,
            'wand_sued': 0.3,
            'wand_ost': 0.3,
            'wand_west': 0.3,
            'dach': 0.2,
            'bodenplatte': 0.4,
        }
        klimadaten = {'heizgradtage': 3500}
        
        heizwaermebedarf = berechne_heizwaermebedarf(
            self.gebaeude, bauteile_dict, klimadaten
        )
        
        self.assertGreater(heizwaermebedarf, 0)
        self.assertIsInstance(heizwaermebedarf, (int, float))

    def test_energiebilanz_berechnung(self):
        bauteile_dict = {
            'wand_nord': 0.3,
            'wand_sued': 0.3,
            'wand_ost': 0.3,
            'wand_west': 0.3,
            'dach': 0.2,
            'bodenplatte': 0.4,
        }
        klimadaten = {
            'heizgradtage': 3500,
            'solarstrahlung_nord': 300,
            'solarstrahlung_sued': 1100,
            'solarstrahlung_ost': 700,
            'solarstrahlung_west': 700,
        }
        
        ergebnis = berechne_energiebilanz(
            self.gebaeude, bauteile_dict, None, None, [], [], klimadaten
        )
        
        self.assertIn('nutzenergie', ergebnis)
        self.assertIn('endenergie', ergebnis)
        self.assertIn('primaerenergie', ergebnis)
        self.assertIn('gebaeudedaten', ergebnis)
        
        self.assertGreater(ergebnis['nutzenergie']['ne_gesamt'], 0)
        self.assertGreater(ergebnis['endenergie']['ee_gesamt'], 0)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.ort = Ort.objects.create(
            name='Test Stadt',
            temperatur_mittel=9.0,
            heizgradtage=3500,
            solarstrahlung_nord=300,
            solarstrahlung_sued=1100,
            solarstrahlung_ost=700,
            solarstrahlung_west=700,
            solarstrahlung_horizontal=1000,
        )

    def test_startseite_view(self):
        response = self.client.get(reverse('startseite'))
        self.assertEqual(response.status_code, 200)

    def test_allg_angaben_view(self):
        response = self.client.get(reverse('allg_angaben'))
        self.assertEqual(response.status_code, 200)

    def test_api_berechnung(self):
        response = self.client.get(reverse('berechnung_api'), {
            'laenge_ns': '20',
            'breite_ow': '15',
            'geschosse': '3',
            'geschosshoehe': '2.8',
            'geb_klasse': 'buero',
        })
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('nutzenergie', data)
        self.assertIn('endenergie', data)
        self.assertIn('gebaeudedaten', data)


class APITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_berechnung_api_get(self):
        response = self.client.get('/api/berechnung/', {
            'laenge_ns': '20',
            'breite_ow': '15',
            'geschosse': '3',
        })
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('nutzenergie', data)
        self.assertIn('gebaeudedaten', data)

    def test_berechnung_api_post_not_allowed(self):
        response = self.client.post('/api/berechnung/')
        self.assertEqual(response.status_code, 405)