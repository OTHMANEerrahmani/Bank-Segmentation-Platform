import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def perform_pca(df: pd.DataFrame) -> dict:
    """Performs PCA on the given dataframe."""
    numeric_df = df.select_dtypes(include=np.number)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_df)
    pca = PCA()
    pca_result = pca.fit_transform(scaled_data)
    eigenvalues = pca.explained_variance_
    results = {
        "pca_result": pca_result,
        "explained_variance": pca.explained_variance_ratio_,
        "cumulative_variance": np.cumsum(pca.explained_variance_ratio_),
        "components": pca.components_,
        "eigenvalues": eigenvalues,
    }
    return results