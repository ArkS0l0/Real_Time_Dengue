# Publishing Guide: Dengue Risk Prediction Notebook

## Overview
This guide shows how to publish the Dengue Risk Prediction Notebook publicly so others can access, use, and contribute to it.

---

## Option 1: GitHub (Recommended for Collaboration)

### Why GitHub?
- Free public repository
- Version control & collaboration
- Easy sharing & forking
- GitHub displays `.ipynb` files natively in the browser
- Integrates with Binder (run notebook in cloud)

### Steps:

1. **Create a GitHub account** (if you don't have one):
   - https://github.com/signup

2. **Create a new repository**:
   - Go to https://github.com/new
   - Repository name: `dengue-risk-prediction` (or similar)
   - Description: "Real-time dengue risk scoring system with AI-powered mitigation recommendations"
   - Make it **Public**
   - Add a README: ✓
   - License: Choose GPL-3.0 or MIT (for public health use)

3. **Upload your files**:
   ```powershell
   # Initialize git locally (if not already done)
   cd "c:\Users\damia\Desktop\SL2\SL2\[Refereces] Dengue Use Case and Waste Management Use Case\Dengue Project"
   git init
   git add .
   git commit -m "Initial commit: Dengue Risk Prediction Notebook"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/dengue-risk-prediction.git
   git push -u origin main
   ```

4. **Add a Binder badge** (so others can run it in the cloud without setup):
   - Go to https://mybinder.org
   - Enter your GitHub repo URL
   - Copy the badge markdown and add to your `README.md`:
   ```markdown
   [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/YOUR_USERNAME/dengue-risk-prediction/main?filepath=notebook.ipynb)
   ```

---

## Option 2: Kaggle (Data Science Community)

### Why Kaggle?
- Large data science community
- Built-in notebook runner (no setup needed)
- Good for datasets + models
- High discoverability

### Steps:

1. **Create Kaggle account**: https://www.kaggle.com/settings/account
2. **Go to Kaggle Notebooks**: https://www.kaggle.com/code
3. **Create new notebook**:
   - Choose "Python" or "Jupyter"
   - Copy/paste your notebook code
   - Add your `dengue_cases.csv` as a dataset
4. **Make it public** and add description/tags:
   - Tags: `dengue`, `public-health`, `disease-prediction`, `singapore`
   - Enable discussions & comments

**Example URL**: `https://www.kaggle.com/your-username/dengue-risk-prediction`

---

## Option 3: NBViewer (Simple Sharing)

### Why NBViewer?
- Quick, no-setup sharing
- Good for one-off sharing
- Not editable (view-only)

### Steps:

1. Upload your `.ipynb` file to GitHub (Option 1 first)
2. Go to https://nbviewer.jupyter.org/
3. Enter your GitHub repo URL:
   ```
   https://github.com/YOUR_USERNAME/dengue-risk-prediction/blob/main/[Jupyter Notebook] Use case of Prediction Model to analyze level of danger Dengue poses to an area.ipynb
   ```
4. Share the NBViewer link (auto-generated)

---

## Option 4: Google Colab (Easy Cloud Access)

### Why Google Colab?
- Free cloud runtime (no local setup)
- Google Drive integration
- Shareable like Google Docs
- Good for teaching/demos

### Steps:

1. **Upload to Google Drive**:
   - Upload your `.ipynb` file to Google Drive
   - Right-click → "Open with" → "Google Colaboratory"

2. **Make shareable**:
   - Click "Share" button
   - Set to "Anyone with the link can view"
   - Copy link

3. **Convert notebook for Colab** (optional):
   - At the top, add a cell:
   ```python
   # Install dependencies
   !pip install -r requirements.txt
   ```

**Example URL**: `https://colab.research.google.com/drive/YOUR_FILE_ID`

---

## Option 5: Zenodo (Citable Archive)

### Why Zenodo?
- Permanent DOI (Digital Object Identifier)
- Citable in academic papers
- Good for archival
- Backed by CERN

### Steps:

1. Go to https://zenodo.org
2. Sign up with GitHub or ORCID
3. Click "New upload"
4. Upload your notebook + files
5. Add metadata:
   - Title, description, authors
   - Funding information
   - Communities (e.g., "Public Health")
6. Publish → Get DOI

**Example**: `https://doi.org/10.5281/zenodo.YOUR_ID`

---

## Option 6: Medium / Towards Data Science (Blog Post)

### Why Medium?
- Reach wider audience
- Combine code + narrative
- Good for tutorials

### Steps:

1. Export notebook as HTML or Markdown
2. Write accompanying article on https://medium.com
3. Embed or link to your GitHub repo

---

## Recommended Publishing Strategy

**For maximum impact, I recommend a multi-channel approach:**

```
GitHub (Primary)
  ↓
  ├─ Binder badge (run in cloud)
  ├─ NBViewer link (view)
  └─ Zenodo DOI (cite)
  ↓
Kaggle (Secondary - for data scientists)
  ↓
Google Colab (Tertiary - for easy access)
  ↓
Medium article (Optional - narrative + marketing)
```

---

## Pre-Publication Checklist

Before publishing, ensure:

- [ ] All cells run without errors
- [ ] Dependencies listed in `requirements.txt`:
  ```
  numpy
  pandas
  matplotlib
  requests
  ```
- [ ] `.gitignore` excludes sensitive data (API keys):
  ```
  *.pyc
  __pycache__/
  .env
  dengue_report.csv
  ```
- [ ] `README.md` is clear and complete
- [ ] Data sources cited (NEA, MOH, OpenWeatherMap)
- [ ] License clearly stated
- [ ] License file (`LICENSE`) included in repo

---

## Quick Start: Publish to GitHub Now

Run these commands in PowerShell:

```powershell
cd "c:\Users\damia\Desktop\SL2\SL2\[Refereces] Dengue Use Case and Waste Management Use Case\Dengue Project"

# Install git if needed
# https://git-scm.com/download/win

git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

git add .
git commit -m "Initial commit: Dengue Risk Prediction Notebook with real-time data integration"

# Then follow GitHub UI steps to create repo and push
```

---

## Sharing Links

Once published, you can share:

| Platform | Link Format | View/Run |
|----------|------------|----------|
| GitHub | `github.com/user/repo` | View + Fork |
| Binder | `mybinder.org/v2/gh/...` | Run in cloud |
| Kaggle | `kaggle.com/user/notebook` | View + Run |
| Colab | `colab.research.google.com/drive/...` | Edit + Run |
| Zenodo | `zenodo.org/record/...` | View + Cite |
| NBViewer | `nbviewer.org/github/...` | View |

---

## License Recommendation

For a public health tool, I recommend:
- **GPL-3.0**: Forces derivative works to stay open (strong copyleft)
- **MIT**: More permissive, easier for others to use/modify
- **CC-BY-4.0**: Good for datasets + educational content

---

## Support & Maintenance

Once public:
- Monitor issues/pull requests
- Keep dependencies updated
- Respond to user feedback
- Add "How to Contribute" guide
- Consider monthly data updates for `dengue_cases.csv`

---

Need help setting up GitHub? Let me know!
