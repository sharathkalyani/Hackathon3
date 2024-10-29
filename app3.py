from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",         # Replace with your MySQL username
        password="Prem@123", # Replace with your MySQL password
        database="government_schemes"
    )
    return conn

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index3.html')

# Route to get all scheme records
@app.route('/api/schemes', methods=['GET'])
def get_schemes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM schemes')
    schemes_records = cursor.fetchall()
    conn.close()
    return jsonify(schemes_records)

# Route to add a new scheme record
@app.route('/api/schemes', methods=['POST'])
def add_scheme():
    new_scheme = request.json
    name = new_scheme['name']
    description = new_scheme['description']
    apply_link = new_scheme['apply_link']
    eligibility_criteria = new_scheme['eligibility_criteria']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO schemes (name, description, apply_link, eligibility_criteria) VALUES (%s, %s, %s, %s)',
                   (name, description, apply_link, eligibility_criteria))
    conn.commit()
    conn.close()
    return jsonify(new_scheme), 201

# Route to delete a scheme record
@app.route('/api/schemes/<int:id>', methods=['DELETE'])
def delete_scheme(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM schemes WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
