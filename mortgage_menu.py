# Tristan Caetano
# Finance Budgeting App: Mortgage Menu
# This menu helps the user manage their mortgage information

# Importing Python scripts
import finance_sql as fs

# Main mortgage menu where the user can add, remove, or view current mortgages
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

# Adding mortgage to current user profile 
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

    # Adding mortgage information to database
    fs.add_mortgage_DB(new_mortgage, con)

# Removing mortgage from the current user profile
def remove_mortgage(con, userid):
    cur = con.cursor()

    while(True):

        # Getting user name
        mortgage = input("\nEnter the name of the mortgage you would like to delete, enter q to quit.\n\n")

        # Quitting
        if mortgage == "q" or mortgage == "Q":
            return

        # Getting mortgages per frequency for the current profile
        query = 'SELECT * FROM mortgage_profiles WHERE ID LIKE "'+str(userid)+'" AND name like "'+mortgage+'"'
        
         # Try except block in case an error is thrown
        try:

            # Getting data for specified mortgage
            mortgages = fs.custom_query(con, query)

            # Printing queried mortgage
            for an_mortgage in mortgages:
                print(an_mortgage[1] + ",",an_mortgage[2])

            # Printing recieved data to user can verify
            user_in = input("Is this correct?\n(Y) or (y) for yes, any other character for no.\n")

        except:
            # If the specified mortgage cannot be found
            print("\nCannot find mortgage using that search.\n")

        # If the user verified the album grabbed was correct, proceed
        if(user_in == "y" or user_in == "Y"):
            # Query that deletes 1 record for a specific album by name
            query = 'DELETE FROM mortgage_profiles WHERE name LIKE "'+mortgage+'" AND ID LIKE "'+str(userid)+'"'

            # Executing the query and saving changes
            cur.execute(query)
            con.commit()
            return

# Displays relavent mortgage information for current user
def view_mortgage(con, userid):
    
    # Getting mortgages per frequency for the current profile
    query = 'SELECT * FROM mortgage_profiles WHERE ID LIKE "'+str(userid)+'"'
    mortgages = fs.custom_query(con, query)
    
    # Mortgage header
    print("Current Mortgages:\n")

    # Print relevant mortgages
    for mortgage in mortgages:
        print(mortgage[1],"costs $"+str(mortgage[2]),"at an interest rate of",str(mortgage[4])+"% with a $"+str(mortgage[3]),"downpayment.")