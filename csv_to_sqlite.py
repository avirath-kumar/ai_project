import sqlite3
import pandas as pd

# Step 1: read csv file as pandas df
csv_file = "02_06_25_close.csv"
df = pd.read_csv(csv_file)

# Step 2: connect to sqlite and create db file
db_file = "transactions.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Step 3: create table based on csv headers
columns = df.columns.tolist()
column_definitions = ", ".join([f'"{col}" TEXT' for col in columns]) # f string expression to create SQL data types expressions to create tables
table_name = "02_06_25_close"

create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({column_definitions})'
cursor.execute(create_table_query)

# Step 4: insert csv data into sqlite table
placeholders = ", ".join(["?"] * len(columns)) # creates list of placeholders for insertion into table
insert_query = f'INSERT INTO "{table_name}" VALUES ({placeholders})'
cursor.executemany(insert_query, df.values.tolist())

# commit to sqlite and close connection
conn.commit()
conn.close()

print(f"Data from '{csv_file}' has been successfully stored in '{db_file}'")