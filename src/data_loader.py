import pandas as pd
from io import BytesIO

MAX_FILE_SIZE_MB = 20

SUPPORTED_ENCODINGS = [
    "utf-8",
    "utf-8-sig",
    "latin-1",
    "cp1252"
]


def detect_encoding(uploaded_file):
    """
    Try multiple encodings and return the first one that works.
    """

    raw_bytes = uploaded_file.getvalue()

    for encoding in SUPPORTED_ENCODINGS:

        try:
            raw_bytes.decode(encoding)

            return encoding

        except UnicodeDecodeError:
            continue

    return None


def load_csv(uploaded_file, skip_bad_rows=False):
    """
    Production-grade CSV loader.
    """

    if uploaded_file is None:
        return None, None, "No file uploaded."

    try:

        file_size_mb = uploaded_file.size / (1024 * 1024)

        if file_size_mb > MAX_FILE_SIZE_MB:

            return None, None, f"File exceeds {MAX_FILE_SIZE_MB} MB."

        encoding = detect_encoding(uploaded_file)

        if encoding is None:

            return None, None, "Could not detect file encoding."

        raw_data = uploaded_file.getvalue()

        df = pd.read_csv(

            BytesIO(raw_data),

            encoding=encoding,

            on_bad_lines="skip" if skip_bad_rows else "error"

        )

        if df.empty:

            return None, encoding, "CSV contains no data."

        return df, encoding, None

    except pd.errors.ParserError as e:

        return None, encoding, f"CSV formatting error:\n{str(e)}"

    except Exception as e:

        return None, encoding, str(e)


def get_file_info(uploaded_file, df):

    return {

        "filename": uploaded_file.name,

        "size_mb": round(uploaded_file.size / (1024 * 1024), 2),

        "rows": df.shape[0],

        "columns": df.shape[1],

        "memory_mb": round(

            df.memory_usage(deep=True).sum()

            / (1024 * 1024),

            2

        )

    }


def create_import_summary(df):

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "missing_cells": int(df.isnull().sum().sum()),

        "duplicate_rows": int(df.duplicated().sum())

    }