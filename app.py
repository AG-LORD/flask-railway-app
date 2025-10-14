import os
import psycopg2
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
DATABASE_URL = os.environ['DATABASE_URL']

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        conn.close()

        return "Registration Successful!"
    return '''
        <form method="post">
            Username: <input name="username" type="text" required><br>
            Password: <input name="password" type="password" required><br>
            <input type="submit" value="Register">
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
