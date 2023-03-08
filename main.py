import base64
import json
import textwrap
import urllib.parse
from copy import deepcopy

import credentials
import requests
from yt_dlp import YoutubeDL


class YouTubeSpotifyTransfer:
    def __init__(self):
        self.userId = credentials.spotifyUserID
        self.spotifyToken = credentials.spotifyToken
        self.spotifyPlayList = credentials.spotifPlayList
        self.allSongs = {}

    def getPlayListSongs(self):
        youtube_playlist = ""
        playlist_dict = YoutubeDL(
            {"ignoreerrors": True, "parse-metadata": "title:%(artist)s - %(title)s"}).extract_info(youtube_playlist,
                                                                                                   download=False)
        for video in playlist_dict["entries"]:
            print("\n" + "*" * 60 + "\n")
            if not video:
                print("ERROR: Unable to get info. Continuing...")
                continue
            else:
                try:
                    video_title = video['title']
                    video_url = video['webpage_url']
                    self.allSongs[video_title] = {
                        "youtubeURl": video_url,
                        "spotifyURI": self.searchSong(video_title)
                    }
                except:
                    print("S-a intamplat o eroare")

        # print(playlist_dict.keys(), end='\n')
        print(playlist_dict['title'])
        for i in self.allSongs:
            print(i)

    def createPlayList(self):
        """
        Add the manual name , description and public settings
        """
        request_body = json.dumps(
            {
                "name": "HEHEHE",
                "description": "New playlist description",
                "public": True
            }
        )
        querry = f"https://api.spotify.com/v1/users/{self.userId}/playlists"
        response = requests.post(
            querry,
            data=request_body,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotifyToken)
            }
        )
        responseJson = response.json()
        # print(response, end='\n')
        # print(responseJson)
        return responseJson["id"]

    def searchSong(self, songName):
        # querry = f"https://api.spotify.com/v1/search?q={artistName}+{songName}&type=track%2Cartist&market=US&limit=10&offset=5"
        # querry = f"https://api.spotify.com/v1/search?q={songName}+{artistName}&type=track&market=KR&limit=20&offset=10"
        # querry = f"https://api.spotify.com/v1/search?q=track%3A{songName}+artist%3A{artistName}&type=track&market=KR&limit=20&offset=0"
        # songName = songName.replace("'","")
        songName_encoded = urllib.parse.quote(songName.encode('utf8'))
        querry = f"https://api.spotify.com/v1/search?q={songName_encoded}&type=track&limit=20&offset=0"
        response = requests.get(querry, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotifyToken),
        })
        if response.status_code not in range(200, 299):
            raise Exception("Not found!")
        responseJson = response.json()
        print(responseJson)
        songs = responseJson["tracks"]["items"]
        uri = songs[0]["uri"]
        # print(uri)
        return uri

    def addSongToPlayList(self):
        pass

    def findAll(self):
        querry = "https://api.spotify.com/v1/playlists/{}/tracks".format(self.spotifyPlayList)
        response = requests.get(querry, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotifyToken)
        })
        responseJson = response.json()
        print(response)

    def addSongsToPlaylist(self):
        self.getPlayListSongs()
        uris = []
        for songs, info in self.allSongs.items():
            uris.append(info['spotifyURI'])

        playlistId = self.createPlayList()
        request_data = json.dumps(uris)
        query = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotifyToken)
            }
        )
        responseJson = response.json()
        return responseJson


if __name__ == '__main__':
    YouTubeSpotifyTransfe = YouTubeSpotifyTransfer()
    # YouTubeSpotifyTransfe.createPlayList()
    # YouTubeSpotifyTransfe.createPlayList()
    # YouTubeSpotifyTransfe.searchSong("BTS (방탄소년단) 'FAKE LOVE' Official MV")
    # YouTubeSpotifyTransfe.getPlayListSongs()
    # YouTubeSpotifyTransfe.getPlayListSongs()
    YouTubeSpotifyTransfe.addSongsToPlaylist()
