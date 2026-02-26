import os
import subprocess
import json
import time
import sys

def run_git(args, cwd):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)

def deploy():
    print("--- Global Printer Savior: Deployment Engine ---")
    
    if len(sys.argv) < 3:
        print("\nUsage: python deploy_global.py <GitHub_Username> <GitHub_Token>")
        return

    username = sys.argv[1]
    token = sys.argv[2]
    
    repo_name = "universal-printer-savior"
    cwd = "C:/Users/Anurag/.gemini/antigravity/scratch/universal_resetter"
    
    # 1. Create Repo via API
    print(f"\nCreating repository '{repo_name}' on GitHub...")
    import urllib.request
    
    api_url = "https://api.github.com/user/repos"
    data = json.dumps({"name": repo_name, "private": False, "description": "One-click reset for Epson EcoTank printers."}).encode('utf-8')
    
    req = urllib.request.Request(api_url, data=data)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            html_url = res_data['clone_url']
            print(f"Success! Repository created: {html_url}")
    except Exception as e:
        print(f"Checking if repo already exists... ({e})")
        html_url = f"https://github.com/{username}/{repo_name}.git"

    # 2. Add Remote and Push
    print("\nPreparing to push files...")
    auth_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    
    run_git(["remote", "remove", "origin"], cwd)
    run_git(["remote", "add", "origin", auth_url], cwd)
    
    print("Pushing to GitHub (master)...")
    push_res = run_git(["push", "-u", "origin", "master", "--force"], cwd)
    
    if push_res.returncode == 0:
        print("\nDEPLOYMENT SUCCESSFUL!")
        print(f"Your code is now at: https://github.com/{username}/{repo_name}")
    else:
        print(f"\nPush failed: {push_res.stderr}")

if __name__ == "__main__":
    deploy()
