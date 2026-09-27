import pandas as pd
import re
def detect_invalid_emails(df):
    """
    Detect invalid email addresses.
    """

    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    issues = []

    for column in df.columns:

        if "email" in column.lower():

            invalid = df[
                ~df[column].fillna("").astype(str).str.match(email_pattern)
                & (df[column].notna())
            ]

            if len(invalid) > 0:

                issues.append({

                    "Column": column,

                    "Issue": "Invalid Email",

                    "Count": len(invalid),

                    "Severity": "High"

                })

    return issues
def detect_whitespace(df):
    """
    Detect leading/trailing spaces.
    """

    issues = []

    for column in df.select_dtypes(include="object"):

        count = (
            df[column]
            .fillna("")
            .astype(str)
            .str.contains(r"^\s|\s$", regex=True)
            .sum()
        )

        if count > 0:

            issues.append({

                "Column": column,

                "Issue": "Leading/Trailing Spaces",

                "Count": int(count),

                "Severity": "Medium"

            })

    return issues
def detect_negative_values(df):
    """
    Detect unexpected negative numbers.
    """

    issues = []

    for column in df.select_dtypes(include="number"):

        negatives = (df[column] < 0).sum()

        if negatives > 0:

            issues.append({

                "Column": column,

                "Issue": "Negative Values",

                "Count": int(negatives),

                "Severity": "High"

            })

    return issues
def detect_currency_formats(df):
    """
    Detect inconsistent currency symbols.
    """

    issues = []

    for column in df.select_dtypes(include="object"):

        values = df[column].fillna("").astype(str)

        has_dollar = values.str.contains(r"\$", regex=True).any()
        has_rupee = values.str.contains("₹").any()

        if has_dollar and has_rupee:

            issues.append({

                "Column": column,

                "Issue": "Mixed Currency Formats",

                "Count": int(len(values)),

                "Severity": "Medium"

            })

    return issues
def detect_date_formats(df):
    """
    Detect multiple date formats.
    """

    issues = []

    date_patterns = [

        r"\d{4}-\d{2}-\d{2}",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{2}-\d{2}-\d{4}",
        r"[A-Za-z]+ \d+ \d{4}"

    ]

    for column in df.columns:

        if "date" in column.lower():

            values = df[column].dropna().astype(str)

            matched_formats = set()

            for value in values:

                for i, pattern in enumerate(date_patterns):

                    if re.fullmatch(pattern, value):

                        matched_formats.add(i)

            if len(matched_formats) > 1:

                issues.append({

                    "Column": column,

                    "Issue": "Multiple Date Formats",

                    "Count": len(values),

                    "Severity": "Medium"

                })

    return issues
def detect_inconsistent_categories(df):
    """
    Detect inconsistent capitalization.
    """

    issues = []

    for column in df.select_dtypes(include="object"):

        values = df[column].dropna().astype(str)

        lowered = values.str.lower()

        if lowered.nunique() < values.nunique():

            issues.append({

                "Column": column,

                "Issue": "Inconsistent Categories",

                "Count": values.nunique(),

                "Severity": "Low"

            })

    return issues
def detect_all_issues(df):
    """
    Run every detector.
    """

    issues = []

    issues.extend(detect_invalid_emails(df))
    issues.extend(detect_whitespace(df))
    issues.extend(detect_negative_values(df))
    issues.extend(detect_currency_formats(df))
    issues.extend(detect_date_formats(df))
    issues.extend(detect_inconsistent_categories(df))

    return pd.DataFrame(issues)
