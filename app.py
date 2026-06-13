from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="portfolio_db"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():

    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    cursor = db.cursor()

    sql = """
    INSERT INTO contacts(name, email, message)
    VALUES (%s, %s, %s)
    """

    values = (name, email, message)

    cursor.execute(sql, values)
    db.commit()

    cursor.close()

    return "Message Submitted Successfully! Data stored in MySQL."

if __name__ == '__main__':
    app.run(debug=True)