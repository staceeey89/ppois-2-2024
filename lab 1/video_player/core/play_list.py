from collections import deque
from tkinter import Tk, filedialog
from core.video_file import VideoFile
import pickle


class PlayList:
    def __init__(self):
        self.queue = deque()

    def add_to_queue(self, file_path: str):
        self.queue.append(VideoFile(file_path))

    def get_video_to_play(self) -> VideoFile | None:
        if len(self.queue) != 0:
            return self.queue.popleft()
        else:
            print("Queue is empty")
            return None

    def save_playlist(self):
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Playlist files", "*.pkl")])
        if file_path:
            with open(file_path, 'wb') as file:
                pickle.dump(list(self.queue), file)
        root.destroy()

    def load_playlist(self):
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.askopenfilename(filetypes=[("Playlist files", "*.pkl")])
        if file_path:
            with open(file_path, 'rb') as file:
                video_files = pickle.load(file)

        root.destroy()
        self.queue = deque(video_files)

