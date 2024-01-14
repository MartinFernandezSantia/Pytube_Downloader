import customtkinter as ctk
import ctypes

# Don't know how it works, but it allows ctk to detect screen resolution correctly
ctypes.windll.shcore.SetProcessDpiAwareness(2)


class Gui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pytube Downloader")
        self.resizable(1, 1)
        self._set_appearance_mode("dark")
        self.dark_mode_color = self.cget("fg_color")[1]
        self.configure(fg_color=self.dark_mode_color)

        self.menu1_opt = None
        self.menu2_opt = None
        self.url = None

        self.h1_font = ctk.CTkFont(family="Times New Roman", size=15, weight="bold")

        self.frame_1 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_2 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_3 = ctk.CTkFrame(self, fg_color="transparent")

        # self.menu2 = None

        self.menu1 = lambda: self.two_opt_menu(
            self.frame_1,
            "Seleccione el formato que desea descargar",
            "Video | MP4",
            "Audio | MP3",
            btn1_command=lambda: (
                self.frame_1.grid_forget(),
                self.menu2(),
                setattr(self, "menu1_opt", "MP4"),
            ),
            btn2_command=lambda: (
                self.frame_1.grid_forget(),
                self.menu2(),
                setattr(self, "menu1_opt", "MP3"),
            ),
        )

        self.menu2 = lambda: (
            self.two_opt_menu(
                self.frame_2,
                "Seleccione la opción de descarga",
                "Descargar desde Playlist",
                "Descargar desde Link Directo",
                btn1_command=lambda: (
                    self.frame_2.grid_forget(),
                    self.input_url(),
                    setattr(self, "menu2_opt", "Playlist"),
                ),
                btn2_command=lambda: (
                    self.frame_2.grid_forget(),
                    self.input_url(),
                    setattr(self, "menu2_opt", "Link"),
                ),
                frame_before=self.menu1,
            ),
        )

        self.ingresar_indice = lambda: (
            self.frame_2.grid_forget(),
            self.two_opt_menu(
                self.frame_3,
                "¿Desea seleccionar los videos a descargar?",
                "Si",
                "No",
                frame_before=self.menu2,
            ),
        )

        self.menu1()
        self.center_window()

    # def update_options(self, menu1_opt=, menu2_opt=None, url=None):
    #     self.menu1_opt = menu1_opt
    #     self.menu2_opt = menu2_opt
    #     self.url = url

    def center_window(self):
        # Center CTK window on screen
        self.update()
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        y = (self.winfo_screenheight() / 2) - (self.winfo_reqheight())

        self.geometry(f"+{x}+{y}")

    def two_opt_menu(
        self,
        frame,
        label,
        btn1_text,
        btn2_text,
        btn1_command=None,
        btn2_command=None,
        frame_before=None,
    ):
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

        if frame_before != None:
            self.go_back(frame_before, frame, 2)

    def go_back(self, frame_remember, curr_frame, columnspan):
        self.go_back_btn = ctk.CTkButton(
            curr_frame,
            text="Volver",
            text_color="white",
            command=lambda: (
                curr_frame.grid_forget(),
                frame_remember(),
            ),
            fg_color="transparent",
            hover_color=self.dark_mode_color,
            width=50,
        )
        self.go_back_btn.grid(
            row=2,
            column=0,
            columnspan=columnspan,
            padx=10,
            pady=10,
            sticky="ew",
        )

    def input_url(self):
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(sticky="nsew")

        # Configure row and column weights for the container frame
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.input_frame_l1 = ctk.CTkLabel(
            self.input_frame,
            text="Ingrese la URL correspondiente",
            font=self.h1_font,
            text_color="white",
        )
        self.input_frame_l1.grid(
            row=0, column=0, columnspan=2, padx=20, pady=(15, 0), sticky="ew"
        )

        self.input_frame_e1 = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="https://www.youtube.com/watch?v=xvFZjo5PgG0",
            width=350,
        )
        self.input_frame_e1.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10
        )

        self.go_back(self.menu2, self.input_frame, 1)

        self.input_frame_b1 = ctk.CTkButton(
            self.input_frame,
            text="Continuar",
            width=50,
            command=lambda: (
                setattr(self, "url", self.input_frame_e1.get()),
                print(self.menu1_opt, self.menu2_opt, self.url),
            ),
        )
        self.input_frame_b1.grid(row=2, column=1, padx=10, pady=10, sticky="ew")


app = Gui()
app.mainloop()
