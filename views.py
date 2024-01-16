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


def config_window(self, root):
    # Global configurations for CTk window
    self.root.title("Pytube Downloader")
    self.root.resizable(1, 1)
    self.root._set_appearance_mode("dark")
    self.root.dark_mode_color = self.root.cget("fg_color")[1]
    self.root.configure(fg_color=self.root.dark_mode_color)


class Gui:
    def __init__(self):
        # Create queque for playlist downloads
        self.download_queue = queue.Queue()

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

        self.root = ctk.CTk()
        self.MENU_OPTIONS = {"v": "MP4", "a": "MP3", "p": "Playlist", "l": "Link"}

        # super().__init__()
        self.root.title("Pytube Downloader")
        self.root.resizable(1, 1)
        self.root._set_appearance_mode("dark")
        self.root.dark_mode_color = self.root.cget("fg_color")[1]
        self.root.configure(fg_color=self.root.dark_mode_color)

        self.menu1_opt = None
        self.menu2_opt = None
        self.url = None

        self.h1_font = ctk.CTkFont(family="Times New Roman", size=15, weight="bold")

        self.frame_1 = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame_2 = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame_3 = ctk.CTkFrame(self.root, fg_color="transparent")
        self.sv_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.input_frame = ctk.CTkFrame(self.root, fg_color="transparent")

        # self.menu2 = None

        self.menu1 = lambda: self.two_opt_menu(
            self.frame_1,
            "Seleccione el formato que desea descargar",
            "Video | MP4",
            "Audio | MP3",
            btn1_command=lambda: (
                self.frame_1.grid_forget(),
                self.menu2(),
                setattr(self, "menu1_opt", self.MENU_OPTIONS["v"]),
            ),
            btn2_command=lambda: (
                self.frame_1.grid_forget(),
                self.menu2(),
                setattr(self, "menu1_opt", self.MENU_OPTIONS["a"]),
            ),
        )

        self.choose_videos = lambda: (
            setattr(self, "menu2_opt", self.MENU_OPTIONS["p"]),
            self.two_opt_menu(
                self.frame_3,
                "¿Desea seleccionar los videos a descargar?",
                "Si",
                "No",
                btn1_command=lambda: self.select_videos(
                    last_window=(self.frame_3, self.choose_videos)
                ),
                btn2_command=lambda: (
                    self.input_url(),
                    setattr(self, "entries_checked", False),
                ),
                last_window=(self.frame_2, self.menu2),
            )
            if self.menu2_opt == self.MENU_OPTIONS["p"]
            else self.input_url(),
        )

        self.menu2 = lambda: (
            self.two_opt_menu(
                self.frame_2,
                "Seleccione la opción de descarga",
                "Descargar desde Playlist",
                "Descargar desde Link Directo",
                btn1_command=self.choose_videos,
                btn2_command=lambda: (
                    self.input_url(),
                    setattr(self, "menu2_opt", self.MENU_OPTIONS["l"]),
                ),
                last_window=(self.frame_1, self.menu1),
            ),
        )

        self.menu1()
        self.center_window()

    def center_window(self):
        # Center CTK window on screen
        self.root.update()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() / 2) - (self.root.winfo_reqheight())

        self.root.geometry(f"+{x}+{y}")

    def two_opt_menu(
        self,
        frame,
        label,
        btn1_text,
        btn2_text,
        btn1_command=None,
        btn2_command=None,
        last_window=None,
    ):
        if last_window != None:
            last_window[0].grid_forget()
            self.buttons(frame_remember=last_window[1], curr_frame=frame)

        frame.grid(sticky="nsew")

        # Configure row and column weights for the container frame
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.frame_l1 = ctk.CTkLabel(
            frame,
            text=label,
            font=self.h1_font,
            text_color="white",
        )
        self.frame_l1.grid(row=0, column=0, columnspan=2, pady=(15, 0), sticky="ew")

        self.frame_b1 = ctk.CTkButton(
            frame,
            text=btn1_text,
            command=btn1_command,
        )
        self.frame_b2 = ctk.CTkButton(frame, text=btn2_text, command=btn2_command)

        self.frame_b1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.frame_b2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def input_url(self):
        self.frame_2.grid_forget()
        self.frame_3.grid_forget()
        self.sv_frame.grid_forget()

        self.input_frame_l1 = ctk.CTkLabel(
            self.input_frame,
            text="Ingrese la URL correspondiente",
            font=self.h1_font,
            text_color="white",
        )
        self.input_frame_e1 = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="https://www.youtube.com/watch?v=xvFZjo5PgG0",
            width=350,
        )
        self.buttons(
            continue_btn_command=lambda: (
                setattr(self, "url", self.input_frame_e1.get()),
                self.download_video(),
            ),
            frame_remember=self.menu2,
            curr_frame=self.input_frame,
            continue_btn_text="Descargar",
        )

        self.progress = ctk.CTkLabel(
            self.input_frame, text_color="white", font=self.h1_font
        )
        self.progress.configure(text="0%")
        self.progressbar = ctk.CTkProgressBar(self.input_frame, width=400)
        self.progressbar.set(0)

        # fmt:off
        self.input_frame.grid(sticky="nsew")
        self.input_frame_l1.grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 0), sticky="ew")
        self.input_frame_e1.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        self.progress.grid(pady=20, row=3, column=0, columnspan=2, sticky="ew")
        self.progressbar.grid(row=4, column=0, columnspan=2, padx=30, pady=(0,30))
        # fmt:on

    def select_videos(self, last_window):
        last_window[0].grid_forget()

        self.entries_checked = False

        self.sv_frame.grid(sticky="nsew")

        # Configure row and column weights for the container frame
        self.sv_frame.grid_rowconfigure(0, weight=1)
        self.sv_frame.grid_rowconfigure(1, weight=1)
        self.sv_frame.grid_columnconfigure(0, weight=1)
        self.sv_frame.grid_columnconfigure(1, weight=1)

        self.sv_frame_l1 = ctk.CTkLabel(
            self.sv_frame,
            text="Ingrese el indice del primer video",
            font=self.h1_font,
            text_color="white",
        )
        self.sv_frame_l1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.sv_frame_e1 = ctk.CTkEntry(self.sv_frame, placeholder_text="1, 2, 3, ...")
        self.sv_frame_e1.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.sv_frame_l2 = ctk.CTkLabel(
            self.sv_frame,
            text="Ingrese el indice del ultimo video",
            font=self.h1_font,
            text_color="white",
        )
        self.sv_frame_l2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.sv_frame_e2 = ctk.CTkEntry(
            self.sv_frame, placeholder_text="... 9, 10, 11, ..."
        )
        self.sv_frame_e2.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        continue_btn_command = lambda: (
            self.input_url()
            if self.check_entries(self.sv_frame_e1.get(), self.sv_frame_e2.get())
            else print("Error")
        )

        self.buttons(
            continue_btn_command=continue_btn_command,
            frame_remember=last_window[1],
            curr_frame=self.sv_frame,
        )

    def buttons(
        self,
        continue_btn_command=None,
        curr_frame=None,
        frame_remember=None,
        continue_btn_text="Continuar",
    ):
        self.buttons_frame = ctk.CTkFrame(curr_frame, fg_color="transparent")
        self.buttons_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)

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
        if entry1.isdigit() != True:
            messagebox.showerror("Error", "Los indices ingresados son incorrectos")
        elif int(entry1) < 1:
            messagebox.showerror("Error", "Los indices ingresados son incorrectos")
        elif entry2.isdigit() != True or entry2 < entry1:
            messagebox.showerror("Error", "Los indices ingresados son incorrectos")
        else:
            self.entries_checked = True
            return True

        return False

    def download_video(self):
        if self.menu2_opt == self.MENU_OPTIONS["l"]:
            yt = YouTube(
                self.url,
                on_progress_callback=lambda stream, chunk, bytes_remaining: threading.Thread(
                    target=self.on_progress,
                    args=(stream, chunk, bytes_remaining),
                ).start(),
            )
            threading.Thread(target=self.download, args=(yt,)).start()

        elif self.menu2_opt == self.MENU_OPTIONS["p"]:
            playlist = Playlist(self.url)

            if self.entries_checked == True:
                videos = playlist.videos[
                    int(self.sv_frame_e1.get()) - 1 : int(self.sv_frame_e2.get())
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
