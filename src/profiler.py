import pandas as pd


def generate_profile(df):
    """
    Creates a complete dataset profile.
    """

    profile = {}

    profile["rows"] = len(df)
    profile["columns"] = len(df.columns)

    profile["missing_cells"] = int(df.isnull().sum().sum())
    profile["duplicate_rows"] = int(df.duplicated().sum())

    profile["numeric_columns"] = df.select_dtypes(include="number").columns.tolist()
    profile["categorical_columns"] = df.select_dtypes(include="object").columns.tolist()

    profile["memory_mb"] = round(
        df.memory_usage(deep=True).sum() / (1024 * 1024),
        2
    )

    return profile


def column_health(df):
    """
    Creates health information for every column.
    """

    health = []

    for column in df.columns:

        health.append({

            "Column": column,

            "Data Type": str(df[column].dtype),

            "Missing": int(df[column].isnull().sum()),

            "Missing %": round(
                df[column].isnull().sum()/len(df)*100,
                2
            ),

            "Unique": int(df[column].nunique())

        })

    return pd.DataFrame(health)


def numeric_summary(df):
    """
    Summary for numeric columns.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    return numeric_df.describe().round(2)


def categorical_summary(df):
    """
    Summary for text columns.
    """

    results = []

    for col in df.select_dtypes(include="object").columns:

        results.append({

            "Column": col,

            "Unique Values": df[col].nunique(),

            "Most Frequent": df[col].mode().iloc[0] if not df[col].mode().empty else None,

            "Frequency": df[col].value_counts(dropna=False).iloc[0]

        })

    return pd.DataFrame(results)


def missing_summary(df):
    """
    Missing value summary.
    """

    return pd.DataFrame({

        "Column": df.columns,

        "Missing": df.isnull().sum().values,

        "Percentage": (
            df.isnull().sum()/len(df)*100
        ).round(2).values

    }).sort_values("Missing", ascending=False)

def detect_outliers(df):
    """
    Detects outliers using the IQR method.
    """

    outlier_data = []

    numeric_df = df.select_dtypes(include="number")

    for column in numeric_df.columns:

        q1 = numeric_df[column].quantile(0.25)
        q3 = numeric_df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = numeric_df[
            (numeric_df[column] < lower) |
            (numeric_df[column] > upper)
        ]

        outlier_data.append({

            "Column": column,

            "Outliers": len(outliers)

        })

    return pd.DataFrame(outlier_data)