from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
DB_FILE = 'habits.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        # Table for habits
        c.execute('''CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                     )''')
        # Table for tracking completions
        c.execute('''CREATE TABLE IF NOT EXISTS habit_tracking (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_id INTEGER,
                        date TEXT,
                        FOREIGN KEY (habit_id) REFERENCES habits(id)
                     )''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        # Get all habits
        c.execute("SELECT * FROM habits")
        habits = c.fetchall()
        # Get tracking data for today
        today = datetime.now().strftime('%Y-%m-%d')
        c.execute("SELECT habit_id FROM habit_tracking WHERE date = ?", (today,))
        completed_habits = [row[0] for row in c.fetchall()]
    return render_template('index.html', habits=habits, completed=completed_habits)

@app.route('/add', methods=['POST'])
def add_habit():
    habit_name = request.form.get('habit_name')
    if habit_name:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO habits (name) VALUES (?)", (habit_name,))
            conn.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:habit_id>', methods=['POST'])
def complete_habit(habit_id):
    today = datetime.now().strftime('%Y-%m-%d')
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        # Mark the habit as completed today
        c.execute("INSERT INTO habit_tracking (habit_id, date) VALUES (?, ?)", (habit_id, today))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
