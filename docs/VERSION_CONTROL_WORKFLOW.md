# Version Control Workflow — MLOps Iris Classifier

## 1. Overview

This document describes the Git-based version control workflow used for this Machine Learning project, developed as part of the MLOps Lab.

- **Repository:** https://github.com/lokeshnarayanpatil28-rgb/mlops-iris-classifier
- **Primary language:** Python
- **Maintainer:** Lokesh Patil

## 2. Branching Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, production-ready code |
| `develop` | Integration branch for day-to-day development |
| `feature/<name>` | Individual features, branched from and merged back into `develop` |
| `conflict-demo-*` | Demonstration branches created for merge conflict resolution practice |

**Rule:** Changes are developed in feature branches and merged into `develop` through Pull Requests. The `main` branch is kept stable.

Example workflow:

`feature/*` → Pull Request → `develop` → `main`

## 3. Commit Convention

Commits use a short, imperative style with a type prefix.

- `feat:` — add new functionality
- `fix:` — correct a bug
- `docs:` — documentation changes
- `chore:` — tooling or configuration changes
- `refactor:` — code changes without changing behavior

Example:

`feat: add classification report to training script`

## 4. Standard Workflow (Feature Development)

```bash
git switch develop
git pull origin develop
git switch -c feature/<short-description>

# Make changes

git add <files>
git commit -m "feat: <description>"
git push -u origin feature/<short-description>

# Open a Pull Request into develop on GitHub
# After review/approval, merge through GitHub

git switch develop
git pull --rebase origin develop