"""Constants and enums used throughout the application."""

from enum import Enum, auto
from pathlib import Path


class TemplateStyle(Enum):
    """Available template styles."""
    MINIMAL = "minimal"
    MODERN = "modern"
    CREATIVE = "creative"


class ColorScheme(Enum):
    """Predefined color schemes."""
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    CUSTOM = "custom"


class FontFamily(Enum):
    """Available font families."""
    SANS_SERIF = "Arial, Helvetica, sans-serif"
    SERIF = "Georgia, Times New Roman, serif"
    MONOSPACE = "Courier New, monospace"
    ROBOTO = "Roboto, sans-serif"
    OPEN_SANS = "Open Sans, sans-serif"
    MONTSERRAT = "Montserrat, sans-serif"


class ExportFormat(Enum):
    """Available export formats."""
    HTML_ONLY = auto()
    FULL_PROJECT = auto()
    ZIP_ARCHIVE = auto()
    GITHUB_PAGES = auto()


# Directory structure
BASE_DIR = Path(__file__).parent.parent.absolute()
TEMPLATES_DIR = BASE_DIR / "templates"
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"
EXPORTS_DIR = BASE_DIR / "exports"
CONFIGS_DIR = BASE_DIR / "configs"

# File paths
DEFAULT_AVATAR = ASSETS_DIR / "default-avatar.png"
CONFIG_FILE = BASE_DIR / "config.json"

# Validation patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
URL_PATTERN = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*/?'