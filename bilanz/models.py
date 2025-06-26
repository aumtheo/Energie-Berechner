from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Ort(models.Model):
    """Klimadaten für verschiedene Orte"""
    name = models.CharField(max_length=100, unique=True)
    temperatur_mittel = models.FloatField(help_text="Mittlere Jahrestemperatur in °C")
    heizgradtage = models.FloatField(help_text="Heizgradtage Kh in Kd")
    solarstrahlung_nord = models.FloatField(help_text="kWh/m²a")
    solarstrahlung_sued = models.FloatField(help_text="kWh/m²a")
    solarstrahlung_ost = models.FloatField(help_text="kWh/m²a")
    solarstrahlung_west = models.FloatField(help_text="kWh/m²a")
    solarstrahlung_horizontal = models.FloatField(help_text="kWh/m²a")
    
    class Meta:
        verbose_name = "Ort"
        verbose_name_plural = "Orte"
    
    def __str__(self):
        return self.name


class Gebaeude(models.Model):
    """Hauptmodell für ein Gebäude"""
    GEBAEUDE_ARTEN = [
        ('buero', 'Bürogebäude'),
        ('schule', 'Schule (ohne Dusche)'),
        ('heim', 'Heim'),
    ]
    
    name = models.CharField(max_length=200, blank=True)
    beschreibung = models.TextField(blank=True)
    ort = models.ForeignKey(Ort, on_delete=models.CASCADE)
    gebaeudeart = models.CharField(max_length=20, choices=GEBAEUDE_ARTEN, default='buero')
    
    # Geometrie
    laenge_ns = models.FloatField(verbose_name="Länge Nord/Süd (m)", validators=[MinValueValidator(0.1)])
    breite_ow = models.FloatField(verbose_name="Breite Ost/West (m)", validators=[MinValueValidator(0.1)])
    geschosse = models.IntegerField(validators=[MinValueValidator(1)])
    geschosshoehe = models.FloatField(verbose_name="Geschosshöhe (m)", default=2.8, validators=[MinValueValidator(2.0)])
    
    # Fensterflächen
    fensterflaeche_nord = models.FloatField(default=0, validators=[MinValueValidator(0)])
    fensterflaeche_sued = models.FloatField(default=0, validators=[MinValueValidator(0)])
    fensterflaeche_ost = models.FloatField(default=0, validators=[MinValueValidator(0)])
    fensterflaeche_west = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    # g-Werte
    g_wert_nord = models.FloatField(default=0.6, validators=[MinValueValidator(0), MaxValueValidator(1)])
    g_wert_sued = models.FloatField(default=0.6, validators=[MinValueValidator(0), MaxValueValidator(1)])
    g_wert_ost = models.FloatField(default=0.6, validators=[MinValueValidator(0), MaxValueValidator(1)])
    g_wert_west = models.FloatField(default=0.6, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Personendichte
    personendichte = models.FloatField(verbose_name="Personendichte (m²/Person)", default=15)
    
    # Timestamps
    erstellt_am = models.DateTimeField(auto_now_add=True)
    aktualisiert_am = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Gebäude"
        verbose_name_plural = "Gebäude"
    
    def __str__(self):
        return self.name or f"Gebäude {self.id}"
    
    @property
    def hoehe(self):
        """Gesamthöhe des Gebäudes"""
        return self.geschosse * self.geschosshoehe
    
    @property
    def grundflaeche(self):
        """Grundfläche in m²"""
        return self.laenge_ns * self.breite_ow
    
    @property
    def bgf(self):
        """Bruttogrundfläche in m²"""
        return self.grundflaeche * self.geschosse
    
    @property
    def nf(self):
        """Nutzfläche in m² (85% der BGF)"""
        return self.bgf * 0.85
    
    @property
    def volumen(self):
        """Volumen in m³"""
        return self.bgf * self.geschosshoehe


class Bauteil(models.Model):
    """U-Werte für verschiedene Bauteile"""
    BAUTEIL_TYPEN = [
        ('wand_nord', 'Wand Nord'),
        ('wand_sued', 'Wand Süd'),
        ('wand_ost', 'Wand Ost'),
        ('wand_west', 'Wand West'),
        ('dach', 'Dach'),
        ('bodenplatte', 'Bodenplatte'),
    ]
    
    gebaeude = models.ForeignKey(Gebaeude, on_delete=models.CASCADE, related_name='bauteile')
    typ = models.CharField(max_length=20, choices=BAUTEIL_TYPEN)
    u_wert = models.FloatField(verbose_name="U-Wert (W/m²K)", validators=[MinValueValidator(0.01)])
    
    class Meta:
        verbose_name = "Bauteil"
        verbose_name_plural = "Bauteile"
        unique_together = ['gebaeude', 'typ']
    
    def __str__(self):
        return f"{self.get_typ_display()} - U={self.u_wert} W/m²K"


class PVAnlage(models.Model):
    """Photovoltaik-Anlage"""
    gebaeude = models.OneToOneField(Gebaeude, on_delete=models.CASCADE, related_name='pv_anlage')
    
    # PV-Flächen vor Fenstern
    pv_vor_fenster_nord = models.FloatField(default=0, validators=[MinValueValidator(0)])
    pv_vor_fenster_sued = models.FloatField(default=0, validators=[MinValueValidator(0)])
    pv_vor_fenster_ost = models.FloatField(default=0, validators=[MinValueValidator(0)])
    pv_vor_fenster_west = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    # PV-Flächen vor opaken Flächen
    pv_vor_opak_nord = models.FloatField(default=0, validators=[MinValueValidator(0)])
    pv_vor_opak_sued = models.FloatField(default=0, validators=[MinValueValidator(0)])
    pv_vor_opak_ost = models.FloatField(default=0, validators=[MinValueValidator(0)])
    pv_vor_opak_west = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    # Wirkungsgrad
    wirkungsgrad = models.FloatField(default=0.2, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    class Meta:
        verbose_name = "PV-Anlage"
        verbose_name_plural = "PV-Anlagen"
    
    def __str__(self):
        return f"PV-Anlage {self.gebaeude}"


class Lueftung(models.Model):
    """Lüftungsanlage"""
    LUEFTUNGSTYPEN = [
        ('natuerlich', 'Natürliche Lüftung'),
        ('mechanisch', 'Mechanische Lüftung'),
        ('mechanisch_wrg', 'Mechanische Lüftung mit WRG'),
    ]
    
    gebaeude = models.OneToOneField(Gebaeude, on_delete=models.CASCADE, related_name='lueftung')
    typ = models.CharField(max_length=20, choices=LUEFTUNGSTYPEN, default='natuerlich')
    luftwechselrate = models.FloatField(default=0.5, validators=[MinValueValidator(0)])
    wirkungsgrad_wrg = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    raum_soll_temperatur = models.FloatField(default=20, validators=[MinValueValidator(15), MaxValueValidator(25)])
    laufzeit_h_d = models.FloatField(default=8, validators=[MinValueValidator(0), MaxValueValidator(24)])
    laufzeit_d_a = models.FloatField(default=250, validators=[MinValueValidator(0), MaxValueValidator(365)])
    
    class Meta:
        verbose_name = "Lüftung"
        verbose_name_plural = "Lüftungsanlagen"
    
    def __str__(self):
        return f"Lüftung {self.gebaeude} - {self.get_typ_display()}"


class Beleuchtung(models.Model):
    """Beleuchtungsanlage"""
    NUTZUNGSBEREICHE = [
        ('buero', 'Büro'),
        ('wohnen', 'Wohnen'),
        ('sanitaer', 'Sanitär'),
        ('verkehr', 'Verkehr'),
    ]
    
    BELEUCHTUNGSARTEN = [
        ('led', 'LED'),
        ('leuchtstoff', 'Leuchtstofflampe'),
        ('halogen', 'Halogen'),
    ]
    
    REGELUNGSARTEN = [
        ('manuell', 'Manuell'),
        ('praesenz', 'Präsenzmelder'),
        ('tageslicht', 'Tageslichtregelung'),
        ('praesenz_tageslicht', 'Präsenz + Tageslicht'),
    ]
    
    gebaeude = models.ForeignKey(Gebaeude, on_delete=models.CASCADE, related_name='beleuchtungen')
    nutzungsbereich = models.CharField(max_length=20, choices=NUTZUNGSBEREICHE)
    beleuchtungsart = models.CharField(max_length=20, choices=BELEUCHTUNGSARTEN, default='led')
    regelungsart = models.CharField(max_length=30, choices=REGELUNGSARTEN, default='manuell')
    e_soll = models.FloatField(verbose_name="E_Soll (lx)", default=500)
    laufzeit_h_d = models.FloatField(default=8, validators=[MinValueValidator(0), MaxValueValidator(24)])
    laufzeit_d_a = models.FloatField(default=250, validators=[MinValueValidator(0), MaxValueValidator(365)])
    
    class Meta:
        verbose_name = "Beleuchtung"
        verbose_name_plural = "Beleuchtungsanlagen"
        unique_together = ['gebaeude', 'nutzungsbereich']
    
    def __str__(self):
        return f"Beleuchtung {self.gebaeude} - {self.get_nutzungsbereich_display()}"


class Waermequelle(models.Model):
    """Interne Wärmequellen"""
    QUELLEN_TYPEN = [
        ('geraet', 'Gerät'),
        ('sonstige', 'Sonstige Quelle'),
    ]
    
    gebaeude = models.ForeignKey(Gebaeude, on_delete=models.CASCADE, related_name='waermequellen')
    typ = models.CharField(max_length=20, choices=QUELLEN_TYPEN)
    name = models.CharField(max_length=100)
    anzahl = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    leistung = models.FloatField(verbose_name="Leistung (W)", validators=[MinValueValidator(0)])
    betrieb_h_d = models.FloatField(default=8, validators=[MinValueValidator(0), MaxValueValidator(24)])
    betrieb_d_a = models.FloatField(default=250, validators=[MinValueValidator(0), MaxValueValidator(365)])
    
    class Meta:
        verbose_name = "Wärmequelle"
        verbose_name_plural = "Wärmequellen"
    
    def __str__(self):
        return f"{self.name} ({self.anzahl}x {self.leistung}W)"


class Sonnenschutz(models.Model):
    """Sonnenschutz für kritische Räume"""
    ORIENTIERUNGEN = [
        ('nord', 'Nord'),
        ('sued', 'Süd'),
        ('ost', 'Ost'),
        ('west', 'West'),
    ]
    
    SONNENSCHUTZARTEN = [
        ('außen_fest', 'Außen fest'),
        ('außen_beweglich', 'Außen beweglich'),
        ('innen', 'Innen'),
        ('zwischen_scheiben', 'Zwischen Scheiben'),
    ]
    
    VERGLASUNGSARTEN = [
        ('zweifach', 'Zweifach'),
        ('dreifach', 'Dreifach'),
        ('zweifach_sonnenschutz', 'Zweifach Sonnenschutzglas'),
    ]
    
    gebaeude = models.OneToOneField(Gebaeude, on_delete=models.CASCADE, related_name='sonnenschutz')
    kritischer_raum = models.CharField(max_length=100, blank=True)
    fassadenorientierung = models.CharField(max_length=10, choices=ORIENTIERUNGEN, default='sued')
    sonnenschutzart = models.CharField(max_length=30, choices=SONNENSCHUTZARTEN, default='außen_beweglich')
    verglasungsart = models.CharField(max_length=30, choices=VERGLASUNGSARTEN, default='zweifach')
    passive_kuehlung = models.BooleanField(default=False)
    fensterneigung = models.FloatField(default=90, validators=[MinValueValidator(0), MaxValueValidator(90)])
    
    class Meta:
        verbose_name = "Sonnenschutz"
        verbose_name_plural = "Sonnenschutzanlagen"
    
    def __str__(self):
        return f"Sonnenschutz {self.gebaeude}"


class Berechnung(models.Model):
    """Gespeicherte Berechnungsergebnisse"""
    gebaeude = models.OneToOneField(Gebaeude, on_delete=models.CASCADE, related_name='berechnung')
    
    # Nutzenergiebedarf
    ne_heizung = models.FloatField(default=0, verbose_name="Nutzenergie Heizung (kWh/a)")
    ne_kuehlung = models.FloatField(default=0, verbose_name="Nutzenergie Kühlung (kWh/a)")
    ne_trinkwarmwasser = models.FloatField(default=0, verbose_name="Nutzenergie TWW (kWh/a)")
    ne_gesamt = models.FloatField(default=0, verbose_name="Nutzenergie gesamt (kWh/a)")
    
    # Endenergiebedarf
    ee_heizung = models.FloatField(default=0, verbose_name="Endenergie Heizung (kWh/a)")
    ee_kuehlung = models.FloatField(default=0, verbose_name="Endenergie Kühlung (kWh/a)")
    ee_lueftung = models.FloatField(default=0, verbose_name="Endenergie Lüftung (kWh/a)")
    ee_beleuchtung = models.FloatField(default=0, verbose_name="Endenergie Beleuchtung (kWh/a)")
    ee_prozesse = models.FloatField(default=0, verbose_name="Endenergie Prozesse (kWh/a)")
    ee_gesamt = models.FloatField(default=0, verbose_name="Endenergie gesamt (kWh/a)")
    
    # Primärenergiebedarf
    pe_gesamt = models.FloatField(default=0, verbose_name="Primärenergie gesamt (kWh/a)")
    
    # PV-Ertrag
    pv_ertrag = models.FloatField(default=0, verbose_name="PV-Ertrag (kWh/a)")
    strom_ueberschuss = models.FloatField(default=0, verbose_name="Stromüberschuss (kWh/a)")
    
    # GWP
    gwp_var1 = models.FloatField(default=0, verbose_name="GWP Variante 1 (kg CO2-eq/a)")
    gwp_var2 = models.FloatField(default=0, verbose_name="GWP Variante 2 (kg CO2-eq/a)")
    
    # Timestamps
    berechnet_am = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Berechnung"
        verbose_name_plural = "Berechnungen"
    
    def __str__(self):
        return f"Berechnung {self.gebaeude}"
    
    @property
    def ne_spezifisch(self):
        """Spezifischer Nutzenergiebedarf in kWh/m²a"""
        if self.gebaeude.nf > 0:
            return self.ne_gesamt / self.gebaeude.nf
        return 0
    
    @property
    def ee_spezifisch(self):
        """Spezifischer Endenergiebedarf in kWh/m²a"""
        if self.gebaeude.nf > 0:
            return self.ee_gesamt / self.gebaeude.nf
        return 0
    
    @property
    def pe_spezifisch(self):
        """Spezifischer Primärenergiebedarf in kWh/m²a"""
        if self.gebaeude.nf > 0:
            return self.pe_gesamt / self.gebaeude.nf
        return 0