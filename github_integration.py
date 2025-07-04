#!/usr/bin/env python3
"""
GitHub Integration for NeuroScribe PDF Copilot
Handles CI/CD, repository operations, and GitHub Actions integration.
"""

import os
import requests
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GitHubIntegration:
    """GitHub API integration for NeuroScribe PDF Copilot."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub integration with token."""
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token not found. Set GITHUB_TOKEN in .env file.")
        
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"
    
    def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository information."""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def create_issue(self, owner: str, repo: str, title: str, body: str, labels: list = None) -> Dict[str, Any]:
        """Create a new issue in the repository."""
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        data = {
            "title": title,
            "body": body
        }
        if labels:
            data["labels"] = labels
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_workflow_runs(self, owner: str, repo: str, workflow_id: str = None) -> Dict[str, Any]:
        """Get workflow runs for the repository."""
        if workflow_id:
            url = f"{self.base_url}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"
        else:
            url = f"{self.base_url}/repos/{owner}/{repo}/actions/runs"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def trigger_workflow(self, owner: str, repo: str, workflow_id: str, ref: str = "main") -> Dict[str, Any]:
        """Trigger a workflow dispatch."""
        url = f"{self.base_url}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
        data = {
            "ref": ref
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def upload_release_asset(self, owner: str, repo: str, release_id: int, file_path: str) -> Dict[str, Any]:
        """Upload an asset to a release."""
        url = f"{self.base_url}/repos/{owner}/{repo}/releases/{release_id}/assets"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, headers=self.headers, files=files)
            response.raise_for_status()
            return response.json()

def setup_github_actions_workflow():
    """Create GitHub Actions workflow for NeuroScribe."""
    workflow_content = {
        "name": "NeuroScribe CI/CD",
        "on": {
            "push": {"branches": ["main"]},
            "pull_request": {"branches": ["main"]}
        },
        "jobs": {
            "test": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"uses": "actions/checkout@v3"},
                    {"uses": "actions/setup-python@v4", "with": {"python-version": "3.10"}},
                    {"run": "pip install -r requirements.txt"},
                    {"run": "python verify_installations.py"},
                    {"run": "python -m pytest tests/"}
                ]
            },
            "build": {
                "runs-on": "ubuntu-latest",
                "needs": "test",
                "steps": [
                    {"uses": "actions/checkout@v3"},
                    {"uses": "actions/setup-python@v4", "with": {"python-version": "3.10"}},
                    {"run": "pip install -r requirements.txt"},
                    {"run": "python build_exe.py"},
                    {"uses": "actions/upload-artifact@v3", "with": {"name": "neuroscribe-build", "path": "dist/"}}
                ]
            }
        }
    }
    
    return workflow_content

def main():
    """Main function for GitHub integration testing."""
    try:
        # Test GitHub integration
        github = GitHubIntegration()
        print("✅ GitHub integration initialized successfully")
        
        # Example: Get repository info (replace with your repo)
        # repo_info = github.get_repo_info("your-username", "neuroscribe-pdf-copilot")
        # print(f"Repository: {repo_info['name']}")
        
        print("🔧 GitHub integration ready for use!")
        print("📝 Available methods:")
        print("  - get_repo_info(owner, repo)")
        print("  - create_issue(owner, repo, title, body)")
        print("  - get_workflow_runs(owner, repo)")
        print("  - trigger_workflow(owner, repo, workflow_id)")
        print("  - upload_release_asset(owner, repo, release_id, file_path)")
        
    except ValueError as e:
        print(f"❌ {e}")
        print("💡 To fix this:")
        print("1. Copy env.template to .env")
        print("2. Add your GitHub token to .env")
        print("3. Run this script again")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 