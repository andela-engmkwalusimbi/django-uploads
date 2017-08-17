from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from api.models import FilesModel

class FileUploadTests(APITestCase):

    def setUp(self):
        self.file_name = 'static/testfile.png'
        with open(self.file_name, 'rb') as file:
            data = {'image': file}
            response = self.client.post(reverse('files-list'), data, format='multipart')
        file.close()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), 'testfile.png')

    def tearDown(self):
        FilesModel.objects.all().delete()

    def test_query_returns_searched_for_file(self):
        file = FilesModel.objects.first()
        response = self.client.get('/api/uploads/files?q={}'.format('testfile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('size'), file.size)
        self.assertEqual(response.data[0].get('name'), file.name)


    def test_query_returns_entire_data_if_file_searched_for_does_mot_exist(self):
        self.assertEqual(FilesModel.objects.count(), 1)
        response = self.client.get('/api/uploads/files?q={}'.format('fake_name'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('size'), file.size)
        self.assertEqual(response.data[0].get('name'), file.name)