# Tristan Caetano
# Finance Budgeting App: Budgeting Menu
# This menu helps the user create budgeting profiles.

# Importing Python scripts
import mortgage_menu as mm
import finance_sql as fs
import profile_menu as pm

# Importing packages
import sqlite3
from os.path import exists
import pandas as pd

# Asking user to create a new profile
def create_new_profile(con):

    # Creating new dictionary for profile
    new_profile = dict()

    # Getting user name
    new_profile["name"] = input("\nEnter your name.\n\n")

    # Default value for payinterval for user input loop
    new_profile["payinterval"] = "NONE"

    list_num = 1

    # Userin loop for payinterval
    while(True):

        list_of_options = ["Weekly", "Bi-Weekly", "Monthly", "Yearly"]

        # Printing out all found files to user
        for option in list_of_options:
            print(str(list_num) + ").", option), "\n"
            list_num += 1
        list_num = 1

        menu_in = input("\nEnter the number of the option that matches your pay frequency.\n")

        if int(menu_in) < len(list_of_options):
            new_profile["payinterval"] = list_of_options[int(menu_in) - 1]
        else:  
            print("Option not found, please input an available number.\n")

        if new_profile["payinterval"] != "NONE":
            break

    new_profile["income"] = input("\nEnter your income\n")

    print("\nLength:", len(new_profile), "\n")

    fs.add_entry(new_profile, con)


def budgeting_menu():

    # List of menu options
    list_of_options = ["Add Budget Profile"]
    
    # Iterator for list
    list_num = 1

    while(True):

        # Initializing DB
        con = fs.init_DB()
        names = fs.get_profile_names(con)

        print("\nBudgeting Menu\n")

        # Printing out all found files to user
        for option in list_of_options:

            print(str(list_num) + ").", option), "\n"
            list_num += 1
        
        for name in names:
            print(str(list_num) + ").", name[1], "ID:", name[0]), "\n"
            list_num += 1
        
        menu_in = input("\nEnter the number of the option you would like, or enter 'q' to go back to the previous menu.\n")

        if menu_in == "q" or menu_in == "Q":
                return
        elif int(menu_in) < list_num and int(menu_in) > 0:
            if menu_in == '1':
                create_new_profile(con)
            else:
                pm.profile_menu(int(menu_in) - 1)
        else:
            print("\nCommand not found, please input an available number or 'q'.\n")

        list_num = 1


