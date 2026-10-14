import pandas as pd
from IPython.display import display

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