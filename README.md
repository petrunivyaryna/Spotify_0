# Spotify_2
## About the project
I created my web application, where the user has to enter the name of the artist, and he will be given a map, in which all the countries where you can listen to the most popular song of this artist will be marked.
### How the app works?
To develop a web application I created two python files:
* **my_map.py** (does all the technical work: getting a token from spotify, looking for an artist id, his most popular song and all available markets. Then it creates a map)
* **main.py** (creates a web application using flask framework)

Also I added the html file, which is called **entry.html**. It builds an entrance page.
To design the entrance page I also created the **hf.css** file.

## Example
Here the user needs to enter the name of the artist:
![image](https://user-images.githubusercontent.com/116542027/221881792-76d778c9-734d-42cb-acb1-58f4e27fc6f3.png)

Output:
![image](https://user-images.githubusercontent.com/116542027/221882750-e10eccfc-14ce-41a1-a0d4-0aa7ea061242.png)

![image](https://user-images.githubusercontent.com/116542027/221883538-33fc8a7b-39f8-4d4b-a995-7bc632c367e8.png)

**In order for the program to work faster, only 100 locations are displayed on the maps, if there are actually more.**

## Pythonanywhere
I posted my program on Pythonanywhere.
Here is the link to my program: http://yarynapetruniv.pythonanywhere.com/

## Built with
To create this module I used lots of modules such as:
* os (to get client id and client secret from .env file)
* base64 (to get the token)
* json (to get the information from json file)
* requests (to get the information from Spotify)
* dotenv
* folium (to create a map)
* pycoutry (to get the name of the countries)
* geopy (to define coordinates)
* flask (to creaet the web application)

All modules that need to be installed to use my program are in the file **requirements.txt**.
