from mutagen import mp3
import Model                         # importing Model.py file 
from pygame import mixer             # explicitly importing mixer 
from tkinter import filedialog       # importing filedialog for opening dialog box from player 
import os                            # importing os module . It will provide us filename from full path of file . we can also use string handling to take out the filename but for simplicity we are using os module. 
from mutagen.mp3 import MP3          # MP3 module will provide us ID3 Tag which will give us length ,genre,singer blah blah blah.....   hehe hehe...

# hehe..... 
# The player module primarily has 2 tasks:
# 1. Managing the media playes functionality 
# 2. Interacting with the Model class

class Player:  # This class will have to do the following tasks:
               #  it will initialize the pygame.mixer module which will provides us several functions to handle music playing and management (pygame.mixer provides instance methods for playing , stopping , pausing and resume a song )
        def __init__(self) :
            mixer.init()                # initializing mixer 
            self.my_model=Model()       # instantiating model 

        def get_db_status(self):
            return self.my_model.get_db_status()

        def close_player(self):
            mixer.music.stop()      # this will stop the music by calling the stop method from mixer.music 
            self.my_model.close_db_connection()
        
        def set_volume(self,volume_level):
            mixer.music.set_volume(volume_level)            # set_volume method from mixer.music will set the volume level which will be passed from view.py module 

        def add_song(self):
            song_path=filedialog.askopenfilename(title="Select ur song...",filetypes=[("mp3 files","*.mp3")])
            if song_path=="":
                return
            song_name=os.path.basename(song_path)
            self.my_model.add_song(song_name,song_path)     #add_song method of model is called to add song in database
            return song_name                                # song name is passed to view.py

        def remove_song(self,song_name):
            self.my_model.remove_song(song_name)
        
        def get_song_legth(self,song_name):                 # this method will give us length of the song and pass it to the view module 
            self.song_path=self.my_model.get_song_path(song_name)
            self.audio_tag=MP3(self.song_path)
            song_length=self.audio_tag.info.length
            return song_length

        def play_song(self):           # As the name indicates itself it will play song 
            mixer.quit()
            mixer.init(frequency=self.audio_tag.info.sample_rate)  # frequency propert will decide the playbackspeed of song if we dont pass it then song will sometimes play fast and sometimes slow .
            mixer.music.load(self.song_path)
            mixer.music.play()
        
        def stop_song(self):
            mixer.music.stop()   # it will stop the song 
        
        def pause_song(self):
            mixer.music.pause()   # it will pause the song 
        
        def unpause_song(self):
            mixer.music.unpause()  # it will resume/unpause the song 

        def add_song_to_favourites(self,song_name):              # this method is calling add_song_to_favourites methods of model module from model object just acting as a bridge between view and model 
            song_path=self.my_model.get_song_path(song_name)
            result=self.my_model.add_song_to_favourites(song_name,song_path)
            return result

        def load_songs_from_favourites(self):                     # this method is calling load_song method of model from model object .
            result=self.my_model.load_song_from_favourites()
            return result,self.my_model.song_dict

        def remove_song_from_favourites(self,song_name):          # this method is calling remove_song_from_favourites method of model from model object .
            result=self.my_model.remove_song_from_favourites(song_name)
            return result
