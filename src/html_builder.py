"""HTML content builder."""

from typing import Dict, Any, List
from pathlib import Path
import json


class HTMLBuilder:
    """Builds HTML content from user data."""
    
    def __init__(self, template_manager):
        self.template_manager = template_manager
    
    def build(self, data: Dict[str, Any]) -> str:
        """Build complete HTML document."""
        context = self._prepare_context(data)
        
        # Render main template
        html = self.template_manager.render_template('index.html', **context)
        
        return html
    
    def _prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare template context from user data."""
        context = {
            'name': data.get('name', ''),
            'title': data.get('title', ''),
            'bio': data.get('bio', ''),
            'email': data.get('email', ''),
            'avatar': data.get('avatar', ''),
            'template': data.get('template', 'minimal'),
            'color_scheme': data.get('color_scheme', 'light'),
            'font': data.get('font', ''),
            'projects': data.get('projects', []),
            'skills': data.get('skills', []),
            'experience': data.get('experience', []),
            'education': data.get('education', []),
            'social_links': data.get('social_links', {}),
            'generation_date': self._get_generation_date(),
            'has_projects': len(data.get('projects', [])) > 0,
            'has_skills': len(data.get('skills', [])) > 0,
            'has_experience': len(data.get('experience', [])) > 0,
            'has_education': len(data.get('education', [])) > 0,
        }
        
        # Format skills for display
        if context['has_skills']:
            context['skills_html'] = self._build_skills_html(data['skills'])
        
        # Format projects for display
        if context['has_projects']:
            context['projects_html'] = self._build_projects_html(data['projects'])
        
        # Format experience for display
        if context['has_experience']:
            context['experience_html'] = self._build_experience_html(data['experience'])
        
        # Format education for display
        if context['has_education']:
            context['education_html'] = self._build_education_html(data['education'])
        
        # Format social links
        context['social_html'] = self._build_social_html(data.get('social_links', {}))
        
        return context
    
    def _build_skills_html(self, skills: List[Dict]) -> str:
        """Build HTML for skills section."""
        html = '<div class="skills-grid">\n'
        
        for skill in skills:
            html += f'''
            <div class="skill-card">
                <div class="skill-header">
                    <span class="skill-name">{skill['name']}</span>
                    <span class="skill-percentage">{skill['level']}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {skill['level']}%"></div>
                </div>
            </div>
            '''
        
        html += '</div>\n'
        return html
    
    def _build_projects_html(self, projects: List[Dict]) -> str:
        """Build HTML for projects section."""
        html = '<div class="projects-grid">\n'
        
        for project in projects:
            html += '<div class="project-card">\n'
            
            if project.get('image'):
                html += f'<img src="{project["image"]}" alt="{project["title"]}" class="project-image">\n'
            
            html += f'<h3>{project["title"]}</h3>\n'
            html += f'<p>{project["description"]}</p>\n'
            
            if project.get('technologies'):
                html += '<div class="project-tech">\n'
                for tech in project['technologies']:
                    html += f'<span class="tech-tag">{tech}</span>\n'
                html += '</div>\n'
            
            if project.get('url'):
                html += f'<a href="{project["url"]}" target="_blank" class="project-link">View Project →</a>\n'
            
            html += '</div>\n'
        
        html += '</div>\n'
        return html
    
    def _build_experience_html(self, experiences: List[Dict]) -> str:
        """Build HTML for experience section."""
        html = '<div class="timeline">\n'
        
        for exp in experiences:
            html += '''
            <div class="timeline-item">
                <div class="timeline-content">
                    <h3>{company}</h3>
                    <h4>{position}</h4>
                    <p class="timeline-date">{start} - {end}</p>
                    <p>{description}</p>
                </div>
            </div>
            '''.format(**exp)
        
        html += '</div>\n'
        return html
    
    def _build_education_html(self, education: List[Dict]) -> str:
        """Build HTML for education section."""
        html = '<div class="education-list">\n'
        
        for edu in education:
            html += '''
            <div class="education-item">
                <h3>{institution}</h3>
                <p class="education-degree">{degree} in {field}</p>
                <p class="education-year">{year}</p>
            </div>
            '''.format(**edu)
        
        html += '</div>\n'
        return html
    
    def _build_social_html(self, social_links: Dict[str, str]) -> str:
        """Build HTML for social links."""
        if not social_links:
            return ''
        
        html = '<div class="social-links">\n'
        
        icon_map = {
            'github': 'fab fa-github',
            'linkedin': 'fab fa-linkedin',
            'twitter': 'fab fa-twitter',
            'instagram': 'fab fa-instagram',
            'youtube': 'fab fa-youtube',
            'medium': 'fab fa-medium',
            'devto': 'fab fa-dev',
            'personal': 'fas fa-globe'
        }
        
        for platform, url in social_links.items():
            icon_class = icon_map.get(platform, 'fas fa-link')
            html += f'<a href="{url}" target="_blank" class="social-link" aria-label="{platform}">'
            html += f'<i class="{icon_class}"></i>'
            html += '</a>\n'
        
        html += '</div>\n'
        return html
    
    def _get_generation_date(self) -> str:
        """Get current date for generation timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")