from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

# Safe DB connection (won't crash app if DB fails)
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
    except Exception as e:
        print("DB CONNECTION ERROR:", e)
        return None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact', methods=['POST'])
def contact():

    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    try:
        db = get_db_connection()

        # If DB not available, don't crash
        if db is None:
            print("Database not connected. Data not saved.")
            return "Message received (DB not connected)"

        cursor = db.cursor()

        sql = """
        INSERT INTO contacts(name, email, message)
        VALUES (%s, %s, %s)
        """

        values = (name, email, message)

        cursor.execute(sql, values)
        db.commit()

        cursor.close()
        db.close()

        return "Message Submitted Successfully!"

    except Exception as e:
        print("ERROR:", e)
        return "Something went wrong while saving data"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)