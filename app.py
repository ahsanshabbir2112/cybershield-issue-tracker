from flask import Flask, request, jsonify
from models import init_db


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return {
        "message": "CyberShield Issue and Vulnerability Tracking System API is running.",
        "company": "CyberShield Solutions Ltd"
    }

@app.route("/issues", methods=["POST"])
def create_issue():
    data = request.get_json(silent=True) or {}

    title = data.get("title")
    description = data.get("description", "")
    severity = data.get("severity")
    status = data.get("status", "Open")
    assigned_to = data.get("assigned_to", "")

    errors = []

    if not title or not str(title).strip():
        errors.append("Title cannot be empty.")

    if severity not in VALID_SEVERITIES:
        errors.append(
            f"Severity must be one of {', '.join(VALID_SEVERITIES)}."
        )

    if status not in VALID_STATUSES:
        errors.append(
            f"Status must be one of {', '.join(VALID_STATUSES)}."
        )

    if errors:
        return jsonify({"errors": errors}), 400

    connection = get_db_connection()

    cursor = connection.execute(
        """
        INSERT INTO issues (
            title,
            description,
            severity,
            status,
            assigned_to,
            date_created
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            str(title).strip(),
            description,
            severity,
            status,
            assigned_to,
            now_iso()
        )
    )

    connection.commit()

    new_issue_id = cursor.lastrowid

    new_issue = connection.execute(
        "SELECT * FROM issues WHERE id = ?",
        (new_issue_id,)
    ).fetchone()

    connection.close()

    return jsonify(row_to_dict(new_issue)), 201

@app.route("/issues", methods=["GET"])
def get_all_issues():
    connection = get_db_connection()

    issues = connection.execute(
        "SELECT * FROM issues ORDER BY id ASC"
    ).fetchall()

    connection.close()

    return jsonify([row_to_dict(issue) for issue in issues]), 200

@app.route("/issues/<int:issue_id>", methods=["GET"])
def get_single_issue(issue_id):
    connection = get_db_connection()

    issue = connection.execute(
        "SELECT * FROM issues WHERE id = ?",
        (issue_id,)
    ).fetchone()

    connection.close()

    if issue is None:
        return jsonify({
            "error": f"Issue with id {issue_id} was not found."
        }), 404

    return jsonify(row_to_dict(issue)), 200

@app.route("/issues/<int:issue_id>", methods=["PUT", "PATCH"])
def update_issue(issue_id):
    connection = get_db_connection()

    existing_issue = connection.execute(
        "SELECT * FROM issues WHERE id = ?",
        (issue_id,)
    ).fetchone()

    if existing_issue is None:
        connection.close()

        return jsonify({
            "error": f"Issue with id {issue_id} was not found."
        }), 404

    data = request.get_json(silent=True) or {}

    title = data.get("title", existing_issue["title"])
    description = data.get(
        "description",
        existing_issue["description"]
    )
    severity = data.get(
        "severity",
        existing_issue["severity"]
    )
    status = data.get(
        "status",
        existing_issue["status"]
    )
    assigned_to = data.get(
        "assigned_to",
        existing_issue["assigned_to"]
    )

    errors = []

    if not str(title).strip():
        errors.append("Title cannot be empty.")

    if severity not in VALID_SEVERITIES:
        errors.append(
            f"Severity must be one of {', '.join(VALID_SEVERITIES)}."
        )

    if status not in VALID_STATUSES:
        errors.append(
            f"Status must be one of {', '.join(VALID_STATUSES)}."
        )

    if errors:
        connection.close()
        return jsonify({"errors": errors}), 400

    connection.execute(
        """
        UPDATE issues
        SET title = ?,
            description = ?,
            severity = ?,
            status = ?,
            assigned_to = ?
        WHERE id = ?
        """,
        (
            str(title).strip(),
            description,
            severity,
            status,
            assigned_to,
            issue_id
        )
    )

    connection.commit()

    updated_issue = connection.execute(
        "SELECT * FROM issues WHERE id = ?",
        (issue_id,)
    ).fetchone()

    connection.close()

    return jsonify(row_to_dict(updated_issue)), 200

@app.route("/issues/<int:issue_id>", methods=["DELETE"])
def delete_issue(issue_id):
    connection = get_db_connection()

    existing_issue = connection.execute(
        "SELECT * FROM issues WHERE id = ?",
        (issue_id,)
    ).fetchone()

    if existing_issue is None:
        connection.close()

        return jsonify({
            "error": f"Issue with id {issue_id} was not found."
        }), 404

    connection.execute(
        "DELETE FROM issues WHERE id = ?",
        (issue_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": f"Issue with id {issue_id} deleted successfully."
    }), 200
    
       
from models import (
    get_db_connection,
    init_db,
    row_to_dict,
    now_iso,
    VALID_SEVERITIES,
    VALID_STATUSES
)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)