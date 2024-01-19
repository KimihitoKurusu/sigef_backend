from django.urls import reverse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.test import APIClient

from .permissions import IsCandidateManagerOrReadOnly
from .permissions import IsSuperUserOrReadOnly
from .serializers import *
from user_management.models import CustomUser


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsSuperUserOrReadOnly]


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            print(f"Error updating Person: {e}")
            return Response({"error": "Error updating Person"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsCandidateManagerOrReadOnly]


class ElectorRegistryViewSet(viewsets.ModelViewSet):
    queryset = ElectorRegistry.objects.all()
    serializer_class = ElectorRegistrySerializer

    def create(self, request, *args, **kwargs):
        admin = CustomUser.objects.get(is_superuser = True)
        try:
            admin = admin.first()
        except Exception:
            print("There's only one superuser.")

        superuser=APIClient()
        superuser.force_authenticate(user=admin)

        # Json sample to be recieved in request
        data = {
            'elector': {
                'ci': '95112740402',
                'election_id': 1
            },
            'candidates': {
                '12345678901': {
                    'staff_votes': True,
                    'president_votes': False
                },
                '09876543219': {
                    'staff_votes': True,
                    'president_votes': True
                },
                '95112740402': {
                    'staff_votes': True,
                    'president_votes': False
                }
            }
        }

        for candidate_ci, votes in request.data['candidates']:
            # Getting the Candidate's staff votes and changing them if necessary
            staff = Candidate.objects.get(pk=candidate_ci).staff_votes
            staff = staff + 1 if votes['staff_votes'] else staff
            votes['staff_votes'] = staff
            # Getting the Candidate's president votes and changing them if necessary
            president = Candidate.objects.get(pk=candidate_ci).president_votes
            president = president + 1 if votes['president_votes'] else president
            votes['president_votes'] = president
            # Force updating the vote changes on the Candidate
            url = reverse('candidate-detail', args=[candidate_ci])
            admin.patch(url, votes, format='json')

        # Refactoring the request content to register the vote
        model_request = request
        model_request.data = request.data['elector']

        # Using the original method to register the vote
        return super.create(self, model_request, *args, **kwargs)
