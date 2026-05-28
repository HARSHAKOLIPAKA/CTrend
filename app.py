from flask import Flask, render_template, request, redirect, session, flash
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key"

socketio = SocketIO(
    app,
    async_mode="threading"
)

# ---------------- DATABASE ----------------
def create_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        message TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()
# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" in session:
        return redirect("/chat")
    return redirect("/login")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users(username, password) VALUES (?, ?)",
                (username, hashed_password)
            )

            conn.commit()
            conn.close()

            flash("Account created successfully!")
            return redirect("/login")

        except:
            flash("Username already exists")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect("/chat")

        flash("Invalid username or password")

    return render_template("login.html")

# ---------------- CHAT ----------------
@app.route("/chat")
def chat():

    if "user" not in session:
        return redirect("/login")

    current_user = session["user"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Get all users except current user
    cursor.execute("""
        SELECT username
        FROM users
        WHERE username != ?
    """, (current_user,))

    users = cursor.fetchall()

    selected_user = request.args.get("user")

    messages = []

    # Load DM messages
    if selected_user:

        cursor.execute("""
        SELECT sender, message, time
        FROM messages
        WHERE
        (sender=? AND receiver=?)
        OR
        (sender=? AND receiver=?)
        ORDER BY id ASC
        """, (
            current_user,
            selected_user,
            selected_user,
            current_user
        ))

        messages = cursor.fetchall()

    conn.close()

    return render_template(
        "chat.html",
        username=current_user,
        users=users,
        selected_user=selected_user,
        messages=messages
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ---------------- REAL-TIME CHAT ----------------
@socketio.on("private_message")
def handle_private_message(data):

    sender = data["sender"]
    receiver = data["receiver"]
    message = data["message"]
    time = data["time"]

    conn = sqlite3.connect(
        "database.db"
    )

    cursor = conn.cursor()

    # Save message
    cursor.execute("""
    INSERT INTO messages
    (
        sender,
        receiver,
        message,
        time
    )
    VALUES (?, ?, ?, ?)
    """, (
        sender,
        receiver,
        message,
        time
    ))

    conn.commit()
    conn.close()

    # Send live message
    socketio.emit(
        "receive_private_message",
        {
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "time": time
        }
    )
    if not sender or not receiver or not message:
        return

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages
        (sender, receiver, message, time)
        VALUES (?, ?, ?, ?)
    """, (sender, receiver, message, time))

    conn.commit()
    conn.close()

    message_data = {
        "from": sender,
        "to": receiver,
        "message": message,
        "time": time
    }

    emit("receive_message", message_data, broadcast=True)

# ---------------- RUN ----------------
if __name__ == "__main__":
    socketio.run(
    app,
    debug=True,
    port=8000
)