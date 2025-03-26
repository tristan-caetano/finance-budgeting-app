# Tristan Caetano
# Finance Budgeting App: Profile Menu
# This menu helps the user navigate their own profile, expenses, mortgage, and can display a full expense report

# Importing Python scripts
import mortgage_menu as mm
import finance_sql as fs
import expenses_menu as em
import tracking_menu as tm

# Main profile menu for the currently selected profile
def profile_menu(userid):

    # Initializing DB
    con = fs.init_DB()

    # Grabbing the name, income, and pay frequency of the user to display
    query = 'SELECT * FROM budgeting_profiles WHERE ID LIKE "'+str(userid)+'"'
    curr_profile = fs.custom_query(con, query)
    for profile in curr_profile:
        print("\nName:", profile[1],
            "\nIncome: $" + str(profile[2]), profile[3])
    
    
    # Iterator for list
    list_num = 1

    # Loop for menu
    while(True):

        print("\nProfile Menu\n")
        list_of_options = ["View Full Profile", "Add Expense", "Remove Expense", "Add Mortgage", "Remove Mortgage", "Add Tracked Payment", "Remove Tracked Payment", "View Payment Tracking Report"]
        list_of_options_link = [view_full_profile, em.add_expense, em.remove_expense, mm.add_mortgage, mm.remove_mortgage, tm.add_tracking, tm.remove_tracking, tm.view_tracking_report]

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
            
        # Resetting interator every time menu is reloaded
        list_num = 1

# Displaying the full user profile report including: user information, expenses, mortgage information, and displaying a monthly cost and how much the user will save each month and year
def view_full_profile(con, userid):
    
    # Initializing DB
    con = fs.init_DB()

    # Querying for profile and mortgage information
    profile_q = 'SELECT * FROM budgeting_profiles WHERE ID LIKE "'+str(userid)+'"'
    mortgage_q = 'SELECT * FROM mortgage_profiles WHERE ID LIKE "'+str(userid)+'"'
    profile = None
    mortgage = None
    monthly_expenses = 0
    monthly_mortgage_payment = 0

    # Beginning of the full budgeting report
    print("\n**********************START OF BUDGETING REPORT**********************\n")

    # Showing profile
    curr_profile = fs.custom_query(con, profile_q)
    for profile_c in curr_profile:
        profile = profile_c
        print("\nName:", profile[1],
            "\nIncome: $" + str(profile[2]), profile[3])
        
        # Querying, showing expenses, and getting the average monthly expense cost
        monthly_expenses = get_monthly_expenses(con, userid)


    try:
        # Showing Mortgage
        mortgages = fs.custom_query(con, mortgage_q)
        for mortgage_c in mortgages:
            mortgage = mortgage_c
            print("\n"+mortgage[1],"costs $"+str(mortgage[2]),"at an interest rate of",str(mortgage[4])+"% with a $"+str(mortgage[3]),"downpayment.")

        # Final math (oh boy)
        # Mortgage Math
        full_house_price = mortgage[2]
        downpayment = mortgage[3]
        P = full_house_price - downpayment # Principal
        i = (mortgage[4]/100) / 12 # Monthly Interest Rate
        n = 30 * 12 # 30 year fixed rate at 12 months a year
        monthly_mortgage_payment = P*((i*((1+i)**n))/(((1+i)**n)-1))
        print("Monthly Mortgage Payment: $"+str(round(monthly_mortgage_payment)))

    except:
        # If no mortages, print nothing
        print("\nNO MORTGAGES")
        monthly_mortgage_payment = 0

    # Finally combining all monthly expenses and mortgage
    all_monthly_expenses = monthly_expenses + monthly_mortgage_payment
    
    # Income math
    # Calculating cost based on monthly expenses
    monthly_income = profile[2]
    if profile[3] == "Weekly": monthly_income = ((profile[2] * 52) / 12)
    elif profile[3] == "Bi-Weekly": monthly_income = ((profile[2] * 26) / 12)
    elif profile[3] == "Yearly": monthly_income = (profile[2] / 12)
    
    # Displaying final information
    print("\nTotal Monthly Expenses: $"+str(round(all_monthly_expenses, 2)))
    print("Based on your income, you will have: $"+str(round(monthly_income - all_monthly_expenses, 2)),"leftover each month, and $"+ str(round((monthly_income - all_monthly_expenses)*12, 2)),"at the end of each year.")
    print("\n***********************END OF BUDGETING REPORT***********************\n")

# Sub function to grab monthly expenses, without the extra stuff we dont need (this will be deleted later.)
def get_monthly_expenses(con, userid):
     # Displaying all expenses organized by frequency
    cost_frequencies = ["Weekly", "Bi-Weekly", "Monthly", "Yearly"]

    # This value keeps track of all monthly spending
    running_total = 0

    # Printing out all expenses organized by their pay frequency
    for frequency in cost_frequencies:

        # Getting expenses per frequency for the current profile
        query = 'SELECT * FROM expense_profiles WHERE ID LIKE "'+str(userid)+'" AND payinterval like "'+str(frequency)+'"'
        expenses = fs.custom_query(con, query)
        
        # Keeping track if the frequency header was printed yet
        printed_freq = 0

        running_total_freq = 0
        
        # Print relevant expenses
        for expense in expenses:

            # Printing frequency header if its the first object
            if printed_freq == 0:
                print("\n" + frequency, "Expenses:")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                printed_freq = 1
            print(expense[1] + ", $"+str(expense[2]))
            running_total_freq += expense[2]
        
        # Calculating cost based on monthly expenses
        if frequency == "Weekly": running_total += ((running_total_freq * 52) / 12)
        elif frequency == "Bi-Weekly": running_total += ((running_total_freq * 26) / 12)
        elif frequency == "Monthly": running_total += running_total_freq
        elif frequency == "Yearly": running_total += (running_total_freq / 12)

    # Printing running total for monthly average expenses
    print("\n*********************************************************************")
    print("Sum of average monthly expenses: $" + str(round(running_total,2)))

    # Retuning the monthly average expenses to be combined with calculated monthly mortgage payment
    return running_total