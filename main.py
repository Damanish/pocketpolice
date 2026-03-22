import sqlite3
import os
from datetime import datetime

#Global entities
DB_PATH ="pocketpolice.db"
config_dict = {
    "monthly_budget":"",
    "per_task_earning":"",
    "bonus":"",
    "penalty":"",
    "deadline":""
}

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
              deadline TEXT
              )
    ''')

    #Creating the config entry
    insert_query = """INSERT INTO config (id, monthly_budget, per_task_earning, bonus, penalty, deadline) VALUES(?,?,?,?,?,?)"""
    c.execute(insert_query, (1,monthly_budget,per_task_earning,bonus,penalty,deadline_string))

    #Create task table
    c.execute('''
            CREATE TABLE IF NOT EXISTS tasks(
              id INTEGER PRIMARY KEY,
              task_name TEXT NOT NULL,
              task_date TEXT NOT NULL,
              created_at TEXT,
              completed INTEGER DEFAULT 0 CHECK (completed in (0,1)),
              completion_time TEXT,
              reward_granted INTEGER DEFAULT 0 CHECK (reward_granted in (0,1))
              )
    ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS transactions(
              id INTEGER PRIMARY KEY,
              timestamp TEXT,
              type TEXT NOT NULL,
              amount INTEGER NOT NULL,
              description TEXT,
              reference_id INTEGER
              )
    ''')

    conn.commit()
    conn.close()

    #Save the values to config dict
    config_dict["monthly_budget"] = monthly_budget
    config_dict["per_task_earning"] = per_task_earning
    config_dict["bonus"] = bonus
    config_dict["penalty"] = penalty
    config_dict["deadline"] = deadline_string

    print("First time setup completed.")

#To load necessary data when starting up
def load_data(DB_PATH):

    #Get the config values from the db
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
            SELECT * FROM config
    ''')
    row = c.fetchall()
    config_dict["monthly_budget"] = row[1]
    config_dict["per_task_earning"] = row[2]
    config_dict["bonus"] = row[3]
    config_dict["penalty"] = row[4]
    config_dict["deadline"] = row[5]
    
    conn.commit()
    conn.close()
    

def startup(DB_PATH):
    if first_time(DB_PATH):
        first_time_setup(DB_PATH)
    
    else:
        load_data(DB_PATH)