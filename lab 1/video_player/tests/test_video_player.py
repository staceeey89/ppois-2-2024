import unittest
from unittest.mock import patch

from core.file_chooser import FileChooser
from core.video_file import VideoFile
from core.play_list import PlayList
from core.volume_controller import VolumeController
from core.brightness_controller import BrightnessController


class TestVolumeController(unittest.TestCase):
    def test_increase_volume(self):
        with patch('pygame.mixer.music.get_volume', return_value=0.5):
            with patch('pygame.mixer.music.set_volume') as mock_set_volume:
                VolumeController.increase_volume(0.1)
                mock_set_volume.assert_called_once_with(0.6)

    def test_decrease_volume(self):
        with patch('pygame.mixer.music.get_volume', return_value=0.5):
            with patch('pygame.mixer.music.set_volume') as mock_set_volume:
                VolumeController.decrease_volume(0.1)
                mock_set_volume.assert_called_once_with(0.4)


class TestPlayList(unittest.TestCase):
    def test_add_to_queue(self):
        playlist = PlayList()
        video_file = VideoFile("test.mp4")
        playlist.add_to_queue(video_file.file_path)
        self.assertEqual(len(playlist.queue), 1)
        self.assertEqual(playlist.queue[0].file_path, "test.mp4")

    def test_get_video_to_play(self):
        playlist = PlayList()
        video_file = VideoFile("test.mp4")
        playlist.add_to_queue(video_file.file_path)

        result = playlist.get_video_to_play()

        self.assertIsNotNone(result)
        self.assertEqual(result.file_path, video_file.file_path)
        self.assertEqual(result.video_clip, video_file.video_clip)
        self.assertEqual(result.fps, video_file.fps)
        self.assertEqual(result.duration, video_file.duration)

        self.assertEqual(len(playlist.queue), 0)


class TestBrightnessController(unittest.TestCase):
    def test_increase_brightness(self):
        current_brightness = BrightnessController.get_brightness()
        BrightnessController.increase_brightness()
        new_brightness = BrightnessController.get_brightness()
        self.assertEqual(new_brightness, current_brightness + 5)

    def test_decrease_brightness(self):
        current_brightness = BrightnessController.get_brightness()
        BrightnessController.decrease_brightness()
        new_brightness = BrightnessController.get_brightness()
        self.assertEqual(new_brightness, current_brightness - 5)


class TestFileChooser(unittest.TestCase):
    @patch('tkinter.Tk')
    @patch('tkinter.filedialog.askopenfilename')
    def test_choose_file(self, mock_askopenfilename, mock_tk):
        mock_askopenfilename.return_value = 'test_video.mp4'
        file_path = FileChooser.choose_file()
        self.assertEqual(file_path, 'test_video.mp4')


if __name__ == '__main__':
    unittest.main()
