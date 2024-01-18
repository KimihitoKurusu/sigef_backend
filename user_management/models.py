from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from elections.models import Person, Election


class UserManager(BaseUserManager):
    use_in_migrations = True

    # TODO: Recieve *param person object
    def _create_user(self, username, password, person_instance=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        if person_instance:
            user.person = person_instance
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, person=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        if not person:
            raise Exception('You have to send the corresponding data to the person table in order to create a user.!!!')
        password_aux = password
        if password is None:
            password_aux = self.make_random_password()

        if person:
            try:
                person_instance, created = Person.objects.get_or_create(person)
            except Exception as err:
                raise Exception(err)

        return self._create_user(username, password=password_aux, person_instance=person_instance, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True, blank=True, editable=True)
    username = models.CharField('Nombre de Usuario', max_length=255, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(
        'Es de la mesa electoral?',
        default=False,
        help_text='Indica si el usuario pertenece a la mesa electoral',
    )
    is_superuser = models.BooleanField(
        'Es super usuario?',
        default=False,
        help_text='Indica si el usuario tiene power',
    )
    election_id = models.ForeignKey(Election, null=True, blank=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def natural_key(self):
        return (self.username,)

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return f'{self.username} ({self.person.__str__()})'

class CustomUserLog(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, editable=True)
    username = models.CharField('Nombre de Usuario', max_length=255)
    date_joined = models.DateTimeField()
    is_staff = models.BooleanField(
        'Es de la mesa electoral?',
        default=False,
        help_text='Indica si el usuario pertenece a la mesa electoral',
    )
    is_superuser = models.BooleanField(
        'Es super usuario?',
        default=False,
        help_text='Indica si el usuario tiene power',
    )
    election_id = models.ForeignKey(Election, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username} ({self.person.__str__()})'