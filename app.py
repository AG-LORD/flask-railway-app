import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE_URL = os.environ['DATABASE_URL']

@app.route('/')
def hello():
    return "Hello World from Flask on Railway!"

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO mytable (info) VALUES (%s)", (data['info'],))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/get', methods=['GET'])
def get():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT info FROM mytable")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
