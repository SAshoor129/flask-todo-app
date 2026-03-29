# Flask ToDo App

## Overview
This is a Flask-based ToDo application with full CRUD functionality, containerized with Docker, and equipped with automated CI/CD pipelines using GitHub Actions. The project follows a professional Git branching workflow and includes automated tests.

---

## Table of Contents
- [Features](#features)
- [Branching Workflow](#branching-workflow)
- [Running the App Locally](#running-the-app-locally)
- [Running with Docker](#running-with-docker)
- [Testing](#testing)
- [CI/CD Pipelines](#cicd-pipelines)
- [Versioning & Releases](#versioning--releases)

---

## Features
- Create, Read, Update, Delete (CRUD) tasks
- Task priorities and statuses
- Tagging support
- Responsive web UI

---

## Branching Workflow
This project uses a professional GitHub workflow:

1. **main**: Production-ready code only
2. **dev**: Integration branch for features
3. **feature branches**: One per feature (e.g., `feature/add-tags`)

**Typical flow:**
- Create `dev` from `main` (once)
- Create feature branches from `dev`
- Implement features, open Pull Requests (PRs) into `dev`
- Merge `dev` into `main` for releases

---

## Running the App Locally
1. **Clone the repo:**
	```bash
	git clone <repo-url>
	cd flask-todo-app
	```
2. **Create a virtual environment (optional but recommended):**
	```bash
	python3 -m venv venv
	source venv/bin/activate
	```
3. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
4. **Initialize the database:**
	```bash
	python
	>>> from app import db
	>>> db.create_all()
	>>> exit()
	```
5. **Run the app:**
	```bash
	python app.py
	```
6. Visit [http://localhost:5000](http://localhost:5000)

---

## Running with Docker
1. **Build the image:**
	```bash
	docker build -t flask-todo-app:latest .
	```
2. **Run the container:**
	```bash
	docker run -p 5000:5000 flask-todo-app:latest
	```
3. Visit [http://localhost:5000](http://localhost:5000)

---

## Testing
Automated tests use `pytest` and Flask's test client.

**Run tests locally:**
```bash
pytest tests/
```

Tests cover:
- Task creation
- Task update
- Task deletion
- Task listing/verification

---

## CI/CD Pipelines
GitHub Actions automate testing, linting, building, and deployment:

### CI Workflow
- Runs on push/PR to `main` and `dev`
- Installs dependencies, runs lint (`flake8`), and tests (`pytest`)

### CD Workflow
- Triggers on GitHub Release publish
- Builds and pushes Docker image to DockerHub
- Tags image with release version (e.g., `0.1.0`)
- Uses GitHub Secrets for DockerHub credentials

---

## Versioning & Releases
- Follows [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH)
- Each release is tagged in GitHub (e.g., `v1.0.0`)
- Docker images are tagged with the release version and `latest`

---

## Quality Gates
- CI must pass for PRs to be merged
- Branch protection rules recommended for `main` and `dev`

---

## Evidence Pack
- See `.github/workflows/` for CI/CD YAMLs
- See `tests/` for automated test cases
- See GitHub Releases and DockerHub for published images

---

## Contact
For questions, open an issue or contact the maintainer.
