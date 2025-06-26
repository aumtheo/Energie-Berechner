from django.contrib import admin
from .models import (
    Ort, Gebaeude, Bauteil, PVAnlage, Lueftung, Beleuchtung, 
    Waermequelle, Sonnenschutz, Berechnung
)


@admin.register(Ort)
class OrtAdmin(admin.ModelAdmin):
    list_display = ['name', 'temperatur_mittel', 'heizgradtage']
    search_fields = ['name']


class BauteilInline(admin.TabularInline):
    model = Bauteil
    extra = 0


class BeleuchtungInline(admin.TabularInline):
    model = Beleuchtung
    extra = 0


class WaermequelleInline(admin.TabularInline):
    model = Waermequelle
    extra = 0


@admin.register(Gebaeude)
class GebaeudeAdmin(admin.ModelAdmin):
    list_display = ['name', 'gebaeudeart', 'ort', 'bgf', 'geschosse', 'erstellt_am']
    list_filter = ['gebaeudeart', 'ort', 'erstellt_am']
    search_fields = ['name', 'beschreibung']
    inlines = [BauteilInline, BeleuchtungInline, WaermequelleInline]
    
    fieldsets = (
        ('Allgemeine Angaben', {
            'fields': ('name', 'beschreibung', 'ort', 'gebaeudeart')
        }),
        ('Geometrie', {
            'fields': ('laenge_ns', 'breite_ow', 'geschosse', 'geschosshoehe', 'personendichte')
        }),
        ('Fensterflächen', {
            'fields': (
                ('fensterflaeche_nord', 'fensterflaeche_sued'),
                ('fensterflaeche_ost', 'fensterflaeche_west')
            )
        }),
        ('g-Werte', {
            'fields': (
                ('g_wert_nord', 'g_wert_sued'),
                ('g_wert_ost', 'g_wert_west')
            )
        }),
    )


@admin.register(Bauteil)
class BauteilAdmin(admin.ModelAdmin):
    list_display = ['gebaeude', 'typ', 'u_wert']
    list_filter = ['typ']
    search_fields = ['gebaeude__name']


@admin.register(PVAnlage)
class PVAnlageAdmin(admin.ModelAdmin):
    list_display = ['gebaeude', 'wirkungsgrad']
    search_fields = ['gebaeude__name']


@admin.register(Lueftung)
class LueftungAdmin(admin.ModelAdmin):
    list_display = ['gebaeude', 'typ', 'luftwechselrate', 'wirkungsgrad_wrg']
    list_filter = ['typ']
    search_fields = ['gebaeude__name']


@admin.register(Beleuchtung)
class BeleuchtungAdmin(admin.ModelAdmin):
    list_display = ['gebaeude', 'nutzungsbereich', 'beleuchtungsart', 'regelungsart']
    list_filter = ['nutzungsbereich', 'beleuchtungsart', 'regelungsart']
    search_fields = ['gebaeude__name']


@admin.register(Waermequelle)
class WaermequelleAdmin(admin.ModelAdmin):
    list_display = ['gebaeude', 'typ', 'name', 'anzahl', 'leistung']
    list_filter = ['typ']
    search_fields = ['gebaeude__name', 'name']


@admin.register(Sonnenschutz)
class SonnenschutzAdmin(admin.ModelAdmin):
    list_display = ['gebaeude', 'fassadenorientierung', 'sonnenschutzart', 'verglasungsart']
    list_filter = ['fassadenorientierung', 'sonnenschutzart', 'verglasungsart']
    search_fields = ['gebaeude__name']


@admin.register(Berechnung)
class BerechnungAdmin(admin.ModelAdmin):
    list_display = ['gebaeude', 'ne_gesamt', 'ee_gesamt', 'pe_gesamt', 'berechnet_am']
    search_fields = ['gebaeude__name']
    readonly_fields = ['berechnet_am']