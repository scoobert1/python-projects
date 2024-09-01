import subprocess
from bs4 import BeautifulSoup
import requests
from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyOAuth

command = "ytmusicapi oauth"
subprocess.run(command, shell=True, capture_output=True, text=True)
ytmusic = YTMusic("oauth.json")




#!!!!!!!!!!!!!!!
client_id = ''
client_secret = ''
redirect_uri = 'http://localhost:8888/callback'
scope = 'playlist-read-private'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))


def spoti_to_yt(playlist_url):
    page = requests.get(playlist_url)
    soup = BeautifulSoup(page.text, "html.parser")
    soup = soup.find('h1').get_text(strip=True)

    playlistID = ytmusic.create_playlist(soup,"")



    playlist_id = playlist_url.split('/')[-1].split('?')[0]


    results = sp.playlist_tracks(playlist_id)

    tracks = results['items']


    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])


    for idx, item in enumerate(tracks):
        track = item['track']
        #print(f"{idx + 1}. {track['name']} - {track['artists'][0]['name']}")
        #while search['artists']['name']!=track['artists']:
        search = ytmusic.search(f"{track['name']} - {track['artists'][0]['name']}", 'songs', None, 20, True)[0]
        ytmusic.add_playlist_items(playlistID, [search['videoId']])
        print(f"{track['name']} - {track['artists'][0]['name']}")

if __name__ == "__main__":
    playlist_url = input("Paste Spotify url: ")
    spoti_to_yt(playlist_url)