# Tristan Caetano
# Finance Budgeting App: Mortgage Menu
# This menu helps the user manage their mortgage information

# Importing Python scripts
import budgeting_menu as bd
import finance_sql as fs

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


def mortgage_menu(userid):

    # Initializing DB
    con = fs.init_DB()

    # List of menu options
    list_of_options = ["Add Mortgage", "Remove Mortgage", "View Mortgages"]
    list_of_options_link = [add_mortgage, remove_mortgage, view_mortgage]

    # Printing User Profile
    query = 'SELECT * FROM budgeting_profiles WHERE ID LIKE "'+str(userid)+'"'
    curr_profile = fs.custom_query(con, query)
    for profile in curr_profile:
        print("\nName:", profile[1],
            "\nIncome: $" + str(profile[2]), profile[3])
    
    # Iterator for list
    list_num = 1

    while(True):

        print("\nMortgage Menu\n")

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

def add_mortgage(con, userid):
     # Creating new dictionary for profile
    new_mortgage = dict()

    # Adding userid to dict
    new_mortgage["ID"] = userid

    # Getting mortgage name
    new_mortgage["name"] = input("\nEnter the name of the mortgage.\n\n")

    # Getting cost of the property
    new_mortgage["cost"] = input("\nEnter the full cost of the property.\n\n")

    # Getting how much the user is putting down
    new_mortgage["downpayment"] = input("\nEnter your downpayment.\n")

    # Getting the interest rate
    new_mortgage["interestrate"] = input("\nEnter your quoted interest rate.\n")

    fs.add_mortgage_DB(new_mortgage, con)

def remove_mortgage(con, userid):
    cur = con.cursor()

    while(True):

        # Getting user name
        mortgage = input("\nEnter the name of the mortgage you would like to delete, enter q to quit.\n\n")

        if mortgage == "q" or mortgage == "Q":
            return

        # Getting mortgages per frequency for the current profile
        query = 'SELECT * FROM mortgage_profiles WHERE ID LIKE "'+str(userid)+'" AND name like "'+mortgage+'"'
        
         # Try except block in case an error is thrown
        try:

            # Getting data for specified mortgage
            mortgages = fs.custom_query(con, query)

            for an_mortgage in mortgages:
                print(an_mortgage[1] + ",",an_mortgage[2])

            # Printing recieved data to user can verify
            user_in = input("Is this correct?\n(Y) or (y) for yes, any other character for no.\n")

        except:
            print("\nCannot find mortgage using that search.\n")

         # If the user verified the album grabbed was correct, proceed
        if(user_in == "y" or user_in == "Y"):
            # Query that deletes 1 record for a specific album by name
            query = 'DELETE FROM mortgage_profiles WHERE name LIKE "'+mortgage+'" AND ID LIKE "'+str(userid)+'"'

            # Executing the query and saving changes
            cur.execute(query)
            con.commit()
            return

def view_mortgage(con, userid):
    
    # Getting mortgages per frequency for the current profile
    query = 'SELECT * FROM mortgage_profiles WHERE ID LIKE "'+str(userid)+'"'
    mortgages = fs.custom_query(con, query)
    
    # Mortgage header
    print("Current Mortgages:\n")

    # Print relevant mortgages
    for mortgage in mortgages:
        print(mortgage[1],"costs $"+str(mortgage[2]),"at an interest rate of",str(mortgage[4])+"% with a $"+str(mortgage[3]),"downpayment.")




