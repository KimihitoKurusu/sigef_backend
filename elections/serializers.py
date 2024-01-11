from rest_framework import serializers

from .models import *
from .permissions import IsCandidateManagerOrReadOnly, IsElectionManagerOrReadOnly


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
        fields = '__all__'


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'

    permission_classes = [IsElectionManagerOrReadOnly]


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['ci', 'name', 'last_name', 'faculty_id', 'election_id', 'biography', 'who_added', 'staff_votes',
                  'president_votes', 'position']

    permission_classes = [IsCandidateManagerOrReadOnly]


class ElectorRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectorRegistry
        fields = '__all__'
