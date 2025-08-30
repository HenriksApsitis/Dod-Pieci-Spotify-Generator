import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from tqdm import tqdm

# Replace with your own credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="ENTER YOUR CLIENT ID",
    client_secret="ENTER YOUR SECRET",
    redirect_uri="http://127.0.0.1:8889/callback",
    scope="playlist-modify-public"
))
playlist_name = "ENTER YOUR PLAYLIST NAME HERE"

# --- 1. Load CSV ---
df = pd.read_csv("songs.csv", header=None, names=["Number", "Track"])
print(df.head())

track_uris = []

# --- 2. Split into artist + title ---
for track in tqdm(df["Track"], desc="Searching tracks", unit="song"):
    if " - " in track:
        artist, title = track.split(" - ", 1)  # split only on first dash
    else:
        artist, title = "", track  # fallback if no dash found

    # --- 3. Search more accurately ---
    query = f"track:{title} artist:{artist}"
    result = sp.search(q=query, type="track", limit=1)

    if result["tracks"]["items"]:
        uri = result["tracks"]["items"][0]["uri"]
        track_uris.append(uri)
        print(f"✅ Found: {artist} - {title}")
    else:
        print(f"❌ Not found: {artist} - {title}")

# --- 4. Create Playlist ---
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
playlist_id = playlist["id"]

# --- 5. Add tracks in batches of 100 (Spotify limit) ---
for i in range(0, len(track_uris), 100):
    sp.playlist_add_items(playlist_id, track_uris[i:i + 100])

print("Playlist created:", playlist["external_urls"]["spotify"])
