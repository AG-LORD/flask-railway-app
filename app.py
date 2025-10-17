import os
import psycopg2
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)
DATABASE_URL = os.environ['DATABASE_URL']

# Home page with student data form
@app.route('/', methods=['GET', 'POST'])
def student_marks():
    message = ''
    if request.method == 'POST':
        # Collect submitted student data from form fields
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            # Expect fields student_name_1, marks_1, student_name_2, marks_2, etc.
            for key, value in request.form.items():
                if key.startswith('student_name_'):
                    suffix = key.split('_')[-1]
                    name = value.strip()
                    marks = request.form.get(f'marks_{suffix}', '').strip()
                    if name and marks:
                        # Insert or update student marks in DB
                        cur.execute("""
                            INSERT INTO students (name, marks)
                            VALUES (%s, %s)
                            ON CONFLICT (name) DO UPDATE SET marks = EXCLUDED.marks
                        """, (name, marks))
            conn.commit()
            cur.close()
            conn.close()
            message = 'Student marks saved successfully!'
        except Exception as e:
            message = f'Error saving marks: {e}'

    # Fetch existing students data to display
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, name, marks FROM students ORDER BY id")
        students = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        students = []
        message = f'Error fetching students: {e}'

    # Render simple HTML page with editable data form
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Student Marks Upload</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f8; padding: 20px; }
        h2 { color: #333; }
        table { border-collapse: collapse; width: 80%; margin-bottom: 20px; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
        th { background: #007BFF; color: white; }
        input[type=text], input[type=number] {
            width: 90%; padding: 6px; border: 1px solid #ccc; border-radius: 4px;
        }
        input[type=submit] {
            background-color: #007BFF; color: white; padding: 10px 20px;
            border: none; border-radius: 5px; cursor: pointer;
        }
        input[type=submit]:hover {
            background-color: #0056b3;
        }
        .message {
            margin-bottom: 20px; padding: 10px; border-radius: 4px;
            color: white; background-color: #28a745;
        }
    </style>
    </head>
    <body>
        <h2>Enter Student Names and Marks</h2>
        {% if message %}
        <div class="message">{{ message }}</div>
        {% endif %}
        <form method="post">
            <table>
                <tr><th>Student Name</th><th>Marks</th></tr>
                {% for id, name, marks in students %}
                <tr>
                    <td><input type="text" name="student_name_{{ loop.index }}" value="{{ name }}"></td>
                    <td><input type="number" name="marks_{{ loop.index }}" value="{{ marks }}"></td>
                </tr>
                {% endfor %}
                <!-- Add 3 empty rows for new entries -->
                {% for i in range(3) %}
                <tr>
                    <td><input type="text" name="student_name_new_{{ i }}"></td>
                    <td><input type="number" name="marks_new_{{ i }}"></td>
                </tr>
                {% endfor %}
            </table>
            <input type="submit" value="Save Marks">
        </form>
    </body>
    </html>
    '''
    # Render with Flask's built-in template engine
    return render_template_string(html, students=students, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
