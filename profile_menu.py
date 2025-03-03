# Tristan Caetano
# Finance Budgeting App: Profile Menu
# This menu helps the user navigate their own profile

# Importing Python scripts
import mortgage_menu as mm
import budgeting_menu as bd
import finance_sql as fs
import expenses_menu as em

# Importing packages
import sqlite3
from os.path import exists
import pandas as pd

def profile_menu(userid):

    # Initializing DB
    con = fs.init_DB()

    query = 'SELECT * FROM budgeting_profiles WHERE ID LIKE "'+str(userid)+'"'

    curr_profile = fs.custom_query(con, query)
    
    for profile in curr_profile:
        print("\nName:", profile[1],
            "\nIncome: $" + profile[2], profile[3])
    
    
    # Iterator for list
    list_num = 1

    while(True):

        print("\nProfile Menu\n")
        list_of_options = ["View Full Profile", "Add/Remove Expenses", "Mortgage Menu"]
        list_of_options_link = [view_full_profile, em.expenses_menu, mm.mortgage_menu]

        # Printing out all found files to user
        for option in list_of_options:

            print(str(list_num) + ").", option), "\n"
            list_num += 1
        
        menu_in = input("\nEnter the number of the option you would like, or enter 'q' to go back to the previous menu.\n")

        if menu_in == "q" or menu_in == "Q":
                return
        elif int(menu_in) < list_num and int(menu_in) > 0:
            list_of_options_link[int(menu_in) - 1](userid)
        else:
            print("\nCommand not found, please input an available number or 'q'.\n")
            

        list_num = 1

def view_full_profile(userid):
     print("prof")