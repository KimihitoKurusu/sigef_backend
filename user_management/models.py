from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from elections.models import Person, Election


class UserManager(BaseUserManager):
    use_in_migrations = True

    # TODO: Recieve *param person object
    def _create_user(self, username, password, create_person=False, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, create_person=False, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        password_aux = password
        if password is None:
            password_aux = self.make_random_password()
        return self._create_user(username, password=password_aux, create_person=create_person, **extra_fields)

    def create_superuser(self, username, password, create_person=False, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, create_person=create_person, **extra_fields)


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
