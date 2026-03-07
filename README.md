# Portfolio Website Generator

A command-line tool that creates personal portfolio websites from templates. Users answer questions about themselves, and the tool generates a complete, ready-to-use website.

## Features

- Interactive command-line interface for data entry
- Multiple template designs (minimal, modern, creative)
- Customizable color schemes and fonts
- Support for projects, skills, work experience, and education
- Generates static HTML/CSS files that work on any web server
- Preview website locally before deploying

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository
2. Navigate to the project directory
3. Install required packages:

```
pip install -r requirements.txt
```

The requirements.txt file includes:
- colorama: For colored terminal output
- jinja2: For template processing
- pyyaml: For template configuration files
- Pillow: For image processing (optional)

## Usage

### Basic Usage

Run the generator with default settings:

```
python run.py
```

The program will guide you through entering:
- Your name, title, and bio
- Contact information
- Projects (with descriptions and technologies)
- Skills and proficiency levels
- Work experience
- Education history

After entering your information, the generator creates a complete website in the `output` folder.

### Using Different Templates

The generator includes three templates in the `templates` directory:
- `minimal`: Clean, simple design focused on content
- `modern`: Contemporary layout with cards and grids
- `creative`: Bold design for creative professionals

To use a specific template, modify the template selection in the script or create a configuration file.

## File Structure

```
portfolio-generator/
│
├── working_generator.py          # Main generator script
├── requirements.txt              # Python dependencies
│
├── templates/                    # Template files
│   ├── minimal/                  # Minimal template
│   │   ├── index.html            # HTML template with Jinja2 syntax
│   │   └── style.css             # CSS styling
│   ├── modern/                   
│   │   ├── index.html
│   │   └── style.css
│   └── creative/
│       ├── index.html
│       └── style.css
│
└── output/                       # Generated websites (created on first run)
```

## Template Customization

### HTML Templates

Templates use Jinja2 syntax for dynamic content. Common variables available:

- `{{ name }}` - User's name
- `{{ title }}` - Professional title
- `{{ bio }}` - Biography text
- `{{ email }}` - Contact email
- `{{ projects }}` - List of project dictionaries
- `{{ skills }}` - List of skill dictionaries
- `{{ experience }}` - List of experience dictionaries
- `{{ education }}` - List of education dictionaries
- `{{ generation_date }}` - Current year for copyright

Conditional blocks:
```
{% if projects %}
  Show projects section
{% endif %}

{% for project in projects %}
  {{ project.title }}
{% endfor %}
```

### CSS Styling

The CSS files use CSS variables for easy customization. Common variables in the minimal template:

```css
:root {
    --bg-primary: #ffffff;
    --text-primary: #1a1a1a;
    --accent: #0366d6;
    --border: #eaeaea;
}
```

## Developer Guide

### Extending the Generator

The generator is built as a single script (`working_generator.py`) for simplicity. To add features:

1. **Add new input fields**: Modify the input collection sections in the `generate()` function
2. **Add new template variables**: Pass additional data to the template.render() method
3. **Create new templates**: Add folders in the `templates` directory with index.html and style.css

### Template Variables Reference

Project dictionary structure:
```python
{
    'title': 'Project Name',
    'description': 'Project description',
    'url': 'https://example.com',
    'technologies': ['Python', 'JavaScript']
}
```

Skill dictionary structure:
```python
{
    'name': 'Python',
    'level': 85  # Integer from 1-100
}
```

Experience dictionary structure:
```python
{
    'company': 'Company Name',
    'position': 'Job Title',
    'start_date': 'Jan 2020',
    'end_date': 'Present',
    'description': 'Job responsibilities'
}
```

### Testing

Run the test files to verify functionality:

```
python -m pytest tests/
```

The `tests` directory contains:
- `test_validators.py`: Tests for input validation
- `test_html_builder.py`: Tests for HTML generation
- `test_generator.py`: Tests for main generator functions

## Deployment

### Local Testing

After generating your website:

1. Navigate to the `output` folder
2. Open `index.html` in any web browser
3. The site works without a web server

### Publishing Online

The generated site consists of static files that can be uploaded to any web hosting service:

1. **GitHub Pages**: Upload the contents of the `output` folder to a GitHub repository and enable GitHub Pages
2. **Netlify/Vercel**: Drag and drop the `output` folder to deploy
3. **Traditional hosting**: Use FTP to upload files to your web server
4. **Local server**: For testing, you can run `python -m http.server` in the output directory

## Troubleshooting

### Common Issues

**Template not found**
- Ensure the templates folder exists with at least one template
- Check that template folders contain index.html and style.css

**Generated HTML shows raw template tags**
- Make sure Jinja2 is installed: `pip install jinja2`
- The template uses Jinja2 syntax (`{{ }}` and `{% %}`)

**CSS not applying**
- Verify style.css is in the same folder as index.html
- Check browser console for 404 errors
- CSS variables require modern browser support

**Git push errors**
- If you get "src refspec main does not match any", run: `git branch -m master main`
- For force push issues: `git push origin main --force`

## License

This project is open source. You can modify and distribute it as needed.

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Include the error message and steps to reproduce
