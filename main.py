import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import schedule
import time
import logging
from datetime import datetime

# Configure logging to save output to spot.log
logging.basicConfig(filename='spot6.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# API keys and playlist ID
SPOTIFY_CLIENT_ID = 'your_spotify_id'
SPOTIFY_CLIENT_SECRET = 'your_client_secret'
SPOTIFY_REDIRECT_URI = 'http://localhost:8889/callback'  # Set this in your Spotify developer app
PLAYLIST_ID = 'your_playlist_id' # This is the string of the playlist in share

# Create global variables to store the access token and SpotifyOAuth instance
access_token = None
sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                       client_secret=SPOTIFY_CLIENT_SECRET,
                       redirect_uri=SPOTIFY_REDIRECT_URI,
                       scope="playlist-modify-public playlist-modify-private",
                       cache_path=".spotipy_cache")  # Specify a cache path

# Function to perform the script's actions
def perform_actions():
    global access_token

    # If the access token is not set or it's expired, obtain it
    if not access_token or is_token_expired():
        access_token = sp_oauth.get_access_token(as_dict=False)

    # Authenticate with Spotify using the access token
    sp = spotipy.Spotify(auth=access_token)

    # URL for the Random Quote API
    quote_api_url = 'https://api.quotable.io/quotes/random?tags=love'

    # Fetch a random quote
    response = requests.get(quote_api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        quote_data = response.json()
        content = quote_data[0]['content']
        author = quote_data[0]['author']

        # Get the current date and time
        current_datetime = datetime.now()

        # Format the date and time as hour-minute day-month
        formatted_datetime = current_datetime.strftime("%H:%M:%S %d-%m-%y")

        # Create a string to add to the Spotify playlist
        quote_to_add = f'"{content}" ~ {author} | Updated: {formatted_datetime}.'

        # Update the specified Spotify playlist with the new quote
        sp.playlist_change_details(playlist_id=PLAYLIST_ID, description=quote_to_add)
    else:
        error_message = "Failed to fetch a random quote."
        print(error_message)
        logging.error(error_message)

# Function to check if the access token is expired
def is_token_expired():
    token_info = sp_oauth.get_cached_token()
    if token_info:
        expires_at = token_info.get("expires_at")
        now = int(time.mktime(datetime.now().timetuple()))
        return expires_at - now < 60  # Check if it expires in less than 60 seconds
    return True

# Schedule the script to run every 1 minute
schedule.every(1).minutes.do(perform_actions) # Modify 1 to update in minutes

# Run the script indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep for 1 second to avoid excessive CPU usage
