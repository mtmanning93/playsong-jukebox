"""
Main app functions.
"""
import time
import sys
import os

from simple_term_menu import TerminalMenu

from utils import (
    JUKEBOX,
    LIBRARY,
    GENRE_LIST,
    SEARCH_MENU
)

from validations import (
    validate_menu_choice,
    validate_length,
    validate_genre,
    validate_removal,
    validate_year,
    link_validation,
    validate_empty_input
)


def get_menu_option():
    """
    Main menu function enables user to select between
    Add, Remove, or Search song.

    params:
        none

    return:
        <str> one of the dictionary keys
    """
    print("------------------------------------------------------------\n")
    print("Welcome to Video JukeboX!\n")
    print("------------------------------------------------------------")
    print("Please begin by selecting from the menu below:\n")

    for option, description in MENU_HANDLERS.items():
        print(option + ')', description.__name__.replace('_', ' ').title())

    print("")

    while True:

        main_menu_choice = input(
            """Please select a menu choice type from A, B, C, D:\n"""
        ).upper()

        if validate_menu_choice(main_menu_choice, MENU_HANDLERS):
            break

    return main_menu_choice


def handle_menu_selection(option):
    """
    Takes users main menu selection and moves to the correct function.

    param:
        option: function name from MENU_HANDLERS

    return:
        None
    """
    print("------------------------------------------------------------\n")
    print(
        f"You chose to {MENU_HANDLERS[option].__name__.replace('_', ' ')}.\n"
    )
    MENU_HANDLERS[option]()
    main()


def show_library():
    """
    Shows scrollable version of entire library and displays link
    when selected. Shows restart as an option also.

    params:
        none

    return:
        <lst> all_songs populated if song is in library.
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
            show_library()

    return all_songs


def add_song():
    """
    Enables user to add songs to the library via these inputs:
    artist name, song title, genre, year, url.
    Creates a new list (new_song) which represents the new song data

    params:
        none

    return:
        <list> new_song a list of the added data
    """
    print(
        "To add a song to JukeboX please follow the steps below. \n"
    )
    new_song = []

    while True:
        add_artist = input("Please enter artist name:\n").lower()
        print("")
        if (
            validate_length(len(add_artist)) and
            validate_empty_input(add_artist)
        ):
            new_song.append(add_artist)
            break

    while True:
        add_title = input("Please enter song title:\n")
        print("")
        if (
            validate_length(len(add_title)) and
            validate_empty_input(add_title)
        ):
            new_song.append(add_title)
            break
        
    while True:
        add_genre = input("Please enter genre:\n").lower()
        if validate_empty_input(add_genre):
            new_song.append(add_genre.lower())
            print("")
            break

    if add_genre not in GENRE_LIST:
        GENRE_LIST.append(add_genre.lower())

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

    search = (
        f'https://www.youtube.com/results?search_query='
        f'{add_artist.replace(" ", "")}+{add_title.replace(" ", "")}'
    )
    print("Use the search link to find a video of your choice.")
    print("Then copy and paste the link below.\n")
    time.sleep(1)
    print(f"Link to search for video (copy/paste):\n{search}\n")
    time.sleep(2)

    while True:
        add_link = input("Paste url here:\n")
        if link_validation(add_link):
            new_song.append(add_link)
            break

    search_for_duplicates(new_song, add_year)

    return new_song


def remove_song():
    """
    Enables user to remove song from library by displaying a menu
    to select from.
    First validates that the song is in library and if not displays
    another input attempt.
    Ability to cancel remove song and return to main menu using 'c'
    as an input.

    param:
        none

    return:
        <str> input by user in order to search library
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

        if validate_empty_input(delete_song_input):
            library_values = []
            for song in LIBRARY:
                if delete_song_input in song:
                    library_values += song

            if validate_removal(delete_song_input, library_values):
                break

    get_remove_options(delete_song_input)

    return delete_song_input


def get_remove_options(search):
    """
    If song is found in library this function will display a menu
    from which the user can choose which song to delete.

    param:
        search: <str> input by user to delete it.

    return:
        delete_menu: <lst> list of options to delete
    """
    search_list = JUKEBOX.findall(search)
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

    if delete == delete_list[-1]:
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


def search_for_duplicates(entry, year):
    """
    Validates if entry is already in library
    If it is it is displayed as an option.
    If it isn't it is added

    params:
        entry: <lst> data of the new song
        year: <str> the year input as string to concat with list,
              reverted to integer.

    return:
        none
    """
    print("------------------------------------------------------------\n")
    if entry in JUKEBOX.get_all_values()[1:]:
        print("Song already in JukeBox!\n")
        get_songs_from_library(entry[4])
    else:
        print("Adding:\n")
        print(' - '.join(entry[:2]).title())
        print("")

        entry[3] = int(year)

        add_song_to_library(entry)


def add_song_to_library(data):
    """
    Updates google sheet by adding new song

    param:
        data: <lst> list of new song data

    return:
        none
    """
    print("Updating library...\n")
    JUKEBOX.append_row(data)
    time.sleep(3)
    print("Library updated. Restarting JukeboX...\n")
    time.sleep(2)
    reboot()


def search_library():
    """
    Search menu options.
    Provides search options for the user to select from.

    param:
        none

    return:
        search_choice: <str> value of SEARCH_MENU
    """
    print("Please select a search method from the list below:\n")
    for option, description in SEARCH_MENU.items():
        print(option + ')', description.title())
    print("")

    while True:

        search_choice = input(
            """Please select a search type from A, B, C, D:\n"""
        ).upper()

        if validate_menu_choice(search_choice, SEARCH_MENU):
            get_search_type(search_choice)
            break

    return search_choice


def get_search_type(option):
    """
    Takes search type option selected by user and provides input method.
    Depending on search type!

    param:
        option: <str> choice from SEARCH_MENU keys.

    return:
        user_Search: <str> validated by length
        genre_input: <str>
        year: <int> to search library for an integer as numbers are not
            found.
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
        get_songs_from_library(user_search)

    elif option == 'C':

        print("Please select from the list of genres below.\n")
        get_genre_list()

        while True:
            genre_input = input("Enter Genre:\n")
            print("")

            if validate_genre(genre_input):
                print(f"Searching library for {genre_input.title()}...\n")
                break

        get_songs_from_library(genre_input)

    else:

        while True:
            try:
                year = int(input("Enter year between 1900 and now:\n"))
                print("")

                if validate_year(year):
                    print(f"Searching library for {year}...\n")
                    time.sleep(1)
                    get_songs_from_library(str(year))
                    break

            except ValueError:
                print(
                    """\nNot a number! Please input a number.
                    (example 1989)\n"""
                )

    return user_search, genre_input, year


def get_genre_list():
    """
    Populates genre list with just one instance of each genre in the
    library.

    param:
        none

    return:
        short_genre_list: <lst> list of one instance of each genre.
    """
    short_genre_list = []

    for genre in GENRE_LIST:
        if genre not in short_genre_list:
            short_genre_list.append(genre)

    short_genre_list.sort()

    for item in short_genre_list:
        print(item.title())
    print("")

    return short_genre_list


def get_songs_from_library(search_input):
    """
    Takes input information from chosen search after validation
    and searches through the library.
    Adds available songs to playlist list.

    param:
        search_input: <str> defined by user inputs

    return:
        is_song_available: <bool> True if song in library
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
        search_library()

    display_user_playlist(playlist)

    return is_song_available


def display_user_playlist(songs):
    """
    Displays all songs generated in the
    playlist for the user to select from. Also displays a restart method
    to return to the original main menu if needed.

    param:
        songs: <lst> A list of songs found in library.

    return:
        none
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

        print("---------------------------------------------------------")
        print("\n".join(chosen_song[:4]).title() + "\n")
        url = chosen_song[-1]
        print("Video link (copy and paste url):\n")
        print(f"{url}\n")


def reboot():
    """
    Restarts program and clears terminal
    """
    os.system('clear')
    python = sys.executable
    os.execl(python, python, * sys.argv)


MENU_HANDLERS = {
    'A': add_song,
    'B': remove_song,
    'C': search_library,
    'D': show_library
}


def main():
    """
    Run all program functions.
    """
    main_choice = get_menu_option()
    handle_menu_selection(main_choice)


if __name__ == '__main__':
    main()
