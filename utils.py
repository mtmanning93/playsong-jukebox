"""
Constants and imports
"""
import time
import datetime
import sys
import os
import gspread
import validators

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
SHEET = GSPREAD_CLIENT.open('JukeboX')
JUKEBOX = SHEET.worksheet('library')
LIBRARY = SHEET.worksheet('library').get_all_values()[1:]
TODAY = datetime.date.today()
YEAR = TODAY.year

GENRE_LIST = JUKEBOX.col_values(3)[1:]

SEARCH_MENU = {
    'A': 'Artist Name',
    'B': 'Song Title',
    'C': 'Genre',
    'D': 'Year'
}