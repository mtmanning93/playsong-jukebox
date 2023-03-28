import time
import gspread
from google.oauth2.service_account import Credentials

from simple_term_menu import TerminalMenu

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('playsong_jukebox')
JUKEBOX = SHEET.worksheet('library')

# Initial genre menu
GENRE_LIST = ['rock', 'hip hop', 'electronic', 'reggae', 'indie', 'blues']

# Initial user menu
SEARCH_MENU = {
    'A': 'Artist Name',
    'B': 'Song Title',
    'C': 'Genre',
    'D': 'Year'
}


def add_song():
    """
    Enables user to add songs to the library
    """
    print(
        "To add a song to the jukebox please follow the steps below. \n"
    )

    new_song = []

    input_artist = input("Please enter artists name: \n")
    new_song.append(input_artist)

    input_title = input("Please enter song title: \n")
    new_song.append(input_title)

    input_genre = input("Please enter genre: \n")
    new_song.append(input_genre)

    input_year = input("Please enter year of release: \n")
    new_song.append(input_year)

    print(new_song)


add_song()
