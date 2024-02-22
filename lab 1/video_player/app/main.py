from core.video_player import VideoPlayer
from core.file_chooser import FileChooser
from core.video_file import VideoFile
from core.play_list import PlayList

if __name__ == "__main__":
    file_chooser = FileChooser()
    playlist = PlayList()
    player = VideoPlayer()

    while True:
        print("1) choose video to play\n"
              "2) add video to queue\n"
              "3) play videos from playlist\n"
              "4) save playlist\n"
              "5) load playlist\n"
              "0) exit")
        choice = input()

        match choice:
            case '1':
                video_path = file_chooser.choose_file()
                if video_path:
                    player.play(VideoFile(video_path))

            case '2':
                video_path = file_chooser.choose_file()
                playlist.add_to_queue(video_path)

            case '3':
                while len(playlist.queue) != 0:
                    video_to_play = playlist.get_video_to_play()
                    if video_to_play is not None:
                        player.play(video_to_play)

            case '4':
                playlist.save_playlist()

            case '5':
                playlist.load_playlist()

            case '0':
                exit()
