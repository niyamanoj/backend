from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL Database Connection
db = pymysql.connect(
    host="localhost",  # Change for production
    user="root",
    password="root",
    database="care_to_cure"
)
cursor = db.cursor()

# ------------------- USER AUTHENTICATION -------------------

def authenticate_user(table, email, password):
    query = f"SELECT * FROM {table} WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    return user

@app.route('/login_patient', methods=['POST'])
def login_patient():
    data = request.json
    email = data['email']
    password = data['password']
    
    user = authenticate_user('Patient', email, password)
    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/login_doctor', methods=['POST'])
def login_doctor():
    data = request.json
    email = data['email']
    password = data['password']
    
    user = authenticate_user('Doctor', email, password)
    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/login_family', methods=['POST'])
def login_family():
    data = request.json
    email = data['email']
    password = data['password']
    
    user = authenticate_user('Family', email, password)
    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]})
    return jsonify({"message": "Invalid credentials"}), 401

# ------------------- USER REGISTRATION -------------------

@app.route('/register_patient', methods=['POST'])
def register_patient():
    data = request.json
    query = "INSERT INTO Patient (name, email, phone_number, password, disease) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (data['name'], data['email'], data['phone_number'], data['password'], data['disease']))
    db.commit()
    return jsonify({"message": "Patient registered successfully!"})

@app.route('/register_doctor', methods=['POST'])
def register_doctor():
    data = request.json
    query = "INSERT INTO Doctor (name, email, phone_number, password, specialization) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (data['name'], data['email'], data['phone_number'], data['password'], data['specialization']))
    db.commit()
    return jsonify({"message": "Doctor registered successfully!"})

@app.route('/register_family', methods=['POST'])
def register_family():
    data = request.json
    query = "INSERT INTO Family (name, email, phone_number, password) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (data['name'], data['email'], data['phone_number'], data['password']))
    db.commit()
    return jsonify({"message": "Family member registered successfully!"})

# ------------------- RUNNING THE API -------------------

if __name__ == '__main__':
    app.run()
