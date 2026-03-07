"""Input validation functions."""

import re
from typing import Optional
from urllib.parse import urlparse
from pathlib import Path

from .constants import EMAIL_PATTERN, URL_PATTERN


def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email:
        return False
    return bool(re.match(EMAIL_PATTERN, email))


def validate_url(url: str, require_http: bool = True) -> bool:
    """Validate URL format."""
    if not url or url == "#":
        return True  # Optional field
    
    if require_http and not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_image_path(image_path: str) -> bool:
    """Validate if image file exists and is an image."""
    path = Path(image_path)
    if not path.exists():
        return False
    
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'}
    return path.suffix.lower() in valid_extensions


def validate_non_empty(value: str, field_name: str) -> tuple[bool, Optional[str]]:
    """Validate that a field is not empty."""
    if not value or not value.strip():
        return False, f"{field_name} cannot be empty"
    return True, None


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be safe for all OS."""
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    
    # Limit length and strip
    return filename[:255].strip()