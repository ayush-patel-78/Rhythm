# huehuehue....  project kaise chalu karu 
from cx_Oracle import *   # cx_oracle module is used to connect from oracle database
from traceback import *   # traceback module is used to help in debugging the code if some exceotion arises 
class Model:              # In model class we have to maintain the collection of songs selected by the user to play . In collection I have to keep 2 things song name and song location so I can store it in dictionary (song_dict). 
                          # In model class we will be providing adding and removing songs methods  from the collection as well as retriving song path corresponding to a given song name from collection .
                          # In model class we will be performing database intraction and also provides methods for adding , removing and loading songs from favourites
                          # huehuehue........
    def __init__(self) :
        self.song_dict={}    
        self.db_status=True  # db_status will tell us the status of database whteher DB is connected or not 
        self.conn=None
        self.cur=None
        try:
            self.conn=connect("mouzikka/music@127.0.0.1/xe") # connecting to database if db is not connected then it will throw an exception  DatabaseError and usko handle karna padega 
            print("Connected successfully to the DB")
            self.cur=self.conn.cursor()
        except DatabaseError:
            self.db_status=False
            print("DB Error:",format_exc())

    def get_db_status(self):      #  get_db_status() function will tell us the state of database whether it is connected or not 
        return self.db_status

    def close_db_connection(self):   # close_db_connection() function is used to close the connection from database 
        if self.cur is not None:     #first close the cursor and then after that close connection 
            self.cur.close()
            print("Cursor closed")
        if self.conn is not None:
            self.conn.close() 
            print("Disconnected successfully from the DB")

    def add_song(self,song_name,song_path):   # add_song() function se hum songs ko add karenge as the name indicates itself . 
        self.song_dict[song_name]=song_path
        print("Song added:",self.song_dict[song_name])

    def get_song_path(self,song_name):        # get_song_path() method will tell us song location from dictionary using song name.
        return self.song_dict[song_name]

    def remove_song(self,song_name):          # remove_song() method will remove the song from dictionary (collections)
        self.song_dict.pop(song_name)
        print("After deletion :",self.song_dict)

    def search_song_in_favourites(self,song_name):    # search_song_in_favourites() method will search the song from database and tells us whether the song is present in table or not 
        self.cur.execute("select song_name from myfavourites where song_name=:1",(song_name,))
        song_tuple=self.cur.fetchone()
        if song_tuple is None:
            return False
        return True


    def add_song_to_favourites(self,song_name,song_path):    # add_song_to_favourites() method will add the song in database table myfavourites but befor adding the song we will check whether the song is already present inside table or not ,if it is not present then we will insert it into table . in this method while inserting the song we are generating the song id from previous song id , if no songs is present inside the table then we will be providing song_id =1 to the song and if songs already present inside the table then we will take out the max song id from table and then increment it by 1 and insert the new song by allocating the incremented id to the song . 
        is_song_present=self.search_song_in_favourites(song_name)
        if is_song_present==True:
            return "Song already present in favourites"
        self.cur.execute("select max(song_id) from myfavourites")
        last_song_id=self.cur.fetchone()[0]
        next_song_id=1
        if last_song_id is not None:
            next_song_id=last_song_id+1
        self.cur.execute("insert into myfavourites values(:1,:2,:3)",(next_song_id,song_name,song_path))
        self.conn.commit()   # python ka autocommit off rehta hai isliye commit hamesha karna bro after executing DML statements
        return "Song successfully added to your favourites"
    
    def load_songs_from_favourites(self):       # load_songs_from_favourites this method is used to load the song from database. 
        self.cur.execute("select song_name,song_path from myfavourites")
        song_present=False
        for song_name,song_path in self.cur:      # cur ke ander list of tuples aaye hai toh apn ko data nikalna hai tuple se toh unpacking karni padegi tuples ki agr ek variale bas lenge toh pura tuple usme aa jayega but we want song_name and song_path both should come in different varibale therefore we are doing unpacking yeh idea pehle kiyun nhi aaya 🤔.
            self.song_dict[song_name]=song_path
            song_present=True
        if song_present:
            return "List populated from favourites"
        else:
            return "No songs present in your favourites"
    
    def remove_song_from_favourites(self,song_name): # remove_song from favourites this method will remove the song from database 
        self.cur.execute("Delete from myfavourites where song_name=:1",(song_name,))
        count=self.cur.rowcount
        if count==0:
            return "Song not present in ur favourites"
        else:
            self.song_dict.pop(song_name)   # song_name is key in dictionary and song_path is value 
            self.conn.commit()
            return "Song deleted from ur favourites"




            