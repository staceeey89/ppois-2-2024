from tkinter import Tk, filedialog


class FileChooser:
    @staticmethod
    def choose_file() -> str:
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.askopenfilename(title="Choose a video file",
                                               filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
        root.destroy()
        return file_path
