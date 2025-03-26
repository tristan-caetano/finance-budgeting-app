# Tristan Caetano
# Finance Budgeting App: Tracking Menu
# This menu allows the user to manage their payments as they make them month to month.

# Importing Python scripts
import finance_sql as fs
from datetime import datetime

# Asking user to create a new profile
def add_tracking(con, userid):

    # Creating new dictionary for profile
    new_payment = dict()

    # day INTEGER, month INTEGER, year INTEGER

    # Adding userid to dict
    new_payment["ID"] = userid

    # Getting user name
    new_payment["name"] = input("\nEnter the name of the payment.\n\n")

    # Asking user how much this payment costs
    new_payment["cost"] = input("\nEnter the cost.\n")

    # Getting todays date for user payment by default   
    new_payment["day"] = int(datetime.today().strftime('%d'))
    new_payment["month"] = int(datetime.today().strftime('%m'))
    new_payment["year"] = int(datetime.today().strftime('%Y'))

    # Asking the user when they made their payment for month to month tracking
    while(True):
        
        print("\nWas the payment made today?", str(datetime.today().strftime('%d-%m-%Y')) ,"\nType 'y' to set the date automatically, type anything else to set it manually.\n")
        user_in = input()

        if user_in != "y" or user_in != "Y":
            new_payment["day"] = input("\nEnter the day as a number.\n")
            new_payment["month"] = input("\nEnter the month as a number.\n")
            new_payment["year"] = input("\nEnter the year as a 4 digit number.\n")
            break
        else:
            break

    # Submitting payment info to database
    fs.add_tracking_DB(new_payment, con)

# Remove specified payment by name
def remove_tracking(con, userid):

    cur = con.cursor()

    print("\nYou can only edit tracking for the CURRENT month.\nRetroactive tracking is currently not implemented.\n")

    # Getting current month and year for query
    curr_month = str(datetime.today().strftime('%m'))
    curr_year = str(datetime.today().strftime('%Y'))

    while(True):

        # Getting user name
        payment = input("\nEnter the name of the tracked payment you would like to delete, enter q to quit.\n\n")

        if payment == "q" or payment == "Q":
            return

        # Getting payments per frequency for the current profile
        query = 'SELECT * FROM tracking_profiles WHERE ID LIKE "'+str(userid)+'" AND name like "'+payment+'" AND month like "'+month+'" AND year like "'+year+'"'
        
         # Try except block in case an error is thrown
        try:

            # Getting data for specified payment
            payments = fs.custom_query(con, query)

            for an_payment in payments:
                print(an_payment[1] + ",",an_payment[2])

            # Printing recieved data to user can verify
            user_in = input("Is this correct?\n(Y) or (y) for yes, any other character for no.\n")

        except:
            print("\nCannot find payment using that search.\n")

         # If the user verified the album grabbed was correct, proceed
        if(user_in == "y" or user_in == "Y"):
            # Query that deletes 1 record for a specific album by name
            query = 'DELETE FROM payment_profiles WHERE name LIKE "'+payment+'" AND ID LIKE "'+str(userid)+'" AND month like "'+month+'" AND year like "'+year+'"'

            # Executing the query and saving changes
            cur.execute(query)
            con.commit()
            return

# Print all payments for current profile
def view_tracking_report(con, userid):

    # Showing profile
    # Grabbing the name, income, and pay frequency of the user to display
    query = 'SELECT * FROM budgeting_profiles WHERE ID LIKE "'+str(userid)+'"'
    curr_profile = fs.custom_query(con, query)
    for profile in curr_profile:
        print("\nName:", profile[1],
            "\nIncome: $" + str(profile[2]), profile[3])

    print("\nThe current date is:", str(datetime.today().strftime('%B %d, %Y')), "\nThese are the current expenses for", str(datetime.today().strftime('%B')), "\n")
    print("_____________________________________________________________________")

    # Getting current month and year for query
    curr_month = str(int(datetime.today().strftime('%m')))
    curr_year = str(datetime.today().strftime('%Y'))

    # Keeping a running total of how much was spent this month
    running_total = 0

    # Getting payments per frequency for the current profile
    query = 'SELECT * FROM tracking_profiles WHERE ID LIKE "'+str(userid)+'" AND month like "'+curr_month+'" AND year like "'+curr_year+'"'
    payments = fs.custom_query(con, query)
    
    # Print relevant payments for this month
    for payment in payments:
        print(payment[1] + ", $"+str(payment[2]), "paid on:", str(payment[4])+"-"+str(payment[3])+"-"+str(payment[5]))
        running_total += payment[2]
    
    # Income math
    # Calculating cost based on monthly expenses
    monthly_income = profile[2]
    if profile[3] == "Weekly": monthly_income = ((profile[2] * 52) / 12)
    elif profile[3] == "Bi-Weekly": monthly_income = ((profile[2] * 26) / 12)
    elif profile[3] == "Yearly": monthly_income = (profile[2] / 12)

    # How much money I have left to spend this month
    money_left = monthly_income - running_total

    # Printing running total for monthly average payments
    print("_____________________________________________________________________")
    print("This month you spent $"+str(round(running_total,2)) , "\nYou have $" + str(round(money_left,2)), "left to spend this month.\n")