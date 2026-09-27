import pandas as pd

# Maximum upload size
MAX_FILE_SIZE_MB = 20


def load_csv(uploaded_file):
    """
    Safely loads a CSV file.
    Returns:
        DataFrame, Error Message
    """

    if uploaded_file is None:
        return None, "No file uploaded."

    try:
        file_size_mb = uploaded_file.size / (1024 * 1024)

        if file_size_mb > MAX_FILE_SIZE_MB:
            return None, f"File exceeds {MAX_FILE_SIZE_MB} MB limit."

        df = pd.read_csv(uploaded_file)

        if df.empty:
            return None, "Uploaded CSV is empty."

        return df, None

    except UnicodeDecodeError:
        return None, "Encoding error. Please use UTF-8."

    except pd.errors.ParserError as e:
        return None, f"CSV formatting error: {str(e)}"

    except Exception as e:
        return None, str(e)


def get_file_info(uploaded_file, df):
    """
    Returns useful file metadata.
    """

    return {
        "filename": uploaded_file.name,
        "size_mb": round(uploaded_file.size / (1024 * 1024), 2),
        "rows": df.shape[0],
        "columns": df.shape[1],
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
    }