from unittest.mock import patch, Mock, call

from django.test import TestCase

from api.utils import save_data, get_reader


class TestUtils(TestCase):

    @patch('api.utils.save_chunk', autospec=True)
    @patch('api.utils.get_reader', autospec=True)
    def test_save_data(self, reader, save_chunk):
        reader.return_value = [1]
        csvfile = Mock()
        csvfile.chunks.return_value = [1, 2, 3]

        self.assertIsNone(save_data(csvfile))
        save_chunk.delay.assert_called_with([1])

        self.assertEqual(
            [call(1), call(2), call(3)],
            reader.call_args_list
        )
        reader.assert_called_with(3)
        
    def test_get_reader(self):
        csvfile = str.encode('x,y\n1,2')
        self.assertEqual([['x', 'y'], ['1', '2']], list(get_reader(csvfile)))
