"""Preview management for generated websites."""

import webbrowser
import time
import threading
from pathlib import Path
from typing import Optional
import http.server
import socketserver
from urllib.parse import urlparse


class PreviewManager:
    """Manages preview functionality for generated websites."""
    
    def __init__(self):
        self.server = None
        self.server_thread = None
        self.port = 8000
        
    def open_in_browser(self, file_path: Path) -> bool:
        """Open the generated HTML file in default browser."""
        try:
            file_url = file_path.absolute().as_uri()
            webbrowser.open(file_url)
            return True
        except Exception:
            return False
    
    def start_local_server(self, directory: Path, port: int = 8000) -> bool:
        """Start a local HTTP server for preview."""
        self.port = port
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(directory), **kwargs)
        
        try:
            self.server = socketserver.TCPServer(("", port), Handler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            # Wait a moment for server to start
            time.sleep(1)
            
            return True
        except Exception:
            return False
    
    def stop_local_server(self):
        """Stop the local HTTP server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
    
    def open_local_server(self, directory: Path, port: int = 8000) -> Optional[str]:
        """Start server and open in browser."""
        if self.start_local_server(directory, port):
            url = f"http://localhost:{port}"
            webbrowser.open(url)
            return url
        return None
    
    def generate_qr_code(self, url: str) -> Optional[Path]:
        """Generate QR code for mobile preview."""
        try:
            import qrcode
            from PIL import Image
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to temp file
            qr_path = Path("preview_qr.png")
            img.save(qr_path)
            
            return qr_path
        except ImportError:
            return None
    
    def get_network_url(self) -> Optional[str]:
        """Get local network URL for mobile testing."""
        import socket
        
        try:
            # Get local IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            
            return f"http://{ip}:{self.port}"
        except Exception:
            return None
    
    def create_preview_screenshot(self, url: str, output_path: Path) -> bool:
        """Create a screenshot of the preview (requires selenium)."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Take screenshot
            driver.save_screenshot(str(output_path))
            driver.quit()
            
            return True
        except ImportError:
            return False
        except Exception:
            return False