import jwt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException

from elections.models import Candidate, Election


class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad Request"


def is_same_election_id(user_election_id, election_id_from_data, election_id_from_url, type):
    if not election_id_from_data and not election_id_from_url:
        raise CustomAPIException("You do not have an election ID")

    if type == 'candidate':
        election_id = election_id_from_data or (
            Candidate.objects.filter(pk=election_id_from_url)
            .values_list('election_id', flat=True)
            .first() if election_id_from_url else None
        )
    elif type == 'election':
        election_id = election_id_from_data or (
            Election.objects.filter(pk=election_id_from_url)
            .values_list('id', flat=True)
            .first() if election_id_from_url else None
        )
    else:
        raise CustomAPIException("Invalid 'type' parameter. Use 'candidate' or 'election'.")

    if user_election_id != election_id:
        raise CustomAPIException("User does not have permission for this election")

    return True


# TODO
def verification_token(request):
    token = request.headers.get('Authorization')
    secret_key = 'tu_clave_secreta'

    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        # El payload ahora contiene la información que enviaste desde el frontend


        # Realiza las operaciones necesarias con la información
        # ...

        return payload
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token expirado'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Token inválido'}, status=401)
