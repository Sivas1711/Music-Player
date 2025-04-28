import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer
from PIL import Image, ImageTk  # New import for background image

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Stylish Python Music Player")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Load background image
        self.bg_image = Image.open("background.jpg")  # Make sure you have a background.jpg in the same folder
        self.bg_image = self.bg_image.resize((600, 450), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(root, width=600, height=450)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Transparent Frame
        self.frame = tk.Frame(root, bg="#ffffff", bd=0)  # 80 = transparent white
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=320)

        mixer.init()
        self.playlist = []
        self.current_index = 0
        self.is_paused = False

        # Title
        self.title_label = tk.Label(self.frame, text="🎶 My Music Player 🎶", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1e3d59")
        self.title_label.pack(pady=10)

        # Current Song Label
        self.label = tk.Label(self.frame, text="No Song Playing", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1e3d59")
        self.label.pack(pady=5)

        # Control Buttons Frame
        self.control_frame = tk.Frame(self.frame, bg="#ffffff")
        self.control_frame.pack(pady=10)

        # Buttons
        self.create_button("📂 Select Folder", self.load_folder, 0, 0, colspan=2)
        self.create_button("▶ Play", self.play_music, 1, 0)
        self.create_button("⏸ Pause", self.pause_music, 1, 1)
        self.create_button("⏹ Stop", self.stop_music, 2, 0)
        self.create_button("⏭ Next", self.next_music, 2, 1)
        self.create_button("⏮ Previous", self.prev_music, 3, 0, colspan=2)

    def create_button(self, text, command, row, col, colspan=1):
        btn = tk.Button(self.control_frame, text=text, command=command,
                        font=("Segoe UI", 10, "bold"),
                        bg="#45b29a", fg="white",
                        activebackground="#334d5c",
                        activeforeground="white",
                        bd=0,
                        relief="flat",
                        padx=20, pady=5)
        if colspan == 2:
            btn.grid(row=row, column=col, columnspan=2, padx=10, pady=5, sticky="ew")
        else:
            btn.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

    def load_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.playlist = [os.path.join(folder_selected, file)
                             for file in os.listdir(folder_selected)
                             if file.endswith(('.mp3', '.wav'))]
            self.current_index = 0
            if self.playlist:
                self.play_music()

    def play_music(self):
        if not self.playlist:
            messagebox.showinfo("No Music", "Please select a music folder first.")
            return
        song = self.playlist[self.current_index]
        mixer.music.load(song)
        mixer.music.play()
        self.label.config(text=f"Playing: {os.path.basename(song)}")
        self.is_paused = False

    def pause_music(self):
        if self.is_paused:
            mixer.music.unpause()
            self.label.config(text=f"Playing: {os.path.basename(self.playlist[self.current_index])}")
        else:
            mixer.music.pause()
            self.label.config(text="Paused")
        self.is_paused = not self.is_paused

    def stop_music(self):
        mixer.music.stop()
        self.label.config(text="Stopped")

    def next_music(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_music()

    def prev_music(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_music()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
