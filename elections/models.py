from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.

class Institution(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Campus(models.Model):
    institution_id = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    campus_id = models.ForeignKey(Campus, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Person(models.Model):
    ci = models.CharField(unique=True, primary_key=True, max_length=11)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name + ' ' + self.last_name


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

    def __str__(self):
        if self.type == 'institution':
            location = Institution.objects.get(pk=self.location_id).name
        elif self.type == 'campus':
            location = Campus.objects.get(pk=self.location_id).name
        else:
            location = Faculty.objects.get(pk=self.location_id).name

        return f'Elecciones de {self.get_type_display()} en {location}'


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

    def __str__(self):
        return f'{self.name} {self.last_name}'


class ElectorRegistry(models.Model):
    ci = models.ForeignKey(Person, on_delete=models.CASCADE)
    election_id = models.ForeignKey(Election, on_delete=models.CASCADE)

    class Meta:
        db_table = 'elector_registry'
        constraints = [
            models.UniqueConstraint(fields=['ci', 'election_id'], name='unique_elector_registry')
        ]

    def __str__(self):
        return Person.objects.get(pk=self.ci).__str__() + ' ' + Election.objects.get(pk=self.election_id).__str__()
