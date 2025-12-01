# Contributing to Dengue Risk Prediction Notebook

Thank you for your interest in improving this public health tool!

## Ways to Contribute

### 1. Report Bugs or Issues
- Found a problem? Open an [Issue](https://github.com/YOUR_USERNAME/dengue-risk-prediction/issues)
- Include:
  - Description of the bug
  - Steps to reproduce
  - Expected vs. actual behavior
  - Environment (Python version, OS, etc.)

### 2. Suggest Improvements
- New feature ideas? Scoring refinements? UI improvements?
- Open an issue with the tag `enhancement`
- Describe the use case and expected benefit

### 3. Update Dengue Case Data
- Help keep `dengue_cases.csv` current by submitting:
  - Latest cases from your region
  - New area data
  - Seasonal trends

**Steps:**
1. Fork the repo
2. Update `dengue_cases.csv` with new data (cite sources)
3. Commit with message: "Update dengue cases - [DATE] - [SOURCE]"
4. Submit Pull Request

### 4. Improve Documentation
- Spelling/clarity fixes
- Better examples
- Translate README to other languages
- Add regional case studies

### 5. Code Contributions
- Fix bugs
- Optimize algorithms
- Add tests
- Improve performance
- Integrate new data sources

## Getting Started

### Setup Development Environment

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/dengue-risk-prediction.git
cd dengue-risk-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest black flake8

# Run notebook
jupyter notebook
```

### Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-feature-name
   ```

2. **Make changes and test:**
   ```bash
   # Test the notebook runs without errors
   # Run code quality checks
   black *.py
   flake8 *.py
   ```

3. **Commit with clear message:**
   ```bash
   git commit -m "Add feature X - improves Y by Z%"
   ```

4. **Push and create Pull Request:**
   ```bash
   git push origin feature/my-feature-name
   ```

## Code Style

- **Python**: Follow PEP 8
  - Use `black` for formatting: `black notebook.ipynb`
  - Use `flake8` for linting
- **Notebooks**: 
  - Keep cells focused (one idea per cell)
  - Add clear markdown descriptions
  - Include comments in complex code

## Scoring Algorithm Contributions

If proposing changes to the danger scoring logic:

1. **Document the rationale:**
   - What epidemiological principle does it follow?
   - What evidence/research supports it?

2. **Validate with test cases:**
   - Show how it affects results for known scenarios
   - Compare with current scoring

3. **Get feedback:**
   - Discuss with public health professionals
   - Test with real outbreak data if possible

Example:
```python
# Before
score += 1.5 if temperature >= 30 else 0

# After: Smoother curve near optimal mosquito range (25-30°C)
score += 1.5 * min(1, (temperature - 25) / 5) if temperature >= 25 else 0

# Reasoning: WHO studies show mosquito activity peaks at 28-30°C
# This better captures sub-optimal temperatures
```

## Data Quality Standards

When contributing case data:

- [ ] Data source is cited (NEA, MOH, published study)
- [ ] Dates are clear (week of X, reported on Y)
- [ ] Numbers are accurate (double-checked)
- [ ] Area names match existing entries or are clearly new
- [ ] Clusters are estimated where not officially available

## Testing

Before submitting, ensure:

```bash
# Notebook runs end-to-end without errors
jupyter nbconvert --to notebook --execute my_notebook.ipynb

# Test with sample data
python -c "
import pandas as pd
df = pd.read_csv('dengue_cases.csv')
print(f'Loaded {len(df)} areas')
assert len(df) > 0
"
```

## Review Process

1. Maintainer reviews your PR
2. May request changes (feedback provided)
3. Once approved, merged to `main` branch
4. Your contribution is acknowledged in CONTRIBUTORS.md

## Recognition

All contributors are recognized in:
- `CONTRIBUTORS.md` file
- GitHub contributors page
- Project documentation

## Questions?

- Open an issue with tag `question`
- Or contact the maintainers directly

## Code of Conduct

Please be respectful and professional. This is a public health project — we're all here to help people stay safe.

**Respect:**
- Diverse viewpoints and expertise
- Different languages and cultures
- Different levels of technical skill
- The importance of accuracy in health data

---

**Thank you for contributing to dengue prevention!** 🦟
