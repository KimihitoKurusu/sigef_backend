from django.db import models
from elections.models import Person
from django.core.validators import MinValueValidator
from django.utils import timezone

# Create your models here.

class User(Person):
    date_joined = models.DateTimeField(validators=[MinValueValidator(timezone.now)], default=timezone.now)
    exp_date = models.DateTimeField(validators=[MinValueValidator(timezone.now)], default=timezone.now)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    class Meta:
        db_table = 'user'
        constraints = [
            models.UniqueConstraint(fields=['ci', 'date_joined'], name='unique_user')
        ]