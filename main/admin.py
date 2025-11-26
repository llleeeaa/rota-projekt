from django.contrib import admin

# registrierte models
from .models import (
    Adresse, Kontaktdaten, Branche, Ausbildungsberuf, Unternehmen,
    UnternehmenAusbildungsplatz, Bewerber, Matching, Einsatz, Evaluation
)

admin.site.register(Adresse)
admin.site.register(Kontaktdaten)
admin.site.register(Branche)
admin.site.register(Ausbildungsberuf)
admin.site.register(Unternehmen)
admin.site.register(UnternehmenAusbildungsplatz)
admin.site.register(Bewerber)
admin.site.register(Matching)
admin.site.register(Einsatz)
admin.site.register(Evaluation)
