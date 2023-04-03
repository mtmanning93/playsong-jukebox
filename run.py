import time
import datetime
import sys
import os
import gspread
from google.oauth2.service_account import Credentials
from simple_term_menu import TerminalMenu
import validators

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('JukeboX')
JUKEBOX = SHEET.worksheet('library')
LIBRARY = SHEET.worksheet('library').get_all_values()[1:]
TODAY = datetime.date.today()
YEAR = TODAY.year

GENRE_LIST = JUKEBOX.col_values(3)[1:]

# MAIN_MENU = {
#     'A': add_song(),
#     'B': "remove song",
#     'C': "search song",
#     'D': "show library"
# }

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
    print("------------------------------------------------------------\n")
    print("Welcome to Video JukeboX!\n")
    print("------------------------------------------------------------")
    print("Please begin by selecting from the menu below:\n""")
    
    for option, description in MAIN_MENU.items():
        print(option, description.__name__.replace('_', ' ').title())
    
    print("")

    while True:
        
        main_menu_choice = input(
            """Please select a menu choice type from A, B, C, D:\n"""
            ).upper()

        if validate_menu_choice(main_menu_choice, MAIN_MENU):
            break

    return main_menu_choice


def validate_menu_choice(value, menu):
    """
    Inside the try checks if input is in SEARCH_MENU dict.
    Raises error if not in dict.
    """
    if value not in menu.keys():
        print(f"\nInvalid input: {value} not an option.\n") 
        return False
        
    return True


def get_user_option(option):
    """
    Takes users main menu selection and moves to the correct funnction.
    """
    menu_choice = MAIN_MENU[option]
    print("------------------------------------------------------------\n")
    print(f"You selected to {menu_choice.__name__.replace('_', ' ')}.\n")
    return menu_choice


def show_library():
    """
    Shows scrollable version of entire library and displays link
    when selected. Shows restart as an option also.
    """
    os.system('clear')
    all_songs = []
    for info in LIBRARY:
        all_songs.append(info)

    all_songs.sort()
    all_songs.append(['Restart'])

    show_all_menu = TerminalMenu(
        [" - ".join(song[:2]).title() for song in all_songs]
        )

    menu = show_all_menu.show()
    library_choice = all_songs[menu]

    if library_choice == all_songs[-1]:
        print('Restart Jukebox...\n')
        time.sleep(1.5)
        reboot()
    else:
        os.system('clear')
        print("You selected:\n")
        print("\n".join(library_choice[:4]).title() + "\n")
        url = library_choice[-1]
        print("Video link (copy and paste url):\n")
        print(f"{url}\n")

        return_buttons = ['Back to list', 'Home']

        back_menu = TerminalMenu(return_buttons)
        button = back_menu.show()
        back_choice = return_buttons[button]

        if back_choice == 'Home':
            reboot()
        else:
            os.system('clear')
            show_library()

    return all_songs


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
        add_artist = input("Please enter artist name:\n").lower()
        print("")
        if validate_length(len(add_artist)):
            new_song.append(add_artist)
            break
    # Title
    while True:
        add_title = input("Please enter song title:\n")
        print("")
        if validate_length(len(add_title)):
            new_song.append(add_title)
            break
    # Genre
    add_genre = input("Please enter genre:\n").lower()
    new_song.append(add_genre.lower())
    print("")

    if add_genre not in GENRE_LIST:
        GENRE_LIST.append(add_genre.lower())
    # Year
    while True:
        try:
            add_year = input("Please enter year of release:\n")
            if validate_year(int(add_year)):
                new_song.append(add_year)
                break
        except ValueError:
            print(
                """\nNot a number! Please input a number.
            (example 1989)\n"""
            )
    # Link
    search = (
        f'https://www.youtube.com/results?search_query='
        f'{add_artist.replace(" ", "")}+{add_title.replace(" ", "")}'
        )
    print("Use the search link to find a video of your choice.")
    print("Then copy and paste the link below.\n")
    time.sleep(1)
    print(f"Link to search for video (copy/paste):\n{search}\n")
    time.sleep(2)
    # webbrowser.open_new_tab(search)
    while True:
        add_link = input("Paste url here:\n")
        if link_validation(add_link):
            new_song.append(add_link)
            break

    validate_song_entry(new_song, add_year)

    return new_song


def remove_song():
    """
    Enables user to remove song from library by displaying a menu
    to select from.
    First validates that the song is in library and if not displays
    another input attempt.
    Ability to cancel remove song and return to main menu using 'c'
    as an input.
    """
    print(
        "To remove a song from JukeboX please follow the steps below. \n"
    )
    while True:

        delete_song_input = input(
            "Enter some song information to remove ((c) cancel):\n"
            ).lower()
        print("")

        if delete_song_input == 'c':
            print('Cancelled restarting Jukebox...\n')
            time.sleep(2)
            reboot()

        library_values = []

        for song in LIBRARY:
            if delete_song_input in song:
                library_values += song
    
        if validate_removal(delete_song_input, library_values):
            break

    removal_menu(delete_song_input)

    return delete_song_input


def validate_removal(val, lst):
    """
    Searches if song is in library and available to delete.
    If song is not in library returns error and displays input again.
    """
    try:
        if val not in lst:
            raise ValueError(
                f"{val} not found.\n"
            )
    except ValueError as err:
        print(f"Couldn't find input in JukeboX:\n{err}\nPlease try again.\n")
        return False

    return True


def removal_menu(val):
    """
    If song is found in library this function will display a menu
    from which the user can choose which song to delete.
    """
    search_list = JUKEBOX.findall(val)
    delete_list = []

    for item in search_list:
        row_num = item.row
        row_info = JUKEBOX.row_values(row_num)
        delete_list.append(row_info[:2])
    
    delete_list.sort()
    delete_list.append(['Cancel'])

    options = TerminalMenu(
            [" ".join(i[:4]).title() for i in delete_list]
            )
        
    print("------------------------------------------------------------\n")
    print("Choose from the list below and press Enter to delete song:\n")

    delete_menu = options.show()
    delete = delete_list[delete_menu]
    deleted_song = " - ".join(delete[:2]).title()

    if (delete == delete_list[-1]):
        print('Restarting Jukebox...\n')
        time.sleep(2)
        reboot()
    else:
        JUKEBOX.delete_rows(row_num)
        print("Deleting...")
        print(f"\n{deleted_song} from JukeboX...\n")
        time.sleep(1)
        print('Song deleted. Restarting JukeboX...')
        time.sleep(3.5)
        reboot()

    return delete_menu


def validate_song_entry(entry, year):
    """
    Validates if entry is already in library
    If it is it is displayed as an option.
    If it isn't it is added
    """
    print("------------------------------------------------------------\n")
    if entry in JUKEBOX.get_all_values()[1:]:
        print("Song already in JukeBox!\n")
        search_library(entry[4])
    else:
        print("Adding:\n")
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
        if wrd > 40:
            raise ValueError(
                f"Maximum 40 characters allowed. {wrd} is too long.\n"
            )
    except ValueError as err:
        print(f"\nInvalid input: {err}Please shorten your input.\n")
        return False

    return True


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
    time.sleep(3)
    print("Library updated. Restarting JukeboX...\n")
    time.sleep(2)
    reboot()


def select_search_type():
    """
    Search menu options.
    Provides search options for the user to select from.
    """
    print("Please select a search method from the list below:\n")
    for option, description in SEARCH_MENU.items():
        print(option, description.title())
    print("")
    
    while True:
        
        search_choice = input(
            """Please select a search type from A, B, C, D:\n"""
            ).upper()

        if validate_menu_choice(search_choice, SEARCH_MENU):
            seperate_search_type(search_choice)
            break

    return search_choice


def seperate_search_type(option):
    """
    Takes search type option selected by user and provides input method.
    Depending on search type!
    """
    search_name = SEARCH_MENU[option]
    print("------------------------------------------------------------\n")
    print(f"You selected to search via {option}) {search_name}.\n")

    if option in ('A', 'B'):

        while True:
            user_search = input(f"Enter {search_name}:\n")
            print("")
            if validate_length(len(user_search)):
                break

        print("Searching library...\n")
        time.sleep(1)
        search_library(user_search)

    elif option == 'C':
        # Provide list of genres for user
        print("Please select from the list of genres below.\n")
        simple_genre_list = []
        for j in GENRE_LIST:
            if j not in simple_genre_list:
                simple_genre_list.append(j)
        for item in simple_genre_list:
            print(item.title())
        print("")

        while True:
            genre_input = input("Enter Genre:\n")
            print("")

            if validate_genre(genre_input):
                print(f"Searching library for {genre_input.title()}...\n")
                break

        search_library(genre_input)

    else:
        # Search validation for year
        while True:
            # The try checks if value given is a number.
            # If not a Value Error is given.
            try:
                year = int(input("Enter year between 1900 and now:\n"))
                print("")

                if validate_year(year):
                    print(f"Searching library for {year}...\n")
                    time.sleep(1)
                    search_library(str(year))
                    break

            except ValueError:
                print(
                    """\nNot a number! Please input a number.
                    (example 1989)\n"""
                )

    return user_search, genre_input, year


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
    between 1900 and present year.
    and between 1900 and current year.
    Raises error if entered number is not in time frame.
    """
    try:
        if (1900 <= num <= YEAR):
            print("")
        else:
            raise ValueError(
                f"Numeric 4 digit year between 1900 and now required (example:"
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

    is_song_available = False

    playlist = []

    for tracks in LIBRARY:
        for data in tracks:
            if search_input in data:
                is_song_available = True
                playlist.append(tracks)

    if not is_song_available:
        print(
            f"Sorry we cannot find {search_input} in our library. "
            f"Please try another search.\n"
        )
        time.sleep(2)
        select_search_type()

    display_user_playlist(playlist)

    return is_song_available


def display_user_playlist(songs):
    """
    Displays all songs generated in the
    playlist for the user to select from. Also displays a restart method
    to return to the original main menu if needed.
    """
    songs.sort()
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
            time.sleep(1.5)
            reboot()
            break

        # what happens when wanting to play a song
        print("\n".join(chosen_song[:4]).title() + "\n")
        url = chosen_song[-1]
        print("Video link (copy and paste url):\n")
        print(f"{url}\n")
        # webbrowser.open_new_tab(url)


def reboot():
    """
    Restarts program and clears terminal
    """
    os.system('clear')
    python = sys.executable
    os.execl(python, python, * sys.argv)


MAIN_MENU = {
    'A': add_song,
    'B': remove_song,
    'C': select_search_type,
    'D': show_library
}


def main():
    """
    Run all program functions.
    """
    main_choice = main_menu()
    get_user_option(main_choice)


main()
