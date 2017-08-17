from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.core.files import File
from api.models import FilesModel

class FileUploadTests(APITestCase):

    def setUp(self):
        self.file_name = 'static/testfile.png'

    def tearDown(self):
        FilesModel.objects.all().delete()

    def test_file_uploads_successfully(self):
        with open(self.file_name, 'rb') as file:
            data = {'image': file}
            response = self.client.post(reverse('files-list'), data, format='multipart')
        file.close()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), 'testfile.png')

    def test_file_uploads_fails_when_you_send_wrong_info(self):
        data = {}
        response = self.client.post(reverse('files-list'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('image')[0], 'No file was submitted.')