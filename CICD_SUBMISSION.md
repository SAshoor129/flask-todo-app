# GitHub Actions CI/CD Pipeline - Assignment Submission

**Student:** SAshoor129  
**Repository:** flask-todo-app  
**Date:** March 5, 2026

---

## Executive Summary

This submission documents the implementation of a complete CI/CD pipeline for the Flask ToDo application using GitHub Actions. The pipeline automates testing, linting, Docker image building, and deployment to DockerHub, replacing manual processes with automated workflows triggered by code pushes, pull requests, and releases.

---

## Part A — CI Workflow (Continuous Integration)

### Overview
The CI workflow automatically runs lint checks and tests on every push and pull request to the `main` and `dev` branches, ensuring code quality before merging.

### CI Workflow Configuration

**File:** `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8

      - name: Lint
        run: flake8 . --count --max-line-length=120 --statistics

      - name: Run tests
        run: pytest tests/ -v --cov=app
```

### Workflow Components

1. **Triggers:** 
   - Push events to `main` and `dev` branches
   - Pull requests targeting `main` and `dev` branches

2. **Steps:**
   - **Checkout:** Uses `actions/checkout@v4` to clone the repository
   - **Python Setup:** Configures Python 3.11 environment using `actions/setup-python@v5`
   - **Dependencies:** Installs application dependencies and testing tools (pytest, pytest-cov, flake8)
   - **Lint:** Runs flake8 with max line length of 120 characters
   - **Tests:** Executes pytest with verbose output and coverage reporting

### Test Suite

**File:** `tests/test_app.py`

The test suite includes 16 comprehensive tests covering:
- **Create operations:** Simple tasks, tasks with details, multiple tasks
- **Read operations:** Empty task list, task detail view
- **Update operations:** Task name, priority, and status updates
- **Delete operations:** Single task deletion, database integrity, multiple deletions
- **Task completion:** Complete task functionality, status route updates
- **Edge cases:** Empty names, nonexistent tasks

All tests use pytest fixtures for clean database setup and teardown.

### Deliverable A - Screenshots

#### 1. Successful CI Run
![Successful CI Run](screenshots/ci-success.png)
*Screenshot showing green checkmarks for all CI steps including lint and test execution*

**Status:** All 16 tests passed with 51% code coverage

#### 2. Failed CI Run (Test Failure)
![Failed CI Run](screenshots/ci-failure.png)
*Screenshot showing intentional test failure introduced to demonstrate CI catching issues*

**Change Made:** Modified a test assertion to intentionally fail
**Result:** CI workflow correctly failed and prevented merge
**Resolution:** Fixed the test and re-ran workflow successfully

---

## Part B — CD Workflow (Continuous Delivery)

### Overview
The CD workflow automates Docker image building and publishing to DockerHub whenever a new GitHub Release is published, ensuring consistent deployment artifacts.

### CD Workflow Configuration

**File:** `.github/workflows/cd.yml`

```yaml
name: CD

on:
  release:
    types: [published]

jobs:
  build-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/flask-todo-app:${{ steps.version.outputs.VERSION }}
            ${{ secrets.DOCKERHUB_USERNAME }}/flask-todo-app:latest
```

### Workflow Components

1. **Trigger:** 
   - Activated when a GitHub Release is published (not just tagged)

2. **Steps:**
   - **Checkout:** Retrieves the repository code
   - **Docker Buildx:** Sets up advanced Docker build capabilities
   - **DockerHub Login:** Authenticates using encrypted secrets
   - **Version Extraction:** Parses release tag (e.g., `v0.2.0` → `0.2.0`)
   - **Build & Push:** Builds Docker image and pushes with version tag and `latest` tag

### GitHub Secrets Configuration

The following secrets were added to the repository settings (Settings → Secrets and variables → Actions):

- `DOCKERHUB_USERNAME`: Your DockerHub username
- `DOCKERHUB_TOKEN`: DockerHub access token (not password) with read/write permissions

**Security Note:** Secrets are encrypted and never exposed in logs or workflow files.

### Deliverable B - Screenshots

#### 1. Successful CD Run
![Successful CD Run](screenshots/cd-success.png)
*Screenshot showing successful Docker build and push to DockerHub triggered by release v0.2.0*

**Workflow Steps:**
- ✓ Checkout code
- ✓ Set up Docker Buildx
- ✓ Log in to DockerHub
- ✓ Extract version (0.2.0)
- ✓ Build and push image

#### 2. DockerHub Image Registry
![DockerHub Registry](screenshots/dockerhub-image.png)
*Screenshot showing the new image tags in DockerHub repository*

**Tags Created:**
- `saashoor129/flask-todo-app:0.2.0` (version-specific)
- `saashoor129/flask-todo-app:latest` (always points to most recent)

---

## Part C — End-to-End Flow

### Workflow Description

I demonstrated the complete CI/CD pipeline by implementing a new feature through the full development lifecycle:

1. **Feature Development:** Created a new branch `feature/add-health-check` from `dev` and added a `/health` endpoint to the Flask application for container health monitoring.

2. **CI Validation:** Pushed changes to the `dev` branch, triggering the CI workflow. All lint checks and 16 tests passed successfully, confirming code quality.

3. **Pull Request:** Opened a PR from `dev` → `main`. The CI workflow ran automatically on the PR, providing validation before merge approval.

4. **Merge to Main:** After CI passed, merged the PR to `main`, triggering another CI run to ensure the main branch remains stable.

5. **Release Creation:** Created GitHub Release `v0.3.0` with release notes describing the health check endpoint addition. This triggered the CD workflow.

6. **Automated Deployment:** The CD workflow built a Docker image, tagged it as `0.3.0` and `latest`, and pushed both to DockerHub automatically.

7. **Verification:** Confirmed the new image tag `saashoor129/flask-todo-app:0.3.0` appeared in DockerHub registry and pulled it locally to verify functionality.

### Deliverable C - Screenshots

#### 1. GitHub Release Page
![GitHub Release v0.3.0](screenshots/release-v0.3.0.png)
*Screenshot showing Release v0.3.0 with release notes*

**Release Notes:**
```
New Features:
- Added /health endpoint for container health monitoring
- Improved Docker image tagging

Pipeline Updates:
- Full CI/CD automation verified end-to-end
```

#### 2. DockerHub Registry with New Tag
![DockerHub v0.3.0](screenshots/dockerhub-v0.3.0.png)
*Screenshot showing both v0.3.0 and latest tags in DockerHub*

**Image Details:**
- Repository: `saashoor129/flask-todo-app`
- Tags: `0.3.0`, `latest`
- Size: ~150 MB
- Architecture: linux/amd64

---

## Additional Implementation Details

### Project Structure
```
flask-todo-app/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Continuous Integration workflow
│       └── cd.yml          # Continuous Delivery workflow
├── app.py                  # Main Flask application
├── models.py               # Database models
├── requirements.txt        # Python dependencies (updated with test tools)
├── Dockerfile              # Container definition
├── tests/
│   ├── __init__.py         # Test package initialization
│   └── test_app.py         # Comprehensive test suite (16 tests)
└── templates/
    ├── index.html
    └── task_detail.html
```

### Updated Dependencies

**File:** `requirements.txt`

Added testing and linting tools:
```
pytest==7.0.0
pytest-cov==3.0.0
flake8==6.0.0
```

### Test Coverage Report

```
Name     Stmts   Miss  Cover
----------------------------
app.py     367    179    51%
----------------------------
TOTAL      367    179    51%
```

**Test Results:** 16/16 passed (100% pass rate)

---

## Key Learnings and Reflection

### What I Learned About GitHub Actions

1. **Workflow Automation Power:** GitHub Actions transforms manual, error-prone processes into reliable, repeatable workflows. The ability to automatically run tests on every push catches bugs before they reach production.

2. **Secret Management:** GitHub's encrypted secrets feature provides secure credential storage. Using access tokens instead of passwords follows security best practices and enables fine-grained permission control.

3. **Workflow Triggers:** Understanding different trigger types (`push`, `pull_request`, `release`) enables precise control over when automation runs, preventing unnecessary builds and optimizing CI/CD costs.

4. **Docker Integration:** The seamless integration between GitHub Actions and container registries (DockerHub/ECR) using official actions (`docker/login-action`, `docker/build-push-action`) significantly simplifies deployment pipelines.

5. **Version Extraction:** Learning shell parameter expansion (`${GITHUB_REF#refs/tags/v}`) for extracting semantic versions from git tags demonstrates how workflows can dynamically adapt to repository state.

### Benefits of Automation

- **Consistency:** Every build follows identical steps, eliminating "works on my machine" issues
- **Speed:** Parallel job execution and cached dependencies reduce feedback time
- **Quality Gates:** Automated testing prevents broken code from reaching production
- **Auditability:** Complete workflow history provides transparency and debugging capability
- **Scalability:** CI/CD scales effortlessly from solo projects to large teams

### Challenges Overcome

1. **Flake8 Configuration:** Initially encountered line length violations. Configured `--max-line-length=120` to match modern Python standards while maintaining readability.

2. **Docker Tag Versioning:** Learned to parse GitHub release tags correctly to create meaningful Docker image versions, enabling easy rollbacks and version tracking.

3. **Test Coverage:** Expanded test suite to achieve meaningful coverage (51%) across CRUD operations and edge cases, improving confidence in automated testing.

---

## Verification Checklist

- [x] CI workflow file (ci.yml) created and configured
- [x] CI triggers on push and PR to main and dev branches
- [x] Lint step using flake8 (max-line-length=120)
- [x] Test step using pytest with coverage reporting
- [x] 16 comprehensive tests covering CRUD and edge cases
- [x] Screenshot of successful CI run
- [x] Screenshot of failed CI run (intentional failure, then fixed)
- [x] CD workflow file (cd.yml) created and configured
- [x] CD triggers on GitHub Release publication
- [x] Docker Buildx setup for advanced builds
- [x] DockerHub authentication using secrets
- [x] Version extraction from release tags
- [x] Build and push with version tag and latest tag
- [x] Screenshot of successful CD run
- [x] Screenshot of DockerHub showing new image tags
- [x] GitHub Secrets configured (DOCKERHUB_USERNAME, DOCKERHUB_TOKEN)
- [x] End-to-end flow demonstration (dev → PR → merge → release → deployed)
- [x] Screenshot of GitHub Release page
- [x] Screenshot of DockerHub registry with version tag
- [x] Reflection paragraph on GitHub Actions learning

---

## Troubleshooting Notes

### Common Issues Resolved

1. **Module Import Errors in Tests**
   - **Problem:** Pytest couldn't find app modules
   - **Solution:** Created `tests/__init__.py` to make tests a proper package

2. **Flake8 Not Installed**
   - **Problem:** CI failed on lint step
   - **Solution:** Added `flake8==6.0.0` to requirements.txt

3. **Docker Login Failures**
   - **Problem:** Authentication failed with password
   - **Solution:** Created DockerHub access token with read/write permissions

4. **CD Workflow Not Triggering**
   - **Problem:** Creating tags didn't trigger workflow
   - **Solution:** Must create a GitHub Release (not just a git tag)

---

## Conclusion

The CI/CD pipeline successfully automates the complete software delivery lifecycle for the Flask ToDo application. The implementation demonstrates industry-standard practices including automated testing, code quality enforcement, containerization, and deployment automation. This foundation scales to support team collaboration, continuous delivery, and production deployments.

**Next Steps:**
- Integrate additional quality gates (security scanning, dependency checks)
- Add deployment environments (staging, production)
- Implement automated rollback on deployment failures
- Configure branch protection rules requiring CI passage

---

## Appendix: Workflow Files

### A.1 Complete CI Workflow
See `.github/workflows/ci.yml` in repository

### A.2 Complete CD Workflow
See `.github/workflows/cd.yml` in repository

### A.3 Test Suite
See `tests/test_app.py` in repository (16 tests, 100% pass rate)

---

**Submission Date:** March 5, 2026  
**Repository:** https://github.com/SAshoor129/flask-todo-app  
**DockerHub:** https://hub.docker.com/r/saashoor129/flask-todo-app
