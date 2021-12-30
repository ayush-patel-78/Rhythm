# hehe..... 
# The player module primarily has 2 tasks:
# 1. Managing the media playes functionality 
# 2. Interacting with the Model class

import Model                         # importing Model.py file 
from pygame import mixer             # explicitly importing mixer 
from tkinter import filedialog       # importing filedialog for opening dialog box from player 
import os                            # importing os module . It will provide us filename from full path of file . we can also use string handling to take out the filename but for simplicity we are using os module. 
from mutagen.mp3 import MP3          # MP3 module will provide us ID3 Tag which will give us length ,genre,singer blah blah blah.....   hehe hehe...

class Player:  # This class will have to do the following tasks:
               #  it will initialize the pygame.mixer module which will provides us several functions to handle music playing and management (pygame.mixer provides instance methods for playing , stopping , pausing and resume a song )
        def __init__(self) :
            mixer.init()                # initializing mixer 
            self.my_model=Model()       # instantiating model 

        def get_db_status(self):
            return self.my_model.get_db_status()

        def close_player(self):
            mixer.music.stop()      # this will stop the music 
            self.my_model.close_db_connection()
        
        def set_volume(self,volume_level):
            mixer.music.set_volume(volume_level)            # set_volume method from mixer.music will set the volume level which will be passed from view.py module 
