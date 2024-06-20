import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

pygame.init()
notification_sound = pygame.mixer.Sound(r'C:\Users\Sammy\Documents\Python\Notification Sound\mixkit-bell-notification-933.wav')

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Timer")
        master.config(bg="#292929")

        self.current_session = "Work"

        self.pomodoro_length = 25 * 60  # 25 minutes in seconds
        self.break_length = 5 * 60  # 5 minutes in seconds

        self.time_remaining = self.pomodoro_length

        self.session_label = tk.Label(master, font=("Helvetica", 15), bg="#292929", fg="#FFFFFF", text=self.current_session)
        self.session_label.pack()

        self.timer_label = tk.Label(master, font=("Helvetica", 48), bg="#292929", fg="#FFFFFF", text=self.format_time(self.time_remaining))
        self.timer_label.pack(padx=10, pady=10)

        button_style = {"bg": "#1c1c1c", "fg": "#FFFFFF", "activebackground": "#666666", "activeforeground": "#FFFFFF", "bd": 0, "highlightthickness": 0, "font": ("Helvetica", 16), "relief": tk.RIDGE, "borderwidth": 0}

        self.start_button = tk.Button(master, text="Start", command=self.start_timer, **button_style)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer, **button_style)
        self.stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer, **button_style)
        self.reset_button.pack(side=tk.BOTTOM, pady=10)

        self.break_button = tk.Button(master, text="Start Break", command=self.start_break, **button_style)
        self.break_button.pack(side=tk.BOTTOM, pady=10)

        self.clock_label = tk.Label(master, font=("Helvetica", 16), bg="#292929", fg="#FFFFFF")
        self.clock_label.pack(side=tk.BOTTOM, pady=10)

        self.timer_running = False
        self.timer_id = None

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer_id = self.master.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.master.after_cancel(self.timer_id)

    def reset_timer(self):
        self.stop_timer()
        self.time_remaining = self.pomodoro_length
        self.timer_label.config(text=self.format_time(self.time_remaining))

    def start_break(self):
        self.stop_timer()
        self.time_remaining = self.break_length
        self.timer_label.config(text=self.format_time(self.time_remaining))
        self.timer_running = True
        self.timer_id = self.master.after(1000, self.update_timer)
        self.current_session = "Break"
        self.session_label.config(text=self.current_session)

    def update_timer(self):
        self.time_remaining -= 1
        self.timer_label.config(text=self.format_time(self.time_remaining))
        if self.time_remaining <= 0:
            self.timer_running = False
            self.timer_id = None
            self.timer_label.config(text="Time's up!")
            notification_sound.play()
        else:
            self.timer_id = self.master.after(1000, self.update_timer)

        current_time = time.strftime("%I:%M:%S %p")
        self.clock_label.config(text=current_time)

    button_style = {"bg": "#1c1c1c", "fg": "#FFFFFF", "activebackground": "#666666", "activeforeground": "#FFFFFF", "bd": 0, "highlightthickness": 0,"font": ("Helvetica", 16), "relief": tk.RIDGE, "borderwidth": 2,}
    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer_id = self.master.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.master.after_cancel(self.timer_id)

    def reset_timer(self):
        self.stop_timer()
        self.time_remaining = 25 * 60
        self.timer_label.config(text=self.format_time(self.time_remaining))
        self.current_session = "Work"
        self.session_label.config(text=self.current_session)
    
    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def update_timer(self):
        self.time_remaining -= 1
        self.timer_label.config(text=self.format_time(self.time_remaining))

        if self.time_remaining == 0:
            notification_sound.play()
            if self.timer_type == "work":
                self.timer_type = "break"
                self.time_remaining = 5 * 60
                self.timer_label.config(fg="#FFFFFF")
                self.timer_label.config(bg="#292929")
                self.start_button.config(text="Start Break")
            elif self.timer_type == "break":
                self.timer_type = "work"
                self.time_remaining = 25 * 60
                self.timer_label.config(fg="#FFFFFF")
                self.timer_label.config(bg="#292929")
                self.start_button.config(text="Start Work")

        self.timer_id = self.master.after(1000, self.update_timer)

        current_time = time.strftime("%I:%M:%S %p")
        self.clock_label.config(text=current_time)

    def start_break(self):
        notification_sound.play()
        self.current_session = "Break"
        self.session_label.config(text=self.current_session)
        self.time_remaining = 5 * 60
        self.timer_label.config(fg="#FFFFFF")
        self.timer_label.config(bg="#292929")
        self.start_timer()
    button_style = {"bg": "#1c1c1c", "fg": "#FFFFFF", "activebackground": "#666666", "activeforeground": "#FFFFFF", "bd": 0, "highlightthickness": 0, "font": ("Helvetica", 16), "relief": tk.RIDGE, "borderwidth": 2,}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="c84b62dbcfa6427e9a4cb99872c256fa",
                                               client_secret="c735c3e927414dba90d2cf963a1f3222",
                                               redirect_uri="http://localhost:8000",
                                               scope="user-read-playback-state,user-modify-playback-state"))
# Define the tkinter application
class SpotifyControlApp:
    def __init__(self, master):      
        self.master = master
        button_frame = tk.Frame(master)
        song_frame = tk.Frame(master)
        song_frame.pack(pady=5)
        button_frame.pack(pady=5)

        self.playback_state = None
        self.current_track_id = None
        self.check_playback_state()

        self.login_text = "Login"

        button_style = {"bg": "#1c1c1c", "fg": "#FFFFFF", "activebackground": "#666666", "activeforeground": "#FFFFFF", "bd": 0, "highlightthickness": 0, "font": (12), "relief": tk.RIDGE, "borderwidth": 0,}
        
        # Create the login button
        self.login_button = tk.Button(master, text=self.login_text , command=self.login_to_spotify,borderwidth=0)
        self.login_button.place(relx=1.0, x=-10, y=10, anchor="ne")
        self.login_button.config(button_style, padx=5, pady=5)

        self.play_photo =  PhotoImage(file = r"C:/Users\Sammy\Documents/Python/Images/play-button-arrowhead.png")
        self.pause_photo = PhotoImage(file = r"C:/Users\Sammy\Documents/Python/Images/pause.png")
        self.next_photo = PhotoImage(file = r"C:/Users\Sammy\Documents/Python/Images/next.png")
        self.previous_photo = PhotoImage(file = r"C:/Users\Sammy\Documents/Python/Images/previous.png")
        self.spotify_photo = PhotoImage(file = r"C:/Users\Sammy\Documents/Python/Images/Spotify.png")
        
        # Create the playback control buttons

        self.label = tk.Label(button_frame,image=self.spotify_photo, compound="center",)
        self.label.config(bg="#292929", fg="#FFFFFF", font=("Helvetica", 16),pady=5)
        self.label.pack()

        self.prev_button = tk.Button(button_frame,command=self.previous, image=self.previous_photo, compound="center", borderwidth=0)
        self.prev_button.config(bg="#292929",activebackground="#1c1c1c")
        self.prev_button.pack(side='left',padx=10,pady=10)

        self.play_button = tk.Button(button_frame,command=self.play, image=self.play_photo, compound="center", borderwidth=0)
        self.play_button.config(bg="#292929",activebackground="#1c1c1c")
        self.play_button.pack(side='left',padx=10,pady=10)
        
        self.pause_button = tk.Button(button_frame,command=self.pause, image=self.pause_photo, compound="center", borderwidth=0)
        self.pause_button.config(bg="#292929",activebackground="#1c1c1c")
        self.pause_button.pack(side='left',padx=10,pady=10)
        
        self.next_button = tk.Button(button_frame,command=self.next, image=self.next_photo, compound="center", borderwidth=0)
        self.next_button.config(bg="#292929",activebackground="#1c1c1c",fg="#FFFFFF")
        self.next_button.pack(side='left',padx=10,pady=10)

        self.track_info = tk.Label(song_frame, text="", bg="#292929", fg="#FFFFFF", font=("Helvetica", 12))
        self.track_info.config(bg="#292929", fg="#FFFFFF", font=("Helvetica", 16))
        self.track_info.pack(pady=5)        
        
        song_frame.place(relx=0.5, rely=0.5, anchor='center')
        song_frame.config(bg="#292929")

        button_frame.place(relx=0.5, rely=0.35, anchor='center')
        button_frame.config(bg="#292929")

        self.prev_button.config(state="disabled")
        self.play_button.config(state="disabled")
        self.pause_button.config(state="disabled")
        self.next_button.config(state="disabled")

    def check_playback_state(self):
        try:
            playback = sp.current_playback()
            if playback is None:
                self.playback_state = None
            else:
                is_playing = playback['is_playing']
                if is_playing and self.playback_state != 'playing':
                    self.playback_state = 'playing'
                    self.update_track_info()
                elif not is_playing and self.playback_state in ('playing', 'paused'):
                    self.playback_state = 'paused'
                # Check for a change in the currently playing track
                current_track_id = playback["item"]["id"]
                if self.current_track_id != current_track_id:
                    self.current_track_id = current_track_id
                    self.update_track_info()
            self.master.after(100, self.check_playback_state)
        except Exception as e:
            print(e)

    def login_to_spotify(self):
            user = sp.current_user()
            if not user:
                webbrowser.open('https://accounts.spotify.com/authorize')
                self.prev_button.config(state="disabled")
                self.play_button.config(state="disabled")
                self.pause_button.config(state="disabled")
                self.next_button.config(state="disabled")
            else:
                self.user_profile = sp.me()
                self.login_text = self.user_profile["display_name"]
                self.login_button.config(text=self.login_text)
                self.update_track_info()
                self.prev_button.config(state="normal")
                self.play_button.config(state="normal")
                self.pause_button.config(state="normal")
                self.next_button.config(state="normal")        

    def update_track_info(self):
        try:
            track = sp.current_user_playing_track()
            track_info_text = ""
            if track is not None:
                track_name = track["item"]["name"]
                track_artist = track["item"]["artists"][0]["name"]
                track_info_text = f"{track_name} - {track_artist}"
                self.track_info_text_len = len(track_info_text)
                if self.track_info_text_len >= 35:
                    self.font_size = 10
                else:
                    self.font_size = 16
            self.track_info.config(text=track_info_text,font=("Helvetica",self.font_size))
        except Exception as e:
            print(e)


    def play(self):
        # Play the current track
        sp.start_playback()
        time.sleep(0.5)  
        self.update_track_info()
        
    def pause(self):
        # Pause the current track
        sp.pause_playback()
        time.sleep(0.5)  
        self.update_track_info()
        
    def next(self):
        # Skip to the next track
        sp.next_track()
        time.sleep(0.5)  
        self.update_track_info()
        
        
    def previous(self):
        # Skip to the previous track
        sp.previous_track() 
        time.sleep(0.5)       
        self.update_track_info()
        

if __name__ == "__main__":
    # Create main window
    root = tk.Tk()
    root.geometry("375x450")
    root.config(bg="#292929")
    root.resizable(False, False)
    # Create SpotifyController instance
    Pomodoro_instance = PomodoroTimer(root)
    Spotify_instance = SpotifyControlApp(root)
    root.mainloop()
# Start the main loop