from random import randint

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty, Clock, ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from sound_service import SoundService
from pygame import mixer
import time

mixer.init()

class MainWidget(BoxLayout):
    TEMPS_MIN = 2
    TEMPS_MAX = 5
    NB_JOUEURS_MIN = 2
    NB_JOUEURS_MAX = 10
    selected_song_tag = StringProperty("choisir un titre")
    play_button = ObjectProperty()
    resume_button = ObjectProperty()
    select_button = ObjectProperty()
    plus_button = ObjectProperty()
    minus_button = ObjectProperty()
    nb_joueurs = NumericProperty(NB_JOUEURS_MIN)
    selected_song_index = -1
    selected_song_length = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = 0
        self.is_paused = False
        self.soundservice = SoundService()
        # self.soundservice.from_folder('C:/Users/spouvreau/Documents/00_PERSO/Musiques_enfants/recup_dir.3')
        self.soundservice.from_folder('C:/Users/spouvreau/Documents/00_PERSO/MP3/Pop/Emma')
        self.nb_songs = self.soundservice.get_nb_songs()
        print("nombre de chansons: " + str(self.nb_songs))

        self.dropdownbox = BoxLayout()
        self.dropdownbox.size_hint_x = None
        self.dropdownbox.width = dp(200)
        self.add_widget(self.dropdownbox)
        self.dropdown = DropDown()
        for i in range(self.nb_songs):
            btn = Button()
            btn.text = self.soundservice.songlist.songs[i].tag
            btn.size_hint_y = None
            btn.height = dp(20)
            btn.bind(on_release=self.select_song)
            self.dropdown.add_widget(btn)
        self.mainbutton = Button(text='selectionner', size_hint=(None, None), width=dp(200), height=dp(20),
                                 pos_hint={'x': 0.8, 'top': 1})
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.dropdownbox.add_widget(self.mainbutton)

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
        print("Start time: " + str(self.start_time))
        self.event = Clock.schedule_interval(self.random_stop, (self.TEMPS_MAX-self.TEMPS_MIN) / 30.)

    def press_resume(self):
        if self.is_paused:
            mixer.music.unpause()
            self.start_time = time.time()
            print("RESUME")
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
        if temps_ecoule > self.TEMPS_MIN and not self.is_paused:
            if randint(0, 1000) > 995 or temps_ecoule > self.TEMPS_MAX:
                #on est dans le cas où on met la musique en pause
                print("temps_ecoule: "+str(temps_ecoule))
                self.resume_button.disabled = False
                mixer.music.pause()
                self.is_paused = True
                if self.nb_joueurs > self.NB_JOUEURS_MIN:
                    self.remove_player()
                else:
                    self.press_stop()

    def remove_player(self):
        if self.nb_joueurs > self.NB_JOUEURS_MIN:
            self.nb_joueurs -= 1

    def add_player(self):
        if self.nb_joueurs < self.NB_JOUEURS_MAX:
            self.nb_joueurs += 1

    print("mixer" + str(mixer.get_init()))

class MonAppliApp(App):
    pass




MonAppliApp().run()
