import os

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from api.serializers import BulkUploadCsvSerializer


class TestBulkUploadCsvSerializer(TestCase):

    def setUp(self):
        self.serializer = BulkUploadCsvSerializer()

    def test_with_no_file(self):
        data = {}
        with self.assertRaises(ValidationError) as context:
            self.serializer.validate(data)

        self.assertIn('file is required', str(context.exception))

    def test_with_file_wrong_extension(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_vectors/test.txt')
        data = {'file': open(path, 'rb')}
        with self.assertRaises(ValidationError) as context:
            self.serializer.validate(data)

        self.assertIn('file extension should be .csv', str(context.exception))

    def test_with_valid_file(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_vectors/data.csv')
        data = {'file': open(path, 'rb')}
        self.assertEqual(data, self.serializer.validate(data))