import json
import os
import sqlite3
from datetime import datetime, timezone

from flask import Flask, jsonify, request, send_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "innoverse.db")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

DEFAULT_STATE = {
    "currentRole": "Student",
    "currentView": "auth",
    "theme": "light",
}

app = Flask(__name__)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS workspace_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        existing = conn.execute(
            "SELECT value FROM workspace_state WHERE key = 'app_state'"
        ).fetchone()

        if existing is None:
            conn.execute(
                "INSERT INTO workspace_state (key, value, updated_at) VALUES (?, ?, ?)",
                ("app_state", json.dumps(DEFAULT_STATE), utc_now()),
            )


def load_state_from_db() -> dict:
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT value, updated_at FROM workspace_state WHERE key = 'app_state'"
        ).fetchone()

    if row is None:
        state = DEFAULT_STATE.copy()
        persist_state(state)
        return state

    try:
        data = json.loads(row["value"])
    except (TypeError, ValueError):
        data = DEFAULT_STATE.copy()

    if not isinstance(data, dict):
        data = DEFAULT_STATE.copy()

    merged = DEFAULT_STATE.copy()
    merged.update(data)
    return merged


def persist_state(state: dict) -> str:
    sanitized = DEFAULT_STATE.copy()
    sanitized.update(state or {})

    updated_at = utc_now()
    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO workspace_state (key, value, updated_at)
            VALUES ('app_state', ?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
            """,
            (json.dumps(sanitized), updated_at),
        )

    return updated_at


@app.before_request
def ensure_db_ready() -> None:
    init_db()


@app.get("/")
def index():
    return send_file(INDEX_PATH, mimetype="text/html")


@app.get("/api/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "INNOVERSE",
            "database": os.path.exists(DB_PATH),
        }
    )


@app.get("/api/state")
def get_state():
    state = load_state_from_db()
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT updated_at FROM workspace_state WHERE key = 'app_state'"
        ).fetchone()

    return jsonify({
        "ok": True,
        "state": state,
        "updated_at": row["updated_at"] if row else utc_now(),
    })


@app.put("/api/state")
def put_state():
    if not request.is_json:
        return jsonify({"ok": False, "error": "Request body must be valid JSON."}), 400

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"ok": False, "error": "JSON payload must be an object."}), 400

    data = payload.get("state", payload)
    if not isinstance(data, dict):
        return jsonify({"ok": False, "error": "State payload must be an object."}), 400

    allowed_keys = {"currentRole", "currentView", "theme"}
    invalid = set(data.keys()) - allowed_keys
    if invalid:
        return jsonify({"ok": False, "error": f"Unsupported state keys: {sorted(invalid)}"}), 400

    if "theme" in data and data["theme"] not in {"light", "dark"}:
        return jsonify({"ok": False, "error": "theme must be 'light' or 'dark'."}), 400

    if "currentRole" in data and not isinstance(data["currentRole"], str):
        return jsonify({"ok": False, "error": "currentRole must be a string."}), 400

    if "currentView" in data and not isinstance(data["currentView"], str):
        return jsonify({"ok": False, "error": "currentView must be a string."}), 400

    merged = DEFAULT_STATE.copy()
    merged.update(data)

    updated_at = persist_state(merged)
    return jsonify({"ok": True, "state": merged, "updated_at": updated_at}), 200


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"ok": False, "error": "Not found."}), 404


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
