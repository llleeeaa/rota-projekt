from django.test import TestCase
from main.models import Bewerber, UnternehmenAusbildungsplatz, Matching
from services.matching_service import setze_status_vorgeschlagen, setze_status_angenommen

class MatchingServiceTest(TestCase):
    def test_matching_status(self):
        bewerber = Bewerber.objects.create(vorname="Max", nachname="Mustermann")
        platz = UnternehmenAusbildungsplatz.objects.create(ausbildungsberuf_id=1, zeitraum="q1", status="frei")
        matching = Matching.objects.create(bewerber=bewerber, unternehmen_ausbildungsplatz=platz, status="berechnet")
        
        setze_status_vorgeschlagen(matching)
        self.assertEqual(matching.status, "vorgeschlagen")
        self.assertEqual(platz.status, "blockiert")

        setze_status_angenommen(matching)
        self.assertEqual(matching.status, "angenommen")
        self.assertEqual(platz.status, "vergeben")
