import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from faker import Faker

from elections.models import Institution, Campus, Faculty, Election, Person, Candidate, ElectorRegistry
from user_management.models import CustomUser

fake = Faker()


class InstitutionFactory(DjangoModelFactory):
    class Meta:
        model = Institution

    name = factory.Faker('company')


class CampusFactory(DjangoModelFactory):
    class Meta:
        model = Campus

    institution_id = factory.SubFactory(InstitutionFactory)
    name = factory.Faker('company')


class FacultyFactory(DjangoModelFactory):
    class Meta:
        model = Faculty

    campus_id = factory.SubFactory(CampusFactory)
    name = factory.Faker('company')


class ElectionFactory(DjangoModelFactory):
    class Meta:
        model = Election

    type = factory.Faker('word')
    location_id = 1
    council_size = factory.Faker('random_digit_not_null')
    voting_date = factory.Faker('date_time_this_year')
    is_active = factory.Faker('boolean')


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    ci = factory.LazyFunction(lambda: f"{fake.unique.random_number(digits=11)}")
    name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    faculty_id = factory.SubFactory(FacultyFactory)


class CandidateFactory(DjangoModelFactory):
    class Meta:
        model = Candidate

    person = factory.SubFactory(PersonFactory)
    election_id = factory.SubFactory(ElectionFactory)
    biography = factory.Faker('paragraph')
    who_added = factory.Faker('random_element', elements=['committee', 'elector'])
    staff_votes = factory.Faker('random_int', min=0, max=100)
    president_votes = factory.Faker('random_int', min=0, max=100)
    position = factory.Faker('job')


class ElectorRegistryFactory(factory.Factory):
    class Meta:
        model = ElectorRegistry

    ci = factory.SubFactory(PersonFactory)
    election_id = factory.SubFactory(ElectionFactory)


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    person = factory.SubFactory(PersonFactory)  # Ajusta según tu estructura de PersonFactory
    username = factory.Sequence(lambda n: f'user{n}')
    date_joined = timezone.now()
    is_staff = True
    is_superuser = False
    election_id = factory.SubFactory(ElectionFactory)

    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     # Hash de la contraseña para evitar problemas al crear el usuario
    #     kwargs['password'] = make_password(kwargs.pop('password', 'password'))
    #     return super()._create(model_class, *args, **kwargs)
