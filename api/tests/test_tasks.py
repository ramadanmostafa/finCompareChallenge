from unittest.mock import patch, Mock, call

from django.test import TestCase, override_settings

from api.models import EmailData
from api.tasks import get_email_from_list, save_chunk, save_record


class TestGetEmailFromList(TestCase):

    def test_with_empty_list(self):
        self.assertEqual('', get_email_from_list([]))

    def test_with_no_emails(self):
        self.assertEqual('', get_email_from_list(['test1', 'test2']))

    def test_with_email(self):
        self.assertEqual('test@test.test', get_email_from_list(['test1', 'test2', 'test@test.test']))

    def test_with_multiple_emails(self):
        self.assertEqual(
            'test@test.test',
            get_email_from_list(['test1', 'test2', 'test@test.test', 'x', 'test1@test.test'])
        )


@override_settings(
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    CELERY_ALWAYS_EAGER=True,
    BROKER_BACKEND='memory',
    TEST_RUNNER='djcelery.contrib.test_runner.CeleryTestSuiteRunner'
)
class TestDelayedTasks(TestCase):

    @patch('api.tasks.save_record', autospec=True)
    def test_save_chunk_with_empty_data(self, save_record_mock):
        save_chunk.delay([])
        self.assertFalse(save_record_mock.delay.called)

    @patch('api.tasks.save_record', autospec=True)
    def test_save_chunk_with_no_emails(self, save_record_mock):
        save_chunk.delay(['test1', 'test2'])
        self.assertFalse(save_record_mock.delay.called)

    @patch('api.tasks.save_record', autospec=True)
    def test_save_chunk_valid_data(self, save_record_mock):
        data = [
            ['1', '2', '3', 'test@test.test'],
            ['1', '2', '3', 'test1@test.test'],
            ['1', '2', '3', 'test2@test.test'],
            ['1', '2', '3', 'test3@test.test'],
        ]
        call_list = [
            call('test@test.test', data[0]),
            call('test1@test.test', data[1]),
            call('test2@test.test', data[2]),
            call('test3@test.test', data[3]),
        ]
        save_chunk.delay(data)
        self.assertEqual(
            call_list,
            save_record_mock.delay.call_args_list
        )

    @patch('api.tasks.save_record', autospec=True)
    def test_save_chunk_mixed_data(self, save_record_mock):
        data = [
            ['1', '2', '3', '4'],
            ['1', '2', '3', '4'],
            ['1', '2', '3', 'test@test.test'],
            ['1', '2', '3', '4'],
            ['1', '2', '3', 'test1@test.test'],
            ['1', '2', '3', '4'],
            ['1', '2', '3', 'test2@test.test'],
            ['1', '2', '3', '4'],
            ['1', '2', '3', '4'],
            ['1', '2', '3', '4'],
        ]
        call_list = [
            call('test@test.test', data[2]),
            call('test1@test.test', data[4]),
            call('test2@test.test', data[6])
        ]
        save_chunk.delay(data)
        self.assertEqual(
            call_list,
            save_record_mock.delay.call_args_list
        )

    def test_save_record_new_email(self):
        self.assertEqual(0, EmailData.objects.all().count())
        save_record.delay('test@test.test', ['x', 'y', 'z'])
        self.assertEqual(1, EmailData.objects.all().count())
        record = EmailData.objects.get(email='test@test.test')
        self.assertEqual(['x', 'y', 'z'], record.data)
        self.assertIsNotNone(record.created)
        self.assertIsNotNone(record.updated)

    def test_save_record_already_existing_email(self):
        self.assertEqual(0, EmailData.objects.all().count())
        record = EmailData.objects.create(email='test@test.test', data=['1', '2', '3'])
        save_record.delay('test@test.test', ['x', 'y', 'z'])
        self.assertEqual(1, EmailData.objects.all().count())
        record.refresh_from_db()
        self.assertEqual(['x', 'y', 'z'], record.data)
        self.assertIsNotNone(record.created)
        self.assertIsNotNone(record.updated)
