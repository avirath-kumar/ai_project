import pandas as pd
import mysql.connector

# DEFINE FUNCTIONS
# defining a function that takes in a CSV filepath and returns a python list of dictionaries
def read_csv(filePath):
    df = pd.read_csv(filePath)
    return df.to_dict(orient="records")

# defining a function that creates a database
def create_database(db_name, host="localhost", user="root", password=""):
    conn = mysql.connector.connect(host=host, user=user, password=password)
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Database '{db_name}' created sucessfully")

    cursor.close()
    conn.close()

# function to create a table in the db
def create_table(db_name, table_name, csv_data, host="localhost", user="root", password=""):
    conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = conn.cursor()

    # get column names and define data types
    columns = csv_data[0].keys()
    column_definitions = ", ".join([f"{col} VARCHAR(255)" for col in columns]) # programmatically create the SQL query for creating the table names

    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})" # create table query using inputs
    cursor.execute(create_table_query)
    print(f"Table '{table_name}' created successfully!")

    cursor.close()
    conn.close()

# function to insert csv data into table
def insert_data(db_name, table_name, csv_data, host="localhost", user="root", password=""):
    conn = mysql.connector.connect(host=host, user=user, password=password, database=db_name)
    cursor = conn.cursor()

    # get column names
    columns = ", ".join(csv_data[0].keys())
    placeholders = ", ".join(["%s"] * len(csv_data[0]))

    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # convert dict values to tuple format
    values = [tuple(row.values()) for row in csv_data] # creating a tuple of all of the csv values

    cursor.executemany(insert_query, values) # bulk insert
    conn.commit()

    print(f"Inserted {cursor.rowcount} rows into '{table_name}'")

    cursor.close()
    conn.close()



# CALL FUNCTIONS
# call csv_read function -> reads CSV file into python
csv_data = read_csv("02_06_25_close.csv")

# call create_database function (prints success message) -> creates mysql db
create_database("transactions_db")

# call create_table function (prints success message) -> creates a new table using CSV headers
create_table("transactions_db", "02_06_25_close", csv_data)

# call insert_data function (prints success message) -> inserts CSV data into the table
insert_data("transactions_db", "02_06_25_close", csv_data)