"""This module is realised to map available markets for the most
popular song of the specified artist.

This module works with json file which is obtained using the Spotify API.
The input is the name of the artist. The module has to find the most popular
of artist's song and then find all available markets for this song and map them.

link to github: https://github.com/yarkapetruniv/Spotify_0.git
"""
import os
import base64
import json
import folium
import pycountry
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from requests import post, get
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    """
    This function should access token, which is used to
    make API calls on behalf the user or application.
    """
    authorization_str = client_id + ":" + client_secret
    authorization_bytes = authorization_str.encode('utf-8')
    authorization_base64 = str(base64.b64encode(authorization_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + authorization_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data, timeout=1.5)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_authorization_header():
    """
    This function is created to get authorization header
    everytime you have to find some new information using token.
    """
    return {"Authorization": "Bearer " + get_token()}


def search_for_artist(name: str) -> tuple:
    """
    This function input is the artist name. The function
    has to return the tuple that consists of artist name and
    artist ID.
    >>> search_for_artist("Miley Cyrus")
    ('Miley Cyrus', '5YGY8feqx7naU7z4HrwZM6')
    >>> search_for_artist("Жадан і Собаки")
    ('Zhadan i Sobaky', '2Reqc0B9PCsI6t78c9k11o')
    """
    url = "https://api.spotify.com/v1/search"
    query = f"?q={name}&type=artist&limit=1"

    query_url = url + query
    headers = get_authorization_header()
    result = get(query_url, headers = headers, timeout = 1.5)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("There is no artist with this name...")
        return None
    return json_result[0]["name"], json_result[0]["id"]


def get_song(artist_id: str) -> str:
    """
    This function should return the most popular song of the
    artist using artist's ID.
    >>> get_song('5YGY8feqx7naU7z4HrwZM6')
    'Flowers'
    >>> get_song('7Ln80lUS6He07XvHI8qqHH')
    'I Wanna Be Yours'
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    query = "?country=US"

    query_url = url + query
    headers = get_authorization_header()
    result = get(query_url, headers = headers, timeout = 1.5)
    json_result = json.loads(result.content)["tracks"]
    return json_result[0]["name"]


def get_available_markets(song, artist_id):
    """
    This function should return all countries where you can listen
    to the most popular song of the artist. It finds information about
    a song by its name and then checks that this song was written by the
    appropriate artist.
    >>> get_available_markets('Summertime Sadness', '00FQb4jTyendYWaN8pK0wa')[:15]
    ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO']
    """
    url = "https://api.spotify.com/v1/search"
    query = f"?q={song}&type=track"

    query_url = url + query
    headers = get_authorization_header()
    result = get(query_url, headers = headers, timeout = 1.5)
    json_result = json.loads(result.content)["tracks"]['items']
    for element in json_result:
        for artists in element["artists"]:
            if artists["id"] == artist_id:
                return element["available_markets"]
    return None


def create_map(markets: list, name: str, song: str):
    """
    Create a map.
    """
    html = """<h3>{}</h3>
    <h4>Information about song:</h4>
    Name: {}<br>
    Artist: {}
    """
    map = folium.Map(location = [39, 34], zoom_start = 2, tiles = "stamenwatercolor")
    layer = folium.FeatureGroup(name = f'Markets for {song}')
    for market in markets:
        geolocator = Nominatim(user_agent = "MyProject")
        # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        country = pycountry.countries.get(alpha_2 = market)
        if country:
            location = RateLimiter(geolocator.geocode, min_delay_seconds=1)(market)
            if location is not None:
                iframe = folium.IFrame(html=html.format(country.name, song, name),
                                    width=300, height=100)
                layer.add_child(folium.Marker(location = [location.latitude, location.longitude],
                                            popup=folium.Popup(iframe), icon=folium.Icon(color = 'black', icon = 'music')))
            else:
                continue
        else:
            continue
    
    map.add_child(layer)
    map.add_child(folium.LayerControl())
    map.save("templates/My_map.html")
