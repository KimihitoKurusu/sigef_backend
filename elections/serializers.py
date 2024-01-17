import logging

from rest_framework import serializers

from .models import *

logger = logging.getLogger(__name__)


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id, campus_id, name']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['ci', 'name', 'last_name', 'faculty_id']


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Candidate
        fields = ['person', 'election_id', 'biography', 'who_added', 'staff_votes', 'president_votes', 'position']

    def create(self, validated_data):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", validated_data)
        try:
            person_data = validated_data.pop('person')
            person_instance, created = Person.objects.get_or_create(ci=person_data['ci'], defaults=person_data)
            validated_data['person'] = person_instance
        except Exception as err:
            raise Exception(err)

        return Candidate.objects.create(**validated_data)




class ElectorRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectorRegistry
        fields = '__all__'

    def create(self, validated_data):
        person_data = validated_data.pop('person', None)
        # Create Person if 'ci' data is provided
        if not Person.objects.filter(ci=person_data['ci']).exists():
            person = Person.objects.create(**person_data)
            validated_data['person'] = person
        else:
            person = Person.objects.get(person_data.ci)

        return Candidate.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        person_data = validated_data.pop('person', None)

        # Update Person if 'ci' data is provided
        if person_data:
            if instance.person:
                instance.person.ci = person_data.get('ci', instance.person.ci)
                instance.person.name = person_data.get('name', instance.person.name)
                instance.person.last_name = person_data.get('last_name', instance.person.last_name)
                instance.person.faculty_id = person_data.get('faculty_id', instance.person.faculty_id)
                instance.person.save()
            else:
                person = person = Person.objects.get(person_data.ci) | Person.objects.create(**person_data)
                instance.person = person

        instance.username = validated_data.get('username', instance.username)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.election_id = validated_data.get('election_id', instance.election_id)
        instance.save()

        return instance
