import pandas as pd
import numpy as np


def execute_cleaning_plan(df, selected_actions):
    """
    Execute approved cleaning actions using vectorized Pandas operations.

    Returns:
        cleaned_df
        cleaning_log (row-level audit log)
    """

    cleaned_df = df.copy()
    original_df = df.copy()

    # ==========================================================
    # Normalize Missing Values
    # ==========================================================

    cleaned_df = cleaned_df.replace(
        ["None", "none", "NULL", "null", "", "nan", "NaN"],
        pd.NA
    )

    # ==========================================================
    # Execute Selected Cleaning Actions
    # ==========================================================

    for action in selected_actions:

        column = action["column"]
        issue = action["issue"]

        if column not in cleaned_df.columns:
            continue

        # ------------------------------------------------------
        # Invalid Email
        # ------------------------------------------------------

        if issue == "Invalid Email":

            cleaned_df[column] = cleaned_df[column].astype("string")

            email_pattern = (
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
            )

            invalid_mask = (
                cleaned_df[column].notna()
                & ~cleaned_df[column].str.match(email_pattern)
            )

            cleaned_df.loc[invalid_mask, column] = pd.NA

        # ------------------------------------------------------
        # Leading/Trailing Spaces
        # ------------------------------------------------------

        elif issue == "Leading/Trailing Spaces":

            cleaned_df[column] = (
                cleaned_df[column]
                .astype("string")
                .str.strip()
            )

            if "name" in column.lower():

                cleaned_df[column] = (
                    cleaned_df[column]
                    .str.title()
                )

        # ------------------------------------------------------
        # Negative Values / Age Cleaning
        # ------------------------------------------------------

        elif issue == "Negative Values":

            extracted = (
                cleaned_df[column]
                .astype("string")
                .str.extract(r"(-?\d+)")[0]
            )

            cleaned_df[column] = pd.to_numeric(
                extracted,
                errors="coerce"
            )

            cleaned_df.loc[
                cleaned_df[column] < 0,
                column
            ] = np.nan

        # ------------------------------------------------------
        # Mixed Currency Formats
        # ------------------------------------------------------

        elif issue == "Mixed Currency Formats":

            cleaned_df[column] = (
                cleaned_df[column]
                .astype("string")
                .str.replace("$", "", regex=False)
                .str.replace("₹", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
            )

            cleaned_df[column] = pd.to_numeric(
                cleaned_df[column],
                errors="coerce"
            )

        # ------------------------------------------------------
        # Date Standardization
        # ------------------------------------------------------

        elif issue == "Multiple Date Formats":

            # Convert values to string while preserving missing values
            date_series = cleaned_df[column].astype("string")

            # First parse normally (correct for ISO: YYYY-MM-DD)
            parsed_dates = pd.to_datetime(
                date_series,
                errors="coerce"
            )

            # Retry only the failed values using dayfirst=True
            failed_mask = parsed_dates.isna() & date_series.notna()

            if failed_mask.any():

                parsed_dates.loc[failed_mask] = pd.to_datetime(
                    date_series.loc[failed_mask],
                    errors="coerce",
                    dayfirst=True
                )

            # Store in a consistent format
            cleaned_df[column] = (
                parsed_dates
                .dt.strftime("%Y-%m-%d")
                .replace("NaT", pd.NA)
            )

        # ------------------------------------------------------
        # Category Standardization
        # ------------------------------------------------------

        elif issue == "Inconsistent Categories":

            cleaned_df[column] = (
                cleaned_df[column]
                .astype("string")
                .str.strip()
            )

            if "gender" in column.lower():

                gender_map = {
                    "m": "Male",
                    "male": "Male",
                    "f": "Female",
                    "female": "Female"
                }

                cleaned_df[column] = (
                    cleaned_df[column]
                    .str.lower()
                    .replace(gender_map)
                    .str.title()
                )

            elif "country" in column.lower():

                country_map = {
                    "usa": "United States",
                    "u.s.a": "United States",
                    "united states": "United States",
                    "uk": "United Kingdom",
                    "united kingdom": "United Kingdom",
                    "india": "India"
                }

                cleaned_df[column] = (
                    cleaned_df[column]
                    .str.lower()
                    .replace(country_map)
                    .str.title()
                )

            else:

                cleaned_df[column] = (
                    cleaned_df[column]
                    .str.title()
                )

    # ==========================================================
    # Remove Duplicate Customers
    # ==========================================================

    duplicate_removed = 0

    if "Customer_ID" in cleaned_df.columns:

        before = len(cleaned_df)

        cleaned_df = cleaned_df.drop_duplicates(
            subset=["Customer_ID"],
            keep="first"
        )

        duplicate_removed = before - len(cleaned_df)

    else:

        before = len(cleaned_df)

        cleaned_df = cleaned_df.drop_duplicates()

        duplicate_removed = before - len(cleaned_df)

    # ==========================================================
    # Build Row-Level Cleaning Log
    # ==========================================================

    cleaning_log = []

    common_rows = min(len(original_df), len(cleaned_df))

    for row in range(common_rows):

        for column in cleaned_df.columns:

            old = original_df.iloc[row][column]
            new = cleaned_df.iloc[row][column]

            old_missing = pd.isna(old)
            new_missing = pd.isna(new)

            if old_missing and new_missing:
                continue

            if str(old) != str(new):

                cleaning_log.append(
                    f"Row {row + 1}: {column}: '{old}' → '{new}'"
                )

    if duplicate_removed:

        cleaning_log.append(
            f"Removed {duplicate_removed} duplicate customer(s)."
        )

    # ==========================================================
    # Final Cleanup & Optimize Data Types
    # ==========================================================

    cleaned_df = cleaned_df.replace(
        ["None", "none", "NULL", "null", "", "nan", "NaN"],
        pd.NA
    )

    cleaned_df = cleaned_df.convert_dtypes()    

    return cleaned_df, cleaning_log