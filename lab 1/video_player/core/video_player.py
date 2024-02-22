import numpy as np
import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT
from core.brightness_controller import BrightnessController
from core.volume_controller import VolumeController
from core.video_file import VideoFile


class VideoPlayer:
    supported_formats = {".mp4", ".avi", ".mkv"}

    def __init__(self):
        self.video_file: VideoFile | None = None
        self.paused: bool = False

    @staticmethod
    def init_pygame():
        pygame.init()
        pygame.mixer.init()

    @staticmethod
    def init_display(size: tuple[int, int]) -> pygame.Surface:
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Video Player")
        return screen

    def play_video(self, screen: pygame.Surface):
        clock = pygame.time.Clock()
        pygame.mixer.music.play()

        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < self.video_file.duration * 1000:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    self.pause()
                elif event.type == KEYDOWN and event.key == K_UP:
                    VolumeController.increase_volume()
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    VolumeController.decrease_volume()
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    BrightnessController.decrease_brightness()
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    BrightnessController.increase_brightness()

            if not self.paused:
                elapsed_time = pygame.time.get_ticks() - start_time
                frame = self.video_file.video_clip.get_frame(elapsed_time / 1000)
                self.display_show_frame(screen, frame)

            clock.tick_busy_loop(self.video_file.fps)

        pygame.quit()

    @staticmethod
    def display_show_frame(screen: pygame.Surface, frame: np.ndarray):
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()

    def pause(self):
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    @staticmethod
    def increase_volume():
        VolumeController.increase_volume()

    @staticmethod
    def decrease_volume():
        VolumeController.decrease_volume()

    def play(self, video_file: VideoFile):
        self.init_pygame()
        self.video_file = video_file

        if not any(video_file.file_path.lower().endswith(fmt) for fmt in self.supported_formats):
            print("Invalid video file format. Please choose a file with supported formats:",
                  ", ".join(self.supported_formats))
            return

        # Configure the video before initializing the display
        self.video_file.configure_video()

        screen = self.init_display(video_file.video_clip.size)

        self.play_video(screen)
