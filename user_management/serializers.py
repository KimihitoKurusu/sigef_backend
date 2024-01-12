# serializers.py

from rest_framework import serializers

from elections.models import Person
from elections.serializers import PersonSerializer
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    person = PersonSerializer()  # Use PersonSerializer for 'person' field

    class Meta:
        model = CustomUser
        fields = ('id', 'person', 'username', 'date_joined', 'is_staff', 'is_superuser', 'election_id')
        read_only_fields = ('id', 'date_joined')

    def create(self, validated_data):
        person_data = validated_data.pop('person', None)
        print(person_data)
        # Create Person if 'ci' data is provided
        if not Person.objects.filter(ci=person_data['ci']).exists():
            person = Person.objects.create(**person_data)
            validated_data['person'] = person

        return CustomUser.objects.create_user(**validated_data)

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
                person = Person.objects.create(**person_data)
                instance.person = person

        instance.username = validated_data.get('username', instance.username)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.election_id = validated_data.get('election_id', instance.election_id)
        instance.save()

        return instance
