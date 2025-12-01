#!/usr/bin/env python3
"""
Download GitHub Actions artifacts without GitHub CLI
Supports multiple download methods to bypass restrictions
"""

import requests
import os
import sys
from pathlib import Path

def download_artifact_browser_url(repo, run_id, artifact_name):
    """Method 1: Generate browser download URL"""
    url = f"https://github.com/{repo}/actions/runs/{run_id}/artifacts/{artifact_name}"
    print(f"🌐 Browser download URL:")
    print(f"   {url}")
    print(f"\n   Open this URL in browser and click download")
    return url

def download_artifact_api(repo, run_id, token=None):
    """Method 2: Use GitHub API (requires authentication token)"""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    # Get artifacts list
    url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/artifacts"
    print(f"\n📦 Fetching artifacts from run {run_id}...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data['total_count'] == 0:
            print("❌ No artifacts found in this run")
            return None
        
        print(f"✅ Found {data['total_count']} artifact(s):\n")
        
        for i, artifact in enumerate(data['artifacts'], 1):
            name = artifact['name']
            size_mb = artifact['size_in_bytes'] / (1024 * 1024)
            expired = artifact['expired']
            artifact_id = artifact['id']
            
            print(f"{i}. {name}")
            print(f"   Size: {size_mb:.2f} MB")
            print(f"   Expired: {expired}")
            print(f"   ID: {artifact_id}")
            
            if not expired and token:
                # Try to get download URL
                download_url = artifact['archive_download_url']
                print(f"   Download URL: {download_url}")
                
                # Attempt download (requires valid token)
                print(f"   Attempting download...")
                dl_response = requests.get(download_url, headers=headers, stream=True)
                
                if dl_response.status_code == 200:
                    filename = f"{name}.zip"
                    with open(filename, 'wb') as f:
                        for chunk in dl_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"   ✅ Downloaded: {filename}")
                else:
                    print(f"   ⚠️ Download failed: {dl_response.status_code}")
                    print(f"   Try browser method instead")
            elif expired:
                print(f"   ⚠️ Artifact expired - cannot download")
            else:
                print(f"   ℹ️ No token provided - showing info only")
            
            print()
        
        return data['artifacts']
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("=" * 60)
    print("GitHub Actions Artifact Downloader")
    print("=" * 60)
    
    # Configuration
    REPO = "sumca1/ollama-downloader"
    
    # Find successful runs
    print(f"\n🔍 Searching for successful runs in {REPO}...\n")
    
    try:
        response = requests.get(f"https://api.github.com/repos/{REPO}/actions/runs?per_page=20")
        response.raise_for_status()
        runs = response.json()
        
        successful_runs = [r for r in runs['workflow_runs'] if r['conclusion'] == 'success']
        
        if not successful_runs:
            print("❌ No successful runs found")
            return
        
        print(f"✅ Found {len(successful_runs)} successful run(s):\n")
        
        for i, run in enumerate(successful_runs[:5], 1):
            print(f"{i}. Run #{run['run_number']} - {run['name']}")
            print(f"   ID: {run['id']}")
            print(f"   Date: {run['created_at']}")
            print(f"   URL: {run['html_url']}")
            print()
        
        # Check first successful run for artifacts
        first_run = successful_runs[0]
        print(f"\n📊 Checking artifacts in Run #{first_run['run_number']}...\n")
        
        # Try API method (without token - just show info)
        artifacts = download_artifact_api(REPO, first_run['id'], token=None)
        
        # Show alternative methods
        print("\n" + "=" * 60)
        print("DOWNLOAD METHODS:")
        print("=" * 60)
        print("\n1️⃣ Manual Browser Download (Recommended):")
        print(f"   Go to: {first_run['html_url']}")
        print(f"   Scroll down to 'Artifacts' section")
        print(f"   Click on artifact name to download\n")
        
        print("2️⃣ API with Token:")
        print(f"   Create GitHub token at: https://github.com/settings/tokens")
        print(f"   Run: python download_artifact.py --token YOUR_TOKEN\n")
        
        print("3️⃣ GitHub CLI:")
        print(f"   Install: winget install GitHub.cli")
        print(f"   Run: gh run download {first_run['id']} --repo {REPO}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if "--token" in sys.argv:
        token_idx = sys.argv.index("--token")
        if token_idx + 1 < len(sys.argv):
            token = sys.argv[token_idx + 1]
            print("🔑 Using provided token")
            # Re-run with token
            download_artifact_api("sumca1/ollama-downloader", None, token)
    else:
        main()
