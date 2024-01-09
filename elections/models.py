from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.

class Institution(models.Model):
    name = models.CharField(max_length=255)


class Campus(models.Model):
    institution_id = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Faculty(models.Model):
    campus_id = models.ForeignKey(Campus, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Person(models.Model):
    ci = models.CharField(unique=True, primary_key=True, max_length=11)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)


class Election(models.Model):
    TYPE_CHOICES = [
        ('institution', 'Institución'),
        ('campus', 'Sede'),
        ('faculty', 'Facultad'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location_id = models.IntegerField()
    council_size = models.IntegerField(validators=[MinValueValidator(3)])
    voting_date = models.DateTimeField(validators=[MinValueValidator(timezone.now)])
    is_active = models.BooleanField(default=False)


class Candidate(Person):
    WHO_ADDED_CHOICES = [
        ('committee', 'Comité'),
        ('elector', 'Elector'),
    ]
    election_id = models.ForeignKey(Election, on_delete=models.CASCADE)
    biography = models.TextField(
        verbose_name="Biografía",
        blank=True,
        null=True,
        help_text="Introduzca la biografía del candidato.",
    )
    who_added = models.CharField(max_length=20, choices=WHO_ADDED_CHOICES)
    staff_votes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    president_votes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    position = models.CharField(max_length=255, blank=True, null=True)


class ElectorRegistry(models.Model):
    ci = models.ForeignKey(Person, on_delete=models.CASCADE)
    election_id = models.ForeignKey(Election, on_delete=models.CASCADE)

    class Meta:
        db_table = 'elector_registry'
        constraints = [
            models.UniqueConstraint(fields=['ci', 'election_id'], name='unique_elector_registry')
        ]
