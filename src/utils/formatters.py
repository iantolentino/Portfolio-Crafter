"""Data formatting utilities."""

import json
import datetime
from typing import Dict, List, Any
from pathlib import Path


def format_date(date: datetime.datetime = None) -> str:
    """Format date for display."""
    if date is None:
        date = datetime.datetime.now()
    return date.strftime("%B %d, %Y")


def format_skills_for_display(skills: List[Dict[str, Any]]) -> str:
    """Format skills list for HTML display."""
    if not skills:
        return ""
    
    html = '<div class="skills-container">\n'
    for skill in skills:
        html += f'  <div class="skill-item">\n'
        html += f'    <span class="skill-name">{skill["name"]}</span>\n'
        html += f'    <div class="skill-bar">\n'
        html += f'      <div class="skill-level" style="width: {skill["level"]}%"></div>\n'
        html += f'    </div>\n'
        html += f'  </div>\n'
    html += '</div>\n'
    return html


def save_config(data: Dict[str, Any], filename: str = "config.json") -> Path:
    """Save configuration to JSON file."""
    config_dir = Path(__file__).parent.parent.parent / "configs"
    config_dir.mkdir(exist_ok=True)
    
    filepath = config_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filepath


def load_config(filepath: Path) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."