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

#Initial user menu
SEARCH_MENU = {
    'A': 'artist_name',
    'B': 'song_title',
    'C': 'genre',
    'D': 'year'
}


def select_search_type(menu):
    """
    Provides search options for the user to select from.
    """
    print("""Please begin by selecting a search method from the list below:\n
    \nA) Artist Name\nB) Song Title\nC) Genre\nD) Year\n""")
    choice = input("Please select a search method from a, b, c or d: ").upper()
    search_choice = SEARCH_MENU.get(choice)
    choice_str = search_choice.title().replace('_', ' ')

    if choice in menu.keys():
        print(f"\nYou selected to search via {choice}) {choice_str}...\n")
        search(search_choice)
    else:
        print("\nPlease choose an option from A, B, C, or D.\n")

    return choice


def search(type):
    """
    Enables user to search via chosen search method.
    Displays list of all entries found in the library with this search input
    """
    search_input = input(f"Enter {type.title().replace('_', ' ')}: ")
    print("")
    print(f"Searching for {search_input}...\n")

    library = SHEET.worksheet('library').get_all_values()[1:]

    for song in library:
        is_song_available = False
        if search_input in song:
            is_song_available = True
            print(song)

    if not is_song_available:
        print(f"Sorry we cannot find {search_input} in our library. "
        f"Please try another {type}.\n")
        search(type)


user_menu = select_search_type(SEARCH_MENU)


# def search_by_artist_name():
#     """
#     Enables user to search via the artists name.
#     Displays list of all entries in the library.
#     """
#     artist_name = input("Enter artist name: ").lower()
#     print(f"\nYou searched for {artist_name}. Searching...\n")

#     column_1 = SHEET.worksheet('library').col_values(1)
#     artist_list = column_1[1:]

#     #Try except possibility
#     if artist_name in artist_list:
#         appearances = SHEET.worksheet('library').findall(artist_name)
#         # print row information of all instances of the artists name.
#         for each in appearances:
#             artists_song_list = SHEET.worksheet('library').row_values(each.row)
#             print(artists_song_list)
#     else:
#         print("""Sorry, we couldnt find that artist in our library. Please try 
#         again.\n""")
#         search_by_artist_name()

#     return artists_song_list


# #Add validation maybe just a keyword search or first 6 letters etc.
# def search_by_song_title():
#     """
#     Enables user to search via the song title.
#     Displays list of all entries in the library.
#     """
#     song_title = input("Enter song title: ").lower()
#     print(f"\nYou searched for {song_title}. Searching...\n")

#     column_2 = SHEET.worksheet('library').col_values(2)
#     song_title_list = column_2[1:]

#     #Try except possibility
#     if song_title in song_title_list:
#         title = SHEET.worksheet('library').find(song_title)
#         song_title_info = SHEET.worksheet('library').row_values(title.row)
#         print(song_title_info)
#     else:
#         print("""Sorry, we couldnt find that song in our library. Please try 
#         again.\n""")
#         search_by_song_title()

#     # return song_title_info


# def search(search_choice, column):
#     """
#     Enables user to search via the song artist or title.
#     Displays list of all entries in the library.
#     """
#     user_input = input(f"Enter {search_choice}: ").lower()
#     print(f"\nYou searched for {user_input}. Searching...\n")

#     column_number = SHEET.worksheet('library').col_values(column)
#     search_results = column_number[1:]
#     print(search_results)
    

# def search_by_genre():
#     """
#     User can search by genre with this function. It extracts all rows with the
#     instance of the selected genre.
#     """
#     genres = ['rock', 'reggae', 'pop', 'hip hop', 'electronic', 'blues', 'indie']

#     print("""Please choose from one of the following genres:\n""")
#     for genre in genres:
#         print(genre.title())
    
#     genre_choice = input("\nEnter genre of choice: ").lower()

#     if genre_choice in genres:
#         genre_list = SHEET.worksheet('library').findall(genre_choice)

#         for item in genre_list:
#             songs_in_genre = SHEET.worksheet('library').row_values(item.row)
#             print(songs_in_genre)
#     else:
#         print("""Sorry, we couldnt find that genre in our library. Please try 
#         again.\n""")
#         search_by_genre()
    
#     return songs_in_genre


# def search_by_year():
#     """
#     Gets all songs from the year of input.
#     If no songs are available display all songs from decade.
#     """

#     year_input = int(input("Enter year (1989): "))
#     print(year_input)
    
#     # print(f"\nYou selected the year {year_input}. Searching library...\n")

#     # if len(year_input) == 4 and year_input.isdigit():
#     #     year_playlist = SHEET.worksheet('library').findall(year_input)
#     #     for song in year_playlist:
#     #         songs_in_year = SHEET.worksheet('library').row_values(song.row)
#     #         print(songs_in_year)
#     # elif len(year_input) < 4 or len(year_input) > 4:
#     #     print("Please enter a 4 digit year (1989)\n")
