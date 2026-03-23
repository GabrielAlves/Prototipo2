from __future__ import annotations
import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_BASE = os.getenv("BACKEND_API_BASE", "http://localhost:8000")

@app.route("/")
def index():
    return render_template("index.html", api_base=API_BASE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
