# Contributing to Music Analytics Data Modeling

Thank you for contributing! This document outlines our development workflow and guidelines.

---

## 🌳 Branch Strategy

We use a **feature branch workflow**:

```
main (protected)
  │
  ├── feature/eda-analysis
  ├── feature/new-dashboard
  ├── fix/database-connection
  └── docs/update-readme
```

### Branch Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Feature | `feature/<description>` | `feature/user-analytics` |
| Bug Fix | `fix/<description>` | `fix/null-pointer-error` |
| Documentation | `docs/<description>` | `docs/api-reference` |
| Refactor | `refactor/<description>` | `refactor/etl-pipeline` |
| Test | `test/<description>` | `test/add-integration-tests` |

---

## 🔄 Pull Request Workflow

### 1. Create a Feature Branch

```bash
# Always start from latest main
git checkout main
git pull origin main

# Create your feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, documented code
- Follow existing code style
- Add/update tests for new functionality
- Update documentation if needed

### 3. Commit Your Changes

Use **conventional commit messages**:

```bash
# Format: <type>: <description>

git commit -m "feat: add user engagement metrics"
git commit -m "fix: resolve database connection timeout"
git commit -m "docs: update installation instructions"
git commit -m "test: add tests for transform module"
git commit -m "refactor: simplify ETL pipeline logic"
```

### 4. Push and Create PR

```bash
# Push your branch
git push origin feature/your-feature-name

# Then create a PR on GitHub
```

### 5. PR Review Process

1. **Author** creates PR with description
2. **Reviewer** reviews code and leaves comments
3. **Author** addresses feedback
4. **Reviewer** approves
5. **Author/Maintainer** merges to main

---

## ✅ PR Checklist

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass (`python -m pytest tests/ -v`)
- [ ] New code has appropriate test coverage
- [ ] Documentation is updated if needed
- [ ] Commit messages follow conventional format
- [ ] Branch is up to date with main

---

## 🧪 Testing Requirements

All PRs must pass tests before merging:

```bash
# Set Python path and run all tests
$env:PYTHONPATH = "."
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

### Test Coverage

- **Unit tests** for all new functions
- **Integration tests** for database operations
- **Data quality tests** for ETL pipeline

---

## 🏃 Running the Project Locally

```bash
# 1. Start database
docker compose up -d

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database and generate data
python setup_database_and_data.py

# 4. Run ETL pipeline
$env:PYTHONPATH = "src"
python src/etl_pipeline.py

# 5. Run EDA analysis
python src/eda_analysis.py

# 6. Run tests
python -m pytest tests/ -v
```

---

## 👥 Code Review Guidelines

### For Reviewers

- Be constructive and respectful
- Focus on logic, readability, and maintainability
- Verify tests are adequate
- Check for security concerns (no hardcoded secrets)

### For Authors

- Keep PRs focused and small when possible
- Respond to all comments
- Request re-review after making changes

---

## 🚫 What NOT to Commit

These are excluded via `.gitignore`:

- `.env` files (contain credentials)
- `data/song_data/` and `data/log_data/` (generated data)
- `.venv/` (virtual environment)
- `__pycache__/` (Python bytecode)

---

## 📞 Getting Help

- Create an issue for bugs or feature requests
- Tag maintainers for urgent items
- Check existing issues before creating new ones

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.
