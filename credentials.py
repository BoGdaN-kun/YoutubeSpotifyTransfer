import base64
import datetime
import json
import requests
from tokens import spotifyUserID_secret, client_id_secret, client_secret_secret, \
    spotifPlayList_secret, redirect_uri_secret

spotifyUserID = spotifyUserID_secret
spotifPlayList = spotifPlayList_secret
client_id = client_id_secret
client_secret = client_secret_secret



class SpotifyApi(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expires = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_credentials = f"{client_id}:{client_secret}"
        client_credentials_base64 = base64.b64encode(client_credentials.encode())
        return client_credentials_base64.decode()

    def get_token_headers(self):
        client_credentials_base64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_credentials_base64}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials",
            "scope": "playlist-modify-public playlist-modify-private user-read-private user-library-modify playlist-read-private"
        }

    def perform_auth(self):
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        token_url = self.token_url
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("could not authentificate")
            # return False
        data = r.json()
        access_token = data['access_token']
        expires_in = data['expires_in']
        now = datetime.datetime.now()
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expires = expires < now
        self.access_token = access_token

        return True

    def get_access_token(self):
        auth_done = self.perform_auth()
        if not auth_done:
            raise Exception("Authentification failed")
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        return token


spotify = SpotifyApi(client_id, client_secret)
spotify.perform_auth()

print(spotify.access_token)
spotifyToken = spotify.access_token

redirect_uri = redirect_uri_secret

auth = "https://accounts.spotify.com/authorize"

from base64 import b64encode

url = 'https://accounts.spotify.com/api/token'

header = spotify.get_token_headers()

data = {
    'grant_type': 'authorization_code',
    'code': "codeFROM_URI",
    'redirect_uri': redirect_uri,
    'scope': "playlist-modify-public playlist-modify-private user-read-private user-library-modify playlist-read-private"}
