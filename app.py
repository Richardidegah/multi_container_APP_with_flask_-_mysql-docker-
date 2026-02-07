from flask import Flask
import mysql.connector
import time

app = Flask(__name__)

DB_CONFIG = {
    "host": "db",
    "user": "user",
    "password": "password",
    "database": "testdb"
}

# function to connect to database
def get_db_connection():
    # retry logic if any error happens
    for i in range(10):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except:
            print("Waiting for database...")
            time.sleep(3)

    raise Exception("database connection failed")


# first endpoint
@app.route("/")
def read_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()     # ✅ FIX (was connection.close())

    return {
        "messages": rows
    }


# second endpoint
# when called, this endpoint creates a table and inserts a new row into the database if it doesnt exist
@app.route("/add")
def add_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text VARCHAR(255)
        )
    """)

    cursor.execute(
        "INSERT INTO messages(text) VALUES ('Hello from Docker + mysql!')"
    )

    conn.commit()
    cursor.close()
    conn.close()

    return "message inserted into the database"


# to run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
