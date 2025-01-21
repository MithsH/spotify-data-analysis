from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re
import mysql.connector

connection = mysql.connector.connect(
    host = 'localhost',           
    user='root',       
    password='root', 
    database='spotify_db'
)

cursor = connection.cursor()

sp=spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='56a6e91ffe634c2da0caccd96d879b4c',
    client_secret='183564aa0b394d7bb0887e7db115dc87',
))    

file_path = "track_urls.txt" #create an txt file to fetch multiple data
with open(file_path, 'r') as file:
    track_urls = file.readlines()

for track_urls in track_urls:
    track_urls=track_urls.strip()
    try:
        track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

         track = sp.track(track_id)


         track_data = {
             'song_name': track['name'],
             'artist': track['artists'][0]['name'],
             'album': track['album']['name'],
             'popularitytrack': ['popularity'],
             'duration': track['duration_ms'] / 60000
         }


        insert_query = """
         INSERT INTO spotify_songs (song_name, artist, album, popularity, duration)
         VALUES (%s, %s, %s, %s, %s)
         """
         cursor.execute(insert_query, (
             track_data['song_name'],
             track_data['artist'],
             track_data['album'],
             track_data['popularity'],
            track_data['duration']
         ))
         connection.commit()

print(f"Track '{track_data['song_name']}' by {track_data['artist']} inserted into the database.")

cursor.close()
connection.close()

