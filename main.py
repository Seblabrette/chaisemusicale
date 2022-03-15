from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from sound_service import SoundService
from pygame import mixer
import time

mixer.init()

class MainWidget(BoxLayout):
    selected_song_tag = StringProperty("choisir un titre")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_paused = False
        self.soundservice = SoundService()
        self.nb_songs = self.soundservice.get_nb_songs()
        print("nombre de chansons: " + str(self.nb_songs))

        self.dropdownbox = BoxLayout()
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
        # Lecture du son sélectionné
        # for i in range(self.nb_songs):
        #     if widget.text == self.soundservice.songlist.songs[i].tag:
        #         self.soundservice.playsong(i, mixer)

    def on_parent(self, widget, parent):
        pass

    def press_play(self):
        if self.selected_song_tag == "choisir un titre":
            print("Pas de chanson sélectionnée")
            return None
        print("PLAY")
        # Lecture du son sélectionné
        for i in range(self.nb_songs):
            if self.selected_song_tag == self.soundservice.songlist.songs[i].tag:
                self.soundservice.playsong(i, mixer)
                self.is_paused = False

    def press_pause_resume(self):
        if self.selected_song_tag == "choisir un titre":
            print("Pas de chanson sélectionnée")
            return None
        if self.is_paused:
            mixer.music.unpause()
            print("RESUME")
            self.is_paused = False
        else:
            mixer.music.pause()
            print("PAUSE")
            self.is_paused = True


    def press_stop(self):
        if self.selected_song_tag == "choisir un titre":
            print("Pas de chanson sélectionnée")
            return None
        print("STOP")
        # Arrêt du son en cours de lecture
        mixer.music.stop()


    print("mixer" + str(mixer.get_init()))

class MonAppliApp(App):
    pass


MonAppliApp().run()
