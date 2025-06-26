from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

from .models import (
    Gebaeude, Bauteil, PVAnlage, Lueftung, Beleuchtung, 
    Waermequelle, Sonnenschutz, Berechnung, Ort
)
from .forms import (
    GebaeudeAllgForm, BauteilForm, PVForm, LueftungForm,
    BeleuchtungForm, WaermequelleForm, SonnenschutzForm
)
from .berechnungen import berechne_energiebilanz


def startseite(request):
    """Startseite der Anwendung"""
    return render(request, 'startseite.html')


def uber_tool(request):
    """Über das Tool Seite"""
    return render(request, 'uber_tool.html')


def entwicklerteam(request):
    """Entwicklerteam Seite"""
    return render(request, 'entwicklerteam.html')


def kontakt(request):
    """Kontakt Seite"""
    return render(request, 'kontakt.html')


def hilfe(request):
    """Hilfe Seite"""
    return render(request, 'hilfe.html')


def allg_angaben(request):
    """Allgemeine Angaben - Schritt 1"""
    gebaeude_id = request.session.get('gebaeude_id')
    gebaeude = None
    
    if gebaeude_id:
        try:
            gebaeude = Gebaeude.objects.get(id=gebaeude_id)
        except Gebaeude.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = GebaeudeAllgForm(request.POST, instance=gebaeude)
        if form.is_valid():
            gebaeude = form.save()
            request.session['gebaeude_id'] = gebaeude.id
            messages.success(request, 'Allgemeine Angaben gespeichert.')
            return redirect('baukrper')
    else:
        form = GebaeudeAllgForm(instance=gebaeude)
    
    # Orte für Dropdown
    orte = Ort.objects.all().values_list('name', flat=True)
    
    context = {
        'form': form,
        'orte': orte,
        'gebaeude': gebaeude,
    }
    return render(request, 'allg_angaben.html', context)


def baukrper(request):
    """Baukörper - Schritt 2"""
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        messages.error(request, 'Bitte füllen Sie zuerst die allgemeinen Angaben aus.')
        return redirect('allg_angaben')
    
    gebaeude = get_object_or_404(Gebaeude, id=gebaeude_id)
    
    context = {
        'gebaeude': gebaeude,
    }
    return render(request, 'baukrper.html', context)


def baukoerper_kp(request):
    """Baukörper komplex"""
    return render(request, 'baukrper_kp.html')


def baukrper_kp_2(request):
    """Baukörper komplex 2"""
    return render(request, 'baukrper_kp_2.html')


def bauteil(request):
    """Bauteil - Schritt 3"""
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        messages.error(request, 'Bitte füllen Sie zuerst die allgemeinen Angaben aus.')
        return redirect('allg_angaben')
    
    gebaeude = get_object_or_404(Gebaeude, id=gebaeude_id)
    
    if request.method == 'POST':
        # Verarbeite U-Werte für alle Bauteile
        bauteil_typen = ['wand_nord', 'wand_sued', 'wand_west', 'wand_ost', 'dach', 'bodenplatte']
        
        for typ in bauteil_typen:
            u_wert_key = f'u_wert_{typ}'
            if u_wert_key in request.POST and request.POST[u_wert_key]:
                try:
                    u_wert = float(request.POST[u_wert_key])
                    bauteil, created = Bauteil.objects.get_or_create(
                        gebaeude=gebaeude,
                        typ=typ,
                        defaults={'u_wert': u_wert}
                    )
                    if not created:
                        bauteil.u_wert = u_wert
                        bauteil.save()
                except ValueError:
                    pass
        
        messages.success(request, 'Bauteil-Daten gespeichert.')
        return redirect('pv')
    
    # Bestehende Bauteile laden
    bauteile = {bt.typ: bt.u_wert for bt in gebaeude.bauteile.all()}
    
    context = {
        'gebaeude': gebaeude,
        'bauteile': bauteile,
    }
    return render(request, 'bauteil.html', context)


def bauteil_kp(request):
    """Bauteil komplex"""
    return render(request, 'bauteil_kp.html')


def pv(request):
    """PV-Anlage - Schritt 4"""
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        messages.error(request, 'Bitte füllen Sie zuerst die allgemeinen Angaben aus.')
        return redirect('allg_angaben')
    
    gebaeude = get_object_or_404(Gebaeude, id=gebaeude_id)
    pv_anlage, created = PVAnlage.objects.get_or_create(gebaeude=gebaeude)
    
    if request.method == 'POST':
        form = PVForm(request.POST, instance=pv_anlage)
        if form.is_valid():
            form.save()
            messages.success(request, 'PV-Daten gespeichert.')
            return redirect('lftung')
    else:
        form = PVForm(instance=pv_anlage)
    
    context = {
        'form': form,
        'gebaeude': gebaeude,
    }
    return render(request, 'pv.html', context)


def lftung(request):
    """Lüftung - Schritt 5"""
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        messages.error(request, 'Bitte füllen Sie zuerst die allgemeinen Angaben aus.')
        return redirect('allg_angaben')
    
    gebaeude = get_object_or_404(Gebaeude, id=gebaeude_id)
    lueftung, created = Lueftung.objects.get_or_create(gebaeude=gebaeude)
    
    if request.method == 'POST':
        form = LueftungForm(request.POST, instance=lueftung)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lüftungsdaten gespeichert.')
            return redirect('beleuchtung')
    else:
        form = LueftungForm(instance=lueftung)
    
    context = {
        'form': form,
        'gebaeude': gebaeude,
    }
    return render(request, 'lftung.html', context)


def beleuchtung(request):
    """Beleuchtung - Schritt 6"""
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        messages.error(request, 'Bitte füllen Sie zuerst die allgemeinen Angaben aus.')
        return redirect('allg_angaben')
    
    gebaeude = get_object_or_404(Gebaeude, id=gebaeude_id)
    
    context = {
        'gebaeude': gebaeude,
    }
    return render(request, 'beleuchtung.html', context)


def beleuchtung_2(request):
    """Beleuchtung 2 - Schritt 6b"""
    return render(request, 'beleuchtung_2.html')


def waermequellen(request):
    """Wärmequellen - Schritt 7"""
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        messages.error(request, 'Bitte füllen Sie zuerst die allgemeinen Angaben aus.')
        return redirect('allg_angaben')
    
    gebaeude = get_object_or_404(Gebaeude, id=gebaeude_id)
    
    context = {
        'gebaeude': gebaeude,
    }
    return render(request, 'wrmequellen.html', context)


def sdf(request):
    """Sonnenschutz - Schritt 8"""
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        messages.error(request, 'Bitte füllen Sie zuerst die allgemeinen Angaben aus.')
        return redirect('allg_angaben')
    
    gebaeude = get_object_or_404(Gebaeude, id=gebaeude_id)
    sonnenschutz, created = Sonnenschutz.objects.get_or_create(gebaeude=gebaeude)
    
    if request.method == 'POST':
        form = SonnenschutzForm(request.POST, instance=sonnenschutz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sonnenschutzdaten gespeichert.')
            return redirect('gwp')
    else:
        form = SonnenschutzForm(instance=sonnenschutz)
    
    context = {
        'form': form,
        'gebaeude': gebaeude,
    }
    return render(request, 'sdf.html', context)


def gwp(request):
    """GWP - Schritt 9"""
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        messages.error(request, 'Bitte füllen Sie zuerst die allgemeinen Angaben aus.')
        return redirect('allg_angaben')
    
    gebaeude = get_object_or_404(Gebaeude, id=gebaeude_id)
    
    context = {
        'gebaeude': gebaeude,
    }
    return render(request, 'gwp.html', context)


def ergebnis(request):
    """Ergebnis - Schritt 10"""
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        messages.error(request, 'Bitte füllen Sie zuerst die allgemeinen Angaben aus.')
        return redirect('allg_angaben')
    
    gebaeude = get_object_or_404(Gebaeude, id=gebaeude_id)
    
    # Berechnung durchführen
    try:
        berechnung = gebaeude.berechnung
    except Berechnung.DoesNotExist:
        berechnung = Berechnung.objects.create(gebaeude=gebaeude)
    
    context = {
        'gebaeude': gebaeude,
        'berechnung': berechnung,
    }
    return render(request, 'ergebnis.html', context)


def einfach_ergebnis(request):
    """Einfaches Ergebnis für Demo"""
    # Demo-Daten
    demo_daten = {
        'laenge_ns': 20,
        'breite_ow': 15,
        'geschosse': 3,
        'geschosshoehe': 2.8,
        'hoehe': 8.4,
        'volumen': 2520,
        'bgf': 900,
        'nf': 765,
    }
    
    # Demo-Berechnungen
    ne_absolut = 45000
    ne_spezifisch = 58.8
    
    context = {
        'daten': demo_daten,
        'ne_absolut': ne_absolut,
        'ne_spezifisch': ne_spezifisch,
    }
    return render(request, 'einfach_ergebnis.html', context)


def ergebnis_pdf(request):
    """PDF-Export des Ergebnisses"""
    # Hier würde normalerweise ein PDF generiert
    # Für jetzt einfach eine Textantwort
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="energiebilanz.txt"'
    response.write('Energiebilanz-Ergebnis\n\nHier würde das PDF stehen.')
    return response