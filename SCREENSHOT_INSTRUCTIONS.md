# Screenshot Instructions for CI/CD Submission

This document provides step-by-step instructions for capturing all required screenshots for the CI/CD assignment submission.

## Prerequisites
- CI and CD workflows are already set up in your repository
- You have write access to the repository
- DockerHub secrets are configured

---

## Part A: CI Workflow Screenshots

### Screenshot 1: Successful CI Run

**Steps:**
1. Make a small change to your code (e.g., add a comment in `app.py`)
2. Commit and push to the `dev` branch:
   ```bash
   git add .
   git commit -m "Test CI workflow"
   git push origin dev
   ```
3. Go to GitHub → Your Repository → Actions tab
4. Click on the latest "CI" workflow run
5. Wait for all steps to complete successfully (green checkmarks)
6. Take a screenshot showing:
   - Workflow name "CI"
   - Green checkmarks for all jobs
   - "Test" job expanded showing all steps passed
   - Timestamp and commit message

**Save as:** `screenshots/ci-success.png`

---

### Screenshot 2: Failed CI Run

**Steps:**
1. Intentionally break a test by editing `tests/test_app.py`:
   ```python
   # Find any assertion like:
   assert resp.status_code == 200
   
   # Change it to:
   assert resp.status_code == 404  # This will fail
   ```

2. Commit and push:
   ```bash
   git add tests/test_app.py
   git commit -m "Intentionally break test for CI demo"
   git push origin dev
   ```

3. Go to GitHub → Actions tab
4. Wait for the workflow to fail (red X)
5. Click on the failed workflow run
6. Expand the "Run tests" step to show the failure
7. Take a screenshot showing:
   - Red X indicating failure
   - Failed step highlighted in red
   - Error message visible
   - The test that failed

**Save as:** `screenshots/ci-failure.png`

8. **Important:** Fix the test immediately:
   ```python
   # Change it back to:
   assert resp.status_code == 200
   ```

9. Commit and push the fix:
   ```bash
   git add tests/test_app.py
   git commit -m "Fix test"
   git push origin dev
   ```

---

## Part B: CD Workflow Screenshots

### Screenshot 3: Successful CD Run

**Prerequisites:** Ensure CI is passing before creating a release.

**Steps:**
1. Go to your GitHub repository
2. Click on "Releases" (right sidebar)
3. Click "Draft a new release"
4. Fill in the release form:
   - **Tag:** `v0.2.0` (choose "Create new tag on publish")
   - **Release title:** `Version 0.2.0 - CI/CD Implementation`
   - **Description:**
     ```
     ## New Features
     - Implemented GitHub Actions CI/CD pipeline
     - Automated testing with pytest
     - Automated linting with flake8
     - Automated Docker image building and publishing
     
     ## Technical Details
     - 16 comprehensive tests
     - 51% code coverage
     - Docker image pushed to DockerHub
     ```
5. Click "Publish release"
6. Immediately go to Actions tab
7. Click on the "CD" workflow that just started
8. Wait for all steps to complete (green checkmarks)
9. Take a screenshot showing:
   - Workflow name "CD"
   - All steps completed successfully
   - "Build and push" step expanded showing image tags
   - Release tag (v0.2.0) visible

**Save as:** `screenshots/cd-success.png`

---

### Screenshot 4: DockerHub Image Registry

**Steps:**
1. Go to https://hub.docker.com
2. Sign in to your account
3. Navigate to your repository (e.g., `saashoor129/flask-todo-app`)
4. Click on the "Tags" tab
5. Take a screenshot showing:
   - Repository name clearly visible
   - At least two tags: `0.2.0` and `latest`
   - Image size
   - Last pushed timestamp
   - Architecture (linux/amd64)

**Save as:** `screenshots/dockerhub-image.png`

---

## Part C: End-to-End Flow Screenshots

### Screenshot 5: GitHub Release Page

**Steps:**
1. Create a third release (v0.3.0):
   - Go to Releases → Draft a new release
   - Tag: `v0.3.0`
   - Title: `Version 0.3.0 - End-to-End Demo`
   - Description:
     ```
     ## End-to-End CI/CD Flow Demonstration
     
     This release demonstrates the complete pipeline:
     1. Code change pushed to dev
     2. CI workflow validates code quality
     3. PR merged to main
     4. Release created
     5. CD workflow builds and publishes Docker image
     
     ## Changes
     - Added health check endpoint at /health
     - Updated documentation
     ```
   - Click "Publish release"

2. On the Releases page, take a screenshot showing:
   - Release v0.3.0 at the top
   - Release notes visible
   - Tag name visible
   - Published date and author

**Save as:** `screenshots/release-v0.3.0.png`

---

### Screenshot 6: DockerHub with New Tag

**Steps:**
1. Wait for CD workflow to complete for v0.3.0
2. Go to DockerHub → Your Repository → Tags
3. Refresh the page to see the new tag
4. Take a screenshot showing:
   - Multiple tags including `0.2.0`, `0.3.0`, and `latest`
   - `latest` pointing to the most recent push
   - Timestamp showing recent push

**Save as:** `screenshots/dockerhub-v0.3.0.png`

---

### Screenshot 7: Complete Actions History (Bonus)

**Steps:**
1. Go to GitHub → Actions tab
2. Take a screenshot showing:
   - Multiple CI workflow runs (some on push, some on PR)
   - Multiple CD workflow runs (triggered by releases)
   - Mix of successful (green) runs
   - The intentional failure (red) followed by fix (green)

**Save as:** `screenshots/actions-history.png`

---

## Screenshot Organization

Create a `screenshots` folder in your repository:

```
flask-todo-app/
├── screenshots/
│   ├── ci-success.png
│   ├── ci-failure.png
│   ├── cd-success.png
│   ├── dockerhub-image.png
│   ├── release-v0.3.0.png
│   ├── dockerhub-v0.3.0.png
│   └── actions-history.png (bonus)
├── CICD_SUBMISSION.md
└── ... (other files)
```

---

## Tips for Good Screenshots

1. **Use Full Screen:** Maximize your browser for clarity
2. **Zoom Appropriately:** 100% or 110% zoom works best
3. **Include Context:** Show navigation/breadcrumbs so reviewers know where you are
4. **Highlight Important Parts:** Use built-in tools or annotations if needed
5. **Clear Text:** Ensure all text is readable
6. **No Sensitive Data:** Don't show secret values or tokens
7. **Timestamps:** Include timestamps to prove recency

---

## Screenshot Tools

### Windows
- Snipping Tool (Win + Shift + S)
- Built-in screenshot (Win + PrtScn)

### macOS
- Screenshot utility (Cmd + Shift + 4)
- Full screen (Cmd + Shift + 3)

### Linux
- GNOME Screenshot (PrtScn)
- Flameshot (recommended)
- Spectacle (KDE)

### Browser Extensions
- Awesome Screenshot
- Lightshot
- Nimbus Screenshot

---

## Verification Checklist

Before submitting, verify you have:

- [ ] ci-success.png - Shows all CI steps passing
- [ ] ci-failure.png - Shows intentional test failure
- [ ] cd-success.png - Shows Docker build and push success
- [ ] dockerhub-image.png - Shows image with version tags
- [ ] release-v0.3.0.png - Shows release page with notes
- [ ] dockerhub-v0.3.0.png - Shows new version tag in registry
- [ ] All screenshots are clear and readable
- [ ] All screenshots have timestamps visible
- [ ] No sensitive information (tokens, passwords) visible

---

## Embedding Screenshots in Submission

In your `CICD_SUBMISSION.md`, embed screenshots using:

```markdown
![Description](screenshots/filename.png)
```

Or create a separate PDF with embedded images.

---

## Common Issues

### "Actions tab is empty"
- Ensure workflows are in `.github/workflows/` directory
- Check workflow YAML has correct syntax
- Push workflows to GitHub (they won't run locally)

### "CD workflow doesn't appear"
- You must **publish a release**, not just create a tag
- Check workflow trigger: `on: release: types: [published]`

### "Docker image not in DockerHub"
- Verify secrets are set correctly
- Check CD workflow logs for errors
- Ensure DockerHub token has write permissions

### "Can't see test output"
- Expand the "Run tests" step in the workflow
- Look for pytest output with test names and results
- Check for coverage report at the end

---

**Good luck with your submission!**
