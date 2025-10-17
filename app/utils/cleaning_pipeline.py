import pandas as pd
import numpy as np
from scipy import stats
import datetime


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str], dict[str, int]]:
    """4-step iterative process for cleaning bank customer data."""
    log = []
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.append(f"[{now}] Starting data cleaning process.")
    initial_rows = len(df)
    df_clean = df.copy()
    missing_before = df_clean.isnull().sum()
    total_missing = int(missing_before.sum())
    log.append(
        f"CONTROL: Detected {total_missing} missing values across {len(missing_before[missing_before > 0])} columns."
    )
    numeric_cols = df_clean.select_dtypes(include=np.number).columns.tolist()
    outliers_detected_total = 0
    for col in numeric_cols:
        if missing_before[col] > 0:
            median_val = df_clean[col].median()
            df_clean[col].fillna(median_val, inplace=True)
            log.append(
                f"TREAT: Filled {missing_before[col]} missing values in '{col}' with median ({median_val:.2f})."
            )
        z_scores = np.abs(stats.zscore(df_clean[col]))
        outliers_mask = z_scores > 3
        num_outliers = outliers_mask.sum()
        if num_outliers > 0:
            outliers_detected_total += num_outliers
            mean = df_clean[col].mean()
            std = df_clean[col].std()
            upper_bound = mean + 3 * std
            lower_bound = mean - 3 * std
            df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
            log.append(
                f"TREAT: Capped {num_outliers} outliers in '{col}' at 3 standard deviations."
            )
    df_clean.drop_duplicates(inplace=True)
    duplicates_removed = initial_rows - len(df_clean)
    if duplicates_removed > 0:
        log.append(f"TREAT: Removed {duplicates_removed} duplicate rows.")
    final_rows = len(df_clean)
    log.append(f"REPORT: Data cleaning finished. Final dataset has {final_rows} rows.")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.append(f"[{now}] Cleaning process complete.")
    summary = {
        "total_rows": final_rows,
        "missing_values": total_missing,
        "outliers_detected": int(outliers_detected_total),
        "duplicates_removed": duplicates_removed,
    }
    return (df_clean, log, summary)