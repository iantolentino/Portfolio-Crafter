"""CSS builder for custom styling."""

from typing import Dict, Any
import re


class CSSBuilder:
    """Builds custom CSS based on user preferences."""
    
    def __init__(self):
        self.css_variables = {}
        self.custom_rules = []
    
    def build(self, template_css: str, customizations: Dict[str, Any]) -> str:
        """Build final CSS by combining template and customizations."""
        # Extract CSS variables from template
        self._extract_variables(template_css)
        
        # Apply customizations
        self._apply_customizations(customizations)
        
        # Replace variables in template
        css = self._replace_variables(template_css)
        
        # Add any custom rules
        if self.custom_rules:
            css += "\n\n/* Custom Rules */\n"
            css += "\n".join(self.custom_rules)
        
        return css
    
    def _extract_variables(self, css: str) -> None:
        """Extract CSS variables from template."""
        # Find :root variables
        root_match = re.search(r':root\s*{([^}]*)}', css, re.DOTALL)
        if root_match:
            root_content = root_match.group(1)
            # Find all --var: value;
            var_matches = re.findall(r'--([^:]+):\s*([^;]+);', root_content)
            for var_name, var_value in var_matches:
                self.css_variables[f'--{var_name.strip()}'] = var_value.strip()
    
    def _apply_customizations(self, customizations: Dict[str, Any]) -> None:
        """Apply user customizations to CSS."""
        color_scheme = customizations.get('color_scheme', 'light')
        
        # Predefined color schemes
        schemes = {
            'light': {
                'primary-color': '#3498db',
                'secondary-color': '#2ecc71',
                'text-color': '#2c3e50',
                'background-color': '#ffffff',
                'card-background': '#f8f9fa'
            },
            'dark': {
                'primary-color': '#64b5f6',
                'secondary-color': '#81c784',
                'text-color': '#ecf0f1',
                'background-color': '#1a1a1a',
                'card-background': '#2d2d2d'
            },
            'blue': {
                'primary-color': '#1976d2',
                'secondary-color': '#42a5f5',
                'text-color': '#1565c0',
                'background-color': '#e3f2fd',
                'card-background': '#bbdefb'
            },
            'green': {
                'primary-color': '#388e3c',
                'secondary-color': '#66bb6a',
                'text-color': '#1b5e20',
                'background-color': '#e8f5e8',
                'card-background': '#c8e6c9'
            },
            'purple': {
                'primary-color': '#7b1fa2',
                'secondary-color': '#9c27b0',
                'text-color': '#4a148c',
                'background-color': '#f3e5f5',
                'card-background': '#e1bee7'
            }
        }
        
        # Apply selected color scheme
        if color_scheme in schemes:
            for key, value in schemes[color_scheme].items():
                self.css_variables[f'--{key}'] = value
        
        # Apply font
        font = customizations.get('font')
        if font:
            self.css_variables['--font-family'] = font
        
        # Apply any custom colors
        if 'custom_colors' in customizations:
            for key, value in customizations['custom_colors'].items():
                self.css_variables[f'--{key}'] = value
    
    def _replace_variables(self, css: str) -> str:
        """Replace CSS variables in the template."""
        # Create :root section with updated variables
        root_vars = ':root {\n'
        for var_name, var_value in self.css_variables.items():
            root_vars += f'    {var_name}: {var_value};\n'
        root_vars += '}\n\n'
        
        # Remove existing :root section
        css = re.sub(r':root\s*{[^}]*}', '', css, flags=re.DOTALL)
        
        return root_vars + css
    
    def add_rule(self, selector: str, properties: Dict[str, str]) -> None:
        """Add a custom CSS rule."""
        rule = f'{selector} {{\n'
        for prop, value in properties.items():
            rule += f'    {prop}: {value};\n'
        rule += '}\n'
        self.custom