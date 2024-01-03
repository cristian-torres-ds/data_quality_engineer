import pandas as pd
import json

with open('taylor_swift_spotify.json', 'r') as file:
    data = json.load(file)

df1 = pd.json_normalize(data=data, record_path=['albums', 'tracks'], 
                        meta=['artist_id', 'artist_name', 'artist_popularity',
                             ['albums', 'album_id'], ['albums', 'album_name'],
                             ['albums', 'album_release_date'], ['albums', 'album_total_tracks']])

df1.rename(inplace=True,
           columns={"albums.album_id": "album_id",
                    "albums.album_name": "album_name",
                    "albums.album_release_date": "album_release_date",
                    "albums.album_total_tracks": "album_total_tracks"})

df1.to_csv('data_prueba.csv', index=False)