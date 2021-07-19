"""
    File name: constants.py
    Author: Timothy Clark
    Date created: 6/24/2021
    Date last modified: 6/26/2021
    Python Version: 3.8

    Description: holds constant variables to be used throughout the project
"""
import os
# alpaca API Constants
API_KEY = ""
API_SECRET_KEY = ""
MARKET = 'https://paper-api.alpaca.markets'

# SQLite connection Constants
SQL_DB_NAME = os.getcwd()+"\\transactions.db"

#celery configuration Constants (redis port)
CELERY_RESULT_BACKEND = ''
CELERY_BROKER_URL=''

LOGO_PATH= "assets/Alpine_png_white-removebg-preview.png"
