from main.models import Einsatz, QUARTAL_DATEN

def erzeuge_einsatz(matching):
    # Erstellt einen Einsatz automatisch nach Annahme des Matchings
    platz = matching.unternehmen_ausbildungsplatz
    quartal = platz.zeitraum
    start, ende = QUARTAL_DATEN[quartal]

    einsatz = Einsatz.objects.create(
        matching=matching,
        bewerber=matching.bewerber,
        unternehmen_ausbildungsplatz=platz,
        startdatum=start,
        enddatum=ende,
        status="ausstehend"
    )
    return einsatz


def setze_einsatz_aktiv(einsatz: Einsatz):
    einsatz.status = "aktiv"
    einsatz.save()
    return einsatz

def setze_einsatz_abgebrochen(einsatz: Einsatz):
    einsatz.status = "abgebrochen"
    einsatz.save()
    return einsatz

def setze_einsatz_abgeschlossen(einsatz: Einsatz):
    einsatz.status = "abgeschlossen"
    einsatz.save()
    return einsatz