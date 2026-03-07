"""User input collection with validation and rich formatting."""

import sys
from typing import Dict, List, Optional, Any
from pathlib import Path
import questionary
from colorama import init, Fore, Style

from .utils.validators import validate_email, validate_url, validate_non_empty
from .utils.constants import TemplateStyle, ColorScheme, FontFamily

# Initialize colorama
init(autoreset=True)


class UserInputCollector:
    """Collect and validate user input with interactive prompts."""
    
    def __init__(self):
        self.data = {}
    
    def collect_all(self) -> Dict[str, Any]:
        """Collect all user information."""
        self._display_welcome()
        
        # Basic Info
        self._collect_basic_info()
        
        # Template Selection
        self._collect_template_preferences()
        
        # Projects
        self._collect_projects()
        
        # Skills
        if self._ask_yes_no("Would you like to add skills?", default=True):
            self._collect_skills()
        
        # Experience
        if self._ask_yes_no("Would you like to add work experience?", default=True):
            self._collect_experience()
        
        # Education
        if self._ask_yes_no("Would you like to add education?", default=True):
            self._collect_education()
        
        # Social Links
        self._collect_social_links()
        
        # Export Options
        self._collect_export_options()
        
        return self.data
    
    def _display_welcome(self):
        """Display welcome message."""
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + "🎨 PORTFOLIO WEBSITE GENERATOR 🎨".center(60))
        print(Fore.CYAN + "=" * 60)
        print(Fore.YELLOW + "Create your professional portfolio in minutes!\n")
    
    def _collect_basic_info(self):
        """Collect basic personal information."""
        print(Fore.GREEN + "\n📋 BASIC INFORMATION")
        print(Fore.GREEN + "-" * 40)
        
        self.data['name'] = questionary.text(
            "What's your full name?",
            validate=lambda x: len(x) > 0
        ).ask()
        
        self.data['title'] = questionary.text(
            "What's your professional title? (e.g., 'Software Developer')"
        ).ask()
        
        self.data['bio'] = questionary.text(
            "Write a short bio about yourself:"
        ).ask()
        
        self.data['email'] = questionary.text(
            "Your email address:",
            validate=lambda x: validate_email(x) or "Please enter a valid email"
        ).ask()
        
        # Optional: Profile picture
        if self._ask_yes_no("Would you like to add a profile picture?", default=False):
            self.data['avatar'] = questionary.path(
                "Path to profile picture:",
                validate=lambda x: Path(x).exists() or "File does not exist"
            ).ask()
    
    def _collect_template_preferences(self):
        """Collect template and styling preferences."""
        print(Fore.GREEN + "\n🎨 DESIGN PREFERENCES")
        print(Fore.GREEN + "-" * 40)
        
        # Template selection
        template_choices = [
            {
                'name': 'Minimal - Clean and simple',
                'value': TemplateStyle.MINIMAL.value
            },
            {
                'name': 'Modern - Contemporary design',
                'value': TemplateStyle.MODERN.value
            },
            {
                'name': 'Creative - Bold and artistic',
                'value': TemplateStyle.CREATIVE.value
            }
        ]
        
        self.data['template'] = questionary.select(
            "Choose a template style:",
            choices=template_choices
        ).ask()
        
        # Color scheme
        color_choices = [
            {'name': '🌞 Light', 'value': ColorScheme.LIGHT.value},
            {'name': '🌙 Dark', 'value': ColorScheme.DARK.value},
            {'name': '💙 Blue', 'value': ColorScheme.BLUE.value},
            {'name': '💚 Green', 'value': ColorScheme.GREEN.value},
            {'name': '💜 Purple', 'value': ColorScheme.PURPLE.value}
        ]
        
        self.data['color_scheme'] = questionary.select(
            "Choose a color scheme:",
            choices=color_choices
        ).ask()
        
        # Font family
        font_choices = [
            {'name': 'Classic Sans-Serif', 'value': FontFamily.SANS_SERIF.value},
            {'name': 'Elegant Serif', 'value': FontFamily.SERIF.value},
            {'name': 'Modern Roboto', 'value': FontFamily.ROBOTO.value},
            {'name': 'Clean Open Sans', 'value': FontFamily.OPEN_SANS.value},
            {'name': 'Bold Montserrat', 'value': FontFamily.MONTSERRAT.value}
        ]
        
        self.data['font'] = questionary.select(
            "Choose a font family:",
            choices=font_choices
        ).ask()
    
    def _collect_projects(self):
        """Collect project information."""
        print(Fore.GREEN + "\n🚀 PROJECTS")
        print(Fore.GREEN + "-" * 40)
        
        projects = []
        
        while True:
            print(Fore.YELLOW + f"\nProject #{len(projects) + 1}")
            
            project = {}
            
            project['title'] = questionary.text("Project title:").ask()
            if not project['title']:
                break
            
            project['description'] = questionary.text(
                "Short description:"
            ).ask()
            
            project['url'] = questionary.text(
                "Project URL (optional):"
            ).ask()
            
            project['technologies'] = questionary.text(
                "Technologies used (comma separated):"
            ).ask()
            
            if project['technologies']:
                project['technologies'] = [t.strip() for t in project['technologies'].split(',')]
            
            project['image'] = questionary.path(
                "Project image path (optional):",
                validate=lambda x: not x or Path(x).exists() or "File does not exist"
            ).ask()
            
            projects.append(project)
            
            if not self._ask_yes_no("Add another project?", default=False):
                break
        
        self.data['projects'] = projects
    
    def _collect_skills(self):
        """Collect skills with proficiency levels."""
        print(Fore.GREEN + "\n⚡ SKILLS")
        print(Fore.GREEN + "-" * 40)
        
        skills = []
        
        while True:
            skill = {}
            
            skill['name'] = questionary.text("Skill name:").ask()
            if not skill['name']:
                break
            
            skill['level'] = questionary.select(
                "Proficiency level:",
                choices=[
                    {'name': 'Beginner', 'value': 25},
                    {'name': 'Intermediate', 'value': 50},
                    {'name': 'Advanced', 'value': 75},
                    {'name': 'Expert', 'value': 100}
                ]
            ).ask()
            
            skills.append(skill)
            
            if not self._ask_yes_no("Add another skill?", default=False):
                break
        
        self.data['skills'] = skills
    
    def _collect_experience(self):
        """Collect work experience."""
        print(Fore.GREEN + "\n💼 WORK EXPERIENCE")
        print(Fore.GREEN + "-" * 40)
        
        experiences = []
        
        while True:
            exp = {}
            
            exp['company'] = questionary.text("Company name:").ask()
            if not exp['company']:
                break
            
            exp['position'] = questionary.text("Your position:").ask()
            exp['start_date'] = questionary.text("Start date (e.g., Jan 2020):").ask()
            exp['end_date'] = questionary.text(
                "End date (or 'Present'):",
                default="Present"
            ).ask()
            
            exp['description'] = questionary.text(
                "Description of responsibilities:"
            ).ask()
            
            experiences.append(exp)
            
            if not self._ask_yes_no("Add another experience?", default=False):
                break
        
        self.data['experience'] = experiences
    
    def _collect_education(self):
        """Collect education information."""
        print(Fore.GREEN + "\n🎓 EDUCATION")
        print(Fore.GREEN + "-" * 40)
        
        education = []
        
        while True:
            edu = {}
            
            edu['institution'] = questionary.text("Institution name:").ask()
            if not edu['institution']:
                break
            
            edu['degree'] = questionary.text("Degree/Certificate:").ask()
            edu['field'] = questionary.text("Field of study:").ask()
            edu['year'] = questionary.text("Graduation year:").ask()
            
            education.append(edu)
            
            if not self._ask_yes_no("Add another education entry?", default=False):
                break
        
        self.data['education'] = education
    
    def _collect_social_links(self):
        """Collect social media links."""
        print(Fore.GREEN + "\n🌐 SOCIAL LINKS")
        print(Fore.GREEN + "-" * 40)
        
        social_links = {}
        
        # Common social platforms
        platforms = [
            ('github', '🐙 GitHub'),
            ('linkedin', '🔗 LinkedIn'),
            ('twitter', '🐦 Twitter'),
            ('instagram', '📸 Instagram'),
            ('youtube', '▶️ YouTube'),
            ('medium', '✍️ Medium'),
            ('devto', '👨‍💻 Dev.to'),
            ('personal', '🌍 Personal Website')
        ]
        
        for key, display_name in platforms:
            url = questionary.text(f"{display_name} URL (optional):").ask()
            if url:
                social_links[key] = url
        
        self.data['social_links'] = social_links
    
    def _collect_export_options(self):
        """Collect export preferences."""
        print(Fore.GREEN + "\n📦 EXPORT OPTIONS")
        print(Fore.GREEN + "-" * 40)
        
        self.data['export_format'] = questionary.select(
            "Choose export format:",
            choices=[
                {'name': 'HTML/CSS files only', 'value': 'html_only'},
                {'name': 'Complete project folder', 'value': 'full_project'},
                {'name': 'ZIP archive', 'value': 'zip'},
                {'name': 'Prepare for GitHub Pages', 'value': 'github_pages'}
            ]
        ).ask()
        
        self.data['open_browser'] = self._ask_yes_no(
            "Open in browser after generation?",
            default=True
        )
        
        self.data['save_config'] = self._ask_yes_no(
            "Save configuration for future edits?",
            default=True
        )
    
    def _ask_yes_no(self, question: str, default: bool = True) -> bool:
        """Ask a yes/no question."""
        return questionary.confirm(question, default=default).ask()