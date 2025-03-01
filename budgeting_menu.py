# Tristan Caetano
# Finance Budgeting App: Budgeting Menu
# This menu helps the user create budgeting profiles.

# Importing Python scripts
import mortgage_menu as mm

# Importing packages
import sqlite3
from os.path import exists
import pandas as pd

def add_entry(record, con):

    # Getting DB info
    cur = con.cursor()

    # Sending 1 entry to the DB
    cur.execute("INSERT INTO budgeting_profiles(name, income, payinterval) VALUES(?, ?, ?)", record)

    # Saving database info
    con.commit()


def create_new_profile(con):

    new_profile = {}

    new_profile[0] = input("\nEnter your name.\n\n")

    new_profile[2] = "NONE"

    list_num = 1

    while(True):

        list_of_options = {"Weekly", "Bi-Weekly", "Monthly"}

        # Printing out all found files to user
        for option in list_of_options:
            print(str(list_num) + ").", option), "\n"
            list_num += 1

        menu_in = input("\nEnter the number of the option that matches your pay frequency.\n")
        
        if menu_in == '1':
            new_profile[2] = "Weekly"
        elif menu_in == '2':
            new_profile[2] = "Bi-Weekly"
        elif menu_in == '3':
            new_profile[2] = "Monthly"
        else:
            print("Option not found, please input an available number.\n")

        list_num = 1

        if new_profile[2] != "NONE":
            break

    new_profile[1] = input("\nEnter your income\n")

    add_entry(new_profile, con)


def budgeting_menu():

    # Initializing DB
    con = init_DB()

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
        elif menu_in == '1':
            create_new_profile(con)
        else:
            print("\nCommand not found, please input an available number or 'q'.\n")

        list_num = 1


def get_DB_data(con):

    # Getting DB info
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
            "CREATE TABLE budgeting_profiles(ID INT PRIMARY KEY, name TEXT, income TEXT, payinterval INT)")

    else:
        # Connecting to DB
        con = sqlite3.connect(finance_sql)

    # Returning DB info
    return con


