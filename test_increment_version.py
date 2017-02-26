import unittest

from mock import patch, mock_open

import increment_version

class TestGetVersion(unittest.TestCase):
    @patch('__builtin__.open', new_callable=mock_open, read_data='data')
    def test_reads_version_file(self, mock_file):
        with self.assertRaises(IndexError):
            increment_version.get_version()
            mock_file.assert_called_with('version.py')

    @patch('__builtin__.open', new_callable=mock_open, read_data="__version__ = '0.1.0'")
    def test_returns_version_number(self, mock_file):
        self.assertEqual(increment_version.get_version(), '0.1.0')

    @patch('__builtin__.open', new_callable=mock_open, read_data='foo')
    def test_handles_invalid_content(self, mock_file):
        with self.assertRaises(IndexError):
            increment_version.get_version()

    @patch('os.path.isfile', return_value=False)
    def test_handles_missing_version_file(self, mock_file):
        self.assertEqual(increment_version.get_version(), '0.0.0')

@patch('__builtin__.open', create=True)
@patch('increment_version.get_version', return_value='0.1.0')
class TestIncrementVersion(unittest.TestCase):
    def test_calls_get_version(self, mock_get_version, mock_open):
        increment_version.increment_version('major')
        mock_get_version.assert_called_once_with()

    def test_writes_to_version_file(self, mock_get_version, mock_open):
        increment_version.increment_version('major')
        mock_open.assert_called_once_with('version.py', 'wb')

    def test_increment_major_version(self, mock_get_version, mock_open):
        increment_version.increment_version('major')
        handle = mock_open()
        handle.__enter__().write.assert_called_once_with("__version__ = '1.0.0'\n")

    def test_increment_minor_version(self, mock_get_version, mock_open):
        increment_version.increment_version('minor')
        handle = mock_open()
        handle.__enter__().write.assert_called_once_with("__version__ = '0.2.0'\n")

    def test_increment_patch_version(self, mock_get_version, mock_open):
        increment_version.increment_version('patch')
        handle = mock_open()
        handle.__enter__().write.assert_called_once_with("__version__ = '0.1.1'\n")

    def test_handles_partial_version(self, mock_get_version, mock_open):
        mock_get_version.return_value = '1.3'
        increment_version.increment_version('minor')
        handle = mock_open()
        handle.__enter__().write.assert_called_once_with("__version__ = '1.4.0'\n")


if __name__ == '__main__':
    unittest.main()
