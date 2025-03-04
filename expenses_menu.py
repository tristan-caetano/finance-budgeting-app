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

# Remove specified expense by name
def remove_expense(con, userid):
    cur = con.cursor()

    while(True):

        # Getting user name
        expense = input("\nEnter the name of the expense you would like to delete, enter q to quit.\n\n")

        if expense == "q" or expense == "Q":
            return

        # Getting expenses per frequency for the current profile
        query = 'SELECT * FROM expense_profiles WHERE ID LIKE "'+str(userid)+'" AND name like "'+expense+'"'
        
         # Try except block in case an error is thrown
        try:

            # Getting data for specified expense
            expenses = fs.custom_query(con, query)

            for an_expense in expenses:
                print(an_expense[1] + ",",an_expense[2])

            # Printing recieved data to user can verify
            user_in = input("Is this correct?\n(Y) or (y) for yes, any other character for no.\n")

        except:
            print("\nCannot find expense using that search.\n")

         # If the user verified the album grabbed was correct, proceed
        if(user_in == "y" or user_in == "Y"):
            # Query that deletes 1 record for a specific album by name
            query = 'DELETE FROM expense_profiles WHERE name LIKE "'+expense+'" AND ID LIKE "'+str(userid)+'"'

            # Executing the query and saving changes
            cur.execute(query)
            con.commit()
            return

# Print all expenses for current profile
def view_expense_report(con, userid):

    # Displaying all expenses organized by frequency
    cost_frequencies = ["Weekly", "Bi-Weekly", "Monthly", "Yearly"]
    for frequency in cost_frequencies:

        # Getting expenses per frequency for the current profile
        query = 'SELECT * FROM expense_profiles WHERE ID LIKE "'+str(userid)+'" AND payinterval like "'+str(frequency)+'"'
        expenses = fs.custom_query(con, query)
        
        # Keeping track if the frequency header was printed yet
        printed_freq = 0

        running_total_freq = 0
        running_total = 0
        
        # Print relevant expenses
        for expense in expenses:

            # Printing frequency header if its the first object
            if printed_freq == 0:
                print("\n" + frequency, "Expenses:")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                printed_freq = 1
            print(expense[1] + ",",expense[2])
            running_total_freq += expense[2]
        
        if printed_freq == 1:
            # Printing running total
            print("_____________________________________________________________________")
            print("Sum of", frequency, "Expenses: $" + str(running_total_freq))
        
        # Calculating cost based on monthly expenses
        if frequency == "Weekly": running_total += ((running_total_freq * 52) / 12)
        elif frequency == "Bi-Weekly": running_total += ((running_total_freq * 26) / 12)
        elif frequency == "Monthly": running_total += running_total_freq
        elif frequency == "Yearly": running_total += (running_total_freq / 12)

    # Printing running total for monthly average expenses
    print("*********************************************************************")
    print("Sum of average monthly expenses: $" + str(running_total))





