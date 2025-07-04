# 🚀 NeuroScribe GitHub Integration & CI/CD Setup

This guide will help you set up GitHub integration, CI/CD pipelines, and automated deployments for NeuroScribe PDF Copilot.

## 📋 Prerequisites

- GitHub account
- NeuroScribe project repository on GitHub
- Python 3.8+ installed locally

## 🔐 Step 1: Create GitHub Personal Access Token

1. **Go to GitHub Settings**:
   - Visit: https://github.com/settings/tokens
   - Click "Generate new token (classic)"

2. **Configure Token Permissions**:
   - **Note**: `NeuroScribe CI/CD Token`
   - **Expiration**: Choose appropriate expiration (90 days recommended)
   - **Scopes**: Select the following:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
     - ✅ `write:packages` (Upload packages to GitHub Package Registry)
     - ✅ `delete:packages` (Delete packages from GitHub Package Registry)

3. **Generate Token**:
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately (you won't see it again!)

## 📁 Step 2: Configure Local Environment

### Option A: Automatic Setup (Recommended)
```bash
# Run the setup script
setup_github_token.bat
```

### Option B: Manual Setup
1. **Copy environment template**:
   ```bash
   copy env.template .env
   ```

2. **Edit .env file**:
   ```bash
   notepad .env
   ```

3. **Add your GitHub token**:
   ```env
   GITHUB_TOKEN=ghp_your_actual_token_here
   ```

## 🔧 Step 3: Test GitHub Integration

```bash
python github_integration.py
```

You should see: `✅ GitHub integration initialized successfully`

## 🚀 Step 4: Set Up GitHub Repository

### 4.1 Initialize Git Repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: NeuroScribe PDF Copilot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 4.2 Add GitHub Token as Repository Secret

1. **Go to your repository on GitHub**
2. **Navigate to**: Settings → Secrets and variables → Actions
3. **Click**: "New repository secret"
4. **Configure**:
   - **Name**: `GITHUB_TOKEN`
   - **Value**: Paste your GitHub token
5. **Click**: "Add secret"

## 🔄 Step 5: GitHub Actions CI/CD Pipeline

The CI/CD pipeline is already configured in `.github/workflows/ci-cd.yml` and will:

### ✅ **Test Job** (Runs on every push/PR)
- Tests on Python 3.9, 3.10, 3.11
- Runs verification script
- Executes unit tests (if available)
- Security scanning with Bandit and Safety

### 🏗️ **Build Job** (Runs on main branch push)
- Builds executable using PyInstaller
- Creates distributable packages
- Uploads build artifacts

### 🚀 **Deploy Job** (Runs on release)
- Downloads build artifacts
- Uploads to GitHub Release
- Creates downloadable executables

## 📦 Step 6: Create a Release

### 6.1 Tag a Release
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 6.2 Create GitHub Release
1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Select the tag you just created
4. Add release notes
5. Click "Publish release"

The CI/CD pipeline will automatically:
- Build the executable
- Upload it to the release
- Make it available for download

## 🔍 Step 7: Monitor CI/CD Pipeline

### View Workflow Runs
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Monitor the workflow runs

### Check Build Status
- ✅ Green: All tests passed
- ❌ Red: Tests failed (check logs)
- 🟡 Yellow: Tests running

## 🛠️ Available GitHub Integration Features

### Repository Operations
```python
from github_integration import GitHubIntegration

github = GitHubIntegration()

# Get repository info
repo_info = github.get_repo_info("username", "repo-name")

# Create issues
github.create_issue("username", "repo-name", "Bug Report", "Description")

# Get workflow runs
runs = github.get_workflow_runs("username", "repo-name")
```

### Automated Workflows
- **Push to main**: Triggers test and build
- **Pull Request**: Triggers test only
- **Release**: Triggers deployment

## 🔒 Security Best Practices

### ✅ Do's
- Use environment variables for tokens
- Set appropriate token expiration
- Use minimal required permissions
- Keep tokens out of source code
- Rotate tokens regularly

### ❌ Don'ts
- Never commit tokens to Git
- Don't share tokens publicly
- Don't use tokens with excessive permissions
- Don't store tokens in plain text files

## 🚨 Troubleshooting

### Common Issues

#### 1. "GitHub token not found"
```bash
# Check if .env file exists
dir .env

# Check if token is set
findstr GITHUB_TOKEN .env
```

#### 2. "Permission denied"
- Verify token has correct permissions
- Check if token is expired
- Ensure repository access is granted

#### 3. "Workflow not triggering"
- Check if workflow file is in correct location
- Verify branch names match
- Check GitHub Actions are enabled

#### 4. "Build failing"
- Check Python version compatibility
- Verify all dependencies are in requirements.txt
- Review build logs for specific errors

### Getting Help
1. Check GitHub Actions logs
2. Verify environment setup
3. Test locally with `python github_integration.py`
4. Review this documentation

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Personal Access Tokens Guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

---

## 🎉 Success!

Once you've completed these steps, your NeuroScribe PDF Copilot will have:

- ✅ Automated testing on every push
- ✅ Automated builds on main branch
- ✅ Automated releases with executables
- ✅ Security scanning
- ✅ GitHub integration for issues and workflows

Your project is now production-ready with full CI/CD capabilities! 🚀 