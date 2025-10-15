import os
import psycopg2
from flask import Flask, request, redirect, url_for

app = Flask(__name__)
DATABASE_URL = os.environ['DATABASE_URL']

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if not username or not password:
            error = "Both fields are required."
        else:
            try:
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                # Check for duplicate usernames
                cur.execute("SELECT 1 FROM users WHERE username=%s", (username,))
                if cur.fetchone():
                    error = "Username already exists."
                else:
                    cur.execute(
                        "INSERT INTO users (username, password) VALUES (%s, %s)",
                        (username, password)
                    )
                    conn.commit()
                    error = "Registration successful!"
                cur.close()
                conn.close()
            except Exception as e:
                error = f"Error: {e}"
    return f'''
        <form method="post">
            Username: <input name="username" type="text" required><br>
            Password: <input name="password" type="password" required><br>
            <input type="submit" value="Register">
        </form>
        <br>{error}
    '''

@app.route('/users')
def users():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM users ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        return f"Database error: {e}"

    user_list = "<ul>"
    for uid, uname in rows:
        user_list += f"<li>User {uid}: {uname}</li>"
    user_list += "</ul>"
    return user_list

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
