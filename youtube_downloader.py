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
        self.frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.h1_font = ctk.CTkFont(family="Times New Roman", size=15, weight="bold")

        # Global configurations for CTk window
        self.root.title("Pytube Downloader")
        self.root.resizable(1, 1)
        self.root._set_appearance_mode("dark")
        self.root.dark_mode_color = self.root.cget("fg_color")[1]
        self.root.configure(fg_color=self.root.dark_mode_color)

        # Configurations for frame
        self.frame.grid(sticky="nsew")

        self.download_format_window()

        self.center_window()

    def download_format_window(self):
        l1 = ctk.CTkLabel(
            self.frame,
            text="Seleccione el formato que desea descargar",
            font=ctk.CTkFont(family="Times New Roman", size=15, weight="bold"),
            text_color="white",
        )
        l1.grid(row=0, column=0, columnspan=2, pady=(15, 0), sticky="ew")

        b1 = ctk.CTkButton(
            self.frame,
            text="Video | MP4",
            command=lambda: (
                self.next_window(
                    current_window=self.frame,
                    next_window=self.download_option_window,
                    option="menu1_opt",
                    value="v",
                )
            ),
        )
        b2 = ctk.CTkButton(
            self.frame,
            text="Audio | MP3",
            command=lambda: (
                self.next_window(
                    current_window=self.frame,
                    next_window=self.download_option_window,
                    option="menu1_opt",
                    value="a",
                )
            ),
        )

        b1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        b2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.go_back(go_back_btn_destroy=True)

    def download_option_window(self):
        l1 = ctk.CTkLabel(
            self.frame,
            text="Seleccione la opción de descarga",
            font=ctk.CTkFont(family="Times New Roman", size=15, weight="bold"),
            text_color="white",
        )
        l1.grid(row=0, column=0, columnspan=2, pady=(15, 0), sticky="ew")

        b1 = ctk.CTkButton(
            self.frame,
            text="Descargar desde Playlist",
            command=lambda: (
                self.next_window(
                    current_window=self.frame,
                    next_window=self.download_option,
                    option="menu2_opt",
                    value="p",
                )
            ),
        )
        b2 = ctk.CTkButton(
            self.frame,
            text="Descargar desde Link Directo",
            command=lambda: (
                self.next_window(
                    current_window=self.frame,
                    next_window=self.download_option_window,
                    option="menu2_opt",
                    value="l",
                )
            ),
        )
        self.go_back(last_window=self.download_format_window)

        b1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        b2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def center_window(self):
        # Center CTK window on screen
        self.root.update()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() / 2) - (self.root.winfo_reqheight())

        self.root.geometry(f"+{x}+{y}")

    def next_window(self, current_window, next_window, option, value):
        setattr(self, option, self.MENU_OPTIONS[value])
        next_window(),

    def go_back(self, last_window=None, continue_btn=False, go_back_btn_destroy=False):
        self.buttons_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.buttons_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        go_back_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Volver",
            text_color="white",
            command=lambda: (last_window(),),
            fg_color="transparent",
            hover_color=self.root.dark_mode_color,
            width=50,
        )
        go_back_btn.grid(
            row=0,
            column=0,
            columnspan=2 if continue_btn == False else 1,
            padx=10,
            sticky="ew",
        )

        # if go_back_btn_destroy == True:
        #     go_back_btn.destroy()


app = Gui()
app.root.mainloop()
