# 🚀 NeuroScribe CI/CD Complete Setup Guide

This guide provides step-by-step instructions for setting up a complete CI/CD pipeline for NeuroScribe PDF Copilot using GitHub Actions, Docker, and automated deployment.

## 📋 Prerequisites

- GitHub account
- Git installed locally
- Docker (optional, for containerized deployment)
- Python 3.8+ installed

## 🔐 Step 1: GitHub Token Setup

### 1.1 Create Personal Access Token
1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Configure with these permissions:
   - ✅ `repo` (Full control of repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `write:packages` (Upload packages)
   - ✅ `delete:packages` (Delete packages)
4. Copy the token immediately (you won't see it again!)

### 1.2 Configure Local Environment
```bash
# Copy environment template
copy env.template .env

# Edit .env file and add your tokens
notepad .env
```

Add to `.env`:
```env
GITHUB_TOKEN=ghp_your_actual_token_here
OPENAI_API_KEY=sk-your_openai_key_here
```

## 🏗️ Step 2: Repository Setup

### 2.1 Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: NeuroScribe PDF Copilot"
git branch -M main
```

### 2.2 Connect to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## 🔧 Step 3: GitHub Secrets Configuration

### 3.1 Add Repository Secrets
1. Go to your GitHub repository
2. Navigate to: Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add these secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `GITHUB_TOKEN` | Your GitHub token | For CI/CD operations |
| `OPENAI_API_KEY` | Your OpenAI key | For GPT features |

## 🔄 Step 4: CI/CD Pipeline Overview

The pipeline includes multiple jobs:

### ✅ **Test Job**
- Runs on Python 3.9, 3.10, 3.11
- Installs dependencies
- Runs verification script
- Executes unit tests (if available)

### 🏗️ **Build & Deploy Job**
- Builds executable using PyInstaller
- Tests Streamlit deployment
- Uploads build artifacts
- Only runs on main branch pushes

### 🔒 **Security Scan Job**
- Runs Bandit security analysis
- Checks dependencies with Safety
- Generates security reports

### 🐳 **Docker Build Job**
- Builds Docker image
- Tags with commit SHA and latest
- Uploads Docker artifacts

### 🚀 **Release Job**
- Downloads build artifacts
- Uploads to GitHub Release
- Creates downloadable executables

## 📁 Step 5: File Structure

Your project now includes:

```
NeuroScribe PDF Copilot Editor/
├── .github/
│   └── workflows/
│       ├── ci-cd.yml          # Main CI/CD pipeline
│       └── deploy.yml         # Deployment workflow
├── src/
│   ├── pdf_utils.py           # PDF processing
│   └── openai_utils.py        # GPT integration
├── app.py                     # Main Streamlit app
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Local deployment
├── requirements.txt           # Python dependencies
├── verify_installations.py    # Dependency checker
├── setup_cicd.bat            # CI/CD setup script
├── env.template              # Environment template
├── .gitignore               # Git exclusions
└── README.md                # Project documentation
```

## 🚀 Step 6: Triggering the Pipeline

### 6.1 Push to Main Branch
```bash
git add .
git commit -m "Update feature"
git push origin main
```

### 6.2 Create a Release
```bash
# Tag a release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Then create GitHub Release via web interface
```

### 6.3 Pull Request
- Create a PR to main branch
- Pipeline runs tests only
- No deployment until merged

## 📊 Step 7: Monitoring the Pipeline

### 7.1 View Workflow Runs
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Monitor workflow execution

### 7.2 Check Job Status
- ✅ **Green**: All tests passed
- ❌ **Red**: Tests failed (check logs)
- 🟡 **Yellow**: Tests running
- ⏸️ **Gray**: Job waiting

### 7.3 Download Artifacts
1. Click on a workflow run
2. Scroll to "Artifacts" section
3. Download build artifacts

## 🐳 Step 8: Docker Deployment

### 8.1 Local Docker Testing
```bash
# Build and run locally
docker build -t neuroscribe .
docker run -p 8501:8501 neuroscribe

# Or use Docker Compose
docker-compose up -d
```

### 8.2 Production Deployment
The CI/CD pipeline automatically:
- Builds Docker image
- Tags with commit SHA
- Uploads to container registry (if configured)

## 🔒 Step 9: Security Features

### 9.1 Automated Security Scanning
- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability checker
- **Reports**: JSON output for analysis

### 9.2 Secret Management
- Environment variables for sensitive data
- GitHub Secrets for CI/CD
- No secrets in source code

## 🛠️ Step 10: Troubleshooting

### Common Issues

#### 1. "GitHub token not found"
```bash
# Check if .env file exists
dir .env

# Verify token is set
findstr GITHUB_TOKEN .env
```

#### 2. "Workflow not triggering"
- Check if workflow file is in `.github/workflows/`
- Verify branch names match
- Ensure GitHub Actions are enabled

#### 3. "Build failing"
- Check Python version compatibility
- Verify all dependencies in `requirements.txt`
- Review build logs for specific errors

#### 4. "Docker build failing"
- Check if Dockerfile exists
- Verify Docker syntax
- Check for missing dependencies

### Getting Help
1. Check GitHub Actions logs
2. Verify environment setup
3. Test locally with `python verify_installations.py`
4. Review this documentation

## 📈 Step 11: Advanced Features

### 11.1 Custom Workflows
You can create additional workflows for:
- Staging deployments
- Performance testing
- Documentation generation
- Dependency updates

### 11.2 Environment-Specific Deployments
```yaml
# Example: Different environments
jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    # Staging deployment steps
    
  deploy-production:
    if: github.ref == 'refs/heads/main'
    # Production deployment steps
```

### 11.3 Automated Testing
Add more test types:
- Unit tests with pytest
- Integration tests
- End-to-end tests
- Performance benchmarks

## 🎉 Success Checklist

Once completed, you should have:

- ✅ Automated testing on every push
- ✅ Automated builds on main branch
- ✅ Automated releases with executables
- ✅ Security scanning
- ✅ Docker containerization
- ✅ GitHub integration
- ✅ Secret management
- ✅ Health checks
- ✅ Monitoring and logging

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud)
- [Python Security Best Practices](https://owasp.org/www-project-python-security-top-10/)

---

## 🚀 Your NeuroScribe CI/CD Pipeline is Ready!

Your project now has enterprise-grade CI/CD capabilities with:
- **Automated Testing**: Every push triggers comprehensive tests
- **Automated Building**: Executables built automatically
- **Automated Deployment**: Releases deployed with one click
- **Security Scanning**: Continuous security monitoring
- **Container Support**: Docker-ready for any deployment

**Next step**: Push your code to GitHub and watch the magic happen! 🎉 