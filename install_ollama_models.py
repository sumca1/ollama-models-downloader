#!/usr/bin/env python3
"""
Ollama Models Manager - Install downloaded models offline
התקנת מודלים של Ollama ממקורות offline
"""

import sys
import json
import tarfile
from pathlib import Path
from typing import List, Dict
import subprocess


class OllamaModelsInstaller:
    def __init__(self):
        self.home = Path.home()
        
        # Detect OS and set paths
        if sys.platform == "win32":
            self.ollama_dir = self.home / ".ollama" / "models"
        else:
            self.ollama_dir = self.home / ".ollama" / "models"
            
        self.models_dir = self.ollama_dir
        
    def check_ollama_installed(self) -> bool:
        """בדיקה אם Ollama מותקן"""
        try:
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
            
    def install_models_from_archive(self, archive_path: Path) -> bool:
        """התקנת מודלים מארכיון שהורד"""
        try:
            archive_path = Path(archive_path)
            
            if not archive_path.exists():
                print(f"❌ Archive not found: {archive_path}")
                return False
                
            print(f"📦 Extracting models from {archive_path.name}...")
            
            # Create models directory if it doesn't exist
            self.models_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract based on file type
            if archive_path.suffix in ['.tar', '.gz', '.tgz']:
                self._extract_tar(archive_path)
            elif archive_path.suffix == '.zip':
                self._extract_zip(archive_path)
            else:
                print(f"❌ Unsupported archive format: {archive_path.suffix}")
                return False
                
            print("✅ Models installed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False
            
    def _extract_tar(self, tar_path: Path):
        """חילוץ קובץ tar"""
        with tarfile.open(tar_path, 'r:*') as tar:
            tar.extractall(self.models_dir)
            
    def _extract_zip(self, zip_path: Path):
        """חילוץ קובץ zip"""
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.models_dir)
            
    def list_installed_models(self) -> List[str]:
        """רשימת מודלים מותקנים"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                models = [line.split()[0] for line in lines if line.strip()]
                return models
            return []
            
        except Exception as e:
            print(f"❌ Failed to list models: {e}")
            return []
            
    def verify_installation(self) -> Dict[str, any]:
        """אימות התקנה"""
        models = self.list_installed_models()
        
        total_size = 0
        if self.models_dir.exists():
            for path in self.models_dir.rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
                    
        return {
            "installed_models": models,
            "total_models": len(models),
            "total_size_gb": round(total_size / (1024**3), 2),
            "models_dir": str(self.models_dir),
            "ollama_installed": self.check_ollama_installed()
        }
        
    def install_from_directory(self, source_dir: Path):
        """התקנה מתיקייה שחולצה"""
        source_dir = Path(source_dir)
        
        if not source_dir.exists():
            print(f"❌ Source directory not found: {source_dir}")
            return False
            
        print(f"📂 Installing from directory: {source_dir}")
        
        # Look for manifests and blobs archives
        for tar_file in source_dir.glob("*.tar.gz"):
            print(f"📦 Extracting {tar_file.name}...")
            self._extract_tar(tar_file)
            
        # Check for metadata
        metadata_file = source_dir / "METADATA.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                print(f"\n📊 Package Info:")
                print(f"   Models: {metadata.get('models', 'Unknown')}")
                print(f"   Downloaded: {metadata.get('downloaded_at', 'Unknown')}")
                print(f"   Size: {metadata.get('total_size_mb', 'Unknown')} MB")
                
        return True


def main():
    print("🤖 Ollama Models Offline Installer")
    print("=" * 50)
    
    installer = OllamaModelsInstaller()
    
    # Check Ollama installation
    if not installer.check_ollama_installed():
        print("\n⚠️  Ollama is not installed!")
        print("Please install Ollama first:")
        print("  Windows: https://ollama.com/download/windows")
        print("  Linux/Mac: curl -fsSL https://ollama.com/install.sh | sh")
        sys.exit(1)
        
    print(f"✅ Ollama is installed")
    print(f"📂 Models directory: {installer.models_dir}")
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("\n❓ Usage:")
        print("  python install_ollama_models.py <path-to-archive-or-directory>")
        print("\nExample:")
        print("  python install_ollama_models.py ./ollama-models-export")
        print("  python install_ollama_models.py ./manifests.tar.gz")
        sys.exit(1)
        
    source = Path(sys.argv[1])
    
    # Install based on source type
    if source.is_dir():
        success = installer.install_from_directory(source)
    elif source.is_file():
        success = installer.install_models_from_archive(source)
    else:
        print(f"❌ Invalid source: {source}")
        sys.exit(1)
        
    if success:
        print("\n" + "=" * 50)
        print("🎉 Installation Complete!")
        print("=" * 50)
        
        # Verify installation
        info = installer.verify_installation()
        print(f"\n📊 Status:")
        print(f"   Installed Models: {info['total_models']}")
        print(f"   Total Size: {info['total_size_gb']} GB")
        print(f"   Location: {info['models_dir']}")
        
        if info['installed_models']:
            print(f"\n📋 Available Models:")
            for model in info['installed_models']:
                print(f"   • {model}")
                
        print("\n🚀 You can now use:")
        print("   ollama list              # List all models")
        print("   ollama run llama3.1-8b   # Run a model")
        
    else:
        print("\n❌ Installation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
