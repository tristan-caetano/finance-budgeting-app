# Tristan Caetano
# Finance Budgeting App: Expenses Menu
# This menu allows the user to manage their expenses.

# Importing Python scripts
import budgeting_menu as bd
import finance_sql as fs
import mortgage_menu as mm

# Importing packages
import sqlite3
from os.path import exists
import pandas as pd

# Asking user to create a new profile
def add_expense(con, userid):

    # Creating new dictionary for profile
    new_expense = dict()

    # Adding userid to dict
    new_expense["ID"] = userid

    # Getting user name
    new_expense["name"] = input("\nEnter the name of the expense.\n\n")

    # Default value for payinterval for user input loop
    new_expense["payinterval"] = "NONE"

    list_num = 1

    # Userin loop for payinterval
    while(True):

        list_of_options = ["Weekly", "Bi-Weekly", "Monthly", "Yearly"]

        # Printing out all found files to user
        for option in list_of_options:
            print(str(list_num) + ").", option), "\n"
            list_num += 1
        list_num = 1

        menu_in = input("\nEnter the number of the option that matches how often you must pay this expense.\n")

        if int(menu_in) <= len(list_of_options):
            new_expense["payinterval"] = list_of_options[int(menu_in) - 1]
        else:  
            print("Option not found, please input an available number.\n")

        if new_expense["payinterval"] != "NONE":
            break

    new_expense["income"] = input("\nEnter the cost.\n")
    fs.add_expense_DB(new_expense, con)


def expenses_menu(userid):

    # Initializing DB
    con = fs.init_DB()

    # List of menu options
    list_of_options = ["Add Expense", "Remove Expense", "View Expense Report"]
    list_of_options_link = [add_expense, remove_expense, view_expense_report]

    # Printing User Profile
    query = 'SELECT * FROM budgeting_profiles WHERE ID LIKE "'+str(userid)+'"'
    curr_profile = fs.custom_query(con, query)
    for profile in curr_profile:
        print("\nName:", profile[1],
            "\nIncome: $" + profile[2], profile[3])
    
    # Iterator for list
    list_num = 1

    while(True):

        print("\nExpense Menu\n")

        # Printing out all found files to user
        for option in list_of_options:

            print(str(list_num) + ").", option), "\n"
            list_num += 1
        
        menu_in = input("\nEnter the number of the option you would like, or enter 'q' to go back to the previous menu.\n")

        if menu_in == "q" or menu_in == "Q":
                return
        elif int(menu_in) < list_num and int(menu_in) > 0:
            list_of_options_link[int(menu_in) - 1](con, userid)
        else:
            print("\nCommand not found, please input an available number or 'q'.\n")

        list_num = 1

def remove_expense():
    print("remove")
def view_expense_report():
    print("view")





