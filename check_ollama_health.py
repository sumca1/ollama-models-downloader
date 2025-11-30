"""
Ollama Health Check - System Verification
בדיקת תקינות התקנת Ollama
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """הרץ פקודה ותחזיר פלט"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)


def check_ollama_installed():
    """בדיקה אם Ollama מותקן"""
    print("🔍 Checking Ollama installation...")
    success, stdout, stderr = run_command("ollama --version")
    
    if success:
        version = stdout.strip().split('\n')[0] if stdout else "Unknown"
        print(f"  ✅ Ollama installed: {version}")
        return True
    else:
        print(f"  ❌ Ollama not found!")
        print(f"     Install from: https://ollama.com/download")
        return False


def check_ollama_running():
    """בדיקה אם שירות Ollama פועל"""
    print("\n🔍 Checking Ollama service...")
    success, stdout, stderr = run_command("ollama list")
    
    if success:
        print(f"  ✅ Ollama service is running")
        return True
    else:
        print(f"  ⚠️  Ollama service might not be running")
        print(f"     Try: ollama serve")
        return False


def list_models():
    """רשימת מודלים זמינים"""
    print("\n📋 Available models:")
    success, stdout, stderr = run_command("ollama list")
    
    if success and stdout:
        lines = stdout.strip().split('\n')
        if len(lines) > 1:
            for line in lines[1:]:
                if line.strip():
                    parts = line.split()
                    if parts:
                        model_name = parts[0]
                        print(f"  • {model_name}")
            return True
        else:
            print("  ⚠️  No models installed yet")
            return False
    else:
        print("  ❌ Could not list models")
        return False


def check_models_directory():
    """בדיקת תיקיית המודלים"""
    print("\n📂 Checking models directory...")
    
    home = Path.home()
    models_dir = home / ".ollama" / "models"
    
    if models_dir.exists():
        print(f"  ✅ Directory exists: {models_dir}")
        
        manifests_dir = models_dir / "manifests"
        if manifests_dir.exists():
            manifest_count = len(list(manifests_dir.rglob("*")))
            print(f"  📄 Manifests: {manifest_count} files")
        else:
            print(f"  ⚠️  No manifests directory")
            
        blobs_dir = models_dir / "blobs"
        if blobs_dir.exists():
            blob_count = len(list(blobs_dir.glob("*")))
            total_size = sum(
                f.stat().st_size for f in blobs_dir.glob("*") if f.is_file()
            )
            size_gb = total_size / (1024**3)
            print(f"  💾 Blobs: {blob_count} files ({size_gb:.2f} GB)")
        else:
            print(f"  ⚠️  No blobs directory")
            
        return True
    else:
        print(f"  ❌ Directory not found: {models_dir}")
        print(f"     Models should be extracted to this location")
        return False


def test_model(model_name="llama3.1:8b"):
    """בדיקת מודל ספציפי"""
    print(f"\n🧪 Testing model: {model_name}...")
    
    cmd = f'ollama run {model_name} "2+2=?"'
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print(f"  ✅ Model works!")
        if stdout:
            response = stdout.strip()[:100]
            print(f"  💬 Response: {response}...")
        return True
    else:
        print(f"  ❌ Model test failed")
        if stderr:
            print(f"     Error: {stderr[:200]}")
        return False


def main():
    print("=" * 60)
    print("🤖 Ollama Models - Quick Health Check")
    print("=" * 60)
    
    checks = {
        "Ollama Installed": check_ollama_installed(),
        "Ollama Running": check_ollama_running(),
        "Models Directory": check_models_directory(),
        "Models Available": list_models()
    }
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    all_good = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if not result:
            all_good = False
    
    if all_good:
        print("\n🎉 Everything looks good!")
        print("\n🚀 Next steps:")
        print("   ollama run llama3.1:8b")
        print('   ollama run llama3.1:8b "שלום עולם"')
    else:
        print("\n⚠️  Some issues detected")
        print("\n📖 Check the guide:")
        print("   OLLAMA_MODELS_GUIDE.md")
        print("   OLLAMA_QUICKSTART.md")
    
    print("=" * 60)
    
    if checks["Models Available"]:
        print("\n🧪 Running quick model test...")
        test_model()
    
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
