#//////////////////////////////////////////IMPORTING MODULES/////////////////////////////////////////////////////////

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
load_dotenv()

#//////////////////////////////////////////DEFINING VARIABLES/////////////////////////////////////////////////////////


SPOTIFY_TOKEN=os.getenv("SPOTIFY_TOKEN")
USER_ID=os.getenv("USER_ID")
SPOTIFY_ENDPOINT="https://api.spotify.com/v1"
SEARCH_ENDPOINT=SPOTIFY_ENDPOINT+"/search"
BASE_URL="https://www.billboard.com/charts/hot-100/"
PLAYLIST_URL=SPOTIFY_ENDPOINT+"/users/"+USER_ID+"/playlists"
SONGS=[]
SONGS_ID=[]

#//////////////////////////////////////////WEBSCRAPING TO FIND SONGS ON THE PARTICULAR DATE GIVEN BY USER /////////////////////////////////////////////////////////

date=input("Which date's  song you wanna add to you playlist? Please enter the date in YYYY-MM-DD\n")
DATE_URL=BASE_URL+str(date)
response=requests.get(DATE_URL)
soup=BeautifulSoup(response.text,"html.parser")
result=soup.findAll('div',{'class':'o-chart-results-list-row-container'})

#//////////////////////////////////////////HEADERS FOR THE SEARCH REQUEST & CREATING PLAYLIST/////////////////////////////////////////////////////////
api_header={
    "Authorization": f"Bearer {SPOTIFY_TOKEN}"
}
play_list_header={
    "Authorization": f"Bearer {SPOTIFY_TOKEN}",
    "Content-Type": "application/json"
    
}
#//////////////////////////////////////////CREATING A PLAYLIST/////////////////////////////////////////////////////////
playlist_data={
  "name": "TODAY'S_NEWPLAYLIST",
  "description": "Dive into nirvana with us",
  "public": 'False'
}
play_data=requests.post(PLAYLIST_URL,json=playlist_data,headers=play_list_header)
PLAY_ID=play_data.json()['id']
#//////////////////////////////////////////LOOPING THRIUGH EACH SONG AND ADDING THEM INTO PLAYLIST CREATED ABOVE/////////////////////////////////////////////////////////
for x,y in enumerate(result):
    nxt=y.find('h3',{'id':'title-of-a-story'}).getText().strip()
    SONGS.append(nxt)
    api_data=urlencode({
        'q':SONGS[x],
        'type':"track"
    })
    Search_url=f"{SEARCH_ENDPOINT}?{api_data}"
    SONG_data=requests.get(Search_url,headers=api_header)
    data=SONG_data.status_code
    if data==200:
        SONGS_ID.append(SONG_data.json()['tracks']['items'][0]['uri'])
        add_data=urlencode({
                "uris":SONGS_ID[x].strip()})
        ADD_END=SPOTIFY_ENDPOINT+"/playlists/"+PLAY_ID+"/tracks?"
        F_ADD=f"{ADD_END}{add_data}"
        add_play=requests.post(F_ADD,headers=play_list_header)
    else:
        print(f"{SONGS[x]} is not available on spotify so it is not going to add.")

