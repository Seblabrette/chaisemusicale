from pygame import mixer


class Song:
    def __init__(self, path:str, tag:str):
        self.path = path
        self.tag = tag

    def load_song(self, mixer):
        mixer.music.load(self.path)
    # def play_song(self,mixer):


class SongList1:
    songs = (
        Song("music/f3110144.mp3", "papa noel"),
        Song("music/f3118336.mp3", "ogres"),
        Song("music/f3125504.mp3", "monstres"),
        Song("music/f3132672.mp3", "interdits")
    )

class SoundService:
    songlist = SongList1()
    def get_nb_songs(self):
        return len(self.songlist.songs)
    def playsong(self, index, mixer):
        self.songlist.songs[index].load_song(mixer)
        mixer.music.play()

# mixer.init()
# songlist = SongList1().songs
#
# for i in range(len(songlist)):
#     songlist[i].load_song(mixer)
#     print("chanson: " + songlist[i].tag)
#     mixer.music.play()
#     input()
