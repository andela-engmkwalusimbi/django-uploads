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


    def test_file_exists(self):
        file = FilesModel.objects.first()
        response = self.client.get(reverse('file-details', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), file.id)
        self.assertEqual(response.data.get('size'), file.size)
        self.assertEqual(response.data.get('name'), file.name)


    def test_file_does_not_exist(self):
        self.assertEqual(FilesModel.objects.count(), 1)
        response = self.client.get(reverse('file-details', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_file_gets_deleted_successfully(self):
        self.assertEqual(FilesModel.objects.count(), 1)
        response = self.client.delete(reverse('file-details', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FilesModel.objects.count(), 0)

    def test_file_does_not_get_deleted_if_it_does_not_exist(self):
        self.assertEqual(FilesModel.objects.count(), 1)
        response = self.client.delete(reverse('file-details', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(FilesModel.objects.count(), 1)