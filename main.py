"""Create the web app.

The user enters the name of the artist, and
the program has to give him a map on which all the countries
where you can listen to the most popular song of this author are marked.
To create this app we use module main.py, which takes the name of the artist,
searches for the necessary information and creates a map. To design this app
the module uses html files and css file.

link to github: 
"""
from flask import Flask, render_template, request
import my_map

app = Flask(__name__)

@app.route('/search4', methods = ['POST'])
def do_search():
    """
    This function processes the data entered by the user and creates a map.
    """
    artist = request.form['Artist name']
    artist_name = my_map.search_for_artist(artist)[0]
    artist_id = my_map.search_for_artist(artist)[1]
    most_popular_song = my_map.get_song(artist_id)
    available_markets = my_map.get_available_markets(most_popular_song, artist_id)
    my_map.create_map(available_markets, artist_name, most_popular_song)
    return render_template('My_map.html')

@app.route('/')
@app.route('/entry')
def entry_page():
    """
    This function creates the entry page using html file.
    """
    return render_template('entry.html')

if __name__ == "__main__":
    app.run(debug = True)
