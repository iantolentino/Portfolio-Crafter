#!/usr/bin/env python3
"""
Working Portfolio Generator with Jinja2 templating
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

def generate():
    print("🎨 Portfolio Generator")
    print("=" * 50)
    
    # Get user input
    data = {}
    
    print("\n📋 BASIC INFORMATION")
    data['name'] = input("Your name: ").strip()
    data['title'] = input("Your title (e.g., Software Developer): ").strip()
    data['bio'] = input("Short bio: ").strip()
    data['email'] = input("Email: ").strip()
    data['github_link'] = input("GitHub URL (optional): ").strip()
    data['linkedin_link'] = input("LinkedIn URL (optional): ").strip()
    
    # Get projects
    print("\n🚀 PROJECTS (press Enter without title to finish)")
    projects = []
    while True:
        print(f"\nProject #{len(projects) + 1}:")
        title = input("  Title: ").strip()
        if not title:
            break
        
        project = {
            'title': title,
            'description': input("  Description: ").strip(),
            'url': input("  URL: ").strip(),
            'technologies': []
        }
        
        tech_input = input("  Technologies (comma separated): ").strip()
        if tech_input:
            project['technologies'] = [t.strip() for t in tech_input.split(',')]
        
        projects.append(project)
    
    data['projects'] = projects
    data['has_projects'] = len(projects) > 0
    
    # Get skills (optional)
    print("\n⚡ SKILLS (press Enter without name to finish)")
    skills = []
    while True:
        name = input("  Skill name: ").strip()
        if not name:
            break
        
        skill = {'name': name}
        
        level = input("  Level (1-100): ").strip()
        if level.isdigit():
            skill['level'] = int(level)
        
        skills.append(skill)
    
    data['skills'] = skills
    data['has_skills'] = len(skills) > 0
    
    # Get experience (optional)
    print("\n💼 EXPERIENCE (press Enter without company to finish)")
    experience = []
    while True:
        company = input("  Company: ").strip()
        if not company:
            break
        
        exp = {
            'company': company,
            'position': input("  Position: ").strip(),
            'start_date': input("  Start date: ").strip(),
            'end_date': input("  End date (or Present): ").strip() or "Present",
            'description': input("  Description: ").strip()
        }
        
        experience.append(exp)
    
    data['experience'] = experience
    data['has_experience'] = len(experience) > 0
    
    # Get education (optional)
    print("\n🎓 EDUCATION (press Enter without institution to finish)")
    education = []
    while True:
        institution = input("  Institution: ").strip()
        if not institution:
            break
        
        edu = {
            'institution': institution,
            'degree': input("  Degree: ").strip(),
            'field': input("  Field of study: ").strip(),
            'year': input("  Year: ").strip()
        }
        
        education.append(edu)
    
    data['education'] = education
    data['has_education'] = len(education) > 0
    
    # Add generation date
    data['generation_date'] = datetime.now().strftime("%Y")
    
    # Setup Jinja2 environment
    template_dir = Path("templates/minimal")
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Load and render template
    try:
        template = env.get_template('index.html')
        html_content = template.render(**data)
    except Exception as e:
        print(f"Error rendering template: {e}")
        return
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Write files
    with open(output_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Copy CSS
    css_source = template_dir / "style.css"
    if css_source.exists():
        shutil.copy2(css_source, output_dir / "style.css")
    
    print(f"\n✅ Portfolio generated successfully!")
    print(f"📁 Location: {output_dir.absolute()}")
    print(f"🌐 Open {output_dir}/index.html in your browser")

if __name__ == "__main__":
    generate()