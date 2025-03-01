# Tristan Caetano
# Finance Budgeting App
# Script that is the hub for where to go whether it's budgeting or mortage calculation.

# Importing packages
import budgeting_menu as bm
import mortgage_menu as mm

from os.path import exists
import pandas as pd
import glob
import os
import sys

def main_menu():
    # List of menu options
    list_of_options = ["Budgeting Menu", 
                        "Mortgage Menu",]
    
    # Iterator for list
    list_num = 1

    while(True):

        print("\nFinance Budgeting App\nMain Menu\n")

        # Printing out all found files to user
        for option in list_of_options:
            print(str(list_num) + ").", option), "\n"
            list_num += 1
        
        menu_in = input("\nEnter the number of the option you would like, or enter 'q' to quit.\n")

        if menu_in == "q" or menu_in == "Q":
            quit()
        elif menu_in == '1':
            bm.budgeting_menu()
        elif menu_in == '2':
            mm.mortgage_menu()
        else:
            print("Option not found, please input an available number or 'q'.\n")

        list_num = 1

main_menu()