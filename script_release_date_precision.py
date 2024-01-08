import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# credenciales
client_id = '******************************'
client_secret = '******************************'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist_name = 'Taylor Swift'

artist_results = sp.search(q=f'artist:{artist_name}', type='artist')
artist_id = artist_results['artists']['items'][0]['id']

albums = sp.artist_albums(artist_id, album_type='album', limit=50)

album_info_list = []

for album in albums['items']:
    album_info = {
        "id": album['id'],
        "name": album['name'],
        "release_date": album['release_date'],
        "release_date_precision": album['release_date_precision'],
    }
    album_info_list.append(album_info)

# Guardar la información de los álbumes en un archivo JSON
with open('release_date_precision.json', 'w') as json_file:
    json.dump(album_info_list, json_file, indent=4)