from flask import Flask, request, render_template_string
import getpass
import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

app = Flask(__name__)

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = getpass.getpass(prompt="Enter your OpenAI API key: ")

# Connect to the SQLite database
db = SQLDatabase.from_uri("sqlite:///transactions.db")

# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Create the SQL agent
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

# HTML template for the web page
html_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>SQL Agent Query</title>
  </head>
  <body>
    <h1>SQL Agent Query</h1>
    <form method="post">
      <label for="query">Enter your query:</label><br>
      <input type="text" id="query" name="query" required><br><br>
      <input type="submit" value="Submit">
    </form>
    {% if result %}
      <h2>Query Result:</h2>
      <p>{{ result }}</p>
    {% endif %}
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        query = request.form['query']
        try:
            result = agent_executor.invoke(query)
        except Exception as e:
            result = f"An error occurred: {e}"
    return render_template_string(html_template, result=result)

if __name__ == '__main__':
    app.run(debug=True)

# print(db.dialect)
# print(db.get_usable_table_names())
# output = db.run("SELECT * FROM feb0625Close LIMIT 10")
# print(output)

