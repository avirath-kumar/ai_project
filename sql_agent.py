import getpass
import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = getpass.getpass()

db = SQLDatabase.from_uri("sqlite:///transactions.db")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

agent_executor.invoke("Return to me the total of the amount column for transactions that have a category like Restaurants or something similar during the month of January and February 1st-6th?")

# print(db.dialect)
# print(db.get_usable_table_names())
# output = db.run("SELECT * FROM feb0625Close LIMIT 10")
# print(output)

