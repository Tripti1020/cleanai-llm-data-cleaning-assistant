import pandas as pd
import numpy as np

# ==========================================================
# Email Cleaning
# ==========================================================

def clean_email(series):

    email_pattern = (
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    series = series.astype("string")

    mask = (
        series.notna()
        & ~series.str.match(email_pattern)
    )

    cleaned = series.copy()

    cleaned[mask] = pd.NA

    return cleaned

# ==========================================================
# Name Cleaning
# ==========================================================

def clean_name(series):

    return (
        series.astype("string")
        .str.strip()
        .str.title()
    )

# ==========================================================
# Numeric Cleaning
# ==========================================================

def clean_numeric(series):

    extracted = (
        series.astype("string")
        .str.extract(r"(-?\d+)")[0]
    )

    cleaned = pd.to_numeric(
        extracted,
        errors="coerce"
    )

    cleaned[cleaned < 0] = np.nan

    return cleaned

# ==========================================================
# Currency Cleaning
# ==========================================================

def clean_currency(series):

    cleaned = (
        series.astype("string")
        .str.replace("$", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    return pd.to_numeric(
        cleaned,
        errors="coerce"
    )

# ==========================================================
# Date Cleaning
# ==========================================================

def clean_dates(series):

    parsed = pd.to_datetime(
        series,
        errors="coerce"
    )

    return parsed.dt.strftime("%Y-%m-%d").replace(
        "NaT",
        pd.NA
    )

# ==========================================================
# Gender Cleaning
# ==========================================================

def clean_gender(series):

    mapping = {

        "m": "Male",
        "male": "Male",
        "f": "Female",
        "female": "Female"

    }

    return (
        series.astype("string")
        .str.strip()
        .str.lower()
        .replace(mapping)
        .str.title()
    )

# ==========================================================
# Country Cleaning
# ==========================================================

def clean_country(series):

    mapping = {

        "usa": "United States",
        "u.s.a": "United States",
        "united states": "United States",
        "uk": "United Kingdom",
        "united kingdom": "United Kingdom",
        "india": "India"

    }

    return (
        series.astype("string")
        .str.strip()
        .str.lower()
        .replace(mapping)
        .str.title()
    )

# ==========================================================
# Generic Category Cleaning
# ==========================================================

def clean_category(series):

    return (
        series.astype("string")
        .str.strip()
        .str.title()
    )

# ==========================================================
# Rule Registry
# ==========================================================

CLEANING_RULES = {

    "Invalid Email": clean_email,

    "Leading/Trailing Spaces": clean_name,

    "Negative Values": clean_numeric,

    "Invalid Numeric Format": clean_numeric,

    "Mixed Currency Formats": clean_currency,

    "Multiple Date Formats": clean_dates

}