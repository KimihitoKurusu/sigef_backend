import json
import unittest
from unittest.mock import MagicMock

import jwt
from django.http import JsonResponse

from elections.helpers.permission_helpers import verification_token


class VerificarTokenTest(unittest.TestCase):

    def assertJsonResponseEqual(self, response, expected_status, expected_data):
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(json.loads(response.content), expected_data)

    def test_verificar_token_exitoso(self):
        # Simula una solicitud HTTP con un encabezado de autorización válido
        request = MagicMock()
        request.headers.get.return_value = 'tu_token_valido'

        # Simula el comportamiento esperado de jwt.decode para un token válido
        with unittest.mock.patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {'info': 'data'}

            # Llama a la función y verifica que devuelva el payload correctamente
            result = verification_token(request)
            self.assertEqual(result, {'info': 'data'})

            # Verifica que la función se llamó correctamente con los parámetros esperados
            mock_decode.assert_called_once_with('tu_token_valido', 'tu_clave_secreta', algorithms=['HS256'])

    def test_verificar_token_expirado(self):
        # Simula una solicitud HTTP con un encabezado de autorización válido
        request = MagicMock()
        request.headers.get.return_value = 'tu_token_expirado'

        # Simula el comportamiento esperado de jwt.decode para un token con firma expirada
        with unittest.mock.patch('jwt.decode') as mock_decode:
            mock_decode.side_effect = jwt.ExpiredSignatureError('Token expirado')

            # Llama a la función y verifica que devuelva un JsonResponse con el error correspondiente
            result = verification_token(request)
            expected_response = JsonResponse({'error': 'Token expirado'}, status=401)
            self.assertJsonResponseEqual(result, expected_response.status_code, json.loads(expected_response.content))

    def test_verificar_token_invalido(self):
        # Simula una solicitud HTTP con un encabezado de autorización válido
        request = MagicMock()
        request.headers.get.return_value = 'tu_token_invalido'

        # Simula el comportamiento esperado de jwt.decode para un token inválido
        with unittest.mock.patch('jwt.decode') as mock_decode:
            mock_decode.side_effect = jwt.InvalidTokenError('Token inválido')

            # Llama a la función y verifica que devuelva un JsonResponse con el error correspondiente
            result = verification_token(request)
            expected_response = JsonResponse({'error': 'Token inválido'}, status=401)
            self.assertJsonResponseEqual(result, expected_response.status_code, json.loads(expected_response.content))
