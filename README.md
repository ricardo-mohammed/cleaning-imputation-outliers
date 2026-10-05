# Lab 2 – Tidying, Cleaning, Imputation, and Outlier Detection

## Project Summary
This project demonstrates foundational data preprocessing techniques required before machine learning model development. Using four distinct datasets (PEW Religion/Income, Billboard Rankings, Auto MPG Cars, and Pima Diabetes), this notebook practices data tidying, handling missing values through imputation, and identifying/managing outliers. The workflow emphasizes reproducible Python data processing, software engineering documentation standards, and evidence-based decision-making for data cleaning.

## Project Structure
```text
project/
├── .gitignore
── README.md
├── requirements.txt
── notebooks/
│   └── week5Lab.ipynb       # Main execution notebook
── data/
    ├── pew-raw.csv          # PEW religion and income dataset
    ├── billboard.csv        # Billboard weekly ranking dataset
    ├── cars.csv             # Auto MPG / Cars dataset
    └── diabetes.csv         # Pima Indians Diabetes dataset
```

## Setup & Installation Instructions

To replicate this project locally, ensure you have Python 3.8+ installed.

1. **Clone the repository** and navigate to the project root directory.
2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```
3. **Activate the virtual environment:**
   - *Windows:* `.venv\Scripts\activate`
   - *macOS/Linux:* `source .venv/bin/activate`
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the notebook:**
   Launch Jupyter Notebook or JupyterLab and open `notebooks/week5Lab.ipynb`. Run all cells from top to bottom.

## Replicability & Testing
*Note: A full replicability check on a secondary machine/clean environment is pending final submission. All data files are loaded using relative paths (`../data/`) to ensure the notebook executes correctly regardless of the host machine's absolute directory structure. No `!pip install` commands are hardcoded in the notebook; all dependencies are managed via `requirements.txt`.*

## Datasets Used
1. **PEW Research Center:** Religion and income survey data (Wide format requiring `melt()`).
2. **Billboard Hot 100:** Song rankings over time (Requires string manipulation and date parsing).
3. **Auto MPG (UCI):** Vehicle fuel consumption and specifications (Contains missing values encoded as `?`).
4. **Pima Indians Diabetes (UCI):** Medical diagnostic measurements (Contains invalid zero-values requiring outlier detection and imputation).

---
*Disclosure: This project was developed with the assistance of Qwen, an AI language model. AI was utilized for code scaffolding, debugging syntax errors, formatting Markdown documentation, and suggesting software engineering best practices. All analytical decisions, statistical interpretations, reflection answers, and final implementations were reviewed, validated, and authored by the student.*