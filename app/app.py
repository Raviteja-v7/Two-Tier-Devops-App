from flask import Flask, render_template, request, redirect
import mysql.connector, os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    name = request.form.get("name")
    message = request.form.get("message")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages(name, message) VALUES (%s, %s)", (name, message))
    conn.commit()
    return redirect("/")

@app.route("/messages")
def messages():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, message FROM messages ORDER BY id DESC")
    data = cur.fetchall()
    return render_template("messages.html", messages=data)

@app.route("/health")
def health():
    try:
        get_db()
        return "OK", 200
    except:
        return "DB DOWN", 500

app.run(host="0.0.0.0", port=5000)
