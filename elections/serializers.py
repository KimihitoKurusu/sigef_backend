from rest_framework import serializers

from .models import *


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


class CandidateSerializer(serializers.ModelSerializer):
   person = PersonSerializer()

   class Meta:
       model = Candidate
       fields = ['person'] + [field.name for field in Candidate._meta.fields]


class ElectorRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectorRegistry
        fields = '__all__'
