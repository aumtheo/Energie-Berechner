"""
Berechnungsmodul für Energiebilanz
"""
import math


def berechne_heizwaermebedarf(gebaeude, bauteile_dict, klimadaten):
    """
    Berechnet den Heizwärmebedarf nach vereinfachtem Verfahren
    """
    # Transmissionswärmeverluste
    q_t = 0
    
    # Wände
    for orientierung in ['nord', 'sued', 'ost', 'west']:
        bauteil_key = f'wand_{orientierung}'
        if bauteil_key in bauteile_dict:
            u_wert = bauteile_dict[bauteil_key]
            if orientierung == 'nord' or orientierung == 'sued':
                flaeche = gebaeude.laenge_ns * gebaeude.hoehe
                fensterflaeche = getattr(gebaeude, f'fensterflaeche_{orientierung}', 0)
            else:  # ost/west
                flaeche = gebaeude.breite_ow * gebaeude.hoehe
                fensterflaeche = getattr(gebaeude, f'fensterflaeche_{orientierung}', 0)
            
            # Opake Fläche = Gesamtfläche - Fensterfläche
            opake_flaeche = max(0, flaeche - fensterflaeche)
            q_t += u_wert * opake_flaeche
    
    # Dach
    if 'dach' in bauteile_dict:
        u_dach = bauteile_dict['dach']
        dach_flaeche = gebaeude.grundflaeche
        q_t += u_dach * dach_flaeche
    
    # Bodenplatte
    if 'bodenplatte' in bauteile_dict:
        u_boden = bauteile_dict['bodenplatte']
        boden_flaeche = gebaeude.grundflaeche
        q_t += u_boden * boden_flaeche * 0.5  # Reduktionsfaktor für Erdreich
    
    # Fenster (U-Wert 1.3 W/m²K angenommen)
    u_fenster = 1.3
    for orientierung in ['nord', 'sued', 'ost', 'west']:
        fensterflaeche = getattr(gebaeude, f'fensterflaeche_{orientierung}', 0)
        q_t += u_fenster * fensterflaeche
    
    # Lüftungswärmeverluste (vereinfacht)
    luftwechsel = 0.5  # 1/h
    rho_luft = 1.2  # kg/m³
    c_luft = 1000  # J/kgK
    q_v = luftwechsel * gebaeude.volumen * rho_luft * c_luft / 3600  # W/K
    
    # Gesamtwärmeverlust
    q_gesamt = q_t + q_v
    
    # Heizgradtage
    heizgradtage = klimadaten.get('heizgradtage', 3500)
    
    # Heizwärmebedarf
    heizwaermebedarf = q_gesamt * heizgradtage * 24 / 1000  # kWh/a
    
    return max(0, heizwaermebedarf)


def berechne_solargewinne(gebaeude, klimadaten):
    """
    Berechnet solare Gewinne durch Fenster
    """
    solargewinne = 0
    
    for orientierung in ['nord', 'sued', 'ost', 'west']:
        fensterflaeche = getattr(gebaeude, f'fensterflaeche_{orientierung}', 0)
        g_wert = getattr(gebaeude, f'g_wert_{orientierung}', 0.6)
        strahlung = klimadaten.get(f'solarstrahlung_{orientierung}', 0)
        
        solargewinne += fensterflaeche * g_wert * strahlung * 0.7  # Reduktionsfaktor
    
    return solargewinne


def berechne_interne_gewinne(gebaeude, waermequellen):
    """
    Berechnet interne Wärmequellen
    """
    interne_gewinne = 0
    
    # Personen (80W pro Person, 8h/d, 250d/a)
    anzahl_personen = gebaeude.nf / gebaeude.personendichte
    personen_gewinne = anzahl_personen * 80 * 8 * 250 / 1000  # kWh/a
    interne_gewinne += personen_gewinne
    
    # Geräte und sonstige Quellen
    for quelle in waermequellen:
        jahresenergie = (quelle.anzahl * quelle.leistung * 
                        quelle.betrieb_h_d * quelle.betrieb_d_a / 1000)  # kWh/a
        interne_gewinne += jahresenergie
    
    return interne_gewinne


def berechne_trinkwarmwasser(gebaeude):
    """
    Berechnet Trinkwarmwasserbedarf basierend auf Gebäudeart
    """
    # Spezifische Werte je Gebäudeart (kWh/m²a)
    tww_spezifisch = {
        'buero': 15,
        'schule': 5,
        'heim': 25,
    }
    
    spez_bedarf = tww_spezifisch.get(gebaeude.gebaeudeart, 15)
    return gebaeude.nf * spez_bedarf


def berechne_lueftungsenergie(gebaeude, lueftung_data):
    """
    Berechnet Lüftungsenergiebedarf
    """
    if not lueftung_data:
        return 0
    
    # Vereinfachte Berechnung
    spez_bedarf = {
        'buero': 8,
        'schule': 6,
        'heim': 5,
    }
    
    lwt_spezifisch = spez_bedarf.get(gebaeude.gebaeudeart, 8)
    return gebaeude.nf * lwt_spezifisch


def berechne_beleuchtungsenergie(gebaeude, beleuchtungen):
    """
    Berechnet Beleuchtungsenergiebedarf
    """
    if not beleuchtungen:
        # Fallback basierend auf Gebäudeart
        spez_bedarf = {
            'buero': 10,
            'schule': 12,
            'heim': 8,
        }
        bel_spezifisch = spez_bedarf.get(gebaeude.gebaeudeart, 10)
        return gebaeude.nf * bel_spezifisch
    
    # Detaillierte Berechnung basierend auf Eingaben
    gesamt_energie = 0
    for beleuchtung in beleuchtungen:
        # Vereinfachte Berechnung: 10W/m² * Laufzeit
        leistung_pro_m2 = 10  # W/m²
        anteil_nutzungsbereich = 0.25  # 25% der Fläche pro Bereich
        flaeche = gebaeude.nf * anteil_nutzungsbereich
        
        jahresenergie = (leistung_pro_m2 * flaeche * 
                        beleuchtung.laufzeit_h_d * beleuchtung.laufzeit_d_a / 1000)
        gesamt_energie += jahresenergie
    
    return gesamt_energie


def berechne_prozessenergie(gebaeude):
    """
    Berechnet Prozessenergiebedarf
    """
    spez_bedarf = {
        'buero': 5,
        'schule': 2,
        'heim': 3,
    }
    
    nutzer_spezifisch = spez_bedarf.get(gebaeude.gebaeudeart, 5)
    return gebaeude.nf * nutzer_spezifisch


def berechne_pv_ertrag(gebaeude, pv_anlage, klimadaten):
    """
    Berechnet PV-Ertrag
    """
    if not pv_anlage:
        return 0
    
    pv_ertrag = 0
    
    for orientierung in ['nord', 'sued', 'ost', 'west']:
        # PV vor Fenstern
        pv_fenster = getattr(pv_anlage, f'pv_vor_fenster_{orientierung}', 0)
        # PV vor opaken Flächen
        pv_opak = getattr(pv_anlage, f'pv_vor_opak_{orientierung}', 0)
        
        pv_gesamt = pv_fenster + pv_opak
        strahlung = klimadaten.get(f'solarstrahlung_{orientierung}', 0)
        
        pv_ertrag += pv_gesamt * strahlung * pv_anlage.wirkungsgrad
    
    return pv_ertrag


def berechne_energiebilanz(gebaeude_data, bauteile_data, pv_data, lueftung_data, 
                          beleuchtungen_data, waermequellen_data, klimadaten):
    """
    Hauptfunktion für die Energiebilanzberechnung
    """
    # Nutzenergiebedarf
    ne_heizung = berechne_heizwaermebedarf(gebaeude_data, bauteile_data, klimadaten)
    ne_tww = berechne_trinkwarmwasser(gebaeude_data)
    
    # Solare und interne Gewinne
    solargewinne = berechne_solargewinne(gebaeude_data, klimadaten)
    interne_gewinne = berechne_interne_gewinne(gebaeude_data, waermequellen_data)
    
    # Heizwärmebedarf reduzieren um Gewinne
    ne_heizung = max(0, ne_heizung - (solargewinne + interne_gewinne) * 0.7)
    
    ne_gesamt = ne_heizung + ne_tww
    
    # Endenergiebedarf (vereinfacht mit Anlagenwirkungsgrad 0.9)
    ee_heizung = ne_heizung / 0.9
    ee_tww = ne_tww / 0.9
    ee_lueftung = berechne_lueftungsenergie(gebaeude_data, lueftung_data)
    ee_beleuchtung = berechne_beleuchtungsenergie(gebaeude_data, beleuchtungen_data)
    ee_prozesse = berechne_prozessenergie(gebaeude_data)
    
    ee_gesamt = ee_heizung + ee_tww + ee_lueftung + ee_beleuchtung + ee_prozesse
    
    # Primärenergiebedarf (Faktor 1.8 für Strom, 1.1 für Gas)
    pe_gesamt = (ee_heizung + ee_tww) * 1.1 + (ee_lueftung + ee_beleuchtung + ee_prozesse) * 1.8
    
    # PV-Ertrag
    pv_ertrag = berechne_pv_ertrag(gebaeude_data, pv_data, klimadaten)
    strom_ueberschuss = max(0, pv_ertrag - (ee_lueftung + ee_beleuchtung + ee_prozesse))
    
    # GWP (vereinfacht)
    gwp_var1 = ee_gesamt * 0.5  # kg CO2-eq/a
    gwp_var2 = ee_gesamt * 0.3  # kg CO2-eq/a
    
    return {
        'nutzenergie': {
            'ne_heizung': round(ne_heizung, 1),
            'ne_tww': round(ne_tww, 1),
            'ne_gesamt': round(ne_gesamt, 1),
            'ne_spezifisch': round(ne_gesamt / gebaeude_data.nf, 1) if gebaeude_data.nf > 0 else 0,
        },
        'endenergie': {
            'ee_heizung': round(ee_heizung, 1),
            'ee_tww': round(ee_tww, 1),
            'ee_lueftung': round(ee_lueftung, 1),
            'ee_beleuchtung': round(ee_beleuchtung, 1),
            'ee_prozesse': round(ee_prozesse, 1),
            'ee_gesamt': round(ee_gesamt, 1),
            'ee_spezifisch': round(ee_gesamt / gebaeude_data.nf, 1) if gebaeude_data.nf > 0 else 0,
        },
        'primaerenergie': {
            'pe_gesamt': round(pe_gesamt, 1),
            'pe_spezifisch': round(pe_gesamt / gebaeude_data.nf, 1) if gebaeude_data.nf > 0 else 0,
        },
        'pv': {
            'pv_ertrag': round(pv_ertrag, 1),
            'strom_ueberschuss': round(strom_ueberschuss, 1),
        },
        'gwp': {
            'gwp_var1': round(gwp_var1, 1),
            'gwp_var2': round(gwp_var2, 1),
        },
        'gebaeudedaten': {
            'hoehe': round(gebaeude_data.hoehe, 1),
            'grundflaeche': round(gebaeude_data.grundflaeche, 1),
            'bgf': round(gebaeude_data.bgf, 1),
            'nf': round(gebaeude_data.nf, 1),
            'volumen': round(gebaeude_data.volumen, 1),
        }
    }