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

# Initial genre menu
GENRE_LIST = ['rock', 'hip hop', 'electronic', 'reggae', 'indie', 'blues']

# Initial user menu
SEARCH_MENU = {
    'A': 'Artist Name',
    'B': 'Song Title',
    'C': 'Genre',
    'D': 'Year'
}


def select_search_type():
    """
    Provides search options for the user to select from.
    """
    while True:
        print("""Please begin by selecting a search method from the list below:
        \nA) Artist Name\nB) Song Title\nC) Genre\nD) Year\n""")
        search_choice = input("""Please select a search type from a, b, c or d: """).upper()

        if validate_choice(search_choice):
            break
    
    return search_choice


def validate_choice(value):
    """
    Inside the try checks if input is in SEARCH_MENU dict.
    Raises error if not in dict.
    """
    try:
        if value not in SEARCH_MENU.keys():
            raise ValueError(
                f"Search type A, B, C, or D required. {value} is not valid.\n"
            )
    except ValueError as e:
        print(f"\nInvalid input: {e}Please try again.\n")
        return False

    return True


def seperate_search_type(option):
    """
    Takes search type option selected by user and provides input method.
    Depending on search type!
    """
    search_name = SEARCH_MENU[option]
    print(f"You selected to search via {option}) {search_name}...\n")

    if option == 'A' or option == 'B':
        
        user_search = input(f"Enter {search_name}: \n")
        print("")

        search_library(user_search)

    elif option == 'C':
        # Provide list of genres for user
        print("Please select from the list of genres below.\n")
        for genre in GENRE_LIST:
            print(genre)
        print("")

        while True:
            genre_input = input("Enter Genre: \n")
            print("")

            if validate_genre(genre_input):
                print("Searching library for genre...\n")
                break

        search_library(genre_input)

        return genre_input
    else:
        # Search validation for year D
        while True:
            try:
                year = int(input("Enter year between 1940 and now: \n"))
                print("")
                if validate_year(year):
                    print("Searching library for year...\n")
                    break
            except ValueError:
                print("\nNot a number! Please input a number. (example 1989)\n")     

        return year


def validate_genre(genre):
    """
    Validates whether the chosen genre input is in the genre list.
    """
    try:
        if genre not in GENRE_LIST:
            raise ValueError(
                f"Genre not in provided list. {genre} is not a valid input.\n"
            )
    except ValueError as e:
        print(f"\nInvalid input: {e}Please try again.\n")
        return False

    return True
            

def validate_year(num):
    """
    Inside the try checks if input is 4 digits long
    and between 1940 and current year.
    Raises error if not in dict.
    """
    # num_int = int(num)
    # print(num_int)
    # print(type(num_int))
    try:
        if (num >= 1940 and num <= 2023):
            print('\nSearching library...\n')
            num_str = str(num)
            search_library(num_str)
        else:
            raise ValueError(
                f"Numeric 4 digit year between 1940 and now required (example:"
                f" 1989). {num} is not valid.\n"
            )
    except ValueError as e:
        print(f"\nInvalid input: {e}Please try again.\n")
        return False

    return True


def search_library(input):
    """
    Takes input information and searches library for results
    """
    library = SHEET.worksheet('library').get_all_values()[1:]
    
    is_song_available = False

    for item in library:
        
        if input in item:
            is_song_available = True
            print(item)

    if not is_song_available:
        print(
            f"Sorry we cannot find {input} in our library. "
            f"Please try another search.\n"
        )



print("Welcome to Playsong Jukebox!\n")

menu_choice = select_search_type() # THIS IS THE SELECTED METHOD (A/B/C/D)
seperate_search_type(menu_choice)