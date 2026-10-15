# Lab 2 — Data Preprocessing and Agile Task Organization

## Project Overview

This group project applies data-preprocessing techniques to four datasets through separate notebooks covering tidying, cleaning, imputation, and outlier detection. The work includes data inspection, string manipulation, missing-value treatment, feature engineering, visualization, and Neon PostgreSQL integration.

At the end of the project, the individual notebooks completed by the team were combined into a single consolidated notebook, `lab2_all_sections.ipynb`, which brings together the full set of preprocessing work into one final submission.

The team practised Agile task classification by organizing the assignment into four areas and assigning responsibility for each area. Each member completed their assigned contribution, and the four notebooks form the combined project submission.

## Team Contributions

| Team member | Assigned task                                     | Notebook                  |
| ----------- | ------------------------------------------------- | ------------------------- |
| Ricardo     | Data tidying and reshaping                        | `tidying_reshaping.ipynb` |
| Zeyneb      | Missing-value analysis and imputation             | `imputation.ipynb`        |
| Senay       | Data cleaning and string manipulation             | `cleaning_lab.ipynb`      |
| Juan        | Anomaly/outlier detection and feature engineering | `outlier_detection.ipynb` |

The task categories provided clear ownership while allowing each member to apply the relevant techniques to an appropriate dataset. The notebooks use a shared project structure and database-access approach. Each dataset remains a separate case study with its own observations and processing decisions.

## Notebook Summaries

### Tidying and Reshaping — Ricardo

**Dataset:** WHO tuberculosis notifications, loaded from `data/who_tb.csv`.

The notebook transforms a wide dataset into a long structure using `pd.melt()`. Country and year identifiers are retained while diagnostic-code columns become observations. Rows without case counts are removed, case counts are converted to integers, and regular expressions extract diagnosis, gender, and age-group information from diagnostic codes. The resulting DataFrame is uploaded to Neon and retrieved for inspection.

**Recorded result:** 7,240 rows and 60 columns are reshaped into 76,046 non-missing case observations. The uploaded DataFrame contains nine columns after demographic extraction.

### Imputation — Zeyneb

**Dataset:** Religious and demographic survey data, loaded from `data/pew_religion.csv`.

The notebook examines missing and invalid values, converts selected numerical columns, and removes duplicate records. It compares dropping incomplete rows or columns with mean, median, and mode imputation. Histograms support the treatment of `AGE_ESTIMATED`, and a median-based `SimpleImputer` fills missing estimated ages. Database results are also explored through religious-affiliation, birth-decade, happiness, and income visualizations.

**Recorded result:** The dataset decreases from 36,918 to 36,908 records after removing ten duplicates. The estimated-age median is 48, and no missing values remain in `AGE_ESTIMATED` after imputation. Other columns still contain missing values.

### Cleaning and String Manipulation — Senay

**Dataset:** CarDekho used-car listings, loaded from `data/raw/car_details_v3.csv`.

The notebook inspects data quality, removes exact repeated records, standardizes text, and extracts manufacturers and models. String methods convert engine-capacity and power measurements into numerical features. Fuel-economy values are separated from their units so `kmpl` and `km/kg` remain distinct. Group-based medians and modes handle selected missing measurements, and flags identify imputed values. Potential price outliers are flagged and retained. The cleaned data is exported to `data/processed/cars_cleaned.csv`, uploaded to Neon, and checked against the stored row count.

**Recorded result:** 1,202 exact repeats are removed from 8,128 records, leaving 6,926 records and 36 columns. The selected derived numerical features have no remaining missing values.

### Outlier Detection and Feature Engineering — Juan

**Dataset:** UCI Bank Marketing, loaded from the semicolon-delimited `data/bank-full.csv`.

The notebook uploads the source data to Neon and reads it back for analysis. It examines `age`, `balance`, `duration`, and `campaign`, comparing Z-score detection using `|z| > 3` with the 1.5 × IQR rule. Potential outliers are retained because unusual values can represent valid customers or campaign activity. Engineered features include age groups, previous-contact indicators, total contacts, IQR flags, an outlier-flag count, and logarithmic transformations. A signed-log transformation accommodates negative balances.

**Recorded result:** All 45,211 records are preserved, and the dataset expands from 17 to 28 columns.

| Feature  | Z-score flags | IQR flags |
| -------- | ------------: | --------: |
| Age      |           381 |       487 |
| Balance  |           745 |     4,729 |
| Duration |           963 |     3,235 |
| Campaign |           840 |     3,064 |

These counts refer to flags within each feature; one record can be flagged for multiple features.

## Database Integration

Database access uses SQLAlchemy, a PostgreSQL driver, and environment variables loaded with `python-dotenv`. The shared connection class is `DatabaseManager` in `src/neon_connect.py`. The imputation notebook also uses functions from `src/imputation_utils.py` and a SQLAlchemy engine for database retrieval.

| Notebook                      | Neon table                 | Records shown in saved results |
| ----------------------------- | -------------------------- | -----------------------------: |
| Tidying and reshaping         | `tidying_who_tb`           |                         76,046 |
| Imputation                    | `pew_religion_cleaned`     |                         36,908 |
| Cleaning                      | `cardekho_clean`           |                          6,926 |
| Outlier detection — source    | `bank_marketing_raw`       |                         45,211 |
| Outlier detection — processed | `bank_marketing_processed` |                         45,211 |

The notebooks document uploads, SQL retrieval, and row-count or shape checks. Uploads using `if_exists="replace"` refresh the named tables during reruns. Database credentials are stored outside the notebooks and excluded from version control.

## Technologies and Supporting Files

- **Python, Pandas, and NumPy:** inspection, transformations, numerical calculations, and feature engineering.
- **Matplotlib and Seaborn:** distributions, comparisons, and categorical visualizations.
- **Scikit-learn:** missing-value imputation with `SimpleImputer`.
- **SQLAlchemy, PostgreSQL driver, python-dotenv, and Neon:** relational storage and database access.
- **Supporting files:** source data under `data/`, reusable modules under `src/`, and environment dependencies in `requirements.txt`.

## Interpretation and Limitations

The recorded results above come from the supplied notebooks' saved outputs. Missing-value treatment is specific to each dataset and selected feature; numerical completeness does not establish that estimated replacements are accurate. Car records with identical attributes are treated as duplicate listings, although no vehicle identifier confirms their identity. Bank-marketing outlier flags indicate statistical unusualness rather than confirmed errors.

The WHO diagnostic-code extraction currently recognizes only part of the available encoding patterns, leaving some demographic fields unmatched. Complete demographic analysis requires coverage of the remaining diagnosis and age-code formats. The survey visualizations describe the notebook's recorded counts and percentages; they are not presented as population estimates adjusted using survey weights.

## Data Sources

- **WHO tuberculosis notifications:** [WHO dataset distributed with tidyr](https://raw.githubusercontent.com/tidyverse/tidyr/master/data-raw/who.csv).
- **Religious and demographic survey:** the local `pew_religion.csv` dataset referenced in `imputation.ipynb`. https://www.pewresearch.org/dataset 2023-24-religious-landscape-study-rls-dataset/
- **CarDekho used-car listings:** [Vehicle dataset — Nehal Birla, Kaggle](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho).
- **Bank Marketing:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/222/bank+marketing).

##  AI Acknowledgement
This project was developed with the assistance of an AI language model. AI was utilized as a productivity tool for:
* **Code Scaffolding & Debugging:** Generating boilerplate code for database connections and data processing pipelines, and troubleshooting syntax or logic errors.
* **Documentation:** Drafting and refining Markdown explanations to meet software engineering documentation standards.
* **Brainstorming:** Exploring different imputation and outlier detection strategies.

All AI-generated code and suggestions were rigorously reviewed, tested, modified, and fully understood by the author(s) before inclusion in the final submission. The analytical decisions, data interpretations, and final implementations remain the sole responsibility of the student(s).
