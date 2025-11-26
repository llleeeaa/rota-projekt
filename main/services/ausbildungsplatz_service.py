from main.models import UnternehmenAusbildungsplatz, QUARTAL_CHOICES

def erzeuge_alle_ausbildungsplaetze_jahr(unternehmen, ausbildungsberuf, anforderungen, adresse):
    
    # Erstellt automatisch 4 Ausbildungsplätze für das nächste Jahr (q1-q4).
    created = []
    for quartal, _ in QUARTAL_CHOICES:
        platz = UnternehmenAusbildungsplatz.objects.create(
            unternehmen=unternehmen,
            ausbildungsberuf=ausbildungsberuf,
            anforderungen_unternehmen=anforderungen,
            adresse=adresse,
            zeitraum=quartal,
            status="frei"
        )
        created.append(platz)
    return created


def blockiere_platz(platz: UnternehmenAusbildungsplatz):
    # Blockiert den Platz (bei vorgeschlagenem Matching)
    if platz.status == "frei":
        platz.status = "blockiert"
        platz.save()
    return platz

def vergebe_platz(platz: UnternehmenAusbildungsplatz):
    # Vergibt den Platz (bei angenommenem Matching)
    platz.status = "vergeben"
    platz.save()
    return platz

def gebe_platz_frei(platz: UnternehmenAusbildungsplatz):
    # Macht den Platz wieder frei (wenn Matching abgelehnt wird)
    platz.status = "frei"
    platz.save()
    return platz

def ist_frei(platz: UnternehmenAusbildungsplatz):
    return platz.status == "frei"

def ist_blockiert(platz: UnternehmenAusbildungsplatz):
    return platz.status == "blockiert"

def ist_vergeben(platz: UnternehmenAusbildungsplatz):
    return platz.status == "vergeben"