from kivy import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '250')
Config.set('graphics', 'minimum_width', '500')
Config.set('graphics', 'minimum_height', '250')

# from kivy.core.window import Window
# Window.clearcolor = (1, 1, 1, 1)

import random
from random import randint

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty, Clock, ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.utils import platform

from sound_service import SoundService
from pygame import mixer
import time

mixer.init()

class FileChoosePopup(Popup):
    load = ObjectProperty()
    DEFAULT_PATH = StringProperty("")#("C:\\Users\\spouvreau\\Documents\\00_PERSO\\MP3")
    if platform == "win":
        DEFAULT_PATH = "C:\\"
    elif platform == "android":
        DEFAULT_PATH = "\\"

class MainWidget(BoxLayout):
    TEMPS_MIN = 5
    TEMPS_MAX = 30
    NB_JOUEURS_MIN = 4
    NB_JOUEURS_MAX = 10
    selected_song_tag = StringProperty("choisir un titre")
    play_button = ObjectProperty()
    resume_button = ObjectProperty()
    select_button = ObjectProperty()
    plus_button = ObjectProperty()
    minus_button = ObjectProperty()
    nb_joueurs = NumericProperty(NB_JOUEURS_MIN)

    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)

    selected_song_index = -1
    selected_song_length = 0
    compteur = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = 0
        self.is_paused = False
        self.soundservice = SoundService()
        self.nb_songs = self.soundservice.get_nb_songs()
        print("nombre de chansons: " + str(self.nb_songs))

        self.box_left = BoxLayout(orientation="horizontal",
                                  size_hint_y=None,
                                  height=dp(40))
        self.add_widget(self.box_left)
        self.folder_select_button = Button(text="",
                                  size_hint_x=None,
                                  width=dp(150))
        self.folder_select_button.border= (0, 0, 0, 0)
        self.folder_select_button.background_normal = "images/button_folder_normal.png"
        self.folder_select_button.background_down = "images/button_folder_down.png"
        self.folder_select_button.bind(on_release=self.open_popup)
        self.box_left.add_widget(self.folder_select_button)


        self.dropdownbox = BoxLayout()
        # self.dropdownbox.size_hint_x = None
        # self.dropdownbox.width = dp(200)
        self.box_left.add_widget(self.dropdownbox)
        self.dropdown = DropDown()
        self.mainbutton = Button(text='Select Song')
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.dropdownbox.add_widget(self.mainbutton)

    def open_popup(self, widget):
        self.the_popup = FileChoosePopup(load=self.load_btn_popup)
        self.the_popup.open()

    def load_btn_popup(self, selection):
        if selection[-4] == ".":
            split = selection.split("\\")
            self.file_path = "\\".join(split[:-1])
        else:
            self.file_path = selection
        # self.file_path = str(path)
        self.the_popup.dismiss()
        print(self.file_path)
        self.update_dropdown_list(self.file_path)

    def update_dropdown_list(self,filepath):
        print("update dropdown menu")
        self.dropdown.clear_widgets()
        self.soundservice.from_folder(filepath)
        self.nb_songs = self.soundservice.get_nb_songs()
        for i in range(self.nb_songs):
            btn = Button()
            btn.text = self.soundservice.songlist.songs[i].tag
            btn.size_hint_y = None
            btn.height = dp(20)
            btn.bind(on_release=self.select_song)
            self.dropdown.add_widget(btn)
        self.mainbutton.text = "Select Song"

    def select_song(self, widget):
        self.dropdown.select(widget.text)
        self.selected_song_tag = widget.text
        self.play_button.disabled = False
        # Stockage de l'index du son sélectionné
        for i in range(self.nb_songs):
            if widget.text == self.soundservice.songlist.songs[i].tag:
                self.selected_song_index = i
                break
        self.selected_song_length = self.soundservice.get_song_length(self.selected_song_index)

    def press_play(self):
        print("PLAY")
        self.play_button.disabled = True
        self.stop_button.disabled = False
        self.plus_button.disabled = True
        self.minus_button.disabled = True
        # Lecture du son sélectionné
        self.soundservice.playsong(self.selected_song_index, mixer)
        self.is_paused = False
        self.start_time = time.time()
        self.play_time = self.TEMPS_MIN + random.random() * (self.TEMPS_MAX-self.TEMPS_MIN)
        print("Start time: " + str(self.start_time))
        print("Play time: " + str(self.play_time))
        self.event = Clock.schedule_interval(self.random_stop, 1 / 30.)

    def press_resume(self):
        if self.is_paused:
            mixer.music.unpause()
            self.resume_button.disabled = True
            self.start_time = time.time()
            self.play_time = self.TEMPS_MIN + random.random() * (self.TEMPS_MAX - self.TEMPS_MIN)
            print("RESUME")
            print("Start time: " + str(self.start_time))
            print("Play time: " + str(self.play_time))
            self.is_paused = False
        else:
            print("Le titre joue déjà")

    def press_stop(self):
        self.play_button.disabled = False
        self.stop_button.disabled = True
        self.resume_button.disabled = True
        self.plus_button.disabled = False
        self.minus_button.disabled = False
        print("STOP")
        if self.event is not None:
            Clock.unschedule(self.event)
        # Arrêt du son en cours de lecture
        mixer.music.stop()
        self.is_paused = True

    def random_stop(self,dt):
        temps_ecoule = time.time() - self.start_time
        if temps_ecoule > self.play_time and not self.is_paused:
            #on est dans le cas où on met la musique en pause
            print("temps_ecoule: "+str(temps_ecoule))
            self.resume_button.disabled = False
            mixer.music.pause()
            self.is_paused = True
            if self.nb_joueurs > 2:
                self.remove_player()
            else:
                self.press_stop()

    def remove_player(self):
        if self.nb_joueurs > 2:
            self.nb_joueurs -= 1

    def add_player(self):
        if self.nb_joueurs < self.NB_JOUEURS_MAX:
            self.nb_joueurs += 1

    print("mixer" + str(mixer.get_init()))


class MonAppliApp(App):
    pass


MonAppliApp().run()
