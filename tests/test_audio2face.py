# py_audio2face/tests/test_audio2face.py

import unittest
from unittest.mock import patch, MagicMock
from py_audio2face.audio2face import Audio2Face


class TestAudio2Face(unittest.TestCase):

    def setUp(self):
        # Optional: Set up any necessary configurations or mocks for the tests
        pass

    def tearDown(self):
        # Optional: Clean up after each test
        pass

    @patch('py_audio2face.audio2face.requests.get')
    def test_start_headless_server_success(self, mock_get):
        # Simulate a successful status response
        mock_get.return_value.json.return_value = "OK"

        a2f = Audio2Face()
        status = a2f.start_headless_server()

        self.assertEqual(status, "OK")

    @patch('py_audio2face.audio2face.requests.get')
    def test_start_headless_server_timeout(self, mock_get):
        # Simulate a timeout scenario
        mock_get.return_value.json.return_value = "NOT OK"

        a2f = Audio2Face()
        status = a2f.start_headless_server()

        self.assertEqual(status, "timeout")

    @patch('py_audio2face.audio2face.os.path.isfile', MagicMock(return_value=True))
    def test_audio2face_single_with_sample_file(self):
        # Mocking necessary methods for file existence check

        with patch('py_audio2face.audio2face.Audio2Face.init_a2f') as mock_init_a2f, \
                patch('py_audio2face.audio2face.Audio2Face.set_root_path') as mock_set_root_path, \
                patch('py_audio2face.audio2face.Audio2Face.set_track') as mock_set_track, \
                patch('py_audio2face.audio2face.Audio2Face.export_blend_shape') as mock_export_blend_shape:
            a2f = Audio2Face()
            sample_audio_file = 'path/to/assets/test_audio.wav'
            output_path = 'path/to/output/sample_animation.usd'
            a2f.audio2face_single(sample_audio_file, output_path, fps=60)

            mock_init_a2f.assert_called_once()
            mock_set_root_path.assert_called_once_with('path/to/assets')
            mock_set_track.assert_called_once_with(sample_audio_file)
            mock_export_blend_shape.assert_called_once_with(output_path=output_path, fps=60)

    def test_shutdown_a2f(self):
        # Optional: Write tests for shutdown_a2f method
        pass

    def test_make_request(self):
        # Optional: Write tests for make_request method
        pass

    # Add more test methods as needed


if __name__ == '__main__':
    unittest.main()