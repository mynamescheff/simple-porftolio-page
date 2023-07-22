from flask import Flask, jsonify, render_template
from flask_cors import CORS 

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

if __name__ == '__main__':
    app.run()