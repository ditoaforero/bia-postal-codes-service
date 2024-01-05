from io import BytesIO
from tests.base_test_case import BaseTestCase
import json
from unittest.mock import patch
import infrastructure

class EndpointTestCase(BaseTestCase):
    def test_calculate_postcode(self):
        response = self.client.get('/calculate-postcode')
        assert response.status_code == 200
        assert json.loads(response.data) == {"message": "Calculating postal code"}


    @patch('infrastructure.database.PostalCodeDB.copy_file_to_db')
    def test_coordinates(self, mock_copy_file_to_db):
        mock_copy_file_to_db.return_value = ""
        file_content = b'52.923454,-1.474217'
        data = {'file': (BytesIO(file_content), 'test1.csv')}

        response = self.client.post('/coordinates', content_type='multipart/form-data', buffered=True, data=data)
        assert response.status_code == 200
        assert json.loads(response.data) == {"message": "Archivo CSV almacenado exitosamente en la base de datos"}
