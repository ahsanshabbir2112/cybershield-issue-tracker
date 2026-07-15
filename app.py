from flask import Flask, request, jsonify
from models import init_db

ALLOWED_SORT_COLUMNS = {
    "id",
    "title",
    "severity",
    "status",
    "assigned_to",
    "date_created"
}
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
    search = request.args.get("search", "").strip()
    severity = request.args.get("severity", "").strip()
    status = request.args.get("status", "").strip()
    assigned_to = request.args.get("assigned_to", "").strip()

    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc").lower()

    errors = []

    if severity and severity not in VALID_SEVERITIES:
        errors.append(
            f"Severity must be one of {', '.join(VALID_SEVERITIES)}."
        )

    if status and status not in VALID_STATUSES:
        errors.append(
            f"Status must be one of {', '.join(VALID_STATUSES)}."
        )

    if sort_by not in ALLOWED_SORT_COLUMNS:
        errors.append(
            f"Sort column must be one of {', '.join(sorted(ALLOWED_SORT_COLUMNS))}."
        )

    if order not in ("asc", "desc"):
        errors.append("Order must be either asc or desc.")

    if errors:
        return jsonify({"errors": errors}), 400

    query = "SELECT * FROM issues WHERE 1 = 1"
    parameters = []

    if search:
        query += """
            AND (
                title LIKE ?
                OR description LIKE ?
            )
        """
        search_value = f"%{search}%"
        parameters.extend([search_value, search_value])

    if severity:
        query += " AND severity = ?"
        parameters.append(severity)

    if status:
        query += " AND status = ?"
        parameters.append(status)

    if assigned_to:
        query += " AND assigned_to LIKE ?"
        parameters.append(f"%{assigned_to}%")

    direction = "DESC" if order == "desc" else "ASC"
    query += f" ORDER BY {sort_by} {direction}"

    connection = get_db_connection()

    issues = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return jsonify({
        "count": len(issues),
        "issues": [row_to_dict(issue) for issue in issues]
    }), 200
@app.route("/reports/summary", methods=["GET"])
def get_summary_report():
    connection = get_db_connection()

    total_issues = connection.execute(
        "SELECT COUNT(*) AS total FROM issues"
    ).fetchone()["total"]

    status_rows = connection.execute(
        """
        SELECT status, COUNT(*) AS total
        FROM issues
        GROUP BY status
        """
    ).fetchall()

    severity_rows = connection.execute(
        """
        SELECT severity, COUNT(*) AS total
        FROM issues
        GROUP BY severity
        """
    ).fetchall()

    connection.close()

    issues_by_status = {
        row["status"]: row["total"]
        for row in status_rows
    }

    issues_by_severity = {
        row["severity"]: row["total"]
        for row in severity_rows
    }

    return jsonify({
        "total_issues": total_issues,
        "open_issues": issues_by_status.get("Open", 0),
        "in_progress_issues": issues_by_status.get("In Progress", 0),
        "resolved_issues": issues_by_status.get("Resolved", 0),
        "closed_issues": issues_by_status.get("Closed", 0),
        "critical_issues": issues_by_severity.get("Critical", 0),
        "issues_by_status": issues_by_status,
        "issues_by_severity": issues_by_severity
    }), 200    

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