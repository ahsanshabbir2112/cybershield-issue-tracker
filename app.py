from flask import Flask
from models import init_db

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return {
        "message": "CyberShield Issue and Vulnerability Tracking System API is running.",
        "company": "CyberShield Solutions Ltd"
    }


if __name__ == "__main__":
    init_db()
    app.run(debug=True)