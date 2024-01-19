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
        fields = '__all__'


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


class CandidateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateLog
        fields = '__all__'