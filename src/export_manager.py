"""Export management for different formats."""

import os
import shutil
import json
import zipfile
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from .utils.constants import EXPORTS_DIR, CONFIGS_DIR
from .utils.formatters import save_config


class ExportManager:
    """Manages exporting of generated portfolios."""
    
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.exports_dir = EXPORTS_DIR
        self.exports_dir.mkdir(exist_ok=True)
    
    def export(self, data: Dict[str, Any], format: str) -> Dict[str, Any]:
        """Export in specified format."""
        export_result = {
            'success': False,
            'format': format,
            'paths': [],
            'message': ''
        }
        
        try:
            if format == 'html_only':
                paths = self._export_html_only()
            elif format == 'full_project':
                paths = self._export_full_project()
            elif format == 'zip':
                paths = self._export_as_zip(data)
            elif format == 'github_pages':
                paths = self._export_for_github_pages(data)
            else:
                export_result['message'] = f"Unknown format: {format}"
                return export_result
            
            export_result['success'] = True
            export_result['paths'] = paths
            export_result['message'] = f"Successfully exported as {format}"
            
        except Exception as e:
            export_result['message'] = str(e)
        
        return export_result
    
    def _export_html_only(self) -> list:
        """Export only HTML and CSS files."""
        paths = []
        
        if self.file_manager.current_output_dir:
            for ext in ['*.html', '*.css']:
                for file in self.file_manager.current_output_dir.glob(ext):
                    paths.append(str(file))
        
        return paths
    
    def _export_full_project(self) -> list:
        """Export complete project folder."""
        paths = []
        
        if self.file_manager.current_output_dir:
            # Create a copy in exports
            export_name = f"{self.file_manager.current_output_dir.name}_full"
            export_path = self.exports_dir / export_name
            shutil.copytree(self.file_manager.current_output_dir, export_path)
            paths.append(str(export_path))
        
        return paths
    
    def _export_as_zip(self, data: Dict[str, Any]) -> list:
        """Export as ZIP archive."""
        paths = []
        
        if self.file_manager.current_output_dir:
            zip_name = f"{self.file_manager.current_output_dir.name}.zip"
            zip_path = self.file_manager.create_zip(zip_name)
            paths.append(str(zip_path))
            
            # Also save config
            if data.get('save_config'):
                config_name = f"{self.file_manager.current_output_dir.name}_config.json"
                config_path = save_config(data, config_name)
                paths.append(str(config_path))
        
        return paths
    
    def _export_for_github_pages(self, data: Dict[str, Any]) -> list:
        """Prepare for GitHub Pages deployment."""
        paths = []
        
        if self.file_manager.current_output_dir:
            # Create a special GitHub Pages structure
            gh_pages_dir = self.exports_dir / f"{self.file_manager.current_output_dir.name}_gh_pages"
            gh_pages_dir.mkdir(exist_ok=True)
            
            # Copy files
            for file in self.file_manager.current_output_dir.glob('*'):
                if file.suffix in ['.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg']:
                    shutil.copy2(file, gh_pages_dir / file.name)
            
            # Create a basic README for GitHub Pages
            readme_content = f"""# Portfolio Website

Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## About
Personal portfolio website for {data.get('name', 'Unknown')}

## Deployment
This site is ready to be deployed on GitHub Pages.
"""
            readme_path = gh_pages_dir / "README.md"
            readme_path.write_text(readme_content)
            
            paths.append(str(gh_pages_dir))
        
        return paths
    
    def create_deployment_package(self, data: Dict[str, Any]) -> Optional[Path]:
        """Create a complete deployment package."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"portfolio_deploy_{timestamp}"
        package_path = self.exports_dir / package_name
        package_path.mkdir(exist_ok=True)
        
        # Copy all generated files
        if self.file_manager.current_output_dir:
            shutil.copytree(
                self.file_manager.current_output_dir,
                package_path / "website",
                dirs_exist_ok=True
            )
        
        # Save configuration
        config_path = package_path / "config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Create deployment instructions
        instructions = f"""# Portfolio Deployment Package

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Contents
- /website - Generated portfolio files
- config.json - Your configuration data

## Deployment Options

### 1. Local Viewing
Open website/index.html in your browser

### 2. GitHub Pages
1. Create a new repository on GitHub
2. Upload the contents of the /website folder
3. Enable GitHub Pages in repository settings

### 3. Netlify/Vercel
Drag and drop the /website folder to deploy

### 4. Traditional Web Hosting
Upload the /website contents to your web server

## Need Help?
Visit our documentation for detailed deployment guides.
"""
        instructions_path = package_path / "DEPLOYMENT.md"
        instructions_path.write_text(instructions)
        
        # Create ZIP of the package
        zip_path = self.exports_dir / f"{package_name}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in package_path.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(package_path)
                    zipf.write(file, arcname)
        
        # Clean up temporary directory
        shutil.rmtree(package_path)
        
        return zip_path