# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('playsong_jukebox')

print("Welcome to Playsong Jukebox!\n")

search_menu = {
    'A': 'Artist Name',
    'B': 'Song Title',
    'C': 'Genre',
    'D': 'Era'
}


def select_search_type():
    """
    Provides search options for the user to select from.
    """
    print("Please begin by selecting a search method from the list below:\n\nA) Artist Name\nB) Song Title\nC) Genre\nD) Era\n")
    choice = input("Please select a search method from a, b, c or d: ").upper()

    if choice in search_menu.keys():
        print(
            f"\nYou selected to search via {choice}) {search_menu.get(choice)}...\n")
        if choice == 'A':
            search_by_artist_name()
        # elif choice == 'B':
        #     search_by_song_title()
        # elif choice == 'C':
        #     search_by_genre()
        # elif choice == 'D':
        #     search_by_era()
    else:
        print("\nPlease choose an option from A, B, C, or D.\n")

    return choice


def search_by_artist_name():
    """
    Enables user to search via the artists name.
    Displays list of all entries in the library.
    """
    artist_name = input("Enter artist name: ").lower()
    print(f"\nYou searched for {artist_name}. Searching...\n")

    column_1 = SHEET.worksheet('library').col_values(1)
    artist_list = column_1[1:]

    if artist_name in artist_list:
        appearances = SHEET.worksheet('library').findall(artist_name)
        # print row information of all instances of the artists name.
        for each in appearances:
            artists_song_list = SHEET.worksheet('library').row_values(each.row)
            print(artists_song_list)
    else:
        print("""Sorry, we couldnt find that artist in our library. Please try 
        again.\n""")
        search_by_artist_name()


select_search_type()
