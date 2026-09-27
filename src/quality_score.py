def calculate_quality_score(df):
    """
    Calculates a 0–100 data quality score.
    """

    score = 100

    total_cells = df.shape[0] * df.shape[1]

    missing_pct = (
        df.isnull().sum().sum() / total_cells
    ) * 100

    duplicate_pct = (
        df.duplicated().sum() / len(df)
    ) * 100

    score -= missing_pct * 0.5
    score -= duplicate_pct * 2

    score = max(0, round(score, 1))

    return score