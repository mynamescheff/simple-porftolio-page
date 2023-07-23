from flask import Flask, jsonify, render_template
from flask_cors import CORS 
from flask import request

app = Flask(__name__)
CORS(app)

# For development purposes only. Remove this line in production.
app.config['DEBUG'] = True

import pyodbc

DB_SERVER = ''
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''

conn_str = f'DRIVER={{SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Route to serve the index.html file for the root URL and /index.html
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/api/projects', methods=['GET'])
def get_projects():
    print('Request received for projects data.')
    query = 'SELECT * FROM Projects' 
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return jsonify(results)

# New route to handle form submission
@app.route('/api/add_project', methods=['POST'])
def add_project():
    project_name = request.form['project_name']
    description = request.form['description']
    technologies = request.form['technologies']
    project_link = request.form['project_link']
    repository_link = request.form['repository_link']

    # Code to insert the data into the SQL database
    # Use '?' as placeholders for values to avoid SQL injection
    # The 'id' column is not provided, as it will be auto-assigned
    query = "INSERT INTO Projects2 (name, description, technologies, project_link, repository_link) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (project_name, description, technologies, project_link, repository_link))
    conn.commit()

    return jsonify({'message': 'Project added successfully'})

if __name__ == '__main__':
    app.run()