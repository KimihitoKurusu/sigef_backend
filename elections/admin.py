from django.contrib import admin
from .models import Institution, Campus, Faculty, Person, Election, Candidate, ElectorRegistry

# Register your models here.

admin.site.register(Institution)
admin.site.register(Campus)
admin.site.register(Faculty)
admin.site.register(Person)
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(ElectorRegistry)
