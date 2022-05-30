"""
    File name: constants.py
    Author: Timothy Clark
    Date created: 6/24/2021
    Date last modified: 5/29/2021
    Python Version: 3.9

    Description: holds constant variables to be used throughout the project
"""
import os
# alpaca API Constants
API_KEY = ""
API_SECRET_KEY = ""
MARKET = 'https://paper-api.alpaca.markets'

# SQLite connection Constants
SQL_DB_NAME = os.getcwd()+"\\transactions.db"

LOGO_PATH= "assets/Alpine_png_white-removebg-preview.png"

# Contstants required for email functionality
SENDER = ''
RECIEVER = ''
PSSWD =''