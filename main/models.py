from django.db import models
from django.core.exceptions import ValidationError

class Adresse(models.Model):
    strasse = models.CharField(max_length=100)
    hausnummer = models.CharField(max_length=10)
    plz = models.CharField(max_length=5, verbose_name="PLZ")
    ortsname = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.strasse} {self.hausnummer}, {self.plz} {self.ortsname}"

class Kontaktdaten(models.Model):
    vorwahl_telefonnummer = models.CharField(max_length=10)
    telefonnummer = models.CharField(max_length=20)
    email = models.EmailField(verbose_name="E-Mail-Adresse")

    def __str__(self):
        return self.email

class Branche(models.Model):
    bezeichnung = models.CharField(max_length=100)

    def __str__(self):
        return self.bezeichnung
   
AUSBILDUNGSBERUF_CHOICES = [
    # IT
    ("fachinformatiker", "Fachinformatiker*in"),
    ("it_systemelektroniker", "IT-Systemelektroniker*in"),
    # Baugewerbe
    ("tiefbaufacharbeiter", "Tiefbaufacharbeiter*in"),
    ("maurer", "Maurer*in"),
    # Handel
    ("einzelhandelskaufmann", "Kaufmann/-frau im Einzelhandel"),
    ("grosshandelskaufmann", "Kaufmann/-frau im Großhandel"),
    # Gesundheit & Pflege
    ("pflegefachkraft", "Pflegefachkraft"),
    ("medizinische_fachangestellte", "Medizinische Fachangestellte*r"),
    # Finanz & Verwaltung
    ("steuerfachangestellte", "Steuerfachangestellte*r"),
    ("versicherungs_kaufmann", "Kaufmann/-frau für Versicherungen & Finanzen"),
    # Verkehr & Logistik
    ("fachkraft_lagerlogistik", "Fachkraft für Lagerlogistik"),
    ("berufskraftfahrer", "Berufskraftfahrer*in"), ]
    
class AusbildungsplatzManager(models.Manager):
    def freie(self):
        return self.get_queryset().filter(blockiert=False)

class Ausbildungsberuf(models.Model):
    BRANCHEN_CHOICES = [
    ("it", "IT"),
    ("bau", "Baugewerbe"),
    ("handel", "Einzel- und Großhandel"),
    ("gesundheit_pflege", "Gesundheit & Pflege"),
    ("finanz_verwaltung", "Finanz & Versicherungswesen"),
    ("verkehr_logistik", "Verkehr & Logistik"), ]

    branche = models.ForeignKey(Branche, on_delete=models.CASCADE)
    bezeichnung = models.CharField(max_length=100, choices=AUSBILDUNGSBERUF_CHOICES)
    beschreibung = models.TextField()
    anforderungen = models.TextField()

    def __str__(self):
        return self.bezeichnung

class Unternehmen(models.Model):
    name = models.CharField(max_length=100, unique=True)
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)
    ansprechpartner = models.CharField(max_length=100)
    kontaktdaten = models.ForeignKey(Kontaktdaten, on_delete=models.CASCADE)
    beschreibung = models.TextField()

    def __str__(self):
        return self.name
 
class Bewerber(models.Model):
    GESCHLECHT_CHOICES = [
        ("m", "Männlich"),
        ("w", "Weiblich"),
        ("d", "Divers"), ]
    
    nachname = models.CharField(max_length=100)
    vorname = models.CharField(max_length=100)
    geburtsdatum = models.DateField()
    geschlecht = models.CharField(max_length=10, choices=GESCHLECHT_CHOICES)
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)
    kontaktdaten = models.ForeignKey(Kontaktdaten, on_delete=models.CASCADE)
    faehigkeiten_qualifikationen = models.TextField()
    motivationsschreiben = models.TextField()

    def __str__(self):
        return f"{self.vorname} {self.nachname}"

class BewerberWunschberuf(models.Model):
    bewerber = models.ForeignKey(Bewerber, on_delete=models.CASCADE)
    ausbildungsberuf = models.ForeignKey(Ausbildungsberuf, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("bewerber", "ausbildungsberuf")

    def clean(self):
        existing_count = BewerberWunschberuf.objects.filter(bewerber=self.bewerber).count()
        if existing_count >= 4 and not self.pk:
            raise ValidationError("Es dürfen maximal 4 Wunschberufe ausgewählt werden.")   

QUARTAL_CHOICES = [
    ("q1", "01.08 – 31.10"),
    ("q2", "01.11 – 31.01"),
    ("q3", "01.02 – 30.04"),
    ("q4", "01.05 – 31.07"),
]

QUARTAL_DATEN = {
    "q1": ("08-01", "10-31"),
    "q2": ("11-01", "01-31"),
    "q3": ("02-01", "04-30"),
    "q4": ("05-01", "07-31"),
}

PLATZ_STATUS_CHOICES = [
    ("frei", "Frei"),
    ("blockiert", "Blockiert"),
    ("vergeben", "Vergeben"), ]

class UnternehmenAusbildungsplatz(models.Model):
    unternehmen = models.ForeignKey(Unternehmen, on_delete=models.CASCADE, null=True, blank=True)
    ausbildungsberuf = models.ForeignKey(Ausbildungsberuf, on_delete=models.CASCADE)
    anforderungen_unternehmen = models.TextField()
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)
    zeitraum = models.CharField(max_length=10, choices=QUARTAL_CHOICES, default="q1")
    status = models.CharField(max_length=20, choices=PLATZ_STATUS_CHOICES, default="frei")

    def __str__(self):
        return f"{self.unternehmen.name} – {self.ausbildungsberuf} ({self.get_zeitraum_display()})"

MATCH_STATUS_CHOICES = [
        ("berechnet", "berechnet"),
        ("vorgeschlagen", "vorgeschlagen"),
        ("angenommen", "angenommen"),
        ("abgelehnt", "abgelehnt"), ]

class Matching(models.Model):
    bewerber = models.ForeignKey(Bewerber, on_delete=models.CASCADE, related_name="matchings")
    unternehmen_ausbildungsplatz = models.ForeignKey(UnternehmenAusbildungsplatz, on_delete=models.CASCADE, related_name="matchings")
    Matchingdatum = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    #score hinzufügen? -> score = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=MATCH_STATUS_CHOICES, default="berechnet")

    def clean(self):
        if self.status in ["vorgeschlagen", "akzeptiert"]:
            bestehende = Matching.objects.filter(
                unternehmen_ausbildungsplatz=self.unternehmen_ausbildungsplatz
            ).exclude(id=self.id)
            for match in bestehende:
                if match.status in ["vorgeschlagen", "akzeptiert", "blockiert"]:
                    raise ValidationError("Dieser Ausbildungsplatz ist bereits reserviert.")

    def save(self, *args, **kwargs):
        self.clean()
        if self.status in ["vorgeschlagen", "akzeptiert"]:
            self.unternehmen_ausbildungsplatz.status = "blockiert" if self.status == "vorgeschlagen" else "vergeben"
            self.unternehmen_ausbildungsplatz.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bewerber} → {self.unternehmen_ausbildungsplatz} ({self.status})"


class Einsatz(models.Model):
    matching = models.OneToOneField(Matching, on_delete=models.CASCADE, null=True, blank=True)
    EINSATZ_STATUS_CHOICES = [
        ("ausstehend", "ausstehend"),
        ("aktiv", "aktiv"),
        ("abgebrochen", "abgebrochen"), 
        ("abgeschlossen", "abgeschlossen"), ]
    
    bewerber = models.ForeignKey(Bewerber, on_delete=models.CASCADE)
    unternehmen_ausbildungsplatz = models.ForeignKey(UnternehmenAusbildungsplatz, on_delete=models.CASCADE)
    startdatum = models.CharField(max_length=5, null=True, blank=True)
    enddatum = models.CharField(max_length=5, null=True, blank=True)
    status = models.CharField(max_length=20, choices=EINSATZ_STATUS_CHOICES, default="ausstehend")

    def save(self, *args, **kwargs):
        quartal = self.matching.unternehmen_ausbildungsplatz.zeitraum
        start, ende = QUARTAL_DATEN[quartal]

        self.start = start
        self.ende = ende

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Einsatz: {self.matching.bewerber} – {self.matching.unternehmen_ausbildungsplatz} ({self.status})"

class Evaluation(models.Model):
    STATUS_CHOICES = [
        ("ausstehend", "ausstehend"),
        ("abgeschlossen", "abgeschlossen"), ]
    
    einsatz = models.ForeignKey(Einsatz, on_delete=models.CASCADE)
    datum = models.DateField()
    bewertung_bewerber = models.TextField()
    bewertung_unternehmen = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

# 4. Migration erstellen und in Railway-DB anwenden:
# Terminal:
# python3 manage.py makemigrations
# python3 manage.py migrate