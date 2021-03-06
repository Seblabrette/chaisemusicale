import os

from mutagen.mp3 import MP3


class Song:
    def __init__(self, path:str, tag:str):
        self.path = path
        self.tag = tag

    def load_song(self, mixer):
        mixer.music.load(self.path)

    def get_song_length(self):
        return MP3(self.path).info.length

    # def play_song(self,mixer):


class SongList1:
    songs = [
        Song("music/f3110144.mp3", "papa noel"),
        Song("music/f3118336.mp3", "ogres"),
        Song("music/f3125504.mp3", "monstres"),
        Song("music/f3132672.mp3", "interdits")
    ]

class SoundService:
    songlist = SongList1()
    songlist.songs = []#SongList1()
    def from_folder(self, path):
        self.songlist.songs = []
        for file in os.listdir(path):
            if file[-3:] == "mp3":
                title = file[:]
                self.songlist.songs.append(Song(path+"/"+file,title))

    def get_nb_songs(self):
        if not self.songlist.songs:
            return 0
        return len(self.songlist.songs)

    def playsong(self, index, mixer):
        self.songlist.songs[index].load_song(mixer)
        mixer.music.play(-1)
    def get_song_length(self,index):
        return self.songlist.songs[index].get_song_length()
