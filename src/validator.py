"""
CleanAI - Dataset Validator

Validates a loaded pandas DataFrame before it enters
the profiling, issue detection, AI analysis and cleaning pipeline.
"""

import pandas as pd


# ==========================================================
# Basic Dataset Validation
# ==========================================================

def validate_dataset(df):
    """
    Perform a complete validation of the uploaded dataset.

    Returns
    -------
    dict
        {
            "valid": bool,
            "errors": list,
            "warnings": list,
            "info": list
        }
    """

    errors = []
    warnings = []
    info = []

    # ------------------------------------------------------
    # 1. Check object type
    # ------------------------------------------------------

    if not isinstance(df, pd.DataFrame):

        errors.append(
            "The uploaded data could not be loaded as a pandas DataFrame."
        )

        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings,
            "info": info
        }

    # ------------------------------------------------------
    # 2. Check empty dataset
    # ------------------------------------------------------

    if df.empty:

        errors.append(
            "The dataset is empty. Please upload a CSV containing data."
        )

    # ------------------------------------------------------
    # 3. Check rows
    # ------------------------------------------------------

    if len(df) == 0:

        errors.append(
            "The dataset contains no rows."
        )

    # ------------------------------------------------------
    # 4. Check columns
    # ------------------------------------------------------

    if len(df.columns) == 0:

        errors.append(
            "The dataset contains no columns."
        )

    # ------------------------------------------------------
    # 5. Check completely empty columns
    # ------------------------------------------------------

    if not df.empty:

        empty_columns = [
            column
            for column in df.columns
            if df[column].isna().all()
        ]

        if empty_columns:

            warnings.append(
                "Completely empty columns detected: "
                + ", ".join(map(str, empty_columns))
            )

    # ------------------------------------------------------
    # 6. Check duplicate column names
    # ------------------------------------------------------

    duplicated_columns = df.columns[
        df.columns.duplicated()
    ].tolist()

    if duplicated_columns:

        errors.append(
            "Duplicate column names detected: "
            + ", ".join(map(str, duplicated_columns))
        )

    # ------------------------------------------------------
    # 7. Check unnamed columns
    # ------------------------------------------------------

    unnamed_columns = [
        column
        for column in df.columns
        if str(column).strip().lower().startswith("unnamed")
    ]

    if unnamed_columns:

        warnings.append(
            "Unnamed columns detected: "
            + ", ".join(map(str, unnamed_columns))
        )

    # ------------------------------------------------------
    # 8. Check missing values
    # ------------------------------------------------------

    if not df.empty:

        total_missing = int(
            df.isna().sum().sum()
        )

        if total_missing > 0:

            missing_percentage = (
                total_missing /
                (df.shape[0] * df.shape[1])
            ) * 100

            warnings.append(
                f"{total_missing:,} missing cells detected "
                f"({missing_percentage:.2f}% of the dataset)."
            )

        else:

            info.append(
                "No missing values detected."
            )

    # ------------------------------------------------------
    # 9. Check duplicate rows
    # ------------------------------------------------------

    if not df.empty:

        duplicate_rows = int(
            df.duplicated().sum()
        )

        if duplicate_rows > 0:

            warnings.append(
                f"{duplicate_rows:,} duplicate rows detected."
            )

        else:

            info.append(
                "No duplicate rows detected."
            )

    # ------------------------------------------------------
    # 10. Check columns containing only one value
    # ------------------------------------------------------

    if not df.empty:

        constant_columns = [
            column
            for column in df.columns
            if df[column].nunique(dropna=True) <= 1
        ]

        if constant_columns:

            warnings.append(
                "Columns containing only one unique value: "
                + ", ".join(map(str, constant_columns))
            )

    # ------------------------------------------------------
    # 11. Check column names
    # ------------------------------------------------------

    blank_column_names = [
        column
        for column in df.columns
        if str(column).strip() == ""
    ]

    if blank_column_names:

        errors.append(
            "One or more columns have blank names."
        )

    # ------------------------------------------------------
    # 12. Dataset information
    # ------------------------------------------------------

    if not df.empty:

        info.append(
            f"Dataset contains {df.shape[0]:,} rows "
            f"and {df.shape[1]:,} columns."
        )

        numeric_columns = len(
            df.select_dtypes(include="number").columns
        )

        text_columns = len(
            df.select_dtypes(include=["object", "string"]).columns
        )

        info.append(
            f"Detected {numeric_columns} numeric "
            f"and {text_columns} text columns."
        )

    # ------------------------------------------------------
    # 13. Final validation status
    # ------------------------------------------------------

    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "info": info
    }


# ==========================================================
# Validation Summary
# ==========================================================

def get_validation_summary(validation_result):
    """
    Create a compact summary of validation results.
    """

    if validation_result["valid"]:

        if validation_result["warnings"]:

            return "Dataset passed validation with warnings."

        return "Dataset passed all validation checks."

    return "Dataset failed validation. Please resolve the errors."


# ==========================================================
# Validation Status
# ==========================================================

def is_valid_dataset(df):
    """
    Return True if the dataset passes validation.
    """

    result = validate_dataset(df)

    return result["valid"]