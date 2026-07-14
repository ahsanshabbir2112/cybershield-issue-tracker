from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return {
        "message": "CyberShield Issue and Vulnerability Tracking System API is running.",
        "company": "CyberShield Solutions Ltd"
    }


if __name__ == "__main__":
    app.run(debug=True)