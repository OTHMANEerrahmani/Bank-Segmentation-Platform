import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
from typing import Any

def perform_hierarchical_clustering(pca_df: pd.DataFrame, k: int) -> np.ndarray:
    """Runs hierarchical clustering with a specified number of clusters."""
    hierarchical = AgglomerativeClustering(n_clusters=int(k), linkage="ward")
    clusters = hierarchical.fit_predict(pca_df)
    return clusters


def compute_dendrogram_data(pca_df: pd.DataFrame) -> dict:
    """Computes linkage matrix and dendrogram data for hierarchical clustering."""
    # Use a sample of data for dendrogram to avoid performance issues
    sample_size = min(50, len(pca_df))  # Reduced for better visualization
    if len(pca_df) > sample_size:
        sample_indices = np.random.choice(len(pca_df), sample_size, replace=False)
        sample_data = pca_df.iloc[sample_indices]
    else:
        sample_data = pca_df
    
    # Compute linkage matrix
    linkage_matrix = linkage(sample_data, method='ward')
    
    # Compute dendrogram data
    dendro_data = dendrogram(linkage_matrix, no_plot=True, count_sort=True)
    
    # Create simplified visualization data
    n_leaves = len(dendro_data['leaves'])
    max_distance = max(dendro_data['dcoord'][0]) if dendro_data['dcoord'] else 1
    
    # Create tree structure for visualization
    tree_structure = create_tree_structure(linkage_matrix, n_leaves)
    
    return {
        "linkage_matrix": linkage_matrix.tolist(),
        "dendro_data": {
            "leaves": dendro_data['leaves'],
            "ivl": dendro_data['ivl'],
            "color_list": dendro_data['color_list'],
            "dcoord": dendro_data['dcoord'],
            "icoord": dendro_data['icoord']
        },
        "tree_structure": tree_structure,
        "n_leaves": n_leaves,
        "max_distance": float(max_distance)
    }


def create_tree_structure(linkage_matrix, n_leaves):
    """Create a simplified tree structure for visualization."""
    tree = []
    node_id = n_leaves
    
    for i, (left, right, distance, count) in enumerate(linkage_matrix):
        tree.append({
            "id": int(node_id),
            "left": int(left),
            "right": int(right),
            "distance": float(distance),
            "count": int(count),
            "level": i
        })
        node_id += 1
    
    return tree


def compute_elbow_data(pca_df: pd.DataFrame) -> list[dict[str, str | int | float]]:
    """Calculates inertia and silhouette scores for k=2 to k=10."""
    elbow_data = []
    K_range = range(2, 11)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(pca_df)
        inertia = kmeans.inertia_
        silhouette = silhouette_score(pca_df, kmeans.labels_)
        elbow_data.append(
            {"k": k, "inertia": float(inertia), "silhouette": float(silhouette)}
        )
    return elbow_data


def perform_clustering(pca_df: pd.DataFrame, k: int) -> np.ndarray:
    """Runs K-Means clustering with a specified number of clusters."""
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(pca_df)
    return clusters


def find_column(df: pd.DataFrame, variations: list[str]) -> str:
    """Find the first matching column name from a list of variations with robust, multi-level matching."""
    import re

    def normalize_key(key: str) -> str:
        """Lowercase, strip, and remove non-alphanumeric characters for robust matching."""
        return re.sub("[^a-z0-9]", "", key.lower().strip())

    df_columns_normalized = {normalize_key(col): col for col in df.columns}
    normalized_variations = [normalize_key(var) for var in variations]
    for norm_var in normalized_variations:
        if norm_var in df_columns_normalized:
            return df_columns_normalized[norm_var]
    for norm_col, original_col in df_columns_normalized.items():
        for norm_var in normalized_variations:
            if norm_var in norm_col:
                return original_col
    raise KeyError(
        f"None of the expected column variations found for: {variations}. Available columns in the dataframe are: {df.columns.tolist()}"
    )


def generate_cluster_profiles(
    original_df: pd.DataFrame, clusters: np.ndarray
) -> list[dict[str, str | int | float]]:
    """Computes mean statistics for each cluster using flexible column matching."""
    profiled_df = original_df.copy()
    if len(profiled_df) != len(clusters):
        raise ValueError(
            f"Shape mismatch: The original data has {len(profiled_df)} rows, but the clustering result has {len(clusters)} entries."
        )
    profiled_df["cluster"] = clusters
    column_mappings = {
        "income": ["Monthly Income (€)", "Monthly Income", "Income", "monthly_income" ],
        "savings": [
            "Savings Amount (€)",
            "Savings Amount",
            "Savings",
            "savings_amount",
        ],
        "credit": ["Credit Balance (€)", "Credit Balance", "Credit", "credit_balance"],
        "spending": [
            "Monthly Card Spending (€)",
            "Monthly Card Spending",
            "Card Spending",
            "Spending",
            "monthly_card_spending",
        ],
        "age": ["Age", "age"],
        "seniority": [
            "Bank Seniority (years)",
            "Bank Seniority",
            "Seniority",
            "bank_seniority",
            "Years",
        ],
    }
    try:
        income_col = find_column(profiled_df, column_mappings["income"])
        savings_col = find_column(profiled_df, column_mappings["savings"])
        credit_col = find_column(profiled_df, column_mappings["credit"])
        spending_col = find_column(profiled_df, column_mappings["spending"])
        age_col = find_column(profiled_df, column_mappings["age"])
        seniority_col = find_column(profiled_df, column_mappings["seniority"])
    except (KeyError, ValueError) as e:
        import logging

        logging.exception(f"Column not found during profiling setup. Details: {e}")
        raise ValueError(
            f"A required column for profiling is missing. Please check your CSV. Details: {e}"
        )
    profile_data = []
    for cluster_id in sorted(np.unique(clusters)):
        cluster_subset = profiled_df[profiled_df["cluster"] == cluster_id]
        profile = {
            "cluster_id": int(cluster_id),
            "size": int(len(cluster_subset)),
            "avg_income": f"{float(cluster_subset[income_col].mean()):.2f}",
            "avg_savings": f"{float(cluster_subset[savings_col].mean()):.2f}",
            "avg_credit": f"{float(cluster_subset[credit_col].mean()):.2f}",
            "avg_spend": f"{float(cluster_subset[spending_col].mean()):.2f}",
            "avg_age": f"{float(cluster_subset[age_col].mean()):.0f}",
            "avg_seniority": f"{float(cluster_subset[seniority_col].mean()):.0f}",
        }
        profile_data.append(profile)
    return profile_data