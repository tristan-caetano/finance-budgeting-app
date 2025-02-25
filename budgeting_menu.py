# Tristan Caetano
# Finance Budgeting App: Budgeting Menu
# This menu helps the user create budgeting profiles.

# Importing Python scripts
import mortgage_menu as mm

# Importing packages
import sqlite3
from os.path import exists
import pandas as pd

def budgeting_menu():

    # List of menu options
    list_of_options = ["Add Budget Profile"]
    
    # Iterator for list
    list_num = 1

    while(True):

        print("\nBudgeting Menu\n")

        # Printing out all found files to user
        for option in list_of_options:
            print(str(list_num) + ").", option), "\n"
            list_num += 1
        
        menu_in = input("\nEnter the number of the option you would like, or enter 'q' to go back to the previous menu.\n")

        if menu_in == "q" or menu_in == "Q":
            return
        elif menu_in == '2':
            mm.mortgage_menu()
        else:
            print("\nCommand not found, please input an available number or 'q'.\n")

        list_num = 1


def get_DB_data():

    # Getting DB info
    con = init_DB()
    cur = con.cursor()

    # SQL query to get all info from DB
    result = cur.execute(
        '''SELECT Name''').fetchall()

    # Returning DB data
    return result

def init_DB():

    # Name of default vinyl record CSV file
    finance_sql = "finance.db"

    # Making sure the SQL exists
    if not exists(finance_sql):
        # Connecting to DB
        con = sqlite3.connect(finance_sql)
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE budgeting_profiles(ID INT PRIMARY KEY, Name TEXT, Income TEXT, PayInterval INT)")

    else:
        # Connecting to DB
        con = sqlite3.connect(finance_sql)

    # Returning DB info
    return con


