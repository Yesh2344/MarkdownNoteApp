"""
Utility functions for MarkdownNoteApp.

Provides file I/O helpers and filename sanitization.
"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

def sanitize_filename(name: str) -> str:
    """
    Convert an arbitrary string into a safe filename.

    Removes disallowed characters and collapses whitespace.
    """
    logger.debug(f"Sanitizing filename: {name}")
    # Replace spaces with underscores
    name = re.sub(r"\s+", "_", name)
    # Remove any character that is not alphanumeric, underscore, or hyphen
    name = re.sub(r"[^\w\-]", "", name)
    safe_name = name[:255]  # Enforce typical filename length limit
    logger.debug(f"Sanitized filename: {safe_name}")
    return safe_name

def write_note(path: Path, content: str) -> None:
    """
    Write markdown content to the given path.

    Overwrites existing files atomically.
    """
    try:
        logger.debug(f"Writing note to {path}")
        # Write to a temporary file first for atomic replace
        temp_path = path.with_suffix(".tmp")
        temp_path.write_text(content, encoding="utf-8")
        temp_path.replace(path)
        logger.info(f"Successfully wrote note to {path}")
    except Exception as exc:
        logger.exception(f"Error writing note to {path}")
        raise IOError(f"Failed to write note: {exc}") from exc