# GitHub Actions CI/CD Quick Reference

## Overview
This repository uses GitHub Actions for automated CI/CD pipelines.

## Workflows

### 🔍 CI Workflow (Continuous Integration)
- **File:** `.github/workflows/ci.yml`
- **Triggers:** Push and PR to `main` and `dev` branches
- **Steps:**
  1. Checkout code
  2. Set up Python 3.11
  3. Install dependencies
  4. Run flake8 linting
  5. Run pytest with coverage

### 🚀 CD Workflow (Continuous Delivery)
- **File:** `.github/workflows/cd.yml`
- **Triggers:** GitHub Release publication
- **Steps:**
  1. Checkout code
  2. Set up Docker Buildx
  3. Login to DockerHub
  4. Extract version from release tag
  5. Build and push Docker image

## Required Secrets

Add these secrets in **Settings → Secrets and variables → Actions:**

- `DOCKERHUB_USERNAME` - Your DockerHub username
- `DOCKERHUB_TOKEN` - DockerHub access token (create at hub.docker.com/settings/security)

## Usage

### Running Tests Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=app

# Run linting
flake8 . --count --max-line-length=120 --statistics
```

### Creating a Release
1. Ensure all tests pass on `main` branch
2. Go to GitHub → Releases → Draft a new release
3. Create tag (e.g., `v0.3.0`)
4. Add release notes
5. Click "Publish release"
6. CD workflow will automatically build and push Docker image

### Pulling the Docker Image
```bash
# Pull latest
docker pull saashoor129/flask-todo-app:latest

# Pull specific version
docker pull saashoor129/flask-todo-app:0.3.0

# Run container
docker run -p 5000:5000 saashoor129/flask-todo-app:latest
```

## Workflow Status Badges

Add these to your README.md:

```markdown
![CI](https://github.com/SAshoor129/flask-todo-app/workflows/CI/badge.svg)
![CD](https://github.com/SAshoor129/flask-todo-app/workflows/CD/badge.svg)
```

## Troubleshooting

### CI Fails on Lint
- Run `flake8 . --count --max-line-length=120` locally
- Fix reported issues
- Commit and push

### CI Fails on Tests
- Run `pytest tests/ -v` locally
- Check test output for failures
- Fix issues and re-test

### CD Doesn't Trigger
- Ensure you published a **Release**, not just created a tag
- Release must be published, not saved as draft

### Docker Login Fails
- Verify secrets are set correctly
- Token must have read/write permissions
- Use access token, not password

## Best Practices

1. **Always** run tests locally before pushing
2. **Never** commit secrets or credentials
3. **Always** create PRs from `dev` to `main`
4. **Tag releases** with semantic versioning (v1.2.3)
5. **Write meaningful** release notes
