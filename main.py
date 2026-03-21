import sqlite3
import os
from datetime import datetime


DB_PATH ="pocketpolice.db"


#To check if it's the first time opening the app
def first_time(DB_PATH):
    return not os.path.exists(DB_PATH)

#To setup the db for first time setup
def first_time_setup(DB_PATH):
    #take config vaariables as input
    monthly_budget = int(input("Enter monthly budget: "))
    per_task_earning = int(input("Enter per task earning: "))
    bonus = int(input("Enter daily task completion bonus: "))
    penalty = int(input("Enter weekly penalty for no tasks done: "))

    while True:
        deadline_string = input("Enter time in HH:MM format(eg: 14:30): ")
        
        try:
            deadline = datetime.strptime(deadline_string, "%H:%M").time()
            break
        except ValueError:
            print("Invalid input. Please use HH:MM")
    
    #Connect to the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    #Create config table
    c.execute('''
            CREATE TABLE IF NOT EXISTS config(
              id INTEGER PRIMARY KEY,
              monthly_budget INT,
              per_task_earning INT,
              bonus INT,
              penalty INT,
              deadline TIME
              )
    ''')

    #Creating the config entry
    insert_query = """INSERT INTO config (id, monthly_budget, per_task_earning, bonus, penalty, deadline) VALUES(?,?,?,?,?,?)"""
    c.execute(insert_query, (1,monthly_budget,per_task_earning,bonus,penalty,deadline))

    conn.commit()
    conn.close()

def startup(DB_PATH):
    if first_time(DB_PATH):
        first_time_setup(DB_PATH)
    
    else:
        load_data(DB_PATH)