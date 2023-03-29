import time
import os
import validators
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
LIBRARY = SHEET.worksheet('library').get_all_values()[1:]

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
        \nA) Add Song\nB) Remove Song\nC) Search JukeboX\n""")
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


def main_menu_selection(opt):
    """
    Takes users main menu selection and moves to the correct funnction.
    """
    menu_choice = MAIN_MENU[opt]
    print(f"You selected to {menu_choice}.\n")

    if opt == "A":
        add_song()
    elif opt == "B":
        remove_song()
    else:
        select_search_type()

    return menu_choice


def remove_song():
    """
    Enables user to remove song from library
    by displaying a menu to select from.
    """
    print(
        "To remove a song from JukeboX please follow the steps below. \n"
        )
    delete_song = input("Enter song title to remove: ").lower()
    print("")
    
    titles = JUKEBOX.col_values(2)

    for rows in titles:
        if delete_song in rows:
            row_num = titles.index(delete_song) + 1
            row_info = JUKEBOX.row_values(row_num)
            print("Are you sure you would like to permanently delete:\n")
            print("\n".join(row_info[:4]).title())
            break

    while True:
    
        answer = input("\nEnter Y / N: ").upper()
        print(answer)

        if validate_y_or_n(answer):
            if answer == "Y":
                print('delete')
            else:
                main()
            break

    return answer            #JUKEBOX.delete_row(row_num)
            

def validate_y_or_n(a):
    """
    Inside the try checks if input is y or n.
    Raises error if anything is input.
    """
    try:
        if a not in ("N", "Y"):
            raise ValueError(
                f"Answer 'y' for yes or 'n' for no. {a} is not valid.\n"
            )
    except ValueError as err:
        print(f"\nInvalid input: {err}\nPlease try again.")
        return False

    return True


def add_song():
    """
    Enables user to add songs to the library via these inputs:
    1) artist name
    2) song title
    3) genre
    4) year
    5) url 
    """
    print(
        "To add a song to JukeboX please follow the steps below. \n"
    )

    new_song = []
    # Artist
    while True:
        add_artist = input("Please enter artist name: \n").lower()
        new_song.append(add_artist)
        print("")
        if validate_length(len(add_artist)):
            break
    # Title
    while True:
        add_title = input("Please enter song title: \n")
        new_song.append(add_title)
        print("")
        if validate_length(len(add_title)):
            break
    # Genre
    add_genre = input("Please enter genre: \n").lower()
    new_song.append(add_genre.lower())
    print("")

    if add_genre not in GENRE_LIST:
        GENRE_LIST.append(add_genre.lower())   
    # Year
    while True:
        try:
            add_year = input("Please enter year of release: \n")
            new_song.append(add_year)
            if validate_year(int(add_year)):
                break
        except ValueError:
            print("""\nNot a number! Please input a number. 
            (example 1989)\n""")
    # Link
    print(
        """Use the link below to find a video of your choice.
        (cmd/ctrl + click to open)"""
        )
    print(
        f'https://www.youtube.com/results?search_query='
        f'{add_artist.replace(" ", "")}'
        f'+{add_title.replace(" ", "")}\n'
        )
    while True:
        add_link = input("Paste url here: ")
        new_song.append(add_link)
        if link_validation(add_link):
            break
    
    validate_song_entry(new_song, add_year)

    return new_song


def validate_song_entry(entry, year):
    """
    Validates if entry is already in library
    If it is it is displayed as an option.
    If it isn't it is added
    """
    if entry in JUKEBOX.get_all_values()[1:]:
        print("")
        print("Song already in JukeBox!\n")
        search_library(entry[4])
    else:
        print("")
        print("Adding:")
        print(' - '.join(entry[:2]).title())
        print("")

        entry[3] = int(year)

        update_library(entry)


def validate_length(wrd):
    """
    Validates that an input string is not too long.
    Limit to 20 characters.
    """
    try:
        if wrd > 20:
            raise ValueError(
                f"Maximum 20 characters allowed. {wrd} is too long.\n"
            )
    except ValueError as err:
        print(f"\nInvalid input: {err}Please shorten your input.\n")
        return False

    return True


def populate_genre_list(data, inst):
    """
    Searches list of genres.
    Creates new genre list of only one instance from each genre.
    When user adds genre input its added to genre list if not already.
    Gets passed the GENRE_LIST in the main() function.
    """
    for x in data:
        if data.count(x) > inst:
            while x in data:
                data.remove(x)

    print(data)

    return data


def link_validation(link):
    """
    Validates whether the input pasted into the url input is a link
    """
    try:
        if not validators.url(f"{link}"):
            raise ValueError(
                "Not a url. "
            )
    except ValueError as err:
        print(f"\nInvalid input: {err}Please insert another url.\n")
        return False

    return True


def update_library(data):
    """
    Updates google sheet by adding new song
    """
    print("Updating library...\n")
    JUKEBOX.append_row(data)
    time.sleep(2)
    print("Library updated. Restarting JukeboX...\n")
    time.sleep(5)
    # clear terminal here
    os.system('clear')
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
            seperate_search_type(search_choice)
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

    if option in ('A', 'B'):
        
        while True:
            user_search = input(f"Enter {search_name}: \n")
            print("")
            if validate_length(len(user_search)):
                break

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
    # library = SHEET.worksheet('library').get_all_values()[1:]
    
    is_song_available = False

    playlist = []

    for tracks in LIBRARY:
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
    Displays all songs generated in the
    playlist for the user to select from. Also displays a restart method
    to return to the original main menu if needed.
    """
    # Scrollable menu
    # list comprehension
    songs.append(['Restart'])
    playlist_menu = TerminalMenu(
        [" ".join(song[:4]).title() for song in songs]
        )

    restart = False

    while restart is False:

        menu = playlist_menu.show()
        chosen_song = songs[menu]

        if chosen_song == songs[-1]:
            restart = True
            print('Restarting Jukebox...\n')
            time.sleep(1)
            main()
            break
        
        # what happens when wanting to play a song
        print("\n".join(chosen_song[:4]).title() + "\n")
        url = f"{chosen_song.pop()}\n"
        print("Video link (cmd/ctrl + click to open):\n")
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
    populate_genre_list(GENRE_LIST, 1)


print("")
print("Welcome to JukeboX!\n")
main()
