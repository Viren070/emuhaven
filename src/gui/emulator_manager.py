import gui.frames as frames
from gui.password_dialog import PasswordDialog()
from settings.settings import Settings
import customtkinter
from tkinter import messagebox
from PIL import Image
import os 
class EmulatorManager(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.define_images()
        self.build_gui()
    def define_images(self):
        self.dolphin_image = customtkinter.CTkImage(Image.open(self.settings.get_image_path("dolphin_logo")), size=(26, 26))
        self.yuzu_image = customtkinter.CTkImage(Image.open(self.settings.get_image_path("yuzu_logo")), size=(26, 26))
        self.play_image = customtkinter.CTkImage(light_image=Image.open(self.settings.get_image_path("play_light")),
                                                     dark_image=Image.open(self.settings.get_image_path("play_dark")), size=(20, 20))
        self.settings_image =  customtkinter.CTkImage(light_image=Image.open(self.settings.get_image_path("settings_light")),
                                                     dark_image=Image.open(self.settings.get_image_path("settings_dark")), size=(20, 20))
        self.lock_image =  customtkinter.CTkImage(light_image=Image.open(self.settings.get_image_path("padlock_light")),
                                                     dark_image=Image.open(self.settings.get_image_path("padlock_dark")), size=(20, 20))
    def build_gui(self):
        self.resizable(False, False)  # disable resizing of window
        self.title("Emulator Manager")  # set title of window
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.minsize(800,500) # set the minimum size of the window 
        
        
        # create navigation frame 
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # create navigation frame title. 
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text= "Emulator Manager v0.7.1",
                                                             compound="left", padx=5, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.navigation_frame_label.bind('<Double-Button-1>', command=lambda event: messagebox.showinfo("About", "Emulator Manager v0.7.1, made by Viren070 on GitHub."))
        # create navigation menu buttons
        self.dolphin_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, image = self.dolphin_image, border_spacing=10, text="Dolphin",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.dolphin_button_event)
        self.dolphin_button.grid(row=1, column=0, sticky="ew")

        self.yuzu_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, image = self.yuzu_image, border_spacing=10, text="Yuzu",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.yuzu_button_event)
        self.yuzu_button.grid(row=2, column=0, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, image = self.settings_image, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=6, column=0, sticky="ew")
    def dolphin_button_event(self):
        self.select_frame_by_name("dolphin")

    def yuzu_button_event(self):
        self.select_frame_by_name("yuzu")

    def settings_button_event(self):
        self.select_frame_by_name("settings")
    
    def select_frame_by_name(self, name):
        if not self.just_opened and ( self.dolphin_settings_changed() or self.yuzu_settings_changed() ) and name != "settings":
            if messagebox.askyesno("Confirmation", "You have unsaved changes in the settings, leave anyways?"):
                self.revert_settings()
            else:
                return 
        self.settings_button.configure(fg_color=("transparent"))
        # show selected frame
        if name == "settings" and not self.settings_unlocked: 
            self.validate_password()
            return
        if name == "settings" and self.settings_unlocked:
            self.minsize(1100,500)
            self.settings_button.configure(fg_color=("gray75", "gray25"))
            self.settings_frame.grid(row=0, column=1, sticky="nsew")       
        else:
            self.settings_frame.grid_forget()
            self.select_settings_frame_by_name(None)
            self.minsize(800,500)
        self.dolphin_button.configure(fg_color=("gray75", "gray25") if name == "dolphin" else "transparent")
        self.yuzu_button.configure(fg_color=("gray75", "gray25") if name == "yuzu" else "transparent")
        
        if name == "dolphin":
            self.dolphin_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dolphin_frame.grid_forget()
            self.select_dolphin_frame_by_name(None)
        if name == "yuzu":
            self.yuzu_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.yuzu_frame.grid_forget()
            self.select_yuzu_frame_by_name(None)
        
    def validate_password(self):
        dialog = PasswordDialog(text="Enter password:", title="Settings Password")
        guess = dialog.get_input()
        if guess == "" or guess is None:
            return
        if pbkdf2_hmac('sha256', guess.encode('utf-8'), bytes(b'GI\xaaK"\xcd`\x1b\x06\xc9\x18\x82\xc8c\xc5\xc9(\xa3\xc3\x93\x9e\xd2\xde\x93\\\x85\xd4\xb5\x1f\xcc\xac\x92'), 100000, dklen=128 ) == bytes(b'\xda\xea,d\x865\xaeS\xb1\\!~\x1c\xf7X\xef\xdfS\x94\x07i\xb8\x83<\x17h\x11Fc\xfd\xbdE\xf8\x044\xd6\xf6\x93m\xc9\xd6`{\xd9.R\xa3\xfe\x86\x00\x90&_\x12=\xdf\x99\xae\xe5\x92w\xdd\xbcwf]\xf41\x94\xa4q\x81P\xfd\x9dv\x9a\xb5\xfb\x13N\xe3"\x00\xe20\xc3\xf0\x01:\x0c\x18\x1d\xb1\x9b\xbdi\xf8\x02\t\xc5\t\xc50n(T\xff\x8b\xb1!\xf1\xba2\xe2y\x94\x89\xae]\x1f\xede\x9c=\xday`'):
            self.settings_unlocked = True
            self.select_frame_by_name("settings")
            self.minsize(1100,500)
            return
        else:
            messagebox.showerror("Incorrect", "That is the incorrect password, to make changes to the settings you require a password")
            return 
        
    def dolphin_settings_button_event(self):
        self.select_settings_frame_by_name("dolphin")
    def yuzu_settings_button_event(self):
        self.select_settings_frame_by_name("yuzu")
    def appearance_settings_button_event(self):
        self.select_settings_frame_by_name("appearance")
        
    def select_settings_frame_by_name(self, name):
        # set button color for selected button
        if not self.just_opened:
            if self.dolphin_settings_changed() and name != "dolphin":
                if messagebox.askyesno("Confirmation", "You have unsaved changes in the settings for dolphin, leave anyways?"):
                    self.revert_settings("dolphin")
                else:
                    return 
            if self.yuzu_settings_changed() and name != "yuzu":
                if messagebox.askyesno("Confirmation", "You have unsaved changes in the settings for dolphin, leave anyways?"):
                    self.revert_settings("yuzu")
                else:
                    return 
        self.yuzu_settings_button.configure(fg_color=("gray75", "gray25") if name == "yuzu" else "transparent")
        self.dolphin_settings_button.configure(fg_color=("gray75", "gray25") if name == "dolphin" else "transparent")
        self.appearance_settings_button.configure(fg_color=("gray75", "gray25") if name == "appearance" else "transparent")
        # show selected frame
        if name == "dolphin":
            self.dolphin_settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dolphin_settings_frame.grid_forget()
        if name == "yuzu":
            self.yuzu_settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.yuzu_settings_frame.grid_forget()
        if name == "appearance":
            self.appearance_settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.appearance_settings_frame.grid_forget()
    def lock_settings(self):
        self.settings_unlocked = False
        self.select_frame_by_name("None")