from flask import Flask, request, render_template
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

# Create DB and table if not exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS submissions (text TEXT, date TEXT)')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO submissions (text, date) VALUES (?, ?)", (text, date))
        conn.commit()
        conn.close()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM submissions ORDER BY rowid DESC")
    submissions = c.fetchall()
    conn.close()
    return render_template("index.html", submissions=submissions)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=80)
