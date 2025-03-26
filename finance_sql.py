# Tristan Caetano
# Finance Budgeting App: SQL File
# This script contains all SQL query functions

# Importing packages
import sqlite3
from os.path import exists

# Custom query so that I dont need to make a function for every query type
def custom_query(con, query):
    cur = con.cursor()
    result = cur.execute(query)

    # Returning DB data
    return result

# Query to get all profile names
def get_profile_names(con):
    cur = con.cursor()

    # Query to get record info for 1 specific album by name
    query = 'SELECT ID, name FROM budgeting_profiles'
    result = cur.execute(query)

    # Returning DB data
    return result

# Adding new profile to DB
def add_entry(record, con):

    # Getting DB info
    cur = con.cursor()

    # Sending 1 entry to the DB
    cur.executemany("INSERT INTO budgeting_profiles (name, income, payinterval) VALUES (:name, :income, :payinterval)", (record, ))

    # Saving database info
    con.commit()

# Adding new expense to DB
def add_expense_DB(record, con):

    # Getting DB info
    cur = con.cursor()

    # Sending 1 entry to the DB
    cur.executemany("INSERT INTO expense_profiles (ID, name, cost, payinterval) VALUES (:ID, :name, :cost, :payinterval)", (record, ))

    # Saving database info
    con.commit()

# Adding new tracking to DB
def add_tracking_DB(record, con):

    # Getting DB info
    cur = con.cursor()

    # Sending 1 entry to the DB
    cur.executemany("INSERT INTO tracking_profiles (ID, name, cost, day, month, year ) VALUES (:ID, :name, :cost, :day, :month, :year)", (record, ))

    # Saving database info
    con.commit()


# Adding new mortgage to DB
def add_mortgage_DB(record, con):

    # Getting DB info
    cur = con.cursor()

    # Sending 1 entry to the DB
    cur.executemany("INSERT INTO mortgage_profiles (ID, name, cost, downpayment, interestrate) VALUES (:ID, :name, :cost, :downpayment, :interestrate)", (record, ))

    # Saving database info
    con.commit()

# Getting all DB data
def get_DB_data(con):

    # Getting DB info
    cur = con.cursor()

    # SQL query to get all info from DB
    result = cur.execute(
        '''SELECT Name''').fetchall()

    # Returning DB data
    return result

# Initializing database
def init_DB():

    # Name of default vinyl record CSV file
    finance_sql = "finance.db"

    # Making sure the SQL exists
    if not exists(finance_sql):
        # Connecting to DB
        con = sqlite3.connect(finance_sql)
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE budgeting_profiles(ID INTEGER PRIMARY KEY, name TEXT, income REAL, payinterval TEXT)")
        cur.execute(
            "CREATE TABLE expense_profiles(ID INTEGER, name TEXT, cost REAL, payinterval TEXT)")
        cur.execute(
            "CREATE TABLE mortgage_profiles(ID INTEGER, name TEXT, cost REAL, downpayment REAL, interestrate REAL)")
        cur.execute(
            "CREATE TABLE tracking_profiles(ID INTEGER, name TEXT, cost REAL, day INTEGER, month INTEGER, year INTEGER)")

    else:
        # Connecting to DB
        con = sqlite3.connect(finance_sql)

    # Returning DB info
    return con