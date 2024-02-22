import pygame
from moviepy.video.io.VideoFileClip import VideoFileClip


class VideoFile:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.video_clip = None
        self.fps = 0.0
        self.duration = 0.0

    def configure_video(self):
        self.video_clip = VideoFileClip(self.file_path)
        audio_clip = self.video_clip.audio

        self.fps = self.video_clip.fps
        self.duration = self.video_clip.duration

        temp_audio_file_path = "temp_audio.wav"
        audio_clip.write_audiofile(temp_audio_file_path, codec="pcm_s16le")

        pygame.mixer.music.load(temp_audio_file_path)
