import json
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# credenciales
client_id = '58667cb1a00e4fda844b6ec55503a98d'
client_secret = '7851c1ffcf054214bf2731d4bb8b0b57'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist_name = 'Taylor Swift'

artist_results = sp.search(q=f'artist:{artist_name}', type='artist')
artist_id = artist_results['artists']['items'][0]['id']

albums = sp.artist_albums(artist_id, album_type='album', limit=50)

complete_info = {"artist": {"id": artist_id, "name": artist_name}, "albums": []}

for album in albums['items']:
    album_id = album['id']
    album_info = {"id": album_id, "name": album['name'], "release_date": album['release_date'], "tracks": []}

    tracks = sp.album_tracks(album_id)

    for track in tracks['items']:
        track_id = track['id']

        audio_features = sp.audio_features(track_id)[0]

        track_info = {
            "id": track_id,
            "name": track['name'],
            "disc_number": track['disc_number'],
            "duration_ms": track['duration_ms'],
            "explicit": track['explicit'],
            "track_number": track['track_number'],
            "audio_features": {
                "danceability": audio_features['danceability'],
                "energy": audio_features['energy'],
                "key": audio_features['key'],
                "loudness": audio_features['loudness'],
                "mode": audio_features['mode'],
                "speechiness": audio_features['speechiness'],
                "acousticness": audio_features['acousticness'],
                "instrumentalness": audio_features['instrumentalness'],
                "liveness": audio_features['liveness'],
                "valence": audio_features['valence'],
                "tempo": audio_features['tempo'],
                "time Signature": audio_features['time_signature'],
                "id": audio_features['id']
            },
            "artist": {
                "id": artist_id,
                "name": artist_name,
                "popularity": artist_results['artists']['items'][0]['popularity']
            },
            "album": {
                "id": album_id,
                "name": album['name'],
                "release_date": album['release_date'],
                "total_tracks": album['total_tracks']
            }
        }

        album_info["tracks"].append(track_info)

    complete_info["albums"].append(album_info)

with open('consulta_actual.json', 'w') as json_file:
    json.dump(complete_info, json_file, indent=4)

# Asignamos el contenido del archivo .json a la variable data
with open('consulta_actual.json', 'r') as file:
    data = json.load(file)

# Usamos los parámetros "record_path" para acceder a la información anidada
# y "meta" para las demas columnas que queremos extraer.
df1 = pd.json_normalize(data=data, record_path=['albums', 'tracks'], 
                        meta=[['albums', 'id'], ['albums', 'name'],
                             ['albums', 'release_date']])

df1.to_csv('consulta_actual.csv', index=False)