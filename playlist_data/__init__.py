from dotenv import load_dotenv
from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ====
# AUTH
# ====

load_dotenv()
client_id = getenv("SPOTIPY_CLIENT_ID")
client_secret = getenv("SPOTIPY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)