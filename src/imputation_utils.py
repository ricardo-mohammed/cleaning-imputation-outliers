import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.impute import SimpleImputer

def read_file(file_path):
    df = pd.read_csv(file_path)
    return df


def inspect_data(df):
    print("1. Dataset Shape:")
    print(df.shape)

    print("\n2. Column Names:")
    print(df.columns.tolist())

    print("\n3. First 10 Rows:")
    display(df.head(10))

    print("\n4. Data Types:")
    print(df.dtypes)


    print("\n5. Missing Values:")
    print(df.isnull().sum())

    print("\n6. Missing Value Percentages:")
    print((df.isnull().mean() * 100).round(2))

    print("\n7. Duplicate Rows:")
    print(df.duplicated().sum())

    print("\n8. Summary Statistics:")
    display(df.describe(include='all'))

    print("\n9. Random Sample Rows:")
    display(df.sample(min(5, len(df))))

    # Check for completely empty rows
    print("Empty rows:", df.isna().all(axis=1).sum())



def assess_missing_invalid(df, numeric_cols=None):
    print("1. Missing Values:")
    print(df.isnull().sum())

    print("\n2. Missing Value Percentages:")
    print((df.isnull().mean() * 100).round(2))

    print("\n3. Valid Observations:")
    print(df.notnull().sum())

    print("\n4. Invalid Numeric Values:")

    if numeric_cols is None:
        numeric_cols = []

    df = df.copy()

    for col in numeric_cols:
        converted = pd.to_numeric(df[col], errors="coerce")

        invalid = df[col].notna() & converted.isna()

        print(f"{col}: {invalid.sum()} invalid values")

        if invalid.any():
            print("Invalid entries:", df.loc[invalid, col].unique())

        df[col] = converted

    print("\n5. Updated Data Types:")
    print(df.dtypes)

    return df

#Adding checking and removing dublication 

def check_duplicates(df):
    # Count duplicate rows
    duplicate_count = df.duplicated().sum()

    print("1. Number of Duplicate Rows:", duplicate_count)

    # Display duplicates if found
    if duplicate_count > 0:
        print("\n2. Duplicate Records:")
        display(df[df.duplicated(keep=False)])

        # Remove duplicate rows
        df = df.drop_duplicates().reset_index(drop=True)
        print("\nDuplicates removed successfully.")
    else:
        print("\nNo duplicate rows found.")

    print("\n3. Dataset Shape:", df.shape)

    return df

#Compare Missing-Value Strategies**

def compare_missing_values(df):

    # 1. Drop rows with missing values
    df_drop_rows = df.dropna()
    print("Rows dropped:", len(df) - len(df_drop_rows))

    # 2. Drop columns with missing values
    df_drop_cols = df.dropna(axis=1)
    print("Columns dropped:", len(df.columns) - len(df_drop_cols.columns))

    # 3. Fill missing numeric values using mean
    df_mean = df.copy()

    numeric_cols = ["WEIGHT", "AGE_ESTIMATED"]

    df_mean[numeric_cols] = df_mean[numeric_cols].fillna(
    df_mean[numeric_cols].mean())

    print("\nMean Imputation:")
    print("Missing values before:", df[numeric_cols].isnull().sum().sum())
    print("Missing values after:", df_mean[numeric_cols].isnull().sum().sum())

    # 4. Fill missing numeric values using median
    df_median = df.copy()

    df_median[numeric_cols] = df_median[numeric_cols].fillna(
    df_median[numeric_cols].median())

    print("\nMedian Imputation:")
    print("Missing values before:", df[numeric_cols].isnull().sum().sum())
    print("Missing values after:", df_median[numeric_cols].isnull().sum().sum())

    # 5. Fill missing categorical values using mode
    df_mode = df.copy()

    categorical_cols = df_mode.select_dtypes(
    include=["object", "category"]).columns

    for col in categorical_cols: modes = df_mode[col].mode(dropna=True)

    if not modes.empty:
        df_mode[col] = df_mode[col].fillna(modes.iloc[0])

    print("\nMode Imputation:")
    print("Missing values before:", df[categorical_cols].isnull().sum().sum())
    print("Missing values after:", df_mode[categorical_cols].isnull().sum().sum())


    return df_drop_rows, df_drop_cols, df_mean, df_median, df_mode

# Using simpleImputer as method
def impute_missing(df, column):
    imputer = SimpleImputer(strategy='median')
    df[[column]] = imputer.fit_transform(df[[column]])
    return df

def validate_cleaning(df, df_miss):

    # 1. Compare shapes
    print("=== Shape ===")
    print("Before:", df.shape)
    print("After:", df_miss.shape)

    # 2. Compare missing values
    print("\n=== Missing Values ===")
    print("Before:\n", df.isnull().sum())
    print("After:\n", df_miss.isnull().sum())

    # 3. Compare duplicates
    print("\n=== Duplicates ===")
    print("Before:", df.duplicated().sum())
    print("After:", df_miss.duplicated().sum())

    # 4. Compare descriptive statistics
    print("\n=== Descriptive Statistics ===")
    print("Before:\n", df.describe())
    print("After:\n", df_miss.describe())

    # 5. Visualization
    before = df.isnull().sum().sum()
    after = df_miss.isnull().sum().sum()

    plt.bar(['Before', 'After'], [before, after])
    plt.title('Missing Values Before vs After Cleaning')
    plt.ylabel('Number of Missing Values')
    plt.show()