# app.py

# Import the 'Flask' class from the 'flask' library.
import psycopg2, psycopg2.extras
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

import os


# Initialize Flask
# We'll use the pre-defined global '__name__' variable to tell Flask where it is.
app = Flask(__name__)

def get_db_connection():
    connection = psycopg2.connect(
        host='localhost',
        database='pets_db',
        # user=os.environ['POSTGRES_USER'],
        # password=os.environ['POSTGRES_PASSWORD']
    )
    return connection

# Define our route
# This syntax is using a Python decorator, which is essentially a succinct way to wrap a function in another function.

@app.route('/pets')
def index():
  try:
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM pets;")
    pets = cursor.fetchall()
    connection.close()
    return pets
  except:
     return "Application Error", 500

@app.route('/pets', methods=['POST'])
def create_pet():
  try:
    new_pet = request.json
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("INSERT INTO pets (name, age, breed) VALUES (%s, %s, %s) RETURNING *",
                   (new_pet['name'], new_pet['age'], new_pet['breed']))
    created_pet = cursor.fetchone()
    connection.commit() # Commit changes to the database
    connection.close()
    return created_pet, 201
  except Exception as e:
     return str(e), 500

@app.route('/pets/<pet_id>', methods=['GET'])
def show_pet(pet_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM pets WHERE id = %s", (pet_id,))
        pet = cursor.fetchone()
        if pet is None:
            connection.close()
            return "Pet Not Found", 404
        connection.close()
        return pet, 200
    except Exception as e:
        return str(e), 500

# Run our application, by default on port 5000
app.run()
