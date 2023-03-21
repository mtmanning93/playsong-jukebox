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


def select_search_type():
    """
    Provides search options for the user to select from.
    """
    print("Please begin by selecting a search method:\n\nA)Artist Name\nB)Song Title\nC)Genre\nD)Era\n")
    choice = input("Please select a search method: ").upper()

    if choice == 'A':
        print("you chose a")
    elif choice == 'B':
        print("you chose b")
    elif choice == 'C':
        print("you chose c")
    elif choice == 'D':
        print("you chose d")
    else:
        print("\nPlease choose an option from A, B, C, or D.\n")

    return choice

        
select_search_type()