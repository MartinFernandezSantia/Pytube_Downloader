from pytube import Playlist, YouTube
from tqdm import tqdm
import os
import re
import sys

class Downloader:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            # If running as an executable (PyInstaller)
            self.BASE_DIR = os.path.dirname(sys.executable)
        else:
            # If running as a script
            self.BASE_DIR = os.path.dirname(os.path.realpath(__file__))

        if not os.path.exists(os.path.join(self.BASE_DIR, "Music")):
            os.makedirs(os.path.join(self.BASE_DIR, "Music"))
        self.music_path = os.path.join(self.BASE_DIR, "Music")

        if not os.path.exists(os.path.join(self.BASE_DIR, "Video")):
            os.makedirs(os.path.join(self.BASE_DIR, "Video"))
        self.video_path = os.path.join(self.BASE_DIR, "Video")

        self.mp3_or_mp4 = ""
        while self.mp3_or_mp4 != "a" and self.mp3_or_mp4 != "v":
            self.mp3_or_mp4 = input("Video (v) o Audio (a)?: ")
        
        playlist_or_video = ""
        while playlist_or_video != "p" and playlist_or_video != "v":
            playlist_or_video = input("Lista de reproduccion (p) o video unico (v)?: ")


        if playlist_or_video == "p":
            self.choice_slice = ""
            while self.choice_slice != "s" and self.choice_slice != "n":
                self.choice_slice = input("Desea ingresar indice del primer y ultimo video a descargar? (s/n): ")

            if self.choice_slice == "s":
                self.start_playlist = int(input("Ingrese el indice de inicio (0,1,2,3,...): "))
                self.end_playlist = int(input("Ingrese el indice final (0,1,2,3,...): "))

        self.url = input("Introduzca la URL del video/lista de reproduccion: ")

        if playlist_or_video == "p":
            self.playlist()
        elif playlist_or_video == "v":
            self.video()


    def playlist(self):
        yt = Playlist(self.url)
    
        if self.choice_slice == "s":
            videos = yt.videos[self.start_playlist:self.end_playlist]
        else:
            videos = yt.videos

        for video in videos:
            try:
                print(f"Downloading: {video.title}")
            except Exception as e:
                print(f'Error in decoding title: {e}')

            video.register_on_progress_callback(self.progress_callback)

            if self.mp3_or_mp4 == "a":
                path = self.music_path
                filename = f"{self.sanitize_filename(video.title)}.mp3"
                streams = video.streams.filter(only_audio=True)
                
                for stream in streams:
                    if int(stream.abr[:-4]) == 160:
                        break

            elif self.mp3_or_mp4 == "v":
                path = self.video_path
                filename = f"{self.sanitize_filename(video.title)}.mp4"
                stream = video.streams.get_highest_resolution()

            self.pbar = tqdm(total=stream.filesize, unit="bytes")
            stream.download(output_path=path, filename=filename)
            self.pbar.close()


    def video(self):
        yt = YouTube(self.url)
        yt.register_on_progress_callback(self.progress_callback)

        try:
            print(f"Downloading: {yt.title}")
        except Exception as e:
            print(f'Error in decoding title: {e}')

        if self.mp3_or_mp4 == "a":
            path = self.music_path
            filename = f"{self.sanitize_filename(yt.title)}.mp3"
            streams = yt.streams.filter(only_audio=True)
            
            for stream in streams:
                if int(stream.abr[:-4]) == 160:
                    break
        elif self.mp3_or_mp4 == "v":
            path = self.video_path
            filename = f"{self.sanitize_filename(yt.title)}.mp4"
            stream = yt.streams.get_highest_resolution()

        self.pbar = tqdm(total=stream.filesize, unit="bytes")
        stream.download(output_path=path, filename=filename)
        self.pbar.close()

    def progress_callback(self, stream, chunk, bytes_remaining):
        self.pbar
        self.pbar.update(len(chunk))

    def sanitize_filename(self, filename):
    # Replace invalid characters with underscores
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

if __name__ == "__main__":
    downloader = Downloader()
