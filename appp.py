from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GENAI_API_KEY")

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=api_key)

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            reply TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bmi_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            bmi_value REAL NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
@app.route("/home.html")
def home_page():
    return render_template("home.html")

@app.route("/chatbot.html")
def chatbot_page():
    return render_template("chatbot.html")

@app.route("/bmi.html")
def bmi_page():
    return render_template("bmi.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    username = data.get("username", "guest")

    if not user_message:
        return jsonify({"reply": "Please type a message."}), 400

    try:
        response = client.models.generate_content(
            model="gemini/1.5-flash",
            contents=f"You are a helpful healthcare assistant. Reply clearly and briefly.\nUser: {user_message}"
        )

        reply = "No reply from AI."
        if hasattr(response, "text") and response.text:
            reply = response.text

        conn = get_db()
        conn.execute(
            "INSERT INTO chat_history (username, message, reply) VALUES (?,?,?)",
            (username, user_message, reply)
        )
        conn.commit()
        conn.close()

        return jsonify({"reply": reply})

    except Exception as e:
        print("CHAT ERROR:", repr(e))
        return jsonify({"reply": "Error connecting to AI."}), 500

@app.route("/get_chat_history", methods=["GET"])
def get_chat_history():
    username = request.args.get("username", "guest")
    conn = get_db()
    history = conn.execute(
        "SELECT message, reply, timestamp FROM chat_history WHERE username=? ORDER BY timestamp DESC LIMIT 20",
        (username,)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in history])

@app.route("/save_bmi", methods=["POST"])
def save_bmi():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    bmi = data.get("bmi")
    weight = data.get("weight")
    height = data.get("height")

    if not username or bmi is None or weight is None or height is None:
        return jsonify({"success": False, "message": "Missing BMI data"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO bmi_history (username, bmi_value, weight, height) VALUES (?,?,?,?)",
        (username, bmi, weight, height)
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/get_bmi_history", methods=["GET"])
def get_bmi_history():
    username = request.args.get("username", "guest")
    conn = get_db()
    history = conn.execute(
        "SELECT bmi_value, weight, height, timestamp FROM bmi_history WHERE username=? ORDER BY timestamp DESC LIMIT 10",
        (username,)
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in history])

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?,?,?)",
            (username, email, generate_password_hash(password))
        )
        conn.commit()
        return jsonify({"success": True, "message": "Signup successful"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Username or email already exists"}), 409
    finally:
        conn.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required"}), 400

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        return jsonify({"success": True, "username": user["username"]})

    return jsonify({"success": False, "message": "Invalid credentials"}), 401

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=8080)