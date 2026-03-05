#!/bin/bash

# CI/CD Pipeline Validation Script
# This script checks if your CI/CD setup is ready for submission

set -e

echo "========================================="
echo "  CI/CD Pipeline Validation Script"
echo "========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 NOT FOUND"
        ((ERRORS++))
        return 1
    fi
}

# Function to check if directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 directory exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 directory NOT FOUND"
        ((ERRORS++))
        return 1
    fi
}

echo "1. Checking Required Files..."
echo "-------------------------------------------"
check_file ".github/workflows/ci.yml"
check_file ".github/workflows/cd.yml"
check_file "requirements.txt"
check_file "Dockerfile"
check_file "app.py"
check_file "tests/test_app.py"
check_file "tests/__init__.py"
check_file ".flake8"
echo ""

echo "2. Checking Workflow Content..."
echo "-------------------------------------------"

# Check CI workflow triggers
if grep -q "push:" .github/workflows/ci.yml && grep -q "pull_request:" .github/workflows/ci.yml; then
    echo -e "${GREEN}✓${NC} CI workflow has correct triggers"
else
    echo -e "${RED}✗${NC} CI workflow missing push or pull_request triggers"
    ((ERRORS++))
fi

# Check CI branches
if grep -q "branches: \[main, dev\]" .github/workflows/ci.yml; then
    echo -e "${GREEN}✓${NC} CI workflow monitors main and dev branches"
else
    echo -e "${YELLOW}⚠${NC} CI workflow may not monitor correct branches"
    ((WARNINGS++))
fi

# Check CD workflow trigger
if grep -q "release:" .github/workflows/cd.yml && grep -q "types: \[published\]" .github/workflows/cd.yml; then
    echo -e "${GREEN}✓${NC} CD workflow has correct release trigger"
else
    echo -e "${RED}✗${NC} CD workflow missing release trigger"
    ((ERRORS++))
fi

# Check for secrets usage
if grep -q "secrets.DOCKERHUB_USERNAME" .github/workflows/cd.yml && grep -q "secrets.DOCKERHUB_TOKEN" .github/workflows/cd.yml; then
    echo -e "${GREEN}✓${NC} CD workflow uses DockerHub secrets"
else
    echo -e "${RED}✗${NC} CD workflow not using DockerHub secrets properly"
    ((ERRORS++))
fi

echo ""

echo "3. Checking Dependencies..."
echo "-------------------------------------------"

# Check if pytest is in requirements
if grep -q "pytest" requirements.txt; then
    echo -e "${GREEN}✓${NC} pytest in requirements.txt"
else
    echo -e "${RED}✗${NC} pytest NOT in requirements.txt"
    ((ERRORS++))
fi

# Check if flake8 is in requirements
if grep -q "flake8" requirements.txt; then
    echo -e "${GREEN}✓${NC} flake8 in requirements.txt"
else
    echo -e "${RED}✗${NC} flake8 NOT in requirements.txt"
    ((ERRORS++))
fi

# Check if pytest-cov is in requirements
if grep -q "pytest-cov" requirements.txt; then
    echo -e "${GREEN}✓${NC} pytest-cov in requirements.txt"
else
    echo -e "${RED}✗${NC} pytest-cov NOT in requirements.txt"
    ((ERRORS++))
fi

echo ""

echo "4. Testing Lint (flake8)..."
echo "-------------------------------------------"

if command -v flake8 &> /dev/null; then
    if flake8 . --count --max-line-length=120 --statistics --exclude=.venv,__pycache__,.git,instance 2>&1 | tail -5; then
        echo -e "${GREEN}✓${NC} Linting passed"
    else
        echo -e "${YELLOW}⚠${NC} Linting has warnings/errors - fix before pushing"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠${NC} flake8 not installed - run: pip install flake8"
    ((WARNINGS++))
fi

echo ""

echo "5. Running Tests..."
echo "-------------------------------------------"

if command -v pytest &> /dev/null; then
    if pytest tests/ -v --tb=short 2>&1 | tail -20; then
        echo -e "${GREEN}✓${NC} All tests passed"
    else
        echo -e "${RED}✗${NC} Some tests failed"
        ((ERRORS++))
    fi
else
    echo -e "${RED}✗${NC} pytest not installed - run: pip install pytest"
    ((ERRORS++))
fi

echo ""

echo "6. Checking Git Status..."
echo "-------------------------------------------"

# Check if on main or dev branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "Current branch: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "dev" ]; then
    echo -e "${GREEN}✓${NC} On main or dev branch"
else
    echo -e "${YELLOW}⚠${NC} Not on main or dev branch - workflows may not trigger"
    ((WARNINGS++))
fi

# Check for uncommitted changes
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${GREEN}✓${NC} No uncommitted changes"
else
    echo -e "${YELLOW}⚠${NC} You have uncommitted changes"
    ((WARNINGS++))
fi

echo ""

echo "7. Checking Documentation..."
echo "-------------------------------------------"

check_file "CICD_SUBMISSION.md"
check_file "CICD_GUIDE.md"
check_file "SCREENSHOT_INSTRUCTIONS.md"

echo ""

echo "8. GitHub Secrets Reminder..."
echo "-------------------------------------------"
echo -e "${YELLOW}ℹ${NC} Make sure these secrets are set in GitHub:"
echo "   - DOCKERHUB_USERNAME"
echo "   - DOCKERHUB_TOKEN"
echo ""
echo "   Check at: GitHub → Settings → Secrets and variables → Actions"

echo ""
echo "========================================="
echo "  Validation Summary"
echo "========================================="
echo -e "Errors:   ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Your CI/CD setup looks good!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Commit and push your changes"
    echo "2. Create a Pull Request"
    echo "3. Create a GitHub Release"
    echo "4. Take screenshots (see SCREENSHOT_INSTRUCTIONS.md)"
    echo "5. Submit CICD_SUBMISSION.md"
    exit 0
else
    echo -e "${RED}✗ Please fix the errors above before proceeding${NC}"
    exit 1
fi
