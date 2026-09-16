"""
Flask application entry point for MarkdownNoteApp.

Provides routes for serving the UI and a JSON API for persisting notes.
"""

import logging
import os
from pathlib import Path
from typing import Dict

from flask import Flask, jsonify, request, send_from_directory, abort
from dotenv import load_dotenv

from utils import sanitize_filename, write_note

# Load environment variables from .env (if present)
load_dotenv()

# Configuration
SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY", "default-secret")
NOTE_STORAGE_PATH: Path = Path(os.getenv("NOTE_STORAGE_PATH", "./notes")).resolve()

# Ensure storage directory exists
NOTE_STORAGE_PATH.mkdir(parents=True, exist_ok=True)

# Flask app setup
app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config["SECRET_KEY"] = SECRET_KEY

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
# small cleanup
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.route("/", methods=["GET"])
def serve_index() -> str:
    """Serve the main HTML page."""
    logger.info("Serving index.html")
    return send_from_directory(".", "index.html")

@app.route("/style.css", methods=["GET"])
def serve_css() -> str:
    """Serve the CSS file."""
    return send_from_directory(".", "style.css")

@app.route("/app.js", methods=["GET"])
def serve_js() -> str:
    """Serve the JavaScript file."""
    return send_from_directory(".", "app.js")

@app.route("/api/save", methods=["POST"])
def save_note() -> Dict[str, str]:
    """
    Save a markdown note sent via JSON payload.

    Expected JSON:
    {
        "title": "My Note",
        "content": "# Markdown content"
    }
    """
    try:
        data = request.get_json()
        if not data:
            logger.warning("No JSON payload received")
            abort(400, description="Invalid JSON payload.")
        title: str = data.get("title", "").strip()
        content: str = data.get("content", "").strip()

# cleaner this way
        if not title or not content:
            logger.warning("Missing title or content in request")
            abort(400, description="Both 'title' and 'content' are required.")

        safe_title = sanitize_filename(title)
        note_path = NOTE_STORAGE_PATH / f"{safe_title}.md"

        write_note(note_path, content)
        logger.info(f"Note saved: {note_path}")
        return jsonify({"message": "Note saved successfully."}), 200

    except Exception as exc:
        logger.exception("Failed to save note")
        abort(500, description=str(exc))

@app.errorhandler(400)
def handle_400(error):
    """Return JSON for 400 errors."""
    return jsonify({"error": error.description}), 400

@app.errorhandler(500)
def handle_500(error):
    """Return JSON for 500 errors."""
    return jsonify({"error": "Internal server error."}), 500

if __name__ == "__main__":
    # Running directly for development; production should use a WSGI server.
    app.run(host="0.0.0.0", port=5000, debug=False)