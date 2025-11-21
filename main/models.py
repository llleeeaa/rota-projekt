# Schritt-für-Schritt Anleitung: Django-Modelle für deine Projektstruktur

# 1. App erstellen (falls noch nicht geschehen)
# Terminal:
# python3 manage.py startapp main

# 2. App in settings.py registrieren
# Datei: rota/settings.py
# INSTALLED_APPS = [..., 'main']

# 3. Datei main/models.py öffnen und folgendes einfügen:

from django.db import models

class Adresse(models.Model):
    strasse = models.CharField(max_length=100)
    hausnummer = models.CharField(max_length=10)
    plz = models.CharField(max_length=10)
    ortsname = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.strasse} {self.hausnummer}, {self.plz} {self.ortsname}"

class Kontaktdaten(models.Model):
    vorwahl_telefonnummer = models.CharField(max_length=10)
    telefonnummer = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.email

class Branche(models.Model):
    bezeichnung = models.CharField(max_length=100)

    def __str__(self):
        return self.bezeichnung

class Ausbildungsberuf(models.Model):
    branche = models.ForeignKey(Branche, on_delete=models.CASCADE)
    bezeichnung = models.CharField(max_length=100)
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

class UnternehmenAusbildungsplatz(models.Model):
    unternehmen = models.ForeignKey(Unternehmen, on_delete=models.CASCADE)
    ausbildungsberuf = models.ForeignKey(Ausbildungsberuf, on_delete=models.CASCADE)
    anforderungen_unternehmen = models.TextField()
    startdatum = models.DateField()
    enddatum = models.DateField()
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.unternehmen.name} – {self.ausbildungsberuf.bezeichnung}"

class Bewerber(models.Model):
    nachname = models.CharField(max_length=100)
    vorname = models.CharField(max_length=100)
    geburtsdatum = models.DateField()
    geschlecht = models.CharField(max_length=10)
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

class Matching(models.Model):
    bewerber = models.ForeignKey(Bewerber, on_delete=models.CASCADE)
    unternehmen_ausbildungsplatz = models.ForeignKey(UnternehmenAusbildungsplatz, on_delete=models.CASCADE)
    matching_datum = models.DateField()
    status = models.CharField(max_length=50)

class Einsatz(models.Model):
    bewerber = models.ForeignKey(Bewerber, on_delete=models.CASCADE)
    unternehmen_ausbildungsplatz = models.ForeignKey(UnternehmenAusbildungsplatz, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

class Evaluation(models.Model):
    einsatz = models.ForeignKey(Einsatz, on_delete=models.CASCADE)
    datum = models.DateField()
    bewertung_bewerber = models.TextField()
    bewertung_unternehmen = models.TextField()
    status = models.CharField(max_length=50)

# 4. Migration erstellen und in Railway-DB anwenden:
# Terminal:
# python3 manage.py makemigrations
# python3 manage.py migrate
