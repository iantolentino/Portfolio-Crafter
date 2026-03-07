"""Template management and selection."""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from .utils.constants import TEMPLATES_DIR, TemplateStyle


class TemplateManager:
    """Manages templates, loading, and customization."""
    
    def __init__(self):
        self.templates_dir = TEMPLATES_DIR
        self.available_templates = self._scan_templates()
        self.current_template = None
        self.env = None
    
    def _scan_templates(self) -> Dict[str, Path]:
        """Scan for available templates."""
        templates = {}
        
        if not self.templates_dir.exists():
            return templates
        
        for item in self.templates_dir.iterdir():
            if item.is_dir():
                # Check if it has required files
                if (item / "index.html").exists() and (item / "style.css").exists():
                    templates[item.name] = item
        
        return templates
    
    def list_templates(self) -> List[str]:
        """List available template names."""
        return list(self.available_templates.keys())
    
    def get_template_preview(self, template_name: str) -> Optional[Path]:
        """Get preview image path for template."""
        if template_name in self.available_templates:
            preview_path = self.available_templates[template_name] / "preview.png"
            if preview_path.exists():
                return preview_path
        return None
    
    def load_template(self, template_name: str) -> bool:
        """Load a template for use."""
        if template_name not in self.available_templates:
            return False
        
        template_path = self.available_templates[template_name]
        self.current_template = template_name
        
        # Setup Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(template_path)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        return True
    
    def render_template(self, template_name: str, **kwargs) -> str:
        """Render a template with provided data."""
        if not self.env:
            raise RuntimeError("No template loaded. Call load_template() first.")
        
        try:
            template = self.env.get_template(template_name)
            return template.render(**kwargs)
        except TemplateNotFound:
            raise FileNotFoundError(f"Template {template_name} not found in {self.current_template}")
    
    def get_template_config(self, template_name: str) -> Dict[str, Any]:
        """Get template configuration if available."""
        template_path = self.available_templates.get(template_name)
        if not template_path:
            return {}
        
        config_path = template_path / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        return {}
    
    def customize_template(self, template_name: str, customizations: Dict[str, Any]) -> bool:
        """Apply customizations to template."""
        # This would modify CSS variables, etc.
        # For now, just return True
        return True
    
    def get_css_path(self, template_name: str) -> Path:
        """Get path to template CSS file."""
        return self.available_templates[template_name] / "style.css"