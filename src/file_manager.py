"""File operations management."""

import os
import shutil
from pathlib import Path
from typing import Optional, List, Union
import hashlib
from datetime import datetime

from .utils.constants import OUTPUT_DIR, ASSETS_DIR
from .utils.validators import sanitize_filename


class FileManager:
    """Manages all file operations."""
    
    def __init__(self, base_dir: Path = OUTPUT_DIR):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.current_output_dir = None
    
    def create_output_directory(self, name: Optional[str] = None) -> Path:
        """Create a new output directory with optional name."""
        if name:
            dir_name = sanitize_filename(name)
            self.current_output_dir = self.base_dir / dir_name
        else:
            # Create timestamp-based directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.current_output_dir = self.base_dir / f"portfolio_{timestamp}"
        
        self.current_output_dir.mkdir(parents=True, exist_ok=True)
        return self.current_output_dir
    
    def write_file(self, filename: str, content: str) -> Path:
        """Write content to a file in current output directory."""
        if not self.current_output_dir:
            self.create_output_directory()
        
        file_path = self.current_output_dir / sanitize_filename(filename)
        file_path.write_text(content, encoding='utf-8')
        return file_path
    
    def copy_file(self, source: Union[str, Path], dest_filename: Optional[str] = None) -> Optional[Path]:
        """Copy a file to output directory."""
        source_path = Path(source)
        if not source_path.exists():
            return None
        
        if not self.current_output_dir:
            self.create_output_directory()
        
        dest_name = dest_filename or source_path.name
        dest_path = self.current_output_dir / sanitize_filename(dest_name)
        
        shutil.copy2(source_path, dest_path)
        return dest_path
    
    def copy_directory(self, source: Union[str, Path], dest_name: Optional[str] = None) -> Optional[Path]:
        """Copy an entire directory to output directory."""
        source_path = Path(source)
        if not source_path.exists() or not source_path.is_dir():
            return None
        
        if not self.current_output_dir:
            self.create_output_directory()
        
        dest_name = dest_name or source_path.name
        dest_path = self.current_output_dir / sanitize_filename(dest_name)
        
        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
        return dest_path
    
    def copy_assets(self, template_name: str) -> List[Path]:
        """Copy template assets to output directory."""
        assets_copied = []
        
        # Copy template-specific assets
        template_assets = ASSETS_DIR / template_name
        if template_assets.exists():
            dest_assets = self.current_output_dir / "assets"
            dest_assets.mkdir(exist_ok=True)
            
            for item in template_assets.glob('*'):
                if item.is_file():
                    shutil.copy2(item, dest_assets / item.name)
                    assets_copied.append(dest_assets / item.name)
        
        # Copy common assets
        common_assets = ASSETS_DIR / "common"
        if common_assets.exists():
            dest_assets = self.current_output_dir / "assets"
            dest_assets.mkdir(exist_ok=True)
            
            for item in common_assets.glob('*'):
                if item.is_file():
                    shutil.copy2(item, dest_assets / item.name)
                    assets_copied.append(dest_assets / item.name)
        
        return assets_copied
    
    def create_zip(self, zip_name: Optional[str] = None) -> Path:
        """Create a ZIP archive of the output directory."""
        import zipfile
        
        if not self.current_output_dir or not self.current_output_dir.exists():
            raise FileNotFoundError("No output directory to zip")
        
        if not zip_name:
            zip_name = f"{self.current_output_dir.name}.zip"
        
        zip_path = self.base_dir / zip_name
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in self.current_output_dir.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(self.current_output_dir)
                    zipf.write(file, arcname)
        
        return zip_path
    
    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def cleanup_old_outputs(self, days: int = 7) -> int:
        """Remove output directories older than specified days."""
        import time
        removed = 0
        current_time = time.time()
        max_age = days * 24 * 60 * 60  # Convert days to seconds
        
        for item in self.base_dir.iterdir():
            if item.is_dir():
                mtime = item.stat().st_mtime
                if current_time - mtime > max_age:
                    shutil.rmtree(item)
                    removed += 1
        
        return removed