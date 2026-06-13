from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

# MySQL Connection (Render + Production Safe)
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():

    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    db = get_db_connection()
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)