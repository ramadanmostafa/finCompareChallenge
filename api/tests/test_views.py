import os

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class FileUploadTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('upload_csv')
        self.format = 'multipart'

    def test_with_no_file(self):
        response = self.client.post(self.url, {}, format=self.format)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({'file': ['No file was submitted.']}, response.json())

    def test_invalid_extension(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_vectors/test.txt')
        data = {'file': open(path, 'rb')}
        # assert authenticated user can upload file
        response = self.client.post(self.url, data, format=self.format)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({'file': ['file extension should be .csv']}, response.json())

    def test_upload_file(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_vectors/data.csv')
        data = {'file': open(path, 'rb')}
        # assert authenticated user can upload file
        response = self.client.post(self.url, data, format=self.format)
        self.assertEqual(status.HTTP_200_OK, response.status_code)