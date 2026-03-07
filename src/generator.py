"""Main generator class orchestrating the portfolio creation process."""

import sys
from pathlib import Path
from typing import Optional
from colorama import init, Fore, Style

from .user_input_collector import UserInputCollector
from .template_manager import TemplateManager
from .html_builder import HTMLBuilder
from .css_builder import CSSBuilder
from .file_manager import FileManager
from .export_manager import ExportManager
from .preview_manager import PreviewManager
from .utils.formatters import save_config
from .utils.constants import OUTPUT_DIR

# Initialize colorama
init(autoreset=True)


class PortfolioGenerator:
    """Main orchestrator for portfolio generation."""
    
    def __init__(self):
        self.input_collector = UserInputCollector()
        self.template_manager = TemplateManager()
        self.html_builder = HTMLBuilder(self.template_manager)
        self.css_builder = CSSBuilder()
        self.file_manager = FileManager()
        self.export_manager = ExportManager(self.file_manager)
        self.preview_manager = PreviewManager()
        
        self.user_data = None
    
    def run(self):
        """Execute the complete portfolio generation workflow."""
        try:
            # Step 1: Check for available templates
            self._check_templates()
            
            # Step 2: Collect user input
            self.user_data = self.input_collector.collect_all()
            
            # Step 3: Generate website
            self._generate_website()
            
            # Step 4: Export based on user preference
            self._export_website()
            
            # Step 5: Preview if requested
            if self.user_data.get('open_browser'):
                self._preview_website()
            
            # Step 6: Save configuration if requested
            if self.user_data.get('save_config'):
                self._save_configuration()
            
            # Step 7: Show summary
            self._show_summary()
            
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n\n⚠️  Generation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(Fore.RED + f"\n❌ Error during generation: {e}")
            raise
    
    def _check_templates(self):
        """Check if templates are available."""
        templates = self.template_manager.list_templates()
        if not templates:
            print(Fore.RED + "❌ No templates found in the 'templates' directory.")
            print(Fore.YELLOW + "Please ensure you have at least one template folder with index.html and style.css")
            sys.exit(1)
    
    def _generate_website(self):
        """Generate the website files."""
        print(Fore.CYAN + "\n🔄 Generating your portfolio...")
        
        # Load selected template
        template_name = self.user_data['template']
        if not self.template_manager.load_template(template_name):
            print(Fore.RED + f"❌ Failed to load template: {template_name}")
            print(Fore.YELLOW + f"Available templates: {', '.join(self.template_manager.list_templates())}")
            sys.exit(1)
        
        # Create output directory
        output_name = f"{self.user_data['name'].replace(' ', '_').lower()}_portfolio"
        self.file_manager.create_output_directory(output_name)
        
        # Generate HTML
        print(Fore.CYAN + "  📝 Generating HTML...")
        html_content = self.html_builder.build(self.user_data)
        html_path = self.file_manager.write_file('index.html', html_content)
        
        # Generate CSS
        print(Fore.CYAN + "  🎨 Generating CSS...")
        template_css_path = self.template_manager.get_css_path(template_name)
        template_css = template_css_path.read_text(encoding='utf-8')
        css_content = self.css_builder.build(template_css, self.user_data)
        css_path = self.file_manager.write_file('style.css', css_content)
        
        # Copy assets
        print(Fore.CYAN + "  🖼️  Copying assets...")
        assets = self.file_manager.copy_assets(template_name)
        
        print(Fore.GREEN + f"  ✅ Generated {len(assets)} assets")
    
    def _export_website(self):
        """Export the website in requested format."""
        export_format = self.user_data.get('export_format', 'html_only')
        
        print(Fore.CYAN + f"\n📦 Exporting as {export_format}...")
        
        result = self.export_manager.export(self.user_data, export_format)
        
        if result['success']:
            print(Fore.GREEN + f"  ✅ Export successful!")
            for path in result['paths']:
                print(Fore.GREEN + f"     📁 {path}")
        else:
            print(Fore.RED + f"  ❌ Export failed: {result['message']}")
    
    def _preview_website(self):
        """Open the website in browser for preview."""
        print(Fore.CYAN + "\n🌐 Opening in browser...")
        
        html_path = self.file_manager.current_output_dir / 'index.html'
        if html_path.exists():
            self.preview_manager.open_in_browser(html_path)
            
            # Optionally start local server
            if self._ask_for_local_server():
                url = self.preview_manager.open_local_server(self.file_manager.current_output_dir)
                if url:
                    print(Fore.GREEN + f"  ✅ Local server started at {url}")
                    
                    # Show network URL for mobile testing
                    network_url = self.preview_manager.get_network_url()
                    if network_url:
                        print(Fore.YELLOW + f"  📱 Mobile testing: {network_url}")
        else:
            print(Fore.RED + "  ❌ HTML file not found for preview")
    
    def _save_configuration(self):
        """Save user configuration for future use."""
        config_name = f"{self.user_data['name'].replace(' ', '_').lower()}_config.json"
        config_path = save_config(self.user_data, config_name)
        print(Fore.GREEN + f"\n💾 Configuration saved: {config_path}")
    
    def _show_summary(self):
        """Display generation summary."""
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.GREEN + "✨ PORTFOLIO GENERATION COMPLETE! ✨".center(60))
        print(Fore.CYAN + "=" * 60)
        
        print(Fore.WHITE + f"\n📊 Summary:")
        print(Fore.WHITE + f"   • Name: {self.user_data.get('name', 'N/A')}")
        print(Fore.WHITE + f"   • Template: {self.user_data.get('template', 'N/A')}")
        print(Fore.WHITE + f"   • Projects: {len(self.user_data.get('projects', []))}")
        print(Fore.WHITE + f"   • Skills: {len(self.user_data.get('skills', []))}")
        print(Fore.WHITE + f"   • Experience: {len(self.user_data.get('experience', []))}")
        print(Fore.WHITE + f"   • Education: {len(self.user_data.get('education', []))}")
        
        print(Fore.WHITE + f"\n📁 Output location:")
        print(Fore.WHITE + f"   {self.file_manager.current_output_dir}")
        
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.YELLOW + "Thank you for using Portfolio Generator! 🚀".center(60))
        print(Fore.CYAN + "=" * 60)
    
    def _ask_for_local_server(self) -> bool:
        """Ask user if they want to start a local server."""
        response = input(Fore.YELLOW + "\nStart local server for better preview? (y/N): ").lower()
        return response == 'y'