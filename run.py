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
# GENRE_LIST = ['rock', 'hip hop', 'electronic', 'reggae', 'indie', 'blues']
GENRE_LIST = JUKEBOX.col_values(3)[1:]

MAIN_MENU = {
    'A': "add song",
    'B': "remove song",
    'C': "search song"
}

# Initial user menu
SEARCH_MENU = {
    'A': 'Artist Name',
    'B': 'Song Title',
    'C': 'Genre',
    'D': 'Year'
}


def main_menu():
    """
    Main menu function enables user to select between
    Add, Remove, or Search song.
    """
    while True:
        print("""Please begin by selecting from the menu below:
        \nA) Add Song\nB) Remove Song\nC) Search Jukebox\n""")
        main_menu_choice = input("""Please select a menu choice type from A, B, C: """).upper()

        if validate_main_choice(main_menu_choice):
            break
    
    return main_menu_choice


def validate_main_choice(value):
    """
    Inside the try checks if input is in SEARCH_MENU dict.
    Raises error if not in dict.
    """
    try:
        if value not in MAIN_MENU.keys():
            raise ValueError(
                f"Search type A, B, C required. {value} is not valid.\n"
            )
    except ValueError as err:
        print(f"\nInvalid input: {err}\n Please try again.\n")
        return False

    return True


def main_menu_selection(option):
    """
    Takes users main menu selection and moves to the correct funnction.
    """
    menu_choice = MAIN_MENU[option]
    print(f"You selected to {menu_choice}.\n")

    if option == "A":
        add_song()
    elif option == "B":
        print("remove song")
        main()
    else:
        select_search_type()


def add_song():
    """
    Enables user to add songs to the library
    """
    print(
        "To add a song to the jukebox please follow the steps below. \n"
    )

    new_song = []

    # artist
    input_artist = input("Please enter artists name: \n")
    new_song.append(input_artist)
    print("")
    # title
    input_title = input("Please enter song title: \n")
    new_song.append(input_title)
    print("")
    # genre
    add_genre = input("Please enter genre: \n")
    new_song.append(add_genre.lower())
    print("")

    if add_genre not in GENRE_LIST:
        GENRE_LIST.append(add_genre.lower())
    
    # year
    while True:
        try:
            add_year = input("Please enter year of release: \n")
            new_song.append(add_year)
            if validate_year(int(add_year)):
                break
        except ValueError:
            print("""\nNot a number! Please input a number. 
            (example 1989)\n""")

    # youtube link
    print(
        """Use the link below to find a video of your choice.
        (cmd/ctrl + click to open)"""
        )
    print(
        f'https://www.youtube.com/results?search_query='
        f'{input_artist.replace(" ", "")}'
        f'+{input_title.replace(" ", "")}\n'
        )
    add_link = input("Paste url here: ")
    new_song.append(add_link)

    print("")
    print("Adding:")
    print(' - '.join(new_song[:2]).title())
    print("")

    new_song[3] = int(add_year)

    update_library(new_song)


def update_genre_list(data, inst):
    """
    Searches list of genres.
    Creates new genre list of only one instance from each genre
    When user adds genre input its added to genre list if not already.
    """
    for x in data:
        if data.count(x) > inst:
            while x in data:
                data.remove(x) 

    print(data)

    return data


def update_library(data):
    """
    Updates google sheet by adding new song
    """
    print("Updating library...\n")
    JUKEBOX.append_row(data)
    time.sleep(2)
    print("Library updated.\n")
    time.sleep(1)
    # clear terminal here
    main()


def select_search_type():
    """
    Search menu options.
    Provides search options for the user to select from.
    """
    while True:
        print("""Please begin by selecting a search method from the list below:
        \nA) Artist Name\nB) Song Title\nC) Genre\nD) Year\n""")
        search_choice = input("""Please select a search type from A, B, C, D: """).upper()

        if validate_search_choice(search_choice):
            break
    
    return search_choice


def validate_search_choice(value):
    """
    Inside the try checks if input is in SEARCH_MENU dict.
    Raises error if not in dict.
    """
    try:
        if value not in SEARCH_MENU.keys():
            raise ValueError(
                f"Search type A, B, C, or D required. {value} is not valid.\n"
            )
    except ValueError as err:
        print(f"\nInvalid input: {err}\n Please try again.\n")
        return False

    return True


def seperate_search_type(option):
    """
    Takes search type option selected by user and provides input method.
    Depending on search type!
    """
    search_name = SEARCH_MENU[option]
    print(f"You selected to search via {option}) {search_name}.\n")

    if option == 'A' or option == 'B':
        
        user_search = input(f"Enter {search_name}: \n")
        print("")

        print("Searching library...\n")
        time.sleep(1)
        search_library(user_search)

        return user_search

    elif option == 'C':
        # Provide list of genres for user
        print("Please select from the list of genres below.\n")
        for genre in GENRE_LIST:
            print(genre.title())
        print("")
        
        while True:
            genre_input = input("Enter Genre: \n")
            print("")

            if validate_genre(genre_input):
                print(f"Searching library for {genre_input.title()}...\n")
                break

        search_library(genre_input)

        return genre_input

    else:
        # Search validation for year
        while True:
            # The try checks if value given is a number. 
            # If not a Value Error is given.
            try:
                year = int(input("Enter year between 1940 and now: \n"))
                print("")
                if validate_year(year):
                    #
                    print(f"Searching library for {year}...\n")
                    search_library(str(year))
                    #
                    break
            except ValueError:
                print("""\nNot a number! Please input a number. 
                (example 1989)\n""")     

        return year


def validate_genre(genre):
    """
    Validates whether the chosen genre input is in the genre list.
    """
    try:
        if genre not in GENRE_LIST:
            raise ValueError(
                f"{genre.title()} is not in provided options.\n"
                
            )
    except ValueError as error:
        print(
            f"\nInvalid input: {error} \n"
            f"Please select from provided genre list above.\n"
            )
        return False

    return True
            

def validate_year(num):
    """
    Inside the try checks if input is a valid date 
    between 1940 and present year.
    and between 1940 and current year.
    Raises error if entered number is not in time frame.
    """
    try:
        if (num >= 1940 and num <= 2023):
            print("")
            # print(f"Searching library for {num}...\n")
            # num_str = str(num)
            # search_library(num_str)
        else:
            raise ValueError(
                f"Numeric 4 digit year between 1940 and now required (example:"
                f" 1989). {num} is not valid.\n"
            )
    except ValueError as err:
        print(f"\nInvalid input: {err}\n Please try again.\n")
        return False

    return True


def search_library(search_input):
    """
    Takes input information from chosen search after validation
    and searches through the library.
    Adds available songs to playlist list.
    """
    library = SHEET.worksheet('library').get_all_values()[1:]
    
    is_song_available = False

    playlist = []

    for tracks in library:
        if search_input in tracks:
            is_song_available = True
            playlist.append(tracks)
    display_user_playlist(playlist)

    if not is_song_available:
        print(
            f"Sorry we cannot find {input} in our library. "
            f"Please try another search.\n"
        )
        select_search_type()

    return is_song_available
 

def display_user_playlist(songs):
    """
    Displays all songs generated in the playlist for the user to select from
    Also displays quit as a restart method to return to the original main menu if needed
    """
    # Scrollable menu
    # list comprehension
    songs.append(['Quit'])
    playlist_menu = TerminalMenu(
        [" ".join(song[:4]).title() for song in songs]
        )

    restart = False

    while restart is False:

        menu = playlist_menu.show()
        chosen_song = songs[menu]

        if chosen_song == songs[-1]:
            restart = True
            print('Restarting search...\n')
            time.sleep(1)
            main()
            break
        else:
            print("\n".join(chosen_song[:4]).title() + "\n")
            url = f"{chosen_song.pop()}\n"
            print("Video link (cmd/ctrl + click to open): \n")
            print(url)


def main():
    """
    Run all program functions.
    """
    main_choice = main_menu()
    main_menu_selection(main_choice)
    add_song()
    search_choice = select_search_type()  # THIS IS THE SELECTED METHOD (A/B/C/D)
    seperate_search_type(search_choice)
    update_genre_list(GENRE_LIST, 1)


print("Welcome to Playsong Jukebox!\n")
main()
