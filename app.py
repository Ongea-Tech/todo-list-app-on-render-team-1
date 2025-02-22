from flask import Flask, render_template, request, redirect
import psycopg2
import os

# Initialize Flask app
app = Flask(__name__)

# Get database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Create a connection to the database
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode='require'
    )

# Function to fetch the latest name
def get_latest_name():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM users ORDER BY id DESC LIMIT 1;")  # Get the last entered name
    name = cur.fetchone()
    cur.close()
    conn.close()
    return name[0] if name else "No name found"

# Function to insert a name into the database
def save_name(name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s);", (name,))
    conn.commit()
    cur.close()
    conn.close()

# Home route (GET & POST)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':  # If form is submitted
        name = request.form['name']
        save_name(name)  # Save name to DB
        return redirect('/')  # Refresh page to show updated name

    latest_name = get_latest_name()
    return render_template('index.html', name=latest_name)

if __name__ == '__main__':
    app.run(debug=True)