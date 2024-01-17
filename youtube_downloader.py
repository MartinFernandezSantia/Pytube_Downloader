import customtkinter as ctk
import ctypes
import threading
from tkinter import messagebox
from pytube import YouTube, Playlist
import re
import sys
import os
import queue

# Don't know how it works, but it allows ctk to detect screen resolution correctly
ctypes.windll.shcore.SetProcessDpiAwareness(2)


class Gui:
    def __init__(self):
        if getattr(sys, "frozen", False):
            # If running as an executable (PyInstaller)
            self.BASE_DIR = os.path.dirname(sys.executable)
        else:
            # If running as a script
            self.BASE_DIR = os.path.dirname(os.path.realpath(__file__))

        # Create Video and Music directories
        if not os.path.exists(os.path.join(self.BASE_DIR, "Music")):
            os.makedirs(os.path.join(self.BASE_DIR, "Music"))
        self.music_path = os.path.join(self.BASE_DIR, "Music")

        if not os.path.exists(os.path.join(self.BASE_DIR, "Video")):
            os.makedirs(os.path.join(self.BASE_DIR, "Video"))
        self.video_path = os.path.join(self.BASE_DIR, "Video")

        # Constants
        self.MENU_OPTIONS = {"v": "MP4", "a": "MP3", "p": "Playlist", "l": "Link"}

        # Variables
        self.menu1_opt = None
        self.menu2_opt = None
        self.url = None

        # Initialize Queque for playlist download
        self.download_queue = queue.Queue()

        # Initialize CTk window
        self.root = ctk.CTk()

        # Global CTk widgets
        self.frame_1 = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame_2 = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame_3 = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame_4 = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame_5 = ctk.CTkFrame(self.root, fg_color="transparent")
        self.h1_font = ctk.CTkFont(family="Times New Roman", size=15, weight="bold")


        # Global configurations for CTk window
        self.root.title("Pytube Downloader")
        self.root.resizable(1, 1)
        self.root._set_appearance_mode("dark")
        self.root.dark_mode_color = self.root.cget("fg_color")[1]
        self.root.configure(fg_color=self.root.dark_mode_color)

        self.download_format_window()
        self.center_window()

    def download_format_window(self):
        self.frame_1.grid(sticky="nsew")

        l1 = ctk.CTkLabel(
            self.frame_1,
            text="Seleccione el formato que desea descargar",
            font=self.h1_font,
            text_color="white",
        )

        b1 = ctk.CTkButton(
            self.frame_1,
            text="Video | MP4",
            command=lambda: (
                self.next_window(
                    current_window=self.frame_1,
                    next_window=self.download_option_window,
                    option="menu1_opt",
                    value="v",
                )
            ),
        )
        b2 = ctk.CTkButton(
            self.frame_1,
            text="Audio | MP3",
            command=lambda: (
                self.next_window(
                    current_window=self.frame_1,
                    next_window=self.download_option_window,
                    option="menu1_opt",
                    value="a",
                )
            ),
        )

        l1.grid(row=0, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        b1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        b2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # self.buttons_frame.grid_remove()

    def download_option_window(self):
        # self.select_videos_frame.grid_forget()
        self.frame_2.grid(sticky="nsew")

        l1 = ctk.CTkLabel(
            self.frame_2,
            text="Seleccione la opción de descarga",
            font=self.h1_font,
            text_color="white",
        )
        b1 = ctk.CTkButton(
            self.frame_2,
            text="Descargar desde Playlist",
            command=lambda: (
                self.next_window(
                    current_window=self.frame_2,
                    next_window=self.yes_or_no_window,
                    option="menu2_opt",
                    value="p",
                )
            ),
        )
        b2 = ctk.CTkButton(
            self.frame_2,
            text="Descargar desde Link Directo",
            command=lambda: (
                self.next_window(
                    current_window=self.frame_2,
                    next_window=self.input_url,
                    option="menu2_opt",
                    value="l",
                ),
                self.progress.configure(text="0%"),
            ),
        )

        l1.grid(row=0, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        b1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        b2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # self.go_back(last_window=self.download_format_window)
        self.buttons(curr_frame=self.frame_2, frame_remember=self.download_format_window, )

    def yes_or_no_window(self):
        self.frame_3.grid(sticky="nsew")

        l1 = ctk.CTkLabel(
            self.frame_3,
            text="¿Desea seleccionar los videos a descargar?",
            font=self.h1_font,
            text_color="white",
        )
        b1 = ctk.CTkButton(
            self.frame_3,
            text="Si",
            command=lambda: (
                self.next_window(
                    current_window=self.frame_3,
                    next_window=self.select_videos_window,
                )
            ),
        )
        b2 = ctk.CTkButton(
            self.frame_3,
            text="No",
            command=lambda: (
                self.next_window(
                    current_window=self.frame_3,
                    next_window=self.input_url,
                ),
            ),
        )
        l1.grid(row=0, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        b1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        b2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # self.buttons_frame.grid_remove()

    def select_videos_window(self):
        self.frame_4.grid(sticky="nsew")

        l1 = ctk.CTkLabel(
            self.frame_4,
            text="Ingrese el indice del primer video",
            font=self.h1_font,
            text_color="white",
        )
        l2 = ctk.CTkLabel(
            self.frame_4,
            text="Ingrese el indice del ultimo video",
            font=self.h1_font,
            text_color="white",
        )

        self.sv_e1 = ctk.CTkEntry(self.frame_4, placeholder_text="1, 2, 3, ...")
        self.sv_e2 = ctk.CTkEntry(
            self.frame_4, placeholder_text="... 9, 10, 11, ..."
        )

        self.buttons(
            continue_btn_command=lambda: (
                self.next_window(current_window=self.frame_4, next_window=self.input_url)
                if self.check_entries(self.sv_e1.get(), self.sv_e2.get())
                else messagebox.showerror("Error", "Los indices ingresados son incorrectos"),
                ),
            curr_frame=self.frame_4,
            frame_remember=self.download_option_window,
        )

        l1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        l2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.sv_e1.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.sv_e2.grid(row=1, column=1, sticky="ew", padx=10, pady=10)


    def input_url(self):
        self.frame_5.grid(sticky="nsew")

        l1 = ctk.CTkLabel(
            self.frame_5,
            text="Ingrese la URL correspondiente",
            font=self.h1_font,
            text_color="white",
        )
        e1 = ctk.CTkEntry(
            self.frame_5,
            placeholder_text="https://www.youtube.com/watch?v=xvFZjo5PgG0",
            width=350,
        )
        self.buttons(
            continue_btn_command=lambda: (
                setattr(self, "url", e1.get()),
                self.download_video(),
            ),
            frame_remember=self.download_option_window,
            curr_frame=self.frame_5,
            continue_btn_text="Descargar",
        )
        self.progress = ctk.CTkLabel(
            self.frame_5, text_color="white", font=self.h1_font
        )
        self.progress.configure(text="0%")
        self.progressbar = ctk.CTkProgressBar(self.frame_5, width=400)
        self.progressbar.set(0)

        # fmt:off
        l1.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 0), sticky="ew")
        e1.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        self.progress.grid(pady=20, row=3, column=0, columnspan=2, sticky="ew")
        self.progressbar.grid(row=4, column=0, columnspan=2, padx=30, pady=(0,30))
        # fmt:on

    def center_window(self):
        # Center CTK window on screen
        self.root.update()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() / 2) - (self.root.winfo_reqheight())

        self.root.geometry(f"+{x}+{y}")

    def next_window(self,current_window, next_window, option=None, value=None):
        if option != None:
            # Set attribute for chosen option
            setattr(self, option, self.MENU_OPTIONS[value])

        # Hide current window
        current_window.grid_forget()
        # Load next window
        next_window(),

    def buttons(
            self,
            continue_btn_command=None,
            curr_frame=None,
            frame_remember=None,
            continue_btn_text="Continuar",
        ):
            # Create frame inside of current frame for the buttons
            self.buttons_frame = ctk.CTkFrame(curr_frame, fg_color="transparent")
            self.buttons_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

            self.buttons_frame.grid_rowconfigure(0, weight=1)
            self.buttons_frame.grid_columnconfigure(0, weight=1)
            self.buttons_frame.grid_columnconfigure(1, weight=1)

            # Create button to go back to last window
            if frame_remember != None:
                self.go_back_btn = ctk.CTkButton(
                    self.buttons_frame,
                    text="Volver",
                    text_color="white",
                    command=lambda: (
                        curr_frame.grid_forget(),
                        frame_remember(),
                    ),
                    fg_color="transparent",
                    hover_color=self.root.dark_mode_color,
                    width=50,
                )
                self.go_back_btn.grid(
                    row=0,
                    column=0,
                    columnspan=2 if continue_btn_command == None else 1,
                    padx=10,
                    sticky="ew",
                )

            # Create button to move forward to next window or download
            if continue_btn_command != None:
                self.continue_btn = ctk.CTkButton(
                    self.buttons_frame,
                    text=continue_btn_text,
                    width=50,
                    command=continue_btn_command,
                )
                self.continue_btn.grid(
                    row=0,
                    column=1,
                    columnspan=1,
                    padx=10,
                    sticky="ew",
                )

    def check_entries(self, entry1, entry2):
        # Check if the input of user is a digit greater or equal to 1
        if entry1.isdigit() != True:
            return False
        elif int(entry1) < 1:
            return False
        # Check if input is lower than first entry
        elif entry2.isdigit() != True or entry2 < entry1:
            return False
        else:
            self.entries_checked = True
            return True
#############################################################
#############################################################
    def download_video(self):
        if self.menu2_opt == self.MENU_OPTIONS["l"]:
            yt = YouTube(
                self.url,
                on_progress_callback=lambda stream, chunk, bytes_remaining: threading.Thread(
                    target=self.on_progress,
                    args=(stream, chunk, bytes_remaining),
                ).start(),
                on_complete_callback=lambda stream, file_path: messagebox.showinfo("", "¡La descarga a finalizado exitosamente!")

            )

            threading.Thread(target=self.download, args=(yt,)).start()

        elif self.menu2_opt == self.MENU_OPTIONS["p"]:
            playlist = Playlist(self.url)

            if self.entries_checked == True:
                videos = playlist.videos[
                    int(self.sv_e1.get()) - 1 : int(self.sv_e2.get())
                ]
            else:
                videos = playlist.videos

            for video in videos:
                self.download_queue.put(video)
        # Start a worker thread
        threading.Thread(target=self.download_worker).start()

    def download_worker(self):
        while not self.download_queue.empty():
            video = self.download_queue.get()
            video.register_on_progress_callback(self.on_progress)
            self.download(video)
            self.download_queue.task_done()

        messagebox.showinfo("", "¡La descarga a finalizado exitosamente!")


    def download(self, yt):
        title = self.sanitize_filename(yt.title)

        if self.menu1_opt == self.MENU_OPTIONS["a"]:
            path = self.music_path
            filename = f"{title}.mp3"
            streams = yt.streams.filter(only_audio=True)

            for stream in streams:
                if int(stream.abr[:-4]) == 160:
                    break
        elif self.menu1_opt == self.MENU_OPTIONS["v"]:
            path = self.video_path
            filename = f"{title}.mp4"
            stream = yt.streams.get_highest_resolution()

        stream.download(output_path=path, filename=filename)

    def sanitize_filename(self, filename, cut_filename=False):
        if cut_filename == True:
            words = filename.split()
            # Cut every 5 words
            filename = "\n".join(
                [" ".join(words[i : i + 5]) for i in range(0, len(words), 5)]
            )

        # Replace invalid characters with underscores
        return re.sub(r'[<>:"/\\|?*]', "_", filename)

    def get_playlist_length(self, url):
        p = Playlist(url)
        return len(p.video_urls)

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_download = total_size - bytes_remaining
        completition_percentage = bytes_download / total_size * 100

        self.progress.configure(
            text=f"Descargando: {self.sanitize_filename(stream.title, cut_filename=True)}\n {int(completition_percentage)}%"
        )
        self.progress.update()

        self.progressbar.set(int(completition_percentage) / 100)


app = Gui()
app.root.mainloop()
