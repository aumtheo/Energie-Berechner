from django import forms
from .models import (
    Gebaeude, Bauteil, PVAnlage, Lueftung, Beleuchtung, 
    Waermequelle, Sonnenschutz, Ort
)


class GebaeudeAllgForm(forms.ModelForm):
    class Meta:
        model = Gebaeude
        fields = [
            'name', 'beschreibung', 'ort', 'gebaeudeart', 'geschosshoehe',
            'laenge_ns', 'breite_ow', 'geschosse', 'personendichte',
            'fensterflaeche_nord', 'fensterflaeche_sued', 
            'fensterflaeche_ost', 'fensterflaeche_west',
            'g_wert_nord', 'g_wert_sued', 'g_wert_ost', 'g_wert_west'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'beschreibung': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ort': forms.Select(attrs={'class': 'form-control'}),
            'gebaeudeart': forms.Select(attrs={'class': 'form-control'}),
            'geschosshoehe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'laenge_ns': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'breite_ow': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'geschosse': forms.NumberInput(attrs={'class': 'form-control'}),
            'personendichte': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'fensterflaeche_nord': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'fensterflaeche_sued': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'fensterflaeche_ost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'fensterflaeche_west': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'g_wert_nord': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
            'g_wert_sued': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
            'g_wert_ost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
            'g_wert_west': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
        }


class BauteilForm(forms.ModelForm):
    class Meta:
        model = Bauteil
        fields = ['typ', 'u_wert']
        widgets = {
            'typ': forms.Select(attrs={'class': 'form-control'}),
            'u_wert': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
        }


class PVForm(forms.ModelForm):
    class Meta:
        model = PVAnlage
        fields = [
            'pv_vor_fenster_nord', 'pv_vor_fenster_sued', 
            'pv_vor_fenster_ost', 'pv_vor_fenster_west',
            'pv_vor_opak_nord', 'pv_vor_opak_sued',
            'pv_vor_opak_ost', 'pv_vor_opak_west',
            'wirkungsgrad'
        ]
        widgets = {
            'pv_vor_fenster_nord': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pv_vor_fenster_sued': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pv_vor_fenster_ost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pv_vor_fenster_west': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pv_vor_opak_nord': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pv_vor_opak_sued': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pv_vor_opak_ost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'pv_vor_opak_west': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'wirkungsgrad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
        }


class LueftungForm(forms.ModelForm):
    class Meta:
        model = Lueftung
        fields = [
            'typ', 'luftwechselrate', 'wirkungsgrad_wrg', 
            'raum_soll_temperatur', 'laufzeit_h_d', 'laufzeit_d_a'
        ]
        widgets = {
            'typ': forms.Select(attrs={'class': 'form-control'}),
            'luftwechselrate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'wirkungsgrad_wrg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
            'raum_soll_temperatur': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'laufzeit_h_d': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'laufzeit_d_a': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
        }


class BeleuchtungForm(forms.ModelForm):
    class Meta:
        model = Beleuchtung
        fields = [
            'nutzungsbereich', 'beleuchtungsart', 'regelungsart',
            'e_soll', 'laufzeit_h_d', 'laufzeit_d_a'
        ]
        widgets = {
            'nutzungsbereich': forms.Select(attrs={'class': 'form-control'}),
            'beleuchtungsart': forms.Select(attrs={'class': 'form-control'}),
            'regelungsart': forms.Select(attrs={'class': 'form-control'}),
            'e_soll': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'laufzeit_h_d': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'laufzeit_d_a': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
        }


class WaermequelleForm(forms.ModelForm):
    class Meta:
        model = Waermequelle
        fields = ['typ', 'name', 'anzahl', 'leistung', 'betrieb_h_d', 'betrieb_d_a']
        widgets = {
            'typ': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'anzahl': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'leistung': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'betrieb_h_d': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'betrieb_d_a': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
        }


class SonnenschutzForm(forms.ModelForm):
    class Meta:
        model = Sonnenschutz
        fields = [
            'kritischer_raum', 'fassadenorientierung', 'sonnenschutzart',
            'verglasungsart', 'passive_kuehlung', 'fensterneigung'
        ]
        widgets = {
            'kritischer_raum': forms.TextInput(attrs={'class': 'form-control'}),
            'fassadenorientierung': forms.Select(attrs={'class': 'form-control'}),
            'sonnenschutzart': forms.Select(attrs={'class': 'form-control'}),
            'verglasungsart': forms.Select(attrs={'class': 'form-control'}),
            'passive_kuehlung': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fensterneigung': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'max': '90'}),
        }