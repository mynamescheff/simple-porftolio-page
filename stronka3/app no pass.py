from flask import Flask, jsonify, render_template
from flask_cors import CORS 
from flask import request
import hashlib


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


@app.route('/api/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    pin_number = request.form['pin_number']
    character_deletion_number = request.form['character_deletion_number']

    # Check if the username already exists
    if check_username_exists(username):
        return jsonify({'error': 'Username already exists. Please choose a different username.'})

    # Validate input lengths
    if len(username) > 20:
        return jsonify({'error': 'Username must be up to 20 characters'})
    if len(password) > 40:
        return jsonify({'error': 'Password must be up to 40 characters'})
    if len(pin_number) != 4 and len(pin_number) != 5:
        return jsonify({'error': 'PIN number must be 4 or 5 characters'})
    if len(character_deletion_number) != 7:
        return jsonify({'error': 'Character deletion number must be 7 characters'})

    # Hash the password for security before storing it in the database
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Code to insert the user data into the 'Logins' table
    query = "INSERT INTO Logins (username, password, pin_number, character_deletion_number) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (username, hashed_password, pin_number, character_deletion_number))
    conn.commit()

    # Create a styled response message as an HTML string
    response_message = """
        <h2>Signup Successful</h2>
        <p>Thank you for signing up! Your account has been created successfully.</p>
        <p>Username: {}</p>
        <p>PIN Number: {}</p>
        <p>Character Deletion Number: {}</p>
    """.format(username, pin_number, character_deletion_number)

    # Return the response message as part of the JSON response
    return jsonify({'message': response_message, 'username': username, 'pin_number': pin_number, 'character_deletion_number': character_deletion_number})

def check_username_exists(username):
    # Query the 'Logins' table to check if the username already exists
    query = "SELECT COUNT(*) FROM Logins WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    # If the username count is greater than 0, it already exists
    return result[0] > 0

if __name__ == '__main__':
    app.run()