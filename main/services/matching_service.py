from django.core.exceptions import ValidationError
from main.models import Matching, Bewerber, UnternehmenAusbildungsplatz
from services.ausbildungsplatz_service import blockiere_platz, vergebe_platz, gebe_platz_frei
from services.einsatz_service import erzeuge_einsatz, setze_daten_einsatz


# grundsätzliche Status-Funktionen 

def setze_status_berechnet(matching: Matching):
    matching.status = "berechnet"
    matching.save()
    return matching

def setze_status_vorgeschlagen(matching: Matching):
    platz = matching.unternehmen_ausbildungsplatz
    bestehende = Matching.objects.filter(unternehmen_ausbildungsplatz=platz).exclude(id=matching.id)
    for m in bestehende:
        if m.status in ["vorgeschlagen", "angenommen"]:
            raise ValidationError("Platz ist bereits reserviert.")
    blockiere_platz(platz)
    matching.status = "vorgeschlagen"
    matching.save()
    return matching

def setze_status_abgelehnt(matching: Matching):
    platz = matching.unternehmen_ausbildungsplatz
    gebe_platz_frei(platz)
    matching.status = "abgelehnt"
    matching.save()
    return matching

def setze_status_angenommen(matching: Matching):
    platz = matching.unternehmen_ausbildungsplatz
    vergebe_platz(platz)
    matching.status = "angenommen"
    matching.save()
    erzeuge_einsatz(matching)
    return matching


# Automatische Matching-Erzeugung für Bewerber

def create_matchings_for_bewerber(bewerber: Bewerber):
    wunschberufe = [
        bewerber.wunschberuf_1,
        bewerber.wunschberuf_2,
        bewerber.wunschberuf_3,
        bewerber.wunschberuf_4,
    ]

    if None in wunschberufe:
        raise ValidationError("Bewerber muss genau 4 Wunschberufe angeben.")

    freie_quartale = {"q1", "q2", "q3", "q4"}
    created_matchings = []

    for beruf in wunschberufe:
        # Filter: nur Plätze für diesen Beruf und freie Quartale
        platz = UnternehmenAusbildungsplatz.objects.filter(
            ausbildungsberuf=beruf,
            zeitraum__in=freie_quartale,
            status="frei"
        ).first()

        if not platz:
            raise ValidationError(f"Kein freier Ausbildungsplatz für {beruf} verfügbar.")

        # Matching erstellen
        matching = Matching.objects.create(
            bewerber=bewerber,
            unternehmen_ausbildungsplatz=platz,
            status="berechnet"
        )

        created_matchings.append(matching)
        freie_quartale.remove(platz.zeitraum)  # Quartal jetzt blockiert für die restlichen Wunschberufe

    return created_matchings