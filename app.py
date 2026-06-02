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
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS chat_history (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, message TEXT NOT NULL, reply TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    conn.execute("CREATE TABLE IF NOT EXISTS bmi_history (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, bmi_value REAL NOT NULL, weight REAL NOT NULL, height REAL NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

# --- Routes ---
@app.route("/")
def home_page(): return render_template("home.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    username = data.get("username", "guest")

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Healthcare Assistant: {user_message}"
        )
        reply = response.text
        conn = get_db()
        conn.execute("INSERT INTO chat_history (username, message, reply) VALUES (?,?,?)", (username, user_message, reply))
        conn.commit()
        conn.close()
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Error connecting to AI."}), 500

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"], password):
            return jsonify({"success": True, "username": user['username']})
        return jsonify({"success": False, "message": "Invalid credentials"})
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.get_json()
        try:
            conn = get_db()
            conn.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", 
                         (data.get("username"), data.get("email"), generate_password_hash(data.get("password"))))
            conn.commit()
            conn.close()
            return jsonify({"success": True})
        except:
            return jsonify({"success": False, "message": "User already exists"})
    return render_template("signup.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=8080)