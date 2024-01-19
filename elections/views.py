import jwt
from decouple import config
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .permissions import IsCandidateManagerOrReadOnly, IsReadOnly
from .permissions import IsSuperUserOrReadOnly
from .serializers import *


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
        if 'token' not in request.data:
            return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = jwt.decode(request.data['token'], config('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        candidates = Candidate.objects.filter(pk__in=data['candidates'].keys())
        elector = Person.objects.get(ci=data['elector']['ci'])
        election = Election.objects.get(pk=data['elector']['election_id'])

        for candidate in candidates:
            votes = data['candidates'][str(candidate.pk)]
            candidate.staff_votes += 1 if votes['staff_votes'] else 0
            candidate.president_votes += 1 if votes['president_votes'] else 0

        Candidate.objects.bulk_update(candidates, ['staff_votes', 'president_votes'])

        new_registry = ElectorRegistry(ci=elector, election_id=election)
        new_registry.save()

        return Response({'message': 'Voting successfully completed!!!'}, status=status.HTTP_201_CREATED)


class CandidateLogViewSet(viewsets.ModelViewSet):
    queryset = CandidateLog.objects.all()
    serializer_class = CandidateLogSerializer
    permission_classes = [IsReadOnly]