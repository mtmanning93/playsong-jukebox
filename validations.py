"""
All validating functions.
"""
import validators

from utils import (
    GENRE_LIST,
    YEAR
)


def validate_menu_choice(value, menu):
    """
    Checks if input is in parameter dictionary.
    Prints invalid input if not in dictionary.

    param:
        value: <str> input choice of user
        menu: <dict> either MENU_HANDLERS or SEARCH_MENU

    return:
        <bool> true if value is in menu keys
    """
    if value not in menu.keys():
        print(f"\nInvalid input: {value} not an option.\n")
        return False

    return True


def validate_removal(val, lst):
    """
    Searches if song is in library and available to delete.
    If song is not in library returns error and displays input again.

    params:
        val: <str> the input from user.
        lst: <list> a list of all instances of the avbove val in the library.

    return:
        <bool> true if the string is valid.
    """
    if val not in lst:
        print(
            f"Couldn't find input in JukeboX: {val} not found.\n"
            f"Please try again.\n"
            )
        return False

    return True


def validate_length(wrd):
    """
    Validates that an input string is not too long.
    Limit to 20 characters.

    param:
        wrd: <str> string

    return:
        <bool> true if the string is valid
    """

    if wrd > 40:
        print(
            f"\nInvalid input: Maximum 40 characters allowed.\n"
            f"{wrd} is too long. Please shorten your input.\n"
            )
        return False

    return True


def link_validation(link):
    """
    Validates whether the input pasted into the url input is a link

    param:
        link: <url> provided by user input

    return:
        <bool> true if the string is valid
    """
    if not validators.url(f"{link}"):
        print("\nInvalid input: Not a url. Please insert another url.\n")
        return False

    return True


def validate_genre(genre):
    """
    Validates whether the chosen genre input is in the genre list.

    param:
        genre: <str> users input to search.

    return:
        <bool> true if the string is valid.
    """
    if genre not in GENRE_LIST:
        print(
            f"\nInvalid input: {genre.title()} is not in provided options.\n"
            f"Please select from the genre list.\n"
            )
        return False

    return True


def validate_year(num):
    """
    Inside the try checks if input is a valid date
    between 1900 and present year.
    and between 1900 and current year.
    Raises error if entered number is not in time frame.

    param:
        num: <int>

    return:
        <bool> true if the string is valid
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
